from dataclasses import dataclass
import os
from pathlib import Path

from errors import ConfigError


WORKSPACE = Path(__file__).resolve().parents[3]
SECRETS_FILES = [
    WORKSPACE / '.secrets' / 'noah-trade.env',
    WORKSPACE / '.secrets' / 'noah-market.env',
    Path.home() / '.openclaw' / '.secrets' / 'noah-market.env',
    Path.home() / '.openclaw' / '.secrets' / 'noah-trade.env',
]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ[key.strip()] = value.strip()


for _env_file in SECRETS_FILES:
    load_env_file(_env_file)


@dataclass
class TradeConfig:
    base_url: str
    token: str
    env: str = "test"
    read_only: bool = True
    timeout_seconds: int = 15


def load_trade_config() -> TradeConfig:
    base_url = os.getenv("NOAH_TRADE_API_BASE_URL", "https://stock-open-api.noahgroup.com").strip()
    token = os.getenv("NOAH_MARKET_APIKEY", "").strip() or os.getenv("NOAH_MARKET_TOKEN", "").strip()
    env = os.getenv("NOAH_TRADE_ENV", "test").strip() or "test"
    read_only = os.getenv("NOAH_TRADE_READ_ONLY", "true").lower() != "false"
    timeout_seconds = int(os.getenv("NOAH_TRADE_TIMEOUT", "15"))

    if not base_url:
        raise ConfigError("NOAH_TRADE_API_BASE_URL is missing", hint="请先配置交易 API Base URL")
    if not token:
        raise ConfigError("NOAH_MARKET_APIKEY is missing", hint="请先配置统一 Bearer token（trade 与 market 共用）")

    return TradeConfig(
        base_url=base_url.rstrip("/"),
        token=token,
        env=env,
        read_only=read_only,
        timeout_seconds=timeout_seconds,
    )
