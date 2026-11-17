"""Record native AnySearch HTTP searches as leads, never as posting detail."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import uuid

import journal

ACTION = 'search_call'


def classify(stdout, stderr, exit_code):
    classification, rows = 'transport', []
    if re.search(r'\b(?:403|429)\b|too many requests|access denied', stderr, re.I):
        classification = 'platform_limit'
    elif exit_code == 0:
        try:
            value = json.loads(stdout)
            rows = value['data']['results']
            if (value.get('code') != 0 or not isinstance(rows, list)
                    or any(not isinstance(r, dict) or not isinstance(r.get('title'), str)
                           or not isinstance(r.get('url'), str)
                           or not r['url'].startswith(('https://', 'http://')) for r in rows)):
                raise ValueError('invalid search envelope')
            classification = 'ok'
        except (ValueError, KeyError, TypeError):
            rows = []
    return dict(classification=classification, row_count=len(rows),
                empty_result=classification == 'ok' and not rows)


def validate_record(record, workspace):
    try:
        root = Path(workspace).resolve()
        if (record.get('action') != ACTION or record.get('backend') != 'anysearch-http'
                or record.get('site') != 'anysearch' or record.get('command') != 'search'
                or not isinstance(record.get('query'), str) or not record['query'].strip()
                or type(record.get('exit_code')) is not int
                or not journal.receipt_intact({k: v for k, v in record.items() if k != '_lineno'})):
            raise ValueError('expected an intact native HTTP search receipt')
        texts = []
        for key in ('stdout_file', 'stderr_file'):
            name = record[key]
            path = (root / name).resolve()
            if (path.parent != root / 'raw' or not path.name.startswith('anysearch-')
                    or journal.sha256_file(path) != record['input_hashes'][name]):
                raise ValueError('search capture path or hash changed')
            texts.append(path.read_text(encoding='utf-8'))
        expected = classify(*texts, record['exit_code'])
        if any(record.get(k) != v for k, v in expected.items()):
            raise ValueError('search metadata differs from captured response')
        if (type(record.get('requested_rows')) is not int or not 1 <= record['requested_rows'] <= 10
                or record['row_count'] > record['requested_rows']):
            raise ValueError('search response exceeded its requested row budget')
        tokens = shlex.split(record['command_line'])
        if tokens[:2] != ['anysearch', 'search'] or tokens[2] != record['query']:
            raise ValueError('search query differs from command')
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        return [f'INVALID_SEARCH_CAPTURE: {exc}']
    return []


def preflight(workspace, site, url=''):
    """Check the owning round before a network read, not only at delivery."""
    from check_search_coverage import FILE, _plan, _registrations
    from record_browser_capture import read_retrieval_calls, check_stop_order, validate_record as browser_record
    root = Path(workspace).resolve()
    if journal.corrupt_lines(root):
        raise ValueError('search journal is corrupt')
    try:
        plan = _plan(journal.load_yaml(root / FILE, dict).get('plan'))
    except journal.YamlUnreadable as exc:
        raise ValueError(f'missing or unreadable search plan: {exc}') from exc
    _registrations(root, plan)
    if site not in {s['site'] for s in plan['sources']}:
        raise ValueError(f'UNPLANNED_SOURCE: register {site} in this round before reading')
    calls = read_retrieval_calls(root)
    if check_stop_order(calls + [dict(action=ACTION, site=site, url=url)]):
        raise ValueError('READ_AFTER_STOP: resolve the source refusal before resuming')
    for call in calls:
        problems = (validate_record(call, root) if call['action'] == ACTION else
                    browser_record(call, root) if call['action'] == 'browser_call' else [])
        if problems:
            raise ValueError('; '.join(problems))
    imported = {str((root / c['snapshot_file']).resolve()) for c in calls if c.get('snapshot_file')}
    for path in (root / 'raw').glob('*.json'):
        if str(path.resolve()) in imported:
            continue
        try:
            value = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        if isinstance(value, dict) and {'url', 'text', 'links', 'retrieved_at'} <= value.keys():
            raise ValueError(f'PENDING_CAPTURE: import {path.name} before another read')
    return calls


def run(workspace, command, arguments, env):
    root = Path(workspace).resolve()
    if not arguments or arguments[0] != 'search':
        raise ValueError('Recorded AnySearch reads require one search query per invocation')
    # The query is one argument; flags remain CLI-owned. Never journal a key.
    if len(arguments) < 2 or not arguments[1].strip() or arguments[1].startswith('-') or any(a.startswith('--api_key') for a in arguments):
        raise ValueError('Pass one quoted query; use ANYSEARCH_API_KEY through the environment')
    if '--format' in arguments:
        raise ValueError('The recorded search wrapper owns --format json')
    if len(arguments) > 2 and not arguments[2].startswith('-'):
        raise ValueError('Pass the full query as one quoted argument')
    options = arguments[2:]
    allowed = {'--tag', '-t', '--domain', '-d', '--sub_domain', '-s', '--params',
               '--sub_domain_params', '--sdp', '-p', '--zone', '--language', '--max_results', '-m'}
    if len(options) % 2 or any(flag not in allowed for flag in options[::2]):
        raise ValueError('Use supported AnySearch search options, each followed by its value')
    limits = [int(value) for flag, value in zip(options[::2], options[1::2]) if flag in {'--max_results', '-m'}]
    if len(limits) > 1:
        raise ValueError('Supply --max_results or -m only once')
    calls = preflight(root, 'anysearch')
    try:
        brief = journal.load_yaml(root / 'brief.yaml', dict)
    except journal.YamlUnreadable as exc:
        raise ValueError(str(exc)) from exc
    limit = brief.get('max_rows_per_round')
    if type(limit) is not int or not 1 <= limit <= 25:
        raise ValueError('brief.max_rows_per_round must be an integer from 1 to 25')
    remaining = limit - sum(c.get('row_count', 0) for c in calls if c.get('site') == 'anysearch')
    requested = limits[0] if limits else 10
    if not 1 <= requested <= min(10, remaining):
        raise ValueError(f'SEARCH_BUDGET: request at most {min(10, max(0, remaining))} remaining rows')
    (root / 'raw').mkdir(exist_ok=True)
    prefix = 'anysearch-' + uuid.uuid4().hex
    out, err = root / 'raw' / (prefix + '.json'), root / 'raw' / (prefix + '.stderr.txt')
    result = subprocess.run(command + arguments + ['--format', 'json'], env=env, capture_output=True)
    out.write_bytes(result.stdout)
    err.write_bytes(result.stderr)
    stdout, stderr = (p.read_text(encoding='utf-8', errors='replace') for p in (out, err))
    record = dict(action=ACTION, backend='anysearch-http', site='anysearch', command='search',
                  query=arguments[1], command_line=shlex.join(['anysearch', *arguments]),
                  requested_rows=requested,
                  exit_code=result.returncode, ts=dt.datetime.now(dt.timezone.utc).isoformat(),
                  stdout_file=out.relative_to(root).as_posix(), stderr_file=err.relative_to(root).as_posix(),
                  input_hashes={p.relative_to(root).as_posix(): journal.sha256_file(p) for p in (out, err)},
                  **classify(stdout, stderr, result.returncode))
    journal.append(root, journal.sign_receipt(record))
    print(stdout, end='')
    print(stderr, end='', file=sys.stderr)
    return 0 if record['classification'] == 'ok' and record['row_count'] <= requested else 1
