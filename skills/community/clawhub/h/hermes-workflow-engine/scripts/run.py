#!/usr/bin/env python3
"""
Hermes Workflow Engine — CLI入口 v3.0
用法:
  python3 run.py list                              # 列出本地工作流
  python3 run.py validate <yaml>                   # 验证工作流
  python3 run.py plan <yaml>                       # 查看执行计划
  python3 run.py next <yaml>                       # 获取下一批可执行步骤
  python3 run.py parallel <yaml>                   # 获取并行执行计划
  python3 run.py execute <yaml> [inputs_json]      # 生成完整执行指令
  python3 run.py delegate <yaml> [inputs_json]     # 生成delegate_task格式
  python3 run.py detect [days] [min_confidence]    # 模式检测
  python3 run.py community list [tag]              # 列出社区工作流
  python3 run.py community search <keyword>        # 搜索社区
  python3 run.py community publish <name>          # 发布到社区
  python3 run.py community install <name>          # 从社区安装
  python3 run.py community rate <name> <1-5>       # 评分
  python3 run.py community export <name>           # 导出.tgz
  python3 run.py community import <tgz_path>       # 导入.tgz
  python3 run.py versions <name>                   # 列出版本
  python3 run.py diff <name> <v1> <v2>             # 版本对比
  python3 run.py rollback <name> <version>         # 回滚版本
  python3 run.py dashboard [run_dir]               # 生成可视化面板
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from engine import DAGParser, WorkflowRunner, validate_workflow
from executor import (
    StepExecutor, Scheduler, load_and_plan,
    generate_agent_instructions, generate_delegate_task_batch
)
from pattern_detector import PatternDetector, format_detection_report
from version_manager import VersionManager, format_version_list, format_diff_report
from community import CommunityHub, format_community_list
from dashboard import generate_dashboard, save_dashboard
from auto_trigger import AutoTrigger, format_trigger_analysis


def cmd_list():
    wf_dir = Path.home() / '.hermes' / 'workflow-engine' / 'examples'
    if not wf_dir.exists():
        print("没有找到工作流定义")
        return
    print("可用工作流:")
    for f in sorted(wf_dir.glob('*.yaml')):
        try:
            parser = DAGParser(yaml_path=str(f))
            spec = parser.spec
            layers = parser.topological_sort()
            has_parallel = any(len(l) > 1 for l in layers)
            tag = " ⚡有并行" if has_parallel else ""
            print(f"  • {f.stem}")
            print(f"    {spec.get('description', '无描述')}")
            print(f"    {len(spec.get('steps', []))} 步, {len(layers)} 层{tag}")
        except Exception as e:
            print(f"  • {f.stem} ❌ {e}")


def cmd_validate(yaml_path):
    result = validate_workflow(yaml_path)
    if result['valid']:
        print("✅ 工作流验证通过")
    else:
        print("❌ 工作流验证失败:")
        for e in result['errors']:
            print(f"  • {e}")
    if result['warnings']:
        print("⚠️  警告:")
        for w in result['warnings']:
            print(f"  • {w}")


def cmd_plan(yaml_path):
    result = load_and_plan(yaml_path)
    print(result['render'])


def cmd_next(yaml_path):
    result = load_and_plan(yaml_path)
    batch = result['first_batch']
    if not batch:
        print("没有可执行的步骤")
        return
    print(f"可执行步骤 ({len(batch)} 个):")
    for step in batch:
        print(json.dumps(step, ensure_ascii=False, indent=2))


def cmd_parallel(yaml_path):
    result = load_and_plan(yaml_path)
    layers = result['parallel_layers']
    if not layers:
        print("没有可执行的步骤")
        return
    print(f"并行执行计划 ({len(layers)} 层):")
    for i, layer in enumerate(layers):
        if len(layer) > 1:
            print(f"\n  ⚡ 第{i+1}层 (并行 {len(layer)} 步):")
            for j, step in enumerate(layer):
                print(f"    [{j+1}] {step['step_name']} ({step['step_type']})")
        else:
            step = layer[0]
            print(f"\n  → 第{i+1}层 (串行): {step['step_name']} ({step['step_type']})")


def cmd_execute(yaml_path, inputs_json=None):
    inputs = json.loads(inputs_json) if inputs_json else {}
    result = load_and_plan(yaml_path, inputs)
    plan = result['plan']
    batch = result['first_batch']
    print(generate_agent_instructions(plan, batch))
    plan_path = Path.home() / '.hermes' / 'workflow-engine' / 'runs' / plan['run_id'] / 'plan.json'
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    with open(plan_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    print(f"\n执行计划已保存: {plan_path}")


def cmd_delegate(yaml_path, inputs_json=None):
    inputs = json.loads(inputs_json) if inputs_json else {}
    result = load_and_plan(yaml_path, inputs)
    layers = result['parallel_layers']
    for i, layer in enumerate(layers):
        print(f"\n=== 第{i+1}层 ===")
        if len(layer) > 1:
            tasks = generate_delegate_task_batch(layer)
            print(f"⚡ 并行执行 {len(tasks)} 个任务:")
            print(json.dumps(tasks, ensure_ascii=False, indent=2))
        else:
            step = layer[0]
            print(f"→ 串行执行: {step['step_name']}")
            print(json.dumps(step, ensure_ascii=False, indent=2))


def cmd_detect(days=7, min_confidence=0.3):
    detector = PatternDetector()
    result = detector.run_detection(days=days, min_confidence=min_confidence)
    print(format_detection_report(result))


def cmd_community(args):
    hub = CommunityHub()
    if not args:
        print("用法: python3 run.py community <subcommand>")
        return

    sub = args[0]

    if sub == 'list':
        tag = args[1] if len(args) > 1 else None
        workflows = hub.list_community(tag)
        print(format_community_list(workflows))

    elif sub == 'search':
        if len(args) < 2:
            print("用法: python3 run.py community search <keyword>")
            return
        results = hub.search_community(args[1])
        print(f"搜索结果: {len(results)} 个")
        for r in results:
            print(f"  • {r['name']}: {r.get('description', '')[:50]}")

    elif sub == 'publish':
        if len(args) < 2:
            print("用法: python3 run.py community publish <name>")
            return
        result = hub.publish_to_community(args[1])
        if result['success']:
            print(f"✅ 已发布: {result['name']}")
        else:
            print(f"❌ 发布失败: {result.get('error')}")

    elif sub == 'install':
        if len(args) < 2:
            print("用法: python3 run.py community install <name>")
            return
        result = hub.install_from_community(args[1])
        if result['success']:
            print(f"✅ 已安装: {result['name']}")
        else:
            print(f"❌ 安装失败: {result.get('error')}")

    elif sub == 'rate':
        if len(args) < 3:
            print("用法: python3 run.py community rate <name> <1-5>")
            return
        result = hub.rate_workflow(args[1], int(args[2]))
        if result['success']:
            print(f"✅ 评分成功: {result['name']} → {result['new_rating']}⭐")
        else:
            print(f"❌ 评分失败: {result.get('error')}")

    elif sub == 'export':
        if len(args) < 2:
            print("用法: python3 run.py community export <name>")
            return
        path = hub.export_workflow(args[1])
        print(f"✅ 已导出: {path}")

    elif sub == 'import':
        if len(args) < 2:
            print("用法: python3 run.py community import <tgz_path>")
            return
        result = hub.import_workflow(args[1])
        if result['success']:
            print(f"✅ 已导入: {result['name']}")
        else:
            print(f"❌ 导入失败: {result.get('error')}")

    else:
        print(f"未知子命令: {sub}")


def cmd_versions(name):
    vm = VersionManager()
    versions = vm.list_versions(name)
    if not versions:
        print(f"工作流 {name} 没有版本记录")
        return
    meta = vm._load_meta(name)
    print(format_version_list(name, versions, meta.get('current')))


def cmd_diff(name, v1, v2):
    vm = VersionManager()
    diff = vm.diff(name, v1, v2)
    if 'error' in diff:
        print(f"❌ {diff['error']}")
        return
    print(format_diff_report(diff))


def cmd_rollback(name, version):
    vm = VersionManager()
    result = vm.rollback(name, version)
    if result['success']:
        print(f"✅ 已回滚到 v{version}")
    else:
        print(f"❌ 回滚失败: {result.get('error')}")


def cmd_dashboard(run_dir=None):
    if not run_dir:
        # 列出可用的运行记录
        runs_dir = Path.home() / '.hermes' / 'workflow-engine' / 'runs'
        if runs_dir.exists():
            runs = sorted(runs_dir.iterdir(), reverse=True)
            if runs:
                run_dir = str(runs[0])
                print(f"使用最新运行记录: {run_dir}")
            else:
                print("没有运行记录")
                return
    path = save_dashboard(run_dir)
    print(f"✅ 面板已生成: {path}")


def cmd_trigger(message):
    """分析用户消息，返回触发建议"""
    trigger = AutoTrigger()
    analysis = trigger.analyze_message(message)
    print(format_trigger_analysis(analysis))


def cmd_trigger_scheduled():
    """检查是否有应该自动执行的工作流"""
    trigger = AutoTrigger()
    scheduled = trigger.check_scheduled_workflows()
    if not scheduled:
        print("没有应该自动执行的工作流")
        return
    print(f"发现 {len(scheduled)} 个应该执行的工作流:")
    for s in scheduled:
        print(f"  • {s['workflow']}: {s['reason']} (置信度: {s['confidence']})")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    try:
        if cmd == 'list': cmd_list()
        elif cmd == 'validate': cmd_validate(args[0])
        elif cmd == 'plan': cmd_plan(args[0])
        elif cmd == 'next': cmd_next(args[0])
        elif cmd == 'parallel': cmd_parallel(args[0])
        elif cmd == 'execute': cmd_execute(args[0], args[1] if len(args) > 1 else None)
        elif cmd == 'delegate': cmd_delegate(args[0], args[1] if len(args) > 1 else None)
        elif cmd == 'detect': cmd_detect(int(args[0]) if args else 7, float(args[1]) if len(args) > 1 else 0.3)
        elif cmd == 'community': cmd_community(args)
        elif cmd == 'versions': cmd_versions(args[0])
        elif cmd == 'diff': cmd_diff(args[0], args[1], args[2])
        elif cmd == 'rollback': cmd_rollback(args[0], args[1])
        elif cmd == 'dashboard': cmd_dashboard(args[0] if args else None)
        elif cmd == 'trigger': cmd_trigger(' '.join(args) if args else '')
        elif cmd == 'trigger-scheduled': cmd_trigger_scheduled()
        else:
            print(f"未知命令: {cmd}")
            print(__doc__)
            sys.exit(1)
    except IndexError:
        print(f"参数不足，用法: python3 run.py {cmd} ...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
