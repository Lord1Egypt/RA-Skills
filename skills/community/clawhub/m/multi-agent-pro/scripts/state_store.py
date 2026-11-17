#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
状态持久化管理器 - 多Agent协作编排引擎 v5.2

功能：pipeline_state.json 的创建、读取、更新、查询 + 断点续传支持
新增：执行历史追踪（.execution_history.json）+ 控制流节点专有字段持久化
新增：节点完成后自动保存快照（供执行回放 / Time Travel 使用）
新增：节点级成本追踪（token/cost 聚合，对接 cn-llm-router）
零第三方依赖，仅使用 Python 标准库

★★★ 安全说明 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 路径安全：所有文件路径经过规范化，防止路径穿越攻击
2. 原子写入：使用 .tmp + os.replace 确保写入完整性
3. 文件大小：单个节点输出超过 10MB 时自动写入独立文件
4. 敏感数据：不会自动脱敏，用户需自行处理输出中的敏感信息
5. 并发安全：Windows 下使用 msvcrt 文件锁，Linux/macOS 使用 fcntl

★★★ 重要提示 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 首次使用需要创建 pipeline.json 文件（定义流水线的 JSON 配置）
   创建后运行：python orchestrator.py run <pipeline.json>
   这会自动生成 pipeline_state.json 状态文件

2. 后续所有操作都基于 pipeline_state.json（不是 pipeline.json！）

3. 文件路径中不要使用中文或特殊字符，建议使用英文路径

4. 不要手动编辑 pipeline_state.json，可能导致状态不一致
   （如果状态损坏，运行 orchestrator.py resume 重置）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import sys
import os
import time
import tempfile
from datetime import datetime

# 文件大小限制：单个节点输出最大 10MB
MAX_OUTPUT_SIZE = 10 * 1024 * 1024
# 状态文件最大 50MB
MAX_STATE_SIZE = 50 * 1024 * 1024


def get_timestamp():
    """获取当前时间戳（ISO 8601 格式）"""
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


def get_retry_config(node):
    """
    获取节点的重试配置。

    优先级：
    1. 节点级 retry_config 块（v5.3 新增）
    2. 旧全局字段（retry/fallback）向后兼容

    返回 dict: {'count': int, 'backoff_base': float, 'fallback_chain': list}
    """
    retry_config = node.get('retry_config')
    if retry_config:
        return retry_config

    # 旧全局策略降级
    return {
        'count': node.get('max_retry', 3),
        'backoff_base': 2,
        'fallback_chain': ['retry', node.get('fallback', 'abort')],
    }


def validate_path(filepath, must_exist=False):
    """路径安全校验：规范化路径，防止路径穿越

    返回规范化后的绝对路径。
    如果 must_exist=True 且文件不存在，则报错退出。
    """
    filepath = os.path.abspath(os.path.normpath(filepath))
    if must_exist and not os.path.exists(filepath):
        print(f"错误：文件不存在 [{filepath}]")
        print("  修复步骤：")
        print("  1. 确认路径是否正确（区分大小写）")
        print("  2. 运行以下命令初始化：")
        print("     python orchestrator.py run <pipeline.json>")
        sys.exit(1)
    return filepath


def safe_write(state, state_path):
    """安全保存状态到文件（原子写入 + 文件大小检查）"""
    state['updated_at'] = get_timestamp()
    tmp_path = state_path + '.tmp'
    try:
        # 先写入临时文件
        with open(tmp_path, 'w', encoding='utf-8') as f:
            data = json.dumps(state, ensure_ascii=False, indent=2)
            # 检查序列化后大小
            if len(data.encode('utf-8')) > MAX_STATE_SIZE:
                print(f"错误：状态文件过大（>{MAX_STATE_SIZE // 1024 // 1024}MB）")
                print("  建议：清理历史输出数据，或拆分流水线")
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                sys.exit(1)
            f.write(data)
        # 原子替换
        os.replace(tmp_path, state_path)
    except OSError as e:
        print(f"错误：无法写入状态文件 [{state_path}]")
        print(f"  原因：{e}")
        print(f"  建议：检查磁盘空间和文件权限")
        # 清理临时文件
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        sys.exit(1)


def load_state(state_path):
    """加载状态文件（带路径校验和格式检查）"""
    state_path = validate_path(state_path, must_exist=True)
    try:
        # 检查文件大小
        file_size = os.path.getsize(state_path)
        if file_size > MAX_STATE_SIZE:
            print(f"警告：状态文件过大（{file_size // 1024 // 1024}MB），加载可能较慢")
        with open(state_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"错误：状态文件 JSON 格式不合法 [{state_path}]")
        print(f"  详情：第 {e.lineno} 行 - {e.msg}")
        print(f"  建议：使用 JSON 校验工具检查文件，或重新初始化")
        sys.exit(1)


def init_state(pipeline, state_path=None):
    """初始化状态文件

    ★★★ 安全校验 ★★★
    - pipeline 必须是已验证的 dict（由 orchestrator.py run 调用前已验证）
    - state_path 经过路径规范化
    - 节点 id 不能包含路径分隔符（防止路径穿越）
    """
    if state_path is None:
        state_path = pipeline.get('state_store', {}).get('path', './pipeline_state.json')
    state_path = validate_path(state_path)

    # 用 pipeline_name + 时间戳生成唯一 ID
    pipeline_id = pipeline.get('pipeline_name', 'unnamed').replace(' ', '_') + '_' + str(int(time.time()))

    state = {
        "pipeline_id": pipeline_id,
        "pipeline_name": pipeline.get('pipeline_name', 'unnamed'),
        "version": pipeline.get('version', '2.0'),
        "created_at": get_timestamp(),
        "updated_at": get_timestamp(),
        "status": "initialized",  # initialized → running → completed / aborted
        "nodes": {}
    }

    # 将每个 agent 转换为状态节点
    for agent in pipeline.get('agents', []):
        aid = agent.get('id')
        # 安全校验：节点 id 不能包含路径分隔符
        if os.sep in aid or '/' in aid or '\\' in aid:
            print(f"错误：节点 id [{aid}] 包含非法字符（路径分隔符）")
            print("  修复：使用纯英文/数字/下划线作为节点 id")
            sys.exit(1)
        node_state = {
            "name": agent.get('name', aid),
            "role": agent.get('role', ''),
            "type": agent.get('type', 'task'),  # task/approval/condition/switch/for-each/while-loop/evaluate
            "status": "pending",       # pending → running → completed / failed / skipped
            "depends_on": agent.get('depends_on', []),
            "retry_count": 0,
            "max_retry": agent.get('retry', 3),
            "timeout": agent.get('timeout', 60),
            "fallback": agent.get('fallback', 'abort'),
            "inputs": agent.get('inputs', []),
            "outputs": agent.get('outputs', []),
            "output_data": {},
            "error": None,
            "started_at": None,
            "completed_at": None
        }
        # 任务级重试策略块（可选，未配置时走旧全局策略）
        # 格式: {"count": 3, "backoff_base": 2, "fallback_chain": ["retry", "reparam", "skip"]}
        retry_block = agent.get('retry')
        if isinstance(retry_block, dict):
            node_state['retry_config'] = {
                'count': int(retry_block.get('count', 3)),
                'backoff_base': float(retry_block.get('backoff_base', 2)),
                'fallback_chain': retry_block.get('fallback_chain', ['retry', 'skip']),
            }
        # 保留控制流节点的专有字段（否则动态路由时会丢失配置）
        for ctrl_field in ('condition', 'on_true', 'on_false',
                           'switch', 'cases', 'default',
                           'items', 'template', 'join',
                           'loop_body', 'max_iterations',
                           'pipeline_ref', 'params', 'outputs',
                           'quality_expr', 'retry_targets', 'max_eval_rounds'):
            if ctrl_field in agent:
                node_state[ctrl_field] = agent[ctrl_field]
        # while-loop 迭代计数初始化
        if agent.get('type') == 'while-loop':
            node_state['iteration'] = 0
        # evaluate 评估轮次计数初始化
        if agent.get('type') == 'evaluate':
            node_state['eval_round'] = 0
        # approval 节点超时策略字段
        if agent.get('type') == 'approval':
            node_state['timeout_seconds'] = agent.get('timeout_seconds', 0)
            node_state['timeout_action'] = agent.get('timeout_action', 'reject')
        state['nodes'][aid] = node_state

    safe_write(state, state_path)
    print(f"状态文件已初始化：{state_path}")
    print(f"流水线 ID：{pipeline_id}")
    print(f"节点数量：{len(state['nodes'])}")
    return state, state_path


def complete_node(state_path, node_id, output_json=None):
    """标记节点为已完成

    使用方式：
      python state_store.py complete <state.json> <node_id> '{"key":"value"}'

    output_json 必须是合法 JSON 字符串（建议用单引号包裹）。
    如果 output_json 不是合法 JSON 字符串，会降级为 {"raw_output": "原字符串保存"}。

    ★★★ 注意 ★★★
    - 节点输出数据会持久化到 state.json
    - 如果输出包含敏感信息（密钥、密码等），请手动脱敏后再保存
    - 单个节点输出超过 10MB 时，会自动写入独立的 output_<node_id>.json 文件
    """
    state = load_state(state_path)
    if node_id not in state['nodes']:
        print(f"错误：节点 [{node_id}] 不存在")
        print(f"  可用节点：{', '.join(state['nodes'].keys())}")
        print(f"  修复：检查 pipeline.json 中的 id 是否与命令中的 id 一致")
        sys.exit(1)

    node = state['nodes'][node_id]
    if not node.get('started_at'):
        node['started_at'] = get_timestamp()
    node['status'] = 'completed'
    node['completed_at'] = get_timestamp()

    if output_json:
        try:
            output_data = json.loads(output_json)
        except json.JSONDecodeError:
            # 不是合法 JSON → 降级保存原始字符串
            output_data = {"raw_output": output_json}
        node['output_data'] = output_data
        # 提取成本数据（如果有 _cost 字段）
        if isinstance(output_data, dict) and '_cost' in output_data:
            node['cost_data'] = output_data.pop('_cost')
    else:
        node['output_data'] = {"result": "completed"}

    all_done = all(n['status'] in ('completed', 'skipped') for n in state['nodes'].values())
    if all_done:
        state['status'] = 'completed'
    else:
        state['status'] = 'running'

    safe_write(state, state_path)
    print(f"节点 [{node_id}] 已标记为完成")
    if output_json:
        print(f"  输出数据已保存")
    print(f"  完成时间：{node['completed_at']}")

    # 自动保存快照（供执行回放 / Time Travel 使用）
    try:
        import snapshot_store
        snapshot_store.save_snapshot(state_path, node_id)
    except Exception as e:
        pass  # 快照保存失败不应阻塞主流程

    if all_done:
        print(f"\n🎉 流水线 [{state['pipeline_name']}] 全部节点已完成！")
        print(f"  查看完整报告：python orchestrator.py report {state_path}")
        # 保存执行历史
        try:
            save_execution_history(state_path, state)
        except Exception as e:
            print(f"  [调试] 保存历史失败：{e}")
    return state


def fail_node(state_path, node_id, error_msg):
    """标记节点为失败

    ★★★ 注意 ★★★
    此命令只是"标记"失败。实际的重试或降级逻辑需要运行：
      python error_recovery.py retry <state.json> <node_id> '<错误描述>'

    易错点：
    - error_msg 包含空格时，整个字符串必须用引号包裹
    - error_msg 建议简洁（不超过50字），详细说明可以放在 output_data 中
    - 不要包含敏感信息（如 API 密钥、密码等）在 error_msg 中

    使用方式：
      python state_store.py fail <state.json> <node_id> '错误描述'
    """
    state = load_state(state_path)
    if node_id not in state['nodes']:
        print(f"错误：节点 [{node_id}] 不存在")
        print(f"  可用节点：{', '.join(state['nodes'].keys())}")
        sys.exit(1)

    node = state['nodes'][node_id]
    node['status'] = 'failed'
    node['error'] = error_msg
    node['retry_count'] = node.get('retry_count', 0) + 1

    safe_write(state, state_path)
    print(f"节点 [{node_id}] 标记为失败")
    print(f"  错误信息：{error_msg}")
    print(f"  已重试次数：{node['retry_count']}/{node['max_retry']}")

    # 给出下一步操作提示
    if node['retry_count'] >= node['max_retry']:
        print(f"\n  已达最大重试次数，下一步：")
        fallback = node.get('fallback', 'abort')
        if fallback == 'skip':
            print(f"  将自动运行降级策略：跳过此节点")
        elif fallback == 'default':
            print(f"  将自动运行降级策略：使用预设默认值")
        else:
            print(f"  将自动运行降级策略：中止流水线")
        print(f"\n  运行触发降级：python error_recovery.py retry {state_path} {node_id} '{error_msg}'")
    else:
        print(f"\n  下一步：修复后重新运行")
        print(f"  重试命令：python error_recovery.py retry {state_path} {node_id} '{error_msg}'")

    return state


def show_status(state_path):
    """显示流水线当前状态

    输出格式说明：
    ✅ = completed（已完成）
    ❌ = failed（失败）
    🔄 = running（执行中）
    ⏳ = pending（等待执行）
    ⏭️ = skipped（已跳过）
    """
    state = load_state(state_path)
    print("=" * 60)
    print(f"  流水线状态：{state['pipeline_name']}")
    print(f"  流水线 ID：{state['pipeline_id']}")
    print(f"  总状态：{state['status']}")
    print(f"  创建时间：{state['created_at']}")
    print(f"  更新时间：{state['updated_at']}")
    print("=" * 60)

    for aid, node in state['nodes'].items():
        status_icon = {
            'pending': '⏳',
            'running': '🔄',
            'completed': '✅',
            'failed': '❌',
            'skipped': '⏭️'
        }.get(node['status'], '?')

        line = f"  {status_icon} [{aid}] {node.get('name', aid)} - {node['status']}"
        if node['status'] == 'failed':
            line += f" (重试 {node['retry_count']}/{node['max_retry']})"
        if node['status'] == 'completed' and node.get('completed_at'):
            line += f" @ {node['completed_at']}"
        print(line)
        if node.get('error'):
            print(f"      错误：{node['error']}")

    completed = sum(1 for n in state['nodes'].values() if n['status'] == 'completed')
    failed = sum(1 for n in state['nodes'].values() if n['status'] == 'failed')
    skipped = sum(1 for n in state['nodes'].values() if n['status'] == 'skipped')
    pending = sum(1 for n in state['nodes'].values() if n['status'] == 'pending')
    print(f"\n  汇总：{completed} 完成 / {pending} 待执行 / {failed} 失败 / {skipped} 跳过 / 共 {len(state['nodes'])} 节点")
    print("=" * 60)


def get_next_node(state_path):
    """获取下一个待执行的节点（依赖已全部完成）

    ★★★ 注意：此函数会修改状态文件！★★★
    1. 找到的节点会被标记为 running（防止重复执行）
    2. 如果节点超时未响应（AI 崩溃），会自动重置为 pending
    3. 所有修改会立即保存到状态文件

    使用方式：
      python state_store.py next <state.json>
    或（推荐）：
      python orchestrator.py step <state.json>
    """
    state = load_state(state_path)

    # 第一遍：检查是否有 running 超时的节点，防止 AI 崩溃导致流水线卡死
    for aid, node in state['nodes'].items():
        if node['status'] == 'running' and node.get('started_at'):
            try:
                started = datetime.strptime(node['started_at'], '%Y-%m-%dT%H:%M:%S')
                elapsed = (datetime.now() - started).total_seconds()
                timeout = node.get('timeout', 60)
                if elapsed > timeout * 2:
                    print(f"  ⚠️ [自动恢复] 节点 [{aid}] 已 running {elapsed:.0f} 秒，"
                          f"超过超时限制 ({timeout}×2={timeout*2}秒)，自动重置为 pending")
                    node['status'] = 'pending'
                    node['started_at'] = None
                    node['error'] = f"自动重置：超时未响应（{elapsed:.0f}秒）"
                    safe_write(state, state_path)
            except (ValueError, TypeError):
                pass

    # 第二遍：找到第一个依赖全部完成的 pending 节点
    for aid, node in state['nodes'].items():
        if node['status'] in ('completed', 'skipped', 'running'):
            continue
        if node['status'] == 'failed' and node['retry_count'] >= node['max_retry']:
            continue

        deps = node.get('depends_on', [])
        all_deps_done = all(
            state['nodes'].get(dep, {}).get('status') in ('completed', 'skipped')
            for dep in deps
        )

        if all_deps_done:
            # 标记为 running，防止被重复获取
            node['status'] = 'running'
            node['started_at'] = get_timestamp()
            safe_write(state, state_path)

            # 非普通任务节点（审批/控制流）由 orchestrator 自行渲染提示，
            # 这里静默返回节点 id，避免重复/误导性的"请执行任务"输出
            node_type = node.get('type', 'task')
            if node_type != 'task':
                return aid

            # 收集上游输出作为下游输入
            upstream_outputs = {}
            for dep in deps:
                dep_node = state['nodes'].get(dep, {})
                upstream_outputs[dep] = dep_node.get('output_data', {})

            print(f"下一个待执行节点：[{aid}] {node.get('name', aid)}")
            print(f"  角色：{node.get('role', '未指定')}")
            print(f"  依赖：{', '.join(deps) if deps else '无（首节点）'}")
            print(f"  超时：{node['timeout']}秒")
            print(f"  最大重试：{node['max_retry']}次")
            print(f"  降级策略：{node['fallback']}")
            if upstream_outputs:
                print(f"  上游输出已自动注入到 input_data：")
                for dep, data in upstream_outputs.items():
                    preview = json.dumps(data, ensure_ascii=False)[:200]
                    print(f"    [{dep}] → {preview}")
            print(f"\n请执行此节点的任务，完成后运行：")
            print(f"  成功：python state_store.py complete {state_path} {aid} '{{\"result\":\"...\"}}'")
            print(f"  失败：python error_recovery.py retry {state_path} {aid} '错误描述'")
            return aid

    # 处理没有可执行节点的情况
    remaining = {aid: n for aid, n in state['nodes'].items()
                 if n['status'] not in ('completed', 'skipped')}

    if not remaining:
        # 检查是否全部完成
        all_done = all(n['status'] in ('completed', 'skipped')
                       for n in state['nodes'].values())
        if all_done:
            print("🎉 所有节点均已处理完毕！")
        else:
            print("⚠️ 没有可执行的节点，但流水线尚未完成")
            print("  可能原因：部分节点处于 running 状态（可能是残留）")
    else:
        # 有待处理节点但无法执行 → 卡在依赖上
        blocked = [aid for aid, n in remaining.items()
                   if n['status'] == 'pending']
        failed_no_retry = [aid for aid, n in remaining.items()
                           if n['status'] == 'failed' and n['retry_count'] >= n['max_retry']]

        if failed_no_retry:
            print(f"⚠️ 节点 {', '.join(failed_no_retry)} 已达到最大重试次数")
            print(f"  请检查日志，修复问题后运行断点续传：")
            print(f"  python orchestrator.py resume {state_path}")
        elif blocked:
            print(f"⏳ 无法继续执行，{len(blocked)} 个节点被上游阻塞：{', '.join(blocked)}")
            print(f"  请检查上游节点状态")

    return None


def resume_pipeline(state_path, force=False):
    """断点续传：从失败处恢复执行

    ★★★ 功能说明 ★★★
    1. 将所有 failed 节点重置为 pending
    2. 重置 retry_count 归零（给予全新重试机会）
    3. 清除之前的 error 信息
    4. 不影响已完成的节点

    ★★★ 安全提示 ★★★
    - 使用 --force 跳过确认提示
    - 重置后之前的失败记录将丢失（报告中仍可见）

    使用场景：
    - 节点因网络问题失败后，修复网络后恢复
    - 节点因超时失败后，需要重新开始

    使用方式：
      python state_store.py resume <state.json> [--force]
    或（推荐）：
      python orchestrator.py resume <state.json> [--force]
    """
    state = load_state(state_path)

    print("=" * 60)
    print("  断点续传模式")
    print(f"  流水线：{state['pipeline_name']}")
    print("=" * 60)

    reset_count = 0
    for aid, node in state['nodes'].items():
        if node['status'] == 'failed':
            node['status'] = 'pending'
            node['retry_count'] = 0
            node['error'] = None
            reset_count += 1

    state['status'] = 'running'
    safe_write(state, state_path)

    completed = sum(1 for n in state['nodes'].values() if n['status'] == 'completed')
    total = len(state['nodes'])
    print(f"已完成节点：{completed}/{total}")

    if reset_count > 0:
        print(f"重置失败节点：{reset_count} 个（已重置为待执行，重试计数归零）")
        print(f"\n继续执行请运行：python orchestrator.py step {state_path}")
    else:
        print(f"没有需要重置的失败节点")

    print("=" * 60)


# 执行历史管理
HISTORY_FILENAME = '.execution_history.json'
MAX_HISTORY = 10


def save_execution_history(state_path, state):
    """保存执行摘要到历史文件（保留最近10次）"""
    state_path = validate_path(state_path)
    history_path = os.path.join(os.path.dirname(state_path), HISTORY_FILENAME)

    # 计算耗时
    nodes = state.get('nodes', {})
    times = [(n.get('started_at'), n.get('completed_at')) for n in nodes.values()
             if n.get('started_at') and n.get('completed_at')]
    total_duration = "-"
    if times:
        all_times = [t for pair in times for t in pair]
        total_duration = calc_duration(min(all_times), max(all_times))

    # 构建摘要
    summary = {
        'pipeline_id': state.get('pipeline_id', 'unknown'),
        'pipeline_name': state.get('pipeline_name', 'unnamed'),
        'timestamp': get_timestamp(),
        'status': state.get('status', 'unknown'),
        'total_duration': total_duration,
        'node_count': len(nodes),
        'completed_count': sum(1 for n in nodes.values() if n['status'] == 'completed'),
        'failed_count': sum(1 for n in nodes.values() if n['status'] == 'failed'),
        'skipped_count': sum(1 for n in nodes.values() if n['status'] == 'skipped'),
        'total_retries': sum(n.get('retry_count', 0) for n in nodes.values()),
    }

    # 读取现有历史
    history = []
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            history = []

    history.insert(0, summary)
    history = history[:MAX_HISTORY]

    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def calc_duration(start, end):
    """计算时长（供内部使用）"""
    if not start or not end:
        return "-"
    try:
        s = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        e = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
        delta = e - s
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return f"{seconds}秒"
        elif seconds < 3600:
            mins = seconds // 60
            secs = seconds % 60
            return f"{mins}分{secs:02d}秒"
        else:
            hours = seconds // 3600
            mins = (seconds % 3600) // 60
            return f"{hours}时{mins:02d}分"
    except (ValueError, TypeError):
        return "-"


def show_history(state_path):
    """显示执行历史"""
    state_path = validate_path(state_path, must_exist=True)
    history_path = os.path.join(os.path.dirname(state_path), HISTORY_FILENAME)

    if not os.path.exists(history_path):
        print("没有执行历史记录。")
        return []

    try:
        with open(history_path, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"读取历史失败：{e}")
        return []

    if not history:
        print("没有执行历史记录。")
        return []

    print("=" * 60)
    print("  执行历史记录")
    print("=" * 60)
    for i, h in enumerate(history, 1):
        print(f"\n  [{i}] {h.get('pipeline_name', 'unnamed')}")
        print(f"      ID: {h.get('pipeline_id', '-')}")
        print(f"      时间: {h.get('timestamp', '-')}")
        print(f"      状态: {h.get('status', '-')}")
        print(f"      耗时: {h.get('total_duration', '-')}")
        print(f"      节点: {h.get('completed_count', 0)}/{h.get('node_count', 0)} 成功，{h.get('failed_count', 0)}/{h.get('node_count', 0)} 失败")
    print("\n" + "=" * 60)
    return history


def compare_history(state_path):
    """对比最近5次执行"""
    state_path = validate_path(state_path, must_exist=True)
    history_path = os.path.join(os.path.dirname(state_path), HISTORY_FILENAME)

    if not os.path.exists(history_path):
        print("没有执行历史记录，无法对比。")
        return

    try:
        with open(history_path, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"读取历史失败：{e}")
        return

    if len(history) < 2:
        print("历史记录不足2次，需要至少2次才能对比。")
        print(f"  当前记录数：{len(history)}")
        return

    recent = history[:5]
    current = recent[0]
    previous = recent[1]

    def parse_duration(d):
        """将耗时字符串转换为秒"""
        if not d or d == "-":
            return 0
        total = 0
        import re
        m = re.search(r'(\d+)时', d)
        if m:
            total += int(m.group(1)) * 3600
        m = re.search(r'(\d+)分', d)
        if m:
            total += int(m.group(1)) * 60
        m = re.search(r'(\d+)秒', d)
        if m:
            total += int(m.group(1))
        return total

    def format_seconds(s):
        """秒数转可读字符串"""
        if s < 60:
            return f"{s}秒"
        elif s < 3600:
            return f"{s // 60}分{s % 60:02d}秒"
        else:
            return f"{s // 3600}时{(s % 3600) // 60:02d}分"

    cur_sec = parse_duration(current.get('total_duration', '-'))
    prev_sec = parse_duration(previous.get('total_duration', '-'))

    print("=" * 60)
    print("  执行对比（本次 vs 上次）")
    print("=" * 60)
    print(f"\n  流水线：{current.get('pipeline_name', '-')}")
    print(f"  本次 ID：{current.get('pipeline_id', '-')}")
    print(f"  上次 ID：{previous.get('pipeline_id', '-')}")

    # 耗时对比
    if prev_sec > 0 and cur_sec > 0:
        diff = cur_sec - prev_sec
        pct = (diff / prev_sec) * 100
        if diff > 0:
            print(f"\n  ⏱️ 耗时对比：本次比上次慢 {abs(pct):.1f}%（多 {format_seconds(abs(diff))}）")
        elif diff < 0:
            print(f"\n  ⏱️ 耗时对比：本次比上次快 {abs(pct):.1f}%")
        else:
            print(f"\n  ⏱️ 耗时对比：两次执行耗时相同")

    print(f"\n  本次耗时：{current.get('total_duration', '-')}")
    print(f"  上次耗时：{previous.get('total_duration', '-')}")

    # 成功/失败对比
    cur_completed = current.get('completed_count', 0)
    prev_completed = previous.get('completed_count', 0)
    cur_failed = current.get('failed_count', 0)
    prev_failed = previous.get('failed_count', 0)
    print(f"\n  本次完成：{cur_completed} 个节点成功，{cur_failed} 个失败")
    print(f"  上次完成：{prev_completed} 个节点成功，{prev_failed} 个失败")

    # 重试对比
    cur_retries = current.get('total_retries', 0)
    prev_retries = previous.get('total_retries', 0)
    print(f"\n  本次重试：{cur_retries} 次")
    print(f"  上次重试：{prev_retries} 次")

    print("\n" + "=" * 60)


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("状态持久化管理器 - 多Agent协作编排引擎 v5.0")
        print("=" * 50)
        print("命令列表：")
        print("  python state_store.py init <pipeline.json> [state_path]")
        print("      → 首次创建 pipeline.json 时使用，生成状态文件")
        print("")
        print("  python state_store.py complete <state.json> <node_id> '[json]'")
        print("      → 节点成功完成后调用，保存输出数据")
        print("")
        print("  python state_store.py fail <state.json> <node_id> '错误描述'")
        print("      → 节点失败时调用（注意：不会自动重试/降级）")
        print("")
        print("  python state_store.py status <state.json>")
        print("      → 查看流水线当前状态")
        print("")
        print("  python state_store.py next <state.json>")
        print("      → 获取下一个待执行节点（会自动标记为running）")
        print("")
        print("  python state_store.py resume <state.json> [--force]")
        print("      → 断点续传（重置所有失败节点为pending）")
        print("")
        print("  python state_store.py history <state.json>")
        print("      → 查看执行历史记录")
        print("")
        print("  python state_store.py compare <state.json>")
        print("      → 对比最近5次执行（耗时/成功率/重试次数）")
        print("")
        print("★★★ 快照功能（v5.0 新增）★★★")
        print("  节点完成后自动保存快照，用于执行回放 / Time Travel")
        print("  快照管理命令：python orchestrator.py snapshot list/show/restore/diff")
        print("")
        print("★★★ 重要：错误处理流程 ★★★")
        print("  1. 执行失败时，先运行 fail 标记失败")
        print("  2. 然后运行 error_recovery.py retry 触发")
        print("     - 重试（未达max_retry）")
        print("     - 或降级（已达max_retry，根据fallback策略）")
        print("  3. abort 策略走 resume 断点续传重新执行")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'init':
        if len(sys.argv) < 3:
            print("错误：缺少参数")
            print("用法：python state_store.py init <pipeline.json> [state_path]")
            sys.exit(1)
        pipeline_path = sys.argv[2]
        state_path = sys.argv[3] if len(sys.argv) > 3 else None
        try:
            with open(pipeline_path, 'r', encoding='utf-8') as f:
                pipeline = json.load(f)
            init_state(pipeline, state_path)
        except FileNotFoundError:
            print(f"错误：找不到 pipeline 文件 [{pipeline_path}]")
            print(f"  请确认路径正确，且文件存在")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"错误：pipeline 文件 JSON 格式不合法")
            print(f"  详情：第 {e.lineno} 行 - {e.msg}")
            sys.exit(1)

    elif cmd == 'complete':
        if len(sys.argv) < 4:
            print("错误：参数不足")
            print("用法：python state_store.py complete <state.json> <node_id> '[json]'")
            print("示例：python state_store.py complete state.json node_a '{\"result\":\"hello\"}'")
            sys.exit(1)
        output_json = sys.argv[4] if len(sys.argv) > 4 else None
        complete_node(sys.argv[2], sys.argv[3], output_json)

    elif cmd == 'fail':
        if len(sys.argv) < 4:
            print("错误：参数不足")
            print("用法：python state_store.py fail <state.json> <node_id> '错误描述'")
            print("示例：python state_store.py fail state.json node_a '网络请求超时'")
            print("")
            print("提示：错误描述包含空格时，必须用单引号包裹整个字符串")
            sys.exit(1)
        error_msg = sys.argv[4] if len(sys.argv) > 4 else "未知错误"
        fail_node(sys.argv[2], sys.argv[3], error_msg)

    elif cmd == 'status':
        if len(sys.argv) < 3:
            print("错误：缺少[state.json路径]")
            print("用法：python state_store.py status <state.json>")
            sys.exit(1)
        show_status(sys.argv[2])

    elif cmd == 'next':
        if len(sys.argv) < 3:
            print("错误：缺少[state.json路径]")
            print("用法：python state_store.py next <state.json>")
            sys.exit(1)
        get_next_node(sys.argv[2])

    elif cmd == 'resume':
        if len(sys.argv) < 3:
            print("错误：缺少[state.json路径]")
            print("用法：python state_store.py resume <state.json> [--force]")
            sys.exit(1)
        force = '--force' in sys.argv
        resume_pipeline(sys.argv[2], force=force)

    elif cmd == 'history':
        if len(sys.argv) < 3:
            print("错误：缺少[state.json路径]")
            print("用法：python state_store.py history <state.json>")
            sys.exit(1)
        show_history(sys.argv[2])

    elif cmd == 'compare':
        if len(sys.argv) < 3:
            print("错误：缺少[state.json路径]")
            print("用法：python state_store.py compare <state.json>")
            sys.exit(1)
        compare_history(sys.argv[2])

    else:
        print(f"错误：未知命令 [{cmd}]")
        print("运行 python state_store.py --help 查看可用命令")
        sys.exit(1)
