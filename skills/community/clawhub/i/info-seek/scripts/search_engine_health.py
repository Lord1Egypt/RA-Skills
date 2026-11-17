#!/usr/bin/env python3
"""search_engine_health.py — 搜索链引擎健康探测（C1 · v1.0.1）

逐引擎探测可用性（免 key 引擎测 HTTP 连通；键控引擎测 key 存在性），
输出健康报告 → 指导配置 Exa/Tavily 等提升召回。

用法：
  python scripts/search_engine_health.py            # 全量探测
  python scripts/search_engine_health.py --timeout 5
"""
import argparse
import json
import os
import socket
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

KEY_ENVS = {
    'exa': 'EXA_API_KEY',
    'tavily': 'TAVILY_API_KEY',
    'tinyfish': 'TINYFISH_API_KEY',
    'zhipu': 'ZHIPU_API_KEY',
    'metaso': 'METASO_API_KEY',
}
# 免费/免 key 引擎（HTTP 连通性探测目标）
FREE_PROBES = {
    'bing_rss': ('https://www.bing.com/search?q=test&format=rss', 5),
    'duckduckgo': ('https://duckduckgo.com/html/?q=test', 5),
    'jina_reader': ('https://r.jina.ai/http://example.com', 8),
}


def probe_http(url: str, timeout: float) -> tuple:
    """返回 (ok, elapsed, err)——GA12 起委托 net_probe 唯一真源（同构签名，严格 200）。"""
    try:
        from net_probe import probe_http as _probe
    except Exception:
        from scripts.net_probe import probe_http as _probe  # type: ignore
    return _probe(url, timeout)


def main() -> int:
    ap = argparse.ArgumentParser(description='infoseek 搜索链引擎健康探测（C1）')
    ap.add_argument('--timeout', type=float, default=8.0, help='探测超时秒（默认 8）')
    ap.add_argument('--json', action='store_true', help='JSON 输出')
    args = ap.parse_args()

    report = {'generated_at': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()),
              'engines': {}}

    print('=== infoseek 搜索链引擎健康探测（v1.0.1 C1）===')
    # 1) 键控引擎：key 状态
    print('\n[键控引擎]（AI 层 · INFOSEEK_SEARCH_ENGINE=ai 启用）')
    for name, env in KEY_ENVS.items():
        has_key = bool(os.environ.get(env, ''))
        report['engines'][name] = {'type': 'keyed', 'key_configured': has_key,
                                   'hint': '' if has_key else f'set {env}'}
        mark = '✅ 已配置 key' if has_key else '❌ 未配置'
        print(f'  {name:10s} {mark}  (env={env})')

    # 2) 免 key 引擎：HTTP 连通
    print('\n[免费引擎]（默认层 · HTTP 连通探测）')
    for name, (url, to) in FREE_PROBES.items():
        ok, dt, err = probe_http(url, min(args.timeout, to))
        report['engines'][name] = {'type': 'free', 'reachable': ok, 'elapsed': dt,
                                   'error': err}
        mark = '✅ 可达' if ok else f'❌ {err}'
        print(f'  {name:12s} {mark}  ({dt}s)')

    # 3) 汇总建议
    keyed_ok = sum(1 for v in report['engines'].values() if v['type'] == 'keyed' and v['key_configured'])
    free_ok = sum(1 for v in report['engines'].values() if v['type'] == 'free' and v['reachable'])
    print(f'\n=== 汇总：键控 {keyed_ok}/{len(KEY_ENVS)} 已配置 · 免费 {free_ok}/{len(FREE_PROBES)} 可达 ===')
    if keyed_ok == 0 and free_ok == 0:
        print('⚠️  当前搜索链可能全部不可达 → 建议配置 Exa/Tavily key（见 references/configuration.md）')
    elif free_ok == 0:
        print('💡 免费引擎不可达（网络受限）→ 配置任一键控引擎可显著提升召回：')
        for name, env in KEY_ENVS.items():
            if not os.environ.get(env):
                print(f'     export {env}=<your-key>  # {name}')

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
