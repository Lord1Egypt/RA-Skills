#!/usr/bin/env python3
"""
学习协调器 v2.0.0 增强功能使用示例
"""

import sys
from pathlib import Path

# 添加插件路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from learning_coordinator import LearningCoordinator

def example_effectiveness_integration():
    """有效性反馈集成示例"""
    print("=== 有效性反馈集成示例 ===")
    
    # 初始化增强学习协调器
    config = {
        'enable_effectiveness_integration': True,
        'enhanced_correction_config': {
            'corrections_file': '~/self-improving/corrections.md'
        }
    }
    
    coordinator = LearningCoordinator(config)
    
    # 健康检查
    health = coordinator.health_check()
    print(f"健康状态: {'✅ 健康' if health.get('healthy') else '❌ 不健康'}")
    print(f"增强功能启用: {health.get('enhanced_features', {}).get('feedback_loop_enabled', False)}")
    
    # 记录模式反馈
    pattern_id = "test_pattern_001"
    feedback_result = coordinator.record_pattern_feedback(
        pattern_id=pattern_id,
        was_helpful=True,
        feedback_context={'example': 'unit_conversion'},
        auto_adjust=True
    )
    
    print(f"\n反馈记录结果:")
    print(f"  成功: {feedback_result.get('success', False)}")
    print(f"  阶段调整: {feedback_result.get('stage_adjusted', False)}")
    if feedback_result.get('new_stage'):
        print(f"  新阶段: {feedback_result.get('new_stage')}")
    
    # 获取有效性报告
    report = coordinator.get_pattern_effectiveness_report(pattern_id)
    if 'error' not in report:
        print(f"\n模式有效性报告:")
        print(f"  当前阶段: {report.get('current_stage')}")
        print(f"  帮助比例: {report.get('effectiveness_metrics', {}).get('help_ratio', 0):.2f}")
        print(f"  学习速度: {report.get('learning_speed', {}).get('category', 'unknown')}")
        
        recommendations = report.get('recommendations', [])
        if recommendations:
            print(f"  建议: {recommendations[0]}")
    
    # 获取反馈循环统计
    stats = coordinator.get_feedback_loop_stats()
    print(f"\n反馈循环统计:")
    print(f"  总模式数: {stats.get('total_patterns', 0)}")
    print(f"  平均有效性: {stats.get('effectiveness_distribution', {}).get('average', 0):.2f}")
    print(f"  快速学习比例: {stats.get('learning_efficiency', {}).get('fast_learning_ratio', 0):.2f}")

def example_auto_adjustment():
    """自动调整示例"""
    print("\n=== 自动阶段调整示例 ===")
    
    coordinator = LearningCoordinator()
    
    # 模拟高有效性模式
    high_effect_pattern = {
        'pattern_id': 'high_effect_example',
        'stage': 'pending',
        'correction_ids': ['corr_h1', 'corr_h2', 'corr_h3'],
        'feedback_history': [
            {'timestamp': '2026-03-20T10:00:00Z', 'was_helpful': True},
            {'timestamp': '2026-03-20T11:00:00Z', 'was_helpful': True},
            {'timestamp': '2026-03-20T12:00:00Z', 'was_helpful': True},
        ],
        'created_at': '2026-03-20T10:00:00Z',
    }
    
    # 添加到缓存（模拟）
    coordinator._pattern_cache['high_effect_example'] = high_effect_pattern
    coordinator._recalculate_pattern_effectiveness('high_effect_example')
    
    # 记录反馈（应触发自动提升）
    result = coordinator.record_pattern_feedback(
        pattern_id='high_effect_example',
        was_helpful=True,
        auto_adjust=True
    )
    
    if result.get('stage_adjusted'):
        print(f"✅ 高有效性模式自动提升: {result.get('new_stage')}")
        print(f"   理由: {result.get('reasoning', '')}")
    else:
        print(f"ℹ️  未触发自动提升（可能需要更多数据）")

def example_enhanced_stats():
    """增强统计示例"""
    print("\n=== 增强统计示例 ===")
    
    coordinator = LearningCoordinator()
    
    # 获取增强统计
    stats = coordinator.get_stats()
    
    print(f"插件版本: {stats.get('plugin', 'unknown')}")
    print(f"规则文件: {stats.get('rules_file', 'unknown')}")
    
    enhanced_metrics = stats.get('enhanced_metrics', {})
    if enhanced_metrics:
        print(f"\n增强指标:")
        print(f"  跟踪模式数: {enhanced_metrics.get('total_patterns_tracked', 0)}")
        print(f"  平均有效性: {enhanced_metrics.get('average_effectiveness', 0):.2f}")
        print(f"  反馈覆盖率: {enhanced_metrics.get('feedback_coverage', 0):.2f}")
    
    feedback_stats = stats.get('feedback_loop_stats', {})
    if feedback_stats:
        print(f"\n反馈循环统计:")
        print(f"  总模式数: {feedback_stats.get('total_patterns', 0)}")
        patterns_by_stage = feedback_stats.get('patterns_by_stage', {})
        if patterns_by_stage:
            print(f"  阶段分布: {patterns_by_stage}")

def main():
    """主示例"""
    print("学习协调器 v2.0.0 增强功能示例")
    print("=" * 50)
    
    try:
        example_effectiveness_integration()
        example_auto_adjustment()
        example_enhanced_stats()
        
        print("\n" + "=" * 50)
        print("✅ 示例执行完成")
        print("=" * 50)
        print("\n核心增强功能:")
        print("  • 有效性反馈集成")
        print("  • 自动阶段调整")
        print("  • 学习速度计算")
        print("  • 反馈循环统计")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 示例执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
