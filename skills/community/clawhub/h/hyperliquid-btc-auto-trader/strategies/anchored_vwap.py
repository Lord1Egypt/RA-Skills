import pandas as pd
import numpy as np
import pandas_ta as ta
from datetime import datetime
from hyperliquid.info import Info
from .market_regime import MarketRegimeDetector
from .volume_profile import VolumeProfileAnalyzer
from .swing_detector import SwingDetector
from .confluence import ConfluenceDetector
from config import Config

class AnchoredVWAPStrategy:
    def __init__(self, info: Info):
        self.info = info
        self.regime_detector = MarketRegimeDetector(info)
        self.volume_analyzer = VolumeProfileAnalyzer()
        self.swing_detector = SwingDetector()
        self.confluence_detector = ConfluenceDetector()
        self.anchor_performance = {k: {"win_rate": 0.5, "avg_pnl": 0} for k in ["volume", "swing", "daily", "weekly", "trend_start"]}
        self.last_signal = 0
        self.last_signal_time = datetime.now()

    def get_candles(self, limit=500):
        candles = self.info.candles(Config.COIN, "1m", limit)
        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df.set_index("timestamp").astype(float)
        return df

    def calculate_signal(self):
        df = self.get_candles()
        current_price = float(self.info.mid_price(Config.COIN)["midPx"])

        regime = self.regime_detector.detect_regime(df)
        volume_anchors = self.volume_analyzer.get_volume_anchors(df)
        swing_anchors = self.swing_detector.get_swing_anchors(df)
        daily_anchors = self._get_daily_anchors()
        weekly_anchors = self._get_weekly_anchors()
        trend_start = self.regime_detector.get_trend_start_anchor(df)

        all_anchors = volume_anchors + swing_anchors + daily_anchors + weekly_anchors
        if trend_start:
            all_anchors.append(trend_start)

        vwap_data = self._compute_all_vwaps(df, all_anchors)
        confluence_zones = self.confluence_detector.find_confluence(vwap_data, current_price)

        weighted_dev = self._calculate_weighted_deviation(vwap_data, current_price)
        confluence_adj = self.confluence_detector.get_confluence_adjustment(confluence_zones)
        regime_adj = 10 if regime == "trending_bull" else -10 if regime == "trending_bear" else 0

        imbalance = self._get_orderbook_imbalance()
        flow_adj = self._get_trade_flow_adjustment()
        candle_adj = self._detect_candle_patterns(df)

        base_score = weighted_dev * 1000
        final_score = base_score + confluence_adj + regime_adj + (imbalance * 25) + (flow_adj * 20) + (candle_adj * 15)
        final_score = np.clip(final_score, -100, 100)

        self.last_signal = final_score
        self.last_signal_time = datetime.now()

        return {
            "score": round(final_score, 2),
            "regime": regime,
            "direction": "BUY" if final_score >= 60 else "SELL" if final_score <= -60 else "NEUTRAL",
            "confidence": abs(final_score),
            "price": current_price,
            "confluence_zones": confluence_zones
        }

    def _compute_all_vwaps(self, df, anchors):
        vwaps = []
        for anchor in anchors:
            mask = df.index >= df.index[0]  # full history for simplicity
            sub = df[mask].copy()
            sub["typical"] = (sub["high"] + sub["low"] + sub["close"]) / 3
            sub["age"] = range(len(sub))
            decay = 0.95 ** sub["age"]
            weighted_pv = (sub["typical"] * sub["volume"] * decay).cumsum()
            weighted_vol = (sub["volume"] * decay).cumsum()
            vwap_price = (weighted_pv / weighted_vol).iloc[-1]
            confidence = self._vwap_confidence(anchor["significance"], len(sub))
            vwaps.append({"price": vwap_price, "confidence": confidence, "type": anchor["type"]})
        return vwaps

    def _vwap_confidence(self, sig, candles):
        recency = max(0, 1 - (candles / (30 * 1440)))
        return (recency * 0.4) + (sig * 0.4) + (min(1.0, candles / 1_000_000) * 0.2)

    def _calculate_weighted_deviation(self, vwaps, current_price):
        if not vwaps:
            return 0
        total_w = sum(v["confidence"] for v in vwaps)
        return sum((current_price - v["price"]) * v["confidence"] for v in vwaps) / total_w

    def _get_orderbook_imbalance(self):
        book = self.info.l2_book(Config.COIN)
        bids_vol = sum(float(level[1]) for level in book.get("bids", [])[:20])
        asks_vol = sum(float(level[1]) for level in book.get("asks", [])[:20])
        return (bids_vol - asks_vol) / (bids_vol + asks_vol) if (bids_vol + asks_vol) > 0 else 0

    def _get_trade_flow_adjustment(self):
        trades = self.info.recent_trades(Config.COIN, 50)
        buy_vol = sum(float(t["px"]) * float(t["sz"]) for t in trades if t["side"] == "B")
        sell_vol = sum(float(t["px"]) * float(t["sz"]) for t in trades if t["side"] == "S")
        total = buy_vol + sell_vol
        return (buy_vol - sell_vol) / total if total > 0 else 0

    def _detect_candle_patterns(self, df):
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        body = abs(latest["close"] - latest["open"])
        lower_wick = min(latest["open"], latest["close"]) - latest["low"]
        vol_surge = latest["volume"] > prev["volume"] * 1.8
        hammer = lower_wick > body * 2
        return 15 if hammer or vol_surge else 0

    def _get_daily_anchors(self):
        # Simplified daily open/high/low from last candle
        return [{"type": "daily", "price": 65000, "significance": 0.55}]  # Replace with real daily fetch if needed

    def _get_weekly_anchors(self):
        return [{"type": "weekly", "price": 64000, "significance": 0.7}]
