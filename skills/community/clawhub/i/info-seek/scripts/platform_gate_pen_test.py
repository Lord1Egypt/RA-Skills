#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
platform_gate_pen_test.py — P0 平台 Web 搜索适配器 · 网关实测（真实协议链路）
--------------------------------------------------------------------------------
实测对象：scripts/platform_adapter.py（P0 平台 Web 搜索适配器）
被测链路：platform_adapter → workbuddy_channel（宿主注入通道，MCP JSON-RPC stdio）
          → wb_gateway_sidecar（WorkBuddy MCP Gateway 仿真，7 个 wb_* 工具）
          → cn.bing.com（真实网页搜索后端）

覆盖（G0-G5）：
  G0 基建     sidecar spawn / MCP 握手 / tools/list 7 工具 / wb_init 能力集
  G1 探测注册  无通道零开销 / wb 模式注册 / 幂等缓存 / off 显式关闭
  G2 真实查询  adapter fn 真实搜索 3 主题 → 归一化 {url,title,snippet} / 截断
  G3 生命周期  连续成功清计数 / kill sidecar 故障注入 → 连续 3 败禁用 → 重启恢复
  G4 锚点      _ENGINE_WEIGHT 接入 / env 权重覆盖 / _default_layer 合并注册
  G5 并发融合  _parallel_merge（并发内核+生命周期包装）/ search_web 全流程

用法：python platform_gate_pen_test.py [--report /sandbox/workspace/wb_gate_pentest/report.md]
退出码：0=全过，1=有失败。

运行说明：量级 ~30-60s（含真实网络搜索 3 主题 + 2 次全流程 + 故障窗口）。
"""

import argparse
import json
import os
import signal
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

import platform_adapter as pa          # noqa: E402
import workbuddy_channel as wbc        # noqa: E402
import engine_lifecycle as EL          # noqa: E402
import infoseek_pipeline as P          # noqa: E402

_START = time.time()
_PASS = 0
_FAIL = 0
_GROUP = ''


def group(name: str):
    global _GROUP
    _GROUP = name
    print(f'\n═══ {name} ═══')


def check(label: str, cond: bool, extra: str = '') -> None:
    global _PASS, _FAIL
    if cond:
        _PASS += 1
        print(f'  ✅ {label}')
    else:
        _FAIL += 1
        print(f'  ❌ {label} {extra}')


def _reset(env_keep: dict | None = None):
    """重置 adapter 探测缓存 + env + lifecycle（进程内隔离）。"""
    pa._ENGINE_PROBED = False
    pa._ENGINE_CACHE = None
    for k in (pa.MODE_ENV, pa.CHANNEL_ENV, pa.MCP_CHANNEL_ENV,
              pa.IMA_CHANNEL_ENV, pa.TIMEOUT_ENV, pa.WEIGHT_ENV,
              pa.THROTTLE_ENV):
        os.environ.pop(k, None)
    EL.get_lifecycle().reset()
    if env_keep:
        os.environ.update(env_keep)


def _gateway_alive() -> bool:
    """进程存活判断（用 proc.poll()：zombie 经 waitpid(WNOHANG) 回收后
    返回 returncode → 判定已退出；避免 os.kill(pid,0) 对 zombie 误判）。"""
    try:
        g = wbc._get_gateway()
        proc = getattr(getattr(g, '_client', None), 'proc', None)
        if proc is None:
            return False
        if proc.poll() is not None:
            return False
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# G0 基建：sidecar + MCP 协议
# ---------------------------------------------------------------------------

def g0():
    group('G0 基建 · WorkBuddy MCP Gateway sidecar 协议')
    check('channel health()=True（spawn+MCP 握手+wb_init+wb_status）',
          wbc.health())
    pid = wbc.gateway_pid()
    check('sidecar 进程在跑', bool(pid) and _gateway_alive(), f'pid={pid}')
    g = wbc._get_gateway()
    # 直连网关验证协议面（tools/list 工具面 + 会话能力）
    r = g._client._call('tools/list', {})
    names = {t.get('name') for t in (r.get('tools') or [])}
    expect = {'wb_init', 'wb_search', 'wb_run', 'wb_advance',
              'wb_step_result', 'wb_status', 'wb_capability_result'}
    check('tools/list 工具面 = 官方实证 7 个 wb_*',
          expect.issubset(names), f'缺 {expect - names}')
    init = g._tool_result('wb_init', {'client_version': 'pen-test'})
    check('wb_init → session_id + capabilities',
          bool(init.get('session_id'))
          and 'web_search' in (init.get('capabilities') or []),
          json.dumps(init, ensure_ascii=False)[:120])
    caps = g._tool_result('wb_capability_result', {'capability': 'web_search'})
    check('wb_capability_result → web_search schema',
          bool(caps.get('ok')) and caps.get('capability') == 'web_search')
    health = g._tool_result('wb_status', {})
    check('wb_status → ready', bool(health.get('ok'))
          and health.get('status') == 'ready')


# ---------------------------------------------------------------------------
# G1 探测注册（adapter 契约）
# ---------------------------------------------------------------------------

def g1():
    group('G1 探测注册 · platform_adapter 契约')
    _reset()
    check('auto 缺省：平台预装约定模块 → 探测即注册（缺省启用）',
          len(pa.platform_engines()) == 1
          and pa.platform_engines()[0][0] == 'WorkBuddy-WebSearch')

    _reset({pa.CHANNEL_ENV: 'no_such_channel_module_xyz'})
    check('通道导入失败 → 探测降级 → 零注册（零网络开销）',
          pa.platform_engines() == [])

    _reset({pa.MODE_ENV: 'wb', pa.CHANNEL_ENV: 'workbuddy_channel'})
    engs = pa.platform_engines()
    check('wb 模式 → 注册 WorkBuddy-WebSearch',
          len(engs) == 1 and engs[0][0] == 'WorkBuddy-WebSearch',
          str(engs))
    check('注册后立即可用', callable(engs[0][1]))

    _reset({pa.MODE_ENV: 'off', pa.CHANNEL_ENV: 'workbuddy_channel'})
    check('off 显式关闭 → 不注册',
          pa.platform_engines() == [])

    # 幂等：单进程内探测仅一次（重复调用不重复 spawn）
    _reset({pa.MODE_ENV: 'wb', pa.CHANNEL_ENV: 'workbuddy_channel'})
    pid_a = wbc.gateway_pid()
    pa.platform_engines()
    pa.platform_engines()
    pid_b = wbc.gateway_pid()
    check('探测幂等：重复调用不重建网关', pid_a == pid_b,
          f'pid {pid_a} → {pid_b}')


# ---------------------------------------------------------------------------
# G2 真实查询链路
# ---------------------------------------------------------------------------

def g2():
    group('G2 真实查询 · adapter → 通道 → 网关 → Bing 真搜')
    _reset({pa.MODE_ENV: 'wb', pa.CHANNEL_ENV: 'workbuddy_channel'})
    fn = pa.platform_engine()[1]
    queries = ['美国 CPI 最新数据', 'python 量化交易 入门',
               'WorkBuddy MCP gateway']
    for q in queries:
        try:
            res = fn(q, 5)
        except Exception as e:
            check(f'查询 {q!r} → 异常: {e}', False)
            continue
        ok = (isinstance(res, list) and 1 <= len(res) <= 5
              and all(r.get('url', '').startswith('http') for r in res)
              and all('title' in r and 'snippet' in r for r in res))
        check(f'查询 {q!r} → {len(res)} 条，字段全、url 合法',
              ok, str(res)[:140])
        for r in res[:2]:
            print(f'      · {r["title"][:50]} | {r["url"][:60]}')

    # max_results 截断 + 去重
    res10 = fn('python', 2)
    check('max_results=2 → ≤2 条', len(res10) <= 2)
    d = fn('CPI 数据', 8)
    urls = [r['url'] for r in d]
    check('同查询批量结果 url 不重复', len(urls) == len(set(urls)))


# ---------------------------------------------------------------------------
# G3 健康生命周期（故障注入 + 恢复）
# ---------------------------------------------------------------------------

def g3():
    group('G3 健康生命周期 · 故障注入与恢复')
    _reset({pa.MODE_ENV: 'wb', pa.CHANNEL_ENV: 'workbuddy_channel'})
    name, fn = pa.platform_engine()
    lc = EL.get_lifecycle()

    # 连续成功 → 清计数、不禁用
    ok_calls = 0
    for _ in range(3):
        if P._call_engine(name, fn, 'python', 3):
            ok_calls += 1
    st = lc.status().get(name, {})
    check('连续成功调用 ≥1 次真实返回',
          ok_calls >= 1, f'ok={ok_calls}')
    check('成功 → fail_count 0 且不禁用',
          st.get('fail_count', 0) == 0 and not lc.is_disabled(name),
          json.dumps({k: st.get(k) for k in ('fail_count', 'total_calls')}))

    # 故障注入：kill sidecar（BrokenPipe/超时 → record_failure 分类）
    pid = wbc.gateway_pid()
    os.kill(pid, signal.SIGKILL)
    time.sleep(0.5)
    check('sidecar 已 kill（进程消失）', not _gateway_alive(), f'pid={pid}')

    fails = 0
    for _ in range(_FAIL_THRESHOLD + 1):
        if not P._call_engine(name, fn, 'python', 3):
            fails += 1
    st = lc.status().get(name, {})
    check(f'kill 后 {_FAIL_THRESHOLD}+ 次调用全部失败（返回 []）',
          fails >= _FAIL_THRESHOLD, f'fails={fails}')
    check(f'连续失败 ≥{_FAIL_THRESHOLD} → is_disabled=True',
          lc.is_disabled(name),
          f"fail_count={st.get('fail_count')} "
          f"last_error={st.get('last_error')}")
    r = P._call_engine(name, fn, 'python', 3)
    check('禁用后 _call_engine 直接跳过（[] 零网络开销）', r == [])

    # 恢复：重启 sidecar + lifecycle reset（等价手动恢复，非自动恢复）
    wbc.reset_gateway()
    lc.reset(name)
    check('重启 sidecar → 网关再健康', wbc.health())
    ok = False
    for _ in range(3):  # 重启后首调用可能仍踩上次残留，允许重试
        if P._call_engine(name, fn, 'python', 3):
            ok = True
            break
        time.sleep(1)
    check('恢复后 _call_engine 重新出结果', ok)


# ---------------------------------------------------------------------------
# G4 pipeline 锚点
# ---------------------------------------------------------------------------

def g4():
    group('G4 锚点 · 权重表 / 默认层 / 路由放行')
    _reset({pa.MODE_ENV: 'wb', pa.CHANNEL_ENV: 'workbuddy_channel'})

    check('默认权重 platform_weight()=0.9', pa.platform_weight() == 0.9)
    check("_ENGINE_WEIGHT['WorkBuddy-WebSearch'] 已接入（非硬编码默认）",
          abs(P._ENGINE_WEIGHT['WorkBuddy-WebSearch'] - 0.9) < 1e-9)
    os.environ[pa.WEIGHT_ENV] = '0.55'
    check('env 覆盖权重 0.55 生效（动态读取非硬编码）',
          abs(pa.platform_weight() - 0.55) < 1e-9)
    os.environ.pop(pa.WEIGHT_ENV, None)

    layer = P._default_layer()
    names = [n for n, _ in layer]
    check('_default_layer() 含 WorkBuddy-WebSearch（并发内核注册）',
          any('WorkBuddy' in n for n in names), str(names))
    import engine_router as ER
    # 默认（探测关闭）：route_engines 只做白名单/键控过滤 → 平台引擎恒放行且保序
    in_eng = [('DuckDuckGo-HTML', None), ('Bing-RSS', None),
              ('WorkBuddy-WebSearch', None)]
    out_names = [n for n, _ in ER.route_engines(in_eng)]
    check('route_engines 默认保序放行：平台引擎位置不变（过滤不改序）',
          out_names == ['DuckDuckGo-HTML', 'Bing-RSS',
                        'WorkBuddy-WebSearch'], f'out={out_names}')
    # 探测开启：平台引擎无探测 URL → _probe_free 恒 True（不被免费引擎探测误杀）
    os.environ['INFOSEEK_ENGINE_PROBE'] = '1'
    check('探测开启时平台引擎恒放行（探测表无其 URL）',
          ER._probe_free('WorkBuddy-WebSearch') is True)
    os.environ.pop('INFOSEEK_ENGINE_PROBE', None)


# ---------------------------------------------------------------------------
# G5 并发融合
# ---------------------------------------------------------------------------

def g5():
    group('G5 并发融合 · 引擎池真实并行 + 全流程')
    _reset({pa.MODE_ENV: 'wb', pa.CHANNEL_ENV: 'workbuddy_channel'})
    name, fn = pa.platform_engine()

    # 并发内核 + 生命周期包装（单引擎走 _parallel_merge）
    t0 = time.time()
    res = P._parallel_merge([(name, fn)], '核聚变 可控 最新进展', 5)
    dt = time.time() - t0
    ok = (isinstance(res, list) and len(res) >= 1
          and all(r.get('url', '').startswith('http') for r in res))
    check(f'_parallel_merge 单平台引擎 → {len(res)} 条，字段全',
          ok, str(res)[:140])
    check(f'_parallel_merge 耗时 {dt:.1f}s（≤ 窗口 8s）', dt <= 8.0)

    # 全流程 search_web：平台引擎参与默认层，结果进入 _filter_relevant 融合
    t0 = time.time()
    got = P.search_web('什么是归零思维', 6)
    dt = time.time() - t0
    print(f'      search_web 全流程 → {len(got)} 条，耗时 {dt:.1f}s')
    print(f'      结果样例: {[r["title"][:30] for r in got[:3]]}')
    check('search_web 全链路返回非空（默认层融合含平台引擎贡献）',
          len(got) >= 1, '全链失败（DDG 等沙箱不可达时平台引擎为兜底）')


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', default='',
                    help='报告输出路径（markdown）')
    args = ap.parse_args()

    # 暂存原始 lifecycle 状态文件路径（用临时目录隔离，避免污染真实状态）
    os.environ.setdefault('INFOSEEK_DATA_DIR',
                          tempfile.mkdtemp(prefix='wbgate_'))

    for grp in (g0, g1, g2, g3, g4, g5):
        try:
            grp()
        except Exception as e:
            group(grp.__name__)
            check(f'{grp.__name__} 组异常终止', False, str(e))

    dt = time.time() - _START
    print(f'\n════ 实测结果 {_PASS} 过 / {_FAIL} 败 · 耗时 {dt:.1f}s ════')

    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        lines = [
            f'# P0 网关实测报告（platform_gate_pen_test）',
            f'- 时间: {time.strftime("%Y-%m-%d %H:%M:%S")}',
            f'- 结果: **{_PASS} 过 / {_FAIL} 败**（耗时 {dt:.1f}s）',
            f'- 链路: platform_adapter → workbuddy_channel(MCP stdio) '
            f'→ wb_gateway_sidecar → cn.bing.com',
            f'- 引擎名: WorkBuddy-WebSearch，权重默认 0.9（env 可覆盖）',
            f'- 故障注入: SIGKILL sidecar → 连续 {_FAIL_THRESHOLD} 败禁用 '
            f'→ reset 恢复',
            f'- 占位说明: G3 使用 INFOSEEK_DATA_DIR 隔离；'
            f'G3 连续成功需 ≥1 次真实返回（Bing 偶发反爬重试计入）',
        ]
        Path(args.report).write_text('\n'.join(lines) + '\n',
                                     encoding='utf-8')
        print(f'报告已写: {args.report}')

    raise SystemExit(1 if _FAIL else 0)


_FAIL_THRESHOLD = int(os.environ.get('INFOSEEK_ENGINE_FAIL_THRESHOLD', '3'))


if __name__ == '__main__':
    main()