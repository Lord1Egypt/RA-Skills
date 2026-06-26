COUNTRY_SCOPES = {
    "US": {
        "aliases": ["US", "USA", "UNITED STATES", "AMERICA"],
        "snapshot_symbols": [
            {"label": "S&P 500", "symbol": "SPY", "kind": "etf"},
            {"label": "Nasdaq 100", "symbol": "QQQ", "kind": "etf"},
            {"label": "Dow Jones", "symbol": "DIA", "kind": "etf"},
            {"label": "Russell 2000", "symbol": "IWM", "kind": "etf"},
            {"label": "Volatility Index", "symbol": "^VIX", "kind": "volatility"},
        ],
        "news_symbols": [
            {"label": "S&P 500", "symbol": "SPY", "kind": "etf"},
            {"label": "Nasdaq 100", "symbol": "QQQ", "kind": "etf"},
            {"label": "Dow Jones", "symbol": "DIA", "kind": "etf"},
            {"label": "Russell 2000", "symbol": "IWM", "kind": "etf"},
        ],
    },
    "UK": {
        "aliases": ["UK", "UNITED KINGDOM", "GB", "GBR", "BRITAIN", "FTSE"],
        "snapshot_symbols": [
            {"label": "FTSE 100", "symbol": "^FTSE", "kind": "index"},
            {
                "label": "iShares MSCI United Kingdom ETF",
                "symbol": "EWU",
                "kind": "etf",
            },
        ],
        "news_symbols": [
            {"label": "FTSE 100", "symbol": "^FTSE", "kind": "index"},
            {
                "label": "iShares MSCI United Kingdom ETF",
                "symbol": "EWU",
                "kind": "etf",
            },
        ],
    },
    "GERMANY": {
        "aliases": ["GERMANY", "DE", "DEU", "DAX"],
        "snapshot_symbols": [
            {"label": "DAX", "symbol": "^GDAXI", "kind": "index"},
            {"label": "iShares MSCI Germany ETF", "symbol": "EWG", "kind": "etf"},
        ],
        "news_symbols": [
            {"label": "DAX", "symbol": "^GDAXI", "kind": "index"},
            {"label": "iShares MSCI Germany ETF", "symbol": "EWG", "kind": "etf"},
        ],
    },
    "NETHERLANDS": {
        "aliases": ["NETHERLANDS", "NL", "NLD", "DUTCH", "AEX", "AMSTERDAM"],
        "snapshot_symbols": [
            {"label": "AEX", "symbol": "^AEX", "kind": "index"},
            {"label": "iShares MSCI Netherlands ETF", "symbol": "EWN", "kind": "etf"},
        ],
        "news_symbols": [
            {"label": "AEX", "symbol": "^AEX", "kind": "index"},
            {"label": "iShares MSCI Netherlands ETF", "symbol": "EWN", "kind": "etf"},
            {"label": "Euronext 100", "symbol": "^N100", "kind": "index"},
        ],
    },
    "JAPAN": {
        "aliases": ["JAPAN", "JP", "JPN", "NIKKEI", "TOKYO"],
        "snapshot_symbols": [
            {"label": "Nikkei 225", "symbol": "^N225", "kind": "index"},
            {"label": "iShares MSCI Japan ETF", "symbol": "EWJ", "kind": "etf"},
        ],
        "news_symbols": [
            {"label": "Nikkei 225", "symbol": "^N225", "kind": "index"},
            {"label": "iShares MSCI Japan ETF", "symbol": "EWJ", "kind": "etf"},
        ],
    },
    "SOUTH_KOREA": {
        "aliases": ["SOUTH KOREA", "KOREA", "KR", "KOR", "KOSPI", "SEOUL"],
        "snapshot_symbols": [
            {"label": "KOSPI", "symbol": "^KS11", "kind": "index"},
            {"label": "iShares MSCI South Korea ETF", "symbol": "EWY", "kind": "etf"},
        ],
        "news_symbols": [
            {"label": "KOSPI", "symbol": "^KS11", "kind": "index"},
            {"label": "iShares MSCI South Korea ETF", "symbol": "EWY", "kind": "etf"},
        ],
    },
}

REGION_SCOPES = {
    "EUROPE": {
        "aliases": ["EUROPE", "EU", "EUR", "EUROZONE", "EURO AREA"],
        "members": ["UK", "GERMANY", "NETHERLANDS"],
    },
    "ASIA": {
        "aliases": ["ASIA", "APAC", "ASIA PACIFIC"],
        "members": ["JAPAN", "SOUTH_KOREA"],
    },
    "GLOBAL": {
        "aliases": ["GLOBAL", "WORLD", "INTERNATIONAL"],
        "members": ["US", "UK", "GERMANY", "NETHERLANDS", "JAPAN", "SOUTH_KOREA"],
    },
}

SUFFIX_SCOPE_MAP = {
    ".DE": "GERMANY",
    ".L": "UK",
    ".AS": "NETHERLANDS",
    ".T": "JAPAN",
    ".KS": "SOUTH_KOREA",
    ".KQ": "SOUTH_KOREA",
}

THEME_KEYWORDS = {
    "Central banks and rates": [
        "fed",
        "rates",
        "yield",
        "treasury",
        "ecb",
        "boe",
        "boj",
        "bank of japan",
        "gilt",
        "bond",
    ],
    "Inflation and economy": [
        "inflation",
        "cpi",
        "ppi",
        "payroll",
        "jobs",
        "gdp",
        "economy",
        "recession",
        "consumer",
    ],
    "Technology and semis": [
        "ai",
        "tech",
        "software",
        "semiconductor",
        "chip",
        "megacap",
        "nasdaq",
        "nikkei",
    ],
    "Energy and commodities": ["oil", "crude", "energy", "gas", "commodity"],
    "Policy and geopolitics": [
        "tariff",
        "war",
        "china",
        "russia",
        "middle east",
        "policy",
        "geopolitical",
    ],
}

BROAD_MARKET_KEYWORDS = [
    "market",
    "markets",
    "stocks",
    "equities",
    "wall street",
    "s&p",
    "nasdaq",
    "dow",
    "russell",
    "vix",
    "ftse",
    "dax",
    "aex",
    "nikkei",
    "kospi",
    "europe",
    "european",
    "asia",
    "asian",
    "global",
    "fed",
    "ecb",
    "boe",
    "boj",
    "rates",
    "yield",
    "treasury",
    "gilt",
    "economy",
    "inflation",
    "cpi",
    "jobs",
    "payroll",
    "recession",
    "tariff",
    "oil",
    "volatility",
    "sector",
]

VALID_SCOPES = [
    "GLOBAL",
    "EUROPE",
    "ASIA",
    "US",
    "UK",
    "GERMANY",
    "NETHERLANDS",
    "JAPAN",
    "SOUTH_KOREA",
]

MAX_HEADLINES = 8
RAW_NEWS_FETCH_LIMIT = 12
