# skills/hyperliquid-btc-auto-trader/strategies/confluence.py
import numpy as np

class ConfluenceDetector:
    def find_confluence(self, vwap_data, current_price):
        """Group VWAPs within 0.5% into confluence zones"""
        if not vwap_data:
            return []
        
        prices = np.array([v["price"] for v in vwap_data])
        sorted_idx = np.argsort(prices)
        sorted_prices = prices[sorted_idx]
        
        zones = []
        current_zone = [sorted_prices[0]]
        current_strength = vwap_data[sorted_idx[0]]["confidence"]
        
        for i in range(1, len(sorted_prices)):
            if (sorted_prices[i] / current_zone[-1] - 1) <= 0.005:  # within 0.5%
                current_zone.append(sorted_prices[i])
                current_strength += vwap_data[sorted_idx[i]]["confidence"]
            else:
                zones.append({
                    "price": float(np.mean(current_zone)),
                    "strength": float(current_strength),
                    "type": "support" if current_price > np.mean(current_zone) * 1.02 else "resistance"
                })
                current_zone = [sorted_prices[i]]
                current_strength = vwap_data[sorted_idx[i]]["confidence"]
        
        # Add last zone
        zones.append({
            "price": float(np.mean(current_zone)),
            "strength": float(current_strength),
            "type": "support" if current_price > np.mean(current_zone) * 1.02 else "resistance"
        })
        
        return [z for z in zones if z["strength"] >= 2.0]  # only strong zones

    def get_confluence_adjustment(self, zones):
        """Return confluence adjustment to signal"""
        adj = 0
        for zone in zones:
            if zone["type"] == "support":
                adj += 30
            else:
                adj -= 30
        return adj
        