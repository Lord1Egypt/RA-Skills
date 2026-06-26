#!/usr/bin/env python3
"""
记忆秘书集成示例

演示如何将记忆秘书集成到现有工作流程中
"""

import sys
from pathlib import Path

# 添加源代码路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from memory_secretary_lite import MemorySecretaryLite


def integrate_with_pilot_check(task_name: str):
    """
    集成到飞行员检查阶段 3
    
    Args:
        task_name: 任务名称
    """
    print("\n🛩️ 飞行员检查阶段 3: 任务前检查")
    print("=" * 60)
    print(f"任务：{task_name}")
    
    secretary = MemorySecretaryLite()
    
    # 检查 1: 重复工作检测
    print("\n📋 检查 1: 重复工作检测")
    similar_tasks = secretary.find_similar_tasks(task_name)
    
    if similar_tasks:
        print(f"  ⚠️ 发现 {len(similar_tasks)} 个相似任务")
        print(f"  建议：查看历史方案，避免重复劳动")
        
        # 显示最相似的 3 个
        for i, task in enumerate(similar_tasks[:3], 1):
            print(f"    {i}. {task['task']} (相似度：{task['similarity']:.2f})")
    else:
        print(f"  ✅ 无相似任务")
    
    # 检查 2: 成功案例参考
    print("\n📋 检查 2: 成功案例参考")
    success_cases = secretary.extract_success_cases()
    
    if success_cases:
        print(f"  ✅ 发现 {len(success_cases)} 个成功案例")
        print(f"  建议：参考历史成功经验")
    else:
        print(f"  ℹ️ 暂无成功案例")
    
    # 检查 3: 常见问题提醒
    print("\n📋 检查 3: 常见问题提醒")
    keywords = task_name.split()
    reminders = secretary.generate_reminders(keywords)
    
    if reminders:
        print(f"  🔔 生成 {len(reminders)} 条提醒")
        for reminder in reminders[:3]:
            print(f"    • [{reminder['priority']}] {reminder['message']}")
    else:
        print(f"  ✅ 无特殊提醒")
    
    # 总结
    print("\n📊 检查总结")
    print("=" * 60)
    
    issues_found = len(similar_tasks) > 0 or len(reminders) > 0
    
    if issues_found:
        print("⚠️ 发现需要注意的事项，建议谨慎执行")
    else:
        print("✅ 检查通过，可以安全执行任务")
    
    print("=" * 60)


def integrate_with_daily_check():
    """集成到每日检查"""
    print("\n📅 每日记忆检查")
    print("=" * 60)
    
    secretary = MemorySecretaryLite()
    
    # 检查记忆质量
    quality = secretary.check_memory_quality()
    
    print(f"\n📊 记忆健康状态:")
    print(f"  总文件数：{quality['total_files']}")
    print(f"  质量评分：{quality['quality_score']}/100")
    print(f"  发现问题：{quality['issue_count']} 个")
    
    # 评估状态
    if quality['quality_score'] >= 90:
        print(f"\n✅ 记忆系统健康状态：优秀")
    elif quality['quality_score'] >= 70:
        print(f"\n👍 记忆系统健康状态：良好")
    elif quality['quality_score'] >= 50:
        print(f"\n⚠️ 记忆系统健康状态：一般")
    else:
        print(f"\n❌ 记忆系统健康状态：需要优化")
    
    # 显示建议
    if quality['recommendations']:
        print(f"\n💡 优化建议:")
        for i, rec in enumerate(quality['recommendations'], 1):
            print(f"  {i}. {rec}")
    
    print("=" * 60)


def integrate_with_workflow():
    """集成到完整工作流程"""
    print("\n🔄 完整工作流程集成")
    print("=" * 60)
    
    # 模拟一个完整的工作流程
    workflow_steps = [
        ("任务接收", "接收新任务：中证 500 数据收集"),
        ("任务前检查", "检查相似任务和成功案例"),
        ("执行任务", "执行数据收集工作"),
        ("任务完成", "记录任务结果到记忆"),
        ("质量检查", "检查记忆文件质量"),
        ("经验总结", "提取成功案例"),
    ]
    
    secretary = MemorySecretaryLite()
    
    for i, (step_name, step_desc) in enumerate(workflow_steps, 1):
        print(f"\n{i}. {step_name}")
        print(f"   {step_desc}")
        
        # 在关键步骤集成记忆秘书
        if step_name == "任务前检查":
            similar = secretary.find_similar_tasks("中证 500 数据收集")
            if similar:
                print(f"   ✅ 发现 {len(similar)} 个相似任务，可参考历史方案")
        
        elif step_name == "任务完成":
            print(f"   ✅ 任务完成，已记录到记忆系统")
        
        elif step_name == "质量检查":
            quality = secretary.check_memory_quality()
            print(f"   ✅ 记忆质量评分：{quality['quality_score']}/100")
        
        elif step_name == "经验总结":
            cases = secretary.extract_success_cases()
            print(f"   ✅ 提取 {len(cases)} 个成功案例")
    
    print("\n" + "=" * 60)
    print("✅ 完整工作流程执行完成")
    print("=" * 60)


def main():
    """主函数 - 运行所有集成示例"""
    print("🔧 记忆秘书集成示例")
    print("=" * 60)
    print("演示如何将记忆秘书集成到现有工作流程")
    print("=" * 60)
    
    try:
        # 示例 1: 集成到飞行员检查
        integrate_with_pilot_check("中证 500 数据收集")
        
        # 示例 2: 集成到每日检查
        integrate_with_daily_check()
        
        # 示例 3: 集成到完整工作流程
        integrate_with_workflow()
        
        print("\n" + "=" * 60)
        print("✅ 所有集成示例运行完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 集成示例运行失败：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
