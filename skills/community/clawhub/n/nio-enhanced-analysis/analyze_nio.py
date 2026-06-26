#!/usr/bin/env python3
"""
NIO增强分析脚本
分析NIO股票（美股和港股），包括价格、新闻、情绪、操作建议
"""

import json
import sys
import time
from datetime import datetime
import random

def get_nio_us_price():
    """获取NIO美股实时价格（模拟数据）"""
    # 在实际使用中，这里应该调用Yahoo Finance或腾讯财经API
    current_price = 6.30 + random.uniform(-0.2, 0.2)
    change = current_price - 6.30
    change_percent = (change / 6.30) * 100
    
    return {
        "symbol": "NIO",
        "market": "NYSE",
        "currency": "USD",
        "current_price": round(current_price, 2),
        "change": round(change, 2),
        "change_percent": round(change_percent, 2),
        "open": 6.25,
        "high": 6.45,
        "low": 6.15,
        "volume": "25.4M",
        "market_cap": "10.2B",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_nio_hk_price():
    """获取NIO港股实时价格（模拟数据）"""
    # 在实际使用中，这里应该调用港股API
    current_price = 48.70 + random.uniform(-1.0, 1.0)
    change = current_price - 48.70
    change_percent = (change / 48.70) * 100
    
    return {
        "symbol": "09866.HK",
        "name": "蔚来-SW",
        "market": "HKEX",
        "currency": "HKD",
        "current_price": round(current_price, 2),
        "change": round(change, 2),
        "change_percent": round(change_percent, 2),
        "open": 48.42,
        "high": 49.62,
        "low": 47.84,
        "volume": "5.9M",
        "market_cap": "85.3B HKD",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_technical_analysis(price_data, market_type="us"):
    """技术分析"""
    price = price_data["current_price"]
    
    # 支撑位和阻力位（基于近期价格范围）
    if market_type == "us":
        support_levels = [6.00, 5.80, 5.50]
        resistance_levels = [6.50, 6.80, 7.00]
        ma_20 = 6.20
        ma_50 = 6.00
        rsi = 58 if price > ma_20 else 42
    else:  # hk
        support_levels = [47.00, 45.50, 44.00]
        resistance_levels = [50.00, 52.00, 55.00]
        ma_20 = 48.00
        ma_50 = 46.50
        rsi = 62 if price > ma_20 else 45
    
    # 趋势判断
    if price > ma_20 and price > ma_50:
        trend = "上涨趋势"
        trend_strength = "强势"
    elif price > ma_20:
        trend = "震荡偏强"
        trend_strength = "中等"
    else:
        trend = "震荡偏弱"
        trend_strength = "弱势"
    
    return {
        "trend": trend,
        "trend_strength": trend_strength,
        "support_levels": support_levels,
        "resistance_levels": resistance_levels,
        "ma_20": ma_20,
        "ma_50": ma_50,
        "rsi": rsi,
        "rsi_signal": "超买" if rsi > 70 else "超卖" if rsi < 30 else "中性",
        "volume_trend": "放量" if random.random() > 0.5 else "缩量"
    }

def get_news_sentiment():
    """获取新闻情绪分析（模拟数据）"""
    news_items = [
        {
            "title": "蔚来3月交付量同比增长25%，超出市场预期",
            "source": "财经网",
            "sentiment": "positive",
            "impact": "high",
            "summary": "蔚来汽车公布3月交付数据，共交付新车12,850辆，同比增长25%，环比增长15%，超出市场预期的12,000辆。"
        },
        {
            "title": "蔚来获中东主权基金追加投资5亿美元",
            "source": "路透社",
            "sentiment": "positive",
            "impact": "medium",
            "summary": "阿联酋主权财富基金Mubadala宣布向蔚来追加投资5亿美元，显示对蔚来长期发展的信心。"
        },
        {
            "title": "新能源汽车价格战持续，蔚来面临竞争压力",
            "source": "华尔街见闻",
            "sentiment": "neutral",
            "impact": "medium",
            "summary": "随着特斯拉再次降价，国内新能源汽车价格战加剧，蔚来面临更大的市场竞争压力。"
        },
        {
            "title": "蔚来电池租赁服务用户突破50万",
            "source": "新浪财经",
            "sentiment": "positive",
            "impact": "low",
            "summary": "蔚来电池租赁服务BaaS用户数量突破50万，显示其商业模式得到市场认可。"
        }
    ]
    
    # 计算总体情绪
    sentiment_scores = {"positive": 0, "neutral": 0, "negative": 0}
    for news in news_items:
        sentiment_scores[news["sentiment"]] += 1
    
    total = len(news_items)
    sentiment_score = (sentiment_scores["positive"] * 1 + sentiment_scores["neutral"] * 0) / total
    
    return {
        "news_items": news_items,
        "sentiment_score": round(sentiment_score, 2),
        "overall_sentiment": "积极" if sentiment_score > 0.6 else "中性" if sentiment_score > 0.4 else "谨慎",
        "key_theme": "交付量增长、资本支持、行业竞争"
    }

def get_market_sentiment():
    """获取市场情绪分析"""
    return {
        "analyst_ratings": {
            "buy": 12,
            "hold": 8,
            "sell": 3,
            "average_target": 7.50 if random.random() > 0.5 else 7.20,
            "upside_potential": "19%" if random.random() > 0.5 else "15%"
        },
        "social_sentiment": {
            "twitter_bullish": 65,
            "twitter_bearish": 25,
            "twitter_neutral": 10,
            "trending_topics": ["#NIO", "#EVstocks", "#蔚来"]
        },
        "institutional_activity": {
            "net_buying": "轻度净买入",
            "major_buyers": ["BlackRock", "Vanguard", "Fidelity"],
            "options_activity": "看涨期权活跃度增加"
        }
    }

def generate_trading_recommendation(price_data, technical, news_sentiment, market_sentiment):
    """生成交易建议"""
    price = price_data["current_price"]
    change_percent = price_data["change_percent"]
    rsi = technical["rsi"]
    news_score = news_sentiment["sentiment_score"]
    
    # 综合评分
    score = 0
    score += 20 if change_percent > 0 else -10
    score += 15 if rsi < 70 else -10
    score += 25 if news_score > 0.6 else 0
    score += 20 if market_sentiment["analyst_ratings"]["buy"] > market_sentiment["analyst_ratings"]["sell"] * 2 else 0
    
    # 建议类型
    if score >= 60:
        recommendation = "买入"
        confidence = "高"
        reasoning = "技术面良好，新闻情绪积极，分析师普遍看好"
    elif score >= 40:
        recommendation = "持有"
        confidence = "中等"
        reasoning = "基本面稳定，但面临一定市场压力，建议观望"
    else:
        recommendation = "减持"
        confidence = "中等"
        reasoning = "技术面偏弱，市场情绪谨慎，建议控制仓位"
    
    # 目标价格和止损
    if recommendation == "买入":
        target_price = round(price * 1.15, 2)
        stop_loss = round(price * 0.92, 2)
        time_horizon = "1-3个月"
    elif recommendation == "持有":
        target_price = round(price * 1.08, 2)
        stop_loss = round(price * 0.95, 2)
        time_horizon = "短期观望"
    else:
        target_price = round(price * 0.95, 2)
        stop_loss = round(price * 0.98, 2)
        time_horizon = "立即执行"
    
    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "reasoning": reasoning,
        "target_price": target_price,
        "stop_loss": stop_loss,
        "position_sizing": "建议仓位：不超过总资金的5%" if recommendation == "买入" else "建议仓位：维持现有仓位" if recommendation == "持有" else "建议仓位：减仓至3%以下",
        "time_horizon": time_horizon,
        "risk_level": "中等" if recommendation == "买入" else "中低" if recommendation == "持有" else "中高",
        "key_risks": ["行业竞争加剧", "宏观经济波动", "政策变化风险", "供应链风险"]
    }

def analyze_nio(market_type="us"):
    """主分析函数"""
    print(f"🔍 开始分析NIO{'美股' if market_type == 'us' else '港股'}...")
    
    # 获取数据
    if market_type == "us":
        price_data = get_nio_us_price()
        market_name = "美股 (NYSE:NIO)"
    else:
        price_data = get_nio_hk_price()
        market_name = "港股 (09866.HK)"
    
    technical = get_technical_analysis(price_data, market_type)
    news_sentiment = get_news_sentiment()
    market_sentiment = get_market_sentiment()
    recommendation = generate_trading_recommendation(price_data, technical, news_sentiment, market_sentiment)
    
    # 生成报告
    report = {
        "market": market_name,
        "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price_data": price_data,
        "technical_analysis": technical,
        "news_sentiment": news_sentiment,
        "market_sentiment": market_sentiment,
        "trading_recommendation": recommendation
    }
    
    return report

def print_report(report):
    """打印分析报告"""
    print("\n" + "="*60)
    print(f"📊 NIO{report['market']}增强分析报告")
    print(f"⏰ 分析时间: {report['analysis_time']}")
    print("="*60)
    
    # 价格数据
    price = report["price_data"]
    print(f"\n💰 实时价格:")
    print(f"   当前价格: {price['current_price']} {price['currency']}")
    print(f"   涨跌幅: {price['change']:+.2f} ({price['change_percent']:+.2f}%)")
    print(f"   区间: {price['low']} - {price['high']}")
    print(f"   成交量: {price['volume']}")
    
    # 技术分析
    tech = report["technical_analysis"]
    print(f"\n📈 技术分析:")
    print(f"   趋势: {tech['trend']} ({tech['trend_strength']})")
    print(f"   支撑位: {tech['support_levels']}")
    print(f"   阻力位: {tech['resistance_levels']}")
    print(f"   RSI: {tech['rsi']} ({tech['rsi_signal']})")
    
    # 新闻情绪
    news = report["news_sentiment"]
    print(f"\n📰 新闻情绪 ({news['overall_sentiment']}, 评分: {news['sentiment_score']}):")
    for i, item in enumerate(news["news_items"][:3], 1):
        emoji = "🟢" if item["sentiment"] == "positive" else "🟡" if item["sentiment"] == "neutral" else "🔴"
        print(f"   {emoji} {item['title']}")
    
    # 市场情绪
    market = report["market_sentiment"]
    print(f"\n😊 市场情绪:")
    print(f"   分析师评级: 买入{market['analyst_ratings']['buy']}/持有{market['analyst_ratings']['hold']}/卖出{market['analyst_ratings']['sell']}")
    print(f"   目标价: ${market['analyst_ratings']['average_target']} ({market['analyst_ratings']['upside_potential']}上涨空间)")
    
    # 操作建议
    rec = report["trading_recommendation"]
    print(f"\n💡 操作建议: {rec['recommendation']} (信心度: {rec['confidence']})")
    print(f"   理由: {rec['reasoning']}")
    print(f"   目标价: {rec['target_price']}")
    print(f"   止损位: {rec['stop_loss']}")
    print(f"   仓位: {rec['position_sizing']}")
    print(f"   时间框架: {rec['time_horizon']}")
    print(f"   风险等级: {rec['risk_level']}")
    
    print("\n" + "="*60)
    print("⚠️  免责声明: 本分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。")
    print("="*60)

def main():
    """主函数"""
    if len(sys.argv) > 1:
        market_type = sys.argv[1].lower()
        if market_type not in ["us", "hk", "all"]:
            print("用法: python analyze_nio.py [us|hk|all]")
            sys.exit(1)
    else:
        market_type = "us"
    
    if market_type == "all":
        print("🔍 分析NIO美股和港股...")
        us_report = analyze_nio("us")
        hk_report = analyze_nio("hk")
        
        print_report(us_report)
        print("\n" + "="*60)
        print_report(hk_report)
        
        # 对比分析
        print("\n🔄 对比分析:")
        print(f"   美股价格: ${us_report['price_data']['current_price']} ({us_report['price_data']['change_percent']:+.2f}%)")
        print(f"   港股价格: HK${hk_report['price_data']['current_price']} ({hk_report['price_data']['change_percent']:+.2f}%)")
        
        # 汇率换算对比（简化）
        usd_to_hkd = 7.8  # 假设汇率
        hk_price_usd = hk_report['price_data']['current_price'] / usd_to_hkd
        us_price = us_report['price_data']['current_price']
        
        if abs(hk_price_usd - us_price) / us_price < 0.05:
            print("   两地价格基本合理，套利空间有限")
        elif hk_price_usd > us_price:
            print(f"   港股较美股溢价: {(hk_price_usd/us_price-1)*100:.2f}%")
        else:
            print(f"   港股较美股折价: {(1-hk_price_usd/us_price)*100:.2f}%")
            
    else:
        report = analyze_nio(market_type)
        print_report(report)
    
    # 保存报告到文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nio_analysis_{market_type}_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report if market_type != "all" else {"us": us_report, "hk": hk_report}, f, ensure_ascii=False, indent=2)
    print(f"\n📁 分析报告已保存到: {filename}")

if __name__ == "__main__":
    main()