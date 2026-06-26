# TradingView Data API

Access real-time market data from TradingView with our comprehensive REST API and WebSocket support. Get stock quotes, candlestick data, technical analysis, market leaderboards, and financial news for stocks, crypto, forex, futures, bonds, and ETFs. Includes WebSocket support for live data streaming with real-time price updates and quotes.

## Available Endpoints

### 📊 Price Data
Historical and real-time OHLCV (Open, High, Low, Close, Volume) candlestick data for charting and analysis.
- **GET /api/price/{symbol}** - Get OHLCV candlestick data with customizable timeframes (1, 5, 15, 30, 60, 240, D, W, M)
- **POST /api/price/batch** - Fetch candlestick data for multiple symbols in one request (max 10)

### 💹 Real-time Quotes
Live market quotes with current prices, bid/ask spreads, volume, and price changes for real-time trading decisions.
- **GET /api/quote/{symbol}** - Get real-time quote data including price, change, volume, bid/ask
- **POST /api/quote/batch** - Get real-time quotes for multiple symbols in one request (max 10)

### 🔍 Market Search
Search and discover trading instruments across stocks, crypto, forex, and other asset types by keyword or symbol.
- **GET /api/search/market/{query}** - Search for stocks, crypto, forex, and other markets by keyword (supports optional filter and offset parameters)

### 📈 Technical Analysis
Professional technical analysis signals and indicators to identify buy/sell opportunities across multiple timeframes.
- **GET /api/ta/{symbol}** - Get professional technical analysis signals (Buy/Sell/Neutral) across multiple timeframes
- **GET /api/ta/{symbol}/indicators** - Get detailed technical indicators data (RSI, MACD, Stoch, CCI, ADX, moving averages, pivot points, etc.)

### 🔄 Batch API
Efficiently retrieve data for multiple symbols in a single request. Batch Get Price Data for up to 10 symbols to retrieve candlestick data, and Batch Get Quotes for up to 10 symbols to access real-time quotes.
- **POST /api/price/batch** - Fetch candlestick data for multiple symbols in one request (max 10)
- **POST /api/quote/batch** - Get real-time quotes for multiple symbols in one request (max 10)

### 📰 Financial News
Access financial news and market updates filtered by symbol, market type, language, and region to stay informed.
- **GET /api/news** - Get financial news list with optional symbol, language, market type, and market country filtering
- **GET /api/news/bond** - Get bond market news
- **GET /api/news/crypto** - Get cryptocurrency market news
- **GET /api/news/economic** - Get economic news
- **GET /api/news/etf** - Get ETF market news
- **GET /api/news/forex** - Get forex market news
- **GET /api/news/futures** - Get futures market news
- **GET /api/news/index** - Get index market news
- **GET /api/news/stock** - Get stock market news
- **GET /api/news/{newsId}** - Get detailed content of a news article by news ID

**News Parameters:**
- `symbol` (optional) - Filter by symbol (e.g., "HKEX:700", "NASDAQ:AAPL")
- `lang` (optional) - Language code (default: "en", e.g., "en", "zh-Hans", "ja")
- `market` (optional, only for /api/news) - Market type filter (stock, crypto, forex, futures, bond, etf, index, economic)
- `market_country` (optional) - Market country code filter (e.g., "US", "CN")

### 🏆 Market Leaderboards
Discover top performers, gainers, losers, and trending instruments across different asset types and markets.
- **GET /api/leaderboard/stocks** - Get stock leaderboard data (requires `market_code` parameter)
- **GET /api/leaderboard/indices** - Get indices leaderboard data
- **GET /api/leaderboard/crypto** - Get cryptocurrency leaderboard data
- **GET /api/leaderboard/futures** - Get futures leaderboard data
- **GET /api/leaderboard/forex** - Get forex leaderboard data
- **GET /api/leaderboard/bonds** - Get government bonds leaderboard data
- **GET /api/leaderboard/corporate-bonds** - Get corporate bonds leaderboard data
- **GET /api/leaderboard/etfs** - Get ETF/funds leaderboard data
- **GET /api/leaderboard/data** - Get leaderboard data by config ID (legacy endpoint)

**Leaderboard Parameters:**
- `tab` (required) - Tab identifier (e.g., "gainers", "all", "major")
- `market_code` (required for stocks) - Market code (e.g., "america", "china")
- `columnset` (optional) - Column set name (default: "overview")
- `start` (optional) - Pagination start index (default: 0)
- `count` (optional) - Number of results, max 150 (default: 20)
- `lang` (optional) - Language code (default: "en")

### 📋 Metadata
Retrieve API configuration data including available markets, tabs, column sets, supported languages, and exchanges.
- **GET /api/metadata/markets** - Get all available market codes
- **GET /api/metadata/tabs** - Get all available tab configurations (optional `type` filter)
- **GET /api/metadata/columnsets** - Get column set metadata by asset type
- **GET /api/metadata/languages** - Get supported language list
- **GET /api/metadata/exchanges** - Get all available exchanges list

**Major Exchanges:**

The API supports 353+ exchanges across different asset types. Here are some of the major exchanges:

**Stock Exchanges:**

| Exchange | Code | Country/Region | Description |
|----------|------|----------------|-------------|
| NASDAQ | NASDAQ | US | NASDAQ Stock Market |
| NYSE | NYSE | US | New York Stock Exchange |
| AMEX | AMEX | US | NYSE Arca |
| HKEX | HKEX | Hong Kong | Hong Kong Exchange |
| SSE | SSE | China | Shanghai Stock Exchange |
| SZSE | SZSE | China | Shenzhen Stock Exchange |
| TSE | TSE | Japan | Tokyo Stock Exchange |
| LSE | LSE | UK | London Stock Exchange |
| Euronext | EURONEXT | EU | Euronext NV |
| XETR | XETR | Germany | Xetra |
| B3 | BMFBOVESPA | Brazil | Brasil Bolsa Balcao S.A. |
| TSX | TSX | Canada | Toronto Stock Exchange |
| ASX | ASX | Australia | Australian Securities Exchange |
| NSE | NSE | India | National Stock Exchange of India |
| BSE | BSE | India | Bombay Stock Exchange |

**Cryptocurrency Exchanges:**

| Exchange | Code | Description |
|----------|------|-------------|
| Binance | BINANCE | Binance |
| Coinbase | COINBASE | Coinbase |
| Kraken | KRAKEN | Kraken |
| Bitfinex | BITFINEX | Bitfinex |
| OKX | OKX | OKX |
| Bybit | BYBIT | Bybit |
| Gate | GATE | Gate |
| MEXC | MEXC | MEXC |
| Deribit | DERIBIT | Deribit |
| KuCoin | KUCOIN | KuCoin |
| HTX | HTX | HTX (formerly Huobi) |
| Bitget | BITGET | Bitget |
| Binance.US | BINANCEUS | Binance.US |

**Note:** The complete list of all 353+ exchanges can be retrieved using the `/api/metadata/exchanges` endpoint.

### 📅 Calendar Events
Access economic calendar, earnings calendar, dividends calendar, and IPO calendar data for tracking important market events.
- **GET /api/calendar/economic** - Get economic calendar events (supports multiple countries via market_code)
- **GET /api/calendar/earnings** - Get earnings calendar with earnings release dates and forecasts
- **GET /api/calendar/revenue** - Get dividends calendar with dividend ex-dates and payment dates
- **GET /api/calendar/ipo** - Get IPO calendar with IPO offer times and details

**Calendar Parameters:**
- `from` (required) - Start time (Unix timestamp in seconds, e.g., 1769356800)
- `to` (required) - End time (Unix timestamp in seconds, e.g., 1769961599)
- `market` (optional) - Market code(s), comma-separated (e.g., "america,china", default: "america")

**Response Format:**
All calendar endpoints return data in standard JSON format:
```json
{
  "success": true,
  "data": {
    "totalCount": 661,
    "data": [
      {
        "symbol": "NASDAQ:FLWS",
        "rank": 1,
        "earnings_release_date": 1761821100,
        "name": "FLWS",
        "description": "1-800-FLOWERS.COM, Inc.",
        ...
      }
    ]
  },
  "msg": "Success"
}
```

**Examples:**
- `/api/calendar/economic?from=1769356800&to=1769961599&market=america,china` - Get economic events for China and US
- `/api/calendar/earnings?from=1769356800&to=1769961599&market=america,china` - Get earnings calendar for multiple markets
- `/api/calendar/revenue?from=1769356800&to=1769961599&market=china` - Get dividends calendar for China
- `/api/calendar/ipo?from=1769356800&to=1769961599&market=america,china` - Get IPO calendar for multiple markets

### 🖼️ Logo Images
Get TradingView logo images. The logo path should be obtained from currency-logoid, base-currency-logoid, or logoid fields returned by other endpoints. These fields can be retrieved from Quote endpoints (`/api/quote/{symbol}` and `/api/quote/batch`) and Leaderboard endpoints (`/api/leaderboard/*`). If the path does not have an extension, .svg will be automatically added. Use the `big` parameter to get large size versions.

- **GET /logo** - Get TradingView logo images using URL query parameters

**Logo Parameters:**
- `url` (required) - Logo path (e.g., "apple.svg" or "crypto/XTVCMIDLE"). If no extension is provided, .svg will be automatically added
- `big` (optional) - Set to true to get large size version

**Examples:**
- `/logo?url=apple.svg` - Get Apple logo
- `/logo?url=apple&big=true` - Get Apple logo (big version)
- `/logo?url=crypto/XTVCMIDLE&big=true` - Get cryptocurrency logo (big version)

**Logo Path Examples by Category:**

| Category | Example Paths |
|----------|---------------|
| **Exchange Providers** | `provider/binance`, `provider/coinbase`, `provider/kraken`, `provider/bitfinex`, `provider/bybit`, `provider/okx`, `provider/huobi`, `provider/okex`, `provider/bitmex`, `provider/deribit`, `provider/ftx`, `provider/gateio`, `provider/kucoin`, `provider/bitstamp`, `provider/gemini` |
| **Exchange Sources** | `source/NASDAQ`, `source/NYSE`, `source/SSE`, `source/HKEX`, `source/LSE`, `source/TSX`, `source/ASX`, `source/FWB`, `source/EURONEXT`, `source/TSE`, `source/BSE`, `source/NSE`, `source/SGX`, `source/KRX` |
| **Cryptocurrencies** | `crypto/XTVCBTC`, `crypto/XTVCETH`, `crypto/XTVCSOL`, `crypto/XTVCDOGE`, `crypto/XTVCADA`, `crypto/XTVCDOT`, `crypto/XTVCLINK`, `crypto/XTVCMATIC`, `crypto/XTVCAVAX`, `crypto/XTVCLUNA` |
| **Stock Companies** | `apple`, `microsoft`, `alphabet`, `tesla`, `amazon`, `meta-platforms`, `nvidia`, `jpmorgan-chase`, `visa`, `johnson-and-johnson`, `berkshire-hathaway`, `unitedhealth-group`, `mastercard`, `home-depot`, `bank-of-america` |
| **Countries/Regions** | `country/EU`, `country/US`, `country/GB`, `country/JP`, `country/CN`, `country/CA`, `country/AU`, `country/DE`, `country/FR`, `country/IN`, `country/KR`, `country/SG`, `country/HK`, `country/CH`, `country/NL` |

### ⚡ WebSocket Real-time Data
WebSocket endpoint for real-time price updates, quotes, and market data streaming.

**Note:** This section describes the WebSocket API structure for reference. The actual WebSocket endpoints shown use example domains for documentation purposes.


## Key Features

- **Real-time Data**: Live price updates and market information
- **Global Coverage**: Access data from major worldwide exchanges
- **Batch Operations**: Efficiently fetch data for multiple symbols
- **Multiple Timeframes**: Support for various chart intervals
- **Professional Analysis**: Built-in technical analysis indicators
- **Market Leaderboards**: Discover trending stocks and market opportunities through comprehensive leaderboards

## Supported Markets

The API supports 8 different asset types:

- **Stocks**: 68+ markets across North America, Europe, Middle East & Africa, South America, and Asia & Oceania
- **Indices**: Global stock indices including major, regional, and sector indices
- **Cryptocurrency**: All major exchanges and trading pairs
- **Futures**: Commodities, energy, metals, currencies, world indices, and interest rates
- **Forex**: All major, minor, and exotic currency pairs
- **Government Bonds**: Government bonds from global markets
- **Corporate Bonds**: Corporate bonds with various terms and coupon types
- **ETFs/Funds**: Comprehensive ETF and fund coverage worldwide

## Asset Types and Tabs

The following tables show all available asset types, their tabs, and column sets:

### Stocks (25 tabs, 9 column sets)

| Tab ID | Title | Market Code Required |
|--------|-------|---------------------|
| all-stocks | All Stocks | Yes |
| gainers | Top Gainers | Yes |
| losers | Top Losers | Yes |
| large-cap | Large Cap | Yes |
| small-cap | Small Cap | Yes |
| largest-employers | Largest Employers | Yes |
| high-dividend | High Dividend | Yes |
| highest-net-income | Highest Net Income | Yes |
| highest-cash | Most Cash | Yes |
| highest-profit-per-employee | Highest Profit Per Employee | Yes |
| highest-revenue-per-employee | Highest Revenue Per Employee | Yes |
| active | Most Active | Yes |
| unusual-volume | Unusual Volume | Yes |
| most-volatile | Most Volatile | Yes |
| high-beta | High Beta | Yes |
| best-performing | Best Performing | Yes |
| highest-revenue | Highest Revenue | Yes |
| most-expensive | Most Expensive | Yes |
| penny-stocks | Penny Stocks | Yes |
| overbought | Overbought | Yes |
| oversold | Oversold | Yes |
| ath | All-Time High | Yes |
| atl | All-Time Low | Yes |
| 52wk-high | 52 Week High | Yes |
| 52wk-low | 52 Week Low | Yes |

**Column Sets:**

| Column Set ID | Title | Column Count |
|---------------|-------|--------------|
| overview | Overview | 12 |
| performance | Performance | 13 |
| valuation | Valuation | 10 |
| dividends | Dividends | 9 |
| profitability | Profitability | 12 |
| income_statement | Income Statement | 10 |
| balance_sheet | Balance Sheet | 10 |
| cash_flow | Cash Flow | 9 |
| technical | Technical | 14 |

### Indices (11 tabs, 3 column sets)

| Tab ID | Title | Market Code Required |
|--------|-------|---------------------|
| all | All | No |
| major | Major | No |
| us | US | No |
| snp | S&P | No |
| currency | Currency | No |
| americas | Americas | No |
| europe | Europe | No |
| asia | Asia | No |
| pacific | Pacific | No |
| middle-east | Middle East | No |
| africa | Africa | No |

**Column Sets:**

| Column Set ID | Title |
|---------------|-------|
| overview | Overview |
| performance | Performance |
| technical | Technical |

### Cryptocurrencies (20 tabs, 3 column sets)

| Tab ID | Title | Market Code Required |
|--------|-------|---------------------|
| all | All | No |
| highest-total-value-locked | Highest Total Value Locked | No |
| defi | Defi | No |
| gainers | Gainers | No |
| losers | Losers | No |
| large-cap | Large Cap | No |
| small-cap | Small Cap | No |
| most-traded | Most Traded | No |
| most-addresses-with-balance | Most Addresses With Balance | No |
| most-addresses-active | Most Addresses Active | No |
| most-transactions | Most Transactions | No |
| highest-transaction-volume | Highest Transaction Volume | No |
| lowest-supply | Lowest Supply | No |
| highest-supply | Highest Supply | No |
| most-expensive | Most Expensive | No |
| most-volatile | Most Volatile | No |
| all-time-high | All-Time High | No |
| all-time-low | All-Time Low | No |
| 52-week-high | 52 Week High | No |
| 52-week-low | 52 Week Low | No |

**Column Sets:**

| Column Set ID | Title |
|---------------|-------|
| overview | Overview |
| performance | Performance |
| technical | Technical |

### Futures (7 tabs, 2 column sets)

| Tab ID | Title | Market Code Required |
|--------|-------|---------------------|
| all | All | No |
| agricultural | Agricultural | No |
| energy | Energy | No |
| currencies | Currencies | No |
| metals | Metals | No |
| world-indices | World Indices | No |
| interest-rates | Interest Rates | No |

**Column Sets:**

| Column Set ID | Title |
|---------------|-------|
| overview | Overview |
| performance | Performance |

### Forex (10 tabs, 3 column sets)

| Tab ID | Title | Market Code Required |
|--------|-------|---------------------|
| all | All | No |
| major | Major | No |
| minor | Minor | No |
| exotic | Exotic | No |
| americas | Americas | No |
| europe | Europe | No |
| asia | Asia | No |
| pacific | Pacific | No |
| middle-east | Middle East | No |
| africa | Africa | No |

**Column Sets:**

| Column Set ID | Title |
|---------------|-------|
| overview | Overview |
| performance | Performance |
| technical | Technical |

### Government Bonds (17 tabs, 2 column sets)

| Tab ID | Title | Market Code Required |
|--------|-------|---------------------|
| all | All | No |
| all-10-year | All 10 Year | No |
| major | Major | No |
| americas | Americas | No |
| europe | Europe | No |
| asia | Asia | No |
| pacific | Pacific | No |
| middle-east | Middle East | No |
| africa | Africa | No |
| usa | USA | No |
| uk | UK | No |
| eu | EU | No |
| germany | Germany | No |
| france | France | No |
| china | China | No |
| india | India | No |
| japan | Japan | No |

**Column Sets:**

| Column Set ID | Title |
|---------------|-------|
| overview | Overview |
| performance | Performance |

### Corporate Bonds (6 tabs, 1 column set)

| Tab ID | Title | Market Code Required |
|--------|-------|---------------------|
| highest-yield | Highest Yield | No |
| long-term | Long Term | No |
| short-term | Short Term | No |
| floating-rate | Floating Rate | No |
| fixed-coupon | Fixed Coupon | No |
| zero-coupon | Zero Coupon | No |

**Column Sets:**

| Column Set ID | Title |
|---------------|-------|
| overview | Overview |

### ETFs/Funds (40 tabs, 3 column sets)

| Tab ID | Title | Market Code Required |
|--------|-------|---------------------|
| largest | Largest | No |
| highest-aum-growth | Highest AUM Growth | No |
| highest-returns | Highest Returns | No |
| biggest-losers | Biggest Losers | No |
| equity | Equity | No |
| bitcoin | Bitcoin | No |
| ethereum | Ethereum | No |
| gold | Gold | No |
| fixed-income | Fixed Income | No |
| real-estate | Real Estate | No |
| total-market | Total Market | No |
| commodities | Commodities | No |
| asset-allocation | Asset Allocation | No |
| inverse-etfs | Inverse ETFs | No |
| leveraged-etfs | Leveraged ETFs | No |
| most-traded | Most Traded | No |
| largest-inflows | Largest Inflows | No |
| largest-outflows | Largest Outflows | No |
| highest-discount | Highest Discount | No |
| highest-premium | Highest Premium | No |
| highest-yield | Highest Yield | No |
| dividend | Dividend | No |
| monthly-distributions | Monthly Distributions | No |
| highest-diversification | Highest Diversification | No |
| actively-managed | Actively Managed | No |
| sector-etfs | Sector ETFs | No |
| highest-beta | Highest Beta | No |
| lowest-beta | Lowest Beta | No |
| negative-beta | Negative Beta | No |
| highest-expense-ratio | Highest Expense Ratio | No |
| all-time-high | All-Time High | No |
| all-time-low | All-Time Low | No |
| 52-week-high | 52 Week High | No |
| 52-week-low | 52 Week Low | No |
| usa | USA | No |
| canada | Canada | No |
| uk | UK | No |
| germany | Germany | No |
| japan | Japan | No |
| australia | Australia | No |

**Column Sets:**

| Column Set ID | Title |
|---------------|-------|
| overview | Overview |
| performance | Performance |
| technical | Technical |

## Market Codes

Market codes are required for stock leaderboard queries. Available market codes:

| Region | Country | Market Code |
|--------|---------|-------------|
| North America | United States | america |
| North America | Canada | canada |
| Europe | Austria | austria |
| Europe | Belgium | belgium |
| Europe | Switzerland | switzerland |
| Europe | Cyprus | cyprus |
| Europe | Czech Republic | czech |
| Europe | Germany | germany |
| Europe | Denmark | denmark |
| Europe | Estonia | estonia |
| Europe | Spain | spain |
| Europe | Finland | finland |
| Europe | France | france |
| Europe | Greece | greece |
| Europe | Hungary | hungary |
| Europe | Ireland | ireland |
| Europe | Iceland | iceland |
| Europe | Italy | italy |
| Europe | Lithuania | lithuania |
| Europe | Latvia | latvia |
| Europe | Luxembourg | luxembourg |
| Europe | Netherlands | netherlands |
| Europe | Norway | norway |
| Europe | Poland | poland |
| Europe | Portugal | portugal |
| Europe | Serbia | serbia |
| Europe | Russia | russia |
| Europe | Romania | romania |
| Europe | Sweden | sweden |
| Europe | Slovakia | slovakia |
| Europe | Turkey | turkey |
| Europe | United Kingdom | uk |
| Middle East & Africa | United Arab Emirates | uae |
| Middle East & Africa | Bahrain | bahrain |
| Middle East & Africa | Egypt | egypt |
| Middle East & Africa | Israel | israel |
| Middle East & Africa | Kenya | kenya |
| Middle East & Africa | Kuwait | kuwait |
| Middle East & Africa | Morocco | morocco |
| Middle East & Africa | Nigeria | nigeria |
| Middle East & Africa | Qatar | qatar |
| Middle East & Africa | Saudi Arabia | saudi-arabia |
| Middle East & Africa | Tunisia | tunisia |
| Middle East & Africa | South Africa | south-africa |
| South America | Argentina | argentina |
| South America | Brazil | brazil |
| South America | Chile | chile |
| South America | Colombia | colombia |
| South America | Mexico | mexico |
| South America | Peru | peru |
| South America | Venezuela | venezuela |
| Asia & Oceania | Australia | australia |
| Asia & Oceania | Bangladesh | bangladesh |
| Asia & Oceania | China | china |
| Asia & Oceania | Hong Kong | hong-kong |
| Asia & Oceania | Indonesia | indonesia |
| Asia & Oceania | India | india |
| Asia & Oceania | Japan | japan |
| Asia & Oceania | South Korea | korea |
| Asia & Oceania | Sri Lanka | sri-lanka |
| Asia & Oceania | Malaysia | malaysia |
| Asia & Oceania | New Zealand | new-zealand |
| Asia & Oceania | Philippines | philippines |
| Asia & Oceania | Pakistan | pakistan |
| Asia & Oceania | Singapore | singapore |
| Asia & Oceania | Thailand | thailand |
| Asia & Oceania | Taiwan | taiwan |
| Asia & Oceania | Vietnam | vietnam |

## Supported Languages

The API supports the following languages (use `lang` parameter):

| Code | Language |
|------|----------|
| en | English |
| zh | 简体中文 |
| de | Deutsch |
| fr | Français |
| es | Español |
| it | Italiano |
| pl | Polski |
| tr | Türkçe |
| ru | Русский |
| pt | Português |
| id | Bahasa Indonesia |
| ms | Bahasa Melayu |
| th | ภาษาไทย |
| vi | Tiếng Việt |
| ja | 日本語 |
| ko | 한국어 |
| zh_TW | 繁體中文 |
| ar | العربية |
| he | עברית |

## Usage Examples

### Get Stock Leaderboard
```bash
# Get top gainers for US stocks
GET /api/leaderboard/stocks?tab=gainers&market_code=america&columnset=overview&count=20
```

### Get Cryptocurrency Leaderboard
```bash
# Get all cryptocurrencies
GET /api/leaderboard/crypto?tab=all&columnset=overview&count=50
```

### Get News
```bash
# Get stock news for a specific symbol
GET /api/news/stock?symbol=HKEX:700&lang=zh-Hans&market_country=US

# Get cryptocurrency news
GET /api/news/crypto?lang=en

# Get general news with market filter
GET /api/news?market=stock&market_country=US&lang=en

# Get news detail by ID
GET /api/news/tag:reuters.com,2025:newsml_L1N3XK042:0?lang=en
```

### Get Metadata
```bash
# Get all tabs for crypto
GET /api/metadata/tabs?type=crypto

# Get all available markets
GET /api/metadata/markets

# Get columnsets by asset type
GET /api/metadata/columnsets

# Get all available exchanges
GET /api/metadata/exchanges
```


Start building with TradingView data today!
