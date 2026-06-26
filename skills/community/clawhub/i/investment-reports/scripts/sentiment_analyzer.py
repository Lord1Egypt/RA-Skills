#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investage Sentiment Analyzer
情緒分析：Polymarket + Reddit
"""

import requests
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json

class SentimentAnalyzer:
    """情緒分析器"""
    
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
    
    def fetch_polymarket(self) -> Dict[str, Any]:
        """抓取 Polymarket 情緒"""
        try:
            # 嘗試多個 API 端點
            endpoints = [
                "https://clobgateway.poly.market/markets",
                "https://gamma.poly.market/markets"
            ]
            
            for url in endpoints:
                try:
                    params = {"closed": "false", "limit": 20}
                    response = requests.get(url, params=params, headers=self.headers, timeout=5)
                    data = response.json()
                    
                    # 找相關市場
                    related_markets = []
                    markets_list = data.get('data', []) if isinstance(data, dict) else data
                    
                    for market in markets_list[:20]:
                        question = market.get('question', '')
                        if self.ticker.lower() in question.lower():
                            outcomes = market.get('outcomes', [])
                            prices = str(market.get('outcomePrices', '')).split(',')
                            
                            if len(outcomes) >= 2 and len(prices) >= 2:
                                try:
                                    p_yes = float(prices[0].strip())
                                    p_no = float(prices[1].strip()) if len(prices) > 1 else (1 - p_yes)
                                    total = p_yes + p_no
                                    
                                    related_markets.append({
                                        "question": question[:100],
                                        "yes_prob": round(p_yes / total * 100, 1) if total > 0 else 50,
                                        "volume": market.get('volume', 0)
                                    })
                                except (ValueError, TypeError):
                                    continue
                    
                    if related_markets:
                        return {"markets": related_markets, "available": True}
                        
                except Exception:
                    continue
            
            return {"markets": [], "available": False, "reason": "No related markets found"}
            
        except Exception as e:
            return {"markets": [], "available": False, "error": str(e)}
    
    def fetch_reddit(self) -> Dict[str, Any]:
        """抓取 Reddit 討論"""
        try:
            # 使用 Reddit search API
            url = f"https://www.reddit.com/search.json?q={self.ticker}&sort=hot&limit=20"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()
            
            posts = []
            total_score = 0
            weighted_sentiment = 0
            
            for post in data.get('data', {}).get('children', [])[:10]:
                title = post.get('data', {}).get('title', '')
                upvotes = post.get('data', {}).get('score', 1)
                num_comments = post.get('data', {}).get('num_comments', 0)
                
                # 簡單情緒分析
                sentiment = self._analyze_sentiment(title)
                weight = min(upvotes, 10000)  # 權重基於 upvotes
                
                total_score += upvotes
                weighted_sentiment += sentiment * weight
                count = len(posts)
                
                posts.append({
                    "title": title[:80],
                    "upvotes": upvotes,
                    "comments": num_comments,
                    "sentiment": sentiment
                })
            
            # 平均情緒 (0-100)
            avg_sentiment = weighted_sentiment / total_score if total_score > 0 else 50
            avg_sentiment = max(0, min(100, avg_sentiment))
            
            # 分類
            if avg_sentiment > 60:
                interpretation = "BULLISH"
            elif avg_sentiment < 40:
                interpretation = "BEARISH"
            else:
                interpretation = "NEUTRAL"
            
            return {
                "posts": posts,
                "avg_sentiment": round(avg_sentiment, 1),
                "interpretation": interpretation,
                "post_count": len(posts)
            }
            
        except Exception as e:
            print(f"Reddit fetch error: {e}")
            return {"posts": [], "avg_sentiment": 50, "interpretation": "UNKNOWN", "error": str(e)}
    
    def _analyze_sentiment(self, text: str) -> float:
        """簡單關鍵詞情緒分析"""
        text_lower = text.lower()
        
        bullish_keywords = [
            'buy', 'bullish', 'long', 'moon', 'rocket', 'to the moon',
            'upgrade', 'outperform', 'overweight', 'breakout', 'buy the dip',
            'calls', 'leap', 'undervalued', 'accumulate', 'add'
        ]
        
        bearish_keywords = [
            'sell', 'bearish', 'short', 'dump', 'crash', 'downgrade',
            'underperform', 'overvalued', 'puts', 'breakdown', 'cut',
            'risk', 'warning', 'drop', 'lose'
        ]
        
        bullish_count = sum(1 for kw in bullish_keywords if kw in text_lower)
        bearish_count = sum(1 for kw in bearish_keywords if kw in text_lower)
        
        if bullish_count > bearish_count:
            return 70
        elif bearish_count > bullish_count:
            return 30
        else:
            return 50
    
    def generate_macro_view(self, sentiment_data: Dict) -> str:
        """生成市場觀察文字"""
        reddit = sentiment_data.get('reddit', {})
        polymarket = sentiment_data.get('polymarket', {})
        
        parts = []
        
        # Reddit 觀察
        if reddit.get('interpretation') == 'BULLISH':
            parts.append(f"Reddit 社區對 {self.ticker} 討論偏多，投資者情緒樂觀")
        elif reddit.get('interpretation') == 'BEARISH':
            parts.append(f"Reddit 社區對 {self.ticker} 討論偏空，投資者情緒謹慎")
        else:
            parts.append(f"Reddit 社區對 {self.ticker} 討論中性，投資者觀望")
        
        # Polymarket 觀察
        markets = polymarket.get('markets', [])
        if markets:
            avg_prob = sum(m['yes_prob'] for m in markets) / len(markets)
            if avg_prob > 60:
                parts.append(f"Polymarket 預測市場偏多 ({avg_prob:.0f}%)")
            elif avg_prob < 40:
                parts.append(f"Polymarket 預測市場偏空 ({avg_prob:.0f}%)")
            else:
                parts.append(f"Polymarket 預測市場看法分歧 ({avg_prob:.0f}%)")
        
        return "。".join(parts) + "。"
    
    def analyze(self) -> Dict[str, Any]:
        """完整情緒分析"""
        polymarket = self.fetch_polymarket()
        reddit = self.fetch_reddit()
        
        sentiment_data = {
            "polymarket": polymarket,
            "reddit": reddit
        }
        
        macro_view = self.generate_macro_view(sentiment_data)
        
        # 情緒評分
        score = 0
        
        # Reddit 評分
        reddit_sentiment = reddit.get('avg_sentiment', 50)
        if reddit_sentiment > 60:
            score += 10
        elif reddit_sentiment < 40:
            score -= 10
        
        # Polymarket 評分
        markets = polymarket.get('markets', [])
        if markets:
            avg_prob = sum(m['yes_prob'] for m in markets) / len(markets)
            if avg_prob > 60:
                score += 10
            elif avg_prob < 40:
                score -= 10
        
        # 限制分數
        score = max(-20, min(20, score))
        
        return {
            "ticker": self.ticker,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            
            "polymarket": {
                "available": polymarket.get('available', False),
                "markets": polymarket.get('markets', [])[:3],
                "avg_probability": round(sum(m['yes_prob'] for m in markets) / len(markets), 1) 
                                   if markets else None
            },
            
            "reddit": {
                "avg_sentiment": reddit.get('avg_sentiment'),
                "interpretation": reddit.get('interpretation'),
                "post_count": reddit.get('post_count'),
                "top_posts": reddit.get('posts', [])[:3]
            },
            
            "overall": {
                "interpretation": "BULLISH" if score > 5 else ("BEARISH" if score < -5 else "NEUTRAL"),
                "score": score
            },
            
            "macro_view": macro_view,
            "score": score
        }


def main():
    """測試"""
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "NVDA"
    
    analyzer = SentimentAnalyzer(ticker)
    result = analyzer.analyze()
    
    print(f"\n📰 {ticker} 情緒分析")
    print("=" * 50)
    print(f"Reddit 情緒: {result['reddit']['avg_sentiment']}% ({result['reddit']['interpretation']})")
    print(f"Reddit 討論數: {result['reddit']['post_count']}")
    print(f"\nPolymarket 平均概率: {result['polymarket']['avg_probability']}%")
    print(f"\n市場觀察:")
    print(result['macro_view'])
    print(f"\n情緒評分: {result['score']}/20")


if __name__ == "__main__":
    main()
