import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WALLET_ADDRESS = os.getenv("HYPERLIQUID_WALLET_ADDRESS")
    PRIVATE_KEY = os.getenv("HYPERLIQUID_PRIVATE_KEY")
    ASSET = "BTC"
    COIN = "BTC-USDC"
    MAX_LEVERAGE = 40
    BASE_POSITION_USD = 2000
    MAX_POSITION_USD = 10000
    MAX_DAILY_LOSS_USD = 500
    MAX_TRADES_PER_DAY = 5
    MIN_USDC_BALANCE = 20
    MAINNET_URL = "https://api.hyperliquid.xyz"