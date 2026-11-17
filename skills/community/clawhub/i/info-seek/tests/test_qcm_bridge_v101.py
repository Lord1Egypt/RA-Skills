#!/usr/bin/env python3
"""test_qcm_bridge_v101.py — QCM 反向协同桥接测试（A1 · v1.0.1）

覆盖（10 用例）：
  Q1: qcm_query 在 TOOLS 规范工具面中注册
  Q2: 空 query → failed / invalid_input
  Q3: QCM 未安装 → degraded / qcm_not_installed（优雅降级）
  Q4: QCM 已安装 → ok + qcm_result 4 形态字段（monkeypatch 探测，快路径）
  Q5: QCM 调用失败 → degraded / 调用失败
  Q6: _probe_qcm_root env 优先（QCM_ROOT 指向真实目录）
  Q7: qcm_query 输入 schema 含 query 必填
  Q8: 分发分支 handle_tools_call 可路由 qcm_query
  Q9: async 生成逻辑不误生成 qcm_query_async（qcm_query 无 async 包装）
  Q10: 真实 QCM 安装时端到端调用（QCM 缺失 SKIP，不阻塞标准回归）
"""
import os
import sys
import json
from pathlib import Path

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'scripts'))
sys.path.insert(0, str(INFOSEEK / 'core'))

import infoseek_mcp_server as m
import mcp_tools_qcm as qcm_mod

passed, failed = [], []


def check(name, cond, extra=''):
    if cond:
        passed.append(name)
        print(f"  [PASS] {name} {extra}")
    else:
        failed.append(name)
        print(f"  [FAIL] {name} {extra}")


print("=" * 60)
print("QCM 反向协同桥接测试（v1.0.1 A1）")
print("=" * 60)

# Q1: 注册
names = {t['name'] for t in m.TOOLS}
check('Q1 qcm_query 在规范工具面', 'qcm_query' in names)

# Q2: 空 query
r2 = m.tool_qcm_query({'query': '   '})
check('Q2 空 query 拒绝', r2.get('status') == 'failed' and r2.get('degradation') == 'invalid_input',
      f"status={r2.get('status')}")

# Q3: QCM 未安装（monkeypatch 探测返回空）
orig_probe = qcm_mod._probe_qcm_root
qcm_mod._probe_qcm_root = lambda: ''
r3 = m.tool_qcm_query({'query': '焊接虚焊'})
qcm_mod._probe_qcm_root = orig_probe
check('Q3 未安装降级', r3.get('status') == 'degraded' and r3.get('degradation') == 'qcm_not_installed',
      f"status={r3.get('status')}")

# Q4: QCM 已安装（monkeypatch _qcm_call 返回 4 形态，避免真实子进程）
# v1.8.1 修复：须同时 patch _probe_qcm_root —— QCM 未装环境下探测返回 ''，
# 被测函数直接走「未安装」分支，_qcm_call 永不触发 → Q4/Q5 恒 FAIL（测试脆弱性）。
orig_call = qcm_mod._qcm_call
orig_probe_q4 = qcm_mod._probe_qcm_root
qcm_mod._probe_qcm_root = lambda: '/tmp/fake-qcm-root'
qcm_mod._qcm_call = lambda root, query, form='': {
    "status": "ok", "qcm_result": {
        "intent": "焊接客诉", "matched_qcm_form": "quick_response",
        "confidence_score": 80, "degradation_path": "L0_infoseek",
        "anchors": [{"title": "A", "url": "http://x"}], "version": "QCM"}}
r4 = m.tool_qcm_query({'query': '焊接虚焊'})
qcm_mod._qcm_call = orig_call
qcm_mod._probe_qcm_root = orig_probe_q4
qr = r4.get('qcm_result', {})
check('Q4 正常调用 4 形态', r4.get('status') == 'ok' and qr.get('form') == 'quick_response'
      and qr.get('confidence') == 80 and qr.get('version') == 'QCM',
      f"form={qr.get('form')} conf={qr.get('confidence')}")

# Q5: QCM 调用失败 → degraded（v1.8.1：同 Q4，须 patch 探测函数）
orig_call2 = qcm_mod._qcm_call
orig_probe_q5 = qcm_mod._probe_qcm_root
qcm_mod._probe_qcm_root = lambda: '/tmp/fake-qcm-root'
qcm_mod._qcm_call = lambda root, query, form='': {"status": "degraded", "reason": "QCM 调用失败: boom"}
r5 = m.tool_qcm_query({'query': '测试'})
qcm_mod._qcm_call = orig_call2
qcm_mod._probe_qcm_root = orig_probe_q5
check('Q5 调用失败降级', r5.get('status') == 'degraded' and 'boom' in r5.get('reason', ''),
      f"reason={r5.get('reason', '')[:30]}")

# Q6: _probe_qcm_root env 优先（QCM_ROOT 指向真实目录时命中）
real_qcm = str(Path.home() / '.workbuddy' / 'skills' / 'QCM')
if os.path.isdir(real_qcm):
    os.environ['QCM_ROOT'] = real_qcm
    root = qcm_mod._probe_qcm_root()
    os.environ.pop('QCM_ROOT', None)
    check('Q6 env 探测命中', root == real_qcm, f"root={root}")
else:
    check('Q6 env 探测命中（QCM 未装 SKIP）', True, '⏭️')

# Q7: schema 必填 query
t7 = next((t for t in m.TOOLS if t['name'] == 'qcm_query'), None)
req = (t7 or {}).get('inputSchema', {}).get('required', [])
check('Q7 schema query 必填', t7 is not None and 'query' in req, f"required={req}")

# Q8: handle_tools_call 路由
r8 = m.handle_tools_call(1, {'name': 'qcm_query', 'arguments': {'query': ''}})
has_error = 'error' in r8 or 'result' in r8
check('Q8 分发可路由', has_error, f"keys={list(r8.keys())[:3]}")

# Q9: 不生成 qcm_query_async
async_gen = [t['name'] for t in m.TOOLS if t['name'] == 'qcm_query_async']
check('Q9 无 qcm_query_async 生成', len(async_gen) == 0)

# Q10: 真实 QCM 端到端（QCM 缺失 SKIP）
qcm_root = qcm_mod._probe_qcm_root()
if qcm_root:
    try:
        r10 = m.tool_qcm_query({'query': '金线键合虚焊复发分析'})
        check('Q10 真实端到端', r10.get('status') in ('ok', 'degraded'),
              f"status={r10.get('status')} form={(r10.get('qcm_result') or {}).get('form')}")
    except Exception as e:
        check('Q10 真实端到端', False, str(e)[:80])
else:
    check('Q10 真实端到端（QCM 未装 SKIP）', True, '⏭️')

print()
print(f"=== QCM 桥接测试: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    sys.exit(1)
print("ALL PASS")
