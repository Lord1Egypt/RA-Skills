#!/usr/bin/env python3
import argparse, concurrent.futures, json, os, pathlib, subprocess, sys, time, uuid

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
WORKSPACE = pathlib.Path(os.environ.get('OPENCLAW_WORKSPACE', os.getcwd())).resolve()
RUNNER = SKILL_DIR / 'scripts/run.py'


def load_input(arg):
    if arg.startswith('@'):
        return json.loads(pathlib.Path(arg[1:]).read_text(encoding='utf-8'))
    return json.loads(arg)


def safe_name(s):
    keep=[]
    for ch in str(s):
        if ch.isalnum() or ch in '-_': keep.append(ch)
        else: keep.append('-')
    return ''.join(keep).strip('-')[:80] or 'task'


def run_one(task, defaults, batch_dir):
    idx = task['_index']
    name = safe_name(task.get('task_name') or f'task-{idx+1}')
    task_dir = batch_dir / f'{idx+1:02d}-{name}'
    task_dir.mkdir(parents=True, exist_ok=True)

    prompt = task.get('prompt')
    if not prompt:
        result = {'ok': False, 'stage': 'invalid_task', 'error': 'missing prompt', 'index': idx, 'task_name': name}
        (task_dir / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        return result

    timeout_ms = int(task.get('timeout_ms') or defaults['timeout_ms'])
    to_open_id = task.get('to_open_id') or defaults.get('to_open_id') or ''
    send = bool(task.get('send_to_feishu', defaults.get('send_to_feishu', False)))

    cmd = [
        'python3', str(RUNNER),
        '--prompt', prompt,
        '--task-name', name,
        '--size', task.get('size') or defaults.get('size') or '1024x1024',
        '--timeout-ms', str(timeout_ms),
    ]
    # Public skill is generation-only; delivery should be handled by OpenClaw/channel tools.
    cmd += ['--no-send']
    if task.get('raw') or defaults.get('raw'):
        cmd += ['--raw']

    meta = {
        'index': idx,
        'task_name': name,
        'prompt': prompt,
        'cmd': cmd,
        'timeout_ms': timeout_ms,
        'send_to_feishu': send,
        'task_dir': str(task_dir),
        'started_at': time.strftime('%Y-%m-%dT%H:%M:%S%z')
    }
    (task_dir / 'batch_task.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(WORKSPACE),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_ms/1000 + 120,
        )
        (task_dir / 'stdout.txt').write_text(proc.stdout or '', encoding='utf-8')
        (task_dir / 'stderr.txt').write_text(proc.stderr or '', encoding='utf-8')
        try:
            data = json.loads((proc.stdout or '').strip())
        except Exception:
            data = {
                'ok': False,
                'stage': 'batch_parse',
                'returncode': proc.returncode,
                'stdout_tail': (proc.stdout or '')[-3000:],
                'stderr_tail': (proc.stderr or '')[-3000:],
            }
        data.update({'index': idx, 'task_name': name, 'batch_task_dir': str(task_dir), 'finished_at': time.strftime('%Y-%m-%dT%H:%M:%S%z')})
    except subprocess.TimeoutExpired as e:
        data = {
            'ok': False,
            'stage': 'batch_timeout',
            'index': idx,
            'task_name': name,
            'error': f'task exceeded wrapper timeout after {timeout_ms/1000 + 120}s',
            'diagnosis': {'category': 'timeout', 'human_reason': '批量任务外层等待超时。', 'retryable': True},
            'batch_task_dir': str(task_dir),
            'finished_at': time.strftime('%Y-%m-%dT%H:%M:%S%z')
        }
        (task_dir / 'stdout.txt').write_text((e.stdout or '') if isinstance(e.stdout, str) else '', encoding='utf-8')
        (task_dir / 'stderr.txt').write_text((e.stderr or '') if isinstance(e.stderr, str) else '', encoding='utf-8')

    (task_dir / 'result.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return data


def main():
    ap = argparse.ArgumentParser(description='Batch runner for happy-img2-direct')
    ap.add_argument('input', help='JSON string or @path')
    args = ap.parse_args()
    cfg = load_input(args.input)
    tasks = cfg.get('tasks') or []
    if not isinstance(tasks, list) or not tasks:
        print(json.dumps({'ok': False, 'stage': 'invalid_input', 'error': 'tasks must be non-empty list'}, ensure_ascii=False, indent=2))
        sys.exit(1)

    max_workers = max(1, min(4, int(cfg.get('max_workers') or 4)))
    defaults = {
        'timeout_ms': int(cfg.get('timeout_ms') or 600000),
        'to_open_id': cfg.get('to_open_id') or '',
        'send_to_feishu': bool(cfg.get('send_to_feishu', False)),
        'size': cfg.get('size') or '1024x1024',
        'raw': bool(cfg.get('raw', False)),
    }
    batch_name = safe_name(cfg.get('batch_name') or 'happy-img2-batch')
    batch_dir = WORKSPACE / 'content-factory/live-course-design/img2/batches' / f"{batch_name}-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    batch_dir.mkdir(parents=True, exist_ok=True)
    (batch_dir / 'batch_request.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8')

    for i,t in enumerate(tasks):
        t['_index']=i

    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs=[ex.submit(run_one, t, defaults, batch_dir) for t in tasks]
        for fut in concurrent.futures.as_completed(futs):
            results.append(fut.result())
    results.sort(key=lambda x: x.get('index', 999999))
    summary = {
        'ok': all(r.get('ok') for r in results),
        'stage': 'done',
        'batch_dir': str(batch_dir),
        'max_workers': max_workers,
        'total': len(results),
        'success': sum(1 for r in results if r.get('ok')),
        'failed': sum(1 for r in results if not r.get('ok')),
        'provider': 'happy',
        'model': 'gpt-image-2',
        'no_local_fallback': True,
        'results': results,
    }
    (batch_dir / 'batch_result.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    sys.exit(0 if summary['ok'] else 1)

if __name__ == '__main__':
    main()
