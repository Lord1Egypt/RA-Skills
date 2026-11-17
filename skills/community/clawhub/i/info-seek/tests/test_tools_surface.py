#!/usr/bin/env python3
"""Infoseek v1.0.0 工具面收敛测试（25 → 13）

验证：
  - TOOLS 暴露 18 个规范工具（11 async + research_v3 + research_stream + Key 管理 2 + QCM 协同 1 + 身份归因 1 + 账号取证 1）
  - DEPRECATED_TOOLS = 12（sync + research），含 deprecated / migrate_to 标记
  - tools/call 调用废弃名仍响应，结果附 deprecated 标记（并存期行为）
  - 未知工具返回 Tool not found
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

import infoseek_mcp_server as mcp

CANONICAL = {
    'search_anchors_async', 'fetch_content_async', 'save_archive_async',
    'check_dedup_async', 'dedup_stats_async', 'fuse_analysis_async',
    'cross_subject_analysis_async', 'summarize_content_async',
    'conflict_detection_async', 'score_source_async',
    'score_contradiction_async', 'research_v3', 'research_stream',
    'manage_keys', 'key_usage',  # v1.0.1: Key 管理工具
    'qcm_query',  # v1.0.1: QCM 反向协同工具（V8.4）
    'identity_attribution',  # v1.5.0: 身份归因（T2/G2）
    'account_forensics',  # v1.6.0 融入: 账号取证（B1）
}
DEPRECATED = {
    'search_anchors', 'fetch_content', 'save_archive', 'check_dedup',
    'dedup_stats', 'fuse_analysis', 'cross_subject_analysis',
    'summarize_content', 'conflict_detection', 'score_source',
    'score_contradiction', 'research',
}

passed, failed = 0, 0


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print(f"  [PASS] {name} {detail}")
    else:
        failed += 1
        print(f"  [FAIL] {name} {detail}")


print("=" * 70)
print("v1.0.0 工具面收敛测试")
print("=" * 70)

# 1. 暴露面
names = {t['name'] for t in mcp.TOOLS}
check("TOOLS 暴露 18 个规范工具（13 + Key 管理 2 + QCM 协同 1 + 身份归因 1 + 账号取证 1）", len(mcp.TOOLS) == 18,
      f"len={len(mcp.TOOLS)}")
check("规范工具名集一致", names == CANONICAL,
      f"缺={sorted(CANONICAL - names)} 多={sorted(names - CANONICAL)}")

# 2. 废弃集
dep_names = {t['name'] for t in mcp.DEPRECATED_TOOLS}
check("DEPRECATED_TOOLS = 12", len(mcp.DEPRECATED_TOOLS) == 12,
      f"len={len(mcp.DEPRECATED_TOOLS)}")
check("废弃工具名集一致", dep_names == DEPRECATED,
      f"缺={sorted(DEPRECATED - dep_names)} 多={sorted(dep_names - DEPRECATED)}")
check("废弃集含迁移标记", all(t.get('deprecated') and t.get('migrate_to')
                            for t in mcp.DEPRECATED_TOOLS))
check("迁移映射 research→research_v3",
      mcp._DEPRECATED_MIGRATION['research'] == 'research_v3')

# 3. 废弃名调用仍响应 + 标记（本地工具 summarize_content）
r = mcp.handle_tools_call(1, {"name": "summarize_content",
                              "arguments": {"text": "人工智能大模型技术正在快速发展，大模型推动了生成式人工智能的应用。",
                                            "max_words": 50}})
if r.get('result'):
    payload = json.loads(r['result']['content'][0]['text'])
    check("废弃名调用仍响应", r['result'] is not None)
    check("结果附 deprecated 标记", payload.get('deprecated') is True,
          f"keys={list(payload.keys())[:6]}")
    check("迁移提示 migrate_to", payload.get('migrate_to') == 'summarize_content_async',
          f"migrate_to={payload.get('migrate_to')}")
else:
    check("废弃名调用仍响应", False, f"error={r.get('error')}")
    failed += 2

# 4. 未知工具
r2 = mcp.handle_tools_call(2, {"name": "no_such_tool", "arguments": {}})
check("未知工具返回 Tool not found",
      r2.get('error', {}).get('code') == -32601,
      f"code={r2.get('error', {}).get('code')}")

# 5. 规范名调用无废弃标记（dedup_stats_async 本地）
r3 = mcp.handle_tools_call(3, {"name": "dedup_stats_async", "arguments": {}})
if r3.get('result'):
    payload3 = json.loads(r3['result']['content'][0]['text'])
    check("规范名调用无废弃标记", not payload3.get('deprecated'))
else:
    check("规范名调用无废弃标记", False, f"error={r3.get('error')}")

print("\n" + "=" * 70)
print(f"v1.0.0 工具面: {passed} PASS / {failed} FAIL")
print("=" * 70)
if failed:
    print("❌ 存在失败")
    sys.exit(1)
print("✅ 工具合并（25→13）验证通过")
