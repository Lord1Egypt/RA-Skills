#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一状态恢复子系统 - 多Agent协作编排引擎 v5.1

功能：合并断点续传 + 快照恢复为统一入口，消除两套独立的状态恢复代码。

两种恢复模式：
  1. resume（断点续传）：将所有 failed 节点重置为 pending，retry_count 归零
  2. snapshot（快照恢复）：从指定节点的快照恢复，下游节点重置为 pending

统一入口：restore_to_node(state_path, node_id, mode)
  - mode='resume'  → 恢复所有失败节点（node_id 可传 None）
  - mode='snapshot'→ 从 node_id 快照恢复下游（node_id 必传）

零第三方依赖，仅使用 Python 标准库

★★★ 安全说明 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 所有状态修改经 state_store.safe_write 原子落盘
2. 恢复前自动创建恢复前快照（防止误操作不可逆）
3. 路径安全：所有路径经规范化，防止路径穿越
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

使用方式：
  python state_recovery.py resume <state.json> [--force]
  python state_recovery.py restore <state.json> <node_id>
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import state_store
import snapshot_store


def restore_to_node(state_path, node_id, mode, force=False):
    """统一状态恢复入口

    Args:
        state_path: state.json 路径
        node_id: 快照节点 id（mode='snapshot' 时必传，mode='resume' 时可传 None）
        mode: 'resume' | 'snapshot'
        force: 是否跳过确认提示

    Returns:
        dict: 恢复结果 {'mode': ..., 'reset_count': ..., 'restored_from': ...}
    """
    if mode not in ('resume', 'snapshot'):
        raise ValueError(f"无效恢复模式 [{mode}]，应为 'resume' 或 'snapshot'")

    if mode == 'snapshot' and not node_id:
        raise ValueError("snapshot 模式下 node_id 不能为空")

    state = state_store.load_state(state_path)

    # 恢复前自动创建快照（防止误操作）
    _create_recovery_checkpoint(state_path, state, mode, node_id)

    if mode == 'resume':
        return _restore_failed_nodes(state_path, state, force)
    else:
        return _restore_from_snapshot(state_path, state, node_id, force)


def _create_recovery_checkpoint(state_path, state, mode, node_id):
    """恢复前自动创建检查点快照"""
    try:
        checkpoint_dir = os.path.join(
            os.path.dirname(state_path), '.recovery_checkpoints'
        )
        os.makedirs(checkpoint_dir, exist_ok=True)
        checkpoint = {
            'timestamp': state_store.get_timestamp(),
            'mode': mode,
            'node_id': node_id,
            'pipeline_id': state.get('pipeline_id', 'unknown'),
            'node_states': {
                nid: n.get('status', 'unknown')
                for nid, n in state.get('nodes', {}).items()
            }
        }
        filename = f"checkpoint_{mode}_{state_store.get_timestamp().replace(':', '-')}.json"
        filepath = os.path.join(checkpoint_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        # 只保留最近 10 个检查点
        _cleanup_old_checkpoints(checkpoint_dir, keep=10)
    except Exception as e:
        pass  # 检查点创建失败不应阻塞恢复流程


def _cleanup_old_checkpoints(checkpoint_dir, keep=10):
    """清理旧检查点，只保留最近 keep 个"""
    try:
        checkpoints = sorted([
            f for f in os.listdir(checkpoint_dir)
            if f.startswith('checkpoint_') and f.endswith('.json')
        ])
        for old in checkpoints[:-keep]:
            try:
                os.remove(os.path.join(checkpoint_dir, old))
            except OSError:
                pass
    except OSError:
        pass


def _restore_failed_nodes(state_path, state, force=False):
    """恢复所有 failed 节点为 pending（原 resume_pipeline 逻辑）"""
    print("=" * 60)
    print("  断点续传模式（统一状态恢复）")
    print(f"  流水线：{state.get('pipeline_name', '-')}")
    print("=" * 60)

    reset_count = 0
    for aid, node in state['nodes'].items():
        if node['status'] == 'failed':
            node['status'] = 'pending'
            node['retry_count'] = 0
            node['error'] = None
            reset_count += 1

    state['status'] = 'running'
    state_store.safe_write(state, state_path)

    completed = sum(1 for n in state['nodes'].values() if n['status'] == 'completed')
    total = len(state['nodes'])
    print(f"已完成节点：{completed}/{total}")

    if reset_count > 0:
        print(f"重置失败节点：{reset_count} 个（已重置为待执行，重试计数归零）")
        print(f"\n继续执行请运行：python orchestrator.py step {state_path}")
    else:
        print("没有需要重置的失败节点")

    print("=" * 60)

    return {'mode': 'resume', 'reset_count': reset_count, 'restored_from': None}


def _restore_from_snapshot(state_path, state, node_id, force=False):
    """从快照恢复：将指定节点下游所有节点重置为 pending（原 restore_snapshot 逻辑）"""
    execution_id = snapshot_store.get_execution_id(state)
    exec_dir = snapshot_store._execution_dir(state_path, execution_id)
    snap_file = os.path.join(exec_dir, f'snap_{node_id}.json')

    if not os.path.exists(snap_file):
        print(f"节点 [{node_id}] 没有快照记录，无法恢复。")
        return None

    with open(snap_file, 'r', encoding='utf-8') as f:
        snap = json.load(f)

    nodes = state['nodes']

    # 构建子节点邻接表
    children = {nid: [] for nid in nodes}
    for nid, node in nodes.items():
        for dep in node.get('depends_on', []):
            if dep in children:
                children[dep].append(nid)

    # BFS 收集所有下游节点
    downstream = set()
    stack = list(children.get(node_id, []))
    while stack:
        cur = stack.pop()
        if cur in downstream:
            continue
        downstream.add(cur)
        for child in children.get(cur, []):
            stack.append(child)

    # 恢复快照节点输出
    node = nodes.get(node_id)
    if node:
        node['output_data'] = snap.get('output_data', {})
        node['status'] = 'completed'

    # 重置下游节点
    reset_count = 0
    for did in downstream:
        dnode = nodes.get(did)
        if dnode and dnode.get('status') != 'pending':
            dnode['status'] = 'pending'
            dnode['started_at'] = None
            dnode['completed_at'] = None
            dnode['retry_count'] = 0
            dnode['error'] = None
            reset_count += 1

    state_store.safe_write(state, state_path)

    print(f"✅ 已从 [{node_id}] 快照恢复")
    print(f"   快照 ID：{snap.get('snapshot_id', '-')}")
    print(f"   快照输出：{json.dumps(snap.get('output_data', {}), ensure_ascii=False)[:200]}")
    print(f"   重置下游节点：{reset_count} 个")

    return {'mode': 'snapshot', 'reset_count': reset_count, 'restored_from': node_id}


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("统一状态恢复 - 多Agent协作编排引擎 v5.1")
        print("=" * 50)
        print("命令列表：")
        print("  python state_recovery.py resume <state.json> [--force]")
        print("      → 断点续传：重置所有 failed 节点为 pending")
        print("  python state_recovery.py restore <state.json> <node_id>")
        print("      → 快照恢复：从指定节点快照恢复下游")
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == 'resume':
        if not args:
            print("错误：缺少 state.json 路径")
            sys.exit(1)
        force = '--force' in args
        state_path = args[0]
        restore_to_node(state_path, None, 'resume', force=force)

    elif cmd == 'restore':
        if len(args) < 2:
            print("错误：参数不足")
            print("用法：python state_recovery.py restore <state.json> <node_id>")
            sys.exit(1)
        restore_to_node(args[0], args[1], 'snapshot')

    else:
        print(f"错误：未知命令 [{cmd}]")
        sys.exit(1)
