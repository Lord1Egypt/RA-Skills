import time
import logging
from config import Config
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from strategies.anchored_vwap import AnchoredVWAPStrategy
from safety.limits import SafetyManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HyperliquidBTCAutoTrader:
    def __init__(self):
        self.info = Info(base_url=Config.MAINNET_URL, skip_ws=True)
        self.exchange = Exchange(Config.WALLET_ADDRESS, Config.PRIVATE_KEY, base_url=Config.MAINNET_URL)
        self.strategy = AnchoredVWAPStrategy(self.info)
        self.safety = SafetyManager(self.exchange, self.info)
        self.running = True
        logging.info("🚀 Hyperliquid BTC-USDC Autonomous Trader STARTED (Mainnet)")

    def run(self):
        while self.running:
            if not self.safety.can_trade():
                time.sleep(60)
                continue

            signal = self.strategy.calculate_signal()
            self.safety.execute_trade_if_valid(signal)

            time.sleep(60)  # 1-minute cycle

if __name__ == "__main__":
    trader = HyperliquidBTCAutoTrader()
    trader.run()