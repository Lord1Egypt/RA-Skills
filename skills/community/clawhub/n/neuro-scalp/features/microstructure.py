import numpy as np
import pandas as pd

class FeatureEngine:
    def __init__(self, window_size=50):
        self.window_size = window_size
        self.prices = []
        self.volumes = []
    
    def update(self, tick_data):
        self.prices.append(tick_data['last_price'])
        # Maintain rolling window
        if len(self.prices) > self.window_size:
            self.prices.pop(0)
            
    def get_features(self, orderbook_snapshot):
        """
        Generates scalping features:
        1. Order Book Imbalance (OBI)
        2. Microprice
        """
        best_bid = orderbook_snapshot['bid']
        best_ask = orderbook_snapshot['ask']
        bid_vol = orderbook_snapshot['bid_vol']
        ask_vol = orderbook_snapshot['ask_vol']

        # Feature 1: Order Book Imbalance (-1 to 1)
        # Positive = Buying Pressure, Negative = Selling Pressure
        obi = (bid_vol - ask_vol) / (bid_vol + ask_vol + 1e-9)

        # Feature 2: Microprice (Volume-weighted mid price)
        microprice = (best_bid * ask_vol + best_ask * bid_vol) / (bid_vol + ask_vol + 1e-9)
        
        # Feature 3: Volatility (Standard Deviation of last X ticks)
        volatility = np.std(self.prices) if len(self.prices) > 10 else 0

        return np.array([obi, microprice, volatility])