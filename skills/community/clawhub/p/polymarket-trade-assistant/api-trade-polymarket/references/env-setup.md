# .env.aizen Configuration Guide

The `.env.aizen` file must be placed in the `scripts/` directory:
```
{baseDir}/scripts/.env.aizen
```

## Required Variables

### PRIVATE_KEY

Your wallet's private key (without `0x` prefix).

```
PRIVATE_KEY=abc123...def456
```

**How to obtain:**
- MetaMask: Settings → Security → Export Private Key
- Other wallets: Check wallet export/backup feature

**Security:**
- Never commit this file to version control
- Never share this value
- Consider using a dedicated trading wallet with limited funds

### FUNDER_ADDRESS

The address that funds transactions. This is:
- Your wallet address for EOA mode
- The proxy wallet address for Polymarket proxy mode
- The Gnosis Safe address for multisig mode

```
FUNDER_ADDRESS=0x1234...abcd
```

**For Polymarket proxy wallets:**
If you deposited through the Polymarket web UI, your funds are held in a proxy wallet (not your EOA). You can find this address:
1. Go to polymarket.com → Profile → Settings
2. Your proxy address is shown under "Deposit Address"

### SIGNATURE_TYPE

Determines how transactions are signed:

| Value | Mode | Description |
|-------|------|-------------|
| `0` | EOA | Direct wallet signing. Use if funds are in your EOA. |
| `1` | Proxy | Polymarket MagicLink proxy. **Most common for web UI users.** |
| `2` | Gnosis Safe | Multisig wallet signing. |

```
SIGNATURE_TYPE=1
```

**Default:** `1` (Proxy) — this is correct for most users who deposited via the Polymarket web interface.

## Example Configuration

```env
# .env.aizen
PRIVATE_KEY=abc123def456...
FUNDER_ADDRESS=0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18
SIGNATURE_TYPE=1
```

## Verification

After setting up, verify your configuration:

```bash
cd {baseDir}/scripts
npx tsx balance.ts
```

Expected output:
```json
{"usdc_balance": 1500.42, "allowance": 10000.00, "wallet_address": "0x...", "status": "ok"}
```

If you see `config_error`, check that all three variables are set correctly.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `config_error` | Missing PRIVATE_KEY or FUNDER_ADDRESS | Check .env.aizen file exists and has values |
| `init_error` | Wrong SIGNATURE_TYPE or invalid key | Try SIGNATURE_TYPE=0 for EOA, =1 for proxy |
| `balance: 0` | Wrong FUNDER_ADDRESS | Verify address matches where funds are held |
| `UNAUTHORIZED` | Stale API key | Usually auto-resolves; re-run if persistent |

## Security Best Practices

1. **Dedicated wallet** — Use a separate wallet for API trading, not your main holdings
2. **Limited funds** — Only keep trading capital in the wallet
3. **File permissions** — `chmod 600 .env.aizen`
4. **.gitignore** — Ensure `.env.aizen` is gitignored (it is by default)
5. **Regular rotation** — Periodically rotate keys for security
