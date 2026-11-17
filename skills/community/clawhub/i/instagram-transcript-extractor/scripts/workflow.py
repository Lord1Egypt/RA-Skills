#!/usr/bin/env python3
"""Offline request planning and conservative reconciliation; no network or storage."""
import json
import math
import re
import sys
from collections import Counter
from urllib.parse import parse_qsl, urlsplit

PATH = re.compile(r'^/(p|reel|reels|tv)/([A-Za-z0-9_-]+)/?$')
TRACKING = {'igsh', 'igshid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'}
TERMINAL = {'SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT'}

class ContractError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def identity(url):
    if not isinstance(url, str):
        return None
    try:
        u = urlsplit(url.strip())
        if u.scheme.lower() not in ('http', 'https') or u.hostname not in ('instagram.com', 'www.instagram.com', 'm.instagram.com') or u.username or u.password or u.port not in (None, 80, 443):
            return None
        match = PATH.fullmatch(u.path)
        # Unknown query keys may have semantic meaning; do not discard them.
        if not match or any(k.lower() not in TRACKING for k, _ in parse_qsl(u.query, keep_blank_values=True)):
            return None
        return (match.group(1), match.group(2))
    except ValueError:
        return None


def prepare(lines):
    if not isinstance(lines, list):
        raise ContractError('invalid_urls', 'urls must be a list of strings')
    for n, value in enumerate(lines, 1):
        if not isinstance(value, str):
            raise ContractError('invalid_urls', f'URL at line {n} must be a string')
    requests, seen, invalid = [], {}, []
    for n, value in enumerate(lines, 1):
        url = value.strip()
        key = identity(url)
        if not key:
            invalid.append({'line': n, 'value': value, 'reason': 'Open the video page and copy its recognizable Instagram post or Reel link.'})
        elif key in seen:
            req = requests[seen[key]]
            req['lines'].append(n)
            req['originals'].append({'line': n, 'url': value})
        else:
            seen[key] = len(requests)
            requests.append({'url': url, 'lines': [n], 'originals': [{'line': n, 'url': value}]})
    return {'input_lines': len(lines), 'invalid': invalid, 'requests': requests, 'batches': ([{'batch_id': 'batch-1', 'request_indices': list(range(len(requests))), 'phase': 'new'}] if requests else [])}


def actor_input(requests):
    urls = [r['url'] for r in requests]
    if not urls:
        raise ContractError('invalid_plan', 'No valid URLs')
    return {'enhancedcrawl': True, **({'videoUrl': urls[0]} if len(urls) == 1 else {'bulkUrls': urls})}


def completeness(evidence, item_count):
    """Verify consistency of agent-supplied observations, not their authenticity."""
    if not isinstance(evidence, list) or not evidence:
        return False
    observed = 0
    for batch in evidence:
        if not isinstance(batch, dict) or not isinstance(batch.get('run_status'), str) or batch['run_status'] not in TERMINAL:
            return False
        pages = batch.get('pages')
        if not isinstance(pages, list) or not pages:
            return False
        offset = 0
        totals = []
        for index, page in enumerate(pages):
            if not isinstance(page, dict):
                return False
            count, limit, start = page.get('count'), page.get('limit'), page.get('offset')
            if any(type(x) is not int for x in (count, limit, start)) or start != offset or limit <= 0 or count < 0 or count > limit or page.get('truncated') is not False:
                return False
            if index < len(pages) - 1 and count != limit:
                return False
            offset += count
            if 'total' in page:
                total = page['total']
                if type(total) is not int or total < 0:
                    return False
                totals.append(total)
        if totals:
            if len(totals) != len(pages) or len(set(totals)) != 1 or offset != totals[0]:
                return False
        elif not (batch.get('end_of_data') is True and isinstance(batch.get('end_evidence'), str) and batch['end_evidence'].strip()):
            return False
        observed += offset
    return observed == item_count


def segments_status(item):
    if 'segments' not in item or item['segments'] is None:
        return 'unavailable', []
    segments = item['segments']
    if not isinstance(segments, list) or not segments:
        return ('unavailable' if segments == [] else 'invalid'), []
    previous = -1
    for s in segments:
        if not isinstance(s, dict) or not isinstance(s.get('text'), str):
            return 'invalid', []
        a, b = s.get('start'), s.get('end')
        if any(type(v) not in (int, float) or not math.isfinite(v) for v in (a, b)) or a < 0 or b < a or a < previous:
            return 'invalid', []
        previous = a
    return 'available', segments


def reconcile(plan, items, evidence):
    if not isinstance(items, list):
        raise ContractError('invalid_items', 'items must be the extracted dataset items array, not an envelope or JSON string')
    if not isinstance(plan, dict) or not isinstance(plan.get('requests'), list) or not isinstance(plan.get('invalid'), list) or type(plan.get('input_lines')) is not int:
        raise ContractError('invalid_plan', 'plan must be the object returned by prepare')
    requests = plan['requests']
    if any(not isinstance(r, dict) or not identity(r.get('url')) or not isinstance(r.get('lines'), list) for r in requests):
        raise ContractError('invalid_plan', 'plan contains invalid requests')
    ids = [identity(r['url']) for r in requests]
    if len(set(ids)) != len(ids):
        raise ContractError('invalid_plan', 'plan contains duplicate request identities')
    batches = plan.get('batches')
    if not isinstance(batches, list) or not isinstance(evidence, list):
        raise ContractError('invalid_plan', 'plan.batches and evidence must be arrays')
    assigned, batch_ids = [], []
    for batch in batches:
        if (not isinstance(batch, dict) or not isinstance(batch.get('batch_id'), str) or not batch['batch_id']
                or not isinstance(batch.get('request_indices'), list) or not batch['request_indices']
                or any(type(i) is not int or i < 0 or i >= len(requests) for i in batch['request_indices'])):
            raise ContractError('invalid_plan', 'Each batch requires a batch_id and valid request_indices')
        assigned.extend(batch['request_indices'])
        batch_ids.append(batch['batch_id'])
    if len(set(batch_ids)) != len(batch_ids) or sorted(assigned) != list(range(len(requests))):
        raise ContractError('invalid_plan', 'Batches must cover each request exactly once')
    # Evidence and items are bound to one explicitly identified batch. Duplicate IDs
    # or item indices invalidate the affected observations, not unrelated batches.
    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())
    run_counts = Counter(b.get('run_id') for b in batches if nonempty(b.get('run_id')))
    dataset_counts = Counter(b.get('dataset_id') for b in batches if nonempty(b.get('dataset_id')))
    evidence_batch_counts = Counter(e.get('batch_id') for e in evidence if isinstance(e, dict) and nonempty(e.get('batch_id')))
    evidence_run_counts = Counter(e.get('run_id') for e in evidence if isinstance(e, dict) and nonempty(e.get('run_id')))
    evidence_dataset_counts = Counter(e.get('dataset_id') for e in evidence if isinstance(e, dict) and nonempty(e.get('dataset_id')))
    index_counts = Counter(i for e in evidence if isinstance(e, dict) and isinstance(e.get('item_indices'), list) for i in e['item_indices'] if type(i) is int)
    matches = [[] for _ in requests]
    unassigned = []
    used_indices = set()
    uncertain = set()
    batch_results = []
    request_complete = [False] * len(requests)
    request_run_status = [None] * len(requests)
    for batch in batches:
        bid = batch['batch_id']
        candidates = [e for e in evidence if isinstance(e, dict) and e.get('batch_id') == bid]
        ev = candidates[0] if len(candidates) == 1 else None
        run, dataset = batch.get('run_id'), batch.get('dataset_id')
        indices = ev.get('item_indices') if ev else None
        bound = (batch.get('phase') == 'submitted' and nonempty(run) and nonempty(dataset)
                 and run_counts[run] == 1 and dataset_counts[dataset] == 1 and ev is not None
                 and evidence_batch_counts[bid] == 1 and ev.get('run_id') == run and ev.get('dataset_id') == dataset
                 and evidence_run_counts[run] == 1 and evidence_dataset_counts[dataset] == 1
                 and ev.get('run_status') == batch.get('run_status') and isinstance(indices, list)
                 and all(type(i) is int and 0 <= i < len(items) and index_counts[i] == 1 for i in indices))
        batch_complete = bool(bound and completeness([ev], len(indices)))
        batch_results.append({'batch_id': bid, 'phase': batch.get('phase'), 'run_status': batch.get('run_status'), 'complete': batch_complete,
                              'status': 'complete' if batch_complete else 'submission_unknown' if batch.get('phase') == 'submission_unknown' else 'pending'})
        for i in batch['request_indices']:
            request_complete[i] = batch_complete
            request_run_status[i] = batch.get('run_status') if bound else None
        if not bound:
            continue
        for item_index in indices:
            used_indices.add(item_index)
            item = items[item_index]
            if not isinstance(item, dict):
                unassigned.append(item)
                continue
            uid = identity(item.get('url'))
            code = item.get('code')
            code = code if isinstance(code, str) and re.fullmatch(r'[A-Za-z0-9_-]+', code) else None
            conflict = bool((item.get('url') and uid is None) or (uid and code and uid[1] != code))
            members = batch['request_indices']
            if conflict:
                candidates = {i for i in members if ids[i] == uid or (code and ids[i][1] == code)}
            else:
                exact = [i for i in members if uid and ids[i] == uid]
                candidates = set(exact if exact else [i for i in members if (code or (uid and uid[1])) and ids[i][1] == (code or uid[1])])
            if len(candidates) == 1 and not conflict:
                matches[next(iter(candidates))].append(item)
            else:
                uncertain.update(candidates)
                unassigned.append(item)
    unassigned.extend(item for i, item in enumerate(items) if i not in used_indices)
    complete = all(b['complete'] for b in batch_results) and bool(batch_results)
    results = []
    for i, req in enumerate(requests):
        rows = matches[i]
        if len(rows) > 1:
            results.append({**req, 'status': 'review', 'run_status': request_run_status[i], 'identity_review': True, 'provisional': not request_complete[i], 'items': rows})
            continue
        if not rows:
            status = ('review' if i in uncertain else 'pending' if not request_complete[i]
                      else 'not_returned' if request_run_status[i] == 'SUCCEEDED' else 'run_failed')
            results.append({**req, 'status': status, 'run_status': request_run_status[i], 'identity_review': i in uncertain, 'provisional': not request_complete[i]})
            continue
        item = rows[0]
        text, error = item.get('text'), item.get('errMsg')
        if (text is not None and not isinstance(text, str)) or (error is not None and not isinstance(error, str)):
            status = 'review'
        else:
            has_text = bool(text and text.strip())
            has_error = bool(error and error.strip())
            status = 'review' if has_text and has_error else 'success' if has_text else 'failed' if has_error else 'empty'
        if i in uncertain:
            status = 'review'
        ts_status, safe_segments = segments_status(item)
        results.append({**req, 'status': status, 'run_status': request_run_status[i], 'identity_review': i in uncertain, 'provisional': not request_complete[i], 'item': item, 'timestamps': ts_status, 'safe_segments': safe_segments})
    return {'input_lines': plan['input_lines'], 'invalid_count': len(plan['invalid']), 'unique_requests': len(requests), 'counts': dict(Counter(r['status'] for r in results)), 'results': results, 'unassigned': unassigned, 'batches': batch_results, 'complete': complete}


def next_action(state):
    if not isinstance(state, dict):
        raise ContractError('invalid_state', 'state must be an object')
    phase = state.get('phase')
    if not isinstance(phase, str):
        raise ContractError('invalid_state', 'Unsupported state phase')
    actions = {'new': 'start', 'submission_unknown': 'find_existing_run', 'unknown_unresolved': 'report_unknown', 'complete': 'report'}
    if phase == 'running':
        return 'get_same_run' if state.get('run_id') else 'find_existing_run'
    if phase in ('terminal', 'read_incomplete'):
        return ('read_dataset' if phase == 'terminal' else 'retry_read') if state.get('dataset_id') else 'inspect_run'
    if phase not in actions:
        raise ContractError('invalid_state', 'Unsupported state phase')
    return actions[phase]


def main():
    try:
        try:
            obj = json.load(sys.stdin, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
        except (ValueError, UnicodeDecodeError):
            raise ContractError('invalid_json', 'Expected one JSON object on standard input')
        if not isinstance(obj, dict):
            raise ContractError('invalid_request', 'Request must be a JSON object')
        op = obj.get('operation')
        if op == 'prepare':
            if 'urls' not in obj:
                raise ContractError('missing_field', 'Missing required field: urls')
            plan = prepare(obj['urls'])
            result = {'plan': plan, 'input': actor_input(plan['requests']) if plan['requests'] else None}
        elif op == 'reconcile':
            if 'plan' not in obj or 'items' not in obj or 'evidence' not in obj:
                raise ContractError('missing_field', 'reconcile requires plan, items and evidence')
            result = reconcile(obj['plan'], obj['items'], obj['evidence'])
        elif op == 'next_action':
            if 'state' not in obj:
                raise ContractError('missing_field', 'Missing required field: state')
            result = {'action': next_action(obj['state'])}
        else:
            raise ContractError('unsupported_operation', 'operation must be prepare, reconcile or next_action')
        json.dump(result, sys.stdout, ensure_ascii=False, allow_nan=False)
        print()
    except ContractError as exc:
        json.dump({'error': {'type': exc.code, 'message': str(exc)}}, sys.stderr)
        print(file=sys.stderr)
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())
