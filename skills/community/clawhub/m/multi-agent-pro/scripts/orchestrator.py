#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编排引擎入口 - 多Agent协作编排引擎 v5.3

功能：统一入口，整合 DAG 验证、状态管理、执行调度、错误恢复、报告生成
支持人工审批节点（含超时策略）、HTML 甘特图、历史执行对比、硬件自适应
动态工作流：if-else 条件分支、switch 多路分支、for-each 动态节点、while-loop 循环
新增：子流水线引用（pipeline 节点）、执行回放 / Time Travel（快照机制+保留策略）
新增：统一状态恢复子系统（合并断点续传 + 快照恢复）
新增：统一可视化命令（visualize --format md|html|both，整合报告 + 甘特图）
新增：Self-Improving 循环（evaluate 节点，质量评估 + 自动重试）
新增：成本追踪（节点级 token/cost 聚合，对接 cn-llm-router）
新增：官方流水线模板库（4类预置模板 + 依赖探测渲染）
新增：任务级重试策略（节点级 retry 块 + 退避 + 降级链）
新增：统一错误恢复命令 recover（retry/fallback/impact 三合一）
新增：条件表达式增强（re_safe + 字符串函数）
新增：节点类型归组（7→4类，认知层归组）
零第三方依赖，仅使用 Python 标准库

★★★ 安全说明 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 所有路径经过规范化校验，防止路径穿越
2. 节点输出超过 10MB 时自动写入独立文件
3. 文件大小检测（状态文件最大 50MB，pipeline.json 最大 10MB）
4. 节点 id 仅允许 [a-zA-Z0-9_.-]，防止注入
5. 不自动处理敏感数据，用户需自行脱敏

★★★ 快速上手（3步）★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
step 1 → 创建 pipeline.json（定义流水线，参考 templates/pipeline_dag_template.json）
step 2 → 运行：python orchestrator.py run <pipeline.json>
step 3 → 循环运行：python orchestrator.py step <state.json> + 执行任务 + complete/fail

详细文档：SKILL.md 第一层「快速入门」
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import sys
import os

# 将脚本目录加入 path 以便导入同级模块
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import dag_validator
import state_store
import error_recovery
import pipeline_reporter
import flow_controller


def cmd_validate(args):
    """验证 DAG 结构（Schema + 循环检测 + 孤立节点）

    ★★★ 安全功能 ★★★
    - 节点 id 字符校验（防注入）
    - 节点数量限制（最多 100 个）
    - 节点输出大小限制（最大 10MB）
    """
    if not args:
        print("错误：缺少[pipeline.json路径]")
        print("用法：python orchestrator.py validate <pipeline.json>")
        print("示例：python orchestrator.py validate templates/pipeline_dag_template.json")
        sys.exit(1)
    dag_validator.validate(args[0])


def cmd_plan(args):
    """查看执行计划（拓扑排序 + 节点详情，不做任何修改）

    安全说明：此命令是只读的，不会创建或修改任何文件。
    """
    if not args:
        print("错误：缺少[pipeline.json路径]")
        print("用法：python orchestrator.py plan <pipeline.json>")
        sys.exit(1)

    pipeline = dag_validator.load_pipeline(args[0])

    # 验证
    errors, warnings = dag_validator.validate_schema(pipeline)
    if errors:
        print("DAG 结构验证失败，请先修复以下错误：")
        for e in errors:
            print(f"  [错误] {e}")
        sys.exit(1)

    cycle_errors = dag_validator.detect_cycles(pipeline)
    if cycle_errors:
        print("检测到循环依赖，请先修复：")
        for e in cycle_errors:
            print(f"  [错误] {e}")
        sys.exit(1)

    # 拓扑排序
    order = dag_validator.topological_sort(pipeline)
    agents = {a['id']: a for a in pipeline.get('agents', [])}

    print("=" * 60)
    print(f"  执行计划：{pipeline.get('pipeline_name', '未命名')}")
    print("=" * 60)
    print(f"\n拓扑排序执行顺序（共 {len(order)} 个节点）：\n")

    for i, node_id in enumerate(order, 1):
        agent = agents.get(node_id, {})
        name = agent.get('name', node_id)
        role = agent.get('role', '')
        deps = agent.get('depends_on', [])
        retry = agent.get('retry', 3)
        timeout = agent.get('timeout', 60)
        fallback = agent.get('fallback', 'abort')

        print(f"  Step {i}: [{node_id}] {name}")
        print(f"    角色：{role}")
        print(f"    依赖：{', '.join(deps) if deps else '无（首节点）'}")
        print(f"    超时：{timeout}秒 | 重试：{retry}次 | 降级：{fallback}")
        if i < len(order):
            print(f"    ↓")
        print()

    print("=" * 60)
    print(f"\n确认无误后运行：python orchestrator.py run {args[0]}")


def cmd_run(args):
    """初始化并开始执行（验证 → 初始化状态）★★★ 首次使用必做 ★★★

    安全说明：
    - 会覆盖已存在的 state.json（先备份再覆盖）
    - 所有节点 id 经过安全校验
    - 如果 state.json 已存在，会提示确认
    """
    if not args:
        print("错误：缺少[pipeline.json路径]")
        print("用法：python orchestrator.py run <pipeline.json>")
        print("示例：python orchestrator.py run templates/pipeline_dag_template.json")
        print("")
        print("★★★ 提示 ★★★")
        print("  首次使用请先运行 plan 查看执行计划：")
        print("  python orchestrator.py plan <pipeline.json>")
        sys.exit(1)

    pipeline_path = args[0]
    state_path_arg = args[1] if len(args) > 1 else None

    # 先验证
    print("[1/2] 验证 DAG 结构...")
    pipeline = dag_validator.load_pipeline(pipeline_path)
    errors, warnings = dag_validator.validate_schema(pipeline)
    if errors:
        print("验证失败：")
        for e in errors:
            print(f"  [错误] {e}")
        print("\n修复建议：参考 templates/pipeline_dag_template.json 检查字段")
        sys.exit(1)
    cycle_errors = dag_validator.detect_cycles(pipeline)
    if cycle_errors:
        print("循环依赖检测失败：")
        for e in cycle_errors:
            print(f"  [错误] {e}")
        sys.exit(1)
    print("  ✅ 验证通过")

    # 检查/state.json是否已存在（避免意外覆盖）
    if state_path_arg is None:
        state_path_check = pipeline.get('state_store', {}).get('path', './pipeline_state.json')
    else:
        state_path_check = state_path_arg
    state_path_check = os.path.abspath(os.path.normpath(state_path_check))

    if os.path.exists(state_path_check):
        print(f"\n⚠️ 状态文件已存在：{state_path_check}")
        print("  继续运行将覆盖此文件（建议使用 resume 恢复）")
        response = input("  是否继续？(y/N): ").strip().lower()
        if response != 'y':
            print("  已取消。运行 resume 恢复或更换输出路径。")
            sys.exit(0)

    # 初始化状态
    print("\n[2/2] 初始化状态文件...")
    state, state_path = state_store.init_state(pipeline, state_path_arg)

    print(f"\n✅ 初始化完成！")
    print(f"\n接下来，循环执行以下步骤：")
    print(f"  1. python orchestrator.py step {state_path}")
    print(f"     → 获取待执行节点，AI 执行任务")
    print(f"  2a. 成功 → python state_store.py complete {state_path} <node_id> '输出JSON'")
    print(f"  2b. 失败 → python error_recovery.py retry {state_path} <node_id> '错误描述'")
    print(f"  3. 重复步骤 1-2，直到流水线完成")
    print(f"\n查看状态：")
    print(f"  python orchestrator.py status {state_path}")


def cmd_step(args):
    """执行下一个待处理节点（从状态文件中获取，自动注入上游输出）

    安全说明：
    - 只有依赖全部完成（completed/skipped）的节点才会被获取
    - running 状态的过期节点会自动重置为 pending（防止死锁）
    - 遇到人工审批节点（type: approval）会暂停等待用户确认
    - 遇到控制流节点（condition/switch/for-each/while-loop）会自动求值并路由
    """
    if not args:
        print("错误：缺少[state.json路径]")
        print("用法：python orchestrator.py step <state.json>")
        print("示例：python orchestrator.py step pipeline_state.json")
        sys.exit(1)

    state_path = args[0]
    node_id = state_store.get_next_node(state_path)

    if node_id:
        state = state_store.load_state(state_path)
        node = state['nodes'][node_id]
        node_type = node.get('type', 'task')

        # 控制流节点：由引擎自动求值并动态路由（不交给 AI）
        if flow_controller.is_control_node(node):
            print(f"\n{'=' * 60}")
            print(f"  ⚙️  控制流节点（引擎自动处理）")
            print(f"{'=' * 60}")
            print(f"节点 ID：{node_id}")
            print(f"节点类型：{node_type}")
            print(f"节点名称：{node.get('name', node_id)}")
            flow_controller.process_control_node(state, node_id, state_path)
            print(f"\n继续运行下一步：python orchestrator.py step {state_path}")
            print(f"{'=' * 60}")
            return

        # 人工审批节点
        if node_type == 'approval':
            print(f"\n{'=' * 60}")
            print(f"  🔐 人工审批节点")
            print(f"{'=' * 60}")
            print(f"节点 ID：{node_id}")
            print(f"节点名称：{node.get('name', node_id)}")
            print(f"角色描述：{node.get('role', '未指定')}")

            # 注入上游输出
            deps = node.get('depends_on', [])
            if deps:
                print(f"\n📥 上游输出（供审批参考）：")
                for dep in deps:
                    dep_data = state['nodes'].get(dep, {}).get('output_data', {})
                    preview = json.dumps(dep_data, ensure_ascii=False)[:300]
                    print(f"  [{dep}] → {preview}")

            # 超时策略
            timeout_seconds = node.get('timeout_seconds', 0)
            timeout_action = node.get('timeout_action', 'reject')

            if timeout_seconds and timeout_seconds > 0:
                print(f"\n⏰ 超时设置：{timeout_seconds}秒后自动{'通过' if timeout_action == 'approve' else '拒绝'}")

            print(f"\n请确认是否继续执行后续节点？")
            print(f"  [Y] 同意 - 继续执行")
            print(f"  [N] 拒绝 - 中止流水线")
            print(f"{'=' * 60}")

            choice = None
            if timeout_seconds and timeout_seconds > 0:
                import select
                print(f"  请输入 (Y/N): ", end='', flush=True)
                try:
                    rlist, _, _ = select.select([sys.stdin], [], [], timeout_seconds)
                    if rlist:
                        choice = sys.stdin.readline().strip().upper()
                    else:
                        choice = 'Y' if timeout_action == 'approve' else 'N'
                        print(f"\n  ⏰ 审批超时（{timeout_seconds}秒），自动{'通过' if timeout_action == 'approve' else '拒绝'}")
                except (OSError, IOError):
                    try:
                        choice = input("  请输入 (Y/N): ").strip().upper()
                    except (EOFError, KeyboardInterrupt):
                        print("\n  已取消。")
                        sys.exit(0)
            else:
                try:
                    choice = input("  请输入 (Y/N): ").strip().upper()
                except (EOFError, KeyboardInterrupt):
                    print("\n  已取消。")
                    sys.exit(0)

            if choice == 'Y':
                node['status'] = 'completed'
                node['output_data'] = {'approved': True, 'approved_at': state_store.get_timestamp()}
                node['completed_at'] = state_store.get_timestamp()
                state_store.safe_write(state, state_path)
                print(f"\n  ✅ 已批准，继续执行")
                print(f"  运行下一步：python orchestrator.py step {state_path}")
            else:
                node['status'] = 'completed'
                node['output_data'] = {'approved': False, 'rejected_at': state_store.get_timestamp()}
                node['completed_at'] = state_store.get_timestamp()
                state_store.safe_write(state, state_path)
                state['status'] = 'aborted'
                state_store.safe_write(state, state_path)
                print(f"\n  ❌ 已拒绝，流水线已中止")
                print(f"  查看报告：python orchestrator.py report {state_path}")
                print(f"  断点续传：python orchestrator.py resume {state_path} --force")
            return

        print(f"\n{'=' * 60}")
        print(f"  🎯 请 AI 执行此节点的任务")
        print(f"{'=' * 60}")
        print(f"节点 ID：{node_id}")
        print(f"节点名称：{node.get('name', node_id)}")
        print(f"角色描述：{node.get('role', '未指定')}")
        print(f"输入参数：{', '.join(node.get('inputs', []))}")
        print(f"期望输出：{', '.join(node.get('outputs', []))}")

        # 注入上游输出
        deps = node.get('depends_on', [])
        if deps:
            print(f"\n📥 上游输出（已自动注入到 input_data）：")
            for dep in deps:
                dep_data = state['nodes'].get(dep, {}).get('output_data', {})
                preview = json.dumps(dep_data, ensure_ascii=False)[:300]
                print(f"  [{dep}] → {preview}")

        print(f"\n完成后运行：")
        print(f"  ✅ 成功：python state_store.py complete {state_path} {node_id} '{{\"result\":\"你的输出\"}}'")
        print(f"  ❌ 失败：python error_recovery.py retry {state_path} {node_id} '错误描述'")
        print(f"{'=' * 60}")


def cmd_status(args):
    """查看当前流水线状态

    安全说明：此命令是只读的，不会修改任何文件。
    """
    if not args:
        print("错误：缺少[state.json路径]")
        print("用法：python orchestrator.py status <state.json>")
        sys.exit(1)
    state_store.show_status(args[0])


def cmd_resume(args):
    """断点续传（统一状态恢复子系统）

    安全说明：
    - 使用 --force 跳过确认提示
    - 重置前自动创建恢复前快照（防误操作）
    - 已完成的节点不受影响
    """
    if not args:
        print("错误：缺少[state.json路径]")
        print("用法：python orchestrator.py resume <state.json> [--force]")
        sys.exit(1)

    force = '--force' in args
    state_path = args[0]
    import state_recovery
    state_recovery.restore_to_node(state_path, None, 'resume', force=force)


def cmd_report(args):
    """生成 Markdown 执行报告（可在任意阶段运行）

    安全说明：
    - 报告文件可能包含节点输出的敏感信息
    - 建议生成的报告文件妥善保管，避免泄露
    """
    if not args:
        print("错误：缺少[state.json路径]")
        print("用法：python orchestrator.py report <state.json> [output.md]")
        print("示例：python orchestrator.py report pipeline_state.json report.md")
        print("")
        print("⚠️ 安全提示：报告文件可能包含敏感数据，请妥善保管")
        sys.exit(1)
    output = args[1] if len(args) > 1 else None
    pipeline_reporter.generate_report(args[0], output)


def cmd_impact(args):
    """分析指定节点的下游影响（用于排查故障传导范围）

    安全说明：此命令是只读的，不会修改任何文件。
    """
    if len(args) < 2:
        print("错误：参数不足")
        print("用法：python orchestrator.py impact <state.json> <node_id>")
        print("示例：python orchestrator.py impact pipeline_state.json node_a")
        sys.exit(1)
    error_recovery.analyze_downstream_impact(args[0], args[1])


def cmd_recover(args):
    """统一错误恢复入口：retry/fallback/impact"""
    if not args:
        print("用法：python orchestrator.py recover <retry|fallback|impact> <state.json> <node_id> [error_msg]")
        sys.exit(1)
    sub = args[0]
    if sub == 'retry':
        if len(args) < 3:
            print("用法：python orchestrator.py recover retry <state.json> <node_id> [error_msg]")
            sys.exit(1)
        error_msg = args[3] if len(args) > 3 else "未知错误"
        error_recovery.execute_retry(args[1], args[2], error_msg)
    elif sub == 'fallback':
        if len(args) < 3:
            print("用法：python orchestrator.py recover fallback <state.json> <node_id> [error_msg]")
            sys.exit(1)
        error_msg = args[3] if len(args) > 3 else "未知错误"
        error_recovery.execute_fallback(args[1], args[2], error_msg)
    elif sub == 'impact':
        if len(args) < 3:
            print("用法：python orchestrator.py recover impact <state.json> <node_id>")
            sys.exit(1)
        error_recovery.analyze_downstream_impact(args[1], args[2])
    else:
        print(f"未知 recover 子命令：{sub}")


USAGE = """
编排引擎 - 多Agent协作编排引擎 v5.3
================================

用法：python orchestrator.py <command> [args]

命令列表（按使用频率排序）：
  run <pipeline.json> [state]                 ★★★ 首次使用 ★★★ 初始化并开始执行
  step <state.json>                            ★☆☆ 逐步执行（获取下一个待执行节点）
  status <state.json>                          ★★☆ 查看流水线状态（只读）
  resume <state.json> [--force]                ★★☆ 断点续传（重置失败节点）
  visualize <state.json> [--format md|html|both] [output]  ★★★ 统一可视化（MD+HTML）
  report <state.json> [output]                 ★★☆ 生成 Markdown 执行报告（visualize --format md 别名）
  gantt <state.json> [output.html]              ★★☆ 生成 HTML 甘特图（visualize --format html 别名）
  validate <pipeline.json>                     ★☆  验证 DAG 结构（只读，不修改文件）
  plan <pipeline.json>                         ★☆  查看执行计划（只读，不修改文件）
  history <state.json>                         ★☆☆ 查看执行历史记录
  compare <state.json>                         ★☆☆ 对比最近5次执行（耗时/成功率/重试）
  hardware                                     ★☆☆ 硬件检测与参数推荐
  check-update                                 ☆☆  检查是否有新版本
  snapshot <cmd> <state.json> [node_id]        ☆☆  快照管理（list/show/restore/diff）
  impact <state.json> <node_id>                ☆☆  分析下游影响（只读）
  template <cmd> [template_file]              ☆☆  预置模板库（list/show/check/render）

典型工作流：
  1. python orchestrator.py plan pipeline.json         # 查看执行计划
  2. python orchestrator.py run pipeline.json           # 初始化
  3. python orchestrator.py step state.json             # 获取待执行节点
  4. AI 执行任务...
  5. python state_store.py complete state.json node '...'
  6. 重复 3-5，直到流水线完成
  7. python orchestrator.py gantt state.json            # 生成 HTML 甘特图
  8. python orchestrator.py report state.json           # 生成 Markdown 报告

★★★ 新功能 v5.0（子流水线 + 执行回放）★★★
  - 子流水线引用：type: pipeline，引用已注册的子流水线隔离执行
  - 执行回放 / Time Travel：节点快照 + 增量存储 + 从快照恢复 + 执行对比
  - 快照命令：snapshot list/show/restore/diff

★★★ v4.0 功能（动态工作流）★★★
  - if-else 条件分支：type: condition，按条件走 on_true / on_false
  - switch 多路分支：type: switch，按值命中 cases / default
  - for-each 动态节点：type: for-each，按列表长度展开子节点并汇合
  - while-loop 循环重试：type: while-loop，条件为真回环重跑循环体
  - 条件表达式：nodes.<id>.output_data.<field> 点路径 + 比较/逻辑/成员运算
    （AST 白名单求值，禁止函数调用，安全无 eval）

★★★ v3.0 功能 ★★★
  - 人工审批节点：在 DAG 中设置 type: approval 暂停等用户确认
  - HTML 甘特图：可视化每个节点的开始/结束/成功/失败（颜色编码）
  - 历史执行对比：自动对比最近5次执行，输出"本次比上次慢X%"
  - 硬件自适应：自动检测 CPU/内存，推荐最优并发数和文件大小限制
  - 更新提醒：启动时检查 GitHub 是否有新版本

★★★ 安全说明 ★★★
  - 节点 id 仅允许 [a-zA-Z0-9_.-]，防止注入
  - 节点输出最大 10MB，超过自动写入独立文件
  - 状态文件最大 50MB
  - pipeline.json 最大 10MB
  - 不自动脱敏，敏感数据需用户自行处理
"""


def cmd_gantt(args):
    """生成 HTML 甘特图"""
    if not args:
        print("错误：缺少[state.json路径]")
        print("用法：python orchestrator.py gantt <state.json> [output.html]")
        print("示例：python orchestrator.py gantt pipeline_state.json gantt.html")
        sys.exit(1)
    output = args[1] if len(args) > 1 else None
    pipeline_reporter.generate_html_gantt(args[0], output)


def cmd_visualize(args):
    """统一可视化（MD 报告 + HTML 甘特图）

    安全说明：
    - 输出文件可能包含节点输出的敏感信息
    - 建议生成的文件妥善保管，避免泄露
    """
    if not args:
        print("错误：缺少[state.json路径]")
        print("用法：python orchestrator.py visualize <state.json> [--format md|html|both] [output]")
        print("示例：python orchestrator.py visualize pipeline_state.json --format both")
        print("      python orchestrator.py visualize pipeline_state.json --format md report.md")
        print("")
        print("⚠️ 安全提示：输出文件可能包含敏感数据，请妥善保管")
        sys.exit(1)

    state_path = args[0]
    fmt = 'both'
    output = None

    # 解析参数
    i = 1
    while i < len(args):
        if args[i] == '--format' and i + 1 < len(args):
            fmt = args[i + 1]
            i += 2
        else:
            output = args[i]
            i += 1

    if fmt not in ('md', 'html', 'both'):
        print(f"错误：无效格式 [{fmt}]，可选：md / html / both")
        sys.exit(1)

    pipeline_reporter.generate_visualization(state_path, output, fmt)


def cmd_history(args):
    """查看执行历史"""
    if not args:
        print("错误：缺少[state.json路径]")
        print("用法：python orchestrator.py history <state.json>")
        sys.exit(1)
    state_store.show_history(args[0])


def cmd_compare(args):
    """对比最近执行"""
    if not args:
        print("错误：缺少[state.json路径]")
        print("用法：python orchestrator.py compare <state.json>")
        sys.exit(1)
    state_store.compare_history(args[0])


def cmd_hardware(args):
    """硬件检测"""
    import hardware_detector
    hardware_detector.detect()


def cmd_check_update(args):
    """检查更新"""
    import update_checker
    update_checker.check_update()


def cmd_snapshot(args):
    """快照管理：list/show/restore/diff"""
    import snapshot_store
    if not args:
        print("用法：python orchestrator.py snapshot <list|show|restore|diff> <state.json> [node_id]")
        sys.exit(1)
    sub = args[0]
    if sub == 'list':
        snapshot_store.list_snapshots(args[1])
    elif sub == 'show':
        snapshot_store.show_snapshot(args[1], args[2])
    elif sub == 'restore':
        snapshot_store.restore_snapshot(args[1], args[2])
    elif sub == 'diff':
        snapshot_store.diff_snapshots(args[1], args[2], args[3])
    else:
        print(f"未知 snapshot 子命令：{sub}")


def cmd_dashboard(args):
    """启动 Web 控制台（只读服务 + ECharts 甘特图）"""
    import web_dashboard
    state_dir = args[0] if args else '.'
    port = int(args[1]) if len(args) > 1 else web_dashboard.DASHBOARD_PORT
    print(f"🖥️  Web 控制台启动中...")
    print(f"   地址：http://127.0.0.1:{port}")
    print(f"   状态目录：{state_dir}")
    print(f"   按 Ctrl+C 停止")
    web_dashboard.start_dashboard(state_dir, port)


def cmd_mcp(args):
    """启动 MCP Server（stdio JSON-RPC）"""
    import mcp_server
    mcp_server.main()


def cmd_cost(args):
    """成本桥接：回填实测成本（cn-llm-router 可用时）"""
    import cost_bridge
    if not args:
        print("用法：python orchestrator.py cost <state_dir> [--pipeline <name>] [--check] [--summary]")
        print("  --check    仅检测 cn-llm-router 是否可用")
        print("  --summary  输出单个状态文件的成本汇总")
        sys.exit(1)

    state_dir = args[0]
    # 去掉前两个位置参数
    remaining_args = args[1:]

    import sys as _sys
    _sys.argv = ['cost_bridge.py', state_dir] + remaining_args
    cost_bridge.main()


def cmd_init(args):
    """新手向导：交互式创建第一条流水线"""
    import template_lib
    template_lib.newbie_wizard()


def cmd_template(args):
    """预置流水线模板库：list/show/check/render/validate"""
    import template_lib
    if not args:
        print("用法：python orchestrator.py template <list|show|check|render|validate> [template_file]")
        sys.exit(1)
    sub = args[0]
    if sub == 'list':
        template_lib.list_templates()
    elif sub == 'show':
        if len(args) < 2:
            print("错误：请指定模板文件名")
            print("用法：python orchestrator.py template show <template_file>")
            sys.exit(1)
        template_lib.show_template(args[1])
    elif sub == 'check':
        if len(args) < 2:
            print("错误：请指定模板文件名")
            print("用法：python orchestrator.py template check <template_file>")
            sys.exit(1)
        req, opt = template_lib.check_dependencies(args[1])
        if not req and not opt:
            print("✅ 所有依赖均已满足")
        else:
            if req:
                print(f"❌ 缺失必需依赖：{', '.join(d['skill_id'] for d in req)}")
            if opt:
                print(f"⚠️ 缺失可选依赖：{', '.join(d['skill_id'] for d in opt)}")
    elif sub == 'render':
        if len(args) < 2:
            print("错误：请指定模板文件名")
            print("用法：python orchestrator.py template render <template_file> [output.json]")
            sys.exit(1)
        output_path = args[2] if len(args) > 2 else None
        pipeline = template_lib.render_pipeline(args[1])
        if pipeline:
            if output_path:
                import json as _json
                with open(output_path, 'w', encoding='utf-8') as f:
                    _json.dump(pipeline, f, ensure_ascii=False, indent=2)
                print(f"✅ 已渲染到 {output_path}")
            else:
                import json as _json
                print(_json.dumps(pipeline, ensure_ascii=False, indent=2))
    elif sub == 'validate':
        if len(args) < 2:
            # 校验所有模板
            all_valid = True
            for fname in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')):
                if not fname.endswith('.json') or fname in ('template_schema.json', 'state_schema.json'):
                    continue
                valid, errors = template_lib.validate_template(fname)
                if not valid:
                    all_valid = False
                    print(f"❌ {fname}: {', '.join(errors)}")
            if all_valid:
                print("✅ 所有模板校验通过")
            else:
                sys.exit(1)
        else:
            valid, errors = template_lib.validate_template(args[1])
            if valid:
                print(f"✅ {args[1]} 校验通过")
            else:
                print(f"❌ {args[1]} 校验失败：{', '.join(errors)}")
                sys.exit(1)
    else:
        print(f"未知 template 子命令：{sub}")


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(USAGE)
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        'validate': cmd_validate,
        'plan': cmd_plan,
        'run': cmd_run,
        'step': cmd_step,
        'status': cmd_status,
        'resume': cmd_resume,
        'report': cmd_report,
        'gantt': cmd_gantt,
        'visualize': cmd_visualize,
        'history': cmd_history,
        'compare': cmd_compare,
        'hardware': cmd_hardware,
        'check-update': cmd_check_update,
        'impact': cmd_impact,
        'snapshot': cmd_snapshot,
        'template': cmd_template,
        'recover': cmd_recover,
        'dashboard': cmd_dashboard,
        'mcp': cmd_mcp,
        'cost': cmd_cost,
        'init': cmd_init,
        # 旧命令别名（向后兼容）
        'retry': lambda a: cmd_recover(['retry'] + a),
        'fallback': lambda a: cmd_recover(['fallback'] + a),
    }

    if cmd not in commands:
        print(f"错误：未知命令 [{cmd}]")
        print(USAGE)
        sys.exit(1)

    commands[cmd](args)
