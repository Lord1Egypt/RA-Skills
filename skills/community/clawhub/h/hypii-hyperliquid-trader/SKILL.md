---
name: hypii-hyperliquid-trader
description: |
  Hypii AI Trading Agent for Hyperliquid perpetual futures.
  Automated trading strategies with SkillPay micropayment integration.
  
  Features:
  - DCA (Dollar Cost Averaging) Strategy
  - Grid Trading Strategy
  - AI Trading Signals
  - Portfolio Management
  - Automated Trade Execution
  
  Pricing:
  - 5 free calls per day
  - 0.01 USDT for basic queries
  - 0.05 USDT for strategy execution
  - 0.1 USDT for automated trading
  - 19.9 USDT/month for unlimited Pro access
---

# 🤖 Hypii Hyperliquid Trading Agent

AI-powered trading strategies for Hyperliquid perpetual futures with integrated SkillPay billing.

## Features

- **📊 Portfolio Management** - View balances, positions, and P&L
- **💰 Price Queries** - Real-time price data for any coin
- **📈 DCA Strategy** - Automated dollar-cost averaging
- **🔲 Grid Trading** - Range-bound automated trading
- **🤖 AI Signals** - Trend analysis and trading signals
- **🚀 Auto Trading** - Execute trades directly through the agent

## Pricing

| Feature | Price | Description |
|---------|-------|-------------|
| Free Tier | $0 | 5 calls per day (portfolio, price queries) |
| Basic Call | 0.01 USDT | Simple queries and data retrieval |
| Strategy | 0.05 USDT | DCA, Grid, Signal generation |
| Auto Trade | 0.1 USDT | Execute live trades |
| Pro Monthly | 19.9 USDT | Unlimited everything |

## Setup

### Prerequisites

1. Hyperliquid account with funds
2. SkillPay API key (for billing)
3. Private key (for trading operations)

### Environment Variables

```bash
# Required for billing
export SKILLPAY_API_KEY="your_skillpay_api_key"

# For read-only operations
export HYPERLIQUID_ADDRESS="0x..."

# For trading operations
export HYPERLIQUID_PRIVATE_KEY="0x..."

# Optional: Use testnet
export HYPERLIQUID_TESTNET="1"
```

### Installation

```bash
# Install dependencies
cd skills/hypii-hyperliquid-trader && npm install

# The skill will be automatically loaded by OpenClaw
```

## Usage

### Free Commands (5 per day)

```bash
# View portfolio
node index.js portfolio

# Get price
node index.js price BTC
```

### Strategy Commands (0.05 USDT)

```bash
# Create DCA strategy
node index.js dca --coin BTC --amount 100 --frequency daily --orders 10

# Create Grid strategy
node index.js grid --coin ETH --lower 2000 --upper 3000 --grids 10 --investment 1000

# Get AI signal
node index.js signal BTC
```

### Trading Commands (0.1 USDT + requires private key)

```bash
# Market buy
node index.js buy BTC 0.1

# Market sell
node index.js sell ETH 1.0

# Limit order
node index.js trade --coin BTC --side buy --size 0.1 --price 45000 --type limit
```

## API Reference

### Handler Input Format

```javascript
{
  action: 'portfolio' | 'price' | 'dca' | 'grid' | 'signal' | 'trade' | 'buy' | 'sell',
  // Action-specific parameters
  coin: 'BTC',           // For price, signal, trade
  amount: 100,           // For DCA
  frequency: 'daily',    // For DCA: 'hourly', 'daily', 'weekly'
  totalOrders: 10,       // For DCA
  lowerPrice: 2000,      // For Grid
  upperPrice: 3000,      // For Grid
  grids: 10,             // For Grid
  totalInvestment: 1000, // For Grid
  side: 'buy',           // For trade: 'buy' | 'sell'
  size: 0.1,             // For trade
  orderType: 'market',   // For trade: 'market' | 'limit'
  price: 45000           // For limit orders
}
```

### Response Format

```javascript
{
  success: true,
  free: false,           // Whether this was a free call
  remaining: 3,          // Free calls remaining (if applicable)
  charged: 0.05,         // Amount charged in USDT
  data: { ... },         // Response data
  message: "..."         // Human-readable message
}
```

## Safety Features

- ✅ **Slippage Protection** - Market orders use 5% slippage protection
- ✅ **Position Sizing Warnings** - Alerts for large positions (>20% of equity)
- ✅ **Price Validation** - Warns if limit orders are >5% from market price
- ✅ **Free Tier** - Try before you pay
- ✅ **Transparent Billing** - Clear pricing before each operation

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  User Request                                                │
│     ↓                                                        │
│  ┌─────────────────┐                                         │
│  │ Billing Check   │ ← Free tier or SkillPay charge          │
│  └─────────────────┘                                         │
│     ↓                                                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Hypii Strategy Engine                                    ││
│  │  ├─ DCA Strategy                                         ││
│  │  ├─ Grid Strategy                                        ││
│  │  ├─ Trend Analysis                                       ││
│  │  └─ Risk Management                                      ││
│  └─────────────────────────────────────────────────────────┘│
│     ↓                                                        │
│  ┌─────────────────┐                                         │
│  │ Hyperliquid SDK │ ← Execute trades                       │
│  └─────────────────┘                                         │
│     ↓                                                        │
│  Response with billing info                                  │
└─────────────────────────────────────────────────────────────┘
```

## Roadmap

- [ ] Advanced AI models for signal generation
- [ ] Backtesting engine
- [ ] Multi-strategy portfolio management
- [ ] Social trading features
- [ ] Mobile app integration

## Support

- GitHub Issues: [Report bugs or request features]
- Discord: [Join our community]
- Email: support@hypii.io

## License

MIT License - See LICENSE file for details

## Disclaimer

Trading cryptocurrencies involves significant risk. This tool is for educational and automation purposes. Always do your own research and never trade more than you can afford to lose.
