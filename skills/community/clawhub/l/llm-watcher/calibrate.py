"""校 —— 给 llm-watcher 出一套真正能用的题

为什么要它：
  llm-watcher 最大的短板不是代码，是题。
  题太简单 → 两个模型都能过 → 测不出任何变化。
  题太难   → 基线就过不了 → 没法当基线。

  对的题：基线模型 3/3 通过，但稍微降级就掉一个。

  这个脚本干三件事：
    一、从题库池里跑一遍，记录每题通过几次
    二、删掉「不稳的」（不是 3/3 的）
    三、把剩下的写进 tasks.json，并给出每题的通过率和字数区间

用法：
    python analysis/calibrate.py --model qwen-plus --n 3
    python analysis/calibrate.py --model qwen-plus --n 3 --out out/watch/tasks.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics as st
import subprocess
import sys
import time
import urllib.error
import urllib.request

WS = r'C:\Users\0\Documents\deepseek-harness\default-workspace'
KEY = ("sk-ws-H.XMPEEEM.vGW6.MEQCIGuo3TOIG_-1Nv5_dw14M0zkh4vF7xPA48z5KcOV56ui"
       "AiBICyqC3stxzGszGSRBEP4GLUJuRgjlkSNgIu04Pt02NQ")
URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
PY = sys.executable

# ── 题库池：从易到难，覆盖不同能力面 ──
# 每题都带一个「不用模型判断」的验收器

POOL = [
    # ── 算术与精确输出 ──
    {"id": "arith1", "prompt": "13 乘以 17 等于多少？只输出数字。",
     "check": {"type": "contains", "any": ["221"]}},
    {"id": "arith2", "prompt": "计算 (27 + 38) × 4 - 100。只输出数字。",
     "check": {"type": "contains", "any": ["160"]}},
    {"id": "arith3", "prompt": "一个数除以 7 余 3，除以 5 余 2，最小正整数是多少？只输出数字。",
     "check": {"type": "contains", "any": ["17"]}},
    {"id": "percent", "prompt": "一件商品原价 240，先打八折，再降 15%，最终价格是多少？只输出数字。",
     "check": {"type": "contains", "any": ["163.2", "163"]}},

    # ── 代码：真跑测试 ──
    {"id": "fib", "prompt": "用 Python 写 fib(n)，返回第 n 个斐波那契数（fib(0)=0, fib(1)=1）。只输出代码。",
     "check": {"type": "python",
               "code": "assert fib(0)==0\nassert fib(1)==1\nassert fib(10)==55\nassert fib(20)==6765"}},
    {"id": "rev", "prompt": "用 Python 写 rev(s)，返回字符串倒序。只输出代码。",
     "check": {"type": "python",
               "code": "assert rev('abc')=='cba'\nassert rev('')==''\nassert rev('a')=='a'"}},
    {"id": "is_pal", "prompt": "用 Python 写 is_pal(s)，判断字符串是否回文（忽略大小写）。只输出代码。",
     "check": {"type": "python",
               "code": "assert is_pal('Aa')==True\nassert is_pal('ab')==False\nassert is_pal('A man')==False"}},
    {"id": "dedupe", "prompt": "用 Python 写 dedupe(xs)，去除重复且保持原顺序。只输出代码。",
     "check": {"type": "python",
               "code": "assert dedupe([1,2,1,3])==[1,2,3]\nassert dedupe([])==[]"}},

    # ── 结构化输出 ──
    {"id": "json1", "prompt": '输出 JSON：name="test", count=42, ok=true。只输出 JSON。',
     "check": {"type": "json", "expect": {"name": "test", "count": 42, "ok": True}}},
    {"id": "json2", "prompt": '输出 JSON 数组，含三个对象，每个有 id（1,2,3）和 tag（都等于 "x"）。只输出 JSON。',
     "check": {"type": "regex", "pattern": r'"id"\s*:\s*[123]', "at_least": 3}},

    # ── 结构化长输出 ──
    {"id": "list10", "prompt": "列出 10 个提高代码可读性的具体做法，每条一行，带编号。不要解释。",
     "check": {"type": "regex", "pattern": r"^\s*\d+[.、)]", "at_least": 10}},
    {"id": "steps5", "prompt": "用 5 个带编号的步骤说明「如何开始写一个 Python 函数」。每步一行，不要解释。",
     "check": {"type": "regex", "pattern": r"^\s*\d+[.、)]", "at_least": 5}},

    # ── 约束遵循 ──
    {"id": "limit", "prompt": "用不超过 8 个字回答：水的化学式是什么？只输出答案本身。",
     "check": {"type": "contains", "any": ["H2O", "H₂O"]}},
    {"id": "no_explain", "prompt": "只输出「是」或「否」：1 是质数吗？不要解释。",
     "check": {"type": "regex", "pattern": r"^(是|否)$", "at_least": 1}},
    {"id": "case", "prompt": "把「hello world」全部变成大写，只输出结果，不要解释。",
     "check": {"type": "exact", "value": "HELLO WORLD"}},

    # ── 翻译 / 改写（可判） ──
    {"id": "translate", "prompt": "把「谢谢」翻译成英文，只输出一个词。",
     "check": {"type": "contains", "any": ["thanks", "thank you", "Thanks"]}},
    {"id": "count_words", "prompt": "「今天天气很好」这句话有几个字？只输出数字。",
     "check": {"type": "contains", "any": ["6"]}},
]


def call(prompt, model, timeout=120):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "temperature": 1.0, "max_tokens": 1200}
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
        j = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"err": f"HTTP {e.code}"}
    except Exception as e:
        return {"err": type(e).__name__}
    msg = (j.get("choices") or [{}])[0].get("message") or {}
    return {"text": msg.get("content") or "", "chars": len(msg.get("content") or "")}


def _fence(t):
    m = re.search(r'```(?:\w+)?\s*(.*?)```', t, re.S)
    return m.group(1) if m else t


def verify(text, spec):
    t = spec.get("type", "contains")
    try:
        if t == "contains":
            low = text.lower()
            any_ = spec.get("any") or []
            all_ = spec.get("all") or []
            if any_ and not any(x.lower() in low for x in any_):
                return False
            if all_ and not all(x.lower() in low for x in all_):
                return False
            return True
        if t == "regex":
            return len(re.findall(spec.get("pattern", ""), text, re.M)) >= spec.get("at_least", 1)
        if t == "exact":
            return text.strip() == spec.get("value", "")
        if t == "json":
            s = _fence(text).strip()
            s = re.sub(r'^```(?:json)?\s*', '', s)
            s = re.sub(r'\s*```$', '', s)
            d = json.loads(s)
            return all(d.get(k) == v for k, v in (spec.get("expect") or {}).items())
        if t == "python":
            code = _fence(text)
            if "def " not in code:
                return False
            full = code + "\n\n" + spec.get("code", "") + '\nprint("__PASS__")\n'
            d = os.path.join(WS, ".tmp-cal")
            os.makedirs(d, exist_ok=True)
            p = os.path.join(d, f"t_{abs(hash(full)) % 99999}.py")
            try:
                open(p, "w", encoding="utf-8").write(full)
                r = subprocess.run([PY, p], capture_output=True, text=True, timeout=25)
                return "__PASS__" in r.stdout
            finally:
                try: os.unlink(p)
                except Exception: pass
    except Exception:
        return False
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='qwen-plus')
    ap.add_argument('--n', type=int, default=3)
    ap.add_argument('--out', default=os.path.join(WS, 'out', 'watch', 'tasks.json'))
    ap.add_argument('--pool-size', type=int, default=0, help='只用前 N 题（调试用）')
    a = ap.parse_args()

    pool = POOL[:a.pool_size] if a.pool_size else POOL
    print(f'模型 {a.model}   题库池 {len(pool)} 题   每題 {a.n} 次   '
          f'共 {len(pool) * a.n} 次调用\n')

    keep = []
    for i, task in enumerate(pool, 1):
        ok_n, chars = 0, []
        for _ in range(a.n):
            r = call(task['prompt'], a.model)
            if r.get('err'):
                continue
            if verify(r['text'], task['check']):
                ok_n += 1
            if r['chars']:
                chars.append(r['chars'])
            time.sleep(0.3)
        stable = ok_n == a.n
        flag = '✓ 留' if stable else '✗ 删'
        c = f'{min(chars)}-{max(chars)}' if chars else '-'
        print(f'  [{i:2d}/{len(pool)}] {flag}  {task["id"]:<12} {ok_n}/{a.n} 通过   字数 {c}')
        if stable and chars:
            keep.append({**task,
                         '_chars_min': min(chars), '_chars_max': max(chars),
                         '_chars_mean': round(st.mean(chars), 1)})

    print(f'\n留下 {len(keep)} 题 / 池 {len(pool)} 题')

    if not keep:
        print('一题都没留下。这不太正常——检查 API key 或模型名。')
        return

    out = {
        "model": a.model,
        "provider": "dashscope",
        "temperature": 1.0,
        "repeat": a.n,
        "_note": f"由 calibrate.py 自动生成于 {time.strftime('%Y-%m-%d %H:%M')}。"
                 f"只保留了 {a.n}/{a.n} 通过的题。_chars_* 字段是实测字数区间，可作基线参考。",
        "tasks": [{k: v for k, v in t.items() if not k.startswith('_')} for t in keep],
    }
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(out, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'写进 {a.out}')

    # 附一份参考表
    ref = os.path.join(os.path.dirname(a.out), 'baseline_chars.json')
    json.dump({t['id']: {'min': t['_chars_min'], 'max': t['_chars_max'],
                         'mean': t['_chars_mean']} for t in keep},
              open(ref, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'字数基线 {ref}')

    print('\n每题实测字数：')
    for t in keep:
        print(f'  {t["id"]:<12} {t["_chars_min"]:>4} - {t["_chars_max"]:>4}  (均 {t["_chars_mean"]})')


if __name__ == '__main__':
    main()
