#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快照存储 - 多Agent协作编排引擎 v5.1

功能：
  1. 节点执行完毕后自动保存上下文快照（增量存储）
  2. 从任意历史快照恢复执行（下游节点重置为 pending）
  3. 执行对比（对比两次执行的输出差异，快速定位问题节点）
  4. 快照保留策略：时间（7天）+ 数量（100次）+ 大小（100MB）三维度淘汰
  5. 版本标识：execution_id（一次运行）+ snapshot_id（每个节点快照）

零第三方依赖，仅使用 Python 标准库

★★★ 存储结构 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
.snapshots/<execution_id>/
├── metadata.json         # 执行元数据（pipeline_name、开始时间、节点列表）
├── snap_<node_id>.json   # 每个节点的快照
└── index.json            # 快照索引（节点→快照文件映射）

★★★ 增量存储 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
首个快照存完整 output_data，后续快照只存 diff（变化的字段）。
重建任意快照 = 前序快照 output_data 依次合并 diff。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

使用方式：
  python snapshot_store.py list <state.json>
  python snapshot_store.py show <state.json> <node_id>
  python snapshot_store.py restore <state.json> <node_id>
  python snapshot_store.py diff <state.json> <node_id_1> <node_id_2>
"""

import json
import os
import sys
import hashlib
import copy
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import state_store

# 快照根目录
SNAPSHOT_ROOT = '.snapshots'

# 快照保留策略
SNAPSHOT_MAX_AGE_DAYS = 7       # 快照最长保留天数
SNAPSHOT_MAX_COUNT = 100        # 快照最大数量
SNAPSHOT_MAX_SIZE_MB = 100      # 快照目录最大大小（MB）

def _snapshot_dir(state_path):
    """根据 state.json 路径确定快照目录"""
    state_dir = os.path.dirname(os.path.abspath(state_path))
    return os.path.join(state_dir, SNAPSHOT_ROOT)

def _execution_dir(state_path, execution_id):
    """某次执行的快照目录"""
    return os.path.join(_snapshot_dir(state_path), execution_id)

def _ensure_dir(path):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)

def _compute_hash(data):
    """计算数据的 hash（用于快速判断变化）"""
    return hashlib.md5(json.dumps(data, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()

def _compute_diff(old_data, new_data):
    """计算两个字典的 diff（只返回变化的字段）"""
    diff = {}
    if not isinstance(old_data, dict) or not isinstance(new_data, dict):
        return new_data
    for k, v in new_data.items():
        if k not in old_data:
            diff[k] = v
        elif old_data[k] != v:
            diff[k] = v
    return diff

def get_execution_id(state):
    """从 state 获取 execution_id"""
    return state.get('pipeline_id', 'unknown')

def save_snapshot(state_path, node_id, log_lines=None):
    """保存节点快照（增量存储）"""
    state = state_store.load_state(state_path)
    execution_id = get_execution_id(state)
    exec_dir = _execution_dir(state_path, execution_id)
    _ensure_dir(exec_dir)

    node = state['nodes'].get(node_id)
    if not node:
        return None

    snap_file = os.path.join(exec_dir, f'snap_{node_id}.json')

    prev_data = {}
    is_incremental = False
    if os.path.exists(snap_file):
        try:
            with open(snap_file, 'r', encoding='utf-8') as f:
                prev_snap = json.load(f)
            prev_data = prev_snap.get('output_data', {})
            is_incremental = True
        except (json.JSONDecodeError, IOError):
            pass

    current_data = node.get('output_data', {})
    diff = _compute_diff(prev_data, current_data)
    state_hash = _compute_hash(current_data)

    snapshot = {
        'snapshot_id': f'{node_id}_{state_hash[:8]}',
        'execution_id': execution_id,
        'node_id': node_id,
        'timestamp': state_store.get_timestamp(),
        'status': node.get('status', 'unknown'),
        'output_data': current_data,
        'diff': diff,
        'is_incremental': is_incremental,
        'state_hash': state_hash,
        'execution_time': _calc_execution_time(node),
        'log': log_lines or [],
    }

    tmp = snap_file + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    os.replace(tmp, snap_file)

    _update_index(exec_dir, execution_id, state)

    # 执行保留策略，淘汰旧快照
    enforce_retention_policy(state_path)

    return snapshot

def _calc_execution_time(node):
    """计算节点执行耗时（秒）"""
    started = node.get('started_at')
    completed = node.get('completed_at')
    if not started or not completed:
        return None
    try:
        s = datetime.strptime(started, '%Y-%m-%dT%H:%M:%S')
        e = datetime.strptime(completed, '%Y-%m-%dT%H:%M:%S')
        return (e - s).total_seconds()
    except (ValueError, TypeError):
        return None

def _update_index(exec_dir, execution_id, state):
    """更新快照索引"""
    index_file = os.path.join(exec_dir, 'index.json')
    index = {}
    if os.path.exists(index_file):
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    index['execution_id'] = execution_id
    index['pipeline_name'] = state.get('pipeline_name', '')
    index['last_updated'] = state_store.get_timestamp()
    index['snapshots'] = index.get('snapshots', {})

    for nid, node in state['nodes'].items():
        if node.get('status') == 'completed':
            snap_file = os.path.join(exec_dir, f'snap_{nid}.json')
            if os.path.exists(snap_file):
                index['snapshots'][nid] = {
                    'file': snap_file,
                    'status': 'completed',
                    'timestamp': node.get('completed_at', ''),
                }

    tmp = index_file + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    os.replace(tmp, index_file)

def list_snapshots(state_path):
    """列出当前执行的所有快照"""
    state = state_store.load_state(state_path)
    execution_id = get_execution_id(state)
    exec_dir = _execution_dir(state_path, execution_id)

    if not os.path.exists(exec_dir):
        print("没有快照记录。")
        return []

    index_file = os.path.join(exec_dir, 'index.json')
    if not os.path.exists(index_file):
        print("没有快照索引。")
        return []

    with open(index_file, 'r', encoding='utf-8') as f:
        index = json.load(f)

    snapshots = index.get('snapshots', {})
    if not snapshots:
        print("没有快照记录。")
        return []

    print("=" * 60)
    print(f"  快照列表：{state.get('pipeline_name', '-')}")
    print(f"  执行 ID：{execution_id}")
    print("=" * 60)
    for nid, meta in snapshots.items():
        print(f"  [{nid}] {meta.get('timestamp', '-')}")
    print("=" * 60)
    return list(snapshots.items())

def show_snapshot(state_path, node_id):
    """显示节点快照详情"""
    state = state_store.load_state(state_path)
    execution_id = get_execution_id(state)
    exec_dir = _execution_dir(state_path, execution_id)
    snap_file = os.path.join(exec_dir, f'snap_{node_id}.json')

    if not os.path.exists(snap_file):
        print(f"节点 [{node_id}] 没有快照记录。")
        return None

    with open(snap_file, 'r', encoding='utf-8') as f:
        snap = json.load(f)

    print("=" * 60)
    print(f"  快照详情：{snap.get('node_id', '-')}")
    print("=" * 60)
    print(f"  快照 ID：{snap.get('snapshot_id', '-')}")
    print(f"  执行 ID：{snap.get('execution_id', '-')}")
    print(f"  保存时间：{snap.get('timestamp', '-')}")
    print(f"  节点状态：{snap.get('status', '-')}")
    print(f"  增量存储：{'是' if snap.get('is_incremental') else '否'}")
    exec_time = snap.get('execution_time')
    print(f"  执行耗时：{f'{exec_time:.2f}秒' if exec_time else '-'}")
    print(f"  输出数据：{json.dumps(snap.get('output_data', {}), ensure_ascii=False)[:300]}")
    if snap.get('diff'):
        print(f"  变化字段：{json.dumps(snap['diff'], ensure_ascii=False)[:200]}")
    print("=" * 60)
    return snap

def restore_snapshot(state_path, node_id):
    """从快照恢复：将该节点下游所有节点重置为 pending"""
    state = state_store.load_state(state_path)
    execution_id = get_execution_id(state)
    exec_dir = _execution_dir(state_path, execution_id)
    snap_file = os.path.join(exec_dir, f'snap_{node_id}.json')

    if not os.path.exists(snap_file):
        print(f"节点 [{node_id}] 没有快照记录，无法恢复。")
        return None

    with open(snap_file, 'r', encoding='utf-8') as f:
        snap = json.load(f)

    nodes = state['nodes']
    children = {nid: [] for nid in nodes}
    for nid, node in nodes.items():
        for dep in node.get('depends_on', []):
            if dep in children:
                children[dep].append(nid)

    downstream = set()
    stack = list(children.get(node_id, []))
    while stack:
        cur = stack.pop()
        if cur in downstream:
            continue
        downstream.add(cur)
        for child in children.get(cur, []):
            stack.append(child)

    node = nodes.get(node_id)
    if node:
        node['output_data'] = snap.get('output_data', {})
        node['status'] = 'completed'

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
    return snap

def diff_snapshots(state_path, node_id_1, node_id_2):
    """对比两个节点的快照输出差异"""
    state = state_store.load_state(state_path)
    execution_id = get_execution_id(state)
    exec_dir = _execution_dir(state_path, execution_id)

    snap1_file = os.path.join(exec_dir, f'snap_{node_id_1}.json')
    snap2_file = os.path.join(exec_dir, f'snap_{node_id_2}.json')

    if not os.path.exists(snap1_file):
        print(f"节点 [{node_id_1}] 没有快照记录。")
        return None
    if not os.path.exists(snap2_file):
        print(f"节点 [{node_id_2}] 没有快照记录。")
        return None

    with open(snap1_file, 'r', encoding='utf-8') as f:
        snap1 = json.load(f)
    with open(snap2_file, 'r', encoding='utf-8') as f:
        snap2 = json.load(f)

    data1 = snap1.get('output_data', {})
    data2 = snap2.get('output_data', {})

    all_keys = set(list(data1.keys()) + list(data2.keys()))
    added = {}
    removed = {}
    changed = {}
    unchanged = {}

    for k in all_keys:
        if k not in data1:
            added[k] = data2[k]
        elif k not in data2:
            removed[k] = data1[k]
        elif data1[k] != data2[k]:
            changed[k] = {'old': data1[k], 'new': data2[k]}
        else:
            unchanged[k] = data1[k]

    print("=" * 60)
    print(f"  快照对比：{node_id_1} vs {node_id_2}")
    print("=" * 60)
    print(f"  [{node_id_1}] 时间：{snap1.get('timestamp', '-')}")
    print(f"  [{node_id_2}] 时间：{snap2.get('timestamp', '-')}")

    if added:
        print(f"\n  新增字段：")
        for k, v in added.items():
            print(f"     {k}: {v!r}")
    if removed:
        print(f"\n  删除字段：")
        for k, v in removed.items():
            print(f"     {k}: {v!r}")
    if changed:
        print(f"\n  变化字段：")
        for k, v in changed.items():
            print(f"     {k}: {v['old']!r} → {v['new']!r}")
    if not added and not removed and not changed:
        print("\n  两次快照输出完全一致")
    print("=" * 60)

    return {'added': added, 'removed': removed, 'changed': changed, 'unchanged': unchanged}


def enforce_retention_policy(state_path):
    """执行快照保留策略，按时间+数量+大小三维度淘汰旧快照

    策略优先级：
    1. 时间：超过 SNAPSHOT_MAX_AGE_DAYS 天的快照淘汰
    2. 数量：超过 SNAPSHOT_MAX_COUNT 个快照时淘汰最旧的
    3. 大小：快照目录超过 SNAPSHOT_MAX_SIZE_MB MB 时淘汰最旧的直到达标
    """
    state = state_store.load_state(state_path)
    execution_id = get_execution_id(state)
    exec_dir = _execution_dir(state_path, execution_id)

    if not os.path.exists(exec_dir):
        return

    index_file = os.path.join(exec_dir, 'index.json')
    if not os.path.exists(index_file):
        return

    with open(index_file, 'r', encoding='utf-8') as f:
        index = json.load(f)

    snapshots = index.get('snapshots', {})
    if not snapshots:
        return

    # 收集快照文件信息
    snap_infos = []
    for nid, meta in snapshots.items():
        snap_file = meta.get('file', '')
        if not snap_file or not os.path.exists(snap_file):
            continue
        try:
            stat = os.stat(snap_file)
            snap_infos.append({
                'node_id': nid,
                'file': snap_file,
                'size': stat.st_size,
                'mtime': stat.st_mtime,
                'timestamp': meta.get('timestamp', ''),
            })
        except OSError:
            continue

    if not snap_infos:
        return

    now = datetime.now().timestamp()
    max_age_secs = SNAPSHOT_MAX_AGE_DAYS * 86400
    to_remove = set()

    # 1. 时间淘汰：超过保留天数的快照
    for info in snap_infos:
        if now - info['mtime'] > max_age_secs:
            to_remove.add(info['node_id'])

    # 2. 数量淘汰：按修改时间排序，保留最新的 SNAPSHOT_MAX_COUNT 个
    remaining = [s for s in snap_infos if s['node_id'] not in to_remove]
    remaining.sort(key=lambda x: x['mtime'], reverse=True)
    if len(remaining) > SNAPSHOT_MAX_COUNT:
        for info in remaining[SNAPSHOT_MAX_COUNT:]:
            to_remove.add(info['node_id'])
        remaining = remaining[:SNAPSHOT_MAX_COUNT]

    # 3. 大小淘汰：计算总大小，超限则从最旧开始淘汰
    total_size = sum(s['size'] for s in remaining)
    max_size_bytes = SNAPSHOT_MAX_SIZE_MB * 1024 * 1024
    if total_size > max_size_bytes:
        # 按时间从旧到新排序
        remaining.sort(key=lambda x: x['mtime'])
        while total_size > max_size_bytes and remaining:
            oldest = remaining.pop(0)
            to_remove.add(oldest['node_id'])
            total_size -= oldest['size']

    # 执行删除
    removed_count = 0
    for nid in to_remove:
        snap_file = os.path.join(exec_dir, f'snap_{nid}.json')
        try:
            if os.path.exists(snap_file):
                os.remove(snap_file)
                removed_count += 1
            if nid in index['snapshots']:
                del index['snapshots'][nid]
        except OSError:
            pass

    if removed_count > 0:
        index['last_updated'] = state_store.get_timestamp()
        tmp = index_file + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        os.replace(tmp, index_file)
        print(f"  快照保留策略：已淘汰 {removed_count} 个旧快照")


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("快照存储 - 多Agent协作编排引擎 v5.0")
        print("=" * 50)
        print("命令列表：")
        print("  python snapshot_store.py list <state.json>")
        print("  python snapshot_store.py show <state.json> <node_id>")
        print("  python snapshot_store.py restore <state.json> <node_id>")
        print("  python snapshot_store.py diff <state.json> <node_id_1> <node_id_2>")
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == 'list':
        if not args:
            print("错误：缺少 state.json 路径")
            sys.exit(1)
        list_snapshots(args[0])
    elif cmd == 'show':
        if len(args) < 2:
            print("错误：参数不足")
            sys.exit(1)
        show_snapshot(args[0], args[1])
    elif cmd == 'restore':
        if len(args) < 2:
            print("错误：参数不足")
            sys.exit(1)
        restore_snapshot(args[0], args[1])
    elif cmd == 'diff':
        if len(args) < 3:
            print("错误：参数不足")
            sys.exit(1)
        diff_snapshots(args[0], args[1], args[2])
    else:
        print(f"错误：未知命令 [{cmd}]")
        sys.exit(1)
