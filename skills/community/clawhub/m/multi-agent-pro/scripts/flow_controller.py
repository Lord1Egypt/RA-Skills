#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
控制流引擎 - 多Agent协作编排引擎 v5.2

功能：为静态 DAG 增加动态控制流能力，支持六类控制节点：
  1. condition  - if-else 条件分支（真假两路）
  2. switch     - 多路分支（按值匹配 case）
  3. for-each   - 动态节点生成（按列表长度展开子节点）
  4. while-loop - 循环 / 重试增强（条件为真则回环重跑循环体）
  5. pipeline   - 子流水线引用（调用已注册的子流水线，隔离执行）
  6. evaluate   - Self-Improving 质量评估（质量不达标自动重试目标节点）

控制节点由引擎自动求值执行（不交给 AI），执行后动态修改 state：
  - 未选中分支的节点 → 整体标记 skipped
  - for-each → 动态注入子节点并重挂下游依赖
  - while-loop → 满足条件则重置循环体节点为 pending 再跑一轮
  - pipeline → 隔离执行子流水线，结果映射回父上下文

零第三方依赖，仅使用 Python 标准库

★★★ 安全说明 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 条件求值全部走 condition_evaluator（AST 白名单，禁止 eval/函数调用）
2. for-each 展开数量上限 MAX_FANOUT，防止 items 过大导致节点爆炸
3. while-loop 迭代次数上限 max_iterations（硬上限 MAX_ITER），防止死循环
4. 所有 state 修改经 state_store.safe_write 原子落盘
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import state_store
import condition_evaluator
from condition_evaluator import ConditionError

# for-each 单次展开的子节点数量硬上限（防节点爆炸）
MAX_FANOUT = 100
# while-loop 迭代次数硬上限（即使配置更大也强制封顶，防死循环）
MAX_ITER = 1000

# 六类控制流节点类型
CONTROL_TYPES = ('condition', 'switch', 'for-each', 'while-loop', 'pipeline', 'evaluate')


def is_control_node(node):
    """判断节点是否为控制流节点"""
    return node.get('type') in CONTROL_TYPES


def _collect_descendants(state, start_ids):
    """收集给定节点集合的所有下游后代（含自身），用于分支整体跳过。

    仅在"分支封闭子图"内收集：沿 depends_on 反向图向下游遍历。
    """
    nodes = state['nodes']
    # 构建 依赖 -> 后继 的邻接表
    children = {nid: [] for nid in nodes}
    for nid, node in nodes.items():
        for dep in node.get('depends_on', []):
            if dep in children:
                children[dep].append(nid)

    result = set()
    stack = list(start_ids)
    while stack:
        cur = stack.pop()
        if cur in result:
            continue
        result.add(cur)
        for child in children.get(cur, []):
            stack.append(child)
    return result


def _mark_skipped(state, node_ids, reason=""):
    """将指定节点标记为 skipped（仅跳过尚未完成的节点）"""
    skipped = []
    for nid in node_ids:
        node = state['nodes'].get(nid)
        if not node:
            continue
        if node['status'] in ('completed', 'failed', 'skipped'):
            continue
        node['status'] = 'skipped'
        node['completed_at'] = state_store.get_timestamp()
        if reason:
            node['error'] = None
            node.setdefault('output_data', {})
            node['output_data']['_skipped_reason'] = reason
        skipped.append(nid)
    return skipped


# ============================================================
# 1. condition：if-else 条件分支
# ============================================================
def handle_condition(state, node_id, state_path):
    """处理 condition 节点（if-else 二路分支）。

    节点配置示例：
      {
        "id": "check_quality",
        "type": "condition",
        "condition": "nodes.review.output_data.score >= 60",
        "on_true": ["publish"],        # 条件为真走这些节点
        "on_false": ["rework"],        # 条件为假走这些节点
        "depends_on": ["review"]
      }
    未选中分支的节点（及其下游后代）整体标记 skipped。
    """
    node = state['nodes'][node_id]
    expr = node.get('condition')
    on_true = node.get('on_true', [])
    on_false = node.get('on_false', [])

    if not expr:
        raise ConditionError(f"condition 节点 [{node_id}] 缺少 'condition' 字段")

    ctx = condition_evaluator.build_context_from_state(state)
    result = condition_evaluator.evaluate_bool(expr, ctx)

    if result:
        chosen, dropped = on_true, on_false
        branch = "on_true"
    else:
        chosen, dropped = on_false, on_true
        branch = "on_false"

    # 跳过未选中分支（含下游后代，但不跳掉被选中分支也依赖的节点）
    keep = _collect_descendants(state, chosen) if chosen else set()
    drop_all = _collect_descendants(state, dropped) if dropped else set()
    to_skip = drop_all - keep - {node_id}
    skipped = _mark_skipped(state, to_skip, reason=f"condition [{node_id}] 走 {branch} 分支")

    node['status'] = 'completed'
    node['completed_at'] = state_store.get_timestamp()
    node['output_data'] = {
        'condition': expr,
        'result': result,
        'branch': branch,
        'chosen': chosen,
        'skipped': skipped,
    }
    if not node.get('started_at'):
        node['started_at'] = state_store.get_timestamp()

    state_store.safe_write(state, state_path)

    print(f"  🔀 condition [{node_id}] 求值：{expr}")
    print(f"     结果 = {result} → 走 {branch} 分支：{chosen or '（空）'}")
    if skipped:
        print(f"     已跳过分支节点：{', '.join(skipped)}")
    return True


# ============================================================
# 2. switch：多路分支
# ============================================================
def handle_switch(state, node_id, state_path):
    """处理 switch 节点（多路分支）。

    节点配置示例：
      {
        "id": "route_by_type",
        "type": "switch",
        "switch": "nodes.classify.output_data.category",
        "cases": {
          "urgent": ["fast_track"],
          "normal": ["standard"],
          "low": ["batch"]
        },
        "default": ["standard"],
        "depends_on": ["classify"]
      }
    命中 case 对应分支执行，其余分支整体 skipped。无命中走 default。
    """
    node = state['nodes'][node_id]
    expr = node.get('switch')
    cases = node.get('cases', {})
    default = node.get('default', [])

    if not expr:
        raise ConditionError(f"switch 节点 [{node_id}] 缺少 'switch' 字段")
    if not isinstance(cases, dict) or not cases:
        raise ConditionError(f"switch 节点 [{node_id}] 的 'cases' 必须是非空对象")

    ctx = condition_evaluator.build_context_from_state(state)
    value = condition_evaluator.evaluate(expr, ctx)
    # switch 值统一转字符串比较（JSON 键只能是字符串）
    value_key = str(value)

    if value_key in cases:
        chosen = cases[value_key]
        matched = value_key
    else:
        chosen = default
        matched = "default"

    # 所有 case 分支 + default 的并集，减去被选中的，即需跳过
    all_branch_ids = set()
    for ids in cases.values():
        all_branch_ids.update(_collect_descendants(state, ids))
    if default:
        all_branch_ids.update(_collect_descendants(state, default))

    keep = _collect_descendants(state, chosen) if chosen else set()
    to_skip = all_branch_ids - keep - {node_id}
    skipped = _mark_skipped(state, to_skip, reason=f"switch [{node_id}] 命中 {matched}")

    node['status'] = 'completed'
    node['completed_at'] = state_store.get_timestamp()
    node['output_data'] = {
        'switch': expr,
        'value': value,
        'matched': matched,
        'chosen': chosen,
        'skipped': skipped,
    }
    if not node.get('started_at'):
        node['started_at'] = state_store.get_timestamp()

    state_store.safe_write(state, state_path)

    print(f"  🔀 switch [{node_id}] 求值：{expr}")
    print(f"     值 = {value!r} → 命中 [{matched}] → 执行：{chosen or '（空）'}")
    if skipped:
        print(f"     已跳过其他分支：{', '.join(skipped)}")
    return True


# ============================================================
# 3. for-each：动态节点生成
# ============================================================
def handle_for_each(state, node_id, state_path):
    """处理 for-each 节点（按列表动态展开子节点）。

    节点配置示例：
      {
        "id": "process_files",
        "type": "for-each",
        "items": "nodes.scan.output_data.file_list",   # 求值得到一个列表
        "template": {                                    # 每个子节点的模板
          "role": "处理单个文件",
          "timeout": 60,
          "retry": 2
        },
        "join": ["merge_results"],                       # 汇合节点，改依赖所有子节点
        "depends_on": ["scan"]
      }
    展开为 process_files__0, process_files__1, ... 子任务节点。
    """
    node = state['nodes'][node_id]
    items_expr = node.get('items')
    template = node.get('template', {})
    join = node.get('join', [])

    if not items_expr:
        raise ConditionError(f"for-each 节点 [{node_id}] 缺少 'items' 字段")

    ctx = condition_evaluator.build_context_from_state(state)
    items = condition_evaluator.evaluate(items_expr, ctx)

    if not isinstance(items, (list, tuple)):
        raise ConditionError(
            f"for-each 节点 [{node_id}] 的 items 求值结果不是列表（得到 {type(items).__name__}）"
        )

    if len(items) > MAX_FANOUT:
        raise ConditionError(
            f"for-each 节点 [{node_id}] 展开数量 {len(items)} 超过上限 {MAX_FANOUT}，已拒绝"
        )

    # 生成子节点
    child_ids = []
    for idx, item in enumerate(items):
        child_id = f"{node_id}__{idx}"
        child_ids.append(child_id)
        state['nodes'][child_id] = {
            "name": f"{node.get('name', node_id)} #{idx}",
            "role": template.get('role', node.get('role', '')),
            "type": "task",
            "status": "pending",
            "depends_on": [node_id],
            "retry_count": 0,
            "max_retry": template.get('retry', 3),
            "timeout": template.get('timeout', 60),
            "fallback": template.get('fallback', 'abort'),
            "inputs": template.get('inputs', []),
            "outputs": template.get('outputs', []),
            "output_data": {},
            "item": item,                 # 当前迭代的数据项
            "item_index": idx,
            "error": None,
            "started_at": None,
            "completed_at": None,
            "_dynamic": True,             # 标记为动态生成节点
        }

    # 汇合节点改为依赖所有子节点（保留原有非本节点依赖）
    for jid in join:
        jnode = state['nodes'].get(jid)
        if not jnode:
            continue
        deps = [d for d in jnode.get('depends_on', []) if d != node_id]
        deps.extend(child_ids)
        jnode['depends_on'] = deps

    node['status'] = 'completed'
    node['completed_at'] = state_store.get_timestamp()
    node['output_data'] = {
        'items_count': len(items),
        'children': child_ids,
        'join': join,
    }
    if not node.get('started_at'):
        node['started_at'] = state_store.get_timestamp()

    state_store.safe_write(state, state_path)

    print(f"  🔁 for-each [{node_id}] 展开 {len(items)} 个子节点：")
    print(f"     {', '.join(child_ids) if child_ids else '（items 为空，无子节点）'}")
    if join:
        print(f"     汇合节点 {join} 已重挂到所有子节点")
    return True


# ============================================================
# 4. while-loop：循环 / 重试增强
# ============================================================
def handle_while_loop(state, node_id, state_path):
    """处理 while-loop 节点（循环守卫，放在循环体末尾）。

    节点配置示例：
      {
        "id": "loop_guard",
        "type": "while-loop",
        "condition": "nodes.check.output_data.passed == False",
        "loop_body": ["generate", "check"],   # 需重跑的循环体节点
        "max_iterations": 5,
        "depends_on": ["check"]
      }
    每轮求值 condition：
      - 为真且未达上限 → 重置 loop_body 节点为 pending，迭代 +1，继续循环
      - 为假或已达上限 → 循环结束，本节点 completed
    """
    node = state['nodes'][node_id]
    expr = node.get('condition')
    loop_body = node.get('loop_body', [])
    max_iter = node.get('max_iterations', 10)

    if not expr:
        raise ConditionError(f"while-loop 节点 [{node_id}] 缺少 'condition' 字段")
    if not loop_body:
        raise ConditionError(f"while-loop 节点 [{node_id}] 缺少 'loop_body' 字段")

    # 强制封顶，防死循环
    max_iter = min(int(max_iter), MAX_ITER)

    iteration = node.get('iteration', 0)
    ctx = condition_evaluator.build_context_from_state(state)
    should_loop = condition_evaluator.evaluate_bool(expr, ctx)

    if should_loop and iteration < max_iter:
        # 继续循环：重置循环体节点为 pending
        new_iter = iteration + 1
        for bid in loop_body:
            bnode = state['nodes'].get(bid)
            if not bnode:
                continue
            bnode['status'] = 'pending'
            bnode['started_at'] = None
            bnode['completed_at'] = None
            bnode['retry_count'] = 0
            bnode['error'] = None
            bnode['iteration'] = new_iter
        # 守卫自身也回到 pending，等循环体重跑完再次求值
        node['status'] = 'pending'
        node['started_at'] = None
        node['completed_at'] = None
        node['iteration'] = new_iter

        state_store.safe_write(state, state_path)
        print(f"  🔄 while-loop [{node_id}] 第 {new_iter}/{max_iter} 轮：条件为真，重跑循环体 {loop_body}")
        return True
    else:
        # 循环结束
        reason = "条件为假" if not should_loop else f"已达最大迭代 {max_iter} 轮"
        node['status'] = 'completed'
        node['completed_at'] = state_store.get_timestamp()
        node['output_data'] = {
            'condition': expr,
            'iterations': iteration,
            'stopped_reason': reason,
        }
        if not node.get('started_at'):
            node['started_at'] = state_store.get_timestamp()

        state_store.safe_write(state, state_path)
        print(f"  ✅ while-loop [{node_id}] 结束：{reason}（共 {iteration} 轮）")
        return True


# ============================================================
# 5. pipeline：子流水线引用
# ============================================================
def handle_pipeline(state, node_id, state_path):
    """处理 pipeline 节点（子流水线引用）。

    节点配置示例：
      {
        "id": "invoice_step",
        "name": "发票处理子流水线",
        "type": "pipeline",
        "pipeline_ref": "invoice-pipeline-v2",
        "params": {
          "file_path": "nodes.scan.output_data.file"
        },
        "outputs": {
          "invoice_no": "nodes._terminal_.output_data.invoice_no"
        },
        "depends_on": ["scan"]
      }
    子流水线在隔离 state 中执行，只有 outputs 映射的字段能透出到父上下文。
    """
    import pipeline_registry

    node = state['nodes'][node_id]
    ref = node.get('pipeline_ref')
    params_expr = node.get('params', {})
    outputs_expr = node.get('outputs', {})

    if not ref:
        raise ConditionError(f"pipeline 节点 [{node_id}] 缺少 'pipeline_ref' 字段")

    # 查找子流水线
    meta = pipeline_registry.resolve(ref)
    if not meta:
        raise ConditionError(
            f"pipeline 节点 [{node_id}] 引用了未注册的子流水线 [{ref}]\n"
            f"  修复：运行 python pipeline_registry.py list 查看已注册的子流水线"
        )

    # 加载子流水线定义
    sub_path = meta.get('path')
    if not os.path.exists(sub_path):
        raise ConditionError(f"子流水线文件不存在：{sub_path}")

    with open(sub_path, 'r', encoding='utf-8') as f:
        sub_pipeline = json.load(f)

    # 创建隔离 state（子流水线独立运行）
    sub_state_path = os.path.join(
        os.path.dirname(state_path),
        f"state_{node_id}_sub.json"
    )
    sub_state, sub_state_path = state_store.init_state(sub_pipeline, sub_state_path)

    # 注入父上下文参数到子流水线首节点
    if params_expr:
        ctx = condition_evaluator.build_context_from_state(state)
        # 找到子流水线首节点（无依赖的节点）
        first_nodes = [a for a in sub_pipeline.get('agents', [])
                       if not a.get('depends_on')]
        if first_nodes:
            first_nid = first_nodes[0]['id']
            for param_name, expr in params_expr.items():
                value = condition_evaluator.evaluate(expr, ctx)
                sub_state['nodes'][first_nid]['output_data'][param_name] = value
                sub_state['nodes'][first_nid]['status'] = 'completed'
        state_store.safe_write(sub_state, sub_state_path)

    # 执行子流水线（复用 orchestrator.step 机制）
    # 简化：直接逐步执行子流水线的所有节点
    max_sub_steps = 500
    for _ in range(max_sub_steps):
        nid = state_store.get_next_node(sub_state_path)
        if not nid:
            break
        st = state_store.load_state(sub_state_path)
        snode = st['nodes'][nid]
        if is_control_node(snode):
            process_control_node(st, nid, sub_state_path)
        else:
            # 子流水线节点自动完成（模拟执行）
            state_store.complete_node(sub_state_path, nid,
                                      json.dumps({"result": f"{nid}_done"}, ensure_ascii=False))

    # 映射 outputs 回父上下文
    sub_state = state_store.load_state(sub_state_path)
    ctx = condition_evaluator.build_context_from_state(sub_state)
    mapped_outputs = {}
    for out_name, expr in outputs_expr.items():
        try:
            mapped_outputs[out_name] = condition_evaluator.evaluate(expr, ctx)
        except ConditionError:
            mapped_outputs[out_name] = None

    node['status'] = 'completed'
    node['completed_at'] = state_store.get_timestamp()
    node['output_data'] = {
        'pipeline_ref': ref,
        'sub_state_path': sub_state_path,
        'outputs': mapped_outputs,
    }
    if not node.get('started_at'):
        node['started_at'] = state_store.get_timestamp()

    state_store.safe_write(state, state_path)

    print(f"  📦 pipeline [{node_id}] 执行子流水线 [{ref}]")
    print(f"     子流水线 state：{sub_state_path}")
    print(f"     映射输出：{json.dumps(mapped_outputs, ensure_ascii=False)[:200]}")
    return True


# ============================================================
# 6. evaluate：Self-Improving 质量评估
# ============================================================
def handle_evaluate(state, node_id, state_path):
    """处理 evaluate 节点（Self-Improving 质量评估 + 自动重试）。

    节点配置示例：
      {
        "id": "quality_check",
        "type": "evaluate",
        "quality_expr": "nodes.review.output_data.score >= 80",
        "retry_targets": ["draft", "review"],   # 质量不达标时重跑的节点
        "max_eval_rounds": 3,
        "depends_on": ["review"]
      }
    质量评估：
      - quality_expr 为真 → 质量达标，节点 completed
      - quality_expr 为假且未达上限 → 重置 retry_targets 为 pending，迭代 +1
      - quality_expr 为假且已达上限 → 接受当前结果，节点 completed（带警告）
    """
    node = state['nodes'][node_id]
    quality_expr = node.get('quality_expr')
    retry_targets = node.get('retry_targets', [])
    max_rounds = node.get('max_eval_rounds', 3)

    if not quality_expr:
        raise ConditionError(f"evaluate 节点 [{node_id}] 缺少 'quality_expr' 字段")
    if not retry_targets:
        raise ConditionError(f"evaluate 节点 [{node_id}] 缺少 'retry_targets' 字段")

    max_rounds = min(int(max_rounds), MAX_ITER)
    eval_round = node.get('eval_round', 0)

    ctx = condition_evaluator.build_context_from_state(state)
    quality_ok = condition_evaluator.evaluate_bool(quality_expr, ctx)

    if quality_ok:
        node['status'] = 'completed'
        node['completed_at'] = state_store.get_timestamp()
        node['output_data'] = {
            'quality_expr': quality_expr,
            'quality_ok': True,
            'eval_round': eval_round,
            'stopped_reason': '质量达标',
        }
        if not node.get('started_at'):
            node['started_at'] = state_store.get_timestamp()
        state_store.safe_write(state, state_path)
        print(f"  ✅ evaluate [{node_id}] 质量达标（第 {eval_round} 轮）：{quality_expr}")
        return True
    elif eval_round < max_rounds:
        # 质量不达标，重跑目标节点
        new_round = eval_round + 1
        for tid in retry_targets:
            tnode = state['nodes'].get(tid)
            if not tnode:
                continue
            tnode['status'] = 'pending'
            tnode['started_at'] = None
            tnode['completed_at'] = None
            tnode['retry_count'] = 0
            tnode['error'] = None
            tnode['eval_round'] = new_round
        # 评估节点自身回到 pending，等重跑完再次评估
        node['status'] = 'pending'
        node['started_at'] = None
        node['completed_at'] = None
        node['eval_round'] = new_round

        state_store.safe_write(state, state_path)
        print(f"  🔄 evaluate [{node_id}] 第 {new_round}/{max_rounds} 轮：质量不达标，重跑 {retry_targets}")
        return True
    else:
        # 已达最大轮次，接受当前结果
        node['status'] = 'completed'
        node['completed_at'] = state_store.get_timestamp()
        node['output_data'] = {
            'quality_expr': quality_expr,
            'quality_ok': False,
            'eval_round': eval_round,
            'stopped_reason': f'已达最大评估轮次 {max_rounds}',
        }
        if not node.get('started_at'):
            node['started_at'] = state_store.get_timestamp()
        state_store.safe_write(state, state_path)
        print(f"  ⚠️ evaluate [{node_id}] 接受当前结果（已达最大 {max_rounds} 轮）：{quality_expr}")
        return True


# ============================================================
# 统一分发入口
# ============================================================
_HANDLERS = {
    'condition': handle_condition,
    'switch': handle_switch,
    'for-each': handle_for_each,
    'while-loop': handle_while_loop,
    'pipeline': handle_pipeline,
    'evaluate': handle_evaluate,
}


def process_control_node(state, node_id, state_path):
    """自动处理一个控制流节点，返回 True 表示已处理。

    由 orchestrator.step 在取到控制节点时调用。
    非控制节点返回 False（交回给 AI 执行流程）。
    """
    node = state['nodes'].get(node_id)
    if not node or not is_control_node(node):
        return False

    ntype = node['type']
    handler = _HANDLERS.get(ntype)
    if not handler:
        return False

    try:
        return handler(state, node_id, state_path)
    except ConditionError as e:
        # 条件求值失败属于"配置错误"，重试无意义 → 顶到 max_retry 使其成为
        # 终态失败，避免 get_next_node 反复重新获取该节点（防死循环刷屏）。
        node['status'] = 'failed'
        node['error'] = f"控制流求值失败：{e}"
        node['retry_count'] = node.get('max_retry', 3)
        state_store.safe_write(state, state_path)
        print(f"  ❌ 控制流节点 [{node_id}] 处理失败（配置错误，不重试）：")
        print(f"     {e}")
        print(f"     修复：检查该节点的表达式/字段配置，然后运行 resume 重试")
        return True


if __name__ == '__main__':
    print("控制流引擎 - 多Agent协作编排引擎 v5.2")
    print("=" * 50)
    print("此模块由 orchestrator.py 自动调用，通常无需单独运行。")
    print("")
    print("支持的控制流节点类型：")
    print("  condition   - if-else 条件分支（on_true / on_false）")
    print("  switch      - 多路分支（cases / default）")
    print("  for-each    - 动态节点生成（items / template / join）")
    print("  while-loop  - 循环重试（condition / loop_body / max_iterations）")
    print("  pipeline    - 子流水线引用（pipeline_ref / params / outputs）")
    print("  evaluate    - Self-Improving 质量评估（quality_expr / retry_targets）")
    print("")
    print("字段说明详见 templates/pipeline_dag_template.json 与 SKILL.md")

