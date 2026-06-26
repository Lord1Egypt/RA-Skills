#!/usr/bin/env python3
import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
from pathlib import Path

TESTS = [
    ('exact_ok', 'Reply with exactly OK'),
    ('math_only', 'Compute 17*19 and answer with digits only.'),
    ('json_only', 'Return valid minified JSON only: {"animal":"cat","n":3}'),
    ('format_strict', 'Return exactly three lines and nothing else:\nA\nB\nC')
]


def http_call(base_url, api_key, endpoint_kind, model, prompt, timeout=25):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0',
    }
    base = base_url.rstrip('/')
    if endpoint_kind == 'responses':
        url = base + '/responses'
        body = {'model': model, 'input': prompt, 'max_output_tokens': 128}
    elif endpoint_kind == 'chat':
        url = base + '/chat/completions'
        body = {'model': model, 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 128, 'temperature': 0}
    elif endpoint_kind == 'models':
        url = base + '/models'
        body = None
    else:
        raise ValueError(endpoint_kind)
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method='GET' if body is None else 'POST')
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode('utf-8', errors='ignore')
            return True, r.status, round(time.time() - started, 2), raw
    except urllib.error.HTTPError as e:
        return False, e.code, round(time.time() - started, 2), e.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return False, None, round(time.time() - started, 2), f'{type(e).__name__}: {e}'


def parse_response(endpoint_kind, raw):
    try:
        data = json.loads(raw)
    except Exception:
        return {'parse_ok': False, 'object': None, 'model': None, 'text': None, 'usage': None, 'data': None}
    if endpoint_kind == 'responses':
        parts = []
        for item in data.get('output', []):
            if item.get('type') == 'message':
                for c in item.get('content', []):
                    if c.get('type') == 'output_text':
                        parts.append(c.get('text', ''))
        text = ''.join(parts).strip() if parts else None
    elif endpoint_kind == 'chat':
        text = None
        try:
            text = data['choices'][0]['message']['content']
        except Exception:
            pass
        if isinstance(text, str):
            text = text.strip()
    else:
        text = None
    return {'parse_ok': True, 'object': data.get('object'), 'model': data.get('model'), 'text': text, 'usage': data.get('usage'), 'data': data}


def summarize_models(raw):
    parsed = parse_response('models', raw)
    data = parsed['data'] or {}
    models = data.get('data', []) if isinstance(data, dict) else []
    ids = [m.get('id') for m in models if isinstance(m, dict)]
    owned = sorted({m.get('owned_by') for m in models if isinstance(m, dict) and m.get('owned_by')})
    families = []
    for keyword in ['gpt', 'claude', 'deepseek', 'kimi', 'moonshot', 'gemini', 'qwen', 'grok']:
        if any(keyword in (mid or '').lower() for mid in ids):
            families.append(keyword)
    return {
        'count': len(models),
        'sample_ids': ids[:20],
        'owned_by': owned[:20],
        'families_detected': families,
        'mixed_pool_signal': len(families) >= 3 or len(owned) >= 3,
    }


def run_provider(name, base_url, api_key, model):
    result = {'name': name, 'baseUrl': base_url, 'model': model}
    ok, http, latency, raw = http_call(base_url, api_key, 'models', model, '', timeout=20)
    result['models_probe'] = {'ok': ok, 'http': http, 'latency_s': latency, 'summary': summarize_models(raw) if ok else None, 'raw_preview': raw[:300]}

    endpoint_probes = []
    for ek in ['responses', 'chat']:
        ok, http, latency, raw = http_call(base_url, api_key, ek, model, 'Reply with exactly OK', timeout=20)
        parsed = parse_response(ek, raw) if ok else {'parse_ok': False, 'object': None, 'model': None, 'text': None, 'usage': None}
        endpoint_probes.append({'endpoint': ek, 'ok': ok, 'http': http, 'latency_s': latency, **parsed, 'raw_preview': raw[:250]})
    result['endpoint_probes'] = endpoint_probes

    working = [x for x in endpoint_probes if x['ok']]
    chosen = sorted(working, key=lambda x: x['latency_s'])[0]['endpoint'] if working else None
    result['chosen_endpoint'] = chosen
    result['stability_runs'] = []
    result['capability_runs'] = []
    if not chosen:
        result['judgment'] = 'low-confidence-or-unusable'
        return result

    latencies = []
    success = 0
    for i in range(5):
        ok, http, latency, raw = http_call(base_url, api_key, chosen, model, 'Reply with exactly OK')
        parsed = parse_response(chosen, raw) if ok else {'parse_ok': False, 'object': None, 'model': None, 'text': None, 'usage': None}
        result['stability_runs'].append({'run': i + 1, 'ok': ok, 'http': http, 'latency_s': latency, **parsed, 'raw_preview': raw[:200]})
        if ok:
            success += 1
            latencies.append(latency)

    for label, prompt in TESTS:
        ok, http, latency, raw = http_call(base_url, api_key, chosen, model, prompt)
        parsed = parse_response(chosen, raw) if ok else {'parse_ok': False, 'object': None, 'model': None, 'text': None, 'usage': None}
        result['capability_runs'].append({'label': label, 'ok': ok, 'http': http, 'latency_s': latency, **parsed, 'raw_preview': raw[:200]})

    mixed_pool = bool(result['models_probe']['summary'] and result['models_probe']['summary']['mixed_pool_signal'])
    stability = success / 5
    avg_latency = round(statistics.mean(latencies), 2) if latencies else None
    reasoning_hits = 0
    for row in result['capability_runs'] + result['stability_runs']:
        usage = row.get('usage') or {}
        if isinstance(usage, dict):
            od = usage.get('output_tokens_details') or usage.get('completion_tokens_details') or {}
            if isinstance(od, dict) and od.get('reasoning_tokens', 0):
                reasoning_hits += 1

    if stability == 1.0 and not mixed_pool and reasoning_hits >= 2:
        judgment = 'high-confidence-real-or-focused-route'
    elif stability >= 0.8:
        judgment = 'medium-confidence-likely-routed-or-wrapped'
    else:
        judgment = 'low-confidence-or-unusable'

    result['summary'] = {
        'stability_success_rate': stability,
        'latency_avg_s': avg_latency,
        'latency_min_s': min(latencies) if latencies else None,
        'latency_max_s': max(latencies) if latencies else None,
        'reasoning_signal_hits': reasoning_hits,
        'mixed_pool_signal': mixed_pool,
    }
    result['judgment'] = judgment
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config')
    ap.add_argument('--providers', nargs='*', default=[])
    ap.add_argument('--model', required=True)
    ap.add_argument('--base-url')
    ap.add_argument('--api-key')
    ap.add_argument('--name', default='custom')
    args = ap.parse_args()

    results = {}
    if args.base_url and args.api_key:
        results[args.name] = run_provider(args.name, args.base_url, args.api_key, args.model)
    else:
        cfg = json.loads(Path(args.config).read_text())
        for name in args.providers:
            p = cfg['models']['providers'][name]
            results[name] = run_provider(name, p['baseUrl'], p['apiKey'], args.model)

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
