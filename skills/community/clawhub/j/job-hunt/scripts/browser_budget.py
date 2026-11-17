"""Count every catalog in a browser journey, not only its final extraction.

The DOM selector is an observed extraction contract, not proof that a site has
no other cards. Missing stage evidence fails closed; historical files stay intact.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import journal


def views(snapshot):
    steps = snapshot.get('navigation_steps') or ([snapshot['navigation']] if snapshot.get('navigation') else [])
    if not steps:
        return [snapshot]
    if not isinstance(steps, list) or any(not isinstance(s, dict) for s in steps):
        raise ValueError('NAVIGATION_BUDGET: invalid navigation steps')
    first = steps[0].get('source_snapshot')
    if not isinstance(first, dict):
        raise ValueError('NAVIGATION_BUDGET_MISSING: intermediate catalogs were not accounted for')
    result = [first]
    for step in steps:
        source, after = step.get('source_snapshot'), step.get('result')
        if not isinstance(source, dict) or not isinstance(after, dict):
            raise ValueError('NAVIGATION_BUDGET: missing before/after snapshot')
        for field in ('url', 'text', 'links', 'catalog_rows'):
            if source.get(field) != result[-1].get(field):
                raise ValueError('NAVIGATION_BUDGET: broken snapshot chain')
        result.append(after)
    for field in ('url', 'text', 'links', 'catalog_rows'):
        if snapshot.get(field) != result[-1].get(field):
            raise ValueError('NAVIGATION_BUDGET: final snapshot differs from last step')
    return result


def usage(snapshot, *, validate_rows):
    """Return (actual search rows, distinct page numbers, all catalog rows)."""
    budget = snapshot.get('navigation_budget')
    if budget is None:
        if snapshot.get('navigation_steps') or snapshot.get('navigation'):
            raise ValueError('NAVIGATION_BUDGET_MISSING: intermediate catalogs were not accounted for')
        return None
    if not isinstance(budget, dict) or budget.get('version') != 1:
        raise ValueError('NAVIGATION_BUDGET: unsupported accounting version')
    if (type(budget.get('max_rows')) is not int or not 1 <= budget['max_rows'] <= 25
            or type(budget.get('max_pages')) is not int or not 1 <= budget['max_pages'] <= 2
            or type(budget.get('used_rows')) is not int or budget['used_rows'] < 0
            or not isinstance(budget.get('used_pages'), list)
            or any(type(p) is not int or p == 0 for p in budget['used_pages'])):
        raise ValueError('NAVIGATION_BUDGET: invalid limits or previous usage')
    stages = budget.get('stages')
    actual = views(snapshot)
    if not isinstance(stages, list) or len(stages) != len(actual):
        raise ValueError('NAVIGATION_BUDGET: every observed stage needs accounting')
    total, pages, rows = 0, set(), []
    for stage, capture in zip(stages, actual):
        if capture.get('catalog_accounting_pending'):
            raise ValueError('NAVIGATION_BUDGET_PENDING: inspect the DOM contract; this diagnostic is not a completed search')
        empty_failure = (validate_rows(capture, []) in ('platform_limit', 'not_logged_in')
                         or (capture.get('http_status') or 0) >= 400)
        if (not isinstance(stage, dict) or 'row_selector' not in stage
                or type(stage.get('page')) is not int or stage['page'] < 1
                or type(stage.get('max_rows')) is not int or not 0 <= stage['max_rows'] <= 25
                or not ((stage.get('row_selector') is None and (stage['max_rows'] == 0 or empty_failure))
                        or (isinstance(stage.get('row_selector'), str) and stage['row_selector'].strip()))):
            raise ValueError('NAVIGATION_BUDGET: invalid stage extraction contract')
        cards = capture.get('catalog_rows')
        if (not isinstance(cards, list) or type(stage.get('row_count')) is not int
                or stage['row_count'] != len(cards)):
            raise ValueError('NAVIGATION_BUDGET: DOM count does not match stage rows')
        if validate_rows(capture, cards) not in ('ok', 'platform_limit', 'not_logged_in', 'transport'):
            raise ValueError('NAVIGATION_BUDGET: invalid stage capture')
        # Count repeated search catalogs again. Source and previous result are
        # the same checkpoint and are never added twice.
        if cards:
            total += len(cards)
            pages.add(stage['page'])
            rows.extend(cards)
        if len(cards) > stage['max_rows'] and not snapshot.get('budget_exceeded'):
            raise ValueError('NAVIGATION_BUDGET: unexpected overflow was concealed')
    if budget.get('observed_rows') != total or budget.get('observed_pages') != sorted(pages):
        raise ValueError('NAVIGATION_BUDGET: aggregate does not match observed stages')
    if (budget['used_rows'] + total > budget['max_rows']
            or len(set(budget['used_pages']) | pages) > budget['max_pages']):
        if not snapshot.get('budget_exceeded'):
            raise ValueError('NAVIGATION_BUDGET_EXCEEDED: round allowance was exceeded')
    return total, sorted(pages), rows


def used(calls, site):
    """Use signed imported counts; non-success overflow still consumed budget."""
    # Share adapter page/offset normalization with the final gate.
    from check_shortlist import _pages_per_site
    rows = 0
    for call in calls:
        if call.get('site') != site:
            continue
        if 'search_row_count' in call:
            rows += call['search_row_count']
        elif call.get('command') == 'search' and call.get('exit_code') == 0:
            rows += int(call.get('row_count') or 0)
    return rows, sorted(_pages_per_site(calls).get(site, set()))


def prepare(workspace, site, plan, calls, validate_record):
    workspace = Path(workspace).resolve()
    if not re.fullmatch(r'[a-z0-9_]+', site):
        raise ValueError('NAVIGATION_BUDGET: invalid source name')
    if journal.corrupt_lines(workspace):
        raise ValueError('NAVIGATION_BUDGET: journal contains an unparsable line')
    if not isinstance(plan, dict) or not isinstance(plan.get('stages'), list):
        raise ValueError('NAVIGATION_BUDGET: plan requires a stages array')
    brief = journal.load_yaml(workspace / 'brief.yaml', dict)
    limits = brief.get('max_rows_per_round'), brief.get('max_pages_per_site')
    if any(type(n) is not int or not 1 <= n <= ceiling for n, ceiling in zip(limits, (25, 2))):
        raise ValueError('NAVIGATION_BUDGET: brief must set limits within 25 rows / 2 pages')
    for call in calls:
        if call.get('site') == site and call.get('action') == 'browser_call':
            findings = validate_record(call, workspace)
            if findings:
                raise ValueError('; '.join(findings))
    # A capture is not permission for another read until it has been imported.
    imported = {str((workspace / c['snapshot_file']).resolve()) for c in calls if c.get('snapshot_file')}
    for path in (workspace / 'raw').glob(site + '-*.json'):
        try:
            value = json.loads(path.read_text())
        except (ValueError, OSError):
            continue
        if isinstance(value, dict) and value.get('navigation_budget') and str(path.resolve()) not in imported:
            raise ValueError('NAVIGATION_BUDGET: import the pending capture before another read')
    count, pages = used(calls, site)
    return dict(version=1, workspace=str(workspace), site=site, max_rows=limits[0], max_pages=limits[1],
                used_rows=count, used_pages=pages, stages=plan['stages'])
