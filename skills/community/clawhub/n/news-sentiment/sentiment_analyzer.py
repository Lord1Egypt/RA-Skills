#!/usr/bin/env python3
"""
📰 News Sentiment Analyzer - 新闻情绪分析
Analyze crypto news sentiment for trading signals
"""

import json
import urllib.request
import urllib.error
import os
from datetime import datetime

# API Configuration
TWITTER_API = "https://ai.6551.io/open/twitter_search"
DASHSCOPE_API = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# Get API keys from environment
TWITTER_TOKEN = os.environ.get("TWITTER_TOKEN", "")
DASHSCOPE_KEY = os.environ.get("DASHSCOPE_API_KEY", "")

def search_twitter(keywords, lang="en", max_results=10):
    """Search Twitter for crypto news"""
    if not TWITTER_TOKEN:
        return {"error": "No Twitter token configured"}
    
    data = json.dumps({
        "keywords": keywords,
        "lang": lang,
        "maxResults": max_results
    }).encode('utf-8')
    
    req = urllib.request.Request(
        TWITTER_API,
        data=data,
        headers={
            "Authorization": f"Bearer {TWITTER_TOKEN}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode())
            return result.get('data', [])
    except Exception as e:
        return {"error": str(e)}

def analyze_sentiment_llm(text):
    """Use LLM to analyze sentiment"""
    if not DASHSCOPE_KEY:
        # Fallback: simple keyword-based analysis
        return simple_sentiment_analysis(text)
    
    prompt = f"""分析以下加密货币相关新闻的情绪，只返回 JSON：
{{
  "sentiment": "bullish" 或 "bearish" 或 "neutral",
  "score": 0-1 之间的数字，
  "confidence": 0-1 之间的数字，
  "keywords": ["关键词 1", "关键词 2"]
}}

新闻内容：{text[:500]}"""

    data = json.dumps({
        "model": "qwen-turbo",
        "input": {"messages": [{"role": "user", "content": prompt}]},
        "parameters": {"temperature": 0.1}
    }).encode('utf-8')
    
    req = urllib.request.Request(
        DASHSCOPE_API,
        data=data,
        headers={
            "Authorization": f"Bearer {DASHSCOPE_KEY}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            # Parse LLM response
            content = result.get('output', {}).get('choices', [{}])[0].get('message', {}).get('content', '{}')
            return json.loads(content)
    except:
        return simple_sentiment_analysis(text)

def simple_sentiment_analysis(text):
    """Simple keyword-based sentiment analysis"""
    text_lower = text.lower()
    
    bullish_keywords = ['bull', 'rise', 'up', 'gain', 'pump', 'moon', 'breakout', 'rally', 'positive', 'adoption', 'partnership', 'upgrade']
    bearish_keywords = ['bear', 'drop', 'down', 'loss', 'dump', 'crash', 'breakdown', 'negative', 'hack', 'exploit', 'lawsuit', 'ban']
    
    bullish_count = sum(1 for word in bullish_keywords if word in text_lower)
    bearish_count = sum(1 for word in bearish_keywords if word in text_lower)
    
    total = bullish_count + bearish_count
    if total == 0:
        return {"sentiment": "neutral", "score": 0.5, "confidence": 0.5, "keywords": []}
    
    score = bullish_count / total
    sentiment = "bullish" if score > 0.6 else "bearish" if score < 0.4 else "neutral"
    
    return {
        "sentiment": sentiment,
        "score": round(score, 2),
        "confidence": 0.7,
        "keywords": []
    }

def analyze_coin_sentiment(coin_symbol):
    """Analyze sentiment for a specific coin"""
    print(f"📰 分析 {coin_symbol} 情绪...")
    print("=" * 60)
    
    # Search Twitter
    tweets = search_twitter(f"{coin_symbol} crypto", lang="en", max_results=10)
    
    if isinstance(tweets, dict) and 'error' in tweets:
        print(f"❌ 错误：{tweets['error']}")
        return
    
    if not tweets:
        print("❌ 未找到相关推文")
        return
    
    print(f"📊 分析 {len(tweets)} 条推文\n")
    
    # Analyze each tweet
    sentiments = []
    for i, tweet in enumerate(tweets[:10], 1):
        text = tweet.get('text', '')
        analysis = analyze_sentiment_llm(text)
        sentiments.append(analysis.get('score', 0.5))
        
        emoji = "🚀" if analysis.get('sentiment') == 'bullish' else "📉" if analysis.get('sentiment') == 'bearish' else "➡️"
        print(f"{i}. {emoji} Score: {analysis.get('score', 0.5):.2f}")
        print(f"   {text[:80]}...")
        print()
    
    # Calculate average
    avg_score = sum(sentiments) / len(sentiments) if sentiments else 0.5
    
    print("=" * 60)
    print(f"📊 {coin_symbol} 情绪分析结果:")
    print(f"   平均分数：{avg_score:.2f}/1.00")
    
    if avg_score > 0.7:
        print(f"   情绪：🚀 非常看涨 (Very Bullish)")
        print(f"   信号：💰 考虑买入")
    elif avg_score > 0.5:
        print(f"   情绪：📈 看涨 (Bullish)")
        print(f"   信号：👀 观望")
    elif avg_score > 0.3:
        print(f"   情绪：📉 看跌 (Bearish)")
        print(f"   信号：⚠️ 谨慎")
    else:
        print(f"   情绪：💥 非常看跌 (Very Bearish)")
        print(f"   信号：🚫 考虑卖出")
    
    print("=" * 60)

if __name__ == "__main__":
    print("📰 News Sentiment Analyzer v1.0")
    print("Starting sentiment analysis...\n")
    
    # Analyze Bitcoin
    analyze_coin_sentiment("BTC Bitcoin")
