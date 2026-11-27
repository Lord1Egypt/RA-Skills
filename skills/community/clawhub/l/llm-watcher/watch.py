"""盯 —— 盯住你正在用的模型，看它哪天悄悄变差

为什么有这个：
  每次厂商发新版、或者服务器吃紧，都会有人觉得「模型变笨了」。
  但没人能证明。手上只有手感、延迟、和一种说不清的口癖。

  这个工具只做一件事：
  用**你自己的活**，定期测一遍，把「感觉」变成「数据」。

  它只测能客观检验的东西：
    写得对不对（跑测试）、答案对不对（对答案）、格式对不对（验 schema）
  它不测写得好不好——实验测过，同一道题它每次写的东西
  有三分之二不一样，写得不一样不等于写得差，那个测不了。

用法：
    python analysis/watch.py init                      建一个空题库
    python analysis/watch.py run                       跑一轮，存快照
    python analysis/watch.py run --note "5.5发布后"     带个备注
    python analysis/watch.py compare                   和上一次比
    python analysis/watch.py list                      看历史快照

题库格式（tasks.json）：
    {
      "model": "qwen-plus",
      "provider": "dashscope",
      "tasks": [
        {"id": "fib", "prompt": "...", "check": {"type": "python", "code": "assert fib(10)==55"}},
        {"id": "math", "prompt": "...", "check": {"type": "contains", "any": ["221"]}},
        {"id": "fmt",  "prompt": "...", "check": {"type": "json", "expect": {"count": 42}}}
      ]
    }
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

def _find_home():
    """找题库和快照放哪。

    顺序：
      一、技能自己旁边（分发出去之后的正常情况）
      二、当前工作区下的 out/watch（开发时的位置）
      三、用户目录下的 .llm-watcher
    """
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(here, 'tasks.json')):
        return here
    ws = os.environ.get('LLM_WATCHER_HOME')
    if ws:
        return ws
    cwd_cand = os.path.join(os.getcwd(), 'out', 'watch')
    if os.path.isdir(cwd_cand):
        return cwd_cand
    return os.path.join(os.path.expanduser('~'), '.llm-watcher')


HOME = _find_home()
TASKS = os.path.join(HOME, 'tasks.json')
SNAPS = os.path.join(HOME, 'snapshots')
WS = os.getcwd()
PY = sys.executable

PROVIDERS = {
    'dashscope': 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
    'deepseek': 'https://api.deepseek.com/chat/completions',
}


# ══════════════════════ 检验器 ══════════════════════
# 每一条都不依赖模型判断，只看事实

def _strip_fence(t: str) -> str:
    m = re.search(r'```(?:\w+)?\s*(.*?)```', t, re.S)
    return m.group(1) if m else t


def check_contains(text, spec):
    any_ = spec.get('any') or []
    all_ = spec.get('all') or []
    low = text.lower()
    if any_ and not any(x.lower() in low for x in any_):
        return False, f'不含任何一项: {any_}'
    if all_ and not all(x.lower() in low for x in all_):
        missing = [x for x in all_ if x.lower() not in low]
        return False, f'缺: {missing}'
    return True, ''


def check_regex(text, spec):
    pat = spec.get('pattern', '')
    n = len(re.findall(pat, text, re.M))
    need = spec.get('at_least', 1)
    if n < need:
        return False, f'匹配 {n} 次，需要 >= {need}'
    return True, ''


def check_json(text, spec):
    s = _strip_fence(text).strip()
    try:
        d = json.loads(s)
    except Exception as e:
        return False, f'不是合法 JSON: {type(e).__name__}'
    for k, v in (spec.get('expect') or {}).items():
        if d.get(k) != v:
            return False, f'{k} = {d.get(k)!r}，期望 {v!r}'
    return True, ''


def check_python(text, spec):
    """把输出当代码真跑一遍"""
    code = _strip_fence(text)
    assertion = spec.get('code', '')
    if not assertion:
        return False, '没有断言'
    full = code + '\n\n' + assertion + '\nprint("__PASS__")\n'
    d = os.path.join(WS, '.tmp-watch')
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f'c_{hashlib.md5(full.encode()).hexdigest()[:8]}.py')
    try:
        open(p, 'w', encoding='utf-8').write(full)
        r = subprocess.run([PY, p], capture_output=True, text=True, timeout=25)
        ok = '__PASS__' in r.stdout
        msg = '' if ok else (r.stderr.strip().splitlines() or ['断言未通过'])[-1][:100]
        return ok, msg
    except Exception as e:
        return False, f'{type(e).__name__}'
    finally:
        try:
            os.unlink(p)
        except Exception:
            pass


def check_exact(text, spec):
    want = spec.get('value', '')
    got = text.strip()
    return (got == want), ('' if got == want else f'得到 {got[:40]!r}')


CHECKS = {
    'contains': check_contains,
    'regex': check_regex,
    'json': check_json,
    'python': check_python,
    'exact': check_exact,
}


# ══════════════════════ 调用 ══════════════════════

def load_key(provider: str) -> str:
    env = os.environ.get(f'{provider.upper()}_API_KEY') or os.environ.get('DASHSCOPE_API_KEY')
    if env:
        return env
    cfg = os.path.join(HOME, 'keys.json')
    if os.path.exists(cfg):
        return (json.load(open(cfg, encoding='utf-8')).get(provider) or '')
    # 兜底：今天验证过能用的那把
    return ("sk-ws-H.XMPEEEM.vGW6.MEQCIGuo3TOIG_-1Nv5_dw14M0zkh4vF7xPA48z5KcOV56ui"
            "AiBICyqC3stxzGszGSRBEP4GLUJuRgjlkSNgIu04Pt02NQ")


def call(prompt: str, model: str, provider: str, key: str,
         temperature: float = 1.0, timeout: int = 150) -> dict:
    url = PROVIDERS.get(provider)
    if not url:
        return {'err': f'不认识的 provider: {provider}'}
    body = {'model': model, 'messages': [{'role': 'user', 'content': prompt}],
            'temperature': temperature, 'max_tokens': 2000}
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    t0 = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
        j = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            eb = json.loads(e.read().decode())
            m = (eb.get('error') or {}).get('message') or ''
        except Exception:
            m = ''
        return {'err': f'HTTP {e.code} {m[:80]}'}
    except Exception as e:
        return {'err': f'{type(e).__name__}'}
    dt = time.time() - t0
    msg = (j.get('choices') or [{}])[0].get('message') or {}
    txt = msg.get('content') or ''
    u = j.get('usage') or {}
    return {'text': txt, 'ms': int(dt * 1000), 'chars': len(txt),
            'out_tok': u.get('completion_tokens') or 0,
            'in_tok': u.get('prompt_tokens') or 0}


# ══════════════════════ 命令 ══════════════════════

SAMPLE = {
    'model': 'qwen-plus',
    'provider': 'dashscope',
    'temperature': 1.0,
    'tasks': [
        {'id': 'arith', 'prompt': '13 乘以 17 等于多少？只输出数字。',
         'check': {'type': 'contains', 'any': ['221']}},
        {'id': 'fib', 'prompt': '用 Python 写一个 fib(n) 函数，返回第 n 个斐波那契数（fib(0)=0, fib(1)=1）。只输出代码。',
         'check': {'type': 'python',
                   'code': 'assert fib(0)==0\nassert fib(10)==55\nassert fib(20)==6765'}},
        {'id': 'fmt', 'prompt': '输出一个 JSON，包含 name="test"、count=42、ok=true。只输出 JSON。',
         'check': {'type': 'json', 'expect': {'name': 'test', 'count': 42, 'ok': True}}},
        {'id': 'list10', 'prompt': '列出 10 个提高代码可读性的具体做法，每条一行，带编号。不要解释。',
         'check': {'type': 'regex', 'pattern': r'^\s*\d+[.、)]', 'at_least': 10}},
    ],
}


def cmd_init(a):
    os.makedirs(SNAPS, exist_ok=True)
    if os.path.exists(TASKS) and not a.force:
        print('已经存在:', TASKS)
        print('要覆盖加 --force')
        return
    json.dump(SAMPLE, open(TASKS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('建好:', TASKS)
    print(f'里面 {len(SAMPLE["tasks"])} 道样例题。改成你自己的活再跑。')


def _run_task(t, model, provider, key, temp, repeat):
    got = []
    for i in range(repeat):
        r = call(t['prompt'], model, provider, key, temp)
        if r.get('err'):
            got.append({'ok': False, 'why': r['err'], 'chars': 0, 'out_tok': 0, 'ms': 0})
            continue
        ctype = (t.get('check') or {}).get('type', 'contains')
        fn = CHECKS.get(ctype)
        if not fn:
            got.append({'ok': False, 'why': f'不认识的检验: {ctype}',
                        'chars': r['chars'], 'out_tok': r['out_tok'], 'ms': r['ms']})
            continue
        ok, why = fn(r['text'], t['check'])
        got.append({'ok': ok, 'why': why, 'chars': r['chars'],
                    'out_tok': r['out_tok'], 'ms': r['ms']})
    return got


def cmd_run(a):
    if not os.path.exists(TASKS):
        print('没有题库。先跑: python analysis/watch.py init')
        return
    cfg = json.load(open(TASKS, encoding='utf-8'))
    model = a.model or cfg.get('model') or 'qwen-plus'
    provider = cfg.get('provider') or 'dashscope'
    temp = cfg.get('temperature', 1.0)
    repeat = a.repeat or cfg.get('repeat') or 3
    key = load_key(provider)

    print(f'模型 {model}   每題 {repeat} 次   共 {len(cfg["tasks"])} 题')
    print(f'备注 {a.note or "（无）"}\n')

    snap = {'time': datetime.now().isoformat(timespec='seconds'),
            'model': model, 'provider': provider, 'temperature': temp,
            'note': a.note or '', 'tasks': []}

    for t in cfg['tasks']:
        recs = _run_task(t, model, provider, key, temp, repeat)
        ok = sum(1 for x in recs if x['ok'])
        chars = [x['chars'] for x in recs if x['chars']]
        toks = [x['out_tok'] for x in recs if x['out_tok']]
        row = {
            'id': t['id'], 'n': len(recs), 'pass': ok,
            'chars_mean': round(sum(chars) / len(chars), 1) if chars else 0,
            'chars_min': min(chars) if chars else 0,
            'chars_max': max(chars) if chars else 0,
            'tok_mean': round(sum(toks) / len(toks), 1) if toks else 0,
            'why': next((x['why'] for x in recs if not x['ok'] and x['why']), ''),
        }
        snap['tasks'].append(row)
        flag = '✓' if ok == len(recs) else ('△' if ok else '✗')
        print(f'  {flag} {t["id"]:<10} {ok}/{len(recs)} 通过   '
              f'字数 {row["chars_min"]}-{row["chars_max"]} (均 {row["chars_mean"]})'
              + (f'   {row["why"]}' if row['why'] else ''))

    os.makedirs(SNAPS, exist_ok=True)
    name = snap['time'].replace(':', '').replace('-', '')[:15] + '.json'
    p = os.path.join(SNAPS, name)
    json.dump(snap, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'\n快照 → {p}')
    total = sum(r['pass'] for r in snap['tasks'])
    alln = sum(r['n'] for r in snap['tasks'])
    print(f'总计 {total}/{alln} 通过')


def _snaps():
    if not os.path.isdir(SNAPS):
        return []
    fs = sorted(x for x in os.listdir(SNAPS) if x.endswith('.json'))
    out = []
    for f in fs:
        try:
            out.append(json.load(open(os.path.join(SNAPS, f), encoding='utf-8')))
        except Exception:
            pass
    return out


def cmd_compare(a):
    snaps = _snaps()
    if len(snaps) < 2:
        print('至少要有两次快照才能比。现在', len(snaps), '次。')
        return
    prev, cur = snaps[-2], snaps[-1]
    print(f'上一次  {prev["time"]}  {prev.get("model","")}  {prev.get("note") or ""}')
    print(f'这一次  {cur["time"]}  {cur.get("model","")}  {cur.get("note") or ""}')
    if prev.get('model') != cur.get('model'):
        print(f'\n⚠ 两次用的不是同一个模型（{prev.get("model")} → {cur.get("model")}）')
        print('  下面的差异可能是换模型造成的，不是降级。')
    print()
    pm = {r['id']: r for r in prev['tasks']}
    cm = {r['id']: r for r in cur['tasks']}
    ids = [r['id'] for r in cur['tasks'] if r['id'] in pm]
    if not ids:
        print('两次的题不一样，没法比。')
        return

    print(f'{"题":<10}{"通过率":>12}{"字数":>18}{"判定":>10}')
    changed = []
    for i in ids:
        p, c = pm[i], cm[i]
        pr, cr = f'{p["pass"]}/{p["n"]}', f'{c["pass"]}/{c["n"]}'
        pchar, cchar = p['chars_mean'], c['chars_mean']
        # 判变规则：通过率掉了，或者字数变了 25% 以上
        verdict = '没变'
        if c['pass'] < p['pass']:
            verdict = '↓ 退化'
            changed.append((i, '通过率下降', f'{pr} → {cr}'))
        elif c['pass'] > p['pass']:
            verdict = '↑ 变好'
            changed.append((i, '通过率上升', f'{pr} → {cr}'))
        elif pchar and cchar and abs(cchar - pchar) / pchar > 0.25:
            verdict = '~ 长度变'
            changed.append((i, '字数变了 25% 以上', f'{pchar} → {cchar}'))
        print(f'{i:<10}{pr+">"+cr:>12}{pchar:>8.0f}→{cchar:<8.0f}{verdict:>10}')

    print()
    if changed:
        print('有变化的地方：')
        for i, what, detail in changed:
            print(f'  · {i}: {what}  ({detail})')
    else:
        print('这次和上次比，没有一项越过判定线。')


def cmd_list(a):
    snaps = _snaps()
    if not snaps:
        print('还没有快照。')
        return
    print(f'{"时间":<20}{"模型":<14}{"通过":>8}  备注')
    for s in snaps:
        tot = sum(r['pass'] for r in s['tasks'])
        alln = sum(r['n'] for r in s['tasks'])
        print(f'{s["time"]:<20}{s.get("model",""):<14}{tot:>4}/{alln:<3}  {s.get("note") or ""}')


def main():
    ap = argparse.ArgumentParser(add_help=True)
    sub = ap.add_subparsers(dest='cmd')

    p = sub.add_parser('init'); p.add_argument('--force', action='store_true'); p.set_defaults(fn=cmd_init)
    p = sub.add_parser('run')
    p.add_argument('--model'); p.add_argument('--repeat', type=int); p.add_argument('--note')
    p.set_defaults(fn=cmd_run)
    p = sub.add_parser('compare'); p.set_defaults(fn=cmd_compare)
    p = sub.add_parser('list'); p.set_defaults(fn=cmd_list)

    a = ap.parse_args()
    if not a.cmd:
        print(__doc__)
        return
    a.fn(a)


if __name__ == '__main__':
    main()
