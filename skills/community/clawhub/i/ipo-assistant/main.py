#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股申购助手 - 主入口
提供新股申购日历、基本面分析、中签率预测等功能
"""

import sys
from datetime import datetime, timedelta
from ipo_calendar import get_today_ipos, get_week_ipos
from ipo_analysis import analyze_ipo
from ipo_prediction import predict_win_rate, predict_premium
from ipo_stats import get_history_stats, get_industry_ranking, compare_ipos
from ipo_reminder import check_today_reminder, check_weekly_reminder

# ============ 配置 ============
CACHE_FILE = "data/ipo_history.csv"
CACHE_EXPIRE_MINUTES = 30

# ============ 主功能函数 ============

def get_today_subscribable():
    """获取今日可申购新股"""
    today = datetime.now().strftime("%Y-%m-%d")
    result = get_today_ipos(today)
    return format_ipo_output(result, today)

def get_week_subscribable():
    """获取本周可申购新股"""
    today = datetime.now()
    week_end = today + timedelta(days=7)
    result = get_week_ipos(today.strftime("%Y-%m-%d"), week_end.strftime("%Y-%m-%d"))
    return format_week_output(result)

def analyze_new_ipo(stock_code):
    """分析新股"""
    result = analyze_ipo(stock_code)
    return format_analysis_output(result)

def predict_ipo_win_rate(stock_code):
    """预测中签率"""
    result = predict_win_rate(stock_code)
    return format_win_rate_output(result)

def predict_ipo_premium(stock_code):
    """预测上市溢价"""
    result = predict_premium(stock_code)
    return format_premium_output(result)

# ============ 格式化输出 ============

def format_ipo_output(data, date):
    """格式化新股列表输出"""
    if not data:
        return f"📭 今日 ({date}) 暂无可申购新股\n\n💡 提示：新股申购通常在交易日（周一至周五）进行"
    
    lines = [f"📅 今日可申购新股 ({date})\n"]
    for i, ipo in enumerate(data, 1):
        lines.append(f"{i}. {ipo['name']} ({ipo['code']})")
        if ipo.get('issue_price', 0) > 0:
            lines.append(f"   - 发行价：{ipo['issue_price']}元")
        else:
            lines.append(f"   - 发行价：待公布")
        if ipo.get('issue_pe', 0) > 0:
            lines.append(f"   - 发行市盈率：{ipo['issue_pe']}倍")
        if ipo.get('industry_pe', 0) > 0:
            lines.append(f"   - 行业市盈率：{ipo['industry_pe']}倍")
        if ipo.get('online_max', 0) > 0:
            lines.append(f"   - 申购上限：{ipo['online_max']:,}股")
        if ipo.get('total_issue', 0) > 0:
            lines.append(f"   - 发行总量：{ipo['total_issue']}万股")
        lines.append(f"   - 行业：{ipo.get('industry', '未知')}")
        lines.append(f"   - 板块：{ipo.get('board', '未知')}")
        lines.append(f"   💡 建议：{ipo['recommendation']}")
        lines.append("")
    
    return "\n".join(lines)

def format_week_output(data):
    """格式化周历输出"""
    if not data:
        return "📭 本周暂无可申购新股"
    
    lines = ["📆 本周新股申购日历\n"]
    for item in data:
        date_str = item['date']
        if ' ' in date_str:
            date_str = date_str.split(' ')[0]
        price_str = f"{item['price']}元" if item.get('price', 0) > 0 else "待公布"
        lines.append(f"{date_str}: {item['name']} ({item['code']}) - 发行价{price_str}")
    
    return "\n".join(lines)

def format_analysis_output(data):
    """格式化分析结果输出"""
    lines = [
        f"📊 {data['name']} ({data['code']}) 分析",
        "",
        f"• 发行价：{data['price']}元",
        f"• 发行市盈率：{data['pe']}倍（行业平均 {data['industry_pe']}倍）",
        f"• 行业：{data['industry']}",
        f"• 2025 年营收：{data['revenue']}亿元（{data['revenue_growth']}%）",
        f"• 净利润：{data['net_profit']}亿元（{data['profit_growth']}%）",
        f"• 毛利率：{data['gross_margin']}%（行业平均 {data['industry_margin']}%）",
        "",
        f"💡 建议：{data['recommendation']}",
    ]
    return "\n".join(lines)

def format_win_rate_output(data):
    """格式化中签率预测输出"""
    lines = [
        f"🎯 {data['name']} 中签率预测",
        "",
        f"• 预测中签率：{data['predicted_rate']}%",
        f"• 历史平均：{data['history_avg']}%",
        f"• 预计冻结资金：{data['frozen_funds']}亿元",
        f"• 发行规模：{data['issue_size']}亿元",
        "",
        f"📊 参考依据：",
        f"  - 发行规模：{'小' if data['issue_size'] < 10 else '中' if data['issue_size'] < 50 else '大'}",
        f"  - 行业热度：{data['industry_hot']}",
        f"  - 市场环境：{data['market_condition']}",
    ]
    return "\n".join(lines)

def format_premium_output(data):
    """格式化溢价预测输出"""
    lines = [
        f"📈 {data['name']} 上市溢价预测",
        "",
        f"• 预测首日涨幅：{data['predicted_premium']}%",
        f"• 合理区间：{data['premium_range'][0]}% - {data['premium_range'][1]}%",
        f"• 预测上市价格：{data['predicted_price']}元",
        f"• 置信度：{data['confidence']}",
        "",
        f"📊 参考依据：",
        f"  - 同行业新股平均涨幅：{data['industry_avg']}%",
        f"  - 近 3 月新股平均涨幅：{data['recent_avg']}%",
        f"  - 发行估值水平：{data['valuation_level']}",
    ]
    return "\n".join(lines)

# ============ CLI 入口 ============

def show_history_stats():
    """显示历史统计"""
    stats = get_history_stats(90)
    if not stats:
        return "📭 暂无历史数据"
    
    lines = [
        "📊 近 90 天新股统计",
        "",
        f"• 新股数量：{stats['total']}只",
        f"• 平均涨幅：{stats['avg_gain']}%",
        f"• 平均中签率：{stats['avg_win_rate']}‰",
        f"• 最高涨幅：{stats['max_gain']['name']} ({stats['max_gain']['gain']}%)",
        f"• 最低涨幅：{stats['min_gain']['name']} ({stats['min_gain']['gain']}%)",
        "",
        "📈 行业涨幅排行:",
    ]
    
    ranking = get_industry_ranking()
    for i, item in enumerate(ranking, 1):
        lines.append(f"  {i}. {item['industry']}: {item['avg_gain']}% ({item['count']}只)")
    
    return "\n".join(lines)


def show_compare(codes):
    """对比新股"""
    if len(codes) < 2:
        return "⚠️ 请提供至少 2 个股票代码进行对比"
    
    comparison = compare_ipos(codes)
    
    lines = ["🔄 新股对比\n"]
    for ipo in comparison:
        lines.append(f"{ipo['name']} ({ipo['code']}):")
        lines.append(f"  发行价：{ipo['issue_price']}元")
        if ipo.get('first_day_gain'):
            lines.append(f"  首日涨幅：{ipo['first_day_gain']}%")
        if ipo.get('win_rate'):
            lines.append(f"  中签率：{ipo['win_rate']*1000:.2f}‰")
        lines.append(f"  行业：{ipo['industry']}")
        lines.append(f"  板块：{ipo['board']}")
        lines.append("")
    
    return "\n".join(lines)


def print_help():
    """打印帮助信息"""
    help_text = """
新股申购助手 - 使用指南

命令:
  today          - 查询今日可申购新股
  week           - 查询本周可申购新股
  analyze <代码>  - 分析指定新股
  winrate <代码>  - 预测中签率
  premium <代码>  - 预测上市溢价
  stats          - 查看历史统计
  compare <代码 1> <代码 2> ... - 对比新股
  reminder       - 今日申购提醒
  help           - 显示帮助信息

示例:
  python main.py today
  python main.py analyze 601127
  python main.py winrate 601127
  python main.py premium 601127
  python main.py stats
  python main.py compare 301234 688123
  python main.py reminder
"""
    print(help_text)

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "today":
        print(get_today_subscribable())
    
    elif command == "week":
        print(get_week_subscribable())
    
    elif command == "analyze" and len(sys.argv) >= 3:
        stock_code = sys.argv[2]
        print(analyze_new_ipo(stock_code))
    
    elif command == "winrate" and len(sys.argv) >= 3:
        stock_code = sys.argv[2]
        print(predict_ipo_win_rate(stock_code))
    
    elif command == "premium" and len(sys.argv) >= 3:
        stock_code = sys.argv[2]
        print(predict_ipo_premium(stock_code))
    
    elif command == "stats":
        print(show_history_stats())
    
    elif command == "compare" and len(sys.argv) >= 4:
        codes = sys.argv[2:]
        print(show_compare(codes))
    
    elif command == "reminder":
        result = check_today_reminder()
        print(result['message'])
    
    elif command == "help":
        print_help()
    
    else:
        print(f"未知命令：{command}")
        print_help()

if __name__ == "__main__":
    main()
