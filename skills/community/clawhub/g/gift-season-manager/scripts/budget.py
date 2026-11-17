#!/usr/bin/env python3
"""Private gift-cost totals from explicit records. Offline, read-only, no purchases."""
import argparse
from decimal import Decimal, InvalidOperation
import json
import sys

def need(condition, message):
    if not condition: raise ValueError(message)

def money(v):
    need(type(v) in (str,int), 'money requires decimal string or integer')
    try: n=Decimal(v)
    except InvalidOperation: raise ValueError('invalid money') from None
    need(n.is_finite() and n>=0 and n.as_tuple().exponent>=-2, 'money must be finite, nonnegative, at most two decimals')
    return n

def report(data):
    need(isinstance(data,dict) and type(data.get('schema_version')) is int and data['schema_version']==1, 'schema_version 1 required')
    currency=data.get('currency'); need(isinstance(currency,str) and len(currency)==3 and currency.isascii() and currency.isalpha() and currency.isupper(), 'currency code required')
    cap=money(data.get('budget')); items=data.get('costs'); need(isinstance(items,list), 'costs must be list')
    paid=refunds=remaining=estimates=Decimal(0); unknown=[]; ids=set()
    for item in items:
        need(isinstance(item,dict), 'cost must be object')
        key=item.get('id'); need(isinstance(key,str) and bool(key.strip()) and key not in ids, 'unique cost id required');ids.add(key)
        need(item.get('currency')==currency, 'mixed/missing currency')
        gross=money(item.get('paid')); refund=money(item.get('refund_received'))
        need(refund<=gross, 'refund exceeds paid')
        cancelled=item.get('cancelled');need(type(cancelled) is bool, 'cancelled boolean required')
        committed=item.get('committed_total');estimate=item.get('estimate')
        if committed is None:
            need(gross==0 and refund==0, 'paid costs need committed_total')
            if not cancelled:
                if estimate is None: unknown.append(key)
                else: estimates+=money(estimate)
        else:
            total=money(committed);need(total>=gross, 'commitment below paid')
            need(estimate is None, 'committed items must not have an uncommitted estimate')
            if not cancelled: remaining+=total-gross
        # Cancelled means outstanding obligation was confirmed released, not that cash was refunded.
        paid+=gross;refunds+=refund
    net=paid-refunds;forecast=net+remaining+estimates
    fmt=lambda n:format(n,'.2f')
    return {'currency':currency,'gross_paid':fmt(paid),'refunds_received':fmt(refunds),'net_paid':fmt(net),
            'unpaid_commitments':fmt(remaining),'uncommitted_estimates':fmt(estimates),'known_forecast':fmt(forecast),
            'headroom_against_known_costs':fmt(cap-forecast),'unknown_cost_ids':unknown,'complete':not unknown}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');args=p.parse_args()
    try:
        with open(args.input,encoding='utf-8') as f:result=report(json.load(f))
    except (OSError,ValueError,TypeError,KeyError) as e:
        print('Invalid input: '+str(e),file=sys.stderr);return 2
    print(json.dumps(result,indent=2));return 0

if __name__=='__main__':sys.exit(main())
