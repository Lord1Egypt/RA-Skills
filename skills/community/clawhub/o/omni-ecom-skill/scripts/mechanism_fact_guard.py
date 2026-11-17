"""Source-check structural report counts without treating them as sales claims."""
import copy
import re
from narrative_value_guard import validate_narrative_numbers, business_numbers


def validate(facts, package):
    if package.get('client_scope') != 'runtime-acceptance-no-client-data':
        raise ValueError('mechanism_scope_not_authorized')
    count = package.get('report_inventory', {}).get('report_count')
    checked = copy.deepcopy(facts)
    bindings = []
    pattern = re.compile(r'(report_count\s*(?:为|=|:)\s*)([0-9]+)')
    for fact in checked:
        def replace(match):
            if type(count) is not int or int(match[2]) != count:
                raise ValueError('mechanism_report_count_mismatch')
            bindings.append({'fact_id':fact.get('id'),'field':'report_inventory.report_count','value':count})
            return match[1]+'结构计数已复核'
        fact['claim'] = pattern.sub(replace, fact.get('claim', ''))
    # Hashes, byte counts and task/card counts are mechanism observations, not
    # sales claims. They remain in the sealed member evidence for independent
    # review. Economic numbers are never granted that exception.
    economic = re.compile(r'推广|投放|花费|成本|GMV|销售|营业|利润|ROI|ROAS|CPC|转化|客单|UV\s*价值|订单|成交|访客|买家|退款|预算', re.I)
    financial_unit = re.compile(r'\d\s*(?:万元|元|%|％|倍|人|单|件|笔)')
    mechanism = re.compile(r'json|csv|SHA256|task|handoff|report_count|row_count|column_count|chapter|manifest|回执|凭证|契约|目录|字节|表头|字段|行|列', re.I)
    for fact in checked:
        text = fact.get('claim', '')
        context = text
        for claim in package['claim_ledger'].get('claims', []):
            claim_id = claim.get('claim_id')
            if isinstance(claim_id,str) and claim_id:
                context = re.sub(r'(?<![A-Za-z0-9_-])'+re.escape(claim_id)+r'(?![A-Za-z0-9_-])','已登记声明编号',context)
        if business_numbers(text) and (economic.search(context) or financial_unit.search(text) or not mechanism.search(text)):
            validate_narrative_numbers({'facts':[fact],'claim_ledger':package['claim_ledger']})
    return bindings
