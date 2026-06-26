#!/usr/bin/env python3
"""
飞书卡片发送器 - 基础使用示例
"""

import os
from feishu_card_sender_advanced import AdvancedFeishuCardSender
from feishu_card_templates import (
    build_news_card, build_flight_deal_card, build_simple_info_card
)

def example_1_simple_card():
    """示例1：发送简单卡片"""
    print("🎯 示例1：发送简单卡片")
    
    sender = AdvancedFeishuCardSender()
    
    result = sender.send_simple_card(
        receive_id="ou_7a6d94f4f20cf166aa429d75fe09cc95",  # 替换为你的用户ID
        receive_id_type="open_id",
        title="🎉 欢迎使用飞书卡片",
        content="**飞书卡片发送器**已成功安装！现在可以发送精美的interactive卡片了。",
        template="green"
    )
    
    print(f"✅ 发送成功！消息ID: {result['message_id']}")
    return result

def example_2_news_card():
    """示例2：发送新闻简报卡片"""
    print("📰 示例2：发送新闻简报卡片")
    
    sender = AdvancedFeishuCardSender()
    
    news_items = [
        {
            "category": "🌍 国际新闻",
            "title": "重大科技突破：AI领域新进展",
            "source": "路透社",
            "time": "2小时前"
        },
        {
            "category": "💰 财经动态",
            "title": "市场分析：科技股表现强劲",
            "source": "财经网",
            "time": "1小时前"
        },
        {
            "category": "🚀 科技前沿",
            "title": "新技术发布：改变行业格局",
            "source": "科技日报",
            "time": "30分钟前"
        }
    ]
    
    result = sender.send_news_card(
        receive_id="oc_9d8226f2c01abdb384724b33e8d66c73",  # 替换为你的群组ID
        receive_id_type="chat_id",
        news_items=news_items,
        title="📰 今日新闻简报"
    )
    
    print(f"✅ 新闻简报发送成功！消息ID: {result['message_id']}")
    return result

def example_3_flight_deal_card():
    """示例3：发送机票特价卡片"""
    print("✈️ 示例3：发送机票特价卡片")
    
    sender = AdvancedFeishuCardSender()
    
    flight_info = {
        "route": "上海浦东 ✈️ 东京成田",
        "price": 899,
        "original_price": 2500,
        "date": "2024年3月15日",
        "discount": "3.6折 💰",
        "valid_until": "3月1日 23:59",
        "book_advance": "建议提前30天",
        "refund_policy": "免费改期一次",
        "booking_url": "https://example.com/book",
        "detail_url": "https://example.com/detail"
    }
    
    result = sender.send_flight_deal_card(
        receive_id="ou_7a6d94f4f20cf166aa429d75fe09cc95",
        receive_id_type="open_id",
        flight_info=flight_info
    )
    
    print(f"✅ 机票特价卡片发送成功！消息ID: {result['message_id']}")
    return result

def example_4_task_management_card():
    """示例4：发送任务管理卡片"""
    print("📋 示例4：发送任务管理卡片")
    
    sender = AdvancedFeishuCardSender()
    
    tasks = [
        {
            "title": "完成飞书卡片技能开发",
            "status": "completed",
            "priority": "high",
            "deadline": "2024-02-28"
        },
        {
            "title": "集成新闻推送系统",
            "status": "in_progress",
            "priority": "medium",
            "deadline": "2024-02-29"
        },
        {
            "title": "优化用户界面设计",
            "status": "pending",
            "priority": "low",
            "deadline": "2024-03-01"
        }
    ]
    
    result = sender.send_task_management_card(
        receive_id="ou_7a6d94f4f20cf166aa429d75fe09cc95",
        receive_id_type="open_id",
        tasks=tasks,
        title="📋 本周任务进度"
    )
    
    print(f"✅ 任务管理卡片发送成功！消息ID: {result['message_id']}")
    return result

def example_5_system_status_card():
    """示例5：发送系统状态卡片"""
    print("🖥️ 示例5：发送系统状态卡片")
    
    sender = AdvancedFeishuCardSender()
    
    status = "normal"  # normal, warning, error
    details = {
        "系统状态": "✅ 运行正常",
        "响应时间": "120ms",
        "在线用户": "1,234人",
        "最后检查": "刚刚"
    }
    
    result = sender.send_system_status_card(
        receive_id="ou_7a6d94f4f20cf166aa429d75fe09cc95",
        receive_id_type="open_id",
        status=status,
        details=details,
        title="🖥️ 系统状态监控"
    )
    
    print(f"✅ 系统状态卡片发送成功！消息ID: {result['message_id']}")
    return result

def example_6_interactive_card():
    """示例6：发送交互式卡片"""
    print("🎮 示例6：发送交互式卡片")
    
    sender = AdvancedFeishuCardSender()
    
    buttons = [
        {
            "type": "primary",
            "text": "确认收到",
            "value": {"action": "confirm"}
        },
        {
            "type": "default", 
            "text": "查看详情",
            "url": "https://example.com/detail"
        },
        {
            "type": "danger",
            "text": "标记异常",
            "value": {"action": "report_error"}
        }
    ]
    
    result = sender.send_interactive_card_with_buttons(
        receive_id="ou_7a6d94f4f20cf166aa429d75fe09cc95",
        receive_id_type="open_id",
        title="🎮 交互式测试",
        content="请点击下方按钮进行交互测试：\n\n**支持功能：**\n• 确认收到消息\n• 跳转到详情页面\n• 报告异常情况",
        buttons=buttons,
        template="turquoise"
    )
    
    print(f"✅ 交互式卡片发送成功！消息ID: {result['message_id']}")
    return result

def main():
    """运行所有示例"""
    print("🚀 飞书卡片发送器 - 基础使用示例")
    print("=" * 60)
    
    # 检查环境变量
    if not os.getenv("FEISHU_APP_ID") or not os.getenv("FEISHU_APP_SECRET"):
        print("❌ 请先设置环境变量：")
        print("   export FEISHU_APP_ID='your_app_id'")
        print("   export FEISHU_APP_SECRET='your_app_secret'")
        return
    
    examples = [
        example_1_simple_card,
        example_2_news_card,
        example_3_flight_deal_card,
        example_4_task_management_card,
        example_5_system_status_card,
        example_6_interactive_card
    ]
    
    results = []
    for example in examples:
        try:
            result = example()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ 示例执行失败: {e}")
            print()
    
    print("=" * 60)
    print(f"🎉 完成！成功执行了 {len(results)} 个示例")
    print("\n📚 更多用法请参考：")
    print("   • feishu_card_integration_guide.md - 集成指南")
    print("   • feishu_card_templates.py - 模板库")
    print("   • AdvancedFeishuCardSender 类文档")

if __name__ == "__main__":
    main()