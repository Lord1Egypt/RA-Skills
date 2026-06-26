from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from config import Config
import time
from datetime import datetime

class SafetyManager:
    def __init__(self, exchange: Exchange, info: Info):
        self.exchange = exchange
        self.info = info
        self.daily_trades = 0
        self.daily_loss = 0.0
        self.last_trade_time = 0
        self.consecutive_losses = 0

    def can_trade(self):
        if self.daily_trades >= Config.MAX_TRADES_PER_DAY:
            return False
        if self.daily_loss >= Config.MAX_DAILY_LOSS_USD:
            return False
        balance = self.get_usdc_balance()
        if balance < Config.MIN_USDC_BALANCE:
            return False
        if time.time() - self.last_trade_time < 300:  # 5 min cooldown
            return False
        return True

    def get_usdc_balance(self):
        state = self.info.user_state(Config.WALLET_ADDRESS)
        return float(state["withdrawable"])

    def execute_trade_if_valid(self, signal):
        if abs(signal["score"]) < 60:
            return

        is_buy = signal["direction"] == "BUY"
        size_usd = Config.BASE_POSITION_USD * (1.5 if signal["score"] >= 80 else 1.2 if signal["score"] >= 60 else 1.0)
        size_usd = min(size_usd, Config.MAX_POSITION_USD)
        sz = round(size_usd / signal["price"], 4)  # BTC quantity

        # Place market order
        order = self.exchange.market_open(Config.ASSET, is_buy, sz, slippage=0.01)
        print(f"✅ TRADE EXECUTED | Score: {signal['score']} | {signal['direction']} {sz} BTC")

        self.daily_trades += 1
        self.last_trade_time = time.time()