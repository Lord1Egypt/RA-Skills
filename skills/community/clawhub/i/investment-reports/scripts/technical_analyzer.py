#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investage Technical Analysis Module
技術分析：MA、RSI、成交量、K線型態、乖離率
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
import json

class TechnicalAnalyzer:
    """技術分析器"""
    
    def __init__(self, ticker: str, period: str = "1y"):
        self.ticker = ticker
        self.period = period
        self.data: Optional[pd.DataFrame] = None
        
    def fetch_data(self) -> bool:
        """取得數據"""
        try:
            ticker_obj = yf.Ticker(self.ticker)
            self.data = ticker_obj.history(period=self.period)
            return not self.data.empty
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False
    
    def calculate_ma(self, window: int) -> pd.Series:
        """計算 MA"""
        if self.data is None:
            return pd.Series()
        return self.data['Close'].rolling(window=window).mean()
    
    def calculate_rsi(self, window: int = 14) -> pd.Series:
        """計算 RSI"""
        if self.data is None:
            return pd.Series()
        
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def get_volume_status(self, days: int = 3, avg_days: int = 30) -> Dict[str, Any]:
        """成交量分析：連續N天是否 > N天平均"""
        if self.data is None or len(self.data) < avg_days:
            return {"status": "UNKNOWN", "streak": 0, "avg_volume": 0, "current_volume": 0, "ratio": 0}
        
        volumes = self.data['Volume'].tail(avg_days).values
        avg_volume = np.mean(volumes)
        current_volume = volumes[-1]
        
        # 計算連續放量天數
        streak = 0
        for i in range(len(volumes) - 1, -1, -1):
            if volumes[i] > avg_volume:
                streak += 1
            else:
                break
        
        return {
            "status": "ABOVE" if current_volume > avg_volume else "BELOW",
            "streak": streak,
            "avg_volume": float(avg_volume),
            "current_volume": float(current_volume),
            "ratio": float(current_volume / avg_volume) if avg_volume > 0 else 0
        }
    
    def calculate_deviation_rate(self, ma_window: int = 30) -> float:
        """計算乖離率 = (現在價格 - MA) / MA * 100%"""
        if self.data is None:
            return 0
        
        current_price = self.data['Close'].tail(1).values[0]
        ma = self.calculate_ma(ma_window).tail(1).values[0]
        
        if ma == 0:
            return 0
        
        return float((current_price - ma) / ma * 100)
    
    def detect_kline_patterns(self) -> Dict[str, Any]:
        """K線型態偵測"""
        if self.data is None or len(self.data) < 3:
            return {"patterns": [], "last_pattern": None}
        
        df = self.data.tail(5).copy()
        
        # 計算基本元素
        df['body'] = abs(df['Close'] - df['Open'])
        df['upper_shadow'] = df['High'] - df[['Close', 'Open']].max(axis=1)
        df['lower_shadow'] = df[['Close', 'Open']].min(axis=1) - df['Low']
        df['range'] = df['High'] - df['Low']
        
        patterns = []
        
        for idx, row in df.iterrows():
            if row['range'] == 0:
                continue
                
            body_ratio = row['body'] / row['range'] if row['range'] > 0 else 0
            lower_shadow_ratio = row['lower_shadow'] / row['range'] if row['range'] > 0 else 0
            upper_shadow_ratio = row['upper_shadow'] / row['range'] if row['range'] > 0 else 0
            
            pattern = None
            pattern_type = None
            
            # 錘子線 (Hammer) - 止跌回升信號
            if (lower_shadow_ratio > 0.6 and 
                body_ratio < 0.3 and 
                upper_shadow_ratio < 0.1):
                pattern = "HAMMER"
                pattern_type = "BULLISH"
                
            # 流星線 (Shooting Star) - 見頂回落信號
            elif (upper_shadow_ratio > 0.6 and 
                  body_ratio < 0.3 and 
                  lower_shadow_ratio < 0.1):
                pattern = "SHOOTING_STAR"
                pattern_type = "BEARISH"
                
            # 十字星 (Doji) - 反轉信號
            elif body_ratio < 0.1:
                pattern = "DOJI"
                pattern_type = "NEUTRAL"
                
            # 吞噬 (Engulfing)
            if len(df) >= 2:
                prev_idx = df.index.get_loc(idx) - 1
                if prev_idx >= 0:
                    prev_row = df.iloc[prev_idx]
                    curr_body_top = max(row['Close'], row['Open'])
                    curr_body_bottom = min(row['Close'], row['Open'])
                    prev_body_top = max(prev_row['Close'], prev_row['Open'])
                    prev_body_bottom = min(prev_row['Close'], prev_row['Open'])
                    
                    # 多頭吞噬
                    if (row['Close'] > row['Open'] and 
                        prev_row['Close'] < prev_row['Open'] and
                        curr_body_bottom < prev_body_top and
                        curr_body_top > prev_row['Close']):
                        pattern = "BULLISH_ENGULFING"
                        pattern_type = "BULLISH"
                    # 空頭吞噬
                    elif (row['Close'] < row['Open'] and 
                          prev_row['Close'] > prev_row['Open'] and
                          curr_body_top > prev_body_bottom and
                          curr_body_bottom < prev_row['Open']):
                        pattern = "BEARISH_ENGULFING"
                        pattern_type = "BEARISH"
            
            if pattern:
                patterns.append({
                    "date": str(idx.date()),
                    "pattern": pattern,
                    "type": pattern_type,
                    "body_ratio": round(body_ratio, 2)
                })
        
        return {
            "patterns": patterns[-3:],  # 最近3個型態
            "last_pattern": patterns[-1] if patterns else None,
            "bullish_count": sum(1 for p in patterns if p['type'] == 'BULLISH'),
            "bearish_count": sum(1 for p in patterns if p['type'] == 'BEARISH')
        }
    
    def get_trend_analysis(self) -> Dict[str, Any]:
        """趨勢分析：MA 排列判斷"""
        if self.data is None:
            return {"trend": "UNKNOWN", "score": 0, "details": {}}
        
        ma30 = self.calculate_ma(30).tail(1).values[0]
        ma100 = self.calculate_ma(100).tail(1).values[0]
        ma200 = self.calculate_ma(200).tail(1).values[0] if len(self.data) >= 200 else None
        current_price = self.data['Close'].tail(1).values[0]
        
        details = {
            "ma30": round(ma30, 2) if not np.isnan(ma30) else None,
            "ma100": round(ma100, 2) if not np.isnan(ma100) else None,
            "ma200": round(ma200, 2) if ma200 and not np.isnan(ma200) else None,
            "current_price": round(current_price, 2)
        }
        
        # 評分
        score = 0
        
        if ma30 and current_price > ma30:
            score += 10
        if ma100 and current_price > ma100:
            score += 10
        if ma200 and current_price > ma200:
            score += 10
            
        # MA 排列
        trend = "NEUTRAL"
        if ma30 and ma100 and ma200:
            if ma30 > ma100 > ma200:
                trend = "STRONG_UPTREND"
                score = 30
            elif ma30 > ma100:
                trend = "UPTREND"
                score = max(score, 20)
        elif ma30 and ma100:
            if ma30 < ma100:
                trend = "DOWNTREND"
                score = -20
        
        return {
            "trend": trend,
            "score": score,
            "details": details
        }
    
    def analyze(self) -> Dict[str, Any]:
        """完整技術分析"""
        if not self.fetch_data():
            return {"error": "Failed to fetch data"}
        
        rsi = self.calculate_rsi()
        rsi_value = round(rsi.tail(1).values[0], 2) if not rsi.empty else None
        volume_status = self.get_volume_status()
        deviation = self.calculate_deviation_rate()
        patterns = self.detect_kline_patterns()
        trend = self.get_trend_analysis()
        
        # RSI 評分
        rsi_score = 0
        if rsi_value:
            if rsi_value < 30:
                rsi_score = 10  # 超賣，可能是買入機會
            elif rsi_value < 50:
                rsi_score = 8
            elif rsi_value < 70:
                rsi_score = 5  # 健康上漲
            else:
                rsi_score = -5  # 超買
        
        # 技術信號評分
        technical_score = rsi_score
        if volume_status["streak"] >= 3:
            technical_score += 5  # 連續放量
        if patterns["last_pattern"]:
            if patterns["last_pattern"]["type"] == "BULLISH":
                technical_score += 5
            elif patterns["last_pattern"]["type"] == "BEARISH":
                technical_score -= 5
        
        return {
            "ticker": self.ticker,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            
            "price": {
                "current": round(self.data['Close'].tail(1).values[0], 2),
                "open": round(self.data['Open'].tail(1).values[0], 2),
                "high": round(self.data['High'].tail(1).values[0], 2),
                "low": round(self.data['Low'].tail(1).values[0], 2),
                "prev_close": round(self.data['Close'].tail(2).iloc[0], 2) if len(self.data) >= 2 else None,
                "change_pct": round((self.data['Close'].pct_change().tail(1).values[0] * 100), 2) if len(self.data) >= 2 else 0
            },
            
            "moving_averages": trend["details"],
            "trend": trend,
            
            "rsi": {
                "value": rsi_value,
                "interpretation": "OVERSOLD" if rsi_value and rsi_value < 30 else 
                                ("OVERBOUGHT" if rsi_value and rsi_value > 70 else "NEUTRAL"),
                "score": rsi_score
            },
            
            "volume": volume_status,
            
            "deviation_rate": {
                "ma30": round(deviation, 2),
                "interpretation": "HIGH" if abs(deviation) > 10 else 
                                 ("MODERATE" if abs(deviation) > 5 else "NORMAL"),
                "risk_score": -5 if abs(deviation) > 10 else (-2 if abs(deviation) > 5 else 0)
            },
            
            "kline_patterns": patterns,
            
            "technical_score": max(-15, min(15, technical_score)),  # 限制在 -15 到 +15
            
            "summary": self._generate_summary(rsi_value, deviation, volume_status, patterns, trend)
        }
    
    def _generate_summary(self, rsi: Optional[float], deviation: float, 
                         volume: Dict, patterns: Dict, trend: Dict) -> str:
        """生成技術分析摘要"""
        parts = []
        
        # RSI
        if rsi:
            if rsi < 30:
                parts.append(f"RSI {rsi} 超賣，可能反彈")
            elif rsi > 70:
                parts.append(f"RSI {rsi} 超買，注意風險")
            else:
                parts.append(f"RSI {rsi} 正常")
        
        # 乖離率
        if abs(deviation) > 10:
            parts.append(f"乖離率 {deviation:.1f}% 偏高")
        elif abs(deviation) > 5:
            parts.append(f"乖離率 {deviation:.1f}% 適中")
        
        # 成交量
        if volume["streak"] >= 3:
            parts.append("連續放量")
        
        # 型態
        if patterns["last_pattern"]:
            pattern_names = {
                "HAMMER": "錘子線(止跌)",
                "SHOOTING_STAR": "流星線(見頂)",
                "DOJI": "十字星(觀望)",
                "BULLISH_ENGULFING": "多頭吞噬(回升)",
                "BEARISH_ENGULFING": "空頭吞噬(回落)"
            }
            name = pattern_names.get(patterns["last_pattern"]["pattern"], patterns["last_pattern"]["pattern"])
            parts.append(f"最新型態: {name}")
        
        # 趨勢
        trend_names = {
            "STRONG_UPTREND": "多頭排列，上漲趨勢明確",
            "UPTREND": "震盪向上",
            "DOWNTREND": "空頭排列，下跌趨勢",
            "NEUTRAL": "方向不明"
        }
        parts.append(trend_names.get(trend["trend"], trend["trend"]))
        
        return "; ".join(parts)


def main():
    """測試"""
    import sys
    
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    
    analyzer = TechnicalAnalyzer(ticker)
    result = analyzer.analyze()
    
    print(f"\n📊 {ticker} 技術分析報告")
    print("=" * 50)
    print(f"價格: ${result['price']['current']}")
    print(f"RSI: {result['rsi']['value']} ({result['rsi']['interpretation']})")
    print(f"乖離率: {result['deviation_rate']['ma30']}%")
    print(f"成交量: {result['volume']['status']} (連續{int(result['volume']['streak'])}天放量)")
    print(f"趨勢: {result['trend']['trend']}")
    print(f"K線型態: {result['kline_patterns']['last_pattern']}")
    print(f"\n技術評分: {result['technical_score']}/15")
    print(f"\n摘要: {result['summary']}")


if __name__ == "__main__":
    main()
