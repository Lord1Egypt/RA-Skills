#!/usr/bin/env python3
"""
记忆秘书基础使用示例

演示记忆秘书的 6 大核心功能
"""

import sys
from pathlib import Path

# 添加源代码路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from memory_secretary_lite import MemorySecretaryLite


def example_1_quality_check():
    """示例 1: 记忆质量检查"""
    print("\n" + "=" * 60)
    print("示例 1: 记忆质量检查")
    print("=" * 60)
    
    secretary = MemorySecretaryLite()
    quality = secretary.check_memory_quality()
    
    print(f"\n📊 质量报告:")
    print(f"  总文件数：{quality['total_files']}")
    print(f"  质量评分：{quality['quality_score']}/100")
    print(f"  发现问题：{quality['issue_count']} 个")
    
    if quality['recommendations']:
        print(f"\n💡 优化建议:")
        for i, rec in enumerate(quality['recommendations'], 1):
            print(f"  {i}. {rec}")


def example_2_similar_tasks():
    """示例 2: 重复工作检测"""
    print("\n" + "=" * 60)
    print("示例 2: 重复工作检测")
    print("=" * 60)
    
    secretary = MemorySecretaryLite()
    
    # 模拟任务开始前检查
    task_name = "中证 500 数据收集"
    print(f"\n🔍 任务前检查：{task_name}")
    
    similar = secretary.find_similar_tasks(task_name)
    
    if similar:
        print(f"\n⚠️ 发现 {len(similar)} 个相似任务:")
        for i, task in enumerate(similar[:5], 1):
            print(f"  {i}. {task['task']} (相似度：{task['similarity']:.2f})")
            print(f"     来源：{task['source_file']}")
        print(f"\n💡 建议：先查看历史方案，避免重复劳动")
    else:
        print(f"\n✅ 无相似任务，可以安全执行")


def example_3_success_cases():
    """示例 3: 成功案例提取"""
    print("\n" + "=" * 60)
    print("示例 3: 成功案例提取")
    print("=" * 60)
    
    secretary = MemorySecretaryLite()
    cases = secretary.extract_success_cases()
    
    print(f"\n✅ 成功案例：{len(cases)} 个")
    
    # 显示前 5 个案例
    for i, case in enumerate(cases[:5], 1):
        print(f"\n  {i}. {case['case']}")
        print(f"     标记：{case['marker']}")
        print(f"     来源：{case['source_file']}")


def example_4_work_patterns():
    """示例 4: 工作模式识别"""
    print("\n" + "=" * 60)
    print("示例 4: 工作模式识别")
    print("=" * 60)
    
    secretary = MemorySecretaryLite()
    patterns = secretary.analyze_work_patterns()
    
    print(f"\n📊 工作模式分析:")
    
    if 'frequent_keywords' in patterns and patterns['frequent_keywords']:
        print(f"\n🔑 高频关键词:")
        for keyword, count in patterns['frequent_keywords'][:10]:
            print(f"  • {keyword}: {count} 次")


def example_5_reminders():
    """示例 5: 智能提醒生成"""
    print("\n" + "=" * 60)
    print("示例 5: 智能提醒生成")
    print("=" * 60)
    
    secretary = MemorySecretaryLite()
    
    # 模拟当前任务关键词
    keywords = ["数据收集", "模型优化", "记忆系统"]
    print(f"\n🔔 当前任务关键词：{', '.join(keywords)}")
    
    reminders = secretary.generate_reminders(keywords)
    
    if reminders:
        print(f"\n📋 生成 {len(reminders)} 条提醒:")
        for i, reminder in enumerate(reminders, 1):
            priority_icon = "🔴" if reminder['priority'] == 'high' else "🟡"
            print(f"  {i}. {priority_icon} [{reminder['priority']}] {reminder['message']}")
    else:
        print(f"\n✅ 无特殊提醒")


def example_6_share_report():
    """示例 6: 分享报告生成"""
    print("\n" + "=" * 60)
    print("示例 6: 分享报告生成")
    print("=" * 60)
    
    secretary = MemorySecretaryLite()
    report = secretary.generate_share_report()
    
    print(f"\n📄 分享报告生成完成")
    print(f"  时间戳：{report.get('timestamp', 'N/A')}")
    print(f"  包含内容:")
    print(f"    - 记忆质量报告")
    print(f"    - 成功案例库")
    print(f"    - 工作模式分析")
    print(f"    - 优化建议")


def main():
    """主函数 - 运行所有示例"""
    print("🧠 记忆秘书 - 基础使用示例")
    print("=" * 60)
    print("演示记忆秘书的 6 大核心功能")
    print("=" * 60)
    
    try:
        # 运行所有示例
        example_1_quality_check()
        example_2_similar_tasks()
        example_3_success_cases()
        example_4_work_patterns()
        example_5_reminders()
        example_6_share_report()
        
        print("\n" + "=" * 60)
        print("✅ 所有示例运行完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 示例运行失败：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
