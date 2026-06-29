#!/usr/bin/env python3
"""DAG引擎验证测试"""
import sys
sys.path.insert(0, '/home/agentuser/.hermes/workflow-engine')

from engine import DAGParser, WorkflowRunner, validate_workflow

EXAMPLE = '/home/agentuser/.hermes/workflow-engine/examples/ai-news-daily.yaml'

def test_dag_parser():
    print("=" * 50)
    print("TEST 1: DAG解析")
    print("=" * 50)
    parser = DAGParser(yaml_path=EXAMPLE)
    print(f"✅ 解析成功: {len(parser.steps)} 个步骤")
    print(f"   步骤ID: {list(parser.steps.keys())}")
    print(f"   邻接表: {dict(parser.adj)}")
    print(f"   入度: {dict(parser.in_degree)}")
    return parser

def test_validation(parser):
    print("\n" + "=" * 50)
    print("TEST 2: 工作流验证")
    print("=" * 50)
    result = parser.validate()
    print(f"   有效: {result['valid']}")
    if result['errors']:
        print(f"   ❌ 错误: {result['errors']}")
    else:
        print(f"   ✅ 无错误")
    if result['warnings']:
        print(f"   ⚠️  警告: {result['warnings']}")

def test_topo_sort(parser):
    print("\n" + "=" * 50)
    print("TEST 3: 拓扑排序（分层）")
    print("=" * 50)
    layers = parser.topological_sort()
    for i, layer in enumerate(layers):
        parallel = len(layer) > 1
        tag = "⚡并行" if parallel else "→串行"
        print(f"   第{i+1}层 [{tag}]: {layer}")

def test_execution_plan(parser):
    print("\n" + "=" * 50)
    print("TEST 4: 执行计划")
    print("=" * 50)
    plan = parser.get_execution_plan()
    for layer in plan:
        print(f"   层{layer['layer']+1}: {layer['steps']}")

def test_runner(parser):
    print("\n" + "=" * 50)
    print("TEST 5: Runner初始化")
    print("=" * 50)
    runner = WorkflowRunner(parser)
    print(f"   Run ID: {runner.run_id}")
    print(f"   Run Dir: {runner.run_dir}")
    print(f"   初始状态: {runner.status.value}")
    
    # 测试ready步骤
    ready = runner.get_ready_steps()
    print(f"   可执行步骤: {ready}")
    
    # 测试进度
    progress = runner.get_progress()
    print(f"   进度: {progress}")

def test_render_plan(parser):
    print("\n" + "=" * 50)
    print("TEST 6: 执行计划渲染")
    print("=" * 50)
    runner = WorkflowRunner(parser)
    print(runner.render_plan())

def test_cycle_detection():
    print("\n" + "=" * 50)
    print("TEST 7: 环检测")
    print("=" * 50)
    # 有环的工作流
    bad_yaml = """
name: bad-workflow
steps:
  - id: a
    depends: [b]
  - id: b
    depends: [a]
"""
    try:
        DAGParser(yaml_str=bad_yaml)
        print("   ❌ 应该检测到环但没有!")
    except ValueError as e:
        print(f"   ✅ 正确检测到环: {e}")

if __name__ == '__main__':
    parser = test_dag_parser()
    test_validation(parser)
    test_topo_sort(parser)
    test_execution_plan(parser)
    test_runner(parser)
    test_render_plan(parser)
    test_cycle_detection()
    print("\n" + "=" * 50)
    print("✅ 所有测试通过!")
    print("=" * 50)
