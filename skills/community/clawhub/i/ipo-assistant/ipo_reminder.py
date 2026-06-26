#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股提醒模块
设置定时任务提醒新股申购
"""

from datetime import datetime, timedelta
import json
import os

REMINDER_CONFIG_FILE = "data/reminder_config.json"


def load_reminder_config():
    """加载提醒配置"""
    if not os.path.exists(REMINDER_CONFIG_FILE):
        return {
            'enabled': True,
            'remind_time': '09:00',  # 提醒时间
            'channels': ['feishu'],  # 提醒渠道
            'auto_subscribe': False,  # 是否自动申购（需要券商 API）
        }
    
    try:
        with open(REMINDER_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None


def save_reminder_config(config):
    """保存提醒配置"""
    os.makedirs(os.path.dirname(REMINDER_CONFIG_FILE), exist_ok=True)
    with open(REMINDER_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def create_cron_reminder():
    """
    创建 OpenClaw 定时任务
    
    每天 9:00 检查当日新股并提醒
    """
    cron_job = {
        'name': '新股申购提醒',
        'schedule': {
            'kind': 'cron',
            'expr': '0 9 * * 1-5',  # 周一至周五 9:00
            'tz': 'Asia/Shanghai',
        },
        'payload': {
            'kind': 'agentTurn',
            'message': '请检查今日可申购新股并发送提醒到飞书',
        },
        'sessionTarget': 'isolated',
        'enabled': True,
    }
    
    return cron_job


def check_today_reminder():
    """
    检查今日是否需要提醒
    
    Returns:
        dict: 提醒信息
    """
    from ipo_calendar import get_today_ipos
    
    today = datetime.now().strftime('%Y-%m-%d')
    today_ipos = get_today_ipos(today)
    
    if not today_ipos:
        return {
            'should_remind': False,
            'message': f'📭 今日 ({today}) 无新股申购',
        }
    
    # 生成提醒消息
    message = f"📅 今日新股申购提醒 ({today})\n\n"
    message += f"共有 {len(today_ipos)} 只新股可申购：\n\n"
    
    for i, ipo in enumerate(today_ipos, 1):
        message += f"{i}. {ipo['name']} ({ipo['code']})\n"
        if ipo.get('issue_price', 0) > 0:
            message += f"   发行价：{ipo['issue_price']}元\n"
        message += f"   行业：{ipo.get('industry', '未知')}\n"
        message += f"   板块：{ipo.get('board', '未知')}\n"
        message += f"   💡 {ipo.get('recommendation', '')}\n\n"
    
    message += "⏰ 申购时间：9:30-11:30, 13:00-15:00\n"
    message += "💰 中签公布：T+2 日\n"
    message += "📊 祝好运！"
    
    return {
        'should_remind': True,
        'message': message,
        'ipo_count': len(today_ipos),
    }


def check_weekly_reminder():
    """
    检查本周新股（每周一使用）
    
    Returns:
        dict: 提醒信息
    """
    from ipo_calendar import get_week_ipos
    
    today = datetime.now()
    # 本周一
    monday = today - timedelta(days=today.weekday())
    # 本周日
    sunday = monday + timedelta(days=6)
    
    week_ipos = get_week_ipos(
        monday.strftime('%Y-%m-%d'),
        sunday.strftime('%Y-%m-%d')
    )
    
    if not week_ipos:
        return {
            'should_remind': False,
            'message': '📭 本周暂无新股申购',
        }
    
    # 生成提醒消息
    message = f"📆 本周新股申购日历\n\n"
    message += f"共有 {len(week_ipos)} 只新股：\n\n"
    
    # 按日期分组
    from collections import defaultdict
    by_date = defaultdict(list)
    for ipo in week_ipos:
        by_date[ipo['date']].append(ipo)
    
    for date in sorted(by_date.keys()):
        ipos = by_date[date]
        weekday = datetime.strptime(date.split(' ')[0], '%Y-%m-%d').strftime('%A')
        message += f"{date} ({weekday}): {len(ipos)}只\n"
        for ipo in ipos:
            price = f"{ipo['price']}元" if ipo.get('price', 0) > 0 else '待公布'
            message += f"  • {ipo['name']} ({ipo['code']}) - {price}\n"
        message += "\n"
    
    return {
        'should_remind': True,
        'message': message,
        'ipo_count': len(week_ipos),
    }


def setup_auto_reminder():
    """
    设置自动提醒
    
    需要调用 OpenClaw cron API
    """
    print("设置新股申购自动提醒...")
    print("\n请在 OpenClaw 中执行以下命令：")
    print("\n```bash")
    print("openclaw cron add --name '新股申购提醒' \\")
    print("  --schedule '0 9 * * 1-5' \\")
    print("  --tz 'Asia/Shanghai' \\")
    print("  --payload '{\"kind\":\"agentTurn\",\"message\":\"检查今日新股申购\"}'")
    print("```")
    
    # 保存配置
    config = load_reminder_config()
    config['enabled'] = True
    save_reminder_config(config)
    
    print("\n✅ 提醒配置已保存")


# ============ 测试入口 ============

if __name__ == "__main__":
    print("=" * 60)
    print("新股提醒测试")
    print("=" * 60)
    
    # 今日提醒
    print("\n📅 今日提醒:")
    today = check_today_reminder()
    if today['should_remind']:
        print(today['message'])
    else:
        print(today['message'])
    
    # 本周提醒
    print("\n\n📆 本周提醒:")
    week = check_weekly_reminder()
    if week['should_remind']:
        print(week['message'])
    else:
        print(week['message'])
