"""Source-backed caliber and trend adjudication against the issued baseline.

Checks declared metric semantics and original period cells, not causal validity
or independent authenticity of platform exports.
"""
import ast
import calendar
import csv
import json
import re
from datetime import date,datetime,timedelta
from pathlib import Path

from adjudication_guard import require,number,calculate,cell_value,sha,fingerprint
from metric_semantics import ADJUDICATION_RECIPES,canonical

RECIPES={
    'GMV':('gmv',{'gmv':'元'},'元'),
    '访客':('visitors',{'visitors':'人'},'人'),
    '访客数':('visitors',{'visitors':'人'},'人'),
    '净销售':('gmv - refund_amount',{'gmv':'元','refund_amount':'元'},'元'),
    **ADJUDICATION_RECIPES,
}


def period(value):
    """Explicit exported year/month/day; ambiguous dates and serials fail closed."""
    if isinstance(value,datetime): value=value.date()
    if isinstance(value,date): return value,value
    if isinstance(value,dict):
        require(set(value)=={'start','end'},'adjudication_period_invalid')
        start,end=date.fromisoformat(value['start']),date.fromisoformat(value['end'])
        require(start<=end,'adjudication_period_invalid')
        return start,end
    value=str(value).strip()
    match=re.fullmatch(r'(\d{4})[-/]?(\d{2})(?:[-/]?(\d{2}))?',value)
    if match:
        year,month=int(match[1]),int(match[2]); day=match[3]
        if day: return date(year,month,int(day)),date(year,month,int(day))
        return date(year,month,1),date(year,month,calendar.monthrange(year,month)[1])
    if re.fullmatch(r'\d{4}',value): return date(int(value),1,1),date(int(value),12,31)
    raise ValueError('adjudication_period_invalid')


def pointer(value,raw):
    require(isinstance(raw,str) and raw.startswith('/'),'adjudication_period_pointer_missing')
    try:
        for part in raw[1:].split('/'):
            part=part.replace('~1','/').replace('~0','~')
            value=value[int(part)] if isinstance(value,list) else value[part]
        return value
    except (KeyError,IndexError,TypeError,ValueError) as exc:
        raise ValueError('adjudication_period_cell_missing') from exc


def period_cells(path,spec):
    if path.suffix.lower()=='.json':
        return [pointer(json.loads(path.read_text(encoding='utf-8-sig')),spec.get('period_pointer'))]
    column=spec.get('period_column')
    require(isinstance(column,str) and bool(column),'adjudication_period_column_missing')
    book=None
    try:
        if path.suffix.lower()=='.csv':
            with path.open(encoding=spec.get('encoding','utf-8-sig'),newline='') as f:
                rows=list(csv.reader(f))
            headings=rows[0] if rows else []; iterator=iter(rows[1:])
        elif path.suffix.lower()=='.xlsx':
            import openpyxl
            book=openpyxl.load_workbook(path,read_only=True,data_only=True)
            iterator=book[spec['sheet']].iter_rows(min_row=spec['header_row'],values_only=True)
            headings=next(iterator,())
        elif path.suffix.lower()=='.xls':
            import xlrd
            book=xlrd.open_workbook(str(path),on_demand=True)
            sheet=book.sheet_by_name(spec['sheet'])
            headings=sheet.row_values(spec['header_row']-1)
            def xls_rows():
                for index in range(spec['header_row'],sheet.nrows):
                    yield [xlrd.xldate.xldate_as_datetime(c.value,book.datemode).date()
                           if c.ctype==xlrd.XL_CELL_DATE else c.value for c in sheet.row(index)]
            iterator=xls_rows()
        else: raise ValueError('adjudication_period_format_unsupported')
        require(headings.count(column)==1,'adjudication_period_column_missing_or_ambiguous')
        index=headings.index(column); selected=set(spec['rows'])
        values=[]
        for n,row in enumerate(iterator):
            if n in selected:
                require(index<len(row),'adjudication_period_cell_missing')
                values.append(row[index])
        require(len(values)==len(selected),'adjudication_period_rows_missing')
        return values
    finally:
        if book is not None:
            if hasattr(book,'close'): book.close()
            else: book.release_resources()


def check_period_cells(path,spec,expected):
    intervals=sorted(period(value) for value in period_cells(path,spec))
    require(bool(intervals) and all(expected[0]<=start<=end<=expected[1] for start,end in intervals),
            'adjudication_source_period_mismatch')
    edge=expected[0]
    for start,end in intervals:
        require(start<=edge,'adjudication_source_period_gap')
        edge=max(edge,end+timedelta(days=1))
    require(edge==expected[1]+timedelta(days=1),'adjudication_source_period_incomplete')


def contract_for(metric,baseline):
    require(metric in RECIPES,'adjudication_metric_recipe_missing')
    contract=baseline.get('metric_contract',{}).get(metric)
    require(isinstance(contract,dict) and all(isinstance(contract.get(k),str) and contract[k].strip()
            for k in ('definition','formula','unit','denominator','dedupe_rule','attribution_window')),
            'adjudication_caliber_incomplete')
    calc=contract.get('calculation',{})
    expected,units,result_unit=RECIPES[metric]
    if result_unit=='ratio':
        require(contract['unit'] in ('ratio','%'),'adjudication_unit_mismatch')
        if contract['unit']=='%': expected='('+expected+') * 100'
    else: require(contract['unit']==result_unit,'adjudication_unit_mismatch')
    expression=calc.get('expression')
    require(isinstance(expression,str) and len(expression)<=2000,'adjudication_expression_missing')
    try:
        require(ast.dump(ast.parse(expression,mode='eval'))==ast.dump(ast.parse(expected,mode='eval')),
                'adjudication_metric_formula_mismatch')
    except (SyntaxError,RecursionError) as exc: raise ValueError('adjudication_expression_invalid') from exc
    bindings=calc.get('inputs')
    require(isinstance(bindings,dict) and set(bindings)==set(units),'adjudication_metric_inputs_mismatch')
    for name,spec in bindings.items():
        require(isinstance(spec,dict) and spec.get('unit')==units[name] and
                isinstance(spec.get('source_field'),str) and bool(spec['source_field']),
                'adjudication_input_definition_invalid')
        require(spec.get('aggregation') in ('value','sum'),'adjudication_aggregation_invalid')
        if units[name]=='人': require(spec['aggregation']=='value','adjudication_people_cannot_sum')
    return contract,expression,bindings


def measure_accounting(data,contract,expression,resolve,report,baseline_scope):
    """ROI decisions use the report's reconciled ledger, not free-text costs."""
    from claim_source_guard import validate_report_sources
    from accounting_guard import scope
    require(isinstance(report,dict),'adjudication_accounting_report_required')
    require(set(data)=={'period','value','accounting_claim_id'},'adjudication_accounting_binding_required')
    root=resolve('report.md').parent
    gate=validate_report_sources(report,root,resolve('report.md').read_text(encoding='utf-8-sig'),require_context=True)
    payload=json.loads((root/gate['claims_file']).read_text(encoding='utf-8-sig'))
    claims={r['claim_id']:r for r in payload['claims']}
    row=claims.get(data['accounting_claim_id'])
    require(isinstance(row,dict) and canonical(row.get('metric'))=='roi' and row.get('status')=='derived',
            'adjudication_accounting_claim_invalid')
    require(row['unit']==contract['unit'] and period(row['period'])==period(data['period']),
            'adjudication_accounting_period_unit_mismatch')
    actual_scope=scope(payload,row)
    require(isinstance(baseline_scope,dict) and all(baseline_scope.get(k)==actual_scope[i]
            and bool(actual_scope[i]) for k,i in (('platform',2),('store',3))),
            'adjudication_accounting_baseline_scope_mismatch')
    require(json.loads(actual_scope[4])==baseline_scope.get('dimensions',{}),
            'adjudication_accounting_baseline_dimensions_mismatch')
    if baseline_scope.get('currency') is not None:
        require(actual_scope[5]==baseline_scope['currency'] and bool(actual_scope[5]),
                'adjudication_accounting_baseline_currency_mismatch')
    checks={r['claim_id']:r for r in gate['source_checks']}
    checked=checks[row['claim_id']]
    require(checked.get('accounting',{}).get('status')=='declared_source_bound_operating_perimeter_reconciled',
            'adjudication_accounting_not_reconciled')
    values={canonical(claims[key]['metric']):number(checks[key]['value']) for key in row['inputs']}
    actual=calculate(expression,values)
    require(actual==number(checked['value'])==number(data['value']),'adjudication_measurement_value_mismatch')
    sources={str(root/item['file']):item['sha256'] for item in gate['inputs']}
    return actual,period(data['period']),values,sources


def measure(data,contract,expression,bindings,resolve,inventory,report=None,baseline_scope=None):
    require(isinstance(data,dict),'adjudication_measurement_missing')
    window=period(data.get('period'))
    if 'profit' in bindings:
        return measure_accounting(data,contract,expression,resolve,report,baseline_scope)
    specs=data.get('inputs')
    require(isinstance(specs,dict) and set(specs)==set(bindings),'adjudication_measurement_inputs_missing')
    values,sources={},{}
    for name,spec in specs.items():
        require(isinstance(spec,dict),'adjudication_input_invalid')
        rows=[r for r in inventory.get('reports',[]) if r.get('report_id')==spec.get('report_id')]
        require(len(rows)==1,'adjudication_source_id_unknown')
        entry=rows[0]; path=resolve(spec.get('file'))
        declared=entry.get('file_path')
        require(isinstance(declared,str) and bool(declared),'adjudication_inventory_path_missing')
        declared_path=Path(declared).resolve() if Path(declared).is_absolute() else resolve(declared)
        require(path==declared_path and spec.get('sha256')==entry.get('sha256')==sha(path),
                'adjudication_source_inventory_mismatch')
        binding=bindings[name]
        source_field=spec.get('pointer') if path.suffix.lower()=='.json' else spec.get('column')
        require(source_field==binding['source_field'] and spec.get('aggregation','value')==binding['aggregation'],
                'adjudication_source_field_mismatch')
        value,_,original=cell_value(spec,resolve,{path.name})
        # Profit may be negative. Counts, costs and these sales/refund inputs may not.
        require(name=='profit' or value>=0,'adjudication_negative_input')
        if binding['unit']=='人': require(value==value.to_integral_value(),'adjudication_people_not_integer')
        check_period_cells(path,spec,window)
        require(sha(path)==original,'recompute_source_changed')
        values[name]=value; sources[str(path)]=original
    if 'buyers' in values and 'visitors' in values:
        require(values['buyers']<=values['visitors'],'adjudication_buyers_exceed_visitors')
    actual=calculate(expression,values)
    require(actual==number(data.get('value')),'adjudication_measurement_value_mismatch')
    return actual,window,values,sources


def validate_semantic(conflict,row,report,resolve,baseline,inventory,baseline_sha256):
    metric=conflict.get('metric'); cid=conflict['conflict_id']
    require(isinstance(baseline,dict) and isinstance(inventory,dict),'adjudication_baseline_required')
    require(row.get('baseline_sha256')==baseline_sha256 and bool(baseline_sha256),'adjudication_baseline_changed')
    contract,expression,bindings=contract_for(metric,baseline)
    require(row.get('metric')==metric and row.get('unit')==contract['unit'],'adjudication_metric_scope_mismatch')
    current,window,values,sources=measure(row.get('current'),contract,expression,bindings,resolve,inventory,report,baseline.get('scope'))
    require(window==period(baseline.get('scope',{}).get('period')),'adjudication_current_period_mismatch')
    expected=dict(metric=metric,unit=contract['unit'],value=str(current),period=row['current']['period'],
                  baseline_sha256=baseline_sha256,caliber_sha256=fingerprint(contract))
    if row['method']=='trend_recomputation':
        require(conflict['type']=='direction','adjudication_method_type_mismatch')
        previous,prior,prior_values,prior_sources=measure(row.get('previous'),contract,expression,bindings,resolve,inventory,report,baseline.get('scope'))
        sources.update(prior_sources)
        require(prior[1]<window[0],'adjudication_periods_overlap_or_reversed')
        require(isinstance(row.get('comparability_note'),str) and bool(row['comparability_note'].strip()),
                'adjudication_comparability_missing')
        direction='up' if current>previous else 'down' if current<previous else 'flat'
        require(row.get('direction')==direction,'adjudication_direction_mismatch')
        expected.update(previous_value=str(previous),previous_period=row['previous']['period'],direction=direction,
                        absolute_change=str(current-previous),comparability_note=row['comparability_note'],
                        current_days=(window[1]-window[0]).days+1,previous_days=(prior[1]-prior[0]).days+1)
        values.update({'previous_'+k:v for k,v in prior_values.items()})
        values.update(previous=previous,change=current-previous)
    else:
        require(row['method']=='caliber_recomputation' and conflict['type']=='caliber','adjudication_method_type_mismatch')
    claim=report.get('adjudicated_claims',{}).get(cid,{})
    require(all(number(claim.get(k))==number(v) if k in ('value','previous_value','absolute_change') else claim.get(k)==v
                for k,v in expected.items()),'adjudication_semantic_report_stale')
    return dict(conflict_id=cid,status='recomputed_against_declared_caliber',method=row['method'],**expected),sources,values,current
