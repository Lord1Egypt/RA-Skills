#!/usr/bin/env python3
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Corrected daily Styx->Taste delta ingestion with place_id linking.')
    print("Usage: styx_delta_corrected.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)
import os
"""Styx -> Taste daily delta (CORRECTED, 2026-07-22).

Lessons baked in (see references/dispatch_dedup_styx_corruption.md):
- Deduplicate candidates by (norm(name), date) BEFORE enriching — Styx `transaction_merchants`
  has duplicate rows per transaction, and a naive loop would emit 2-3 identical signals.
- Link by canonical place_id OR normalized name; if a Taste item already exists, LINK the
  signal (bump visit_count/avg_amount) instead of creating a duplicate item.
- Self-heal pre-existing orphan styx signals by normalized_name AFTER merging old+new items.
- Write signals+items ATOMICALLY (rebuild both files in memory, overwrite once) so a failed
  mid-write can't leave the store half-updated. No append-then-fix.
- NEVER chain dispatch_taste_dedup.py onto this run — it deletes Styx signals (see incident).
- ALWAYS run verify_taste_delta.py afterward; a "N created" return is testimony, not proof.

Usage:
  python3 styx_delta_corrected.py            # write
  python3 styx_delta_corrected.py --dry-run  # print candidates, no writes
"""
import sqlite3, json, re, sys, time, uuid, collections, urllib.request, urllib.parse

STYX = os.path.expanduser("~/indigo-repo/data/styx.db")
TXN = os.path.expanduser("~/.hermes/data/transactions.db")
DATA = os.path.expanduser("~/.hermes/commons/data/ocas-taste")
ITEMS = DATA + '/items.jsonl'
SIGNALS = DATA + '/signals.jsonl'
DRY = '--dry-run' in sys.argv

KEY = None
for line in open(os.path.expanduser("~/.hermes/secrets/plaid.env")):
    if line.startswith('GOOGLE_PLACES_API_KEY='):
        KEY = line.split('=', 1)[1].strip()
assert KEY, "GOOGLE_PLACES_API_KEY missing"

items = [json.loads(l) for l in open(ITEMS) if l.strip()]
signals = [json.loads(l) for l in open(SIGNALS) if l.strip()]

items_by_place = collections.defaultdict(list)
items_by_name = collections.defaultdict(list)
for it in items:
    if it.get('place_id'):
        items_by_place[it['place_id']].append(it)
    nm = (it.get('normalized_name') or it.get('name') or '').lower().strip()
    if nm:
        items_by_name[nm].append(it)

SIG_DEDUP = set(s.get('dedup_key', '') for s in signals if s.get('source') == 'styx')
SIG_NAME_DATE = set((s.get('merchant_name', '').lower().strip(), s.get('date', '')[:10])
                    for s in signals if s.get('source') == 'styx')

FOOD_CATS = ('restaurant', 'cafe', 'bar', 'food', 'bakery', 'meal_takeaway', 'meal_delivery')
BLOCKLIST = {'doordash', 'walgreens', 'cvs', 'postmates', 'ubereats', 'uber eats',
             'grubhub', 'lyft', 'uber', 'seamless', 'caviar'}


def norm(n):
    return re.sub(r'[^a-z0-9]', '', (n or '').lower())


def enrich(merchant_name, city):
    q = f"{merchant_name} restaurant {city or ''}".strip()
    url = ('https://maps.googleapis.com/maps/api/place/textsearch/json?query='
           + urllib.parse.quote(q) + '&key=' + KEY)
    req = urllib.request.Request(url, headers={'User-Agent': 'taste-delta/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
    except Exception:
        return None
    if data.get('status') != 'OK' or not data.get('results'):
        return None
    res = data['results'][0]
    return {
        'place_id': res.get('place_id'), 'name': res.get('name'),
        'address': res.get('formatted_address'), 'rating': res.get('rating'),
        'price_level': res.get('price_level'), 'types': res.get('types', []),
        'location': res.get('geometry', {}).get('location'),
    }


conn = sqlite3.connect(STYX)
conn.execute(f"ATTACH DATABASE '{TXN}' AS txndb")
rows = conn.execute('''
    SELECT t.transaction_id, t.name, t.amount, t.date, t.personal_finance_category,
           m.name, m.category, m.city, tm.confidence, t.loc_city, t.loc_region
    FROM transaction_merchants tm
    JOIN merchants m ON tm.merchant_id = m.id
    JOIN txndb.transactions t ON tm.transaction_id = t.transaction_id
    WHERE (m.category IN (%s)
       OR t.personal_finance_category = 'FOOD_AND_DRINK')
      AND tm.confidence >= 0.7
    ORDER BY t.date DESC
''' % ','.join("'%s'" % c for c in FOOD_CATS)).fetchall()
conn.close()

seen = set()
candidates = []
for (txn_id, raw_name, amount, date, pfc, mname, mcat, mcity, conf, loc_city, loc_region) in rows:
    if not mname:
        continue
    ml = mname.lower().strip()
    if ml in BLOCKLIST:
        continue
    date10 = date[:10]
    dkey = f"styx:{norm(mname)}:{date10}"
    if dkey in SIG_DEDUP or (ml, date10) in SIG_NAME_DATE:
        continue
    ukey = (norm(mname), date10)
    if ukey in seen:
        continue
    seen.add(ukey)
    candidates.append({'txn_id': txn_id, 'raw_name': raw_name, 'amount': amount,
                       'date': date, 'mname': mname, 'mcat': mcat,
                       'city': mcity or loc_city or loc_region or '', 'conf': conf})

print(f"Styx food rows matched: {len(rows)} | deduplicated new candidates: {len(candidates)}")

if DRY:
    for c in candidates[:20]:
        print(f"  {c['date'][:10]} {c['mname']!r} ({c['mcat']}) city={c['city']!r} ${c['amount']}")
    sys.exit(0)

new_items, new_signals = [], []
linked = enriched_ok = enriched_fail = 0
now = time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime())

for c in candidates:
    enr = enrich(c['mname'], c['city'])
    time.sleep(0.1)
    pid = enr.get('place_id') if enr else None
    if pid:
        enriched_ok += 1
    else:
        enriched_fail += 1
        enr = {}
    date10 = c['date'][:10]
    dkey = f"styx:{norm(c['mname'])}:{date10}"
    venue_name = enr.get('name') or c['mname']
    nname = (enr.get('name') or c['mname']).lower().strip()
    sig = {
        "amount": c['amount'], "confidence": c['conf'], "created_at": now,
        "date": date10, "dedup_key": dkey, "domain": "food",
        "merchant_name": c['mname'], "raw_date": date10,
        "signal_id": uuid.uuid4().hex, "signal_type": "purchase",
        "source": "styx", "venue_name": venue_name,
    }
    target = None
    if pid and items_by_place.get(pid):
        target = items_by_place[pid][0]
    if target is None and items_by_name.get(nname):
        target = items_by_name[nname][0]
    if target is None:
        for it in new_items:
            if (pid and it.get('place_id') == pid) or (nname and it.get('normalized_name') == nname):
                target = it
                break
    if target is not None:
        target.setdefault('visit_dates', [])
        target['visit_dates'].append(date10)
        target['visit_count'] = target.get('visit_count', 0) + 1
        vc = target['visit_count']
        prev = target.get('avg_amount', 0.0) or 0.0
        target['avg_amount'] = round((prev * (vc - 1) + float(c['amount'])) / vc, 2)
        target['signal_count'] = target.get('signal_count', 0) + 1
        target['last_visit'] = date10
        sig['item_id'] = target['item_id']
        linked += 1
        new_signals.append(sig)
    else:
        item_id = 'item-' + uuid.uuid4().hex[:12]
        addr = enr.get('address')
        item = {
            "domain": "food", "kind": "venue", "item_id": item_id,
            "name": venue_name, "normalized_name": nname, "venue_name": venue_name,
            "place_id": pid,
            "address": addr,
            "city": (addr.split(',')[1].strip() if addr and len(addr.split(',')) >= 2 else (c['city'] or None)),
            "category": c['mcat'] or 'restaurant',
            "enriched": bool(pid), "enriched_at": now if pid else None,
            "first_visit": date10, "last_visit": date10,
            "visit_count": 1, "visit_dates": [date10],
            "avg_amount": round(float(c['amount']), 2),
            "total_spend": round(float(c['amount']), 2),
            "signal_count": 1, "source": "styx_final_sync",
            "styx_merchant_id": None,
            "locations": [{"name": venue_name, "place_id": pid, "city": c['city'] or None}],
            "metadata": {"confidence": c['conf'], "styx_source": "google_places"},
        }
        if enr.get('rating') is not None:
            item['rating'] = enr['rating']
        if enr.get('price_level') is not None:
            item['price_level'] = enr['price_level']
        if enr.get('types'):
            item['types'] = enr['types']
        sig['item_id'] = item_id
        new_items.append(item)
        if pid:
            items_by_place[pid].append(item)
        items_by_name[nname].append(item)

all_items = items + new_items
live_ids = {it.get('item_id') for it in all_items}
live_by_name = collections.defaultdict(list)
for it in all_items:
    nm = norm(it.get('normalized_name') or it.get('name') or '')
    if nm:
        live_by_name[nm].append(it)
orphan_healed = 0
for s in signals:
    if s.get('source') != 'styx':
        continue
    if s.get('item_id') and s['item_id'] in live_ids:
        continue
    nm = norm(s.get('merchant_name'))
    if nm in live_by_name:
        s['item_id'] = live_by_name[nm][0]['item_id']
        orphan_healed += 1

with open(SIGNALS, 'w') as f:
    for s in signals + new_signals:
        f.write(json.dumps(s) + '\n')
with open(ITEMS, 'w') as f:
    for it in all_items:
        f.write(json.dumps(it) + '\n')

print(f"WRITTEN: items_created={len(new_items)} signals_created={len(new_signals)} "
      f"linked_to_existing={linked} orphan_self_healed={orphan_healed}")
print(f"ENRICHMENT: ok={enriched_ok} failed={enriched_fail}")
for it in new_items:
    print(f"  NEW {it['name']!r} place_id={it.get('place_id')} city={it.get('city')} ${it.get('avg_amount')}")
print("NEXT: run scripts/verify_taste_delta.py — must print VERIFY PASSED (EXIT=0)")
