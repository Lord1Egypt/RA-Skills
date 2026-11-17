"""Check the actual structured values consumed by KPI/chart rendering.

This does not prove free-text narratives or source authenticity. It rejects
contradictions; it never overwrites source values using a decision label.
"""
from decimal import Decimal, InvalidOperation
import json
import re
from datetime import date,timedelta


KEYS = ('gmv','visitors','buyers','orders','refund_amount','ad_spend','attributed_gmv',
        'profit','total_cost','conversion_rate','refund_rate_amount','aov','roas','roi','uv_value','net_sales','net_gmv_reference',
        'net_roas','attributed_net_sales','attributed_refund','contribution_roas',
        'attributed_contribution_before_ad','attributed_discount','attributed_product_cost',
        'attributed_platform_fee','attributed_fulfillment_cost')
ALIASES = {
    **{key:key for key in KEYS},
    'gmv':'gmv','访客':'visitors','访客数':'visitors','visitors':'visitors',
    '支付买家数':'buyers','paid_buyers':'buyers','buyers':'buyers','orders':'orders','订单数':'orders',
    '转化率':'conversion_rate','conversion_rate':'conversion_rate',
    '退款率':'refund_rate_amount','refund_rate_amount':'refund_rate_amount',
    '客单价':'aov','aov':'aov','roas':'roas','roi':'roi','uv价值':'uv_value',
    'uv_value':'uv_value','净销售':'net_sales','net_sales':'net_sales',
    '推广花费':'ad_spend','投放花费':'ad_spend','退款金额':'refund_amount','归因gmv':'attributed_gmv'}
UNITS = {'gmv':('元',),'visitors':('人',),'buyers':('人',),'orders':('单',),
         'aov':('元/人','元'),'uv_value':('元/人','元'),'net_sales':('元',),
         'conversion_rate':('ratio','%'),'refund_rate_amount':('ratio','%'),
         'roas':('倍','ratio'),'roi':('ratio','%'),
         'ad_spend':('元',),'refund_amount':('元',),'attributed_gmv':('元',),'profit':('元',),'total_cost':('元',)}
UNITS['net_gmv_reference']=('元',)
UNITS.update(net_roas=('倍','ratio'),attributed_net_sales=('元',),attributed_refund=('元',))
UNITS.update(contribution_roas=('倍','ratio'),attributed_contribution_before_ad=('元',),
             attributed_discount=('元',),attributed_product_cost=('元',),
             attributed_platform_fee=('元',),attributed_fulfillment_cost=('元',))
ALIASES.update({'净roas':'net_roas','扣退款roas':'net_roas',
                '归因净销售额':'attributed_net_sales','归因退款额':'attributed_refund',
                '贡献roas':'contribution_roas','扣变动成本roas':'contribution_roas',
                '广告前归因贡献额':'attributed_contribution_before_ad',
                '归因优惠':'attributed_discount','归因商品成本':'attributed_product_cost',
                '归因平台费用':'attributed_platform_fee','归因履约成本':'attributed_fulfillment_cost'})


def require(condition,reason):
    if not condition: raise ValueError(reason)


def number(value):
    require(not isinstance(value,bool),'report_metric_boolean_not_number')
    try: result=Decimal(str(value))
    except (InvalidOperation,TypeError,ValueError): raise ValueError('report_metric_number_invalid') from None
    require(result.is_finite(),'report_metric_number_invalid')
    return result


def locations(row,key):
    require(isinstance(row,dict),'report_metric_row_invalid')
    result=[]
    for name in ('metrics','inputs'):
        container=row.get(name,{})
        require(isinstance(container,dict),'report_metric_container_invalid')
        if key in container: result.append((name+'.'+key,container[key]))
    if key in row: result.append((key,row[key]))
    return result


def metric_value(row,key):
    entries=locations(row,key)
    if not entries: return None
    values=[None if raw is None else number(raw) for _,raw in entries]
    require(all(value==values[0] for value in values),'report_metric_duplicate_conflict:'+key)
    return values[0]


def period_key(value):
    from semantic_adjudication import period
    if isinstance(value,str):
        week=re.fullmatch(r'(\d{4})-W(\d{2})',value)
        quarter=re.fullmatch(r'(\d{4})-Q([1-4])',value)
        interval=re.fullmatch(r'(\d{4}-\d{2}-\d{2})\s*至\s*(\d{4}-\d{2}-\d{2})',value)
        if week:
            try:
                start=date.fromisocalendar(int(week[1]),int(week[2]),1)
                return start,start+timedelta(days=6)
            except ValueError: raise ValueError('report_metric_period_invalid') from None
        if quarter:
            year,month=int(quarter[1]),(int(quarter[2])-1)*3+1
            return date(year,month,1),date(year+1,1,1)-timedelta(days=1) if month==10 else date(year,month+3,1)-timedelta(days=1)
        if interval: return period(dict(start=interval[1],end=interval[2]))
    try: return period(value)
    except (ValueError,TypeError,KeyError):
        require(isinstance(value,str) and bool(value.strip()),'report_metric_period_missing')
        # Non-date labels can match only literally; never guess 本期/上期 dates.
        return value.strip()


def normalized_claim(value,unit,key):
    require(unit in UNITS[key],'report_metric_unit_unbound:'+key)
    value=number(value)
    return value/100 if unit=='%' else value


def scope_key(package,point):
    root=package.get('scope',{})
    require(isinstance(root,dict),'report_metric_scope_invalid')
    inherited=(root.get('platform'),root.get('store'))
    members=root.get('members',[])
    require(isinstance(members,list) and all(isinstance(m,dict) and
            all(isinstance(m.get(k),str) and bool(m[k]) for k in ('platform','store')) for m in members),
            'report_metric_scope_members_invalid')
    allowed={inherited}|{(m['platform'],m['store']) for m in members}
    nested=point.get('scope',{})
    require(isinstance(nested,dict),'report_metric_scope_invalid')
    values=[]
    for index,field in enumerate(('platform','store')):
        require(field not in point or field not in nested or point[field]==nested[field], 'report_metric_scope_conflict')
        value=point.get(field,nested.get(field,inherited[index]))
        require(value is None or isinstance(value,str),'report_metric_scope_invalid')
        values.append(value)
    require(tuple(values) in allowed,'report_metric_scope_mismatch')
    require('dimensions' not in point or 'dimensions' not in nested or point['dimensions']==nested['dimensions'],
            'report_metric_scope_conflict')
    dimensions=point.get('dimensions',nested.get('dimensions',{}))
    require(isinstance(dimensions,dict) and all(isinstance(k,str) and isinstance(v,str) for k,v in dimensions.items()),
            'report_metric_dimensions_invalid')
    if 'client_scope' in point:
        require(point['client_scope']==package.get('client_scope'),'report_metric_client_mismatch')
    return (*values,json.dumps(dimensions,ensure_ascii=False,sort_keys=True))


def metric_groups(package):
    """Group scopes/dimensions before comparison, sort dates without mutating input."""
    groups={}
    for row in package.get('metrics',[]):
        groups.setdefault(scope_key(package,row),[]).append(row)
    output=[]
    for signature,rows in groups.items():
        periods=[period_key(row.get('period')) for row in rows]
        require(len(periods)==len(set(periods)),'report_metric_duplicate_period')
        if len(rows)>1:
            require(all(isinstance(p,tuple) for p in periods),'report_metric_period_order_unverified')
            rows=[row for _,row in sorted(zip(periods,rows),key=lambda item:item[0])]
            ordered=sorted(periods)
            require(all(a[1]<b[0] for a,b in zip(ordered,ordered[1:])), 'report_metric_period_overlap')
        dimensions=json.loads(signature[2])
        label=' / '.join(str(v) for v in signature[:2] if v)
        if dimensions: label+='；'+'，'.join(f'{k}={v}' for k,v in dimensions.items())
        output.append((label or '当前范围',rows))
    return output


def validate(package):
    rows=package.get('metrics',[])
    require(isinstance(rows,list) and all(isinstance(row,dict) for row in rows),'report_metric_rows_invalid')
    for row in rows:
        for key in KEYS:
            value=metric_value(row,key)
            if value is not None and key in ('visitors','buyers','orders'):
                require(value>=0 and value==value.to_integral_value(),'report_metric_count_invalid:'+key)
    claims=package.get('adjudicated_claims',{})
    require(isinstance(claims,dict),'report_metric_claims_invalid')
    ledger_package=package.get('claim_ledger',{})
    require(isinstance(ledger_package,dict),'report_metric_ledger_invalid')
    ledger=ledger_package.get('claims',[])
    require(isinstance(ledger,list) and all(isinstance(c,dict) for c in ledger),'report_metric_ledger_invalid')
    checks=[]
    for cid,claim in claims.items():
        require(isinstance(claim,dict),'report_metric_claim_invalid')
        key=ALIASES.get(str(claim.get('metric','')).casefold())
        if key is None:
            checks.append(dict(conflict_id=cid,metric=claim.get('metric'),status='unmapped_not_checked'))
            continue  # No supported renderer mapping; never guess or claim coverage.
        signature=scope_key(package,claim)
        selected=[(i,row) for i,row in enumerate(rows) if locations(row,key) and scope_key(package,row)==signature]
        selected_ledger=[c for c in ledger if ALIASES.get(str(c.get('metric','')).casefold())==key and scope_key(package,c)==signature]
        if not selected and not selected_ledger: continue
        points=[(claim.get('period'),claim.get('value'))]
        if 'previous_value' in claim:
            points.append((claim.get('previous_period'),claim['previous_value']))
        for point_period,raw_value in points:
            expected=normalized_claim(raw_value,claim.get('unit'),key)
            period=period_key(point_period)
            matching=[(i,row) for i,row in selected if period_key(row.get('period'))==period]
            matching_ledger=[c for c in selected_ledger if period_key(c.get('period'))==period]
            if point_period==claim.get('period') and selected:
                require(bool(matching),'report_metric_period_unbound:'+key)
            for i,row in matching:
                # Renderer metrics belong to report scope. Explicit other-client
                # or platform rows cannot be silently reconciled as shop totals.
                require(metric_value(row,key)==expected,'report_metric_adjudication_stale:'+key)
            for item in matching_ledger:
                actual=normalized_claim(item.get('value'),item.get('unit'),key)
                require(actual==expected,'report_ledger_adjudication_stale:'+key)
            checks.append(dict(conflict_id=cid,metric=key,period=point_period,
                               status='matched_present_structured_values',
                               metric_rows=[i for i,_ in matching],claim_ids=[c.get('claim_id') for c in matching_ledger]))
    return checks


def validate_delivery_metrics(package):
    """Mandatory production gate: consistency plus provenance for every value."""
    checks=validate(package)
    metric_groups(package)  # No mixed-scope or unordered comparison in renderers.
    ledger=package.get('claim_ledger',{}).get('claims',[])
    by_id={row.get('claim_id'):row for row in ledger}
    require(len(by_id)==len(ledger),'report_metric_claim_id_duplicate')
    def canonical(name): return ALIASES.get(str(name).casefold(),str(name))
    for index,row in enumerate(package.get('metrics',[])):
        signature=scope_key(package,row)
        period=period_key(row.get('period'))
        keys=set(key for key in KEYS if key in row)
        if 'metrics' not in row and 'inputs' not in row:
            metadata={'period','platform','store','scope','dimensions','metric_bindings','metric_units',
                      'label','note','status','gate_status'}
            keys.update(set(row)-metadata)
        for container in ('metrics','inputs'):
            keys.update(row.get(container,{}))
        bindings=row.get('metric_bindings',{})
        units=row.get('metric_units',{})
        require(isinstance(bindings,dict) and set(bindings).issubset(keys), 'report_metric_bindings_invalid')
        require(isinstance(units,dict) and set(units).issubset(keys), 'report_metric_units_invalid')
        for key in sorted(keys):
            value=metric_value(row,key)
            if value is None and key not in bindings:
                checks.append(dict(metric_row=index,metric=key,status='missing_not_plotted'))
                continue
            target=canonical(key)
            if value is not None and target in ('visitors','buyers','orders'):
                require(value>=0 and value==value.to_integral_value(),'report_metric_count_invalid:'+key)
            candidates=[c for c in ledger if canonical(c.get('metric'))==target
                        and period_key(c.get('period'))==period and scope_key(package,c)==signature]
            if key in bindings:
                require(isinstance(bindings[key],str) and bindings[key] in by_id,'report_metric_bound_claim_missing:'+key)
                selected=by_id[bindings[key]]
                require(selected in candidates,'report_metric_claim_identity_mismatch:'+key)
            else:
                require(len(candidates)==1,'report_metric_claim_missing_or_ambiguous:'+key)
                selected=candidates[0]
            if value is None:
                require(selected.get('status')=='unknown' and selected.get('value') is None,'report_metric_missing_claim_mismatch')
            else:
                require(selected.get('status') in ('verified','derived'),'report_metric_claim_not_known:'+key)
                if target in UNITS:
                    expected=normalized_claim(selected.get('value'),selected.get('unit'),target)
                    native_units=tuple(unit for unit in UNITS[target] if unit!='%')
                    require(key not in units or units[key] in native_units,'report_metric_renderer_unit_mismatch:'+key)
                else:
                    require(isinstance(units.get(key),str) and bool(units[key]) and units[key]==selected.get('unit'),
                            'report_metric_custom_unit_required:'+key)
                    expected=number(selected.get('value'))
                require(value==expected,'report_metric_ledger_value_mismatch:'+key)
            checks.append(dict(metric_row=index,metric=key,period=row['period'],claim_id=selected['claim_id'],
                               status='ledger_value_matched' if value is not None else 'unknown_matched'))
    return checks
