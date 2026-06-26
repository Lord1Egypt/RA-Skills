#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investage Valuation Analyzer
估值分析：PEG、DCF、目標價
"""

import yfinance as yf
import numpy as np
from typing import Dict, Any, Optional
import json

class ValuationAnalyzer:
    """估值分析器"""
    
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.ticker_obj = yf.Ticker(ticker)
        
    def get_financial_data(self) -> Dict:
        """取得財報數據"""
        try:
            info = self.ticker_obj.info
            
            # 基本估值數據
            pe_ratio = info.get('trailingPE', None)
            forward_pe = info.get('forwardPE', None)
            peg_ratio = info.get('pegRatio', None)
            
            # 營收成長
            revenue_growth = info.get('revenueGrowth', 0) * 100
            earnings_growth = info.get('earningsGrowth', 0) * 100
            
            # EPS
            eps_current = info.get('trailingEps', None)
            eps_forward = info.get('forwardEps', None)
            
            # 股息
            dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
            
            # 市值
            market_cap = info.get('marketCap', None)
            
            # 52週範圍
            week52_high = info.get('fiftyTwoWeekHigh', None)
            week52_low = info.get('fiftyTwoWeekLow', None)
            
            return {
                "pe_ratio": pe_ratio,
                "forward_pe": forward_pe,
                "peg_ratio": peg_ratio,
                "revenue_growth": revenue_growth,
                "earnings_growth": earnings_growth,
                "eps_current": eps_current,
                "eps_forward": eps_forward,
                "dividend_yield": dividend_yield,
                "market_cap": market_cap,
                "week52_high": week52_high,
                "week52_low": week52_low,
                "current_price": info.get('currentPrice') or info.get('regularMarketPrice'),
                "target_mean_price": info.get('targetMeanPrice'),
                "recommendation": info.get('recommendationKey')
            }
        except Exception as e:
            print(f"Error getting financial data: {e}")
            return {}
    
    def calculate_dcf(self, years: int = 5, discount_rate: float = 0.10) -> Optional[float]:
        """簡化 DCF 計算 - 使用 FCFE per share"""
        try:
            info = self.ticker_obj.info
            
            # 取得自由現金流 (以百萬為單位)
            fcfe = info.get('freeCashflow', 0)
            if not fcfe or fcfe < 0:
                return None
            
            # 取得流通股數 (轉換成百萬)
            shares = info.get('sharesOutstanding', 0)
            if not shares or shares <= 0:
                return None
            
            # FCFE per share (轉換成美元)
            fcfe_per_share = (fcfe / shares) if shares > 0 else 0
            
            if fcfe_per_share <= 0:
                return None
            
            # 簡化假設：現金流每年成長 10%
            growth_rate = 0.10
            terminal_growth = 0.03  # 永續成長率
            
            # 預測未來現金流並計算現值
            pv_cashflows = 0
            for year in range(1, years + 1):
                cf = fcfe_per_share * (1 + growth_rate) ** year
                pv = cf / (1 + discount_rate) ** year
                pv_cashflows += pv
            
            # 永續價值 (Gordon Growth Model)
            terminal_cf = fcfe_per_share * (1 + growth_rate) ** years * (1 + terminal_growth)
            terminal_value = terminal_cf / (discount_rate - terminal_growth)
            pv_terminal = terminal_value / (1 + discount_rate) ** years
            
            dcf_per_share = pv_cashflows + pv_terminal
            
            return round(dcf_per_share, 2)
            
        except Exception as e:
            print(f"DCF calculation error: {e}")
            return None
    
    def calculate_target_price(self) -> Dict[str, float]:
        """計算目標價範圍 - 優先使用分析師預期"""
        try:
            info = self.ticker_obj.info
            
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            target_mean = info.get('targetMeanPrice')
            target_high = info.get('targetHighPrice')
            target_low = info.get('targetLowPrice')
            
            if not current_price:
                return {"low": None, "mid": None, "high": None}
            
            # 如果有分析師目標價，用分析師的
            if target_mean:
                # 樂觀 = 均價 * 1.2, 保守 = 均價 * 0.8
                mid = target_mean
                high = target_high if target_high else mid * 1.3
                low = target_low if target_low else mid * 0.7
            else:
                # 否則用 DCF
                dcf = self.calculate_dcf()
                if dcf:
                    high = dcf * 1.15
                    low = dcf * 0.85
                    mid = dcf
                else:
                    high = current_price * 1.2
                    low = current_price * 0.8
                    mid = current_price
            
            return {
                "low": round(low, 2),
                "mid": round(mid, 2),
                "high": round(high, 2)
            }
            
        except Exception as e:
            print(f"Target price calculation error: {e}")
            return {"low": None, "mid": None, "high": None}
    
    def analyze(self) -> Dict[str, Any]:
        """完整估值分析"""
        financials = self.get_financial_data()
        target = self.calculate_target_price()
        dcf = self.calculate_dcf()
        
        current_price = financials.get('current_price', 0)
        
        # 估值評分
        score = 0
        details = []
        
        # PEG 評分
        peg = financials.get('peg_ratio')
        if peg:
            if peg < 0.5:
                score += 15
                details.append(f"PEG {peg:.2f} 極低，成長被嚴重低估")
            elif peg < 1:
                score += 10
                details.append(f"PEG {peg:.2f} 低於1，成長被低估")
            elif peg < 1.5:
                score += 5
                details.append(f"PEG {peg:.2f} 合理")
            else:
                score -= 5
                details.append(f"PEG {peg:.2f} 偏高")
        
        # PE 評分
        pe = financials.get('pe_ratio')
        if pe and pe > 0:
            if pe < 15:
                score += 5
                details.append(f"PE {pe:.1f} 低，價值合理")
            elif pe > 40:
                score -= 5
                details.append(f"PE {pe:.1f} 高，估值偏貴")
        
        # 與目標價比較
        if target.get('mid') and current_price:
            upside = (target['mid'] - current_price) / current_price * 100
            if upside > 30:
                score += 5
                details.append(f"潛在上漲空間 {upside:.0f}%")
            elif upside < 0:
                score -= 5
                details.append(f"潛在下跌風險 {upside:.0f}%")
        
        # 限制分數
        score = max(-10, min(25, score))
        
        return {
            "ticker": self.ticker,
            "analysis_date": str(financials.get('analysis_date', '')),
            
            "current_price": current_price,
            
            "pe_ratio": financials.get('pe_ratio'),
            "forward_pe": financials.get('forward_pe'),
            "peg": peg,
            
            "revenue_growth": financials.get('revenue_growth'),
            "earnings_growth": financials.get('earnings_growth'),
            "dividend_yield": financials.get('dividend_yield'),
            
            # Yahoo Finance 分析師目標價
            "analyst_target": {
                "low": target.get('low'),
                "mid": target.get('mid'),
                "high": target.get('high'),
                "source": "Yahoo Finance 分析師共識"
            },
            
            # 我們的 DCF 計算 (標示為 inveStage)
            "investage_dcf": {
                "value": dcf,
                "source": "inveStage 估計 (待驗證)",
                "note": "計算模型待優化，僅供參考"
            },
            
            "week52_range": {
                "high": financials.get('week52_high'),
                "low": financials.get('week52_low'),
                "position_pct": ((current_price - financials.get('week52_low', 0)) / 
                                 (financials.get('week52_high', current_price) - financials.get('week52_low', 0)) * 100)
                if financials.get('week52_high') and financials.get('week52_low') else None
            },
            
            "analyst_recommendation": financials.get('recommendation'),
            
            "score": score,
            "details": details,
            
            # 為了向後相容，保留這些欄位
            "target_low": target.get('low'),
            "target_high": target.get('high'),
            "target_mid": target.get('mid'),
            "dcf_fair_value": dcf
        }


def main():
    """測試"""
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    
    analyzer = ValuationAnalyzer(ticker)
    result = analyzer.analyze()
    
    print(f"\n💰 {ticker} 估值分析")
    print("=" * 50)
    print(f"現價: ${result['current_price']}")
    print(f"PE: {result['pe_ratio']}")
    print(f"PEG: {result['peg']}")
    print(f"DCF: ${result['dcf_fair_value']}")
    print(f"目標價: ${result['target_low']} - ${result['target_high']}")
    print(f"\n估值評分: {result['score']}/25")
    print(f"原因: {'; '.join(result['details'])}")


if __name__ == "__main__":
    main()
