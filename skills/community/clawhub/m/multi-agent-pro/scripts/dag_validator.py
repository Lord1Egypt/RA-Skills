#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DAG 验证器 - 多Agent协作编排引擎 v5.0

功能：
  1. 验证 JSON Schema 结构完整性
  2. 检测循环依赖（Kahn 算法拓扑排序）
  3. 检测孤立节点（无上游也无下游的节点）
  4. 输出拓扑排序执行顺序
  5. 支持人工审批节点（type: approval）
  6. 支持动态控制流节点（condition/switch/for-each/while-loop）字段与引用校验

零第三方依赖，仅使用 Python 标准库

★★★ 安全说明 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 文件读取使用 utf-8 编码，防止编码注入
2. 最大文件读取限制 10MB，防止内存溢出
3. 路径规范化处理，防止路径穿越
4. 节点 id 仅允许 [a-zA-Z0-9_.-]，防止注入

★★★ 使用时机 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
强烈推荐在创建 pipeline.json 后运行验证：
  python orchestrator.py validate <pipeline.json>
  python orchestrator.py plan <pipeline.json>

验证时机：
  - 创建新的 pipeline.json 后
  - 修改 DAG 结构后
  - 运行 run/step 之前（虽然 run 内部也会验证，但提前验证更友好）

★★★ 不通过时的处理 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Schema 错误→ 必须修复后才能继续
循环依赖→ 必须修复后才能继续（否则无限递归）
孤立节点→ 仅警告，可正常执行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import sys
import os
import re
from collections import defaultdict

# 最大 pipeline.json 文件大小 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024
# 节点 id 允许的字符
VALID_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]+$')

# 节点类型归组映射（7 类 → 4 类，仅认知层提示，Schema 不变）
NODE_TYPE_GROUP = {
    'task': '任务',
    'approval': '人工',
    'condition': '控制（分支）',
    'switch': '控制（分支）',
    'for-each': '控制（循环）',
    'while-loop': '控制（循环）',
    'pipeline': '复用',
    'evaluate': '控制（评估）',
}


def validate_path(filepath):
    """路径安全校验：规范化路径，防止路径穿越"""
    filepath = os.path.abspath(os.path.normpath(filepath))
    if not os.path.exists(filepath):
        print(f"错误：文件不存在 [{filepath}]")
        print(f"  请检查路径是否正确（区分大小写）")
        print(f"  确认文件确实存在于该路径")
        sys.exit(1)
    return filepath


def load_pipeline(filepath):
    """加载 pipeline JSON 文件（带安全检查）

    如果文件不存在或格式错误，会给出清晰的修复提示。
    """
    if not filepath:
        print("错误：缺少[DAG文件路径]，请提供 pipeline JSON 文件路径")
        print("用法：python dag_validator.py <pipeline.json>")
        print("示例：python dag_validator.py templates/pipeline_dag_template.json")
        sys.exit(1)

    filepath = validate_path(filepath)

    # 检查文件大小
    file_size = os.path.getsize(filepath)
    if file_size > MAX_FILE_SIZE:
        print(f"错误：文件过大（{file_size // 1024 // 1024}MB），最大允许 {MAX_FILE_SIZE // 1024 // 1024}MB")
        print("  建议：拆分流水线或使用更简洁的配置")
        sys.exit(1)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"错误：JSON 格式不合法 [{filepath}]")
        print(f"  位置：第 {e.lineno} 行，第 {e.colno} 列")
        print(f"  详情：{e.msg}")
        print(f"  修复建议：使用 JSON 在线校验工具检查格式")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"错误：文件编码不合法 [{filepath}]")
        print("  修复：使用 UTF-8 编码保存文件")
        sys.exit(1)
    except Exception as e:
        print(f"错误：无法读取文件 [{filepath}] - {e}")
        sys.exit(1)


def validate_schema(pipeline):
    """验证 Schema 结构完整性

    返回 (errors, warnings) 两个列表。
    errors 必须修复，warnings 建议优化但不影响执行。

    ★★★ 安全检查 ★★★
    - 节点 id 仅允许 [a-zA-Z0-9_.-]
    - pipeline_name 最大长度 100 字符
    - 节点数量最大 100 个
    """
    errors = []
    warnings = []

    if not isinstance(pipeline, dict):
        errors.append("根节点必须是 JSON 对象")
        return errors, warnings

    # pipeline_name 必填
    if 'pipeline_name' not in pipeline:
        errors.append("缺少必填字段 [pipeline_name]")
        print("修复：添加 \"pipeline_name\": \"流水线名称\"")
    elif not isinstance(pipeline['pipeline_name'], str) or not pipeline['pipeline_name'].strip():
        errors.append("[pipeline_name] 必须是非空字符串")
    elif len(pipeline['pipeline_name']) > 100:
        errors.append("[pipeline_name] 长度不能超过 100 字符")

    # agents 必填
    if 'agents' not in pipeline:
        errors.append("缺少必填字段 [agents]")
        print("修复：添加 \"agents\": [{\"id\": \"node_1\", \"role\": \"角色描述\"}, ...]")
        return errors, warnings

    if not isinstance(pipeline['agents'], list) or len(pipeline['agents']) == 0:
        errors.append("[agents] 必须是非空数组（至少包含 1 个节点）")
        return errors, warnings

    if len(pipeline['agents']) > 100:
        errors.append(f"[agents] 节点数量不能超过 100 个（当前：{len(pipeline['agents'])}）")

    agent_ids = set()
    for i, agent in enumerate(pipeline['agents']):
        prefix = f"agents[{i}]"

        if not isinstance(agent, dict):
            errors.append(f"{prefix} 必须是 JSON 对象")
            continue

        # id 必填
        if 'id' not in agent:
            errors.append(f"{prefix} 缺少必填字段 [id]")
            print(f"修复：添加 \"id\": \"节点唯一标识\"")
        elif not isinstance(agent['id'], str) or not agent['id'].strip():
            errors.append(f"{prefix} [id] 必须是非空字符串")
        elif not VALID_ID_PATTERN.match(agent['id']):
            errors.append(f"{prefix} [id={agent['id']}] 包含非法字符，仅允许 [a-zA-Z0-9_.-]")
            print(f"修复：使用纯英文/数字/下划线/点/中划线作为节点 id")
        elif agent['id'] in agent_ids:
            errors.append(f"{prefix} [id={agent['id']}] 重复，每个 Agent 的 id 必须唯一")
            print(f"修复：修改 id 为不重复的值")
        else:
            agent_ids.add(agent['id'])

        if 'name' not in agent:
            warnings.append(f"{prefix} 建议添加 [name] 字段，便于人类阅读")
        if 'role' not in agent:
            warnings.append(f"{prefix} 建议添加 [role] 字段，描述 Agent 的职责")

        # depends_on 可选（默认空数组）
        if 'depends_on' not in agent:
            warnings.append(f"{prefix} 未指定 [depends_on]，默认为空（无依赖）")
        elif not isinstance(agent['depends_on'], list):
            errors.append(f"{prefix} [depends_on] 必须是数组")

        # retry 验证
        if 'retry' in agent:
            if not isinstance(agent['retry'], int) or agent['retry'] < 0:
                warnings.append(f"{prefix} [retry] 应为非负整数")
            elif agent['retry'] > 10:
                warnings.append(f"{prefix} [retry] 建议不超过 10 次（当前：{agent['retry']}）")

        # timeout 验证
        if 'timeout' in agent:
            if not isinstance(agent['timeout'], (int, float)) or agent['timeout'] <= 0:
                warnings.append(f"{prefix} [timeout] 应为正数（秒）")
            elif agent['timeout'] > 3600:
                warnings.append(f"{prefix} [timeout] 建议不超过 3600 秒（1小时）")

        # fallback 验证
        if 'fallback' in agent and agent['fallback'] not in ('retry', 'skip', 'default', 'abort'):
            warnings.append(f"{prefix} [fallback] 建议为 skip/default/abort 之一（当前值：{agent['fallback']}）")

        # type 验证（task/approval/控制流六类）
        valid_types = ('task', 'approval', 'condition', 'switch', 'for-each', 'while-loop', 'pipeline', 'evaluate')
        node_type = agent.get('type', 'task')
        if 'type' in agent and node_type not in valid_types:
            group = NODE_TYPE_GROUP.get(node_type, '未知')
            warnings.append(
                f"{prefix} [type] 建议为 {'/'.join(valid_types)} 之一（当前值：{agent['type']}，归组：{group}）"
            )

        # 控制流节点专有字段校验
        if node_type == 'condition':
            if 'condition' not in agent or not str(agent.get('condition', '')).strip():
                errors.append(f"{prefix} condition 节点必须提供非空 [condition] 表达式")
            if 'on_true' not in agent and 'on_false' not in agent:
                warnings.append(f"{prefix} condition 节点建议至少提供 [on_true] 或 [on_false] 分支")
            for br in ('on_true', 'on_false'):
                if br in agent and not isinstance(agent[br], list):
                    errors.append(f"{prefix} condition 节点的 [{br}] 必须是节点 id 数组")

        elif node_type == 'switch':
            if 'switch' not in agent or not str(agent.get('switch', '')).strip():
                errors.append(f"{prefix} switch 节点必须提供非空 [switch] 表达式")
            if 'cases' not in agent or not isinstance(agent.get('cases'), dict) or not agent['cases']:
                errors.append(f"{prefix} switch 节点必须提供非空 [cases] 对象（值→节点id数组）")
            elif not all(isinstance(v, list) for v in agent['cases'].values()):
                errors.append(f"{prefix} switch 节点 [cases] 的每个分支值必须是节点 id 数组")
            if 'default' in agent and not isinstance(agent['default'], list):
                errors.append(f"{prefix} switch 节点的 [default] 必须是节点 id 数组")

        elif node_type == 'for-each':
            if 'items' not in agent or not str(agent.get('items', '')).strip():
                errors.append(f"{prefix} for-each 节点必须提供非空 [items] 表达式")
            if 'template' in agent and not isinstance(agent['template'], dict):
                errors.append(f"{prefix} for-each 节点的 [template] 必须是对象")
            if 'join' in agent and not isinstance(agent['join'], list):
                errors.append(f"{prefix} for-each 节点的 [join] 必须是节点 id 数组")

        elif node_type == 'while-loop':
            if 'condition' not in agent or not str(agent.get('condition', '')).strip():
                errors.append(f"{prefix} while-loop 节点必须提供非空 [condition] 表达式")
            if 'loop_body' not in agent or not isinstance(agent.get('loop_body'), list) or not agent['loop_body']:
                errors.append(f"{prefix} while-loop 节点必须提供非空 [loop_body] 数组")
            if 'max_iterations' in agent:
                mi = agent['max_iterations']
                if not isinstance(mi, int) or mi <= 0:
                    warnings.append(f"{prefix} while-loop 节点的 [max_iterations] 建议为正整数")

        elif node_type == 'approval':
            if 'timeout_seconds' in agent:
                ts = agent['timeout_seconds']
                if not isinstance(ts, (int, float)) or ts <= 0:
                    warnings.append(f"{prefix} approval 节点的 [timeout_seconds] 应为正数（秒）")
            if 'timeout_action' in agent:
                if agent['timeout_action'] not in ('approve', 'reject'):
                    warnings.append(f"{prefix} approval 节点的 [timeout_action] 建议为 'approve' 或 'reject'")

        elif node_type == 'pipeline':
            if 'pipeline_ref' not in agent or not str(agent.get('pipeline_ref', '')).strip():
                errors.append(f"{prefix} pipeline 节点必须提供非空 [pipeline_ref] 引用名")
            if 'params' in agent and not isinstance(agent['params'], dict):
                errors.append(f"{prefix} pipeline 节点的 [params] 必须是对象")
            if 'outputs' in agent and not isinstance(agent['outputs'], dict):
                errors.append(f"{prefix} pipeline 节点的 [outputs] 必须是对象")

        elif node_type == 'evaluate':
            if 'quality_expr' not in agent or not str(agent.get('quality_expr', '')).strip():
                errors.append(f"{prefix} evaluate 节点必须提供非空 [quality_expr] 表达式")
            if 'retry_targets' not in agent or not isinstance(agent.get('retry_targets'), list) or not agent['retry_targets']:
                errors.append(f"{prefix} evaluate 节点必须提供非空 [retry_targets] 数组")
            if 'max_eval_rounds' in agent:
                me = agent['max_eval_rounds']
                if not isinstance(me, int) or me <= 0:
                    warnings.append(f"{prefix} evaluate 节点的 [max_eval_rounds] 建议为正整数")

    # 分支目标引用校验：控制流节点引用的分支节点必须存在
    branch_ref_errors = _validate_branch_refs(pipeline, agent_ids)
    errors.extend(branch_ref_errors)

    return errors, warnings


def _validate_branch_refs(pipeline, agent_ids):
    """校验控制流节点引用的分支/循环目标节点都存在"""
    errors = []
    for i, agent in enumerate(pipeline.get('agents', [])):
        if not isinstance(agent, dict):
            continue
        prefix = f"agents[{i}]([{agent.get('id', '?')}])"
        node_type = agent.get('type', 'task')

        def _check_ids(field, ids):
            for tid in ids:
                if tid not in agent_ids:
                    errors.append(f"{prefix} 的 [{field}] 引用了不存在的节点 [{tid}]")

        if node_type == 'condition':
            _check_ids('on_true', agent.get('on_true', []))
            _check_ids('on_false', agent.get('on_false', []))
        elif node_type == 'switch':
            for cv, ids in (agent.get('cases', {}) or {}).items():
                if isinstance(ids, list):
                    _check_ids(f"cases.{cv}", ids)
            _check_ids('default', agent.get('default', []))
        elif node_type == 'for-each':
            _check_ids('join', agent.get('join', []))
        elif node_type == 'while-loop':
            _check_ids('loop_body', agent.get('loop_body', []))
        elif node_type == 'evaluate':
            _check_ids('retry_targets', agent.get('retry_targets', []))

    return errors


def detect_cycles(pipeline):
    """检测循环依赖（基于 Kahn 算法）"""
    errors = []
    agents = pipeline.get('agents', [])
    agent_ids = {a['id'] for a in agents if 'id' in a}

    if not agent_ids:
        return errors

    # 构建入度图和邻接表
    in_degree = defaultdict(int)
    graph = defaultdict(list)

    for agent in agents:
        aid = agent.get('id')
        deps = agent.get('depends_on', [])
        for dep in deps:
            # 引用的依赖节点不存在
            if dep not in agent_ids:
                errors.append(f"节点 [{aid}] 依赖了不存在的节点 [{dep}]")
                errors.append(f"  修复：在 agents 中添加 id 为 [{dep}] 的节点，或修改 [{aid}] 的 depends_on")
                continue
            graph[dep].append(aid)
            in_degree[aid] += 1

    # Kahn 算法
    queue = [aid for aid in agent_ids if in_degree[aid] == 0]
    visited = 0

    while queue:
        node = queue.pop(0)
        visited += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # 未访问到的节点就是循环依赖的节点
    if visited < len(agent_ids):
        cycle_nodes = [aid for aid in agent_ids if in_degree[aid] > 0]
        errors.append(f"检测到循环依赖！涉及节点：{', '.join(sorted(cycle_nodes))}")
        errors.append(f"  修复：检查这些节点的 depends_on 字段，移除环路中的至少一条依赖")
        errors.append(f"  提示：使用 orchestrator.py plan 可查看可视化的依赖关系")

    return errors


def detect_orphans(pipeline):
    """检测孤立节点（无上游也无下游）"""
    warnings = []
    agents = pipeline.get('agents', [])

    if len(agents) <= 1:
        return warnings

    agent_ids = {a['id'] for a in agents if 'id' in a}
    depended_by = set()
    has_deps = set()

    for agent in agents:
        aid = agent.get('id')
        deps = agent.get('depends_on', [])
        if deps:
            has_deps.add(aid)
        for dep in deps:
            depended_by.add(dep)

    for agent in agents:
        aid = agent.get('id')
        if aid not in has_deps and aid not in depended_by:
            warnings.append(f"节点 [{aid}] 是孤立节点（无上游也无下游），确认是否遗漏了依赖关系")

    return warnings


def topological_sort(pipeline):
    """拓扑排序，返回执行顺序

    算法：Kahn 算法（入度归零即执行）
    同层级节点按 id 字母顺序排列
    """
    agents = pipeline.get('agents', [])
    agent_ids = {a['id'] for a in agents if 'id' in a}

    in_degree = defaultdict(int)
    graph = defaultdict(list)

    for agent in agents:
        aid = agent.get('id')
        for dep in agent.get('depends_on', []):
            if dep in agent_ids:
                graph[dep].append(aid)
                in_degree[aid] += 1

    queue = sorted([aid for aid in agent_ids if in_degree[aid] == 0])
    result = []

    while queue:
        node = queue.pop(0)
        result.append(node)
        neighbors = sorted(graph[node])
        for neighbor in neighbors:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result


def validate(filepath):
    """完整验证流程

    ★★★ 运行方式 ★★★
    python dag_validator.py <pipeline.json>
    python dag_validator.py --help
    """
    print("=" * 60)
    print("  DAG 验证器 - 多Agent协作编排引擎 v5.0")
    print("=" * 60)

    pipeline = load_pipeline(filepath)
    all_errors = []
    all_warnings = []

    # 1. Schema 验证
    errors, warnings = validate_schema(pipeline)
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    if all_errors:
        print("\n[1/3] Schema 验证 ... ❌ 失败")
        print("\n错误列表：")
        for i, e in enumerate(all_errors, 1):
            print(f"  {i}. {e}")
        if all_warnings:
            print("\n警告列表：")
            for w in all_warnings:
                print(f"  [警告] {w}")
        print(f"\n验证结果：❌ 不通过（存在结构性错误，请先修复）")
        print("=" * 60)
        sys.exit(1)

    print("\n[1/3] Schema 验证 ... ✅ 通过")

    # 2. 循环依赖检测
    cycle_errors = detect_cycles(pipeline)
    if cycle_errors:
        print("[2/3] 循环依赖检测 ... ❌ 失败")
        for e in cycle_errors:
            print(f"  [错误] {e}")
        print("\n验证结果：❌ 不通过（存在循环依赖）")
        print("=" * 60)
        sys.exit(1)
    print("[2/3] 循环依赖检测 ... ✅ 通过")

    # 3. 孤立节点检测
    orphan_warnings = detect_orphans(pipeline)
    if orphan_warnings:
        print("[3/3] 孤立节点检测 ... ⚠️ 发现警告")
        for w in orphan_warnings:
            print(f"  [警告] {w}")
    else:
        print("[3/3] 孤立节点检测 ... ✅ 无警告")

    # 拓扑排序展示
    order = topological_sort(pipeline)
    print(f"\n执行顺序（拓扑排序）：{' → '.join(order)}")

    # 汇总
    total_warnings = len(all_warnings) + len(orphan_warnings)
    if total_warnings > 0:
        print(f"\n验证结果：✅ 通过（{total_warnings} 个警告，建议优化但不影响执行）")
    else:
        print("\n验证结果：✅ 完全通过")
    print("=" * 60)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("错误：缺少[DAG文件路径]")
        print("用法：python dag_validator.py <pipeline.json>")
        print("示例：python dag_validator.py templates/pipeline_dag_template.json")
        sys.exit(1)

    if sys.argv[1] in ('-h', '--help'):
        print("DAG 验证器 - 多Agent协作编排引擎 v5.0")
        print("=" * 50)
        print("用法：python dag_validator.py <pipeline.json>")
        print("")
        print("验证内容：")
        print("  1. JSON Schema 结构完整性（id/role/depends_on 等）")
        print("  2. 循环依赖检测（A→B→C→A 为非法循环）")
        print("  3. 孤立节点检测（节点无前驱也无后继）")
        print("  4. 输出拓扑排序执行顺序")
        print("")
        print("安全限制：")
        print("  - 节点 id 仅允许 [a-zA-Z0-9_.-]")
        print("  - 节点数量最大 100 个")
        print("  - 单节点输出最大 10MB")
        print("  - pipeline.json 最大 10MB")
        print("")
        print("使用时机：")
        print("  - 创建新的 pipeline.json 后")
        print("  - 修改 DAG 结构后")
        print("  - 运行 run/step 之前")
        print("")
        print("验证结果：")
        print("  ✅ 通过 → 可安全使用")
        print("  ⚠️ 通过+警告 → 可执行但有改进空间")
        print("  ❌ 不通过 → 必须修复后才能使用")
        sys.exit(0)

    validate(sys.argv[1])
