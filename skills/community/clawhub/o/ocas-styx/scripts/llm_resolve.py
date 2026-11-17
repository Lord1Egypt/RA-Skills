#!/usr/bin/env python3
"""LLM resolution for Styx enrichment — resolves transaction names the pipeline
couldn't match via exact/fuzzy/search methods.

Reads prompts from a JSONL file, sends each to the LLM for resolution,
and writes results back to the Styx database.

Usage:
    python3 llm_resolve.py [--input /tmp/styx_llm_queue.jsonl] [--batch-size 20]
"""

import json
import os
import subprocess
import sys
import time

sys.path.insert(0, __import__('os').path.dirname(__file__))
from styx_common import CATEGORY_MAP, init_styx_db

STYX_DB = '~/.hermes/data/styx.db'

def resolve_via_llm(prompt):
    """Send a resolution prompt to the LLM via hermes CLI.

    Returns (business_name, confidence) or (None, 0.0) if unresolved.
    """
    try:
        # Use hermes ask for LLM access
        result = subprocess.run(
            ['hermes', 'ask', '--no-stream', prompt],
            capture_output=True, text=True, timeout=30
        )
        answer = result.stdout.strip()

        if not answer or answer.upper() == 'UNKNOWN' or len(answer) < 2:
            return None, 0.0

        # Clean up the answer — take just the first line
        business_name = answer.split('\n')[0].strip()
        # Remove quotes if present
        business_name = business_name.strip('"').strip("'")

        if not business_name or business_name.upper() == 'UNKNOWN':
            return None, 0.0

        return business_name, 0.7  # LLM confidence baseline
    except subprocess.TimeoutExpired:
        return None, 0.0
    except FileNotFoundError:
        # hermes CLI not available — return None
        return None, 0.0

def normalize_for_db(name):
    """Normalize a name for database storage."""
    norm = name.lower()
    norm = ''.join(c for c in norm if c.isalnum() or c == ' ')
    return ' '.join(norm.split())

def process_queue(input_file, batch_size=20):
    """Process LLM resolution queue."""
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return

    styx_conn = init_styx_db(STYX_DB)

    items = []
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))

    total = len(items)
    print(f"Resolving {total} transactions via LLM (batch size: {batch_size})...")
    print(f"{'='*60}")

    resolved = 0
    unresolved = 0
    merchants_created = 0

    for i, item in enumerate(items):
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i+1}/{total} ({resolved} resolved, {unresolved} unresolved)")

        prompt = item['prompt']
        business_name, confidence = resolve_via_llm(prompt)

        if business_name and confidence > 0.5:
            cat = CATEGORY_MAP.get(item.get('personal_finance_category', ''), 'other')
            norm = normalize_for_db(business_name)

            # Get or create merchant
            row = styx_conn.execute(
                'SELECT id FROM merchants WHERE normalized_name = ?', (norm,)
            ).fetchone()
            if row:
                mid = row[0]
            else:
                cur = styx_conn.execute(
                    'INSERT INTO merchants (name, normalized_name, category, source, confidence) VALUES (?, ?, ?, ?, ?)',
                    (business_name, norm, cat, 'llm', confidence)
                )
                mid = cur.lastrowid
                merchants_created += 1

            # Link transaction
            styx_conn.execute(
                '''INSERT OR REPLACE INTO transaction_merchants
                (transaction_id, merchant_id, raw_name, match_method, confidence, is_primary)
                VALUES (?, ?, ?, ?, ?, 1)''',
                (item['transaction_id'], mid, item['raw_name'], 'llm', confidence)
            )
            styx_conn.commit()
            resolved += 1
        else:
            # Add to review queue
            review_file = '~/.hermes/data/styx/review_queue.jsonl'
            os.makedirs(os.path.dirname(review_file), exist_ok=True)
            with open(review_file, 'a') as f:
                f.write(json.dumps(item) + '\n')
            unresolved += 1

        # Rate limiting
        if (i + 1) % batch_size == 0:
            print(f"  Pausing after batch of {batch_size}...")
            time.sleep(2)

    styx_conn.close()

    print(f"\n{'='*60}")
    print("LLM resolution complete:")
    print(f"  Resolved:          {resolved}")
    print(f"  Unresolved:        {unresolved}")
    print(f"  Merchants created: {merchants_created}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='LLM resolution for Styx')
    parser.add_argument('--input', default='/tmp/styx_llm_queue.jsonl', help='Input JSONL file')
    parser.add_argument('--batch-size', type=int, default=20, help='Batch size before pause')
    args = parser.parse_args()
    process_queue(args.input, args.batch_size)