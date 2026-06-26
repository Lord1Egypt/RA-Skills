# Mobula Wallet - Portfolio Tracking & Whale Analytics

> Track wallet portfolios and transaction history across 88+ blockchains. Monitor holdings, analyze trades, and follow whale wallets.

[![ClawHub](https://img.shields.io/badge/ClawHub-Install-blue)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What This Skill Does

**mobula-wallet** gives your OpenClaw agent the ability to analyze any wallet across all major blockchains, track portfolios in real-time, and monitor whale activity.

### Key Features

✅ **Cross-chain portfolio** - See all holdings across 88+ chains in one call
✅ **Transaction history** - Full on-chain activity analysis
✅ **Whale tracking** - Monitor large wallet movements
✅ **Portfolio analytics** - Allocation, profit/loss, trends
✅ **ENS support** - Use vitalik.eth instead of 0x addresses

### Perfect For

- Tracking your own portfolio across chains
- Analyzing whale wallet holdings
- Monitoring wallet transactions
- Following smart money
- Portfolio allocation analysis

---

## Quick Start (5 minutes)

### 1. Install the Skill

**Via ClawHub (recommended):**
```
Tell your agent: "Install mobula-wallet from ClawHub"
```

**Via URL:**
```
Tell your agent: "Install skill from https://raw.githubusercontent.com/Flotapponnier/Crypto-date-openclaw/main/skills/mobula-wallet/SKILL.md"
```

### 2. Get Your Free API Key

1. Go to [mobula.io](https://mobula.io)
2. Sign up (takes 30 seconds)
3. Copy your API key from the dashboard

**Free tier includes:**
- 100 requests/minute
- No credit card required
- Access to all 88+ blockchains
- Unlimited wallet queries

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
- "Show portfolio for wallet vitalik.eth"
- "What did this wallet buy recently: 0x742d35Cc..."
- "Track this whale wallet's activity"

---

## Example Prompts

### Portfolio Tracking
```
"Show portfolio for wallet vitalik.eth"
"What's the total value of wallet 0x742d35..."
"What tokens does this wallet hold?"
"Show me the top 5 holdings in this wallet"
```

### Transaction Analysis
```
"What did this wallet buy recently?"
"Show me the last 10 transactions for 0x123..."
"When did this wallet last sell ETH?"
"What tokens has this wallet been accumulating?"
```

### Whale Watching
```
"Track this whale's activity: 0xabc..."
"Show me large transactions from this wallet"
"What's this whale buying right now?"
"Has this wallet made any big moves today?"
```

### Portfolio Analysis
```
"What's the allocation breakdown of this wallet?"
"Show me profit/loss for this portfolio"
"Which tokens in this wallet are up today?"
"Is this wallet concentrated in one asset?"
```

---

## What Data You Get

### Portfolio Overview
- Total portfolio value (USD)
- All tokens held across all chains
- Token balances (amount + USD value)
- Current prices for each holding
- 24h price changes
- Estimated profit/loss per token
- Portfolio allocation percentages
- NFTs (if present)

### Transaction History
- Type (swap, transfer, mint, burn)
- Tokens involved (from/to)
- Trade amounts
- USD values at transaction time
- Timestamps
- Chain information
- Transaction hashes
- Wallet addresses (sender/receiver)

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

## Security & Privacy

✅ **Read-only access** - No trading, no transactions
✅ **No private keys** - Only public blockchain data
✅ **Open source** - [View code on GitHub](https://github.com/Flotapponnier/Crypto-date-openclaw)
✅ **VirusTotal verified** - Benign scan results

### Privacy Important Notes

⚠️ **Wallet addresses are public data:**
- On-chain data is already public on blockchain explorers
- This skill queries that public data via Mobula API
- Wallet addresses you query are sent to Mobula's servers

⚠️ **Best practices:**
- Only query public wallet addresses (e.g., vitalik.eth, known whales)
- Don't query wallets you want to keep private
- Don't query wallets that link to your identity if you value privacy
- Use a separate API key for testing vs production

**Your API key cannot:**
- Access private keys or seed phrases
- Execute trades or transactions
- Sign anything on your behalf
- Transfer funds

---

## Use Cases

### 1. Portfolio Guardian

Monitor your own wallet 24/7 for concentration risks:

```
"Monitor my wallet 0x... and alert me if any token
drops more than 15% or my allocation exceeds 40%
on one asset. Daily summary at 9am."
```

Combine with [mobula-alerts](../mobula-alerts/) skill for automation.

### 2. Whale Tracking

Follow smart money and get insights:

```
"Watch these whale wallets: 0xabc, 0xdef, 0x123.
Show me whenever they make a transaction over $50K."
```

### 3. Portfolio Analysis

Understand your allocation and risk:

```
"Analyze my wallet 0x... and tell me if I'm too
concentrated in any single token. Suggest rebalancing
if needed."
```

### 4. Transaction Forensics

Track where money is flowing:

```
"Show me all ETH transactions from this wallet in
the last 30 days. Who are they sending to?"
```

---

## Rate Limits

**Free tier:** 100 requests/minute

**Tips to stay within limits:**
- Cache portfolio data (doesn't change every second)
- Use transaction filters to limit results
- Batch wallet queries when possible
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

### "Invalid wallet address" error
- Wallet addresses should be 42 characters starting with 0x
- Or use ENS names like vitalik.eth
- Check for typos in the address

### "No activity found" error
- Wallet may have no balance or transactions
- Try a different blockchain (use `blockchains` parameter)
- Verify the wallet address is correct

---

## Related Skills

Want more Mobula features? Check out:

- **[mobula-prices](../mobula-prices/)** - Token prices and market data
- **[mobula-alerts](../mobula-alerts/)** - 24/7 monitoring and smart alerts

---

## Resources

- **Get API Key:** [mobula.io](https://mobula.io)
- **API Documentation:** [docs.mobula.io](https://docs.mobula.io)
- **Main Repository:** [GitHub](https://github.com/Flotapponnier/Crypto-date-openclaw)
- **Privacy Policy:** [mobula.io/privacy](https://mobula.io/privacy)
- **Report Issues:** [GitHub Issues](https://github.com/Flotapponnier/Crypto-date-openclaw/issues)
- **Skill Documentation:** [SKILL.md](./SKILL.md)

---

## FAQ

**Q: Can I track my own wallet?**
A: Yes, but remember that wallet addresses you query are sent to Mobula's API. Only query wallets you're comfortable being associated with publicly.

**Q: Does this work across all blockchains?**
A: Yes. One query returns holdings across all 88+ supported chains.

**Q: Can I see NFTs?**
A: Yes. The portfolio endpoint includes NFT holdings if present.

**Q: Can this skill execute trades?**
A: No. This skill is read-only. It can only view public on-chain data.

**Q: How do I track multiple wallets?**
A: Ask your agent to query each wallet. Combine with [mobula-alerts](../mobula-alerts/) for automated monitoring.

**Q: Can I filter transactions by token?**
A: Yes. Use the `asset` parameter to filter by specific token.

---

## License

MIT License - See [LICENSE](../../LICENSE)

---

## Credits

- **Built by:** [Mobula](https://mobula.io)
- **For:** [OpenClaw](https://openclaw.ai)
- **Coverage:** 88+ blockchains, cross-chain portfolio tracking
