#!/usr/bin/env python3
"""
飞书卡片模板库
提供标准化的卡片模板，支持新闻、机票、任务等多种场景
"""

from typing import Dict, Any, List, Optional

def build_news_card(news_items: List[Dict[str, str]], 
                   title: str = "📰 今日新闻简报") -> Dict[str, Any]:
    """构建新闻简报卡片"""
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": "blue"
        },
        "elements": []
    }
    
    for item in news_items:
        # 每条新闻
        card["elements"].append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**[{item['category']}] {item['title']}**\n*来源：{item['source']} | 时间：{item['time']}*"
            }
        })
        
        # 添加分隔线（除了最后一个）
        if item != news_items[-1]:
            card["elements"].append({"tag": "hr"})
    
    # 添加底部提示
    card["elements"].append({
        "tag": "note",
        "elements": [{
            "tag": "plain_text",
            "content": "💡 每日精选5-7条重要信息，避免信息过载"
        }]
    })
    
    return card

def build_flight_deal_card(flight_info: Dict[str, Any], 
                          title: str = "✈️ 特价机票发现") -> Dict[str, Any]:
    """构建机票特价卡片"""
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": "green"
        },
        "elements": [
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": f"**航线：**\n{flight_info['route']}"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md", 
                            "content": f"**价格：**\n¥{flight_info['price']} (原价¥{flight_info['original_price']})"
                        }
                    }
                ]
            },
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": f"**日期：**\n{flight_info['date']}"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": f"**折扣：**\n{flight_info['discount']}"
                        }
                    }
                ]
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**⚡ 抢购建议：**\n• 价格有效期至：{flight_info['valid_until']}\n• 建议提前{flight_info['book_advance']}天预订\n• 退改政策：{flight_info['refund_policy']}"
                }
            }
        ]
    }
    
    # 添加按钮
    actions = []
    if flight_info.get('booking_url'):
        actions.append({
            "tag": "button",
            "type": "primary",
            "value": {"booking_url": flight_info['booking_url']},
            "text": {"tag": "plain_text", "content": "立即预订"}
        })
    if flight_info.get('detail_url'):
        actions.append({
            "tag": "button",
            "type": "default",
            "value": {"detail_url": flight_info['detail_url']},
            "text": {"tag": "plain_text", "content": "查看详情"}
        })
    
    if actions:
        card["elements"].append({
            "tag": "action",
            "actions": actions
        })
    
    return card

def build_task_management_card(tasks: List[Dict[str, Any]], 
                              title: str = "📋 任务管理") -> Dict[str, Any]:
    """构建任务管理卡片"""
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": "watchet"
        },
        "elements": []
    }
    
    # 任务统计
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.get('status') == 'completed')
    
    card["elements"].append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"**任务进度：** {completed_tasks}/{total_tasks} 已完成"
        }
    })
    
    # 每个任务
    for task in tasks:
        status_icon = "✅" if task.get('status') == 'completed' else "⏳"
        priority_color = "🔴" if task.get('priority') == 'high' else "🟡" if task.get('priority') == 'medium' else "🟢"
        
        card["elements"].append({
            "tag": "div",
            "fields": [
                {
                    "is_short": True,
                    "text": {
                        "tag": "lark_md",
                        "content": f"{status_icon} {task['title']}"
                    }
                },
                {
                    "is_short": True,
                    "text": {
                        "tag": "lark_md",
                        "content": f"{priority_color} {task.get('priority', 'normal')}"
                    }
                }
            ]
        })
        
        if task.get('deadline'):
            card["elements"].append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"⏰ 截止时间：{task['deadline']}"
                }
            })
        
        if task != tasks[-1]:
            card["elements"].append({"tag": "hr"})
    
    return card

def build_simple_info_card(title: str, 
                          content: str, 
                          template: str = "blue",
                          icon: str = "🎯") -> Dict[str, Any]:
    """构建简单信息卡片"""
    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"{icon} {title}"},
            "template": template
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": content
                }
            }
        ]
    }

def build_system_status_card(status: str, 
                           details: Dict[str, str],
                           title: str = "🖥️ 系统状态") -> Dict[str, Any]:
    """构建系统状态卡片"""
    template = "green" if status == "normal" else "red" if status == "error" else "yellow"
    
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": template
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**状态：** {'✅ 正常' if status == 'normal' else '❌ 异常' if status == 'error' else '⚠️ 警告'}"
                }
            }
        ]
    }
    
    # 添加详细信息
    for key, value in details.items():
        card["elements"].append({
            "tag": "div",
            "fields": [
                {
                    "is_short": True,
                    "text": {
                        "tag": "lark_md",
                        "content": f"**{key}：**"
                    }
                },
                {
                    "is_short": True,
                    "text": {
                        "tag": "lark_md",
                        "content": value
                    }
                }
            ]
        })
    
    return card

def build_interactive_card(title: str,
                        content: str,
                        buttons: List[Dict[str, str]],
                        template: str = "blue") -> Dict[str, Any]:
    """构建交互式卡片"""
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": template
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": content
                }
            },
            {
                "tag": "action",
                "actions": []
            }
        ]
    }
    
    # 添加按钮
    for button in buttons:
        button_config = {
            "tag": "button",
            "type": button.get("type", "default"),
            "text": {"tag": "plain_text", "content": button["text"]},
            "value": button.get("value", {"action": button["text"]})
        }
        
        if button.get("url"):
            button_config["url"] = button["url"]
            
        card["elements"][-1]["actions"].append(button_config)
    
    return card

# 预设模板
def get_news_template() -> Dict[str, Any]:
    """获取新闻简报预设模板"""
    return build_news_card([
        {
            "category": "国际新闻",
            "title": "重大科技突破",
            "source": "路透社",
            "time": "2024-02-28 15:30"
        },
        {
            "category": "财经动态",
            "title": "市场分析报告",
            "source": "财经网",
            "time": "2024-02-28 14:20"
        }
    ])

def get_flight_deal_template() -> Dict[str, Any]:
    """获取机票特价预设模板"""
    return build_flight_deal_card({
        "route": "上海 → 东京",
        "price": 899,
        "original_price": 2500,
        "date": "2024-03-15",
        "discount": "3.6折",
        "valid_until": "2024-03-01",
        "book_advance": 30,
        "refund_policy": "可免费改期一次",
        "booking_url": "https://example.com/book",
        "detail_url": "https://example.com/detail"
    })

def get_task_management_template() -> Dict[str, Any]:
    """获取任务管理预设模板"""
    return build_task_management_card([
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
        }
    ])

# 导出所有模板函数
__all__ = [
    'build_news_card',
    'build_flight_deal_card', 
    'build_task_management_card',
    'build_simple_info_card',
    'build_system_status_card',
    'build_interactive_card',
    'get_news_template',
    'get_flight_deal_template',
    'get_task_management_template'
]