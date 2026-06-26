# skills/hyperliquid-btc-auto-trader/strategies/market_regime.py
import pandas as pd
import pandas_ta as ta
import numpy as np
from hyperliquid.info import Info
from config import Config

class MarketRegimeDetector:
    def __init__(self, info: Info):
        self.info = info

    def detect_regime(self, df: pd.DataFrame):
        """Detects market regime using ADX, ATR%, and SMAs"""
        # ADX (14-period)
        df["adx"] = ta.adx(df["high"], df["low"], df["close"], length=14)["ADX_14"]
        
        # ATR % of price
        df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)
        df["atr_pct"] = (df["atr"] / df["close"]) * 100
        
        # SMAs
        df["sma50"] = df["close"].rolling(50).mean()
        df["sma200"] = df["close"].rolling(200).mean()
        
        current_adx = df["adx"].iloc[-1]
        current_atr_pct = df["atr_pct"].iloc[-1]
        current_price = df["close"].iloc[-1]
        sma50 = df["sma50"].iloc[-1]
        
        if np.isnan(current_adx):
            return "transition"
        
        if current_adx > 30 and current_price > sma50:
            return "trending_bull"
        elif current_adx > 30 and current_price < sma50:
            return "trending_bear"
        elif current_adx < 20:
            return "ranging"
        elif current_atr_pct > 5:
            return "volatile"
        return "transition"

    def get_trend_start_anchor(self, df: pd.DataFrame):
        """Finds the candle where ADX crossed above 25"""
        if len(df) < 50:
            return None
        adx_series = ta.adx(df["high"], df["low"], df["close"], length=14)["ADX_14"]
        cross = adx_series > 25
        if cross.any():
            cross_idx = cross[cross].index[-1]
            return {
                "type": "trend_start",
                "price": float(df.loc[cross_idx]["close"]),
                "significance": 0.8
            }
        return None