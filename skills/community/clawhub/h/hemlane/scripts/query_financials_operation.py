#!/usr/bin/env python3
"""Replay Hemlane Financials GraphQL operations from captured HAR samples.

This is a narrow, read-oriented utility for financials HAR-derived queries. It
loads the operation query + sample variables from HAR, applies JSON overrides,
and can walk simple page-based pagination.
"""
import argparse, json, sys
from pathlib import Path
from urllib import request, error

DEFAULT_HARS = [
    '/home/umbrel/Downloads/har/financials_hemlane.com.har',
    '/home/umbrel/Downloads/har/financials_pages_hemlane.com.har',
]
ENDPOINT='https://api.hemlane.com/graphql'
KEEP_HEADERS={'authorization','x-csrf-token','content-type','origin','referer','user-agent','cookie','accept','apollographql-client-name','apollographql-client-version'}
SENSITIVE={'cookie','authorization','x-csrf-token'}

KNOWN_PAGE_PATHS={
    'RecurringNextCursorQuery': ['pagination','page'],
    'TransactionsNextCursorQuery': ['pagination','page'],
    'PagedFinancialTransactions': ['page'],
}
KNOWN_DATA_PATHS={
    'RecurringNextCursorQuery': ['recurringPaymentRequestsCursor'],
    'TransactionsNextCursorQuery': ['transactionsNextCursor'],
    'PagedFinancialTransactions': ['financialTransactions'],
}

def normalize_headers(headers):
    out={}
    for k,v in (headers or {}).items():
        if v is None: continue
        lk=k.lower()
        if lk in KEEP_HEADERS or lk.startswith('x-'):
            out[k]=str(v)
    out.setdefault('content-type','application/json')
    out.setdefault('accept','application/json')
    return out

def load_headers(path):
    data=json.loads(Path(path).read_text())
    if 'headers' in data and isinstance(data['headers'],dict): data=data['headers']
    return normalize_headers(data)

def iter_har_ops(paths):
    for path in paths:
        p=Path(path)
        if not p.exists(): continue
        har=json.loads(p.read_text())
        for e in har.get('log',{}).get('entries',[]):
            req=e.get('request',{})
            if 'api.hemlane.com/graphql' not in req.get('url',''): continue
            text=((req.get('postData') or {}).get('text') or '').strip()
            if not text: continue
            try: payload=json.loads(text)
            except Exception: continue
            op=payload.get('operationName')
            q=payload.get('query') or ''
            if op and q:
                yield op, q, payload.get('variables') or {}, str(p)

def load_operation(name, paths):
    first=None
    for op,q,v,p in iter_har_ops(paths):
        if op == name:
            # prefer sample with richer variables
            cand={'operationName':op,'query':q,'variables':v,'sourceHar':p}
            if first is None or len(v) > len(first['variables']): first=cand
    if not first: raise SystemExit(f'Operation not found in HARs: {name}')
    return first

def deep_update(a,b):
    for k,v in b.items():
        if isinstance(v,dict) and isinstance(a.get(k),dict): deep_update(a[k],v)
        else: a[k]=v
    return a

def set_path(obj,path,val):
    cur=obj
    for k in path[:-1]:
        cur=cur.setdefault(k,{})
    cur[path[-1]]=val

def get_path(obj,path):
    cur=obj
    for k in path:
        if cur is None: return None
        cur=cur.get(k) if isinstance(cur,dict) else None
    return cur

def gql(headers, op, query, variables):
    payload={'operationName':op,'query':query,'variables':variables}
    req=request.Request(ENDPOINT, data=json.dumps(payload).encode(), headers=headers, method='POST')
    try:
        with request.urlopen(req, timeout=60) as resp:
            body=resp.read().decode('utf-8','replace')
    except error.HTTPError as e:
        body=e.read().decode('utf-8','replace')
        raise SystemExit(f'HTTP {e.code}: {body[:2000]}')
    data=json.loads(body)
    if data.get('errors'):
        raise SystemExit(json.dumps({'errors':data['errors']}, indent=2))
    return data.get('data') or {}

def main():
    ap=argparse.ArgumentParser(description='Replay a Hemlane Financials GraphQL operation from HAR.')
    ap.add_argument('--operation-name', required=True)
    ap.add_argument('--auth-file', required=True)
    ap.add_argument('--variables-json', default='{}', help='JSON object merged into HAR sample variables')
    ap.add_argument('--har', action='append', dest='hars', help='HAR path; repeatable. Defaults to financials HARs.')
    ap.add_argument('--page', type=int)
    ap.add_argument('--limit', type=int)
    ap.add_argument('--all-pages', action='store_true')
    ap.add_argument('--output')
    ap.add_argument('--dry-run', action='store_true')
    args=ap.parse_args()
    hars=args.hars or DEFAULT_HARS
    op=load_operation(args.operation_name, hars)
    variables=json.loads(json.dumps(op['variables']))
    deep_update(variables, json.loads(args.variables_json))
    page_path=KNOWN_PAGE_PATHS.get(args.operation_name)
    if args.page is not None and page_path: set_path(variables,page_path,args.page)
    if args.limit is not None:
        if 'pagination' in variables and isinstance(variables['pagination'],dict): variables['pagination']['limit']=args.limit
        elif args.operation_name in ('TransactionsNextCursorQuery','RecurringNextCursorQuery'): variables.setdefault('pagination',{})['limit']=args.limit
    headers=load_headers(args.auth_file)
    if args.dry_run:
        print(json.dumps({'endpoint':ENDPOINT,'operationName':args.operation_name,'sourceHar':op['sourceHar'],'variables':variables,'headers':{k:('<redacted>' if k.lower() in SENSITIVE else v) for k,v in headers.items()}}, indent=2))
        return
    pages=[]; page=get_path(variables,page_path) if page_path else None
    if page is None and page_path: page=1; set_path(variables,page_path,page)
    while True:
        data=gql(headers,args.operation_name,op['query'],variables)
        pages.append(data)
        if not args.all_pages or not page_path: break
        root=get_path(data, KNOWN_DATA_PATHS.get(args.operation_name, [])) or {}
        info=root.get('pageInfo') or {}
        has_next=info.get('hasNextPage') or (info.get('totalPages') and info.get('page') and info['page'] < info['totalPages'])
        if not has_next: break
        page=(get_path(variables,page_path) or page or 1)+1
        set_path(variables,page_path,page)
    out={'operationName':args.operation_name,'sourceHar':op['sourceHar'],'pageCount':len(pages),'pages':pages}
    if args.output: Path(args.output).write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
if __name__=='__main__': main()
