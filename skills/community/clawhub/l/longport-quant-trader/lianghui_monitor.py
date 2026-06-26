#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
两会政策监控系统 v3.0
功能：监控两会相关政策新闻，分析对股市影响，推送操作建议
更新：使用 RSS 源 + 长桥 API 行情
"""

import os
import requests
import json
import subprocess
import feedparser
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from bs4 import BeautifulSoup

# ============ 配置 ============
# 飞书应用凭证（请从环境变量读取，勿硬编码）
# export FEISHU_APP_ID="your_app_id"
# export FEISHU_APP_SECRET="your_app_secret"
# export FEISHU_USER_OPEN_ID="your_open_id"
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_USER_OPEN_ID = os.getenv("FEISHU_USER_OPEN_ID", "")

# 新闻源（RSS + 网页）
NEWS_SOURCES = {
    "bbc_china": {
        "name": "BBC 中文网",
        "url": "https://feeds.bbci.co.uk/news/world/asia/china/rss.xml",
        "language": "en",
        "type": "rss"
    },
    "reuters_china": {
        "name": "Reuters China",
        "url": "https://www.reuters.com/rssfeed/world/china",
        "language": "en",
        "type": "rss"
    }
}

# 中文关键词（用于匹配英文新闻中的 China/Beijing 相关内容）
LIANGHUI_KEYWORDS_EN = [
    "China", "Beijing", "Chinese", "NPC", "Two Sessions",
    "monetary policy", "fiscal policy", "interest rate", "reserve requirement",
    "GDP", "economic growth", "stimulus", "deficit", "bond",
    "property", "real estate", "capital market", "stock",
    "technology", "innovation", "trade", "export", "import",
    "financial", "bank", "insurance", "securities",
    "loose", "easing", "support", "reform", "development"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 两会政策关键词 - 扩展版
LIANGHUI_KEYWORDS = [
    "两会", "人大", "政协", "政府工作报告",
    "货币政策", "财政政策", "降准", "降息", "LPR",
    "赤字率", "特别国债", "地方政府专项债",
    "GDP", "CPI", "就业", "经济增长",
    "房地产", "资本市场", "注册制", "科创板",
    "科技", "创新", "产业", "新质生产力",
    "内需", "消费", "基建", "投资",
    "开放", "自贸区", "一带一路", "外贸",
    "金融", "银行", "保险", "证券",
    "宽松", "刺激", "支持", "发展", "改革"
]

# 政策影响分类
POLICY_IMPACT = {
    "利好": ["降准", "降息", "减税", "补贴", "放宽", "支持", "鼓励", "刺激"],
    "利空": ["收紧", "限制", "调控", "去杠杆", "加息", "提高准备金"],
    "中性": ["稳健", "平稳", "合理", "适度", "预期之内"]
}

# 受益板块映射
SECTOR_MAPPING = {
    "货币政策宽松": ["银行", "券商", "房地产", "基建"],
    "财政政策扩张": ["建筑", "建材", "工程机械", "基建"],
    "房地产支持": ["房地产", "家电", "建材", "银行"],
    "科技创新": ["半导体", "人工智能", "新能源", "生物医药"],
    "消费升级": ["白酒", "食品饮料", "旅游", "零售"],
    "资本市场改革": ["券商", "金融科技", "创投"]
}


def get_feishu_token() -> str:
    """获取飞书 API Token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    response = requests.post(url, json=payload)
    data = response.json()
    if data.get("code") == 0:
        return data.get("tenant_access_token")
    else:
        raise Exception(f"获取飞书 Token 失败：{data}")


def send_feishu_message(title: str, content: str, color: str = "blue"):
    """发送飞书消息"""
    try:
        token = get_feishu_token()
        
        # 使用新的飞书 API v1
        url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # 使用文本消息 - content 直接是 JSON 对象，不是字符串
        message_content = {
            "text": f"{title}\n\n{content}"
        }
        
        payload = {
            "receive_id": FEISHU_USER_OPEN_ID,
            "msg_type": "text",
            "content": json.dumps(message_content)  # content 字段需要是 JSON 字符串
        }
        
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        if result.get("code") == 0:
            print(f"✅ 飞书推送成功：{title}")
            return True
        else:
            print(f"❌ 飞书推送失败：{result}")
            return False
            
    except Exception as e:
        print(f"❌ 发送飞书消息异常：{e}")
        return False


def analyze_sentiment(text: str) -> Dict:
    """分析新闻情感和政策倾向"""
    text_lower = text.lower()
    
    # 检查是否包含两会关键词
    is_lianghui = any(kw in text for kw in LIANGHUI_KEYWORDS)
    
    # 分析政策倾向
    positive_count = sum(1 for kw in POLICY_IMPACT["利好"] if kw in text_lower)
    negative_count = sum(1 for kw in POLICY_IMPACT["利空"] if kw in text_lower)
    neutral_count = sum(1 for kw in POLICY_IMPACT["中性"] if kw in text_lower)
    
    # 判断整体倾向
    if positive_count > negative_count + 2:
        impact = "利好"
        color = "green"
    elif negative_count > positive_count + 2:
        impact = "利空"
        color = "red"
    else:
        impact = "中性"
        color = "blue"
    
    return {
        "is_lianghui": is_lianghui,
        "impact": impact,
        "color": color,
        "positive_score": positive_count,
        "negative_score": negative_count
    }


def fetch_news(hours: int = 6) -> List[Dict]:
    """抓取新闻 - RSS 版"""
    all_news = []
    
    for source_key, source_info in NEWS_SOURCES.items():
        try:
            if source_info.get("type") == "rss":
                feed = feedparser.parse(source_info["url"])
                
                for entry in feed.entries[:30]:
                    title = entry.title
                    summary = entry.summary if hasattr(entry, 'summary') else ""
                    content = f"{title} {summary}"
                    
                    # 检查是否包含关键词（中英文）
                    has_keyword = (
                        any(kw in content for kw in LIANGHUI_KEYWORDS) or
                        any(kw.lower() in content.lower() for kw in LIANGHUI_KEYWORDS_EN)
                    )
                    
                    if has_keyword:
                        sentiment = analyze_sentiment(content)
                        news_item = {
                            "id": f"{source_key}_{len(all_news)}",
                            "source": source_info["name"],
                            "title": title,
                            "summary": summary[:200] if summary else "",
                            "link": entry.link,
                            "published": entry.published if hasattr(entry, 'published') else datetime.now().isoformat(),
                            "sentiment": sentiment
                        }
                        all_news.append(news_item)
            else:
                # 网页抓取（备用）
                response = requests.get(source_info["url"], headers=HEADERS, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                titles = []
                for link in soup.find_all('a')[:100]:
                    text = link.get_text().strip()
                    if text and 15 < len(text) < 80:
                        titles.append(text)
                
                for title in titles[:50]:
                    if any(kw in title for kw in LIANGHUI_KEYWORDS):
                        sentiment = analyze_sentiment(title)
                        news_item = {
                            "id": f"{source_key}_{len(all_news)}",
                            "source": source_info["name"],
                            "title": title,
                            "summary": "",
                            "link": source_info["url"],
                            "published": datetime.now().isoformat(),
                            "sentiment": sentiment
                        }
                        all_news.append(news_item)
                
        except Exception as e:
            print(f"❌ 抓取 {source_info['name']} 失败：{e}")
    
    return all_news


def get_sectors_from_news(news_list: List[Dict]) -> List[str]:
    """从新闻中提取受益板块"""
    sectors = set()
    
    for news in news_list:
        title = news["title"] + news["summary"]
        
        for policy, sector_list in SECTOR_MAPPING.items():
            if any(kw in title for kw in policy):
                sectors.update(sector_list)
    
    return list(sectors)


def generate_trading_advice(news_list: List[Dict]) -> str:
    """生成操作建议"""
    if not news_list:
        return "暂无重大政策新闻，维持现有仓位观望"
    
    # 统计利好/利空比例
    positive_count = sum(1 for n in news_list if n["sentiment"]["impact"] == "利好")
    negative_count = sum(1 for n in news_list if n["sentiment"]["impact"] == "利空")
    
    # 提取受益板块
    sectors = get_sectors_from_news(news_list)
    
    advice = []
    
    if positive_count > negative_count:
        advice.append("📈 整体政策偏利好，可适度加仓")
        if sectors:
            advice.append(f"🎯 关注板块：{', '.join(sectors[:5])}")
        advice.append("✅ 建议：分批建仓，避免追高")
    elif negative_count > positive_count:
        advice.append("📉 政策信号偏紧，注意风险控制")
        advice.append("✅ 建议：降低仓位，等待明确信号")
    else:
        advice.append("⚖️ 政策信号中性，维持现有策略")
        advice.append("✅ 建议：关注后续政策落地情况")
    
    advice.append("")
    advice.append("⚠️ 风险提示：设置止损位，控制单票仓位")
    
    return "\n".join(advice)


def format_push_message(news_list: List[Dict]) -> str:
    """格式化推送消息"""
    if not news_list:
        return "🔍 两会政策监控\n\n暂无最新相关政策新闻"
    
    lines = []
    lines.append("📢 两会政策监控快报")
    lines.append(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 50)
    lines.append("")
    
    # 最新新闻（最多 5 条）
    lines.append("📰 最新政策动态：")
    for i, news in enumerate(news_list[:5], 1):
        emoji = "🟢" if news["sentiment"]["impact"] == "利好" else "🔴" if news["sentiment"]["impact"] == "利空" else "⚪"
        lines.append(f"{i}. {emoji} {news['title']}")
        lines.append(f"   来源：{news['source']} | 倾向：{news['sentiment']['impact']}")
        lines.append("")
    
    # 受益板块
    sectors = get_sectors_from_news(news_list)
    if sectors:
        lines.append("🎯 受益板块：")
        lines.append(f"   {', '.join(sectors)}")
        lines.append("")
    
    # 操作建议
    lines.append("💡 操作建议：")
    lines.append(generate_trading_advice(news_list))
    
    return "\n".join(lines)


def get_market_data() -> Dict:
    """获取长桥 API 实时行情"""
    try:
        from longport.openapi import QuoteContext, Config, SubType, PushQuote
        import time
        
        config = Config.from_env()
        ctx = QuoteContext(config)
        
        symbols = ["QQQ.US", "NVDA.US", "SPY.US"]
        received_quotes = {}
        
        def on_quote(symbol: str, quote: PushQuote):
            received_quotes[symbol] = quote
        
        ctx.set_on_quote(on_quote)
        ctx.subscribe(symbols, [SubType.Quote])
        
        # 等待 5 秒接收推送
        time.sleep(5)
        
        data = {}
        for symbol, quote in received_quotes.items():
            data[symbol] = {
                "price": quote.last_done,
                "change": quote.change if hasattr(quote, 'change') else 0,
                "change_pct": quote.change_rate if hasattr(quote, 'change_rate') else 0
            }
        
        return data
        
    except Exception as e:
        print(f"⚠️ 长桥 API 连接失败：{e}")
        return {}


def format_market_data(market_data: Dict) -> str:
    """格式化行情数据"""
    if not market_data:
        return "⚠️ 行情数据暂不可用"
    
    lines = []
    lines.append("📈 实时行情：")
    
    for symbol, data in market_data.items():
        ticker = symbol.replace(".US", "")
        emoji = "🟢" if data["change"] >= 0 else "🔴"
        lines.append(f"  {emoji} {ticker}: ${data['price']:.2f} ({data['change']:+.2f}, {data['change_pct']:+.2%})")
    
    return "\n".join(lines)


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🇨🇳 两会政策监控系统 v2.0")
    print("=" * 80)
    print(f"启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 抓取新闻
    print("\n📡 正在抓取新闻...")
    news_list = fetch_news(hours=6)
    print(f"✅ 抓取到 {len(news_list)} 条相关政策新闻")
    
    # 获取行情
    print("\n📊 正在获取行情...")
    market_data = get_market_data()
    
    # 格式化消息
    message = format_push_message(news_list)
    
    # 添加行情数据
    if market_data:
        message += "\n\n" + "=" * 50 + "\n\n"
        message += format_market_data(market_data)
    
    # 发送飞书（使用 OpenClaw message 工具）
    print("\n📱 正在发送飞书推送...")
    
    # 使用 subprocess 调用 OpenClaw message 工具
    try:
        cmd = [
            "openclaw", "message", "send",
            "--channel", "feishu",
            "--target", FEISHU_USER_OPEN_ID,
            "--message", message
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("\n✅ 监控完成，推送成功")
        else:
            print(f"\n❌ 推送失败：{result.stderr}")
    except Exception as e:
        print(f"\n❌ 发送消息异常：{e}")
        # 降级使用飞书 API
        success = send_feishu_message("两会政策监控", message)
        if success:
            print("\n✅ 监控完成（降级模式）")
    
    # 输出完整报告
    print("\n" + "=" * 80)
    print("📊 完整报告：")
    print("=" * 80)
    print(message)


if __name__ == "__main__":
    from datetime import timedelta
    main()
