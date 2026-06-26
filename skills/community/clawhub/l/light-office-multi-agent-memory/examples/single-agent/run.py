#!/usr/bin/env python3
"""
单Agent示例 - 演示如何使用多Agent记忆系统

功能：
  演示单Agent如何使用记忆系统进行自动捕获、检索、图谱构建等

作者：光光教授 (光光事务所)
版本：v1.0.0
许可证：MIT
"""

import os
import sys
from pathlib import Path

# 添加技能脚本到路径
SKILL_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SKILL_DIR))

from hook_capture import HookManager
from rrf_search import RRFSearch
from graph_builder import MemoryGraphBuilder
from conflict_detector import ConflictDetector
from token_tracker import TokenTracker


def main():
    """主函数"""
    print("=" * 60)
    print("单Agent示例 - 多Agent记忆系统")
    print("=" * 60)
    
    # 1. Hook自动捕获
    print("\n1. Hook自动捕获")
    hook_manager = HookManager()
    hook_manager.trigger("session_start", session_id="example-001", user_count=1)
    hook_manager.trigger("tool_use", tool_name="exec", input_summary="ls -la", output_summary="total 100")
    hook_manager.trigger("task_complete", task_id="task-001", duration=60, result_summary="任务完成")
    
    # 2. RRF融合检索
    print("\n2. RRF融合检索")
    rrf_search = RRFSearch()
    results = rrf_search.search("记忆系统优化")
    print(f"  检索结果: {len(results)}条")
    
    # 3. 知识图谱构建
    print("\n3. 知识图谱构建")
    graph_builder = MemoryGraphBuilder()
    stats = graph_builder.build_graph()
    print(f"  图谱统计: {stats['total_nodes']}节点, {stats['total_edges']}边")
    
    # 4. 矛盾检测
    print("\n4. 矛盾检测")
    conflict_detector = ConflictDetector()
    new_conflicts = conflict_detector.detect_conflicts()
    resolved = conflict_detector.resolve_conflicts()
    print(f"  冲突解决: {resolved}/{len(conflict_detector.conflicts)}")
    
    # 5. Token消耗追踪
    print("\n5. Token消耗追踪")
    token_tracker = TokenTracker()
    entry = token_tracker.log_session("example-001", "qwen3.5-plus", 5000, 3000)
    print(f"  Token消耗: {entry['total_tokens']}tokens, ¥{entry['total_cost']}")
    
    print("\n✅ 单Agent示例完成")


if __name__ == "__main__":
    main()
