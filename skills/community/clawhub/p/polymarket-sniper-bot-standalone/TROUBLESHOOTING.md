# Troubleshooting: Polymarket Sniper Bot

## Common Errors

### 1. Insufficient USDC balance
- **Cause:** Wallet balance is below `position_size_usd` (default $100).
- **Fix:** Fund your wallet on Polygon with USDC (Bridged). Ensure you have enough to cover the position size.

### 2. Invalid private key
- **Cause:** `wallet_private_key` in `config.yaml` is missing, malformed, or still set to placeholder `0xYOUR_PRIVATE_KEY`.
- **Fix:** Replace with your actual private key (64 hex chars, prefixed with `0x`). Keep this secret.

### 3. CLOB API error 401/403
- **Cause:** CLOB API credentials (`clob_api_key`, `clob_api_secret`, `clob_api_passphrase`) are incorrect or missing.
- **Fix:** Obtain these from Polymarket Settings → API. Double‑check values in `config.yaml`.

### 4. Orders not filling
- **Cause:** The bot uses a mock price ($0.50) if market data is unavailable; the market may lack liquidity at that price or the order size is too small.
- **Fix:** Ensure the Gamma API is accessible. Consider enhancing `calculate_momentum` to fetch the latest price dynamically. Adjust `position_size_usd`.

### 5. pro_mode not taking effect
- **Cause:** `pro_mode: true` not set in `config.yaml` or the file wasn't reloaded.
- **Fix:** Add `pro_mode: true` (YAML boolean) to `config.yaml` and restart the bot.

---

Still stuck? Contact: wessmith9822@gmail.com
