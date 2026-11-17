"""Bind declared metric context to selected cells in the same source file.

This checks local exported labels, not acquisition authenticity or full-period coverage.
"""
import csv
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

from adjudication_guard import require, sha
from report_metric_guard import period_key


def expected_context(payload, row):
    base=payload.get('scope',{}); own=row.get('scope',{})
    require(isinstance(base,dict) and isinstance(own,dict),'source_context_scope_invalid')
    expected={'period':row.get('period'),'unit':row.get('unit')}
    for key in ('platform','store','currency'):
        require(key not in row or key not in own or row[key]==own[key],'source_context_scope_conflict')
        value=row.get(key,own.get(key,base.get(key)))
        if value is not None: expected[key]=value
    for declared in (base.get('dimensions'),own.get('dimensions'),row.get('dimensions')):
        require(declared is None or isinstance(declared,dict),'source_context_dimensions_invalid')
    dimensions=row.get('dimensions',own.get('dimensions',base.get('dimensions',{})))
    require(isinstance(dimensions,dict) and all(isinstance(k,str) and isinstance(v,str) for k,v in dimensions.items()),
            'source_context_dimensions_invalid')
    require('dimensions' not in row or 'dimensions' not in own or row['dimensions']==own['dimensions'],
            'source_context_scope_conflict')
    require('dimensions' not in row or 'dimensions' not in base or row['dimensions']==base['dimensions'],
            'source_context_scope_conflict')
    require('dimensions' not in own or 'dimensions' not in base or own['dimensions']==base['dimensions'],
            'source_context_scope_conflict')
    expected.update({'dimensions.'+k:v for k,v in dimensions.items()})
    if payload.get('source_context_policy')=='required':
        require('platform' in expected and 'store' in expected,'source_context_store_platform_required')
    require(all(isinstance(v,str) and bool(v.strip()) for v in expected.values()),'source_context_expected_missing')
    return expected


def cell(raw):
    match=re.fullmatch(r'([A-Z]+)([1-9][0-9]*)',str(raw))
    require(match is not None,'source_context_cell_invalid')
    column=0
    for letter in match[1]: column=column*26+ord(letter)-64
    row=int(match[2])
    require(column<=16384 and row<=1048576,'source_context_cell_invalid')
    return row,column-1


def pointer_parent(data, pointer):
    require(isinstance(pointer,str) and pointer.startswith('/'),'source_context_pointer_invalid')
    for part in pointer[1:].split('/')[:-1]:
        key=part.replace('~1','/').replace('~0','~')
        if isinstance(data,list):
            require(bool(re.fullmatch(r'0|[1-9][0-9]*',key)),'source_context_pointer_invalid')
            data=data[int(key)]
        else: data=data[key]
    require(isinstance(data,dict),'source_context_record_required')
    return data


def read_values(path, source, contexts, batch=None):
    if path.suffix.lower()=='.json':
        record=pointer_parent(batch.json_value(path) if batch is not None else json.loads(path.read_text(encoding='utf-8-sig')),source.get('pointer'))
        values={}
        for key,spec in contexts.items():
            require(isinstance(spec,dict) and set(spec)=={'field'} and isinstance(spec['field'],str),
                    'source_context_json_sibling_required')
            require(spec['field'] in record,'source_context_field_missing')
            values[key]=[record[spec['field']]]
        return values
    selection=str(source.get('range','')).split(':')
    start,_=cell(selection[0]); end,_=cell(selection[-1])
    header=source.get('header_row',1)
    require(type(header) is int and 1<=header<start<=end,'source_context_rows_invalid')
    wanted={header}; selectors={}
    for key,spec in contexts.items():
        require(isinstance(spec,dict),'source_context_selector_invalid')
        require(isinstance(spec.get('field'),str) and bool(spec['field'].strip()),'source_context_field_missing')
        if set(spec)=={'column','field'}:
            _,column=cell(str(spec['column'])+'1')
            selectors[key]=('column',column,spec['field']); wanted.update(range(start,end+1))
        else:
            require(set(spec)=={'cell','label_cell','field'},'source_context_selector_invalid')
            value_cell,label_cell=cell(spec['cell']),cell(spec['label_cell'])
            require(value_cell[0]<header and label_cell[0]<header,'source_context_metadata_must_precede_header')
            require(value_cell!=label_cell,'source_context_metadata_label_overlaps_value')
            selectors[key]=('metadata',value_cell,label_cell,spec['field'])
            wanted.update([value_cell[0],label_cell[0]])
    rows={}; book=None
    try:
        suffix=path.suffix.lower()
        snapshot=batch.rows(path,source) if batch is not None else None
        if snapshot is not None:
            iterator=iter(snapshot)
        elif suffix=='.csv':
            book=path.open(encoding=source.get('encoding','utf-8-sig'),newline=''); iterator=csv.reader(book)
        elif suffix=='.xlsx':
            import openpyxl
            book=openpyxl.load_workbook(path,read_only=True,data_only=True)
            require(source.get('sheet') in book.sheetnames,'source_context_sheet_missing')
            iterator=book[source['sheet']].iter_rows(values_only=True)
        elif suffix=='.xls':
            import xlrd
            book=xlrd.open_workbook(str(path),on_demand=True)
            require(source.get('sheet') in book.sheet_names(),'source_context_sheet_missing')
            sheet=book.sheet_by_name(source['sheet']); iterator=(sheet.row_values(i) for i in range(sheet.nrows))
        else: raise ValueError('source_context_format_unsupported')
        last=max(wanted)
        for index,row in enumerate(iterator,1):
            if index in wanted: rows[index]=row
            if index>=last: break
    finally:
        if book is not None:
            if hasattr(book,'close'): book.close()
            elif hasattr(book,'release_resources'): book.release_resources()
    def value(position):
        r,c=position
        require(r in rows and c<len(rows[r]),'source_context_cell_missing')
        return rows[r][c]
    output={}
    for key,spec in selectors.items():
        if spec[0]=='column':
            _,column,field=spec
            require(value((header,column))==field and rows[header].count(field)==1,'source_context_field_mismatch')
            output[key]=[value((r,column)) for r in range(start,end+1)]
        else:
            _,position,label,field=spec
            require(value(label)==field,'source_context_metadata_label_mismatch')
            output[key]=[value(position)]
    return output


def validate_context(payload, row, root, batch=None):
    policy=payload.get('source_context_policy','legacy_unbound')
    require(policy in ('legacy_unbound','required'),'source_context_policy_invalid')
    source=row['source_ref']; contexts=source.get('contexts')
    if contexts is None:
        require(policy!='required','source_context_required')
        return {'status':'source_context_unbound'}
    expected=expected_context(payload,row)
    require(isinstance(contexts,dict) and bool(contexts) and set(contexts)==set(expected),
            'source_context_keys_mismatch')
    path=(root/source['source_file']).resolve()
    require(path.is_relative_to(root) and path.is_file(),'source_context_path_invalid')
    digest=batch.digest(path) if batch is not None else sha(path)
    require(digest==str(source['source_sha256']).lower(),'source_context_hash_mismatch')
    values=read_values(path,source,contexts,batch)
    mode=source.get('period_mode','exact')
    require(mode in ('exact','contained'),'source_context_period_mode_invalid')
    observed={}
    for key,raw_values in values.items():
        require(bool(raw_values),'source_context_values_missing')
        for raw in raw_values:
            require(isinstance(raw,(str,date,datetime)) and bool(str(raw).strip()),'source_context_value_invalid')
            if key=='period':
                actual,wanted=period_key(raw),period_key(expected[key])
                require(isinstance(actual,tuple) and isinstance(wanted,tuple),'source_context_period_unparsed')
                matches=actual==wanted if mode=='exact' else wanted[0]<=actual[0]<=actual[1]<=wanted[1]
            else: matches=str(raw).strip()==expected[key].strip()
            require(matches,'source_context_value_mismatch:'+key)
        observed[key]=sorted({v.isoformat() if isinstance(v,(date,datetime)) else str(v) for v in raw_values})
    coverage_result={'status':'exact_period_label_checked'}
    if mode=='contained':
        coverage=source.get('period_coverage')
        require(isinstance(coverage,dict) and coverage.get('frequency')=='daily' and
                coverage.get('status')=='complete_no_missing_dates',
                'source_context_period_coverage_required')
        wanted=period_key(expected['period'])
        require(isinstance(wanted,tuple),'source_context_period_unparsed')
        days=(wanted[1]-wanted[0]).days+1
        require(1<=days<=3660,'source_context_period_coverage_too_large')
        actual=[]
        for raw in values['period']:
            parsed=period_key(raw)
            require(isinstance(parsed,tuple) and parsed[0]==parsed[1],
                    'source_context_daily_period_required')
            actual.append(parsed[0])
        require(len(actual)==len(set(actual)),'source_context_period_duplicate_date')
        expected_days={wanted[0]+timedelta(days=index) for index in range(days)}
        require(set(actual)==expected_days,'source_context_period_incomplete')
        coverage_result={'status':'complete_daily_period_verified','expected_days':days,
                         'observed_days':len(actual),'start':wanted[0].isoformat(),
                         'end':wanted[1].isoformat()}
    if batch is None:
        require(sha(path)==digest,'source_context_changed_during_read')
    return dict(status='source_context_verified',period_mode=mode,observed=observed,
                period_coverage=coverage_result,
                evidence_kind=('local_export_labels_and_complete_daily_period_not_authenticity'
                    if mode=='contained' else 'local_export_labels_not_authenticity_or_period_coverage'))


def summary(checks):
    originals=[c for c in checks if c.get('status')=='source_recomputed']
    verified=sum(c.get('source_context',{}).get('status')=='source_context_verified' for c in originals)
    return dict(status=('no_verified_source_labels' if not originals else
                        'all_verified_source_labels_checked' if verified==len(originals) else
                        'some_source_labels_unbound'),
                verified_sources=len(originals),context_checked=verified,context_unbound=len(originals)-verified)
