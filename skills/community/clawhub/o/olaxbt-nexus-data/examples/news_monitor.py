#!/usr/bin/env python3
"""
News monitoring example for OlaXBT Nexus Data API.
"""

import os
import sys
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.olaxbt_nexus_data import NexusClient


class NewsMonitor:
    """Monitor cryptocurrency news with sentiment analysis."""
    
    def __init__(self):
        self.client = NexusClient()
        self.seen_news_ids = set()
    
    def monitor_news(self, symbols=None, interval_minutes=5, max_iterations=None):
        """
        Monitor news for specified symbols.
        
        Args:
            symbols: List of symbols to monitor (None for all)
            interval_minutes: Check interval in minutes
            max_iterations: Maximum number of checks (None for infinite)
        """
        if symbols is None:
            symbols = ["BTC", "ETH", "SOL"]
        
        print(f"📰 Starting news monitor for {symbols}")
        print(f"⏰ Check interval: {interval_minutes} minutes")
        print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        iteration = 0
        while True:
            if max_iterations and iteration >= max_iterations:
                print(f"\n✅ Completed {max_iterations} iterations")
                break
            
            iteration += 1
            print(f"\n=== Check #{iteration} at {datetime.now().strftime('%H:%M:%S')} ===")
            
            try:
                self._check_news(symbols)
            except Exception as e:
                print(f"❌ Error in check #{iteration}: {str(e)}")
            
            if iteration < (max_iterations or float('inf')):
                print(f"⏳ Next check in {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
    
    def _check_news(self, symbols):
        """Check for new news items."""
        all_new_items = []
        
        for symbol in symbols:
            try:
                # Get latest news for symbol
                news_items = self.client.news.get_latest(
                    symbols=[symbol],
                    limit=10
                )
                
                # Filter for new items
                new_items = []
                for item in news_items:
                    news_id = item.get('id')
                    if news_id and news_id not in self.seen_news_ids:
                        self.seen_news_ids.add(news_id)
                        new_items.append(item)
                
                if new_items:
                    print(f"\n📈 {symbol}: {len(new_items)} new news items")
                    all_new_items.extend(new_items)
                    
                    # Display top new items
                    for i, item in enumerate(new_items[:3], 1):
                        title = item.get('title', 'No title')[:80]
                        source = item.get('source', 'Unknown')
                        sentiment = item.get('sentiment', 0)
                        
                        sentiment_emoji = "😐"
                        if sentiment > 0.3:
                            sentiment_emoji = "📈"
                        elif sentiment < -0.3:
                            sentiment_emoji = "📉"
                        
                        print(f"   {i}. {title}")
                        print(f"      Source: {source} | Sentiment: {sentiment:.2f} {sentiment_emoji}")
                
            except Exception as e:
                print(f"⚠️  Failed to get news for {symbol}: {str(e)}")
        
        # Get overall sentiment if we have new items
        if all_new_items:
            self._analyze_sentiment(all_new_items)
        
        # Get trending topics periodically
        if iteration % 3 == 0:  # Every 3 checks
            self._check_trending_topics()
    
    def _analyze_sentiment(self, news_items):
        """Analyze sentiment of new news items."""
        if not news_items:
            return
        
        total_sentiment = 0
        positive_count = 0
        negative_count = 0
        
        for item in news_items:
            sentiment = item.get('sentiment', 0)
            total_sentiment += sentiment
            
            if sentiment > 0.1:
                positive_count += 1
            elif sentiment < -0.1:
                negative_count += 1
        
        avg_sentiment = total_sentiment / len(news_items)
        
        print(f"\n📊 Sentiment Analysis:")
        print(f"   Average: {avg_sentiment:.3f}")
        print(f"   Positive: {positive_count} items")
        print(f"   Negative: {negative_count} items")
        print(f"   Neutral: {len(news_items) - positive_count - negative_count} items")
        
        # Overall sentiment assessment
        if avg_sentiment > 0.3:
            print("   🟢 Overall: Bullish sentiment")
        elif avg_sentiment < -0.3:
            print("   🔴 Overall: Bearish sentiment")
        else:
            print("   🟡 Overall: Neutral sentiment")
    
    def _check_trending_topics(self):
        """Check trending news topics."""
        try:
            trending = self.client.news.get_trending(
                timeframe="24h",
                limit=10
            )
            
            if trending:
                print(f"\n🔥 Trending Topics (24h):")
                for i, topic in enumerate(trending[:5], 1):
                    name = topic.get('topic', 'Unknown')[:40]
                    mentions = topic.get('mention_count', 0)
                    sentiment = topic.get('avg_sentiment', 0)
                    
                    print(f"   {i}. {name}")
                    print(f"      Mentions: {mentions} | Sentiment: {sentiment:.2f}")
        
        except Exception as e:
            print(f"⚠️  Failed to get trending topics: {str(e)}")


def main():
    """Main function for news monitoring example."""
    print("=== OlaXBT News Monitoring Example ===\n")
    
    # Check environment (obtain JWT via Nexus auth flow — see skills/nexus/SKILL.md)
    if not os.getenv("NEXUS_JWT"):
        print("❌ Please set NEXUS_JWT (obtain via Nexus auth flow)")
        return
    
    # Create monitor
    monitor = NewsMonitor()
    
    # Run with demo settings
    try:
        monitor.monitor_news(
            symbols=["BTC", "ETH", "SOL", "XRP", "ADA"],
            interval_minutes=2,  # Short interval for demo
            max_iterations=3     # Run 3 checks for demo
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()