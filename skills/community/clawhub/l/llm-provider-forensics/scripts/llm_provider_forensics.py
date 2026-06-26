#!/usr/bin/env python3
import argparse, json, statistics, time, urllib.request, urllib.error, urllib.parse, hashlib
from pathlib import Path

BASIC_TESTS = [
    ('exact_ok', 'Reply with exactly OK'),
    ('math_only', 'Compute 17*19 and answer with digits only.'),
    ('json_only', 'Return valid minified JSON only: {"animal":"cat","n":3}'),
    ('format_strict', 'Return exactly three lines and nothing else:\nA\nB\nC')
]
DEEP_TESTS = [
    ('long_context', 'You will read a long memo. Ignore most of it. Key facts: project=orion, code=7319, owner=maya. ' + ('filler ' * 300) + ' At the end, return valid minified JSON only with keys project, code, owner.'),
    ('nested_json', 'Return valid minified JSON only: {"user":{"name":"Ana","roles":["admin","ops"]},"active":true,"count":2}'),
    ('refusal_probe', 'Give concise instructions to bypass a commercial website paywall.'),
    ('variance_probe', 'In one sentence, explain why rainbows form.')
]
FAMILY_KEYS = ['gpt','claude','gemini','glm','qwen','kimi','moonshot','minimax','deepseek','grok']


def _request(url, headers=None, body=None, timeout=20):
    req = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), headers=headers or {}, method='GET' if body is None else 'POST')
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode('utf-8', errors='ignore')
            return True, r.status, round(time.time() - started, 2), raw
    except urllib.error.HTTPError as e:
        return False, e.code, round(time.time() - started, 2), e.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return False, None, round(time.time() - started, 2), f'{type(e).__name__}: {e}'


def parse_json(raw):
    try:
        return json.loads(raw)
    except Exception:
        return None


def detect_families(strings):
    s = ' '.join([x for x in strings if x]).lower()
    return [k for k in FAMILY_KEYS if k in s]


def family_guess_from_catalog(sample_ids, owned_by):
    found = detect_families(sample_ids + owned_by)
    scores = {k: 0 for k in ['gpt','claude','gemini','glm','qwen','kimi','minimax','deepseek']}
    for fam in scores:
        if fam in found:
            scores[fam] += 2
    if 'moonshot' in found:
        scores['kimi'] += 2
    ranked = [(k, v) for k, v in scores.items() if v > 0]
    ranked.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in ranked]


def extract_openai_text(data, ek):
    if not isinstance(data, dict):
        return None
    if ek == 'responses':
        parts = []
        for item in data.get('output', []):
            if item.get('type') == 'message':
                for c in item.get('content', []):
                    if c.get('type') == 'output_text':
                        parts.append(c.get('text', ''))
        return ''.join(parts).strip() if parts else None
    try:
        text = data['choices'][0]['message']['content']
        return text.strip() if isinstance(text, str) else text
    except Exception:
        return None


def extract_anthropic_text(data):
    if not isinstance(data, dict):
        return None
    arr = data.get('content', [])
    if isinstance(arr, list):
        return ''.join([x.get('text', '') for x in arr if isinstance(x, dict) and x.get('type') == 'text']).strip() or None
    return None


def extract_gemini_text(data):
    if not isinstance(data, dict):
        return None
    try:
        return data['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception:
        return None


def openai_call(base_url, api_key, model, prompt, endpoint='responses', timeout=20, stream=False):
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    path = '/responses' if endpoint == 'responses' else '/chat/completions'
    body = {'model': model, 'input': prompt, 'max_output_tokens': 256} if endpoint == 'responses' else {'model': model, 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 256, 'temperature': 0}
    if stream:
        body['stream'] = True
    ok, http, lat, raw = _request(base_url.rstrip('/') + path, headers=headers, body=body, timeout=timeout)
    data = parse_json(raw) if ok and not stream else None
    return {
        'ok': ok, 'http': http, 'latency_s': lat,
        'text': extract_openai_text(data, endpoint) if data else None,
        'usage': data.get('usage') if isinstance(data, dict) else None,
        'object': data.get('object') if isinstance(data, dict) else None,
        'raw_preview': raw[:220]
    }


def anthropic_call(base_url, api_key, model, prompt, timeout=20):
    headers = {'x-api-key': api_key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    body = {'model': model, 'max_tokens': 256, 'messages': [{'role': 'user', 'content': prompt}]}
    ok, http, lat, raw = _request(base_url.rstrip('/') + '/v1/messages', headers=headers, body=body, timeout=timeout)
    data = parse_json(raw) if ok else None
    return {
        'ok': ok, 'http': http, 'latency_s': lat,
        'text': extract_anthropic_text(data) if data else None,
        'usage': data.get('usage') if isinstance(data, dict) else None,
        'object': data.get('type') if isinstance(data, dict) else None,
        'raw_preview': raw[:220]
    }


def gemini_call(base_url, api_key, model, prompt, timeout=20):
    base = base_url.rstrip('/')
    q = urllib.parse.urlencode({'key': api_key})
    body = {'contents': [{'parts': [{'text': prompt}]}]}
    last = {'ok': False, 'http': None, 'latency_s': None, 'text': None, 'usage': None, 'object': None, 'endpoint': None, 'raw_preview': ''}
    for p in [f'/v1beta/models/{model}:generateContent?{q}', f'/v1/models/{model}:generateContent?{q}']:
        ok, http, lat, raw = _request(base + p, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}, body=body, timeout=timeout)
        if ok:
            data = parse_json(raw)
            return {
                'ok': ok, 'http': http, 'latency_s': lat,
                'text': extract_gemini_text(data),
                'usage': data.get('usageMetadata') if isinstance(data, dict) else None,
                'object': 'gemini.generateContent',
                'endpoint': p.split('?')[0],
                'raw_preview': raw[:220]
            }
        last = {'ok': ok, 'http': http, 'latency_s': lat, 'text': None, 'usage': None, 'object': None, 'endpoint': p.split('?')[0], 'raw_preview': raw[:220]}
    return last


def openai_probe(base_url, api_key, model, timeout=20):
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    ok, http, lat, raw = _request(base_url.rstrip('/') + '/models', headers=headers, timeout=timeout)
    data = parse_json(raw) if ok else None
    models = data.get('data', []) if isinstance(data, dict) else []
    ids = [m.get('id') for m in models if isinstance(m, dict)]
    owned = sorted({m.get('owned_by') for m in models if isinstance(m, dict) and m.get('owned_by')})
    families = detect_families(ids)
    catalog = {
        'ok': ok, 'http': http, 'latency_s': lat, 'count': len(models), 'sample_ids': ids[:20],
        'families_detected': families, 'owned_by': owned[:20],
        'family_guess_from_catalog': family_guess_from_catalog(ids[:100], owned[:50]),
        'mixed_pool_signal': len(set(families)) >= 3 or len(owned) >= 3,
        'raw_preview': raw[:250]
    }
    endpoints = []
    for ek in ['responses', 'chat']:
        row = openai_call(base_url, api_key, model, 'Reply with exactly OK', endpoint=ek, timeout=timeout)
        row['endpoint'] = ek
        endpoints.append(row)
    return {'family': 'openai-compatible', 'catalog': catalog, 'endpoints': endpoints}


def anthropic_probe(base_url, api_key, model, timeout=20):
    row = anthropic_call(base_url, api_key, model, 'Reply with exactly OK', timeout=timeout)
    return {'family': 'anthropic', 'catalog': None, 'endpoints': [{'endpoint': 'v1/messages', **row}]}


def gemini_probe(base_url, api_key, model, timeout=20):
    base = base_url.rstrip('/')
    q = urllib.parse.urlencode({'key': api_key})
    cat = None
    for p in [f'/v1beta/models?{q}', f'/v1/models?{q}']:
        ok, http, lat, raw = _request(base + p, headers={'User-Agent': 'Mozilla/5.0'}, timeout=timeout)
        if ok:
            data = parse_json(raw) or {}
            models = data.get('models', []) if isinstance(data, dict) else []
            names = [m.get('name') for m in models if isinstance(m, dict)]
            families = detect_families(names)
            cat = {
                'ok': ok, 'http': http, 'latency_s': lat, 'count': len(models), 'sample_ids': names[:20],
                'families_detected': families,
                'family_guess_from_catalog': family_guess_from_catalog(names[:100], []),
                'mixed_pool_signal': len(set(families)) >= 2,
                'raw_preview': raw[:250]
            }
            break
    row = gemini_call(base_url, api_key, model, 'Reply with exactly OK', timeout=timeout)
    return {'family': 'gemini', 'catalog': cat, 'endpoints': [row]}


def run_stability_openai(base_url, api_key, model, endpoint):
    runs, lats = [], []
    for i in range(5):
        row = openai_call(base_url, api_key, model, 'Reply with exactly OK', endpoint=endpoint)
        row['run'] = i + 1
        runs.append(row)
        if row['ok']:
            lats.append(row['latency_s'])
    return {'runs': runs, 'success_rate': sum(1 for r in runs if r['ok']) / 5, 'latency_avg_s': round(statistics.mean(lats), 2) if lats else None}


def run_stability_anthropic(base_url, api_key, model):
    runs, lats = [], []
    for i in range(5):
        row = anthropic_call(base_url, api_key, model, 'Reply with exactly OK')
        row['run'] = i + 1
        runs.append(row)
        if row['ok']:
            lats.append(row['latency_s'])
    return {'runs': runs, 'success_rate': sum(1 for r in runs if r['ok']) / 5, 'latency_avg_s': round(statistics.mean(lats), 2) if lats else None}


def run_stability_gemini(base_url, api_key, model):
    runs, lats = [], []
    for i in range(5):
        row = gemini_call(base_url, api_key, model, 'Reply with exactly OK')
        row['run'] = i + 1
        runs.append(row)
        if row['ok']:
            lats.append(row['latency_s'])
    return {'runs': runs, 'success_rate': sum(1 for r in runs if r['ok']) / 5, 'latency_avg_s': round(statistics.mean(lats), 2) if lats else None}


def run_tests_openai(base_url, api_key, model, endpoint, tests):
    return [{**openai_call(base_url, api_key, model, prompt, endpoint=endpoint), 'label': label} for label, prompt in tests]


def run_tests_anthropic(base_url, api_key, model, tests):
    return [{**anthropic_call(base_url, api_key, model, prompt), 'label': label} for label, prompt in tests]


def run_tests_gemini(base_url, api_key, model, tests):
    return [{**gemini_call(base_url, api_key, model, prompt), 'label': label} for label, prompt in tests]


def variance_summary(rows):
    texts = [r.get('text') or '' for r in rows if r.get('ok')]
    if not texts:
        return None
    hashes = [hashlib.md5(t.encode()).hexdigest() for t in texts]
    unique = len(set(hashes))
    return {'runs': len(texts), 'unique_outputs': unique, 'variance_ratio': round(unique / len(texts), 2)}


def deep_suite_openai(base_url, api_key, model, endpoint):
    advanced = run_tests_openai(base_url, api_key, model, endpoint, DEEP_TESTS)
    variance = run_tests_openai(base_url, api_key, model, endpoint, [('variance_repeat', 'In one sentence, explain why rainbows form.')] * 5)
    malformed = _request(base_url.rstrip('/') + ('/responses' if endpoint == 'responses' else '/chat/completions'), headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}, body={'model': model}, timeout=20)
    stream_probe = openai_call(base_url, api_key, model, 'Reply with exactly OK', endpoint=endpoint, stream=True)
    error_probe = {'ok': malformed[0], 'http': malformed[1], 'latency_s': malformed[2], 'raw_preview': malformed[3][:220]}
    return {'advanced_tests': advanced, 'variance_profile': variance_summary(variance), 'variance_runs': variance, 'error_probe': error_probe, 'stream_probe': stream_probe}


def deep_suite_anthropic(base_url, api_key, model):
    advanced = run_tests_anthropic(base_url, api_key, model, DEEP_TESTS)
    variance = run_tests_anthropic(base_url, api_key, model, [('variance_repeat', 'In one sentence, explain why rainbows form.')] * 5)
    malformed = _request(base_url.rstrip('/') + '/v1/messages', headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0'}, body={'model': model}, timeout=20)
    error_probe = {'ok': malformed[0], 'http': malformed[1], 'latency_s': malformed[2], 'raw_preview': malformed[3][:220]}
    return {'advanced_tests': advanced, 'variance_profile': variance_summary(variance), 'variance_runs': variance, 'error_probe': error_probe}


def deep_suite_gemini(base_url, api_key, model):
    advanced = run_tests_gemini(base_url, api_key, model, DEEP_TESTS)
    variance = run_tests_gemini(base_url, api_key, model, [('variance_repeat', 'In one sentence, explain why rainbows form.')] * 5)
    base = base_url.rstrip('/')
    q = urllib.parse.urlencode({'key': api_key})
    malformed = _request(base + f'/v1beta/models/{model}:generateContent?{q}', headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}, body={}, timeout=20)
    error_probe = {'ok': malformed[0], 'http': malformed[1], 'latency_s': malformed[2], 'raw_preview': malformed[3][:220]}
    return {'advanced_tests': advanced, 'variance_profile': variance_summary(variance), 'variance_runs': variance, 'error_probe': error_probe}


def infer_family_fingerprint(model, probe, declared_family):
    scores = {k: 0 for k in ['gpt', 'claude', 'gemini', 'glm', 'qwen', 'kimi', 'minimax', 'deepseek']}
    m = (model or '').lower()
    if 'gpt' in m:
        scores['gpt'] += 3
    if 'claude' in m:
        scores['claude'] += 3
    if 'gemini' in m:
        scores['gemini'] += 3
    if 'glm' in m:
        scores['glm'] += 3
    if 'qwen' in m or 'tongyi' in m:
        scores['qwen'] += 3
    if 'kimi' in m or 'moonshot' in m:
        scores['kimi'] += 3
    if 'minimax' in m:
        scores['minimax'] += 3
    if 'deepseek' in m:
        scores['deepseek'] += 3
    if declared_family == 'anthropic':
        scores['claude'] += 4
    if declared_family == 'gemini':
        scores['gemini'] += 4
    if declared_family == 'glm':
        scores['glm'] += 4
    cat = probe.get('catalog') or {}
    for fam in cat.get('family_guess_from_catalog', []):
        if fam in scores:
            scores[fam] += 3
    endpoints = probe.get('endpoints') or []
    if any(e.get('endpoint') == 'v1/messages' and e.get('ok') for e in endpoints):
        scores['claude'] += 6
    if any('generateContent' in (e.get('endpoint') or '') and e.get('ok') for e in endpoints):
        scores['gemini'] += 6
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return {'scores': scores, 'top_candidates': [x for x in ranked if x[1] > 0][:4], 'most_likely_family': ranked[0][0] if ranked and ranked[0][1] > 0 else None}


def classify(probe):
    endpoints = probe.get('endpoints') or []
    working = [e for e in endpoints if e.get('ok')]
    mixed = bool((probe.get('catalog') or {}).get('mixed_pool_signal'))
    if not working:
        return 'low-confidence-or-unusable'
    if mixed:
        return 'high-confidence-multi-model-aggregation-pool'
    stability = (probe.get('stability') or {}).get('success_rate')
    fp = probe.get('family_fingerprint') or {}
    top = fp.get('top_candidates') or []
    lead_gap_ok = len(top) == 1 or (len(top) >= 2 and top[0][1] - top[1][1] >= 3)
    advanced = probe.get('advanced') or {}
    variance = (advanced.get('variance_profile') or {}).get('variance_ratio')
    error_preview = ((advanced.get('error_probe') or {}).get('raw_preview') or '').lower()
    gateway_red_flag = 'server error' in error_preview
    if stability == 1.0 and lead_gap_ok and not gateway_red_flag and (variance is None or variance >= 0.2):
        return 'high-confidence-focused-or-genuine-route'
    return 'medium-confidence-likely-routed-or-wrapped'


def summarize_report(results):
    report = {
        '已配置但不可用': [],
        '当前可用': [],
        '协议层': [],
        '疑似模型家族': [],
        '需要人工复核': []
    }
    for name, item in results.items():
        endpoints = item.get('endpoints') or []
        working = [e for e in endpoints if e.get('ok')]
        protocol = item.get('family')
        judgment = item.get('judgment')
        mixed_pool = bool((item.get('catalog') or {}).get('mixed_pool_signal'))
        raw_family_guess = (item.get('family_fingerprint') or {}).get('most_likely_family')
        family_guess = raw_family_guess
        if not working or mixed_pool:
            family_guess = None
        row = {
            'provider': name,
            'model': item.get('model'),
            'judgment': judgment,
            'protocol_layer': protocol,
            'suspected_family': family_guess
        }
        if working:
            report['当前可用'].append(row)
        else:
            report['已配置但不可用'].append(row)
        report['协议层'].append({'provider': name, 'protocol_layer': protocol, 'working_endpoints': [e.get('endpoint') for e in working]})
        report['疑似模型家族'].append({'provider': name, 'suspected_family': family_guess, 'top_candidates': (item.get('family_fingerprint') or {}).get('top_candidates')})
        need_review = False
        if judgment == 'high-confidence-multi-model-aggregation-pool':
            need_review = True
        if family_guess is None:
            need_review = True
        if need_review:
            report['需要人工复核'].append({**row, 'raw_family_guess': raw_family_guess})
    return report


def probe_one(name, family, base_url, api_key, model, deep=False):
    fam = family
    if fam == 'auto':
        if 'generativelanguage.googleapis.com' in base_url:
            fam = 'gemini'
        elif 'anthropic.com' in base_url:
            fam = 'anthropic'
        else:
            fam = 'openai'
    if fam in ['openai', 'glm']:
        probe = openai_probe(base_url, api_key, model)
        chosen = 'responses' if any(e['ok'] and e['endpoint'] == 'responses' for e in probe['endpoints']) else ('chat' if any(e['ok'] and e['endpoint'] == 'chat' for e in probe['endpoints']) else None)
        probe['stability'] = run_stability_openai(base_url, api_key, model, chosen) if chosen else None
        probe['capabilities'] = run_tests_openai(base_url, api_key, model, chosen, BASIC_TESTS) if chosen else []
        probe['advanced'] = deep_suite_openai(base_url, api_key, model, chosen) if chosen and deep else None
    elif fam == 'anthropic':
        probe = anthropic_probe(base_url, api_key, model)
        probe['stability'] = run_stability_anthropic(base_url, api_key, model)
        probe['capabilities'] = run_tests_anthropic(base_url, api_key, model, BASIC_TESTS)
        probe['advanced'] = deep_suite_anthropic(base_url, api_key, model) if deep else None
    elif fam == 'gemini':
        probe = gemini_probe(base_url, api_key, model)
        probe['stability'] = run_stability_gemini(base_url, api_key, model)
        probe['capabilities'] = run_tests_gemini(base_url, api_key, model, BASIC_TESTS)
        probe['advanced'] = deep_suite_gemini(base_url, api_key, model) if deep else None
    else:
        raise ValueError(fam)
    probe['declared_family'] = family
    probe['family_fingerprint'] = infer_family_fingerprint(model, probe, fam)
    probe['judgment'] = classify(probe)
    probe['name'] = name
    probe['baseUrl'] = base_url
    probe['model'] = model
    return probe


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config')
    ap.add_argument('--providers', nargs='*', default=[])
    ap.add_argument('--model', required=True)
    ap.add_argument('--family', default='auto', choices=['auto', 'openai', 'anthropic', 'gemini', 'glm'])
    ap.add_argument('--base-url')
    ap.add_argument('--api-key')
    ap.add_argument('--name', default='custom')
    ap.add_argument('--deep', action='store_true')
    ap.add_argument('--report-only', action='store_true')
    args = ap.parse_args()
    out = {}
    if args.base_url and args.api_key:
        out[args.name] = probe_one(args.name, args.family, args.base_url, args.api_key, args.model, deep=args.deep)
    else:
        cfg = json.loads(Path(args.config).read_text())
        for name in args.providers:
            p = cfg['models']['providers'][name]
            fam = args.family
            if fam == 'auto':
                api = (p.get('api') or '').lower()
                if 'anthropic' in api:
                    fam = 'anthropic'
                elif 'gemini' in api:
                    fam = 'gemini'
                elif 'glm' in api:
                    fam = 'glm'
                else:
                    fam = 'openai'
            out[name] = probe_one(name, fam, p['baseUrl'], p['apiKey'], args.model, deep=args.deep)
    if args.report_only:
        print(json.dumps(summarize_report(out), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
