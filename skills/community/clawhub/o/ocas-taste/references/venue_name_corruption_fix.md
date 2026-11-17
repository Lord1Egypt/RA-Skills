# venue_name corruption fix — "… is confirmed" subject fragments

**Incident (2026-07-14):** A past `taste_scan.py` email scan run wrote 567 signals whose
`venue_name` field contained the DoorDash order-confirmation email **subject** instead of the
venue. Examples found in `signals.jsonl`:

- `"Jane on Larkin is confirmed"`
- `"Kasa Indian Eatery (Polk Street) is confirmed"`
- `"Mendocino Farms (Mission St) is confirmed"`
- `"Nepa Indian Cuisine (Divisadero St) is confirmed"`

~19 signals per venue (one batch), all pre-existing (none `created` on the day of discovery).
No `items.jsonl` corruption — only `venue_name` on signals. The artifact is the literal
string ` is confirmed` (and possibly other trailing subject text) appended to the real venue.

## Symptom check
```bash
cd <hermes-home>/commons/data/ocas-taste
python3 - <<'PYEOF'
import json
bad=[l for l in open('signals.jsonl') if 'is confirmed' in (json.loads(l).get('venue_name') or '')]
print('corrupted signals:', len(bad))
PYEOF
```

## Fix (deterministic, idempotent)
Strip the trailing ` is confirmed.*$` from `venue_name` (and `merchant_name` if affected),
then re-run dispatch dedup — the name normalization exposes real duplicates.

```bash
cd <hermes-home>/commons/data/ocas-taste
python3 - <<'PYEOF'
import json, re
fixed=0; out=[]
for l in open('signals.jsonl'):
    if not l.strip(): continue
    s=json.loads(l)
    vn=(s.get('venue_name') or '')
    if ' is confirmed' in vn:
        s['venue_name']=re.sub(r'\s+is confirmed.*$','',vn).strip()
        if ' is confirmed' in (s.get('merchant_name') or ''):
            s['merchant_name']=re.sub(r'\s+is confirmed.*$','',s['merchant_name']).strip()
        # if item_id is None and the cleaned name matches an existing item, link it
        fixed+=1
    out.append(json.dumps(s))
with open('signals.jsonl','w') as f: f.write('\n'.join(out)+'\n')
print(f'fixed {fixed} signals')
PYEOF

# Re-dedup — name change exposes real duplicates
<hermes-venv>/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/dispatch_taste_dedup.py
```

In the 2026-07-14 run this fixed 567 + 17 (this-run) signals and the re-dedup removed 64
total duplicates (12 dispatch-dup + 52 newly-exposed).

## If it recurs from a FRESH scan
The fix above patches data, not the parser. If a new scan produces `is confirmed` artifacts,
the email subject parser in `taste_scan.py` is regenerating them — audit
`references/email_extraction.md` / the DoorDash branch in `taste_scan.py` and fix at the
source (extract venue from the order payload / structured fields, not the subject line).