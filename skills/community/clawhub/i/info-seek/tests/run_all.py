#!/usr/bin/env python3
"""run_all.py — Infoseek 全量回归 runner（v1.8.1 新增）

固化回归口径，消除"声称 49 PASS / 1 SKIP 不可复现"（v1.7.8 审计 P1-2）：
- 统一发现：tests/test_*.py（排除本文件）
- 统一隔离：INFOSEEK_PLATFORM_WEBSEARCH=off 等 env 注入（防真实抓取）
- 统一超时：per-suite timeout（默认 120s），TIMEOUT 单独归类不混淆 FAIL
- 统一并发：--parallel N（默认 4）
- 统一产出：终端汇总表 + JSON 落盘（--json PATH）

用法：
    python3 tests/run_all.py                       # 全量，4 并发，120s/套件
    python3 tests/run_all.py --timeout 300         # 放宽超时
    python3 tests/run_all.py --parallel 1          # 串行（排查串扰）
    python3 tests/run_all.py --only v178 version   # 只跑名字含关键词的套件
    python3 tests/run_all.py --json /tmp/reg.json  # 落盘结果
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(ROOT, 'tests')

# 测试隔离 env：关闭真实联网抓取 / 固定数据目录，避免副作用与串扰
ISOLATE_ENV = {
    'INFOSEEK_PLATFORM_WEBSEARCH': 'off',
    'INFOSEEK_OFFLINE': '1',
    'PYTHONIOENCODING': 'utf-8',
}


# 已知慢套件（性能/压力）：给足超时使其暴露真实结论，而非零输出 TIMEOUT。
# v1.8.2 P1：test_deep_v101 的 S 压力段已拆出至 test_perf_v101（与功能回归解耦）。
# test_perf_v101 含 1000-3000 源评分/research 大批量断言；LRU 缓存优化后实测
# S1 4.8s / S2 59.3s / S4 90.5s（research 全链路），整链 ~170s，给 300s 超时。
SLOW_SUITES = {
    'test_perf_v101.py': 300,
}

# 已知问题套件：单列 KNOWN 归类（不计入 FAIL，也不计入绿基线），必须附归因。
# 新增条目须写明：现象 + 根因 + 是否本次引入 + 追踪出处（ROADMAP 章节）。
# v1.8.2 P1：test_deep_v101 性能挂点已闭合——LRU 缓存根治 S1（38→4.8s），S 段拆出
# test_perf_v101 独立观测（阈值按优化后实测校准），功能回归 B+C 全绿，KNOWN 清空。
KNOWN_ISSUES = {}


def timeout_for(name, default):
    return max(default, SLOW_SUITES.get(name, 0))


def discover(only=None):
    files = sorted(
        f for f in os.listdir(TESTS)
        if f.startswith('test_') and f.endswith('.py')
    )
    if only:
        files = [f for f in files if any(k in f for k in only)]
    return files


_NUM_FIRST = r'(\d+)\s*(?:{k})'          # 'N PASS' / '33 passed'
_KEY_FIRST = r'(?:{k})\s*[=:：]\s*(\d+)'  # 'PASS=N' / 'PASS: N'

# 自报格式别名：各套件历史遗留三种写法（大写 PASS / 小写 passed / SKIP 计数）
_KEY_ALIAS = {
    'PASS': r'PASS|passed',
    'FAIL': r'FAIL|failed',
    'SKIP': r'SKIP|skipped',
}


def _pick(line, key):
    """同一行内取计数，兼容 'N PASS' 与 'PASS=N' 两种自报格式。

    KEY_FIRST 必须优先：对 'PASS=46 FAIL=0'，NUM_FIRST 的 (\\d+)\\s*FAIL 会误吃
    "46 FAIL" 使 fail 串位为 46；先匹配 'FAIL=0' 可避免。
    """
    k = _KEY_ALIAS[key]
    m = re.search(_KEY_FIRST.format(k=k), line) or re.search(_NUM_FIRST.format(k=k), line)
    return int(m.group(1)) if m else None


def parse_counts(out):
    """从套件输出解析自报计数（解析不到返回 None）。

    v1.8.1 修复：原实现只认 'N PASS' 且全文扫描，对 'PASS=46 FAIL=0' 格式
    会误解析（曾把 test_g5_budget 显示成 0P/46F）。改为逐行解析 + 双格式兼容，
    且只采信含 PASS/FAIL 关键字的行（避免 engine-stats 日志中 fail=0 干扰）。
    注意：套件 PASS/FAIL 判定始终以退出码为准，本计数仅为辅助展示。
    """
    p = f = s = None
    for line in out.splitlines():
        up = line.upper()
        if 'PASS' not in up and 'FAIL' not in up:
            continue
        vp, vf, vs = _pick(line, 'PASS'), _pick(line, 'FAIL'), _pick(line, 'SKIP')
        if vp is not None:
            p = vp
        if vf is not None:
            f = vf
        if vs is not None:
            s = vs
    if p is None and f is None:
        return None
    return {'pass': p or 0, 'fail': f or 0, 'skip': s or 0}


def run_one(name, timeout):
    path = os.path.join(TESTS, name)
    env = dict(os.environ)
    env.update(ISOLATE_ENV)
    t0 = time.time()
    try:
        r = subprocess.run(
            [sys.executable, path],
            cwd=ROOT, env=env, timeout=timeout,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        out = (r.stdout or b'').decode('utf-8', 'replace')
        rc = r.returncode
        status = 'PASS' if rc == 0 else 'FAIL'
    except subprocess.TimeoutExpired as e:
        _raw = e.stdout or b''
        out = _raw.decode('utf-8', 'replace') if isinstance(_raw, bytes) else str(_raw)
        rc, status = 124, 'TIMEOUT'
    dt = time.time() - t0
    # SKIP 归类（v1.8.1 严格化）：仅两条硬判据，避免子项 SKIP 字样误升为套件级
    #   a) 有自报计数且 pass==0（环境缺失全跳过）
    #   b) 无计数但存在行首显式 SKIP/SKIPPED/⏭ 标记
    # 反例（已修）：test_qveris_bridge_v130 输出 '33 passed, 0 failed' 且含子项
    #   'QVeris 被标记配额禁用' 字样，旧逻辑因 counts=None + 全文匹配 '跳过' 误判 SKIP。
    counts = parse_counts(out)
    if status == 'PASS':
        if counts and counts['pass'] == 0:
            status = 'SKIP'
        elif not counts and re.search(r'^\s*(SKIP|SKIPPED|⏭)', out, re.M):
            status = 'SKIP'
    if status in ('FAIL', 'TIMEOUT') and name in KNOWN_ISSUES:
        status = 'KNOWN'
    tail = '\n'.join([l for l in out.strip().splitlines() if l.strip()][-3:])
    return {'suite': name, 'status': status, 'rc': rc, 'sec': round(dt, 1),
            'counts': counts, 'tail': tail,
            'known_reason': KNOWN_ISSUES.get(name) if status == 'KNOWN' else None}


def main():
    ap = argparse.ArgumentParser(description='Infoseek 全量回归 runner')
    ap.add_argument('--parallel', type=int, default=4)
    ap.add_argument('--timeout', type=int, default=120)
    ap.add_argument('--only', nargs='*', default=None)
    ap.add_argument('--json', default=None)
    a = ap.parse_args()

    suites = discover(a.only)
    print(f'发现 {len(suites)} 套件 | 并发 {a.parallel} | 单套件超时 {a.timeout}s')
    print('=' * 72)
    t0 = time.time()
    results = []
    icons = {'PASS': '✅', 'SKIP': '⏭', 'FAIL': '❌', 'TIMEOUT': '⏱', 'KNOWN': '🟡'}
    with ThreadPoolExecutor(max_workers=a.parallel) as ex:
        futs = [ex.submit(run_one, n, timeout_for(n, a.timeout)) for n in suites]
        for i, fu in enumerate(as_completed(futs), 1):
            r = fu.result()
            results.append(r)
            print(f"[{i}/{len(suites)}] {icons[r['status']]} {r['status']:<7} "
                  f"{r['suite']:<44} {r['sec']:>6.1f}s rc={r['rc']}", flush=True)
    total = time.time() - t0

    results.sort(key=lambda r: (r['status'] == 'PASS', r['suite']))
    npass = sum(1 for r in results if r['status'] == 'PASS')
    nskip = sum(1 for r in results if r['status'] == 'SKIP')
    nfail = sum(1 for r in results if r['status'] == 'FAIL')
    nto = sum(1 for r in results if r['status'] == 'TIMEOUT')
    nknown = sum(1 for r in results if r['status'] == 'KNOWN')

    for r in results:
        icon = {'PASS': '✅', 'SKIP': '⏭', 'FAIL': '❌',
                'TIMEOUT': '⏱', 'KNOWN': '🟡'}[r['status']]
        c = r['counts']
        cs = f" ({c['pass']}P/{c['fail']}F/{c['skip']}S)" if c else ''
        print(f"{icon} {r['status']:<7} {r['suite']:<46} {r['sec']:>6.1f}s rc={r['rc']}{cs}")

    print('=' * 72)
    print(f'汇总: {npass} PASS / {nskip} SKIP / {nfail} FAIL / {nto} TIMEOUT '
          f'/ {nknown} KNOWN（共 {len(results)} 套件，耗时 {total:.1f}s）')
    green = (nfail == 0 and nto == 0)
    print(f'绿基线: {"✅ 达成（0 FAIL / 0 TIMEOUT）" if green else "❌ 未达成"}'
          + (f' ｜ 已知问题 {nknown} 项（见下）' if nknown else ''))

    if nfail or nto or nknown:
        print('\n--- 非 PASS 套件详情 ---')
        for r in results:
            if r['status'] in ('FAIL', 'TIMEOUT', 'KNOWN'):
                print(f"\n[{r['status']}] {r['suite']} (rc={r['rc']}, {r['sec']}s)")
                if r.get('known_reason'):
                    print(f'  归因: {r["known_reason"]}')
                if r['tail']:
                    print(f'  尾部: {r["tail"]}')

    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump({'version': '1.8.3', 'total_sec': round(total, 1),
                       'summary': {'pass': npass, 'skip': nskip, 'fail': nfail,
                                   'timeout': nto, 'known': nknown,
                                   'green_baseline': green,
                                   'suites': len(results)},
                       'results': results}, fh, ensure_ascii=False, indent=2)
        print(f'\n结果已落盘: {a.json}')

    sys.exit(1 if (nfail or nto) else 0)


if __name__ == '__main__':
    main()
