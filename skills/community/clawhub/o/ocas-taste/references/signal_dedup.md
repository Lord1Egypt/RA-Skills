# Same-Day Cross-Source Signal Deduplication

## Problem

When the same restaurant appears via multiple sources (email + calendar + styx) on the same date, the enrichment pipeline creates duplicate signals. For example:
- DoorDash email for "Nopa" on 2026-04-15
- Calendar reservation for "Nopa" on 2026-04-15  
- Styx charge for "Nopa" on 2026-04-15

After enrichment, there are 3 signals for the same visit. This inflates visit counts and corrupts the taste model.

## Solution

Dedup signals by `(normalized_name, date)` keeping only one signal per group.

Source priority (keep highest):
1. `styx` / `styx_places` — most reliable (actual transaction)
2. `calendar` — reservation confirmed
3. `email` / `email_scan` — order confirmation
4. `enrichment` — added by enrichment script (lowest priority)

## Script

```bash
python3 <hermes-home>/commons/data/ocas-taste/scripts/taste_signals_dedup.py
```

The script:
1. Groups signals by `(normalized_name, first_seen date)`
2. For groups with multiple signals, keeps the one with highest source priority
3. Removes duplicates from `signals.jsonl`
4. Reports counts before/after

## When to run

- After any enrichment run (`taste_full_enrich.py`, `taste_cleanup_and_enrich.py`)
- After `taste.scan` if multiple sources were scanned
- Periodically as maintenance (e.g., weekly cron)

## Verification

After dedup, verify no same-day duplicates remain:
```python
from collections import defaultdict
import json

signals = [json.loads(l) for l in open('signals.jsonl') if l.strip()]
groups = defaultdict(list)
for s in signals:
    key = (s.get('normalized_name','').lower(), s.get('created_at','')[:10])
    groups[key].append(s.get('source','?'))

dupes = {k:v for k,v in groups.items() if len(v) > 1}
print(f"Same-day dupes: {len(dupes)}")
```