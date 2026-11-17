"""Shared normalized ratio definitions, not a certificate of accounting completeness."""
import ast
from decimal import Decimal

from adjudication_guard import require


# metric: numerator, denominator, numerator units, denominator units, output units
RULES={
    'conversion_rate':('buyers','visitors',('人',),('人',),('ratio','%')),
    'orders_per_visitor':('orders','visitors',('单',),('人',),('单/人',)),
    'aov':('gmv','buyers',('元',),('人',),('元/人','元')),
    'uv_value':('gmv','visitors',('元',),('人',),('元/人','元')),
    'refund_rate_amount':('refund_amount','gmv',('元',),('元',),('ratio','%')),
    'roas':('attributed_gmv','ad_spend',('元',),('元',),('倍','ratio')),
    'net_roas':('attributed_net_sales','ad_spend',('元',),('元',),('倍','ratio')),
    'contribution_roas':('attributed_contribution_before_ad','ad_spend',('元',),('元',),('倍','ratio')),
    'roi':('profit','total_cost',('元',),('元',),('ratio','%')),
}
ALIASES={**{key:key for key in RULES},
    'conversion':'conversion_rate','转化率':'conversion_rate','支付转化率':'conversion_rate',
    'paid_buyers':'buyers','支付买家数':'buyers','buyers':'buyers','visitors':'visitors','uv':'visitors','访客':'visitors','访客数':'visitors',
    'orders':'orders','订单数':'orders','每访客订单数':'orders_per_visitor',
    'gmv':'gmv','销售额':'gmv','支付金额':'gmv','客单价':'aov',
    'gmv_per_visitor':'uv_value','访客价值':'uv_value','uv价值':'uv_value',
    '退款率':'refund_rate_amount','refund_rate':'refund_rate_amount','退款金额':'refund_amount','refund_amount':'refund_amount',
    '归因gmv':'attributed_gmv','attributed_gmv':'attributed_gmv',
    '广告花费':'ad_spend','推广花费':'ad_spend','投放花费':'ad_spend','ad_spend':'ad_spend',
    '利润':'profit','profit':'profit','总成本':'total_cost','total_cost':'total_cost',
    '净roas':'net_roas','扣退款roas':'net_roas',
    '贡献roas':'contribution_roas','扣变动成本roas':'contribution_roas',
    '归因净销售额':'attributed_net_sales','归因退款额':'attributed_refund',
    '归因优惠':'attributed_discount','归因商品成本':'attributed_product_cost',
    '归因平台费用':'attributed_platform_fee','归因履约成本':'attributed_fulfillment_cost',
    '广告前归因贡献额':'attributed_contribution_before_ad'}


def canonical(value):
    value=str(value).strip().casefold()
    return ALIASES.get(value,value)


def definition_errors(row,by_id,index):
    key=canonical(row.get('metric'))
    if key not in RULES or row.get('status')=='unknown': return []
    errors=[]
    def check(ok,reason):
        if not ok: errors.append(f'claim_{index}_{reason}')
    numerator,denominator,num_units,den_units,out_units=RULES[key]
    check(row.get('status')=='derived','normalized_ratio_requires_derived')
    check(row.get('unit') in out_units,'ratio_output_unit_invalid')
    formula=row.get('formula')
    if not isinstance(formula,dict): return errors+[f'claim_{index}_ratio_formula_missing']
    check(canonical(formula.get('numerator'))==numerator and canonical(formula.get('denominator'))==denominator,
          'ratio_definition_mismatch:'+key)
    # A backend field named ROI may be an advertising ROAS. Its source field
    # name is retained; it cannot rename the normalized metric or formula.
    if key in ('roi','roas','net_roas','contribution_roas'):
        check(canonical(formula.get('name'))==key,'ratio_name_mismatch:'+key)
    inputs=row.get('inputs')
    if not isinstance(inputs,list) or len(inputs)!=2 or not all(isinstance(i,str) and i in by_id for i in inputs):
        return errors+[f'claim_{index}_ratio_inputs_invalid']
    selected=[by_id[i] for i in inputs]
    numerators=[c for c in selected if canonical(c.get('metric'))==numerator]
    denominators=[c for c in selected if canonical(c.get('metric'))==denominator]
    check(len(numerators)==1 and len(denominators)==1,'ratio_input_identity_mismatch')
    if len(numerators)==len(denominators)==1:
        check(numerators[0].get('unit') in num_units and denominators[0].get('unit') in den_units,
              'ratio_input_unit_mismatch')
    currencies=[c.get('currency') for c in [row,*selected]]
    if any(c is not None for c in currencies):
        check(all(isinstance(c,str) and bool(c) and c==currencies[0] for c in currencies),'ratio_currency_mismatch')
    return errors


def validate_expression(row,claims,bindings,values,tree,result):
    key=canonical(row.get('metric'))
    if key not in RULES: return False
    numerator,denominator,*_=RULES[key]
    formula=row['formula']; left,right=formula['numerator'],formula['denominator']
    body=tree.body
    percent=row['unit']=='%'
    if percent:
        require(isinstance(body,ast.BinOp) and isinstance(body.op,ast.Mult),'claim_percent_expression_requires_scale')
        if isinstance(body.right,ast.Constant) and type(body.right.value) in (int,float) and body.right.value==100:
            body=body.left
        elif isinstance(body.left,ast.Constant) and type(body.left.value) in (int,float) and body.left.value==100:
            body=body.right
        else: raise ValueError('claim_percent_expression_requires_scale')
    require(isinstance(body,ast.BinOp) and isinstance(body.op,ast.Div) and
            isinstance(body.left,ast.Name) and isinstance(body.right,ast.Name) and
            body.left.id==left and body.right.id==right,'claim_ratio_expression_mismatch')
    require(left in bindings and right in bindings and
            canonical(claims[bindings[left]]['metric'])==numerator and
            canonical(claims[bindings[right]]['metric'])==denominator,'claim_ratio_binding_mismatch')
    require(values[right]>0,'claim_ratio_denominator_not_positive')
    if key not in ('roi','contribution_roas'):
        require(values[left]>=0,'claim_ratio_numerator_negative')
    if key=='conversion_rate':
        require(values[left]<=values[right],'claim_buyers_exceed_visitors')
        require(0<=result<=(Decimal(100) if percent else Decimal(1)),'claim_conversion_out_of_range')
    return True


ADJUDICATION_NAMES={'转化率':'conversion_rate','客单价':'aov','退款率':'refund_rate_amount',
                    'ROAS':'roas','ROI':'roi','UV价值':'uv_value'}
ADJUDICATION_RECIPES={name:(f'{RULES[key][0]} / {RULES[key][1]}',
    {RULES[key][0]:RULES[key][2][0],RULES[key][1]:RULES[key][3][0]},RULES[key][4][0])
    for name,key in ADJUDICATION_NAMES.items()}
