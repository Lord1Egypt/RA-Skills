#!/usr/bin/env python3
"""Query Hemlane recurring payment requests using HAR-derived GraphQL."""
import argparse, json, sys
from pathlib import Path
from urllib import request, error

ENDPOINT = 'https://api.hemlane.com/graphql'

PROPERTY_SEARCH_QUERY = """
query PageFiltersPropertySearchQuery($search: String, $ownerUserId: ID, $portfolioId: ID, $id: ID, $isDeleted: Boolean, $propertyOnly: Boolean, $searchAlgo: String) {
  myPropertyAndUnits(search: $search, ownerUserId: $ownerUserId, portfolioId: $portfolioId, id: $id, isDeleted: $isDeleted, propertyOnly: $propertyOnly, searchAlgo: $searchAlgo) {
    __typename
    ... on Property { id nickname addressStreet isSingleFamily __typename }
    ... on PropertyUnit { id unitNumber nicknameWithUnit property { id nickname addressStreet __typename } __typename }
  }
}
"""

RECURRING_QUERY = """
query RecurringNextCursorQuery($status: RecurringPaymentRequestStatus, $paymentStatus: RecurringPaymentRequestPaymentStatus, $pagination: PagedPaginationInput = {page: 1, limit: 12}, $propertyId: ID, $propertyUnitId: ID, $portfolioId: ID, $ownerUserId: ID) {
  recurringPaymentRequestsCursor(status: $status, paymentStatus: $paymentStatus, pagination: $pagination, propertyId: $propertyId, propertyUnitId: $propertyUnitId, portfolioId: $portfolioId, ownerUserId: $ownerUserId) {
    pageInfo { page hasNextPage hasPreviousPage __typename }
    data {
      allowCreditCard amount confirmedAmount destinationDescription
      destinationTenant { id invitationName status user { id fullName __typename } __typename }
      destinationUser { id fullName userType __typename }
      endDate endDateOriginal id interval intervalCount isOverride isSourcePayingProcessingFee monthlyAnchor nextProjectedDueDate overrideInitialAmount
      property { id isSingleFamily nickname addressStreet __typename }
      propertyUnit { id unitNumber nicknameWithUnit __typename }
      paymentCategory { id label __typename }
      paymentSubcategory { id label __typename }
      recurringPayments { id amount status createdAt daysAhead __typename }
      rentSplitSchema singlePaymentRequired sourceDescription
      sourceTenantGroup { id status tenants { id status invitationName user { id fullName __typename } __typename } __typename }
      sourceUser { id fullName __typename }
      startDate status weeklyAnchor __typename
    }
    __typename
  }
}
"""

SENSITIVE = {'cookie','authorization','x-csrf-token','x-csrf','csrf-token'}
KEEP_HEADERS = {'authorization','x-csrf-token','content-type','origin','referer','user-agent','cookie','apollographql-client-name','apollographql-client-version'}

def load_headers(auth_file=None, auth_from_har=None):
    if auth_file:
        data=json.loads(Path(auth_file).read_text())
        if 'headers' in data and isinstance(data['headers'], dict):
            data=data['headers']
        return normalize_headers(data)
    if auth_from_har:
        har=json.loads(Path(auth_from_har).read_text())
        for e in har.get('log',{}).get('entries',[]):
            req=e.get('request',{})
            if 'api.hemlane.com/graphql' not in req.get('url',''):
                continue
            headers={h.get('name',''):h.get('value','') for h in req.get('headers',[])}
            return normalize_headers(headers)
        raise SystemExit('No api.hemlane.com/graphql request found in HAR')
    raise SystemExit('Provide --auth-file or --auth-from-har')

def normalize_headers(headers):
    out={}
    for k,v in (headers or {}).items():
        lk=k.lower()
        if v is None:
            continue
        if lk in KEEP_HEADERS or lk.startswith('x-'):
            out[k]=str(v)
    out.setdefault('content-type','application/json')
    out.setdefault('accept','application/json')
    return out

def redacted(headers):
    return {k:('<redacted>' if k.lower() in SENSITIVE else v) for k,v in headers.items()}

def gql(headers, query, variables, operation_name, endpoint=ENDPOINT):
    payload={'query':query,'variables':variables,'operationName':operation_name}
    req=request.Request(endpoint, data=json.dumps(payload).encode(), headers=headers, method='POST')
    try:
        with request.urlopen(req, timeout=60) as resp:
            body=resp.read().decode('utf-8','replace')
    except error.HTTPError as e:
        body=e.read().decode('utf-8','replace')
        raise SystemExit(f'HTTP {e.code}: {body[:2000]}')
    data=json.loads(body)
    if data.get('errors'):
        raise SystemExit(json.dumps({'errors':data['errors']}, indent=2))
    return data.get('data')

def compact_request(r):
    tenants=[]
    tg=(r.get('sourceTenantGroup') or {})
    for t in tg.get('tenants') or []:
        u=t.get('user') or {}
        tenants.append({'id':t.get('id'),'status':t.get('status'),'invitationName':t.get('invitationName'),'fullName':u.get('fullName')})
    prop=r.get('property') or {}
    unit=r.get('propertyUnit') or {}
    cat=r.get('paymentCategory') or {}
    sub=r.get('paymentSubcategory') or {}
    return {
        'id': r.get('id'),
        'status': r.get('status'),
        'amount': r.get('amount'),
        'confirmedAmount': r.get('confirmedAmount'),
        'interval': r.get('interval'),
        'intervalCount': r.get('intervalCount'),
        'startDate': r.get('startDate'),
        'endDate': r.get('endDate'),
        'nextProjectedDueDate': r.get('nextProjectedDueDate'),
        'property': {'id':prop.get('id'),'nickname':prop.get('nickname'),'addressStreet':prop.get('addressStreet')},
        'propertyUnit': {'id':unit.get('id'),'unitNumber':unit.get('unitNumber'),'nicknameWithUnit':unit.get('nicknameWithUnit')},
        'category': cat.get('label'),
        'subcategory': sub.get('label'),
        'sourceDescription': r.get('sourceDescription'),
        'destinationDescription': r.get('destinationDescription'),
        'tenantGroupId': tg.get('id'),
        'tenantGroupStatus': tg.get('status'),
        'tenants': tenants,
        'recentRecurringPayments': r.get('recurringPayments') or [],
    }

def text_blob(obj):
    return json.dumps(obj, ensure_ascii=False).lower()

def main():
    ap=argparse.ArgumentParser(description='Query Hemlane recurring payment requests.')
    ap.add_argument('--auth-file')
    ap.add_argument('--auth-from-har')
    ap.add_argument('--search', help='Filter returned requests by text, e.g. "1518 Dille 1520"')
    ap.add_argument('--property-id')
    ap.add_argument('--property-unit-id')
    ap.add_argument('--status', default='Active', help='Hemlane recurring status, e.g. Active, Cancelled, or blank for all')
    ap.add_argument('--page', type=int, default=1)
    ap.add_argument('--limit', type=int, default=50)
    ap.add_argument('--all-pages', action='store_true')
    ap.add_argument('--include-raw', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--output')
    args=ap.parse_args()
    headers=load_headers(args.auth_file, args.auth_from_har)
    variables={'pagination':{'page':args.page,'limit':args.limit},'propertyId':args.property_id,'propertyUnitId':args.property_unit_id,'portfolioId':None,'ownerUserId':None}
    if args.status:
        variables['status']=args.status
    if args.dry_run:
        print(json.dumps({'endpoint':ENDPOINT,'headers':redacted(headers),'operationName':'RecurringNextCursorQuery','variables':variables}, indent=2))
        return
    items=[]; page=args.page
    while True:
        variables['pagination']['page']=page
        data=gql(headers, RECURRING_QUERY, variables, 'RecurringNextCursorQuery')
        cur=data['recurringPaymentRequestsCursor']
        batch=cur.get('data') or []
        items.extend(batch)
        if not args.all_pages or not (cur.get('pageInfo') or {}).get('hasNextPage'):
            break
        page+=1
    if args.search:
        terms=[t.lower() for t in args.search.split()]
        items=[r for r in items if all(t in text_blob(r) for t in terms)]
    out={'count':len(items),'requests':items if args.include_raw else [compact_request(r) for r in items]}
    if args.output:
        Path(args.output).write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
if __name__ == '__main__':
    main()
