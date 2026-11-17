#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误恢复引擎 - 多Agent协作编排引擎 v2.0

功能：三级降级策略（重试 → 降级 → 中止）的决策与执行
零第三方依赖，仅使用 Python 标准库

★★★ 安全说明 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 所有状态文件路径经过规范化校验
2. 错误信息中可能包含敏感数据，注意日志管理
3. abort 后状态文件保留，便于审计
4. resume 操作会清除失败记录，谨慎使用

★★★ 易错点和注意事项 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 必须先 fail 再 retry：
   错误流程：step → 任务失败 → 直接 retry
   正确流程：step → 任务失败 → fail_node（标记失败）→ retry（触发恢复）

2. retry 命令会自动判断：
   - 未达 max_retry → 重置为 pending，等待 step 重新获取
   - 已达 max_retry → 自动执行 fallback 降级策略

3. retry_count 由 fail_node() 递增，不需要手动管理

4. fallback 策略说明：
   - skip：跳过此节点，下游收到 output_data={"skipped": true}
   - default：使用预设 default_value 作为输出，状态标记为 completed
   - abort：中止流水线，后续节点不再执行

5. abort 后恢复：运行 orchestrator.py resume <state.json> [--force]
   这将重置所有 failed 节点，给予全新重试机会（retry_count 归零）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import sys
import os
import time
from datetime import datetime

# 复用 state_store 的状态读写函数（单一真相来源）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
import state_store


def get_timestamp():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


def should_retry(node):
    """判断节点是否可以重试

    retry_count 由 fail_node() 负责递增，此处只读。
    语义：retry_count < max_retry 表示还可以再试。
    """
    return node.get('retry_count', 0) < node.get('max_retry', 3)


def execute_retry(state_path, node_id, error_msg):
    """Level 1: 重试策略

    使用流程：
    1. AI 执行节点任务失败
    2. 运行：python state_store.py fail <state.json> <node_id> '错误描述'
    3. 运行：python error_recovery.py retry <state.json> <node_id> '错误描述'
       → 未达 max_retry：节点重置为 pending，等待重新执行
       → 已达 max_retry：自动执行 fallback 降级策略

    ★★★ 安全提示 ★★★
    - error_msg 会写入 state.json，不要包含敏感信息
    - 建议 error_msg 简洁清晰，不超过 200 字符
    """
    state = state_store.load_state(state_path)
    node = state['nodes'].get(node_id)

    if not node:
        print(f"错误：节点 [{node_id}] 不存在")
        print(f"  可用节点：{', '.join(state['nodes'].keys())}")
        sys.exit(1)

    # 获取节点重试配置（优先节点级 retry_config，降级到旧全局策略）
    retry_config = state_store.get_retry_config(node)
    max_retry = retry_config['count']
    backoff_base = retry_config['backoff_base']
    fallback_chain = retry_config['fallback_chain']

    # 检查是否还有重试次数
    if not should_retry(node):
        print(f"节点 [{node_id}] 已达最大重试次数 ({max_retry})")
        print(f"  自动进入降级流程...")
        return execute_fallback(state_path, node_id, error_msg, fallback_chain)

    # 将节点状态重置为 pending，等待重新执行
    node['status'] = 'pending'
    node['error'] = error_msg

    retry_num = node['retry_count']  # 已经失败的次数
    remaining = max_retry - retry_num  # 还有几次机会（本次重置后）
    delay = backoff_base ** retry_num  # 指数退避

    state_store.safe_write(state, state_path)

    print("=" * 60)
    print(f"  🔄 Level 1: 重试策略")
    print("=" * 60)
    print(f"节点：{node_id}")
    print(f"错误：{error_msg}")
    print(f"已失败：{retry_num}/{max_retry} 次")
    print(f"重置为 pending 后，还剩 {remaining} 次重试机会")
    print(f"建议等待：{delay} 秒后重新执行")
    print(f"\n操作步骤：")
    print(f"  1. 等待 {delay} 秒（可选，用于限流恢复）")
    print(f"  2. 运行：python orchestrator.py step {state_path}")
    print(f"  3. 重新执行节点 [{node_id}] 的任务")
    print(f"  4. 成功后：python state_store.py complete {state_path} {node_id} '{{\"result\":\"...\"}}'")
    print(f"  5. 仍失败：python state_store.py fail {state_path} {node_id} '错误描述'")
    print(f"             python error_recovery.py retry {state_path} {node_id} '错误描述'")
    print("=" * 60)
    return state


def execute_fallback(state_path, node_id, error_msg, fallback_chain=None):
    """Level 2: 降级策略

    在 retry 耗尽后自动执行，也可手动调用：
      python error_recovery.py fallback <state.json> <node_id> '错误描述'

    fallback_chain: 降级动作链（来自节点 retry_config），默认使用旧全局 fallback

    ★★★ 安全提示 ★★★
    - abort 后状态文件保留，便于事后审计
    - skip/default 会继续执行下游节点，注意数据完整性
    """
    state = state_store.load_state(state_path)
    node = state['nodes'].get(node_id)

    if not node:
        print(f"错误：节点 [{node_id}] 不存在")
        sys.exit(1)

    # 确定降级动作：优先 fallback_chain[0]，否则旧 fallback，否则 abort
    fallback = fallback_chain[0] if fallback_chain else node.get('fallback', 'abort')

    print("=" * 60)
    print(f"  ⬇️ Level 2: 降级策略 ({fallback})")
    print("=" * 60)
    print(f"节点：{node_id}")
    print(f"错误：{error_msg}")

    if fallback == 'skip':
        node['status'] = 'skipped'
        node['error'] = f"已跳过：{error_msg}"
        node['output_data'] = {"skipped": True, "reason": error_msg}
        state_store.safe_write(state, state_path)
        print(f"\n策略：⏭️ 跳过此节点")
        print(f"影响：下游节点将收到 output_data={{\"skipped\":true,\"reason\":\"...\"}}")
        print(f"\n继续执行：python orchestrator.py step {state_path}")

    elif fallback == 'default':
        default_val = node.get('default_value', {})
        node['status'] = 'completed'
        node['error'] = f"使用默认值降级：{error_msg}"
        node['output_data'] = default_val
        state_store.safe_write(state, state_path)
        print(f"\n策略：✅ 使用预设默认值完成")
        print(f"默认值：{json.dumps(default_val, ensure_ascii=False)}")
        print(f"影响：下游节点将收到默认值作为输入")
        print(f"\n继续执行：python orchestrator.py step {state_path}")

    elif fallback == 'abort':
        print(f"\n策略：🛑 中止流水线")
        print(f"\n后续操作：")
        print(f"  1. 分析错误原因：python orchestrator.py impact {state_path} {node_id}")
        print(f"  2. 修复问题后断点续传：python orchestrator.py resume {state_path} --force")
        print(f"  3. 查看部分报告：python orchestrator.py report {state_path}")
        node['status'] = 'failed'
        node['error'] = error_msg
        state['status'] = 'aborted'
        state_store.safe_write(state, state_path)

    else:
        print(f"\n⚠️ 未知降级策略 [{fallback}]，默认中止")
        node['status'] = 'failed'
        node['error'] = f"未知策略[{fallback}]，已中止"
        state['status'] = 'aborted'
        state_store.safe_write(state, state_path)

    print("=" * 60)
    return state


def analyze_downstream_impact(state_path, node_id):
    """分析失败节点的下游影响（递归查找所有受影响的节点）

    ★★★ 使用场景 ★★★
    当某个节点失败时，查看影响范围，决定是修复还是跳过。

    ★★★ 安全说明 ★★★
    此命令是只读的，不会修改任何状态文件。

    使用方式：
      python error_recovery.py impact <state.json> <node_id>
    或：
      python orchestrator.py impact <state.json> <node_id>
    """
    state = state_store.load_state(state_path)
    node = state['nodes'].get(node_id)

    if not node:
        print(f"错误：节点 [{node_id}] 不存在")
        sys.exit(1)

    # 找出所有直接和间接依赖此节点的下游节点（BFS）
    all_nodes = state['nodes']
    affected = set()
    queue = [node_id]

    while queue:
        current = queue.pop(0)
        for aid, anode in all_nodes.items():
            if current in anode.get('depends_on', []) and aid not in affected:
                affected.add(aid)
                queue.append(aid)

    print("=" * 60)
    print(f"  📊 下游影响分析：{node_id}")
    print("=" * 60)

    if not affected:
        print(f"✅ 无下游节点受影响（此节点为末端节点或无人依赖它）")
    else:
        print(f"受影响节点（{len(affected)} 个）：")
        for aid in sorted(affected):
            anode = all_nodes[aid]
            status_icon = {
                'pending': '⏳',
                'running': '🔄',
                'completed': '✅',
                'failed': '❌',
                'skipped': '⏭️'
            }.get(anode['status'], '?')
            print(f"  {status_icon} [{aid}] {anode.get('name', aid)} - 当前状态: {anode['status']}")

    print("=" * 60)
    return affected


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("错误恢复引擎 - 多Agent协作编排引擎 v2.0")
        print("=" * 50)
        print("命令列表：")
        print("  python error_recovery.py retry <state.json> <node_id> [error_msg]")
        print("      → 重试节点（自动判断是否还可重试）")
        print("      → 未达上限：重置为 pending")
        print("      → 已达上限：自动执行 fallback 降级")
        print("")
        print("  python error_recovery.py fallback <state.json> <node_id> [error_msg]")
        print("      → 手动执行降级策略（skip/default/abort）")
        print("")
        print("  python error_recovery.py impact <state.json> <node_id>")
        print("      → 分析失败节点的下游影响范围")
        print("")
        print("★★★ 典型失败处理流程 ★★★")
        print("  1. 节点任务执行失败")
        print("  2. python state_store.py fail <state.json> <node_id> '错误描述'")
        print("  3. python error_recovery.py retry <state.json> <node_id> '错误描述'")
        print("  4a. 重试成功 → 修复后运行 orchestrator.py step <state.json>")
        print("  4b. 重试耗尽 → 自动执行 fallback 降级")
        print("  5. abort 策略 → 修复后运行 orchestrator.py resume <state.json> --force")
        print("")
        print("★★★ 安全提示 ★★★")
        print("  - error_msg 会持久化到 state.json，不要包含敏感信息")
        print("  - abort 后状态文件保留，便于事后审计")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'retry':
        if len(sys.argv) < 4:
            print("错误：参数不足")
            print("用法：python error_recovery.py retry <state.json> <node_id> [error_msg]")
            print("示例：python error_recovery.py retry state.json node_a '网络超时'")
            print("")
            print("★★★ 注意 ★★★")
            print("  运行 retry 之前，先运行 fail 标记失败：")
            print("  python state_store.py fail <state.json> <node_id> '错误描述'")
            sys.exit(1)
        error_msg = sys.argv[4] if len(sys.argv) > 4 else "未知错误"
        execute_retry(sys.argv[2], sys.argv[3], error_msg)

    elif cmd == 'fallback':
        if len(sys.argv) < 4:
            print("错误：参数不足")
            print("用法：python error_recovery.py fallback <state.json> <node_id> [error_msg]")
            print("示例：python error_recovery.py fallback state.json node_a '网络超时'")
            sys.exit(1)
        error_msg = sys.argv[4] if len(sys.argv) > 4 else "未知错误"
        execute_fallback(sys.argv[2], sys.argv[3], error_msg)

    elif cmd == 'impact':
        if len(sys.argv) < 4:
            print("错误：参数不足")
            print("用法：python error_recovery.py impact <state.json> <node_id>")
            print("示例：python error_recovery.py impact state.json node_a")
            sys.exit(1)
        analyze_downstream_impact(sys.argv[2], sys.argv[3])

    else:
        print(f"错误：未知命令 [{cmd}]")
        print("可用命令：retry / fallback / impact")
        print("运行 python error_recovery.py --help 查看详细用法")
        sys.exit(1)
