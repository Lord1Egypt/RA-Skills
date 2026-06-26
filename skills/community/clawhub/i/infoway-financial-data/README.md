# Infoway MCP Server

MCP (Model Context Protocol) Server that gives Claude and other AI assistants access to real-time financial data through the [Infoway API](https://infoway.io). Query stock prices, crypto markets, forex, market sentiment, sector analysis, and company fundamentals -- all from within your AI conversation.

## Features

- **17 financial data tools** covering real-time quotes, K-line charts, market overview, sector analysis, and stock fundamentals
- **Multi-market support**: US, HK, CN, SG, JP, IN equities + crypto + forex
- **Zero configuration**: just add your API key and start asking questions
- Works with Claude Desktop, Cursor, and any MCP-compatible client

## Installation

```bash
# Using uvx (recommended)
uvx infoway-mcp-server

# Using pip
pip install infoway-mcp-server
```

## Configuration

### Claude Desktop

Add the following to your Claude Desktop configuration file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "infoway": {
      "command": "uvx",
      "args": ["infoway-mcp-server"],
      "env": {
        "INFOWAY_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### Cursor

Add to your Cursor MCP settings (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "infoway": {
      "command": "uvx",
      "args": ["infoway-mcp-server"],
      "env": {
        "INFOWAY_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

## Available Tools

### Real-Time Market Data

| Tool | Description |
|------|-------------|
| `get_realtime_trade` | Get real-time trade data (price, volume, change) for stocks, crypto, or forex |
| `get_market_depth` | Get order book / bid-ask depth for given symbols |
| `get_kline` | Get candlestick / K-line (OHLCV) data with multiple intervals (1m to yearly) |

### Market Overview

| Tool | Description |
|------|-------------|
| `get_market_temperature` | Market sentiment and heat indicators for HK, US, CN, SG |
| `get_market_breadth` | Advance/decline statistics for a market |
| `get_global_indexes` | Real-time data for major global indexes (Dow, S&P, Nasdaq, HSI, etc.) |
| `get_leading_industries` | Top-performing industry sectors ranked by performance |

### Sector / Plate Analysis

| Tool | Description |
|------|-------------|
| `get_industry_list` | Full list of industry sectors with performance data |
| `get_concept_list` | Thematic/concept sectors (AI, EV, Metaverse, etc.) |
| `get_plate_members` | All stocks within a specific sector/plate |
| `get_plate_heatmap` | Sector heatmap data for market visualization |

### Stock Fundamentals

| Tool | Description |
|------|-------------|
| `get_company_overview` | Company profile, description, CEO, headquarters, key metrics |
| `get_stock_valuation` | Valuation ratios: P/E, P/B, EV/EBITDA, dividend yield, market cap |
| `get_stock_ratings` | Analyst consensus: buy/sell/hold counts, target price |
| `get_stock_panorama` | Comprehensive stock summary with key financial data |
| `get_stock_drivers` | Key price drivers and catalysts affecting the stock |

### Utilities

| Tool | Description |
|------|-------------|
| `search_symbols` | Search and list available trading symbols, optionally filtered by market |

## Example Conversations

Once configured, you can ask Claude questions like:

> **"What's the current price of Apple and Tesla?"**
> Claude will use `get_realtime_trade` with codes `AAPL.US,TSLA.US`

> **"Show me the daily K-line for Bitcoin over the last 30 days"**
> Claude will use `get_kline` with codes `BTCUSDT`, market_type `crypto`, kline_type 8, count 30

> **"How is the US market doing today? Which sectors are leading?"**
> Claude will use `get_market_temperature` and `get_leading_industries` for market `US`

> **"Give me a full analysis of Tencent"**
> Claude will combine `get_company_overview`, `get_stock_valuation`, `get_stock_ratings`, and `get_stock_drivers` for `700.HK`

> **"Compare the valuation of NVIDIA vs AMD"**
> Claude will call `get_stock_valuation` for both `NVDA.US` and `AMD.US`

## Get Your API Key

Get your free API key at [infoway.io](https://infoway.io) -- includes a **7-day free trial** with full access to all endpoints.

## Development

```bash
# Clone and install in development mode
git clone https://github.com/infoway-io/infoway-openapi.git
cd infoway-openapi/mcp-server
pip install -e .

# Run directly
infoway-mcp-server

# Or with Python
python -m infoway_mcp_server.server
```

---

# Infoway MCP Server (中文)

MCP（模型上下文协议）服务器，让 Claude 和其他 AI 助手可以通过 [Infoway API](https://infoway.io) 访问实时金融数据。在 AI 对话中即可查询股票价格、加密货币行情、外汇、市场情绪、板块分析和公司基本面。

## 功能特点

- **17 个金融数据工具**，涵盖实时行情、K线图、市场概览、板块分析和个股基本面
- **多市场支持**：美股、港股、A股、新加坡、日本、印度 + 加密货币 + 外汇
- **零配置**：只需添加 API Key 即可开始使用
- 支持 Claude Desktop、Cursor 及所有兼容 MCP 协议的客户端

## 安装

```bash
# 使用 uvx（推荐）
uvx infoway-mcp-server

# 使用 pip
pip install infoway-mcp-server
```

## 配置 Claude Desktop

将以下内容添加到 Claude Desktop 配置文件：

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "infoway": {
      "command": "uvx",
      "args": ["infoway-mcp-server"],
      "env": {
        "INFOWAY_API_KEY": "你的API密钥"
      }
    }
  }
}
```

## 工具列表

### 实时行情
- `get_realtime_trade` — 获取股票、加密货币、外汇的实时成交数据
- `get_market_depth` — 获取买卖盘口深度数据
- `get_kline` — 获取K线（OHLCV）数据，支持1分钟到年线

### 市场概览
- `get_market_temperature` — 市场温度/情绪指标
- `get_market_breadth` — 市场涨跌统计
- `get_global_indexes` — 全球主要指数实时数据
- `get_leading_industries` — 领涨行业板块排名

### 板块分析
- `get_industry_list` — 行业板块列表及涨跌数据
- `get_concept_list` — 概念板块列表（AI、新能源车等）
- `get_plate_members` — 板块成分股列表
- `get_plate_heatmap` — 板块热力图数据

### 个股基本面
- `get_company_overview` — 公司简介与基本信息
- `get_stock_valuation` — 估值指标（PE、PB、市值等）
- `get_stock_ratings` — 分析师评级与目标价
- `get_stock_panorama` — 个股全景数据概览
- `get_stock_drivers` — 股价驱动因素分析

### 其他
- `search_symbols` — 搜索和查询可用交易品种

## 对话示例

> **"苹果和特斯拉现在什么价格？"**
> Claude 会调用 `get_realtime_trade`，代码 `AAPL.US,TSLA.US`

> **"看一下比特币最近30天的日K线"**
> Claude 会调用 `get_kline`，代码 `BTCUSDT`，market_type `crypto`

> **"今天美股表现怎么样？哪些板块领涨？"**
> Claude 会调用 `get_market_temperature` 和 `get_leading_industries`

> **"帮我全面分析一下腾讯"**
> Claude 会组合调用 `get_company_overview`、`get_stock_valuation`、`get_stock_ratings`、`get_stock_drivers`

## 获取 API Key

前往 [infoway.io](https://infoway.io) 免费注册获取 API Key，包含 **7天免费试用**，可访问全部接口。

## License

MIT
