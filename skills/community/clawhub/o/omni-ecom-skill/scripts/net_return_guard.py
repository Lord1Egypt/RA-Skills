"""Matched-refund advertising return; never a profit or full-cost metric."""
import ast

from adjudication_guard import require
from metric_semantics import canonical
from accounting_guard import scope


METRICS = {'net_roas', 'attributed_net_sales', 'attributed_contribution_before_ad',
           'contribution_roas'}
CONTRIBUTION_INPUTS = {'attributed_net_sales', 'attributed_discount',
                       'attributed_product_cost', 'attributed_platform_fee',
                       'attributed_fulfillment_cost'}


def _subtraction_chain(body):
    deductions=[]
    while isinstance(body,ast.BinOp) and isinstance(body.op,ast.Sub) and isinstance(body.right,ast.Name):
        deductions.append(body.right.id)
        body=body.left
    return body.id if isinstance(body,ast.Name) else None, deductions


def definition(row, claims, payload=None):
    metric = canonical(row.get('metric'))
    if metric not in METRICS or row.get('status') == 'unknown': return
    require(row.get('status') == 'derived', 'net_return_requires_derivation')
    inputs = row.get('inputs')
    expected_count = 5 if metric == 'attributed_contribution_before_ad' else 2
    require(isinstance(inputs,list) and len(inputs)==expected_count and
            all(isinstance(i,str) and i in claims for i in inputs), 'net_return_inputs_missing')
    by_metric = {canonical(claims[i].get('metric')): claims[i] for i in inputs}
    if metric == 'attributed_net_sales':
        expected = {'attributed_gmv','attributed_refund'}
    elif metric == 'attributed_contribution_before_ad':
        expected = CONTRIBUTION_INPUTS
    elif metric == 'contribution_roas':
        expected = {'attributed_contribution_before_ad','ad_spend'}
    else:
        expected = {'attributed_net_sales','ad_spend'}
    require(set(by_metric)==expected, 'net_return_input_metric_mismatch')
    formula = row.get('formula')
    require(isinstance(formula,dict), 'net_return_formula_missing')
    if metric=='attributed_net_sales':
        require(row.get('unit')=='元' and all(c.get('unit')=='元' for c in by_metric.values()),
                'net_return_unit_mismatch')
        require(canonical(formula.get('name'))=='attributed_net_sales' and
                canonical(formula.get('numerator'))=='attributed_gmv' and
                canonical(formula.get('denominator'))=='attributed_refund', 'net_return_definition_mismatch')
    elif metric=='attributed_contribution_before_ad':
        require(row.get('unit')=='元' and all(c.get('unit')=='元' for c in by_metric.values()),
                'net_return_unit_mismatch')
        require(canonical(formula.get('name'))=='attributed_contribution_before_ad',
                'net_return_definition_mismatch')
    attribution = row.get('attribution')
    require(isinstance(attribution,dict), 'net_return_attribution_missing')
    keys = ('source_id','window','level','refund_basis')
    require(all(isinstance(attribution.get(k),str) and bool(attribution[k].strip()) for k in keys),
            'net_return_attribution_missing')
    require(attribution['refund_basis']=='matched_attributed_sales', 'net_return_refund_basis_mismatch')
    from acquisition_guard import validate as validate_acquisition
    acquisition=validate_acquisition(attribution,payload)
    if metric in {'attributed_contribution_before_ad','contribution_roas'}:
        require(attribution.get('cost_basis')=='matched_attributed_sales' and
                isinstance(attribution.get('reconciliation_id'),str) and
                bool(attribution['reconciliation_id'].strip()), 'net_return_cost_reconciliation_missing')
        keys += ('cost_basis','reconciliation_id')
    for item in [row,*by_metric.values()]:
        actual = item.get('attribution')
        require(isinstance(actual,dict) and all(actual.get(k)==attribution[k] for k in keys),
                'net_return_attribution_mismatch')
        require(isinstance(item.get('source_ref'),dict) and
                item['source_ref'].get('source_id')==attribution['source_id'], 'net_return_source_mismatch')
    return acquisition


def validate(payload, row, claims, bindings, values, tree, result):
    metric = canonical(row.get('metric'))
    if metric not in METRICS: return None
    acquisition=definition(row,claims,payload)
    for key in row['inputs']:
        require(scope(payload,row)==scope(payload,claims[key]), 'net_return_scope_mismatch')
    if metric=='attributed_net_sales':
        left,right=row['formula']['numerator'],row['formula']['denominator']
        body=tree.body
        require(isinstance(body,ast.BinOp) and isinstance(body.op,ast.Sub) and
                isinstance(body.left,ast.Name) and isinstance(body.right,ast.Name) and
                body.left.id==left and body.right.id==right,'net_return_expression_mismatch')
        require(left in bindings and right in bindings and
                canonical(claims[bindings[left]]['metric'])=='attributed_gmv' and
                canonical(claims[bindings[right]]['metric'])=='attributed_refund', 'net_return_binding_mismatch')
        require(values[left]>=0 and values[right]>=0 and values[right]<=values[left],
                'net_return_refund_out_of_range')
    elif metric=='attributed_contribution_before_ad':
        base,deductions=_subtraction_chain(tree.body)
        require(base in bindings and canonical(claims[bindings[base]]['metric'])=='attributed_net_sales' and
                {canonical(claims[bindings[name]]['metric']) for name in deductions}==
                CONTRIBUTION_INPUTS-{'attributed_net_sales'} and len(deductions)==4,
                'net_return_contribution_expression_mismatch')
        require(all(values[name]>=0 for name in values), 'net_return_contribution_input_negative')
    elif metric=='contribution_roas':
        require(canonical(claims[bindings[row['formula']['numerator']]]['metric'])==
                'attributed_contribution_before_ad', 'net_return_contribution_binding_mismatch')
    return dict(status='matched_refund_return_recomputed', profit_checked=False,
                acquisition=acquisition,
                return_kind=metric, attribution=row['attribution'], value=str(result))
