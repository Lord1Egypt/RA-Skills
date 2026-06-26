# skills/hyperliquid-btc-auto-trader/strategies/volume_profile.py
import pandas as pd
import numpy as np

class VolumeProfileAnalyzer:
    def get_volume_anchors(self, df: pd.DataFrame):
        """Build 50-bin volume profile and return top 3 HVNs"""
        if len(df) < 50:
            return []
        
        price_min = df["low"].min()
        price_max = df["high"].max()
        bins = np.linspace(price_min, price_max, 51)
        
        volume_per_bin = np.zeros(50)
        for i in range(len(df)):
            idx = np.digitize(df["close"].iloc[i], bins) - 1
            if 0 <= idx < 50:
                volume_per_bin[idx] += df["volume"].iloc[i]
        
        total_volume = volume_per_bin.sum()
        if total_volume == 0:
            return []
        
        top_indices = np.argsort(volume_per_bin)[-3:]
        anchors = []
        for idx in top_indices:
            price = (bins[idx] + bins[idx + 1]) / 2
            sig = min(1.0, volume_per_bin[idx] / total_volume * 10)
            anchors.append({
                "type": "volume",
                "price": float(price),
                "significance": float(sig)
            })
        return anchors