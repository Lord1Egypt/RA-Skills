"""Pure, read-only analysis. No filesystem, network, process, or credential access."""
import re
import math

def safe_id(value):
    return value if isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_.:/-]{1,160}', value) else '[redacted identifier]'

VERSION = '4.1.1'

def finding(code, severity, message):
    return {'code': code, 'severity': severity, 'message': message}

def catalog_rows(catalog):
    rows = catalog.get('models', [])
    if not isinstance(rows, list):
        raise ValueError('catalog.models must be an array')
    return {r['key']: r for r in rows if isinstance(r, dict) and isinstance(r.get('key'), str)}

def route(catalog, status, policy, tier, image=False, tools=False, context=0):
    """Operator-ordered tiers; availability is not proof of successful inference."""
    rows = catalog_rows(catalog)
    allowed = status.get('allowed')
    missing = status.get('auth', {}).get('missingProvidersInUse', [])
    candidates = policy.get('tiers', {}).get(tier, [])
    if not isinstance(candidates, list) or any(not isinstance(x, str) for x in candidates):
        raise ValueError('policy tier must contain model identifiers')
    rejected = []
    for key in candidates:
        row = rows.get(key)
        reasons = []
        if safe_id(key) != key:
            rejected.append({'model': '[redacted identifier]', 'reasons': ['invalid identifier']})
            continue
        issues = status.get('auth', {}).get('modelRouteIssues', [])
        if issues:
            reasons.append('native status reports unresolved route issues; resolve before recommendation')
        if row is None:
            reasons.append('absent from catalog')
        else:
            if row.get('available') is not True:
                reasons.append('availability missing or not true')
            if allowed is None or key not in allowed:
                reasons.append('not explicitly allowed by supplied status')
            if key.split('/')[0] in missing:
                reasons.append('provider authentication missing')
            if image and 'image' not in str(row.get('input', '')):
                reasons.append('image capability not established')
            if tools and row.get('supportsTools') is not True:
                reasons.append('tool capability not established')
            limit = row.get('contextTokens') or row.get('contextWindow')
            if context and (not isinstance(limit, (int, float)) or limit < context):
                reasons.append('context capacity insufficient or unknown')
        if reasons:
            rejected.append({'model': key, 'reasons': reasons})
        else:
            return {'version': VERSION, 'tier': tier, 'candidate': key,
                    'activation': 'not_performed', 'canaryRequired': True,
                    'reason': 'First eligible model in operator preference order; price and latency not inferred.',
                    'rejected': rejected}
    return {'version': VERSION, 'tier': tier, 'candidate': None, 'activation': 'not_performed',
            'canaryRequired': True, 'rejected': rejected,
            'reason': 'No proven eligible candidate. Supply policy and current catalog/status; do not guess.'}

def audit(catalog, status, config, jobs, sessions=None):
    rows = catalog_rows(catalog)
    out = []
    agents = config.get('agents', {})
    defaults = agents.get('defaults', {})
    entries = agents.get('entries', {})
    if not isinstance(entries, dict):
        raise ValueError('agents.entries must be an object')
    def check_model(model, label):
        if isinstance(model, str):
            primary, fallbacks = model, []
        elif isinstance(model, dict):
            primary, fallbacks = model.get('primary'), model.get('fallbacks', [])
        else:
            return
        for key in ([primary] if primary else []) + fallbacks:
            if key not in rows:
                out.append(finding('model_absent', 'warning', f'{label}: model is absent from supplied catalog: {safe_id(key)}'))
            elif rows[key].get('available') is not True:
                out.append(finding('model_unverified', 'warning', f'{label}: availability is unverified: {safe_id(key)}'))
        if primary and fallbacks and all(x.split('/')[0] == primary.split('/')[0] for x in fallbacks):
            out.append(finding('shared_provider_fallback', 'info', f'{label}: all fallbacks share the primary provider; provider-wide outages may affect all routes.'))
    heartbeat = defaults.get('heartbeat', {})
    if heartbeat.get('every'):
        out.append(finding('heartbeat_review', 'info', 'A default heartbeat interval is configured; verify task necessity, quiet hours and delivery rather than assuming cache savings.'))
    for field in ('bootstrapMaxChars', 'bootstrapTotalMaxChars'):
        limit = defaults.get(field)
        if isinstance(limit, (int, float)) and limit > 40000:
            out.append(finding('bootstrap_large_limit', 'info', f'{field} allows more than 40,000 characters; inspect native /context detail before reducing it. This is a review heuristic, not measured waste.'))
    check_model(defaults.get('model'), 'defaults')
    for agent, entry in entries.items():
        check_model(entry.get('model', defaults.get('model')), f'agent {safe_id(agent)}')
    for key in status.get('allowed', []):
        if key not in rows:
            out.append(finding('allowlist_absent', 'warning', f'Allowed model absent from catalog: {safe_id(key)}'))
    for provider in status.get('auth', {}).get('missingProvidersInUse', []):
        out.append(finding('auth_missing', 'warning', f'Authentication unavailable for provider: {safe_id(provider)}'))
    if status.get('auth', {}).get('modelRouteIssues'):
        out.append(finding('route_issues', 'warning', 'Native model status reports route issues; inspect locally with openclaw models status.'))
    if sessions is None:
        out.append(finding('sessions_unknown', 'info', 'Session overrides were not supplied; default-vs-session comparisons unavailable.'))
    else:
        for s in sessions:
            agent = s.get('agentId')
            model = entries.get(agent, {}).get('model', defaults.get('model', {}))
            primary = model if isinstance(model, str) else model.get('primary')
            if s.get('model') and primary and s['model'] != primary:
                out.append(finding('session_override', 'info', f'Agent {safe_id(agent)}: session model differs from configured primary.'))
    for index, job in enumerate(jobs):
        if not job.get('enabled', True):
            continue
        payload = job.get('payload', {})
        label = f'Automation #{index + 1}'  # Never output job names, commands, or prompts.
        # Native heartbeat/system events use their own execution configuration.
        # Do not apply agentTurn-only model/timeout/lightContext rules to them.
        if payload.get('kind') in ('command', 'heartbeat', 'systemEvent'):
            continue
        if payload.get('kind') not in ('agentTurn', 'agent'):
            out.append(finding('automation_kind_unknown', 'info', f'{label}: payload kind not recognized; inspect manually.'))
            continue
        if not payload.get('model'):
            out.append(finding('automation_model_inherited', 'info', f'{label}: inherits its model; verify effective cost.'))
        else:
            check_model(payload['model'], label)
        if not payload.get('timeoutSeconds'):
            out.append(finding('automation_timeout', 'info', f'{label}: no explicit timeout.'))
        if not payload.get('lightContext'):
            out.append(finding('automation_context', 'info', f'{label}: consider lightContext only if required instructions remain available.'))
        every = job.get('schedule', {}).get('everyMs')
        if isinstance(every, (int, float)) and 0 < every < 3600000:
            out.append(finding('frequent_agent_job', 'warning', f'{label}: runs more than hourly; consider a command job if the task is deterministic.'))
        if not job.get('delivery'):
            out.append(finding('automation_delivery', 'info', f'{label}: delivery intent not explicit.'))
    out.append(finding('cache_economics', 'info', 'Do not schedule cache-only heartbeats without provider-specific TTL and measured net savings.'))
    return {'version': VERSION, 'mode': 'read-only', 'catalogCount': len(rows),
            'findings': sorted(out, key=lambda x: {'warning': 0, 'info': 1}[x['severity']]),
            'savingsEstimate': None, 'limitations': ['No inference canary or authentication probe performed.',
            'Catalog availability is not exact-route inference proof.', 'No pricing or savings assumed.']}

def context_report(files):
    results = []
    seen = {}
    for name, content in files.items():
        normalized = content.strip()
        item = {'file': name, 'characters': len(content), 'estimatedTokens': (len(content) + 3) // 4}
        if normalized and normalized in seen:
            item['duplicateOf'] = seen[normalized]
        seen[normalized] = name
        results.append(item)
    return {'version': VERSION, 'files': sorted(results, key=lambda x: -x['characters']),
            'note': 'Character/4 heuristic, not measured prompt tokens. Native /context detail is authoritative; no truncation or edits performed.'}

def budget(usage=None, limit=None):
    if usage is None:
        return {'version': VERSION, 'status': 'unknown', 'costUSD': None, 'tokens': None,
                'reason': 'No usage supplied. Missing data is not zero usage.'}
    cost = usage.get('costUSD')
    if cost is not None and (isinstance(cost, bool) or not isinstance(cost, (int, float)) or not math.isfinite(cost) or cost < 0):
        raise ValueError('costUSD must be a non-negative number or null')
    complete = usage.get('complete') is True
    return {'version': VERSION, 'status': 'exceeded' if cost is not None and limit is not None and cost >= limit else ('ok' if complete and cost is not None else 'incomplete'),
            'costUSD': cost, 'complete': complete, 'limitUSD': limit,
            'note': 'Supplied aggregate only; native usage ingestion and automated budget alerts are planned for v4.1.'}
