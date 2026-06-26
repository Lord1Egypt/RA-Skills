#!/usr/bin/env python3
import argparse, json, os, pathlib, random, re, subprocess, sys, time

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
GEN_SCRIPT = SKILL_DIR / 'scripts/generate-image.js'
DEFAULT_OUTPUT_DIR = os.path.expanduser('~/.openclaw/generated-images')

RETRYABLE_CATEGORIES = {'timeout', 'upstream_failure', 'rate_limit', 'rate_limited', 'wrapper_error'}
RETRYABLE_STAGES = {'timeout', 'request', 'wrapper_parse', 'batch_timeout'}

def safe_err(s):
    s = str(s)
    s = re.sub(r'sk-[A-Za-z0-9_\-]{8,}', 'sk-***', s)
    s = re.sub(r'Bearer\s+[A-Za-z0-9_\.\-]+', 'Bearer ***', s, flags=re.I)
    s = re.sub(r'(app_secret|appSecret|apiKey|api_key|token|secret)["\']?\s*[:=]\s*["\'][^"\']+', r'\1:"[redacted]', s, flags=re.I)
    return s[-4000:]

def is_retryable(data):
    if data.get('ok'): return False
    diag = data.get('diagnosis') or {}
    return bool(diag.get('retryable') or diag.get('category') in RETRYABLE_CATEGORIES or (data.get('stage') in RETRYABLE_STAGES and data.get('http_status') in (None,408,429,500,502,503,504)) or data.get('http_status') in (408,429,500,502,503,504))

def delay_for(attempt_index, base_delay, max_delay, jitter):
    delay = min(max_delay, base_delay * (2 ** (attempt_index - 1)))
    return delay + (random.uniform(0, jitter) if jitter > 0 else 0)

def slugify(name):
    name = name or 'happy-img2-direct'
    name = re.sub(r'[^A-Za-z0-9._-]+', '-', name).strip('-._')
    return name[:80] or 'happy-img2-direct'

def main():
    ap = argparse.ArgumentParser(description='Generate one image via an OpenAI-compatible images API provider configured in OpenClaw.')
    ap.add_argument('--prompt', required=True)
    ap.add_argument('--task-name', default='happy-img2-direct')
    ap.add_argument('--provider', default=os.environ.get('OPENCLAW_IMAGE_PROVIDER', 'happy'))
    ap.add_argument('--model', default=os.environ.get('OPENCLAW_IMAGE_MODEL', 'gpt-image-2'))
    ap.add_argument('--size', default='1024x1024')
    ap.add_argument('--timeout-ms', type=int, default=600000)
    ap.add_argument('--output-dir', default=DEFAULT_OUTPUT_DIR)
    ap.add_argument('--raw', action='store_true', help='marker only: keep prompt as-is')
    ap.add_argument('--max-attempts', type=int, default=3)
    ap.add_argument('--retry-base-delay', type=float, default=8.0)
    ap.add_argument('--retry-max-delay', type=float, default=45.0)
    ap.add_argument('--retry-jitter', type=float, default=5.0)
    # Compatibility flags. Sending is intentionally not implemented in the public skill.
    ap.add_argument('--no-send', action='store_true')
    ap.add_argument('--to-open-id', default='')
    args = ap.parse_args()

    max_attempts = max(1, min(5, args.max_attempts))
    output_dir = pathlib.Path(os.path.expanduser(args.output_dir))
    output_dir.mkdir(parents=True, exist_ok=True)
    run_dir = output_dir / '_runs' / f"{slugify(args.task_name)}-{time.strftime('%Y%m%d-%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    attempts=[]; final_data=None
    for attempt in range(1, max_attempts+1):
        attempt_name = args.task_name if attempt == 1 else f"{args.task_name}-retry{attempt}"
        output = output_dir / f"{slugify(attempt_name)}-{time.strftime('%Y%m%d-%H%M%S')}.png"
        cmd = ['node', str(GEN_SCRIPT), '--prompt', args.prompt, '--output', str(output), '--provider', args.provider, '--model', args.model, '--size', args.size, '--timeout-ms', str(args.timeout_ms)]
        attempt_dir = run_dir / f'attempt-{attempt:02d}'; attempt_dir.mkdir(parents=True, exist_ok=True)
        (attempt_dir/'request.json').write_text(json.dumps({'prompt': args.prompt, 'task_name': attempt_name, 'provider': args.provider, 'model': args.model, 'size': args.size, 'timeout_ms': args.timeout_ms, 'output': str(output)}, ensure_ascii=False, indent=2), encoding='utf-8')
        started=time.time()
        try:
            proc=subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=args.timeout_ms/1000+90)
            stdout=proc.stdout or ''; stderr=proc.stderr or ''
            try: data=json.loads(stdout.strip())
            except Exception: data={'ok':False,'stage':'wrapper_parse','returncode':proc.returncode,'stdout':stdout[-4000:],'stderr':stderr[-4000:],'diagnosis':{'category':'wrapper_error','human_reason':'Generator did not return parseable JSON.','retryable':True}}
        except subprocess.TimeoutExpired as e:
            stdout=e.stdout if isinstance(e.stdout,str) else ''; stderr=e.stderr if isinstance(e.stderr,str) else ''
            data={'ok':False,'stage':'wrapper_timeout','error':f'outer wrapper timeout after {args.timeout_ms/1000+90}s','diagnosis':{'category':'timeout','human_reason':'Outer wrapper timed out.','retryable':True}}
        elapsed=round(time.time()-started,3)
        (attempt_dir/'stdout.txt').write_text(stdout or '', encoding='utf-8')
        (attempt_dir/'stderr.txt').write_text(stderr or '', encoding='utf-8')
        data.update({'attempt':attempt,'max_attempts':max_attempts,'elapsed_seconds':elapsed,'attempt_dir':str(attempt_dir)})
        (attempt_dir/'result.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        attempts.append(data)
        if data.get('ok'):
            final_data=data; break
        if attempt < max_attempts and is_retryable(data): time.sleep(delay_for(attempt,args.retry_base_delay,args.retry_max_delay,args.retry_jitter))
        elif attempt < max_attempts: break
    if final_data:
        result={**final_data,'attempts_count':len(attempts),'run_dir':str(run_dir)}
        print(json.dumps(result,ensure_ascii=False,indent=2)); sys.exit(0)
    result={'ok':False,'stage':'failed_after_retries','error':safe_err(attempts[-1] if attempts else 'unknown'),'attempts_count':len(attempts),'run_dir':str(run_dir),'attempts':attempts}
    print(json.dumps(result,ensure_ascii=False,indent=2)); sys.exit(1)
if __name__ == '__main__': main()
