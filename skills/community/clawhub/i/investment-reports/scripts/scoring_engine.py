#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investage Scoring Engine
綜合評分系統
"""

from typing import Dict, Any, Optional


class ScoringEngine:
    """評分引擎 - 整合所有維度"""
    
    def __init__(self):
        # 權重配置 (可調整)
        self.weights = {
            "valuation": 0.30,      # 估值 30%
            "trend": 0.25,          # 趨勢 25%
            "macro": 0.20,          # 宏觀/情緒 20%
            "technical": 0.15,      # 技術信號 15%
            "risk": 0.10            # 風險 10%
        }
    
    def calculate_scores(
        self, 
        technical: Dict, 
        valuation: Dict, 
        sentiment: Dict
    ) -> Dict[str, Any]:
        """計算綜合評分"""
        
        # 1. 技術評分 (已標準化到 -15 到 +15)
        tech_score = technical.get('technical_score', 0)
        tech_pct = (tech_score + 15) / 30 * 100  # 轉換成 0-100
        
        # 2. 估值評分 (已標準化到 -10 到 +25)
        val_score = valuation.get('score', 0)
        val_pct = (val_score + 10) / 35 * 100  # 轉換成 0-100
        
        # 3. 情緒評分 (已標準化到 -20 到 +20)
        sent_score = sentiment.get('score', 0)
        sent_pct = (sent_score + 20) / 40 * 100  # 轉換成 0-100
        
        # 4. 趨勢評分 (從技術分析中提取)
        trend_info = technical.get('trend', {})
        trend_score = trend_info.get('score', 0)
        trend_pct = (trend_score + 30) / 60 * 100  # 轉換成 0-100
        
        # 5. 風險評分
        risk_info = technical.get('deviation_rate', {})
        risk_penalty = risk_info.get('risk_score', 0)
        # 乖離率風險已經在技術分數中體現
        
        # 計算加權總分 (0-100)
        total_pct = (
            val_pct * self.weights["valuation"] +
            trend_pct * self.weights["trend"] +
            sent_pct * self.weights["macro"] +
            tech_pct * self.weights["technical"] +
            (100 + risk_penalty * 5) * self.weights["risk"]  # 風險是扣分
        )
        
        # 最終決策
        if total_pct >= 65:
            recommendation = "BUY"
        elif total_pct >= 50:
            recommendation = "HOLD"
        elif total_pct >= 40:
            recommendation = "WATCH"
        else:
            recommendation = "SELL"
        
        # 計算建議價
        current_price = technical.get('price', {}).get('current', 0)
        target_low = valuation.get('target_low')
        target_high = valuation.get('target_high')
        dcf = valuation.get('dcf_fair_value')
        
        if recommendation == "BUY":
            # 買入價低於現價 5-10%
            action_price = round(current_price * 0.95, 2) if current_price else None
            stop_loss = round(current_price * 0.90, 2) if current_price else None  # 10% 停損
            target_price = target_high if target_high else round(current_price * 1.15, 2)
        elif recommendation == "HOLD":
            action_price = current_price
            stop_loss = round(current_price * 0.92, 2) if current_price else None
            target_price = target_high if target_high else round(current_price * 1.10, 2)
        elif recommendation == "WATCH":
            action_price = None
            stop_loss = round(current_price * 0.90, 2) if current_price else None
            target_price = target_high if target_high else None
        else:  # SELL
            action_price = round(current_price * 1.02, 2) if current_price else None
            stop_loss = None
            target_price = None
        
        return {
            "total_score": round(total_pct, 1),
            "max_score": 100,
            "percentage": f"{total_pct:.0f}%",
            
            "breakdown": {
                "valuation": {
                    "score": round(val_pct, 1),
                    "raw_score": val_score,
                    "weight": self.weights["valuation"],
                    "weighted": round(val_pct * self.weights["valuation"], 1)
                },
                "trend": {
                    "score": round(trend_pct, 1),
                    "raw_score": trend_score,
                    "weight": self.weights["trend"],
                    "weighted": round(trend_pct * self.weights["trend"], 1)
                },
                "macro": {
                    "score": round(sent_pct, 1),
                    "raw_score": sent_score,
                    "weight": self.weights["macro"],
                    "weighted": round(sent_pct * self.weights["macro"], 1)
                },
                "technical": {
                    "score": round(tech_pct, 1),
                    "raw_score": tech_score,
                    "weight": self.weights["technical"],
                    "weighted": round(tech_pct * self.weights["technical"], 1)
                },
                "risk": {
                    "score": round(100 + risk_penalty * 5, 1),
                    "raw_score": risk_penalty,
                    "weight": self.weights["risk"],
                    "weighted": round((100 + risk_penalty * 5) * self.weights["risk"], 1)
                }
            },
            
            "recommendation": recommendation,
            "action_price": action_price,
            "stop_loss": stop_loss,
            "target_price": target_price,
            
            "signals": self._generate_signals(technical, valuation, sentiment)
        }
    
    def _generate_signals(
        self, 
        technical: Dict, 
        valuation: Dict, 
        sentiment: Dict
    ) -> Dict[str, List[str]]:
        """生成具體信號"""
        signals = {
            "bullish": [],
            "bearish": [],
            "neutral": []
        }
        
        # 估值信號
        peg = valuation.get('peg')
        if peg and peg < 1:
            signals["bullish"].append(f"PEG {peg:.2f} 低於1")
        elif peg and peg > 2:
            signals["bearish"].append(f"PEG {peg:.2f} 高於2")
        
        dcf = valuation.get('dcf_fair_value')
        current = technical.get('price', {}).get('current', 0)
        if dcf and current:
            if dcf > current * 1.1:
                signals["bullish"].append(f"DCF ${dcf} > 現價 ${current}")
            elif dcf < current * 0.9:
                signals["bearish"].append(f"DCF ${dcf} < 現價 ${current}")
        
        # 趨勢信號
        trend = technical.get('trend', {})
        if trend.get('trend') == 'STRONG_UPTREND':
            signals["bullish"].append("多頭排列")
        elif trend.get('trend') == 'DOWNTREND':
            signals["bearish"].append("空頭排列")
        
        # RSI 信號
        rsi = technical.get('rsi', {})
        if rsi.get('value') and rsi['value'] < 30:
            signals["bullish"].append(f"RSI {rsi['value']:.0f} 超賣")
        elif rsi.get('value') and rsi['value'] > 70:
            signals["bearish"].append(f"RSI {rsi['value']:.0f} 超買")
        
        # 乖離率信號
        deviation = technical.get('deviation_rate', {})
        if deviation.get('ma30') and abs(deviation['ma30']) > 10:
            if deviation['ma30'] > 0:
                signals["bearish"].append(f"乖離率 +{deviation['ma30']:.1f}% 偏高")
            else:
                signals["bullish"].append(f"乖離率 {deviation['ma30']:.1f}% 偏低")
        
        # K線型態信號
        patterns = technical.get('kline_patterns', {})
        last = patterns.get('last_pattern')
        if last:
            if last['type'] == 'BULLISH':
                signals["bullish"].append(f"K線型態: {last['pattern']}")
            elif last['type'] == 'BEARISH':
                signals["bearish"].append(f"K線型態: {last['pattern']}")
        
        # 成交量信號
        volume = technical.get('volume', {})
        if volume.get('streak', 0) >= 3:
            signals["bullish"].append(f"連續{volume['streak']}天放量")
        
        # 情緒信號
        overall = sentiment.get('overall', {})
        if overall.get('interpretation') == 'BULLISH':
            signals["bullish"].append("市場情緒偏多")
        elif overall.get('interpretation') == 'BEARISH':
            signals["bearish"].append("市場情緒偏空")
        
        return signals


def main():
    """測試"""
    scoring = ScoringEngine()
    
    # 模擬數據
    technical = {
        "technical_score": 8,
        "price": {"current": 175.0},
        "trend": {"trend": "STRONG_UPTREND", "score": 25},
        "rsi": {"value": 55},
        "deviation_rate": {"ma30": 5, "risk_score": 0},
        "kline_patterns": {"last_pattern": {"type": "BULLISH", "pattern": "HAMMER"}},
        "volume": {"streak": 3}
    }
    
    valuation = {
        "score": 15,
        "peg": 0.8,
        "dcf_fair_value": 195,
        "target_low": 180,
        "target_high": 220
    }
    
    sentiment = {
        "score": 8,
        "overall": {"interpretation": "BULLISH"}
    }
    
    result = scoring.calculate_scores(technical, valuation, sentiment)
    
    print("\n📊 綜合評分報告")
    print("=" * 50)
    print(f"總分: {result['total_score']}/100 ({result['percentage']})")
    print(f"建議: {result['recommendation']}")
    print(f"買入價: ${result['action_price']}")
    print(f"停損價: ${result['stop_loss']}")
    print(f"目標價: ${result['target_price']}")
    
    print("\n分項:")
    for key, val in result['breakdown'].items():
        print(f"  {key}: {val['score']}/100 (原始: {val['raw_score']}, 權重: {val['weight']})")
    
    print("\n信號:")
    print(f"  🟢 多頭: {result['signals']['bullish']}")
    print(f"  🔴 空頭: {result['signals']['bearish']}")


if __name__ == "__main__":
    main()
