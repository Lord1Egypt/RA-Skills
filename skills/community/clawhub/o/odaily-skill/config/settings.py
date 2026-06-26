import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    """Skill 配置 - 从环境变量读取，全部有默认值可直接运行"""

    # Odaily
    ODAILY_BASE_URL: str = "https://www.odaily.news"
    ODAILY_API_FLASH: str = "https://web-api.odaily.news/newsflash/page"
    ODAILY_API_POST: str = "https://web-api.odaily.news/post/page"

    # Market Data
    COINGECKO_API_URL: str = "https://api.coingecko.com/api/v3"
    COINGECKO_API_KEY: str = field(
        default_factory=lambda: os.environ.get("COINGECKO_API_KEY", "")
    )
    BINANCE_API_URL: str = "https://data-api.binance.vision/api/v3"
    BINANCE_FUTURES_URL: str = "https://fapi.binance.com/fapi/v1"

    # Polymarket
    POLYMARKET_DATA_API: str = "https://data-api.polymarket.com"

    # Supabase (可选，用于巨鲸数据持久化)
    SUPABASE_URL: str = field(
        default_factory=lambda: os.environ.get("SUPABASE_URL", "")
    )
    SUPABASE_KEY: str = field(
        default_factory=lambda: os.environ.get("SUPABASE_KEY", "")
    )

    # Fear & Greed
    FEAR_GREED_API: str = "https://api.alternative.me/fng/"

    # 通用
    REQUEST_TIMEOUT: int = 30
    USER_AGENT: str = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    TRACKED_TOKENS: list = field(default_factory=lambda: [
        "BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE",
        "AVAX", "DOT", "LINK", "UNI", "AAVE", "ARB", "OP",
        "APT", "SUI", "NEAR", "TON", "PEPE", "WIF",
    ])


settings = Settings()
