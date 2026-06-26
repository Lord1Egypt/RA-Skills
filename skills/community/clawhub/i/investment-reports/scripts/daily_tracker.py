#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investage Daily Tracker
每日追蹤系統
"""

import os
import sys
import json
from datetime import datetime, date
from typing import Dict, Any, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import yfinance as yf
import pandas as pd

# 技術分析
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from technical_analyzer import TechnicalAnalyzer

# 估值計算
from valuation_analyzer import ValuationAnalyzer

# 情緒分析
from sentiment_analyzer import SentimentAnalyzer

# 評分系統
from scoring_engine import ScoringEngine

# 配置
DB_CONFIG = {
    "host": "localhost",
    "database": "investage",
    "user": "george",
    "password": ""
}

RECIPIENTS = ["george@precaster.com.tw", "ching@precaster.com.tw"]


class InvestageTracker:
    """Investage 每日追蹤器"""
    
    def __init__(self):
        self.conn = None
        self.connect()
        
    def connect(self):
        """連接資料庫"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            print("✅ Database connected")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    def get_holdings(self) -> List[Dict]:
        """取得持股"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT h.ticker, h.shares, h.avg_cost, s.company_name, s.sector
                FROM holdings h
                JOIN stocks s ON h.ticker = s.ticker
                ORDER BY h.ticker
            """)
            return cur.fetchall()
    
    def get_or_create_thesis(self, ticker: str, ai_analyzer) -> int:
        """取得或建立投資邏輯"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            # 檢查是否有有效版本
            cur.execute("""
                SELECT id FROM thesis_history
                WHERE ticker = %s AND valid_to IS NULL
                ORDER BY version DESC LIMIT 1
            """, (ticker,))
            result = cur.fetchone()
            
            if result:
                return result['id']
            
            # AI 生成投資邏輯
            thesis = ai_analyzer.generate_thesis(ticker)
            
            # 插入新版本
            cur.execute("""
                INSERT INTO thesis_history (ticker, thesis_text, version, valid_from)
                VALUES (%s, %s, 1, %s)
                RETURNING id
            """, (ticker, thesis, date.today()))
            
            return cur.fetchone()['id']
    
    def update_portfolio_value(self, holdings: List[Dict]) -> Dict:
        """更新持股總值"""
        total_value = 0
        prev_total = 0
        positions = []
        
        for h in holdings:
            ticker = h['ticker']
            try:
                data = yf.Ticker(ticker).history(period="2d")
                if len(data) >= 2:
                    current_price = data['Close'].iloc[-1]
                    prev_price = data['Close'].iloc[-2]
                    current_value = current_price * h['shares']
                    prev_value = prev_price * h['shares']
                    
                    positions.append({
                        "ticker": ticker,
                        "shares": float(h['shares']),
                        "current_price": float(current_price),
                        "current_value": float(current_value),
                        "prev_value": float(prev_value),
                        "change_pct": float((current_price - prev_price) / prev_price * 100) if prev_price > 0 else 0,
                        "cost": float(h['avg_cost']),
                        "unrealized_pnl": float(current_value - h['avg_cost'] * h['shares'])
                    })
                    
                    total_value += current_value
                    prev_total += prev_value
            except Exception as e:
                print(f"⚠️ Error getting price for {ticker}: {e}")
        
        return {
            "total_value": total_value,
            "prev_total_value": prev_total,
            "change_pct": ((total_value - prev_total) / prev_total * 100) if prev_total > 0 else 0,
            "positions": positions
        }
    
    def scan_volume_alerts(self, holdings: List[Dict]) -> List[Dict]:
        """掃描放量股票"""
        alerts = []
        
        for h in holdings:
            analyzer = TechnicalAnalyzer(h['ticker'])
            result = analyzer.analyze()
            
            if 'error' not in result:
                if result['volume']['streak'] >= 3:
                    alerts.append({
                        "ticker": h['ticker'],
                        "streak": result['volume']['streak'],
                        "current_price": result['price']['current'],
                        "rsi": result['rsi']['value'],
                        "pattern": result['kline_patterns']['last_pattern']
                    })
        
        return alerts
    
    def generate_daily_report(self, ticker: str) -> Dict:
        """為單一股票生成完整報告"""
        holdings = self.get_holdings()
        h = next((x for x in holdings if x['ticker'] == ticker), None)
        
        if not h:
            return {"error": f"Ticker {ticker} not found in holdings"}
        
        # 技術分析
        tech = TechnicalAnalyzer(ticker)
        tech_result = tech.analyze()
        
        # 估值分析
        val = ValuationAnalyzer(ticker)
        val_result = val.analyze()
        
        # 情緒分析
        sent = SentimentAnalyzer(ticker)
        sent_result = sent.analyze()
        
        # 評分
        scorer = ScoringEngine()
        scores = scorer.calculate_scores(tech_result, val_result, sent_result)
        
        return {
            "ticker": ticker,
            "company_name": h['company_name'],
            "shares": float(h['shares']),
            "avg_cost": float(h['avg_cost']),
            "investment_thesis": h.get('thesis', 'No thesis generated'),
            
            "price": tech_result.get('price', {}),
            "technical": {
                "trend": tech_result.get('trend', {}),
                "rsi": tech_result.get('rsi', {}),
                "volume": tech_result.get('volume', {}),
                "deviation": tech_result.get('deviation_rate', {}),
                "patterns": tech_result.get('kline_patterns', {}),
                "score": tech_result.get('technical_score', 0),
                "summary": tech_result.get('summary', '')
            },
            
            "valuation": {
                "target_low": val_result.get('target_low'),
                "target_high": val_result.get('target_high'),
                "peg": val_result.get('peg'),
                "dcf_fair_value": val_result.get('dcf_fair_value'),
                "score": val_result.get('score', 0)
            },
            
            "sentiment": {
                "polymarket": sent_result.get('polymarket', {}),
                "reddit": sent_result.get('reddit', {}),
                "overall": sent_result.get('overall', {}),
                "macro_view": sent_result.get('macro_view', ''),
                "score": sent_result.get('score', 0)
            },
            
            "scores": scores,
            "recommendation": scores.get('recommendation', 'WATCH'),
            "action_price": scores.get('action_price'),
            "stop_loss": scores.get('stop_loss'),
            "target_price": scores.get('target_price')
        }
    
    def run_daily_update(self) -> Dict:
        """執行每日更新"""
        print(f"\n📊 Investage 每日更新 - {date.today()}")
        print("=" * 50)
        
        holdings = self.get_holdings()
        print(f"📈 持股數量: {len(holdings)}")
        
        # 1. 更新持股總值
        print("\n1️⃣ 更新持股總值...")
        portfolio = self.update_portfolio_value(holdings)
        print(f"   總值: ${portfolio['total_value']:,.2f}")
        print(f"   變化: {portfolio['change_pct']:+.2f}%")
        
        # 2. 掃描放量股票
        print("\n2️⃣ 掃描放量股票...")
        volume_alerts = self.scan_volume_alerts(holdings)
        if volume_alerts:
            for a in volume_alerts:
                print(f"   🚨 {a['ticker']}: 連續{a['streak']}天放量")
        else:
            print("   ✅ 無放量信號")
        
        # 3. 生成買賣建議
        print("\n3️⃣ 生成買賣建議...")
        buy_signals = []
        sell_signals = []
        hold_signals = []
        
        for h in holdings:
            report = self.generate_daily_report(h['ticker'])
            rec = report.get('recommendation', 'HOLD')
            
            if rec == 'BUY':
                buy_signals.append(h['ticker'])
            elif rec == 'SELL':
                sell_signals.append(h['ticker'])
            else:
                hold_signals.append(h['ticker'])
        
        print(f"   🟢 買入: {buy_signals if buy_signals else '無'}")
        print(f"   🔵 持有: {hold_signals if hold_signals else '無'}")
        print(f"   🔴 賣出: {sell_signals if sell_signals else '無'}")
        
        # 儲存快照
        print("\n4️⃣ 儲存快照...")
        self.save_snapshot(portfolio, volume_alerts, buy_signals, sell_signals)
        
        return {
            "date": str(date.today()),
            "portfolio": portfolio,
            "volume_alerts": volume_alerts,
            "buy_signals": buy_signals,
            "sell_signals": sell_signals,
            "hold_signals": hold_signals
        }
    
    def save_snapshot(self, portfolio: Dict, volume_alerts: List, 
                     buy_signals: List, sell_signals: List):
        """儲存每日快照"""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO portfolio_snapshot (
                    snapshot_date, total_value, prev_total_value, 
                    portfolio_change_pct, total_positions,
                    winning_positions, losing_positions,
                    buy_signals, sell_signals, volume_alert
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (snapshot_date) DO UPDATE SET
                    total_value = EXCLUDED.total_value,
                    prev_total_value = EXCLUDED.prev_total_value,
                    portfolio_change_pct = EXCLUDED.portfolio_change_pct,
                    buy_signals = EXCLUDED.buy_signals,
                    sell_signals = EXCLUDED.sell_signals,
                    volume_alert = EXCLUDED.volume_alert
            """, (
                date.today(),
                portfolio['total_value'],
                portfolio['prev_total_value'],
                portfolio['change_pct'],
                len(portfolio['positions']),
                sum(1 for p in portfolio['positions'] if p['unrealized_pnl'] > 0),
                sum(1 for p in portfolio['positions'] if p['unrealized_pnl'] <= 0),
                json.dumps(buy_signals),
                json.dumps(sell_signals),
                json.dumps([a['ticker'] for a in volume_alerts])
            ))
            self.conn.commit()
        print("   ✅ 快照已儲存")
    
    def close(self):
        """關閉連接"""
        if self.conn:
            self.conn.close()


def main():
    """主程式"""
    tracker = InvestageTracker()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "update":
            tracker.run_daily_update()
        elif command == "report":
            ticker = sys.argv[2] if len(sys.argv) > 2 else "AAPL"
            report = tracker.generate_daily_report(ticker)
            print(json.dumps(report, indent=2, default=str))
        elif command == "portfolio":
            holdings = tracker.get_holdings()
            portfolio = tracker.update_portfolio_value(holdings)
            print(json.dumps(portfolio, indent=2, default=str))
        else:
            print("Unknown command")
    else:
        # 預設：執行每日更新
        tracker.run_daily_update()
    
    tracker.close()


if __name__ == "__main__":
    main()
