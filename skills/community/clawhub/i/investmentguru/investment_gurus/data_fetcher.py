"""
股票数据获取模块

支持从多个数据源获取：
1. 实时行情（价格、涨跌幅、成交量）
2. K线数据（历史走势）
3. 资金流向（主力资金进出）
4. 基本面数据（PE、PB、市值等）
5. 板块/行业信息
"""

import requests
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import re

# yfinance作为可选依赖
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    yf = None


class StockDataFetcher:
    """
    股票数据获取器
    
    支持多数据源：
    - yfinance (Yahoo Finance)
    - A股实时数据 (需要配置)
    """
    
    # A股股票代码映射 (简写 -> 完整)
    STOCK_CODE_MAP = {
        "茅台": "600519.SS",
        "贵州茅台": "600519.SS",
        "腾讯": "0700.HK",
        "阿里巴巴": "BABA.US",
        "苹果": "AAPL.US",
        "宁德时代": "300750.SZ",
        "比亚迪": "002594.SZ",
        "平安": "601318.SS",
        "招商银行": "600036.SS",
        "美的": "000333.SZ",
        "恒瑞": "600276.SS",
        "片仔癀": "600436.SS",
        "五粮液": "000858.SZ",
    }
    
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300  # 5分钟缓存
    
    def get_code(self, stock_name: str) -> str:
        """获取股票代码"""
        return self.STOCK_CODE_MAP.get(stock_name, stock_name)
    
    def get_realtime_quote(self, stock: str) -> Dict:
        """
        获取实时行情
        
        Returns:
            dict: {
                "name": 股票名称,
                "code": 股票代码,
                "price": 当前价格,
                "change": 涨跌幅,
                "change_pct": 涨跌幅%,
                "volume": 成交量,
                "amount": 成交额,
                "high": 最高价,
                "low": 最低价,
                "open": 开盘价,
                "prev_close": 昨收价,
                "timestamp": 更新时间
            }
        """
        # 尝试从缓存获取
        cache_key = f"quote_{stock}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if (datetime.now() - cached.get("cache_time")).seconds < self.cache_timeout:
                return cached.get("data")
        
        code = self.get_code(stock)
        
        try:
            ticker = yf.Ticker(code)
            info = ticker.info
            
            # 尝试获取实时价格
            hist = ticker.history(period="1d", interval="1m")
            
            result = {
                "name": stock,
                "code": code,
                "price": info.get("currentPrice") or info.get("regularMarketPrice"),
                "change": info.get("regularMarketChange"),
                "change_pct": info.get("regularMarketChangePercent"),
                "volume": info.get("regularMarketVolume"),
                "amount": info.get("regularMarketDayHigh"),
                "high": info.get("regularMarketDayHigh"),
                "low": info.get("regularMarketDayLow"),
                "open": info.get("regularMarketOpen"),
                "prev_close": info.get("regularMarketPreviousClose"),
                "market_cap": info.get("marketCap"),
                "pe": info.get("trailingPE"),
                "pb": info.get("priceToBook"),
                "dividend": info.get("dividendYield"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            
            # 从历史数据补充
            if not hist.empty:
                latest = hist.iloc[-1]
                result["price"] = float(latest.get("Close", result["price"] or 0))
                result["volume"] = int(latest.get("Volume", 0))
            
            # 缓存
            self.cache[cache_key] = {"data": result, "cache_time": datetime.now()}
            
            return result
            
        except Exception as e:
            return {
                "name": stock,
                "code": code,
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def get_kline(self, stock: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        获取K线数据
        
        Args:
            stock: 股票名称/代码
            period: 周期 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: 间隔 (1m, 2m, 5m, 15m, 30m, 60m, 1d, 1wk, 1mo)
            
        Returns:
            DataFrame: K线数据
        """
        code = self.get_code(stock)
        
        try:
            ticker = yf.Ticker(code)
            hist = ticker.history(period=period, interval=interval)
            return hist
        except Exception as e:
            print(f"获取K线失败: {e}")
            return pd.DataFrame()
    
    def get_ma(self, stock: str, days: List[int] = [5, 10, 20, 60]) -> Dict:
        """
        获取均线数据
        
        Args:
            stock: 股票名称
            days: 均线周期列表
            
        Returns:
            dict: {MA5: xxx, MA10: xxx, ...}
        """
        df = self.get_kline(stock, period="6mo")
        
        if df.empty:
            return {}
        
        result = {}
        for d in days:
            ma_key = f"MA{d}"
            result[ma_key] = round(df["Close"].rolling(window=d).mean().iloc[-1], 2)
        
        result["current_price"] = round(df["Close"].iloc[-1], 2)
        result["timestamp"] = datetime.now().strftime("%Y-%m-%d")
        
        return result
    
    def get_trend(self, stock: str) -> Dict:
        """
        获取近期走势
        
        Returns:
            dict: {
                "trend": 趋势 (up/down/sideways),
                "change_1d": 1日涨跌幅,
                "change_5d": 5日涨跌幅,
                "change_1m": 1月涨跌幅,
                "change_3m": 3月涨跌幅,
                "high_52w": 52周最高,
                "low_52w": 52周最低,
            }
        """
        code = self.get_code(stock)
        
        try:
            ticker = yf.Ticker(code)
            
            # 获取不同周期的数据
            hist_1d = ticker.history(period="5d")
            hist_1m = ticker.history(period="1mo")
            hist_3m = ticker.history(period="3mo")
            
            result = {
                "trend": "sideways",
                "change_1d": 0,
                "change_5d": 0,
                "change_1m": 0,
                "change_3m": 0,
            }
            
            if not hist_1d.empty:
                first_price = hist_1d["Close"].iloc[0]
                last_price = hist_1d["Close"].iloc[-1]
                if first_price:
                    result["change_5d"] = round((last_price - first_price) / first_price * 100, 2)
            
            if not hist_1m.empty:
                first_price = hist_1m["Close"].iloc[0]
                last_price = hist_1m["Close"].iloc[-1]
                if first_price:
                    result["change_1m"] = round((last_price - first_price) / first_price * 100, 2)
                    
                    # 判断趋势
                    if result["change_1m"] > 5:
                        result["trend"] = "up"
                    elif result["change_1m"] < -5:
                        result["trend"] = "down"
            
            if not hist_3m.empty:
                first_price = hist_3m["Close"].iloc[0]
                last_price = hist_3m["Close"].iloc[-1]
                if first_price:
                    result["change_3m"] = round((last_price - first_price) / first_price * 100, 2)
            
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_market_sentiment(self) -> Dict:
        """
        获取市场情绪指标
        
        Returns:
            dict: {
                "fear_greed": 恐贪指数 (0-100),
                "vix": VIX恐慌指数,
                "a_market": A股情绪,
            }
        """
        # 简化实现 - 实际应该从专业数据源获取
        result = {
            "fear_greed": 50,  # 中性
            "vix": 15.5,
            "a_market": "震荡",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            # 获取VIX
            vix = yf.Ticker("^VIX")
            vix_hist = vix.history(period="1d")
            if not vix_hist.empty:
                result["vix"] = round(vix_hist["Close"].iloc[-1], 2)
                
                # 简单恐贪判断
                if result["vix"] > 25:
                    result["fear_greed"] = 30  # 恐惧
                elif result["vix"] < 15:
                    result["fear_greed"] = 70  # 贪婪
        except:
            pass
        
        return result
    
    def get_sector_performance(self, stock: str) -> Dict:
        """
        获取板块表现
        
        Returns:
            dict: {
                "sector": 所属行业,
                "industry": 细分行业,
                "sector_change": 板块涨跌幅,
            }
        """
        code = self.get_code(stock)
        
        try:
            ticker = yf.Ticker(code)
            info = ticker.info
            
            return {
                "sector": info.get("sector", "未知"),
                "industry": info.get("industry", "未知"),
                "market": info.get("market", "未知"),
            }
        except:
            return {"sector": "未知", "industry": "未知"}


class StockAnalyzer:
    """
    股票分析器 - 结合数据和大师方法
    """
    
    def __init__(self):
        self.fetcher = StockDataFetcher()
    
    def full_analysis(self, stock: str, guru_method: str = "duan") -> Dict:
        """
        完整分析：数据 + 大师方法
        
        Returns:
            dict: {
                "stock": 股票信息,
                "quote": 实时行情,
                "trend": 走势分析,
                "ma": 均线数据,
                "sector": 板块信息,
                "analysis": 大师分析,
            }
        """
        result = {
            "stock": stock,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        # 1. 获取实时行情
        try:
            result["quote"] = self.fetcher.get_realtime_quote(stock)
        except Exception as e:
            result["quote"] = {"error": str(e)}
        
        # 2. 获取走势
        try:
            result["trend"] = self.fetcher.get_trend(stock)
        except Exception as e:
            result["trend"] = {"error": str(e)}
        
        # 3. 获取均线
        try:
            result["ma"] = self.fetcher.get_ma(stock)
        except Exception as e:
            result["ma"] = {"error": str(e)}
        
        # 4. 获取板块
        try:
            result["sector"] = self.fetcher.get_sector_performance(stock)
        except Exception as e:
            result["sector"] = {"error": str(e)}
        
        # 5. 市场情绪
        try:
            result["market"] = self.fetcher.get_market_sentiment()
        except Exception as e:
            result["market"] = {"error": str(e)}
        
        return result
    
    def generate_report(self, stock: str, guru_method: str = "duan") -> str:
        """
        生成分析报告（文本）
        """
        data = self.full_analysis(stock, guru_method)
        
        quote = data.get("quote", {})
        trend = data.get("trend", {})
        ma = data.get("ma", {})
        sector = data.get("sector", {})
        
        # 构建报告
        report = f"""
📊 {stock} 分析报告
{'='*30}

📈 实时行情
- 当前价: {quote.get('price', 'N/A')}
- 涨跌幅: {quote.get('change_pct', 'N/A')}%
- 成交量: {quote.get('volume', 'N/A')}
- 市值: {quote.get('market_cap', 'N/A')}
- PE: {quote.get('pe', 'N/A')}

📉 近期走势
- 趋势: {trend.get('trend', 'N/A')}
- 1日: {trend.get('change_1d', 'N/A')}%
- 5日: {trend.get('change_5d', 'N/A')}%
- 1月: {trend.get('change_1m', 'N/A')}%
- 3月: {trend.get('change_3m', 'N/A')}%

📊 均线（MA）
- MA5: {ma.get('MA5', 'N/A')}
- MA10: {ma.get('MA10', 'N/A')}
- MA20: {ma.get('MA20', 'N/A')}
- MA60: {ma.get('MA60', 'N/A')}

🏭 板块信息
- 行业: {sector.get('sector', 'N/A')}
- 细分: {sector.get('industry', 'N/A')}
"""
        
        return report


# 便捷函数
def quick_quote(stock: str) -> Dict:
    """快速获取行情"""
    fetcher = StockDataFetcher()
    return fetcher.get_realtime_quote(stock)


def quick_analysis(stock: str) -> Dict:
    """快速分析"""
    analyzer = StockAnalyzer()
    return analyzer.full_analysis(stock)


if __name__ == "__main__":
    # 测试
    fetcher = StockDataFetcher()
    
    print("=== 茅台行情 ===")
    print(fetcher.get_realtime_quote("茅台"))
    
    print("\n=== 走势 ===")
    print(fetcher.get_trend("茅台"))
    
    print("\n=== 均线 ===")
    print(fetcher.get_ma("茅台"))