# Polymarket API Setup Guide

This guide walks you through getting API access for live trading. **Paper trading works without any setup** - API keys are only needed for placing real orders.

## Quick Start (Paper Trading Only)

No setup required! All tools work in dry-run mode:

```bash
npm install
node demo.cjs                    # Test all tools
node negrisk_scanner.cjs scan    # Find arbitrage opportunities
node btc_15m.cjs watch --dry     # Paper trade BTC scalping
```

## Live Trading Setup

### Step 1: Polymarket Account

1. **Create Account:** Go to [polymarket.com](https://polymarket.com)
2. **Verify Email:** Check your inbox and click the verification link
3. **Complete KYC:** Upload government ID and complete identity verification
4. **Fund Account:** Deposit USDC (minimum $1,000 recommended for CLOB access)

### Step 2: Get API Credentials

**Method A: CLOB API Keys (Recommended)**

1. Log into Polymarket
2. Go to **Account Settings** → **API Keys**
3. Click **Generate New API Key**
4. Copy and save:
   - API Key
   - Secret Key
   - Passphrase
   - Funder Address (your wallet address)

**Method B: Private Key (Advanced)**

If you prefer direct wallet access:
1. Export your private key from MetaMask/wallet
2. Note your wallet address
3. Ensure wallet has USDC balance

### Step 3: Configure Environment

Create a `.env` file in the polymarket-alpha directory:

```bash
# CLOB API Method (Recommended)
POLYMARKET_API_KEY=your_api_key_here
POLYMARKET_SECRET=your_secret_key_here
POLYMARKET_PASSPHRASE=your_passphrase_here
POLYMARKET_FUNDER=your_wallet_address_here

# OR Private Key Method
POLY_PK=your_private_key_without_0x
POLY_FUNDER=your_wallet_address

# Optional: Custom settings
MAX_TRADE_SIZE=50        # Maximum $ per trade
MIN_EDGE_THRESHOLD=0.03  # Minimum 3% edge required
```

### Step 4: Test Connection

```bash
# Test API connection (will show balance/error)
node btc_15m.cjs trade --dry

# If working, try small live trade
node negrisk_scanner.cjs scan
# (manually place small trade to test)
```

## API Access Tiers

### Tier 1: Public Data (No Account)
- ✅ Market scanning
- ✅ Price feeds  
- ✅ Volume data
- ✅ Paper trading
- ❌ Order placement
- ❌ Portfolio tracking

**Tools that work:** All tools in `--dry` mode

### Tier 2: Basic Account (Free)
- ✅ Everything in Tier 1
- ✅ Account balance
- ✅ Order history
- ❌ CLOB API access
- ❌ Automated trading

**Tools that work:** All tools, some live trading via web interface

### Tier 3: CLOB API Access ($1,000+ balance)
- ✅ Everything in Tier 2
- ✅ Automated order placement
- ✅ Real-time order books
- ✅ Full API access
- ✅ Institutional features

**Tools that work:** All tools with full automation

## Rate Limits

Polymarket has the following rate limits:

- **Gamma API:** 10 requests/second (market data)
- **CLOB API:** 5 requests/second (trading)
- **Order Books:** 2 requests/second (book data)

All tools automatically handle rate limiting with exponential backoff.

## Trading Fees

- **15-minute markets:** 0% fees
- **Regular markets:** 2% on winnings
- **High-volume traders:** Reduced fees available

## Security Best Practices

### API Keys
- ✅ Store in `.env` file (never commit to git)
- ✅ Use read-only keys when possible
- ✅ Rotate keys monthly
- ✅ Monitor API usage
- ❌ Never share keys in chat/email
- ❌ Don't hardcode keys in scripts

### Wallet Security
- ✅ Use hardware wallet when possible
- ✅ Keep private keys offline
- ✅ Use separate wallet for trading
- ✅ Enable 2FA on Polymarket account
- ❌ Never store large amounts in hot wallets

### Trading Security
- ✅ Start with small position sizes
- ✅ Test in paper trading first
- ✅ Monitor positions regularly
- ✅ Set stop-losses
- ❌ Never risk more than you can afford to lose

## Common Setup Issues

### "Invalid API credentials"
1. Check that API key, secret, and passphrase are correct
2. Ensure no extra spaces or quotes
3. Verify your account has CLOB access ($1K+ balance)
4. Try regenerating API keys

### "Insufficient balance"
1. Check USDC balance on Polymarket
2. Ensure funds are settled (not pending)
3. Verify minimum trade sizes
4. Check if funds are in open orders

### "Rate limit exceeded"
1. Tools automatically retry with backoff
2. Reduce concurrent tool usage
3. Use `--no-books` flags to reduce API calls
4. Wait a few minutes and retry

### "Network timeout"
1. Check internet connection
2. Try different network/VPN
3. Polymarket API may be temporarily down
4. Use `--timeout=60` to increase timeout

### "Market not found"
1. Market may have closed/resolved
2. Check if market slug is correct
3. Try scanning for active markets first
4. Some markets are region-restricted

## Environment Variables Reference

```bash
# REQUIRED for live trading (CLOB method)
POLYMARKET_API_KEY=           # Your API key
POLYMARKET_SECRET=            # Your secret key  
POLYMARKET_PASSPHRASE=        # Your passphrase
POLYMARKET_FUNDER=            # Your wallet address

# ALTERNATIVE (private key method)
POLY_PK=                      # Private key (without 0x)
POLY_FUNDER=                  # Wallet address

# OPTIONAL settings
MAX_TRADE_SIZE=10             # Max $ per trade (default: 10)
MIN_EDGE_THRESHOLD=0.05       # Min edge % (default: 0.05 = 5%)
POLL_INTERVAL=60000           # Polling interval ms (default: 60000)
RATE_LIMIT_DELAY=200          # API delay ms (default: 200)
TIMEOUT_MS=30000              # Request timeout (default: 30000)

# DEBUG settings
DEBUG=1                       # Enable debug logging
VERBOSE=1                     # Verbose output
LOG_LEVEL=info                # Log level (error/warn/info/debug)
```

## Testing Your Setup

### 1. Paper Trading Test
```bash
# Should work without any credentials
node demo.cjs
node alpha_scan.cjs
node negrisk_scanner.cjs scan
```

### 2. API Connection Test
```bash
# With credentials configured:
node btc_15m.cjs trade --dry    # Should show balance/connection status
```

### 3. Small Live Trade Test
```bash
# Find a small arbitrage opportunity
node negrisk_scanner.cjs scan

# Place a $1-2 test trade manually via web interface
# Verify it appears in trade history
```

### 4. Full Automation Test
```bash
# Run continuous paper trading for 30 minutes
node latency_arb.cjs watch --dry

# Check trade history
node latency_arb.cjs history
```

## Support

### Self-Help
1. Check this SETUP.md file
2. Review error messages carefully
3. Try paper trading first
4. Verify API credentials
5. Check Polymarket status page

### Get Help
- **Email:** support@openclaw.com
- **Subject Line:** "Polymarket Alpha Setup - [Your Issue]"
- **Include:** Error messages, tool name, operating system
- **Response Time:** 24-48 hours

### Community
- **Twitter:** @OpenClaw for updates
- **Status:** Check Polymarket social media for API issues
- **Updates:** Watch for skill updates in ClawHub

## Legal Notes

- **Testing:** Always test with small amounts first
- **Compliance:** Ensure prediction market trading is legal in your jurisdiction
- **Risk:** Only risk capital you can afford to lose
- **Age:** Must be 18+ and meet Polymarket's terms of service
- **Taxes:** Consult a tax professional for trading gains/losses

---

**Ready to start?** Run `node demo.cjs` to test all tools!

**Questions?** Email support@openclaw.com with "Setup Help" in the subject line.