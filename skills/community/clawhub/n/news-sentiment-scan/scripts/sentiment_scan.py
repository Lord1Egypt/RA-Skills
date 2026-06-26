#!/usr/bin/env python3
"""
舆情监控与情绪分析脚本
扫描新闻、公告、社交媒体，进行情绪打分
"""

import sys
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict

try:
    import yfinance as yf
    import pandas as pd
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"缺少依赖: {e}，请运行: pip install yfinance pandas"}))
    sys.exit(1)


# ==================== 情绪词典 ====================

POSITIVE_WORDS = [
    "超预期", "大涨", "涨停", "突破", "增长", "盈利", "买入", "推荐", "增持", "上调",
    "看好", "强劲", "创新高", "首涨", "领涨", "利好", "业绩", "高增长", "超预期",
    "upgrade", "bullish", "beat", "surge", "jump", "rally", "buy", "recommend",
    "strong", "growth", "profit", "soar", "rally", "gain", "positive", "upside"
]

NEGATIVE_WORDS = [
    "亏损", "大跌", "跌停", "下调", "减持", "卖出", "预警", "风险", "调查", "利空",
    "造假", "欺诈", "违规", "处罚", "下修", "不及预期", "暴跌", "破发", "警示",
    "downgrade", "bearish", "miss", "plunge", "crash", "sell", "warning", "risk",
    "investigate", "fraud", "penalty", "loss", "decline", "drop", "fall", "negative"
]

EVENT_PATTERNS = {
    # 业绩相关
    r"(业绩|营收|利润|净利润).*(增长|大涨|超预期|提升|创新高)": ("业绩超预期", 5),
    r"(业绩|营收|利润).*(下降|下滑|减少|不及预期|亏损)": ("业绩不及预期", -4),
    r"Q[1-4].*(营收|利润|同比).*(\d+%)": ("季度业绩公告", 2),
    
    # 评级相关
    r"(买入|推荐|增持|强烈推荐|上调).*(评级|目标价|评级)": ("券商上调评级", 3),
    r"(卖出|减持|中性|下调).*(评级|目标价|评级)": ("券商下调评级", -3),
    r"券商|投行|机构.*(研报|评级|目标价)": ("券商研报发布", 2),
    
    # 股东相关
    r"(大股东|高管|管理层|董事长).*(增持|买入|回购)": ("大股东增持", 3),
    r"(大股东|高管|管理层|董事长).*(减持|卖出|抛售)": ("大股东减持", -3),
    
    # 政策相关
    r"(政策|补贴|支持|利好).*(出台|发布|加大)": ("政策利好", 4),
    r"(监管|政策|限制|收紧).*(出台|发布|加强)": ("监管政策收紧", -3),
    
    # 产品相关
    r"(新品|新产品|新产品).*(发布|上市|推出)": ("产品发布", 2),
    r"(召回|质量问题|投诉).*(产品)": ("产品质量问题", -3),
    
    # 合作相关
    r"(合作|签约|战略|伙伴).*(达成|签署|签订)": ("战略合作", 2),
    r"(终止|取消|破裂|解约)": ("合作终止", -2),
    
    # 诉讼相关
    r"(诉讼|起诉|仲裁|纠纷)": ("法律诉讼", -2),
    r"(罚款|处罚|警示函)": ("监管处罚", -4),
}


# ==================== 工具函数 ====================

def get_sentiment_label(score):
    """根据分数返回情绪标签"""
    if score >= 8:
        return "🤩 极度乐观"
    elif score >= 5:
        return "😊 偏正面"
    elif score >= 2:
        return "🙂 轻微正面"
    elif score >= -2:
        return "😐 中性"
    elif score >= -5:
        return "😟 轻微负面"
    elif score >= -8:
        return "😰 偏负面"
    else:
        return "😱 极度悲观"


def get_sentiment_icon(score):
    """获取情绪图标"""
    if score >= 5:
        return "🟢"
    elif score >= 2:
        return "🟡"
    elif score >= -2:
        return "⚪"
    elif score >= -5:
        return "🟠"
    else:
        return "🔴"


def calculate_sentiment(text, source_weight=0.8):
    """
    计算文本情绪分数
    返回: (分数, 事件类型, 置信度)
    """
    if not text:
        return 0, None, 0
    
    text_lower = text.lower()
    score = 0
    matched_events = []
    
    # 检查事件模式
    for pattern, (event_type, event_score) in EVENT_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            matched_events.append(event_type)
            score += event_score
    
    # 词汇情绪分析
    pos_count = sum(1 for word in POSITIVE_WORDS if word.lower() in text_lower)
    neg_count = sum(1 for word in NEGATIVE_WORDS if word.lower() in text_lower)
    
    word_sentiment = (pos_count - neg_count) * 0.5
    score += word_sentiment
    
    # 归一化到 -10 到 +10
    score = max(-10, min(10, score))
    
    # 计算置信度
    confidence = min(100, (abs(score) * 10 + len(matched_events) * 15))
    
    return round(score, 1), matched_events[0] if matched_events else None, round(confidence, 1)


def normalize_ticker(ticker, market=None):
    """标准化股票代码"""
    ticker = ticker.strip()
    
    if market == "hk" or (not market and ticker.endswith(".HK")):
        if not ticker.endswith(".HK"):
            ticker = ticker.zfill(5) + ".HK"
        return ticker.upper(), "hk"
    
    if market == "us" or (not market and ticker.isalpha()):
        return ticker.upper(), "us"
    
    if market == "a" or (not market and ticker.endswith(".SZ") or ticker.endswith(".SS")):
        return ticker, "a"
    
    # 自动识别
    if ticker.endswith(".HK"):
        return ticker.upper(), "hk"
    elif ticker.endswith(".SS"):
        return ticker, "a"
    elif ticker.endswith(".SZ"):
        return ticker, "a"
    elif ticker.isdigit():
        if len(ticker) == 5:
            return ticker.zfill(5) + ".HK", "hk"
        elif len(ticker) == 6:
            if ticker.startswith(("0", "3")):
                return ticker + ".SZ", "a"
            else:
                return ticker + ".SS", "a"
    
    return ticker.upper(), "us"


def get_company_news(ticker, days=7):
    """获取公司新闻"""
    try:
        ticker_obj = yf.Ticker(ticker)
        company_info = ticker_obj.info
        
        news = []
        
        # 获取新闻
        if hasattr(ticker_obj, 'news') and ticker_obj.news:
            for item in ticker_obj.news:
                news.append({
                    "title": item.get("title", ""),
                    "publisher": item.get("publisher", "Unknown"),
                    "link": item.get("link", ""),
                    "published": item.get("published", ""),
                    "type": "news"
                })
        
        return news, company_info
    except Exception as e:
        return [], {}


def analyze_news_sentiment(news_list, days=7):
    """分析新闻情绪"""
    cutoff_date = datetime.now() - timedelta(days=days)
    events = []
    
    for item in news_list:
        title = item.get("title", "")
        if not title:
            continue
        
        # 计算情绪
        score, event_type, confidence = calculate_sentiment(title)
        
        if abs(score) >= 1:  # 只保留有意义的情绪
            events.append({
                "title": title,
                "source": item.get("publisher", "Unknown"),
                "time": item.get("published", ""),
                "score": score,
                "event_type": event_type,
                "confidence": confidence,
                "type": item.get("type", "news")
            })
    
    # 按分数排序
    events.sort(key=lambda x: abs(x["score"]), reverse=True)
    
    return events


def generate_report(ticker, company_name, events, days):
    """生成舆情报告"""
    if not events:
        return {
            "status": "success",
            "ticker": ticker,
            "company_name": company_name,
            "period_days": days,
            "sentiment_score": 0,
            "sentiment_label": "😐 中性",
            "events": [],
            "summary": {
                "positive_count": 0,
                "neutral_count": 0,
                "negative_count": 0
            },
            "message": "未找到相关新闻或公告"
        }
    
    # 计算总体情绪
    total_score = sum(e["score"] for e in events)
    avg_score = total_score / len(events) if events else 0
    
    # 分类统计
    positive = [e for e in events if e["score"] > 2]
    neutral = [e for e in events if -2 <= e["score"] <= 2]
    negative = [e for e in events if e["score"] < -2]
    
    # 生成建议
    if avg_score >= 5:
        suggestion = "整体情绪偏正面，可适当关注，但需结合基本面谨慎操作"
    elif avg_score >= 2:
        suggestion = "情绪整体偏暖，可保持关注，注意观察后续催化剂"
    elif avg_score >= -2:
        suggestion = "情绪中性，建议观望，等待更明确的信号"
    elif avg_score >= -5:
        suggestion = "情绪偏弱，注意风险，建议谨慎操作"
    else:
        suggestion = "情绪明显负面，短期规避，等待市场情绪改善"
    
    return {
        "status": "success",
        "ticker": ticker,
        "company_name": company_name,
        "period_days": days,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sentiment_score": round(avg_score, 1),
        "sentiment_label": get_sentiment_label(avg_score),
        "events": events[:10],  # 最多10个重大事件
        "summary": {
            "total_events": len(events),
            "positive_count": len(positive),
            "neutral_count": len(neutral),
            "negative_count": len(negative),
            "positive_ratio": round(len(positive) / len(events) * 100, 1) if events else 0,
            "negative_ratio": round(len(negative) / len(events) * 100, 1) if events else 0
        },
        "suggestion": suggestion
    }


def print_report(report):
    """格式化打印报告"""
    if report["status"] != "success":
        print(f"❌ 错误: {report.get('message', '未知错误')}")
        return
    
    ticker = report["ticker"]
    name = report["company_name"]
    days = report["period_days"]
    score = report["sentiment_score"]
    label = report["sentiment_label"]
    events = report.get("events", [])
    summary = report.get("summary", {})
    
    print("=" * 60)
    print(f"📰 舆情监控报告：{name}（{ticker}）")
    print("=" * 60)
    print(f"📅 监控周期：最近{days}天")
    print(f"⏰ 生成时间：{report.get('generated_at', 'N/A')}")
    print()
    
    # 情绪温度计
    print("━" * 60)
    print(f"🌡️ 情绪温度计：{score}（{label}）")
    print()
    
    # 温度计可视化
    bar_length = 40
    # 将 -10 到 +10 映射到 0-40
    position = int((score + 10) / 20 * bar_length)
    
    thermometer = ""
    for i in range(bar_length + 1):
        if i < position:
            thermometer += "█"
        elif i == position:
            thermometer += "●"
        else:
            thermometer += "░"
    
    print(f"   -10 {thermometer} +10")
    print(f"        😱            😐            🤩")
    print("━" * 60)
    print()
    
    # 重大事件清单
    if events:
        print("📋 重大事件清单：")
        print()
        for i, event in enumerate(events, 1):
            icon = get_sentiment_icon(event["score"])
            event_type = event.get("event_type", "一般新闻")
            print(f"{i}. [{icon}] {event['title']}")
            print(f"   来源：{event['source']} | 类型：{event_type}")
            print(f"   情绪贡献：{event['score']:+} | 置信度：{event['confidence']}%")
            print()
    else:
        print("📋 重大事件：无")
        print()
    
    # 情绪统计
    print("━" * 60)
    print("📊 情绪统计：")
    print(f"├── 正面事件：{summary.get('positive_count', 0)}条（{summary.get('positive_ratio', 0)}%）")
    print(f"├── 中性事件：{summary.get('neutral_count', 0)}条")
    print(f"├── 负面事件：{summary.get('negative_count', 0)}条（{summary.get('negative_ratio', 0)}%）")
    print(f"└── 事件总数：{summary.get('total_events', 0)}条")
    print()
    
    # 操作建议
    print("━" * 60)
    print(f"💡 操作建议：{report.get('suggestion', '暂无建议')}")
    print("=" * 60)


# ==================== 主程序 ====================

def main():
    if len(sys.argv) < 2:
        print("用法: python3 sentiment_scan.py <stock_code> [days] [market]")
        print("示例: python3 sentiment_scan.py 002594 7")
        print("      python3 sentiment_scan.py 0700.HK 30")
        print("      python3 sentiment_scan.py AAPL 7 us")
        sys.exit(1)
    
    ticker = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    market = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 输入安全校验
    if not re.match(r'^[A-Za-z0-9.]{1,20}$', ticker):
        print("❌ 无效的股票代码")
        sys.exit(1)
    
    # 标准化代码
    ticker_norm, market_type = normalize_ticker(ticker, market)
    
    print(f"🔍 正在获取 {ticker_norm} 的舆情数据...", file=sys.stderr)
    
    # 获取新闻
    news_list, company_info = get_company_news(ticker_norm, days)
    
    # 分析情绪
    events = analyze_news_sentiment(news_list, days)
    
    # 生成报告
    company_name = company_info.get("shortName", ticker_norm)
    report = generate_report(ticker_norm, company_name, events, days)
    
    # 打印报告
    print_report(report)


if __name__ == "__main__":
    main()
