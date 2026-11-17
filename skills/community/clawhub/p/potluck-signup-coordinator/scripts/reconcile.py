#!/usr/bin/env python3
"""Compare supplied signup snapshots; never reads a provider or writes state."""
import argparse
import json
import sys

def need(condition, message):
    if not condition: raise ValueError(message)

def text(value):
    need(isinstance(value, str) and bool(value.strip()), 'nonempty id required'); return value

def integer(value, name, zero=False):
    need(type(value) is int and value >= (0 if zero else 1), name+' must be an integer in range'); return value

def index(items, name):
    need(isinstance(items, list), name+' must be list'); out={}
    for row in items:
        need(isinstance(row, dict), name+' rows must be objects')
        key=text(row.get('id')); need(key not in out, 'duplicate '+name+' id'); out[key]=row
    return out

def snapshot(data):
    need(isinstance(data, dict), 'snapshot must be object')
    need(type(data.get('complete')) is bool, 'complete boolean required')
    slots=index(data.get('slots'), 'slot'); claims=index(data.get('claims'), 'claim')
    for row in slots.values(): integer(row.get('capacity'), 'capacity', True)
    for row in claims.values():
        need(row.get('slot_id') in slots, 'claim references unknown slot')
        integer(row.get('units'), 'units')
        need(row.get('status') in ('confirmed','cancelled'), 'claim status must be confirmed or cancelled')
        if row.get('portions') is not None: integer(row['portions'], 'portions', True)
    return slots,claims

def report(data):
    need(isinstance(data, dict) and type(data.get('schema_version')) is int and data['schema_version']==1, 'schema_version 1 required')
    _, old=snapshot(data.get('before')); slots,new=snapshot(data.get('after')); complete=data['after']['complete']
    added=sorted(new.keys()-old.keys()); missing=sorted(old.keys()-new.keys())
    # Arbitrary private fields never enter output. Compare operational fields only.
    fields=('slot_id','units','portions','status','dish')
    changed=[key for key in sorted(old.keys() & new.keys()) if any(old[key].get(f)!=new[key].get(f) for f in fields)]
    coverage=[]
    for key,slot in sorted(slots.items()):
        claims=[c for c in new.values() if c['slot_id']==key and c['status']=='confirmed']
        used=sum(c['units'] for c in claims)
        coverage.append({'slot_id':key, 'capacity':slot['capacity'], 'claimed_units':used,
                         'open_units':max(0,slot['capacity']-used) if complete else None,
                         'possible_open_units_upper_bound':max(0,slot['capacity']-used),
                         'overfilled_units':max(0,used-slot['capacity']),
                         'known_portions':sum(c['portions'] for c in claims if c.get('portions') is not None),
                         'unknown_portion_claims':sum(c.get('portions') is None for c in claims),
                         'coverage_complete':complete})
    return {'added_claim_ids':added, 'changed_claim_ids':changed,
            'removed_claim_ids':missing if complete else [], 'missing_in_partial_claim_ids':missing if not complete else [],
            'explicitly_cancelled_claim_ids':sorted(k for k,v in new.items() if v['status']=='cancelled'),
            'coverage':coverage, 'scope':'snapshot observations, not attendance or authenticated consent'}

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('input'); args=p.parse_args()
    try:
        with open(args.input, encoding='utf-8') as f: result=report(json.load(f))
    except (OSError,ValueError,TypeError,KeyError) as e:
        print('Invalid input: '+str(e), file=sys.stderr); return 2
    print(json.dumps(result,indent=2)); return 0

if __name__=='__main__': sys.exit(main())
