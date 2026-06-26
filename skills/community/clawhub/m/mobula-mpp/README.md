# mpp-skill

Pay-as-you-go Mobula API skill for ClaudeHub / OpenClaw agents.

Fetch crypto prices, wallet positions, and market data without any signup, API key, or subscription. Each call costs ~$0.0004 in USDC.e on the Tempo chain (chainId 4217), settled directly from a wallet you control.

## Quick start

```bash
git clone https://github.com/Flotapponnier/mpp-skill.git
cd mpp-skill
bun install

# 1. Create a Tempo wallet (saved at ~/.mpp-skill/wallet.json, chmod 600)
bun run start wallet-create

# 2. Fund it with USDC.e via the bridge link printed by step 1
#    https://relay.link/bridge/tempo?toAddress=<your-address>

# 3. Make calls
bun run start price bitcoin
bun run start wallet 0xd04b77bb40944110ec9c9e3165f67dadf9d52f21
bun run start lighthouse
```

That's it — no API key, no signup, no subscription.

## How it works

When you hit `https://mpp.mobula.io/api/2/*` Mobula returns HTTP 402 with a payment challenge. This skill:
1. Decodes the challenge,
2. Signs and broadcasts `transferWithMemo` on USDC.e (Tempo, chainId 4217) from your wallet,
3. Retries the request with the resulting tx hash as a payment credential,
4. Returns the data.

Tempo's gas is USDC (no separate ETH required), so a few dollars of USDC.e last for thousands of calls.

## Use as an agent skill

```bash
cd ~/your-agent/skills/
git clone https://github.com/Flotapponnier/mpp-skill.git mpp
cd mpp && bun install
```

Then from your agent code:

```ts
// Per-user encrypted wallets (one wallet per Telegram user, etc.)
import { createUserWallet, getUserWalletAddress } from "mpp-skill/src/wallet";
import { userMobulaCall } from "mpp-skill/src/mpp/user-mpp";

const userId = 1162998296;
if (!(await getUserWalletAddress(userId))) await createUserWallet(userId);
const price = await userMobulaCall(userId, "/api/2/token/price", { asset: "bitcoin" });
```

See [SKILL.md](./SKILL.md) for the full agent-facing docs, payment flow internals, and the per-call vs subscription decision.

## Project structure

```
mpp-skill/
├── src/
│   ├── index.ts             # CLI entry
│   ├── cli-wallet.ts        # Single hot wallet for the CLI (~/.mpp-skill/wallet.json)
│   ├── wallet.ts            # Per-user encrypted wallets (for multi-tenant agents)
│   ├── commands/
│   │   └── mpp.ts           # CLI command handler
│   └── mpp/
│       ├── tempo-client.ts  # 402 → sign → retry flow on Tempo USDC.e
│       └── user-mpp.ts      # Helpers tying per-user wallets to tempoFetch
├── SKILL.md
├── package.json
└── README.md
```

## Requirements

- Bun ≥ 1.0.0
- viem (auto-installed via `bun install`)

## License

MIT
