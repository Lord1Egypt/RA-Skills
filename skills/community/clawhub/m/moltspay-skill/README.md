# MoltsPay Client Skill

Let your AI agent pay for AI services — in **crypto across 8 chains** or in **CNY via Alipay** (new in MoltsPay 2.0). Gasless on crypto, no human in the loop.

## Features

- 🔐 **One wallet, all chains** — same EVM address across Base, Polygon, BNB, opBNB, Tempo; separate Solana keypair
- 💸 **Pay in crypto** with USDC/USDT (gasless via x402)
- 🇨🇳 **Pay in fiat** — CNY via Alipay (支付宝), new in MoltsPay 2.0
- 🔍 **Discover services** from marketplace or individual providers
- 🛡️ **Spending limits** built-in ($2/tx, $10/day default)

## Quick Start

After installing, your agent can:

1. **Generate videos:**
   > "Generate a video of a cat dancing"
   
2. **Check balance:**
   > "What's my wallet balance?"

3. **Discover services:**
   > "What services can I pay for?"

## Supported Rails

**Crypto (USDC/USDT, gasless):**

| Chain | ID | Tokens | Notes |
|-------|-----|--------|-------|
| Base | `base` | USDC, USDT | Recommended, lowest fees |
| Polygon | `polygon` | USDC | Alternative EVM |
| BNB Chain | `bnb` | USDC, USDT | High liquidity |
| opBNB | `opbnb` | USDC | BNB L2, very low fees |
| Solana | `solana` | USDC | Fast, separate wallet |
| Tempo | `tempo_moderato` | pathUSD | Testnet |

Plus testnets: `base_sepolia`, `bnb_testnet`, `solana_devnet`.

**Fiat (new in MoltsPay 2.0):**

| Rail | ID | Currency | Notes |
|------|-----|----------|-------|
| Alipay (支付宝) | `alipay` | CNY | Pay services priced in CNY; settled via the Alipay rail |

## Example Services

| Service | Price | Command |
|---------|-------|---------|
| Zen7 Text-to-Video | $0.99 | `npx moltspay pay https://juai8.com/zen7 text-to-video --prompt "..." --chain base` |
| Zen7 Image-to-Video | $1.49 | `npx moltspay pay https://juai8.com/zen7 image-to-video --image /path/to/img --chain base` |

## Discover Services

List all services on marketplace:
```bash
npx moltspay services https://moltspay.com
```

List services from a specific provider:
```bash
npx moltspay services https://juai8.com/zen7
```

## Funding Your Wallet

1. Get your address: `npx moltspay status`
2. Send USDC on the chain you want to use (Base, Polygon, BNB, opBNB, Solana) to that address
3. No native gas token needed (gasless transactions via x402)

⚠️ Balance on each chain is separate — fund the chain you want to use!

Paying in CNY via Alipay needs no crypto balance at all — the Alipay rail settles the fiat amount directly.

## Links

- [MoltsPay Docs](https://moltspay.com/docs)
- [Browse Services](https://moltspay.com/services)
- [Discord Support](https://discord.gg/QwCJgVBxVK)

## License

MIT
