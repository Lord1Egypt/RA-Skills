"""Reconcile a declared operating-profit perimeter against actual ledger inputs.

This is local evidence reconciliation, not an independent accounting audit.
"""
import ast
import json
import re
from datetime import datetime
from decimal import Decimal

from adjudication_guard import require
from metric_semantics import canonical


COST_METRICS = ('product_cost', 'ad_spend', 'platform_fee', 'fulfillment_cost',
                'inventory_loss', 'tax_cost', 'other_operating_cost')
METHOD = 'net_operating_profit_over_operating_cost'
ACCOUNTING_BASES = {'accrual', 'cash', 'platform_settlement'}
COST_TREATMENTS = {'direct_source', 'explicit_zero', 'allocated'}
PERIMETER_COMPLETENESS = 'declared_complete_for_listed_perimeter'
AUTHENTICITY_BOUNDARY = 'source_bound_not_independently_authenticated'
ALLOCATION_METHOD = 'proportional_actual_base'


def scope(payload, row):
    base = payload.get('scope', {})
    own = row.get('scope', {})
    require(isinstance(base, dict) and isinstance(own, dict), 'accounting_scope_invalid')
    values = []
    for key in ('platform', 'store'):
        require(key not in row or key not in own or row[key] == own[key],
                'accounting_scope_conflict')
        values.append(row.get(key, own.get(key, base.get(key))))
    for declared in (base.get('dimensions'), own.get('dimensions'), row.get('dimensions')):
        require(declared is None or isinstance(declared, dict), 'accounting_dimensions_invalid')
    dimensions = row.get('dimensions', own.get('dimensions', base.get('dimensions', {})))
    require('dimensions' not in row or 'dimensions' not in own or row['dimensions'] == own['dimensions'],
            'accounting_scope_conflict')
    require('dimensions' not in row or 'dimensions' not in base or row['dimensions'] == base['dimensions'],
            'accounting_scope_conflict')
    require('dimensions' not in own or 'dimensions' not in base or own['dimensions'] == base['dimensions'],
            'accounting_scope_conflict')
    currency = row.get('currency', own.get('currency', base.get('currency')))
    require('currency' not in row or 'currency' not in own or row['currency'] == own['currency'],
            'accounting_scope_conflict')
    require('currency' not in row or 'currency' not in base or row['currency'] == base['currency'],
            'accounting_scope_conflict')
    require('currency' not in own or 'currency' not in base or own['currency'] == base['currency'],
            'accounting_scope_conflict')
    return (row.get('client_scope', payload.get('client_scope')), row.get('period'),
            *values, json.dumps(dimensions, sort_keys=True, ensure_ascii=False), currency)


def footprints(key, claims, root):
    item = claims[key]
    if item['status'] == 'derived':
        return [part for child in item['inputs'] for part in footprints(child, claims, root)]
    source = item['source_ref']
    path = (root / source['source_file']).resolve()
    if path.suffix.lower() == '.json':
        return [(str(path), 'json', source['pointer'], 0, 0)]
    match = re.fullmatch(r'([A-Z]+)(\d+)(?::([A-Z]+)(\d+))?', source['range'].upper())
    require(match is not None, 'accounting_source_range_invalid')
    return [(str(path), source.get('sheet', '') if path.suffix.lower() in ('.xlsx', '.xls') else '',
             match[1], int(match[2]), int(match[4] or match[2]))]


def _text(value, reason):
    require(isinstance(value, str) and bool(value.strip()), reason)
    return value.strip()


def _validate_perimeter(contract):
    perimeter = contract.get('perimeter')
    require(isinstance(perimeter, dict), 'accounting_perimeter_required')
    _text(perimeter.get('perimeter_id'), 'accounting_perimeter_id_required')
    require(perimeter.get('accounting_basis') in ACCOUNTING_BASES,
            'accounting_basis_invalid')
    require(perimeter.get('period_status') == 'closed',
            'accounting_period_not_closed')
    require(perimeter.get('completeness_status') == PERIMETER_COMPLETENESS,
            'accounting_completeness_statement_invalid')
    require(perimeter.get('authenticity_status') == AUTHENTICITY_BOUNDARY,
            'accounting_authenticity_overclaim')
    _text(perimeter.get('source_system'), 'accounting_source_system_required')
    _text(perimeter.get('export_record_id'), 'accounting_export_record_id_required')
    exported = _text(perimeter.get('exported_at'), 'accounting_exported_at_required')
    try:
        datetime.fromisoformat(exported.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError('accounting_exported_at_invalid') from exc
    covered = perimeter.get('covered_cost_categories')
    require(isinstance(covered, list) and len(covered) == len(set(covered)) and
            set(covered) == set(COST_METRICS), 'accounting_perimeter_cost_coverage_invalid')
    excluded = perimeter.get('excluded_items')
    require(isinstance(excluded, list) and all(isinstance(item, str) and item.strip()
            for item in excluded), 'accounting_excluded_items_invalid')
    return perimeter


def _same_core_scope(payload, left, right):
    a, b = scope(payload, left), scope(payload, right)
    return a[:4] == b[:4] and a[5] == b[5]


def _validate_allocation(payload, category, component_key, allocation, claims, evaluate, root):
    require(isinstance(allocation, dict) and allocation.get('method') == ALLOCATION_METHOD,
            'accounting_allocation_contract_required')
    _text(allocation.get('basis_name'), 'accounting_allocation_basis_required')
    keys = {name: allocation.get(name) for name in
            ('pool_claim', 'scope_base_claim', 'total_base_claim', 'schedule_total_claim')}
    require(all(isinstance(key, str) and key in claims for key in keys.values()),
            'accounting_allocation_claim_missing')
    require(len(set(keys.values())) == 4 and component_key not in keys.values(),
            'accounting_allocation_claim_reused')
    component = claims[component_key]
    require(component.get('status') == 'derived', 'accounting_allocated_cost_must_be_derived')
    require(set(component.get('inputs', [])) == {keys['pool_claim'], keys['scope_base_claim'],
            keys['total_base_claim']}, 'accounting_allocation_inputs_mismatch')
    formula = component.get('formula')
    bindings = formula.get('bindings') if isinstance(formula, dict) else None
    expected_bindings = {'shared_pool': keys['pool_claim'], 'scope_base': keys['scope_base_claim'],
                         'total_base': keys['total_base_claim']}
    require(bindings == expected_bindings, 'accounting_allocation_bindings_mismatch')
    try:
        body = ast.parse(formula['expression'], mode='eval').body
    except (SyntaxError, KeyError, TypeError) as exc:
        raise ValueError('accounting_allocation_expression_mismatch') from exc
    require(isinstance(body, ast.BinOp) and isinstance(body.op, ast.Div) and
            isinstance(body.left, ast.BinOp) and isinstance(body.left.op, ast.Mult) and
            isinstance(body.left.left, ast.Name) and body.left.left.id == 'shared_pool' and
            isinstance(body.left.right, ast.Name) and body.left.right.id == 'scope_base' and
            isinstance(body.right, ast.Name) and body.right.id == 'total_base',
            'accounting_allocation_expression_mismatch')
    pool = evaluate(keys['pool_claim'])
    base = evaluate(keys['scope_base_claim'])
    total_base = evaluate(keys['total_base_claim'])
    schedule_total = evaluate(keys['schedule_total_claim'])
    require(all(value is not None and value >= 0 for value in
            (pool, base, total_base, schedule_total)), 'accounting_allocation_value_invalid')
    require(total_base > 0 and base <= total_base, 'accounting_allocation_base_invalid')
    require(schedule_total == pool, 'accounting_allocation_schedule_not_reconciled')
    require(evaluate(component_key) == pool * base / total_base,
            'accounting_allocation_amount_mismatch')
    require(scope(payload, claims[keys['scope_base_claim']]) == scope(payload, component),
            'accounting_allocation_scope_base_mismatch')
    for name in ('pool_claim', 'total_base_claim', 'schedule_total_claim'):
        require(_same_core_scope(payload, claims[keys[name]], component),
                'accounting_allocation_core_scope_mismatch')
    # Pool, basis and total-basis evidence cannot be aliases of one source cell.
    selectors = []
    for name in ('pool_claim', 'scope_base_claim', 'total_base_claim'):
        for selector in footprints(keys[name], claims, root):
            require(not any(selector[:3] == old[:3] and
                            max(selector[3], old[3]) <= min(selector[4], old[4])
                            for old in selectors), 'accounting_allocation_source_reused')
            selectors.append(selector)
    return dict(category=category, method=ALLOCATION_METHOD,
                component_claim=component_key, **keys, amount=str(evaluate(component_key)))


def validate_accounting(payload, row, claims, evaluate, root):
    if canonical(row.get('metric')) != 'roi':
        return None
    contract = row.get('accounting')
    require(isinstance(contract, dict) and contract.get('method') == METHOD,
            'accounting_contract_required')
    require(isinstance(contract.get('scope_note'), str) and bool(contract['scope_note'].strip()),
            'accounting_scope_note_required')
    perimeter = _validate_perimeter(contract)
    costs = contract.get('costs')
    require(isinstance(costs, dict) and set(costs) == set(COST_METRICS),
            'accounting_cost_categories_incomplete')
    pairs = [('recognized_revenue', contract.get('revenue_claim')),
             ('revenue_refund', contract.get('refund_claim')), *costs.items()]
    ids = [key for _, key in pairs]
    require(all(isinstance(key, str) and key in claims for key in ids),
            'accounting_claim_missing')
    require(len(ids) == len(set(ids)), 'accounting_duplicate_component')
    treatments = contract.get('cost_treatment')
    require(isinstance(treatments, dict) and set(treatments) == set(COST_METRICS) and
            all(value in COST_TREATMENTS for value in treatments.values()),
            'accounting_cost_treatment_incomplete')
    allocations = contract.get('allocations', {})
    require(isinstance(allocations, dict) and set(allocations) ==
            {key for key, value in treatments.items() if value == 'allocated'},
            'accounting_allocations_mismatch')
    expected_scope = scope(payload, row)
    values = {}
    selectors = []
    for metric, key in pairs:
        item = claims[key]
        require(canonical(item.get('metric')) == metric, 'accounting_component_metric_mismatch')
        require(item.get('unit') == '元', 'accounting_component_unit_mismatch')
        require(scope(payload, item) == expected_scope, 'accounting_component_scope_mismatch')
        value = evaluate(key)
        require(value is not None, 'accounting_component_unknown')
        require(value >= 0, 'accounting_negative_component')
        if metric in COST_METRICS and treatments[metric] == 'explicit_zero':
            require(item.get('status') == 'verified' and value == 0,
                    'accounting_explicit_zero_not_sourced')
        # Renamed IDs, overlapping ranges and derived wrappers cannot count
        # the same cells as different revenue/refund/cost components.
        for selector in footprints(key, claims, root):
            require(not any(selector[:3] == old[:3] and
                            max(selector[3], old[3]) <= min(selector[4], old[4])
                            for old in selectors), 'accounting_source_component_reused')
            selectors.append(selector)
        values[metric] = value
    allocation_checks = []
    for category, allocation in allocations.items():
        allocation_checks.append(_validate_allocation(payload, category, costs[category],
                                                       allocation, claims, evaluate, root))
    require(values['revenue_refund'] <= values['recognized_revenue'],
            'accounting_refund_exceeds_revenue')
    totals = {canonical(claims[key]['metric']): key for key in row['inputs']}
    require(set(totals) == {'profit', 'total_cost'}, 'accounting_totals_missing')
    for key in totals.values():
        require(scope(payload, claims[key]) == expected_scope, 'accounting_total_scope_mismatch')
    total_cost = sum((values[key] for key in COST_METRICS), Decimal(0))
    profit = values['recognized_revenue'] - values['revenue_refund'] - total_cost
    require(evaluate(totals['total_cost']) == total_cost, 'accounting_cost_total_mismatch')
    require(evaluate(totals['profit']) == profit, 'accounting_profit_mismatch')
    return dict(status='declared_source_bound_operating_perimeter_reconciled', method=METHOD,
                perimeter_id=perimeter['perimeter_id'], accounting_basis=perimeter['accounting_basis'],
                completeness_status=PERIMETER_COMPLETENESS,
                authenticity_status=AUTHENTICITY_BOUNDARY,
                evidence_kind='local_reconciliation_not_completeness_or_independent_authenticity_audit',
                component_claims=ids, allocation_checks=allocation_checks,
                total_cost=str(total_cost), profit=str(profit))
