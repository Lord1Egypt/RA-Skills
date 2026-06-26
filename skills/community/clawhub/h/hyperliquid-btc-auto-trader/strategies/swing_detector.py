# skills/hyperliquid-btc-auto-trader/strategies/swing_detector.py
import pandas as pd

class SwingDetector:
    def get_swing_anchors(self, df: pd.DataFrame):
        """Detect swing highs/lows with volume confirmation"""
        if len(df) < 11:
            return []
        
        swings = []
        avg_vol = df["volume"].rolling(20).mean()
        
        for i in range(5, len(df) - 5):
            # Swing high
            if df["high"].iloc[i] == df["high"].iloc[i-5:i+6].max() and \
               df["volume"].iloc[i] > avg_vol.iloc[i] * 1.5:
                sig = min(1.0, df["volume"].iloc[i] / avg_vol.iloc[i] / 3)
                swings.append({
                    "type": "swing",
                    "price": float(df["high"].iloc[i]),
                    "significance": float(sig)
                })
            # Swing low
            elif df["low"].iloc[i] == df["low"].iloc[i-5:i+6].min() and \
                 df["volume"].iloc[i] > avg_vol.iloc[i] * 1.5:
                sig = min(1.0, df["volume"].iloc[i] / avg_vol.iloc[i] / 3)
                swings.append({
                    "type": "swing",
                    "price": float(df["low"].iloc[i]),
                    "significance": float(sig)
                })
        
        # Return top 5 most recent significant swings
        return swings[-5:]