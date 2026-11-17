"""Bind business numbers in narrative and actions to claims or declared proposals.

This prevents prose from bypassing the structured metric ledger. It does not
judge whether a proposed target is commercially wise.
"""
import re
from decimal import Decimal, InvalidOperation

from adjudication_guard import require


NUMBER = re.compile(r"(?<![A-Za-z0-9_.-])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:\s*(?:万元|元|%|％|倍|人|单|件|笔))?")
TIME_AFTER = re.compile(r"^\s*(?:天|日|周|月|年|小时|分钟)")
FIELDS = {
    'facts': ('claim',),
    'judgments': ('claim','counter_conditions'),
    'hypotheses': ('claim','verification_method','counter_conditions'),
    'actions': ('action','target','baseline','acceptance','stop_condition'),
}
PROPOSAL_FIELDS = {
    'judgments': {'counter_conditions'},
    'hypotheses': {'claim','verification_method','counter_conditions'},
    'actions': {'action','target','acceptance','stop_condition'},
}
FINANCIAL_UNITS = {'元','万元','%','％','倍'}


def field_texts(item, names):
    for name in names:
        value=item.get(name)
        if isinstance(value,str): yield name,value
        elif isinstance(value,list):
            for index,text in enumerate(value):
                if isinstance(text,str): yield f'{name}[{index}]',text


def business_numbers(text):
    found=[]
    ignored=[m.span() for m in re.finditer(r'(?<!\d)\d{4}[-/]\d{1,2}(?:[-/]\d{1,2})?(?!\d)',text)]
    for match in NUMBER.finditer(text):
        if any(start<=match.start() and match.end()<=end for start,end in ignored): continue
        token=match.group().strip()
        before=text[max(0,match.start()-3):match.start()]
        after=text[match.end():match.end()+4]
        if re.search(r'T\+\s*$',before,re.I) or TIME_AFTER.match(after): continue
        if (match.start()>0 and text[match.start()-1] in '-/' and
                match.end()<len(text) and text[match.end()] in '-/'): continue
        found.append(token)
    return found


def token_value(token):
    compact=token.replace(',','').replace(' ','').replace('％','%')
    unit=''
    for suffix in ('万元','元','%','倍','人','单','件','笔'):
        if compact.endswith(suffix): unit=suffix; compact=compact[:-len(suffix)]; break
    try: value=Decimal(compact)
    except InvalidOperation as exc: raise ValueError('narrative_number_invalid') from exc
    if unit=='万元': value*=Decimal(10000)
    return value,unit


def claim_matches(token,claim):
    value,unit=token_value(token)
    require(claim.get('status') in ('verified','derived') and claim.get('value') is not None,
            'narrative_claim_not_known')
    require(value==Decimal(str(claim['value'])),'narrative_claim_value_mismatch')
    actual=str(claim.get('unit') or '').replace('％','%')
    allowed={'万元':{'元'},'%':{'%'},'倍':{'倍','ratio'},'元':{'元'},
             '人':{'人'},'单':{'单'},'件':{'件'},'笔':{'笔'}}
    if unit: require(actual in allowed[unit],'narrative_claim_unit_mismatch')


def validate_narrative_numbers(report):
    ledger=report.get('claim_ledger',{})
    claims={r.get('claim_id'):r for r in ledger.get('claims',[]) if isinstance(r,dict)}
    checks=[]
    for section,names in FIELDS.items():
        rows=report.get(section,[])
        require(isinstance(rows,list),'narrative_section_invalid:'+section)
        for index,item in enumerate(rows):
            require(isinstance(item,dict),'narrative_item_invalid:'+section)
            detected=[]
            for field,text in field_texts(item,names):
                for occurrence,token in enumerate(business_numbers(text),1):
                    detected.append((field,token,occurrence))
            bindings=item.get('number_bindings',[])
            require(isinstance(bindings,list),'narrative_bindings_invalid')
            declared=[]
            for binding in bindings:
                require(isinstance(binding,dict),'narrative_binding_invalid')
                key=(binding.get('field'),binding.get('token'),binding.get('occurrence'))
                require(isinstance(key[0],str) and isinstance(key[1],str) and
                        type(key[2]) is int and key[2]>=1,'narrative_binding_key_invalid')
                require(key not in declared,'narrative_binding_duplicate')
                declared.append(key)
                kind=binding.get('kind')
                if kind=='claim':
                    claim=claims.get(binding.get('claim_id'))
                    require(isinstance(claim,dict),'narrative_claim_id_missing')
                    claim_matches(str(binding.get('token')),claim)
                    status='claim_bound'
                else:
                    require(kind=='proposal' and section in PROPOSAL_FIELDS and
                            str(binding.get('field')).split('[',1)[0] in PROPOSAL_FIELDS[section],
                            'narrative_proposal_location_forbidden')
                    basis=binding.get('basis_claim_ids')
                    require(isinstance(basis,list) and bool(basis) and len(basis)==len(set(basis)) and
                            all(k in claims and claims[k].get('status') in ('verified','derived') for k in basis),
                            'narrative_proposal_basis_missing')
                    require(isinstance(binding.get('rationale'),str) and bool(binding['rationale'].strip()) and
                            binding.get('label') in ('target','threshold','test_budget','sample_size'),
                            'narrative_proposal_definition_missing')
                    _,unit=token_value(str(binding.get('token')))
                    if section=='actions' and unit in FINANCIAL_UNITS:
                        require(item.get('approval_required') is True and item.get('approval_state')!='not_required',
                                'narrative_financial_proposal_requires_approval')
                    status='proposal_declared'
                checks.append(dict(section=section,index=index,field=key[0],token=key[1],
                                   occurrence=key[2],status=status))
            require(sorted(declared)==sorted(detected),'narrative_number_binding_mismatch:'+section+':'+str(index))
    return dict(status='narrative_numbers_bound',checked=len(checks),checks=checks,
                evidence_kind='structured_number_binding_not_recommendation_quality')
