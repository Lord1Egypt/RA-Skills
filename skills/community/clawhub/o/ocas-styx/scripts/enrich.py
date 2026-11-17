#!/usr/bin/env python3
"""Styx enrichment pipeline — resolves garbled transaction names into real businesses.

Stages:
  1. Exact match against known merchants
  2. Fuzzy match against known merchants
  3. SearXNG search
  4. LLM resolution
  5. Manual review queue for low-confidence matches
"""

import json
import os
import re
import sqlite3
import sys
import urllib.error
import urllib.request
from difflib import SequenceMatcher

sys.path.insert(0, __import__('os').path.dirname(__file__))
from styx_common import (
    CATEGORY_MAP,
    get_or_create_merchant,
    init_styx_db,
    is_redacted,
    link_transaction,
    normalize,
)

STYX_DB = '~/.hermes/data/styx.db'
TXN_DB = '~/.hermes/data/transactions.db'
REVIEW_QUEUE = '~/.hermes/data/styx/review_queue.jsonl'
NAME_MAPPINGS = '~/.hermes/data/styx/name_mappings.json'

# ── Name cleaning ────────────────────────────────────────────────────────────

PREFIX_PATTERNS = [
    r'^ABM-',
    r'^TCB\*',
    r'^MED\*',
    r'^FSP\*',
    r'^ABC\*',
    r'^TST\*',
    r'^DD\s+\*DOORDASH\s+',
    r'^DD\s+\*',
    r'^POSH\*',
    r'^AMZN',
    r'^TGT\*',
    r'^TGT\s+',
    r'^WMT\*',
    r'^WMT\s+',
    r'^COSTCO\s+',
    r'^SAFEWAY\s+',
    r'^TRADER\s+JOE',
    r'^WHOLE\s+FOODS\s+',
    r'^UBER\s+\*',
    r'^LYFT\s+\*',
]

REDACTED_PATTERNS = [
    r'\*{3,}',           # 3+ asterisks = redacted
    r'\*{2,}\d+',        # **digits pattern
]

def clean_name(name):
    """Strip known prefixes and normalize a transaction name."""
    if not name:
        return ''
    cleaned = name.strip()
    for pat in PREFIX_PATTERNS:
        cleaned = re.sub(pat, '', cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip()
    return cleaned

def extract_base_name(name):
    """Extract the recognizable base from a redacted name like 'UNITED **************'."""
    if not name:
        return ''
    # Take the part before the asterisks
    parts = re.split(r'\*+', name)
    base = parts[0].strip() if parts else ''
    return base

# ── Stage 1: Exact match ────────────────────────────────────────────────────

def stage_exact_match(conn, raw_name, merchant_name):
    """Check if the name directly matches a known merchant."""
    candidates = []
    for name in [merchant_name, raw_name]:
        if not name:
            continue
        norm = normalize(name)
        row = conn.execute(
            'SELECT id, name, category, confidence FROM merchants WHERE normalized_name = ?',
            (norm,)
        ).fetchone()
        if row:
            candidates.append((row[0], row[1], row[2], row[3], 'exact'))
    return candidates

# ── Stage 2: Fuzzy match ────────────────────────────────────────────────────

def stage_fuzzy_match(conn, cleaned_name):
    """Fuzzy match cleaned name against known merchants."""
    if not cleaned_name or len(cleaned_name) < 3:
        return []
    norm = normalize(cleaned_name)
    merchants = conn.execute(
        'SELECT id, name, normalized_name, category FROM merchants'
    ).fetchall()
    matches = []
    for mid, mname, mnorm, mcat in merchants:
        score = SequenceMatcher(None, norm, mnorm).ratio()
        if score > 0.85:
            matches.append((mid, mname, mcat, score, 'fuzzy'))
    matches.sort(key=lambda x: x[3], reverse=True)
    return matches[:3]

# ── Stage 3: SearXNG search ─────────────────────────────────────────────────

def get_searxng_url():
    """Get SearXNG URL from environment or default."""
    return os.environ.get('SEARXNG_URL', 'http://localhost:8888')

def searxng_search(query, num_results=5):
    """Search via SearXNG."""
    url = get_searxng_url()
    params = urllib.parse.urlencode({
        'q': query,
        'format': 'json',
        'language': 'en',
        'categories': 'general,map',
        'pageno': 1,
    })
    try:
        req = urllib.request.Request(f'{url}/search?{params}')
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data.get('results', [])[:num_results]
    except Exception as e:
        print(f"  SearXNG error: {e}", file=sys.stderr)
        return []

def stage_search(conn, cleaned_name, category_hint=None):
    """Search for the business via SearXNG."""
    if not cleaned_name or len(cleaned_name) < 3:
        return None

    query = f"{cleaned_name} San Francisco business"
    if category_hint:
        query = f"{cleaned_name} {category_hint} San Francisco"

    results = searxng_search(query)
    if not results:
        return None

    # Look for a clear business match in results
    for r in results:
        title = r.get('title', '')
        content = r.get('content', '')
        url = r.get('url', '')

        # Skip results that are obviously not about the business
        if any(skip in title.lower() for skip in ['wikipedia', 'yelp', 'tripadvisor']):
            continue

        # If the cleaned name appears in the title, likely a match
        if normalize(cleaned_name) in normalize(title):
            return {
                'name': cleaned_name,
                'source': 'searxng',
                'confidence': 0.8,
                'url': url,
                'snippet': content[:200] if content else '',
            }

    # Use the first result as a guess
    if results:
        r = results[0]
        return {
            'name': cleaned_name,
            'source': 'searxng_guess',
            'confidence': 0.6,
            'url': r.get('url', ''),
            'snippet': r.get('content', '')[:200],
        }

    return None

# ── Stage 4: LLM resolution ─────────────────────────────────────────────────

def stage_llm_resolve(raw_name, cleaned_name, amount, category, personal_finance_category):
    """Use LLM to identify a business from transaction details.

    This is a fallback for transactions that couldn't be resolved by
    exact/fuzzy/search matching. We build a prompt and return the
    LLM's best guess.
    """
    # We'll build the prompt and return it for the caller to execute
    # (since we can't call the LLM directly from within this script easily)
    prompt = f"""Given this bank transaction, identify the most likely real business name.

Transaction name (raw): {raw_name}
Cleaned name: {cleaned_name}
Amount: ${amount}
Category: {category}
Personal finance category: {personal_finance_category}

Rules:
- If the name is too redacted or garbled to identify, respond with "UNKNOWN"
- If you can identify the business, respond with just the business name
- Do not include explanations, just the business name or UNKNOWN
- Consider that this is in San Francisco

Business name:"""

    return prompt

# ── Main enrichment ──────────────────────────────────────────────────────────

def enrich_transactions(dry_run=False, use_llm=True):
    """Run the full enrichment pipeline on all unenriched transactions."""
    styx_conn = init_styx_db(STYX_DB)
    txn_conn = sqlite3.connect(TXN_DB)

    # Start enrichment run
    if not dry_run:
        styx_conn.execute(
            'INSERT INTO enrichment_runs (started_at, status) VALUES (datetime("now"), "running")'
        )
        styx_conn.commit()
        run_id = styx_conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    else:
        run_id = 0

    # Get all transactions that don't have a merchant link
    # We need to attach the transactions.db to query it
    styx_conn.execute(f'ATTACH DATABASE "{TXN_DB}" AS txndb')

    unresolved = styx_conn.execute('''
        SELECT t.transaction_id, t.name, t.merchant_name, t.amount, t.date,
               t.category, t.personal_finance_category
        FROM txndb.transactions t
        LEFT JOIN transaction_merchants tm ON t.transaction_id = tm.transaction_id
        WHERE tm.id IS NULL
        ORDER BY t.date DESC
    ''').fetchall()

    total = len(unresolved)
    print(f"Enriching {total} transactions...")
    print(f"{'='*60}")

    stats = {
        'exact': 0, 'fuzzy': 0, 'search': 0, 'llm': 0, 'review': 0, 'skipped': 0,
        'merchants_created': 0, 'merchants_found': 0,
    }
    llm_queue = []  # transactions needing LLM resolution
    review_items = []

    for i, (txn_id, name, merchant_name, amount, date, category, pfc) in enumerate(unresolved):
        if (i + 1) % 50 == 0:
            print(f"  Progress: {i+1}/{total}")

        raw_name = name or merchant_name or ''
        if not raw_name:
            stats['skipped'] += 1
            continue

        # Skip fully redacted names
        if is_redacted(raw_name) and not extract_base_name(raw_name):
            stats['skipped'] += 1
            continue

        cat = CATEGORY_MAP.get(pfc, 'other')

        # ── Stage 1: Exact match ──
        candidates = stage_exact_match(styx_conn, raw_name, merchant_name)
        if candidates:
            mid, mname, mcat, mconf, method = candidates[0]
            if not dry_run:
                link_transaction(styx_conn, txn_id, mid, raw_name, 'exact', 1.0)
            stats['exact'] += 1
            stats['merchants_found'] += 1
            continue

        # ── Clean the name ──
        cleaned = clean_name(raw_name)
        base = extract_base_name(raw_name) if is_redacted(raw_name) else ''
        search_name = cleaned or base

        if not search_name or len(search_name) < 2:
            stats['skipped'] += 1
            continue

        # ── Stage 2: Fuzzy match ──
        fuzzy = stage_fuzzy_match(styx_conn, search_name)
        if fuzzy:
            mid, mname, mcat, score, method = fuzzy[0]
            if not dry_run:
                link_transaction(styx_conn, txn_id, mid, raw_name, 'fuzzy', score)
            stats['fuzzy'] += 1
            stats['merchants_found'] += 1
            continue

        # ── Stage 3: SearXNG search ──
        search_result = stage_search(styx_conn, search_name, cat)
        if search_result and search_result['confidence'] >= 0.6:
            if not dry_run:
                mid, created = get_or_create_merchant(
                    styx_conn, search_result['name'],
                    category=cat, source='searxng',
                    confidence=search_result['confidence']
                )
                link_transaction(styx_conn, txn_id, mid, raw_name, 'search', search_result['confidence'])
                if created:
                    stats['merchants_created'] += 1
            stats['search'] += 1
            stats['merchants_found'] += 1
            continue

        # ── Stage 4: Queue for LLM ──
        if use_llm:
            prompt = stage_llm_resolve(raw_name, search_name, amount, category, pfc)
            llm_queue.append({
                'transaction_id': txn_id,
                'raw_name': raw_name,
                'cleaned_name': search_name,
                'amount': amount,
                'date': date,
                'category': category,
                'personal_finance_category': pfc,
                'prompt': prompt,
            })
        else:
            # Queue for manual review
            review_items.append({
                'transaction_id': txn_id,
                'raw_name': raw_name,
                'cleaned_name': search_name,
                'amount': amount,
                'date': date,
                'personal_finance_category': pfc,
            })
            stats['review'] += 1

    # ── Stage 4: LLM resolution (batch) ──
    if llm_queue and use_llm and not dry_run:
        print(f"\nResolving {len(llm_queue)} transactions via LLM...")
        # Write prompts to a file for batch processing
        llm_file = '/tmp/styx_llm_queue.jsonl'
        with open(llm_file, 'w') as f:
            f.writelines(json.dumps(item) + '\n' for item in llm_queue)
        print(f"  Wrote {len(llm_queue)} prompts to {llm_file}")
        print("  Run: python3 ~/.hermes/skills/ocas-styx/scripts/llm_resolve.py")
        stats['llm'] = len(llm_queue)

    # Write review queue
    if review_items and not dry_run:
        os.makedirs(os.path.dirname(REVIEW_QUEUE), exist_ok=True)
        with open(REVIEW_QUEUE, 'a') as f:
            f.writelines(json.dumps(item) + '\n' for item in review_items)

    if not dry_run:
        styx_conn.commit()
        styx_conn.execute('''
            UPDATE enrichment_runs SET
                completed_at = datetime("now"),
                transactions_processed = ?,
                merchants_found = ?,
                merchants_created = ?,
                status = 'completed'
            WHERE id = ?
        ''', (total, stats['merchants_found'], stats['merchants_created'], run_id))
        styx_conn.commit()

    styx_conn.close()
    txn_conn.close()

    print(f"\n{'='*60}")
    print(f"Enrichment complete ({'dry run' if dry_run else 'live'}):")
    print(f"  Total transactions: {total}")
    print(f"  Exact matches:      {stats['exact']}")
    print(f"  Fuzzy matches:      {stats['fuzzy']}")
    print(f"  Search matches:     {stats['search']}")
    print(f"  LLM queued:         {stats['llm']}")
    print(f"  Review queue:       {stats['review']}")
    print(f"  Skipped:            {stats['skipped']}")
    print(f"  Merchants created:  {stats['merchants_created']}")
    print(f"  Merchants found:    {stats['merchants_found']}")

    return stats

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Styx enrichment pipeline')
    parser.add_argument('--dry-run', action='store_true', help='Do not write to database')
    parser.add_argument('--no-llm', action='store_true', help='Skip LLM resolution')
    args = parser.parse_args()
    enrich_transactions(dry_run=args.dry_run, use_llm=not args.no_llm)