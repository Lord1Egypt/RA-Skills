#!/usr/bin/env python3
"""
记忆系统自进化引擎
实现检索策略优化、记忆价值评分、自动归档等自进化功能

功能:
- 检索策略 A/B 测试
- 记忆价值评分算法（引用频率、情感强度、时间衰减）
- 自动归档低价值记忆
- 策略优化建议生成
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, asdict, field
import argparse
import subprocess

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_MD = WORKSPACE / "MEMORY.md"
INDEX_DIR = WORKSPACE / "index"
ARCHIVE_DIR = MEMORY_DIR / "archive"
EMOTION_INDEX_FILE = INDEX_DIR / "emotion_index.json"
EVOLUTION_STATE_FILE = WORKSPACE / "memory" / "state" / "evolution_state.json"
EVOLUTION_REPORT_FILE = WORKSPACE / "docs" / "evolution-report.md"


@dataclass
class RetrievalConfig:
    """检索配置"""
    top_k: int = 5
    min_similarity: float = 0.3
    emotion_boost: float = 0.1  # 情感加成权重
    value_boost: float = 0.15  # 价值评分加成权重
    time_decay_factor: float = 0.95  # 时间衰减因子
    diversity_factor: float = 0.2  # 多样性因子


@dataclass
class ABTestResult:
    """A/B 测试结果"""
    test_id: str
    config_a: Dict[str, Any]
    config_b: Dict[str, Any]
    accuracy_a: float
    accuracy_b: float
    sample_size: int
    winner: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class MemoryValue:
    """记忆价值评估"""
    entry_id: str
    reference_count: int
    emotion_intensity: float
    time_score: float
    content_length: int
    keyword_density: float
    total_score: float


def load_evolution_state() -> Dict[str, Any]:
    """加载自进化状态"""
    if EVOLUTION_STATE_FILE.exists():
        try:
            with open(EVOLUTION_STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load evolution state: {e}")
    
    return {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "current_config": asdict(RetrievalConfig()),
        "ab_tests": [],
        "optimizations": [],
        "archive_history": [],
        "statistics": {
            "total_archived": 0,
            "total_optimizations": 0,
            "avg_accuracy_improvement": 0.0
        }
    }


def save_evolution_state(state: Dict[str, Any]):
    """保存自进化状态"""
    EVOLUTION_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(EVOLUTION_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Saved evolution state to {EVOLUTION_STATE_FILE}")


def load_emotion_index() -> Dict[str, Any]:
    """加载情感索引"""
    if EMOTION_INDEX_FILE.exists():
        try:
            with open(EMOTION_INDEX_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load emotion index: {e}")
    
    return {"entries": {}, "statistics": {}}


def calculate_time_score(created_at: str, decay_factor: float = 0.95) -> float:
    """
    计算时间衰减分数
    越近的记忆得分越高
    """
    try:
        created = datetime.fromisoformat(created_at)
        days_old = (datetime.now() - created).days
        
        # 指数衰减
        score = decay_factor ** days_old
        
        # 最低不低于 0.1
        return max(0.1, score)
        
    except Exception:
        return 0.5


def calculate_memory_value(entry_id: str, entry_data: Dict[str, Any], 
                           emotion_index: Dict[str, Any]) -> MemoryValue:
    """
    计算记忆的综合价值评分
    
    评分因素：
    1. 引用频率 (0-1)
    2. 情感强度 (0-1)
    3. 时间衰减 (0-1)
    4. 内容长度 (0-1)
    5. 关键词密度 (0-1)
    """
    # 引用频率
    ref_count = entry_data.get("reference_count", 0)
    ref_score = min(ref_count / 10, 1.0)  # 10次引用达到满分
    
    # 情感强度
    emotion_tag = entry_data.get("emotion_tag", {})
    emotion_intensity = emotion_tag.get("confidence", 0.5)
    
    # 时间衰减
    created_at = entry_data.get("created_at", datetime.now().isoformat())
    time_score = calculate_time_score(created_at)
    
    # 内容长度
    content_preview = entry_data.get("content_preview", "")
    content_length = len(content_preview)
    length_score = min(content_length / 500, 1.0)  # 500字符达到满分
    
    # 关键词密度
    keywords = emotion_tag.get("keywords_matched", [])
    keyword_density = min(len(keywords) / 5, 1.0) if keywords else 0.0
    
    # 综合评分（加权平均）
    weights = {
        "reference": 0.25,
        "emotion": 0.20,
        "time": 0.25,
        "length": 0.15,
        "keyword": 0.15
    }
    
    total_score = (
        ref_score * weights["reference"] +
        emotion_intensity * weights["emotion"] +
        time_score * weights["time"] +
        length_score * weights["length"] +
        keyword_density * weights["keyword"]
    )
    
    return MemoryValue(
        entry_id=entry_id,
        reference_count=ref_count,
        emotion_intensity=emotion_intensity,
        time_score=time_score,
        content_length=content_length,
        keyword_density=keyword_density,
        total_score=total_score
    )


def run_ab_test(config_a: RetrievalConfig, config_b: RetrievalConfig,
                test_queries: List[Dict[str, Any]]) -> ABTestResult:
    """
    运行 A/B 测试比较两种检索配置
    
    Args:
        config_a: 配置 A
        config_b: 配置 B
        test_queries: 测试查询列表，每个包含 query 和 expected_sources
    
    Returns:
        A/B 测试结果
    """
    test_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def evaluate_config(config: RetrievalConfig) -> float:
        """评估单个配置的准确率"""
        correct = 0
        total = len(test_queries)
        
        for test in test_queries:
            query = test["query"]
            expected = set(test.get("expected_sources", []))
            
            # 模拟检索（实际实现需要调用 search_memory.py）
            # 这里使用简化的评估逻辑
            try:
                result = subprocess.run(
                    ["python3", str(WORKSPACE / "scripts" / "search_memory.py"), 
                     query, "-k", str(config.top_k)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # 解析结果
                output = result.stdout
                for src in expected:
                    if src in output:
                        correct += 1
                        break
                        
            except Exception as e:
                logger.warning(f"Search failed for query '{query}': {e}")
        
        return correct / total if total > 0 else 0.0
    
    accuracy_a = evaluate_config(config_a)
    accuracy_b = evaluate_config(config_b)
    
    # 确定胜者
    if accuracy_a > accuracy_b + 0.05:  # 5% 显著性阈值
        winner = "A"
    elif accuracy_b > accuracy_a + 0.05:
        winner = "B"
    else:
        winner = "tie"
    
    return ABTestResult(
        test_id=test_id,
        config_a=asdict(config_a),
        config_b=asdict(config_b),
        accuracy_a=accuracy_a,
        accuracy_b=accuracy_b,
        sample_size=len(test_queries),
        winner=winner
    )


def auto_archive_low_value(threshold: float = 0.3, dry_run: bool = False) -> List[Dict[str, Any]]:
    """
    自动归档低价值记忆
    
    Args:
        threshold: 价值阈值，低于此值的记忆将被归档
        dry_run: 仅模拟，不实际执行
    
    Returns:
        归档的记忆列表
    """
    emotion_index = load_emotion_index()
    archived = []
    
    for entry_id, entry_data in emotion_index.get("entries", {}).items():
        value = calculate_memory_value(entry_id, entry_data, emotion_index)
        
        if value.total_score < threshold:
            # 准备归档信息
            archive_info = {
                "entry_id": entry_id,
                "source": entry_data.get("source", "unknown"),
                "content_preview": entry_data.get("content_preview", ""),
                "value_score": value.total_score,
                "archived_at": datetime.now().isoformat(),
                "reason": f"价值评分 {value.total_score:.2f} 低于阈值 {threshold}"
            }
            
            if not dry_run:
                # 创建归档目录
                ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
                
                # 移动到归档文件
                archive_file = ARCHIVE_DIR / f"archived_{entry_id}.json"
                with open(archive_file, 'w', encoding='utf-8') as f:
                    json.dump(archive_info, f, ensure_ascii=False, indent=2)
                
                # 从索引中移除
                del emotion_index["entries"][entry_id]
            
            archived.append(archive_info)
    
    # 保存更新后的索引
    if not dry_run and archived:
        # 更新统计
        if "statistics" not in emotion_index:
            emotion_index["statistics"] = {}
        
        # 重新计算统计
        from emotion_tagger import update_statistics
        emotion_index["statistics"] = update_statistics(emotion_index)
        
        # 保存索引
        with open(EMOTION_INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(emotion_index, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Archived {len(archived)} low-value memories (threshold={threshold})")
    
    return archived


def optimize_retrieval_params() -> Tuple[RetrievalConfig, List[str]]:
    """
    基于历史数据优化检索参数
    
    Returns:
        (优化后的配置, 优化建议列表)
    """
    state = load_evolution_state()
    suggestions = []
    
    # 分析历史 A/B 测试结果
    ab_tests = state.get("ab_tests", [])
    
    if len(ab_tests) >= 3:
        # 统计哪种配置更常胜出
        config_wins = {}
        
        for test in ab_tests:
            winner = test.get("winner", "tie")
            if winner == "A":
                config = tuple(sorted(test["config_a"].items()))
                config_wins[config] = config_wins.get(config, 0) + 1
            elif winner == "B":
                config = tuple(sorted(test["config_b"].items()))
                config_wins[config] = config_wins.get(config, 0) + 1
        
        # 选择最常获胜的配置参数
        if config_wins:
            best_config = max(config_wins.items(), key=lambda x: x[1])
            suggestions.append(f"基于 {len(ab_tests)} 次 A/B 测试，推荐配置: {dict(best_config[0])}")
    
    # 分析情感分布
    emotion_index = load_emotion_index()
    stats = emotion_index.get("statistics", {})
    
    emotion_dist = stats.get("emotion_distribution", {})
    if emotion_dist:
        # 找出主导情感
        dominant_emotion = max(emotion_dist.items(), key=lambda x: x[1])
        if dominant_emotion[1] > sum(emotion_dist.values()) * 0.5:
            suggestions.append(f"主导情感为 '{dominant_emotion[0]}'，建议增加情感权重")
    
    # 分析价值分布
    value_dist = stats.get("value_distribution", {})
    if value_dist:
        high_value_count = sum(value_dist.get(str(i), 0) for i in range(4, 6))
        total = sum(value_dist.values())
        
        if total > 0 and high_value_count / total > 0.3:
            suggestions.append(f"高价值记忆占比 {high_value_count/total:.1%}，建议降低 value_boost")
        elif total > 0 and high_value_count / total < 0.1:
            suggestions.append(f"高价值记忆占比 {high_value_count/total:.1%}，建议提高 value_boost")
    
    # 生成优化后的配置
    current_config = state.get("current_config", {})
    optimized_config = RetrievalConfig(**current_config)
    
    # 应用优化规则
    if "情感权重" in str(suggestions):
        optimized_config.emotion_boost = min(0.2, optimized_config.emotion_boost + 0.02)
    
    if "value_boost" in str(suggestions):
        if "降低" in str(suggestions):
            optimized_config.value_boost = max(0.05, optimized_config.value_boost - 0.02)
        elif "提高" in str(suggestions):
            optimized_config.value_boost = min(0.3, optimized_config.value_boost + 0.02)
    
    return optimized_config, suggestions


def generate_evolution_report(state: Dict[str, Any], 
                              optimization_suggestions: List[str]) -> str:
    """生成自进化优化报告"""
    lines = []
    lines.append("# 记忆系统自进化优化报告")
    lines.append(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # 当前状态
    lines.append("## 当前状态")
    lines.append(f"- 版本: {state.get('version', 'N/A')}")
    lines.append(f"- 创建时间: {state.get('created_at', 'N/A')}")
    lines.append("")
    
    # 当前检索配置
    current_config = state.get("current_config", {})
    lines.append("## 当前检索配置")
    lines.append("```json")
    lines.append(json.dumps(current_config, indent=2, ensure_ascii=False))
    lines.append("```")
    lines.append("")
    
    # A/B 测试历史
    ab_tests = state.get("ab_tests", [])
    lines.append(f"## A/B 测试历史 ({len(ab_tests)} 次)")
    lines.append("")
    
    if ab_tests:
        lines.append("| 测试ID | A 准确率 | B 准确率 | 胜者 | 样本量 |")
        lines.append("|--------|----------|----------|------|--------|")
        
        for test in ab_tests[-10:]:  # 最近 10 次
            lines.append(f"| {test['test_id']} | {test['accuracy_a']:.1%} | {test['accuracy_b']:.1%} | {test['winner']} | {test['sample_size']} |")
        lines.append("")
    
    # 优化建议
    lines.append("## 优化建议")
    if optimization_suggestions:
        for i, suggestion in enumerate(optimization_suggestions, 1):
            lines.append(f"{i}. {suggestion}")
    else:
        lines.append("暂无优化建议")
    lines.append("")
    
    # 归档历史
    archive_history = state.get("archive_history", [])
    stats = state.get("statistics", {})
    lines.append("## 归档统计")
    lines.append(f"- 总归档数: {stats.get('total_archived', 0)}")
    lines.append(f"- 总优化次数: {stats.get('total_optimizations', 0)}")
    lines.append(f"- 平均准确率提升: {stats.get('avg_accuracy_improvement', 0):.1%}")
    lines.append("")
    
    # 最近归档
    if archive_history:
        lines.append("### 最近归档的记忆")
        for entry in archive_history[-5:]:
            lines.append(f"- [{entry['archived_at']}] {entry['source']}: {entry['reason']}")
        lines.append("")
    
    return '\n'.join(lines)


def run_evolution_cycle(dry_run: bool = False, archive_threshold: float = 0.3) -> Dict[str, Any]:
    """
    运行一次完整的自进化周期
    
    步骤:
    1. 评估当前记忆价值
    2. 归档低价值记忆
    3. 优化检索参数
    4. 生成报告
    """
    logger.info("Starting evolution cycle...")
    
    state = load_evolution_state()
    
    # 1. 归档低价值记忆
    archived = auto_archive_low_value(threshold=archive_threshold, dry_run=dry_run)
    
    # 2. 优化检索参数
    optimized_config, suggestions = optimize_retrieval_params()
    
    # 3. 更新状态
    if not dry_run:
        state["current_config"] = asdict(optimized_config)
        state["archive_history"].extend(archived)
        state["statistics"]["total_archived"] = state["statistics"].get("total_archived", 0) + len(archived)
        state["statistics"]["total_optimizations"] = state["statistics"].get("total_optimizations", 0) + 1
        
        save_evolution_state(state)
    
    # 4. 生成报告
    report = generate_evolution_report(state, suggestions)
    
    # 保存报告
    EVOLUTION_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EVOLUTION_REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"Evolution cycle complete. Archived: {len(archived)}, Suggestions: {len(suggestions)}")
    
    return {
        "archived_count": len(archived),
        "suggestions": suggestions,
        "optimized_config": asdict(optimized_config),
        "report_path": str(EVOLUTION_REPORT_FILE)
    }


def simulate_ab_test(sample_size: int = 5) -> ABTestResult:
    """
    模拟一次 A/B 测试
    使用预设的测试查询集
    """
    # 预设测试查询
    test_queries = [
        {"query": "Phi-4-mini 下载决定", "expected_sources": ["MEMORY.md", "2026-03-18.md"]},
        {"query": "iflow 工具集成", "expected_sources": ["MEMORY.md", "2026-03-18.md"]},
        {"query": "记忆系统架构", "expected_sources": ["MEMORY.md"]},
        {"query": "qwen2.5 测试结果", "expected_sources": ["2026-03-18.md"]},
        {"query": "语义搜索功能", "expected_sources": ["MEMORY.md", "2026-03-18.md"]},
        {"query": "待办事项跟踪", "expected_sources": ["MEMORY.md"]},
        {"query": "模型状态确认", "expected_sources": ["2026-03-18.md"]},
        {"query": "记忆索引构建", "expected_sources": ["MEMORY.md", "2026-03-18.md"]},
    ]
    
    # 选择测试样本
    import random
    selected = random.sample(test_queries, min(sample_size, len(test_queries)))
    
    # 创建两种配置
    config_a = RetrievalConfig(top_k=5, min_similarity=0.3, emotion_boost=0.1, value_boost=0.15)
    config_b = RetrievalConfig(top_k=10, min_similarity=0.2, emotion_boost=0.15, value_boost=0.2)
    
    # 运行测试
    result = run_ab_test(config_a, config_b, selected)
    
    # 保存结果
    state = load_evolution_state()
    state["ab_tests"].append(asdict(result))
    save_evolution_state(state)
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="记忆系统自进化引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行完整的自进化周期
  python self_evolution_engine.py evolve
  
  # 模拟运行（不实际修改数据）
  python self_evolution_engine.py evolve --dry-run
  
  # 运行 A/B 测试
  python self_evolution_engine.py ab-test --sample-size 5
  
  # 归档低价值记忆
  python self_evolution_engine.py archive --threshold 0.3
  
  # 查看优化建议
  python self_evolution_engine.py suggest
  
  # 生成报告
  python self_evolution_engine.py report
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 自进化周期命令
    evolve_parser = subparsers.add_parser("evolve", help="运行自进化周期")
    evolve_parser.add_argument("--dry-run", action="store_true", help="模拟运行，不修改数据")
    evolve_parser.add_argument("--threshold", type=float, default=0.3, help="归档价值阈值")
    
    # A/B 测试命令
    ab_parser = subparsers.add_parser("ab-test", help="运行 A/B 测试")
    ab_parser.add_argument("--sample-size", type=int, default=5, help="测试样本数量")
    
    # 归档命令
    archive_parser = subparsers.add_parser("archive", help="归档低价值记忆")
    archive_parser.add_argument("--threshold", type=float, default=0.3, help="价值阈值")
    archive_parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    
    # 建议命令
    subparsers.add_parser("suggest", help="查看优化建议")
    
    # 报告命令
    subparsers.add_parser("report", help="生成进化报告")
    
    # 评估价值命令
    value_parser = subparsers.add_parser("evaluate", help="评估记忆价值")
    value_parser.add_argument("--top", type=int, default=10, help="显示前 N 个")
    
    args = parser.parse_args()
    
    if args.command == "evolve":
        result = run_evolution_cycle(dry_run=args.dry_run, archive_threshold=args.threshold)
        print(f"\n✅ 自进化周期完成")
        print(f"   归档记忆: {result['archived_count']}")
        print(f"   优化建议: {len(result['suggestions'])}")
        print(f"   报告路径: {result['report_path']}")
        
        if result['suggestions']:
            print("\n📋 优化建议:")
            for i, s in enumerate(result['suggestions'], 1):
                print(f"   {i}. {s}")
        
    elif args.command == "ab-test":
        result = simulate_ab_test(args.sample_size)
        print(f"\n📊 A/B 测试完成")
        print(f"   测试ID: {result.test_id}")
        print(f"   配置 A 准确率: {result.accuracy_a:.1%}")
        print(f"   配置 B 准确率: {result.accuracy_b:.1%}")
        print(f"   胜者: {result.winner}")
        print(f"   样本量: {result.sample_size}")
        
    elif args.command == "archive":
        archived = auto_archive_low_value(threshold=args.threshold, dry_run=args.dry_run)
        action = "模拟归档" if args.dry_run else "已归档"
        print(f"\n📦 {action} {len(archived)} 条低价值记忆")
        
        for entry in archived[:5]:
            print(f"   - {entry['source']}: 价值 {entry['value_score']:.2f}")
        if len(archived) > 5:
            print(f"   ... 还有 {len(archived) - 5} 条")
            
    elif args.command == "suggest":
        _, suggestions = optimize_retrieval_params()
        print("\n💡 优化建议:")
        if suggestions:
            for i, s in enumerate(suggestions, 1):
                print(f"   {i}. {s}")
        else:
            print("   暂无优化建议")
            
    elif args.command == "report":
        state = load_evolution_state()
        _, suggestions = optimize_retrieval_params()
        report = generate_evolution_report(state, suggestions)
        print(report)
        
    elif args.command == "evaluate":
        emotion_index = load_emotion_index()
        values = []
        
        for entry_id, entry_data in emotion_index.get("entries", {}).items():
            value = calculate_memory_value(entry_id, entry_data, emotion_index)
            values.append((entry_id, value))
        
        # 按价值排序
        values.sort(key=lambda x: x[1].total_score, reverse=True)
        
        print(f"\n📊 记忆价值评估 (前 {args.top} 个):")
        print("=" * 70)
        
        for i, (entry_id, value) in enumerate(values[:args.top], 1):
            print(f"\n{i}. {entry_id}")
            print(f"   总分: {value.total_score:.2f}")
            print(f"   引用: {value.reference_count}, 情感: {value.emotion_intensity:.2f}, 时间: {value.time_score:.2f}")
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
