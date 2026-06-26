#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ALLOWED_SIGNAL_TYPES = {
    'manual_urls', 'x_bookmarks', 'browser_reading_list', 'read_later',
    'rss', 'newsletter', 'web_search', 'local_manifest'
}
ALLOWED_PRESETS = {
    'classic-newspaper', 'modern-review', 'weekend-magazine',
    'research-brief', 'compact-wire'
}
ALLOWED_DENSITIES = {'airy', 'standard', 'compact'}


def fail(msg):
    print(f'FAIL {msg}')
    return False


def warn(msg):
    print(f'WARN {msg}')


def value_at(cfg, dotted):
    cur = cfg
    for part in dotted.split('.'):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def is_filled(value):
    if value is None:
        return False
    if isinstance(value, str) and not value.strip():
        return False
    if isinstance(value, (list, dict)) and not value:
        return False
    return True


def main(path):
    cfg_path = Path(path)
    cfg = json.loads(cfg_path.read_text())
    ok = True

    for key in ['newspaper', 'cadence', 'editorial', 'signals', 'issue', 'design', 'delivery']:
        if key not in cfg:
            ok = fail(f'missing top-level section: {key}') and ok

    onboarding = cfg.get('onboarding', {})
    onboarding_complete = bool(onboarding.get('complete'))

    signals = cfg.get('signals', [])
    if not isinstance(signals, list) or not signals:
        ok = fail('signals must contain at least one signal source') and ok
    else:
        for i, signal in enumerate(signals, 1):
            typ = signal.get('type')
            if typ not in ALLOWED_SIGNAL_TYPES:
                ok = fail(f'signals[{i}].type is unknown: {typ}') and ok
            priority = signal.get('priority')
            if priority is not None and not isinstance(priority, (int, float)):
                ok = fail(f'signals[{i}].priority must be numeric') and ok

    design = cfg.get('design', {})
    preset = design.get('preset')
    if preset and preset not in ALLOWED_PRESETS:
        ok = fail(f'design.preset is unknown: {preset}') and ok
    density = design.get('density')
    if density and density not in ALLOWED_DENSITIES:
        ok = fail(f'design.density is unknown: {density}') and ok

    issue = cfg.get('issue', {})
    max_pages = issue.get('maxPages')
    if max_pages is not None and (not isinstance(max_pages, int) or max_pages < 1):
        ok = fail('issue.maxPages must be a positive integer') and ok

    required = onboarding.get('requiredBeforePersonalIssue') or [
        'newspaper.title', 'newspaper.language', 'editorial.readerPromise',
        'editorial.topics', 'editorial.exclusions', 'signals', 'cadence',
        'delivery', 'design'
    ]
    missing = []
    for field in required:
        if field == 'signals':
            enabled = [s for s in signals if s.get('enabled')]
            if not enabled:
                missing.append('signals.enabled')
        elif field in {'cadence', 'delivery', 'design'}:
            if not isinstance(cfg.get(field), dict) or not cfg.get(field):
                missing.append(field)
        elif not is_filled(value_at(cfg, field)):
            missing.append(field)

    if onboarding_complete:
        if missing:
            ok = fail('onboarding.complete=true but missing: ' + ', '.join(missing)) and ok
        cadence = cfg.get('cadence', {})
        if cadence.get('createCron') and (not cadence.get('mode') or not cadence.get('time')):
            ok = fail('cadence.createCron=true requires cadence.mode and cadence.time') and ok
    else:
        warn('onboarding is incomplete; do not generate a personalized issue, create cron, or set up external delivery yet')
        if missing:
            warn('missing personalization fields: ' + ', '.join(missing))

    if ok:
        newspaper = cfg.get('newspaper', {})
        title = newspaper.get('title') or '(not set)'
        print(f'ok config: {cfg_path}')
        print(f"title={title} preset={preset or 'default'} onboardingComplete={onboarding_complete}")
        return 0
    return 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: check_config.py <config.json>', file=sys.stderr)
        sys.exit(2)
    try:
        sys.exit(main(sys.argv[1]))
    except json.JSONDecodeError as e:
        print(f'FAIL invalid JSON: {e}')
        sys.exit(1)
