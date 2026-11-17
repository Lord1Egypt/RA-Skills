#!/usr/bin/env python3
"""Infoseek v1.0.1 MCP 行为快照测试（G11 前置）

目的：为 mcp_server 关键路径建立行为快照，作为后续模块拆分（G11）的回归基线。
覆盖：
- tools/list：18 规范工具 + 12 废弃（名称集合快照）
- tools/call：核心工具调用行为（score_source / conflict_detection / summarize / manage_keys）
- 协议层：initialize / 未知工具错误码
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

import infoseek_mcp_server as m

passed, failed = [], []

def check(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  [PASS] {name} {extra}")
    else:
        failed.append(name); print(f"  [FAIL] {name} {extra}")



def _unwrap(r):
    """解包 MCP content 包装 → 实际 dict"""
    res = r.get('result', {}) if isinstance(r, dict) else {}
    content = res.get('content', [])
    if content and isinstance(content[0], dict):
        text = content[0].get('text', '')
        try:
            return json.loads(text)
        except Exception:
            return {'raw': text}
    return res

# ── SN1: tools/list 快照（规范工具名集合）──
CANONICAL_EXPECTED = {
    'research_v3', 'research_stream',
    'search_anchors_async', 'fetch_content_async', 'save_archive_async',
    'check_dedup_async', 'dedup_stats_async', 'fuse_analysis_async',
    'cross_subject_analysis_async', 'summarize_content_async',
    'conflict_detection_async', 'score_source_async', 'score_contradiction_async',
    'manage_keys', 'key_usage',
    'qcm_query',  # v1.0.1: QCM 反向协同（V8.4）
    'identity_attribution',  # v1.5.0: 身份归因（T2/G2）
    'account_forensics',  # v1.6.0 融入: 账号取证（B1）
}
names = {t['name'] for t in m.TOOLS}
check('SN1 规范工具名集合', names == CANONICAL_EXPECTED,
      f"缺={sorted(CANONICAL_EXPECTED - names)} 多={sorted(names - CANONICAL_EXPECTED)}")

# ── SN2: 废弃工具快照（12 个 sync + research）──
DEP_EXPECTED = {
    'search_anchors', 'fetch_content', 'save_archive', 'check_dedup',
    'dedup_stats', 'fuse_analysis', 'cross_subject_analysis',
    'summarize_content', 'conflict_detection', 'score_source',
    'score_contradiction', 'research',
}
dep_names = {t['name'] for t in m.DEPRECATED_TOOLS}
check('SN2 废弃工具名集合', dep_names == DEP_EXPECTED,
      f"缺={sorted(DEP_EXPECTED - dep_names)} 多={sorted(dep_names - DEP_EXPECTED)}")

# ── SN3: 每个规范工具都有 inputSchema ──
check('SN3 规范工具 schema 完整',
      all('inputSchema' in t and 'type' in t['inputSchema'] for t in m.TOOLS))

# ── SN4: 每个 async 工具 schema 与 sync 等价（字段描述完整，G12 快照）──
sync_map = {t['name']: t for t in m.DEPRECATED_TOOLS}
async_ok = True
for t in m.TOOLS:
    if t['name'].endswith('_async'):
        sync_name = t['name'][:-6]  # 去 _async 后缀
        sync_t = sync_map.get(sync_name)
        if sync_t:
            a_props = t['inputSchema'].get('properties', {})
            s_props = sync_t['inputSchema'].get('properties', {})
            # async 应包含 sync 的全部字段（且字段有 description）
            missing = set(s_props) - set(a_props)
            no_desc = [k for k in a_props if k in s_props and 'description' in s_props[k]
                       and 'description' not in a_props[k]]
            if missing or no_desc:
                async_ok = False
                print(f"    [diff] {t['name']} 缺字段={missing} 缺描述={no_desc[:2]}")
check('SN4 async schema 与 sync 对齐', async_ok)

# ── SN5: handle_tools_call score_source 行为快照 ──
r = m.handle_tools_call(1, {'name': 'score_source',
                            'arguments': {'subject': 'DeepSeek',
                                          'source': {'title': 'DeepSeek 开源', 'url': 'https://x.com'}}})
result = r.get('result', {})
check('SN5 score_source 调用', 'final_score' in result or 'scored' in result or
      isinstance(result, dict) and len(result) > 0, f"keys={list(result.keys())[:4]}")

# ── SN6: 废弃工具调用附 deprecated 标记 ──
r6 = m.handle_tools_call(2, {'name': 'score_source'})
result6 = r6.get('result', {})
check('SN6 废弃标记', isinstance(result6, dict) and result6.get('deprecated') is not None or
      'deprecated' in str(result6)[:200], f"deprecated={result6.get('deprecated') if isinstance(result6, dict) else '?'}")

# ── SN7: manage_keys 行为快照 ──
r7 = m.handle_tools_call(3, {'name': 'manage_keys', 'arguments': {'action': 'list'}})
result7 = _unwrap(r7)
check('SN7 manage_keys list', isinstance(result7, dict) and 'masked' in result7,
      f"keys={list(result7.keys())[:4]}")

# ── SN8: 未知工具返回错误码 -32601 ──
r8 = m.handle_tools_call(4, {'name': 'nonexistent_tool', 'arguments': {}})
err = r8.get('error', {})
check('SN8 未知工具错误码', err.get('code') == -32601, f"code={err.get('code')}")

# ── SN9: initialize 协议快照 ──
r9 = m.handle_initialize(0, {})
check('SN9 initialize 协议', r9.get('result', {}).get('protocolVersion') == '2024-11-05' or
      'protocolVersion' in str(r9)[:200], f"keys={list(r9.get('result', {}).keys())[:3] if isinstance(r9.get('result'), dict) else '?'}")

# ── SN10: 工具分发 deprecated 迁移（sync → async 转发标记）──
r10 = m.handle_tools_call(5, {'name': 'search_anchors', 'arguments': {'subject': '测试'}})
result10 = _unwrap(r10)
migrated = result10.get('migrate_to') if isinstance(result10, dict) else None
check('SN10 sync 转发 migrate_to', migrated == 'search_anchors_async',
      f"migrate_to={migrated}")

print(f"\n=== MCP 快照测试: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL PASS")
