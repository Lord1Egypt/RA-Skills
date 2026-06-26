#!/usr/bin/env python3
"""
Newsletter Growth Hacker - 主入口
整合订阅者获取、内容优化、A/B 测试和分析功能
"""

import sys
import json
from datetime import datetime

# 导入各模块
from subscriber_acquisition import SubscriberAcquisition
from content_optimizer import ContentOptimizer, SubjectLineGenerator
from analytics_engine import AnalyticsEngine, GrowthTracker, NewsletterMetrics


def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def interactive_menu():
    """交互式菜单"""
    print_header("Newsletter Growth Hacker v1.0")
    print("\n欢迎使用邮件营销增长工具！\n")
    
    while True:
        print("\n请选择功能:")
        print("1. 订阅者获取策略")
        print("2. 内容优化分析")
        print("3. A/B 测试主题行生成")
        print("4. 数据分析与报告")
        print("5. 增长追踪与预测")
        print("0. 退出")
        
        choice = input("\n输入选项 (0-5): ").strip()
        
        if choice == "0":
            print("再见！👋")
            break
        
        elif choice == "1":
            subscriber_acquisition_menu()
        
        elif choice == "2":
            content_optimization_menu()
        
        elif choice == "3":
            ab_test_menu()
        
        elif choice == "4":
            analytics_menu()
        
        elif choice == "5":
            growth_tracking_menu()
        
        else:
            print("无效选项，请重试")


def subscriber_acquisition_menu():
    """订阅者获取策略菜单"""
    print_header("订阅者获取策略")
    
    acquisition = SubscriberAcquisition()
    
    print("\n可用策略:\n")
    strategies = acquisition.get_strategies()
    
    for i, strat in enumerate(strategies, 1):
        print(f"{i}. {strat['name']}")
        print(f"   {strat['description']}")
        print(f"   转化率：{strat['conversion_rate']} | 投入：{strat['effort']} | ROI: {strat['roi']}\n")
    
    # 增长预测
    try:
        current = int(input("\n当前订阅者数量：") or "1000")
        months = int(input("预测月数：") or "6")
        
        print("\n选择策略进行预测:")
        for i, strat in enumerate(strategies, 1):
            print(f"  {i}. {strat['name']}")
        
        strategy_idx = int(input("选项：") or "1") - 1
        if 0 <= strategy_idx < len(strategies):
            projection = acquisition.calculate_projection(
                current_subscribers=current,
                strategy=strategies[strategy_idx]["id"],
                months=months
            )
            
            print(f"\n📈 增长预测 - {projection['strategy']}")
            print(f"   初始订阅者：{projection['initial_subscribers']}")
            print(f"   {months}个月后：{projection['final_subscribers']}")
            print(f"   总增长：{projection['total_growth']}")
            print(f"   月增长率：{projection['growth_rate']}")
    except Exception as e:
        print(f"错误：{e}")


def content_optimization_menu():
    """内容优化菜单"""
    print_header("内容优化分析")
    
    optimizer = ContentOptimizer()
    
    print("\n粘贴您的邮件内容（输入 END 结束）:\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    
    content = "\n".join(lines)
    analysis = optimizer.analyze_content(content)
    
    print("\n📊 内容分析报告:")
    print(f"   字数：{analysis['word_count']}")
    print(f"   段落数：{analysis['paragraph_count']}")
    print(f"   可读性评分：{analysis['readability_score']}/100")
    print(f"   有主题行：{'✓' if analysis['has_subject_line'] else '✗'}")
    print(f"   有 CTA: {'✓' if analysis['has_cta'] else '✗'}")
    
    if analysis["suggestions"]:
        print("\n💡 优化建议:")
        for sug in analysis["suggestions"]:
            print(f"   • {sug}")


def ab_test_menu():
    """A/B 测试菜单"""
    print_header("A/B 测试主题行生成")
    
    generator = SubjectLineGenerator()
    
    topic = input("\n邮件主题/话题：") or "邮件营销"
    goal = input("目标/好处：") or "提升效果"
    variants = int(input("生成变体数量 (1-7):") or "3")
    
    ab_test = generator.create_ab_test(
        topic=topic,
        goal=goal,
        variants=min(max(variants, 1), 7)
    )
    
    print(f"\n🧪 A/B 测试方案")
    print(f"   主题：{ab_test['topic']}")
    print(f"   目标：{ab_test['goal']}")
    
    print("\n测试变体:")
    for i, variant in enumerate(ab_test["variants"], 1):
        print(f"\n   变体{i} [{variant['style']}]:")
        print(f"   「{variant['subject']}」")
        print(f"   预测打开率：{variant['predicted_performance']['open_rate']}")
    
    print("\n测试设置:")
    for key, value in ab_test["test_setup"].items():
        print(f"   • {key}: {value}")


def analytics_menu():
    """分析菜单"""
    print_header("数据分析与报告")
    
    engine = AnalyticsEngine()
    
    print("\n输入邮件活动数据:\n")
    try:
        sent = int(input("发送数量：") or "10000")
        delivered = int(input("送达数量：") or str(int(sent * 0.98)))
        opened = int(input("打开数量：") or str(int(delivered * 0.25)))
        clicked = int(input("点击数量：") or str(int(opened * 0.20)))
        unsubscribed = int(input("退订数量：") or str(int(delivered * 0.003)))
        bounced = int(input("退回数量：") or str(sent - delivered))
        spam = int(input("垃圾邮件投诉：") or "0")
        
        metrics = NewsletterMetrics(
            sent=sent, delivered=delivered, opened=opened,
            clicked=clicked, unsubscribed=unsubscribed,
            bounced=bounced, spam_complaints=spam
        )
        
        report = engine.create_report(
            campaign_name="测试活动",
            metrics=metrics
        )
        
        print("\n📈 核心指标:")
        km = report["key_metrics"]
        print(f"   送达率：{km['delivery_rate']:.1f}%")
        print(f"   打开率：{km['open_rate']:.1f}% ({km['ratings']['open_rate']})")
        print(f"   点击率：{km['click_rate']:.1f}% ({km['ratings']['click_rate']})")
        print(f"   点开比：{km['click_to_open_rate']:.1f}%")
        print(f"   退订率：{km['unsubscribe_rate']:.2f}%")
        
        print("\n💡 数据洞察:")
        for insight in report["insights"]:
            emoji = "🔴" if insight["severity"] == "critical" else \
                    "⚠️" if insight["severity"] == "high" else \
                    "✅" if insight["severity"] == "positive" else "ℹ️"
            print(f"   {emoji} [{insight['category']}] {insight['finding']}")
            print(f"      → {insight['recommendation']}")
        
        if report["action_items"]:
            print("\n📋 行动项:")
            for action in report["action_items"]:
                print(f"   {action['priority']}. [{action['category']}] {action['action']}")
    
    except Exception as e:
        print(f"错误：{e}")


def growth_tracking_menu():
    """增长追踪菜单"""
    print_header("增长追踪与预测")
    
    tracker = GrowthTracker()
    
    print("\n输入历史数据（至少 1 个月）:\n")
    
    months = int(input("要输入的月份数量：") or "3")
    
    for i in range(months):
        print(f"\n第{i+1}个月:")
        date = input(f"  月份 (如 2026-01): ") or f"2026-{i+1:02d}"
        subs = int(input(f"  期末订阅者数：") or "5000")
        new = int(input(f"  新增订阅者：") or "300")
        lost = int(input(f"  流失订阅者：") or "50")
        
        tracker.add_period(date, subs, new, lost)
    
    summary = tracker.get_growth_summary()
    
    print("\n📊 增长摘要:")
    print(f"   追踪周期：{summary['periods_tracked']} 个月")
    print(f"   净增长：{summary['net_growth']} 订阅者")
    print(f"   平均增长率：{summary['average_growth_rate']}")
    print(f"   最佳月份：{summary['best_period']['date']} (+{summary['best_period']['growth']})")
    
    if summary["top_sources"]:
        print("\n   主要来源:")
        for source in summary["top_sources"]:
            print(f"     • {source['source']}: {source['subscribers']}")
    
    # 预测
    forecast_months = int(input("\n预测月数：") or "6")
    projections = tracker.project_growth(forecast_months)
    
    print(f"\n🔮 {forecast_months}个月增长预测:")
    for proj in projections:
        growth_pct = (proj["new_subscribers"] / proj["projected_subscribers"] * 100) if proj["projected_subscribers"] > 0 else 0
        print(f"   第{proj['month']}月：{proj['projected_subscribers']} 订阅者 (+{proj['new_subscribers']}, {growth_pct:.1f}%)")


def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # JSON 模式（用于 API 集成）
        print(json.dumps({"status": "ready", "version": "1.0.0"}))
    else:
        # 交互模式
        interactive_menu()


if __name__ == "__main__":
    main()
