# Mobula Prices - Real-Time Crypto Market Data

> Get real-time token prices, market caps, volume, and analytics across 88+ blockchains. Free tier, no credit card required.

[![ClawHub](https://img.shields.io/badge/ClawHub-Install-blue)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What This Skill Does

**mobula-prices** gives your OpenClaw agent instant access to crypto market data for 200M+ tokens across 88+ blockchains.

### Key Features

✅ **Real-time prices** - Current price, 24h change, volume, market cap
✅ **Historical data** - Charts and trends for any timeframe
✅ **Batch queries** - Compare up to 500 tokens in one request
✅ **Token metadata** - Project info, social links, contract addresses

### Perfect For

- Checking token prices quickly
- Comparing multiple tokens
- Analyzing price trends and charts
- Monitoring trading volume
- Researching new tokens

---

## Quick Start (5 minutes)

### 1. Install the Skill

**Via ClawHub (recommended):**
```
Tell your agent: "Install mobula-prices from ClawHub"
```

**Via URL:**
```
Tell your agent: "Install skill from https://raw.githubusercontent.com/Flotapponnier/Crypto-date-openclaw/main/skills/mobula-prices/SKILL.md"
```

### 2. Get Your Free API Key

1. Go to [mobula.io](https://mobula.io)
2. Sign up (takes 30 seconds)
3. Copy your API key from the dashboard

**Free tier includes:**
- 100 requests/minute
- No credit card required
- Access to all 88+ blockchains
- 200M+ token coverage

### 3. Set Your API Key

```bash
export MOBULA_API_KEY="your_api_key_here"
```

**Make it permanent:**
```bash
echo 'export MOBULA_API_KEY="your_key"' >> ~/.zshrc
source ~/.zshrc
```

### 4. Test It

Ask your agent:
- "What's the price of Bitcoin?"
- "Compare BTC, ETH, and SOL performance today"
- "Show me ETH price history for the last 30 days"

---

## Example Prompts

### Basic Price Checks
```
"What's the price of Bitcoin?"
"Show me PEPE's market cap"
"Is ETH pumping or dumping right now?"
```

### Multi-Token Comparisons
```
"Compare BTC, ETH, and SOL performance today"
"Show me the top 10 tokens by volume"
"Which is up more in the last 24h: DOGE or SHIB?"
```

### Historical Analysis
```
"Show me ETH price for the last 30 days"
"What was Bitcoin's price on January 1st?"
"Has PEPE been trending up or down this week?"
```

### Advanced Queries
```
"Get market data for BRETT on Base chain"
"Show recent trades for this contract: 0x532f27..."
"Find me the project website for this token"
```

---

## What Data You Get

### Market Data
- Current price (USD)
- Price changes: 1h, 24h, 7d, 30d
- Volume (24h)
- Market cap & fully diluted valuation
- Liquidity
- All-time high/low with dates
- Supply metrics

### Historical Charts
- Price points with timestamps
- Volume at each point
- Market cap over time
- Customizable timeframes

### Live Trade Feed
- Recent buy/sell activity
- Trade amounts (tokens + USD)
- Wallet addresses
- DEX and chain info
- Transaction hashes

### Token Information
- Name, symbol, logo
- Project description
- Official website
- Social links (Twitter, Telegram, Discord)
- Contract addresses across all chains
- Launch date

---

## Supported Blockchains

**88+ chains including:**
- Ethereum
- Base
- Arbitrum
- Optimism
- Polygon
- BNB Chain
- Avalanche
- Solana
- Fantom
- Cronos
- And many more...

Full list: [docs.mobula.io/blockchains](https://docs.mobula.io/blockchains)

---

## Security

✅ **Read-only access** - No trading, no transactions
✅ **No private keys** - Only public blockchain data
✅ **Open source** - [View code on GitHub](https://github.com/Flotapponnier/Crypto-date-openclaw)
✅ **VirusTotal verified** - Benign scan results

Your API key only provides access to public market data. It cannot:
- Execute trades
- Access your wallets
- Sign transactions
- Access private information

---

## Rate Limits

**Free tier:** 100 requests/minute

**Tips to stay within limits:**
- Use batch queries (`mobula_market_multi`) for multiple tokens
- Cache results when appropriate
- Upgrade to higher tier at [mobula.io](https://mobula.io) if needed

---

## Troubleshooting

### "API key not found" error
```bash
# Check if key is set
echo $MOBULA_API_KEY

# Set it if missing
export MOBULA_API_KEY="your_key_here"

# Restart your agent
openclaw restart
```

### "Token not found" error
- Try using the contract address instead of name
- Check spelling of token name
- Verify the token exists on the specified blockchain

### Rate limit errors
- Wait a few minutes and retry
- Use batch endpoints for multiple tokens
- Consider upgrading your plan at [mobula.io](https://mobula.io)

---

## Related Skills

Want more Mobula features? Check out:

- **[mobula-wallet](../mobula-wallet/)** - Portfolio tracking and wallet analytics
- **[mobula-alerts](../mobula-alerts/)** - 24/7 monitoring and smart alerts

---

## Resources

- **Get API Key:** [mobula.io](https://mobula.io)
- **API Documentation:** [docs.mobula.io](https://docs.mobula.io)
- **Main Repository:** [GitHub](https://github.com/Flotapponnier/Crypto-date-openclaw)
- **Report Issues:** [GitHub Issues](https://github.com/Flotapponnier/Crypto-date-openclaw/issues)
- **Skill Documentation:** [SKILL.md](./SKILL.md)

---

## FAQ

**Q: Do I need to pay for the API key?**
A: No. The free tier (100 req/min) is sufficient for most users. No credit card required.

**Q: Can I check prices for any token?**
A: Yes. Mobula covers 200M+ tokens across 88+ blockchains.

**Q: Does this work with Solana tokens?**
A: Yes. Mobula supports Ethereum, Base, Solana, and 85+ other chains.

**Q: Can I use this to execute trades?**
A: No. This skill is read-only market data. For trading, use dedicated trading skills.

**Q: How often is the data updated?**
A: Real-time. Prices update continuously with sub-second latency.

---

## License

MIT License - See [LICENSE](../../LICENSE)

---

## Credits

- **Built by:** [Mobula](https://mobula.io)
- **For:** [OpenClaw](https://openclaw.ai)
- **Coverage:** 88+ blockchains, 200M+ tokens
- **Trusted by:** Chainlink, Supra, API3 (oracle-grade pricing)
