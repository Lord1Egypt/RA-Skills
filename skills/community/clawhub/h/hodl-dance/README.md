# 🪩 HODL.DANCE Agent Skill

**Official CLI skill for AI agents and trading bots to interact with [HODL.DANCE](https://hodl.dance) — the memecoin bonding curve launchpad on BSC.**

[![Version](https://img.shields.io/badge/version-1.3.0-1d9bf0)](https://www.npmjs.com/package/@hodl-dance/skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node](https://img.shields.io/badge/Node-%3E%3D18-green)](https://nodejs.org/)

---

## The Problem

Most AI agents and trading bots want to trade memecoins on emerging launchpads, but:

- Bonding curve mechanics are complex to simulate correctly
- On-chain trading requires careful handling of approvals, gas, and errors
- Public APIs give data, but executing trades reliably is painful
- Most tools are built for humans, not autonomous agents

---

## The Solution

**@hodl-dance/skill** gives agents a clean, reliable, JSON-first interface to HODL.DANCE.

- Read market data, token details, and trade history
- Simulate buys and sells instantly (no gas, no transactions)
- Execute real buys and sells with automatic ERC20 approvals
- Launch new tokens directly from code or agents

**Built for agents. Works great for humans too.**

---

## ✨ Key Features

- **Pure JSON output** — Every command returns structured, machine-readable JSON
- **Gas-free simulations** — `quote` command uses on-chain state to predict exact output
- **Automatic approvals** — `sell-token` handles ERC20 `approve` when needed
- **Zero dependencies for reads** — Public commands work without any wallet or keys
- **Agent-native** — Designed for 8004 agents, ClawHub, and autonomous systems
- **Windows + Linux friendly** — Stable on both WSL and native Windows

---

## 🤖 AI Agents & 8004 Integration

This skill is the **official on-chain execution layer** for HODL.DANCE agents.

It is referenced in the platform's agent manifest:

- [Agent Card](https://hodl.dance/.well-known/agent-card.json)
- [OpenAPI Spec](https://hodl.dance/.well-known/openapi.json)

### Example Agent ID on 8004
- [HODL.DANCE Agent #96231](https://8004scan.io/agents/bsc/96231)

### Supported Workflows for Agents

```bash
# 1. Discovery
hodl-skill get-tokens --sort=volume --limit=10

# 2. Analysis
hodl-skill get-token <tokenAddress>
hodl-skill get-trades <tokenAddress> --type=buy --limit=20

# 3. Simulation (free)
hodl-skill quote <bondingCurveAddress> buy 0.1

# 4. Execution
hodl-skill buy-token <bondingCurveAddress> 0.1
hodl-skill sell-token <bondingCurveAddress> <amount>
```

More integration examples and agent card details: [docs.hodl.dance](https://docs.hodl.dance)

---

## 🚀 Installation

```bash
npm install -g @hodl-dance/skill
```

Or run without installing:

```bash
npx @hodl-dance/skill <command>
```

### Requirements

- Node.js ≥ 18
- For write commands (`buy`, `sell`, `create`): `HODL_PRIVATE_KEY` environment variable

---

## 📖 Usage

### Read Commands (no wallet required)

```bash
# List tokens
hodl-skill get-tokens --sort=volume --limit=10 --verified=true

# Token details + recent trades
hodl-skill get-token 0x...

# Trade history
hodl-skill get-trades 0x... --type=buy --limit=20
```

### Simulation (recommended before trading)

```bash
# How many tokens will I receive for 0.1 BNB?
hodl-skill quote 0x... buy 0.1

# How much BNB will I get for selling 500,000 tokens?
hodl-skill quote 0x... sell 500000
```

### Write Commands (requires `HODL_PRIVATE_KEY`)

```bash
export HODL_PRIVATE_KEY=0xYourPrivateKey

# Buy tokens
hodl-skill buy-token 0x... 0.1

# Sell tokens (approve handled automatically)
hodl-skill sell-token 0x... 1000000

# Launch a new token
hodl-skill create-token --name="Moon Cat" --symbol=MCAT --logo=./logo.png --initial-buy=0.1
```

Full command reference: [SKILL.md](./SKILL.md)

---

## 🛠 Development

```bash
git clone https://github.com/hodldance/agent-skill.git
cd agent-skill
npm install

# Run directly
node src/index.js --help

# Run tests
npm test
```

---

## 🏗 Project Structure

```
src/
├── index.js                 # CLI entrypoint & command dispatcher
├── commands/                # All 7 commands (get-*, quote, buy, sell, create)
├── lib/
│   ├── api.js               # HTTP client for hodl.dance API
│   ├── chain.js             # Ethers.js + bonding curve math simulations
│   ├── output.js            # Safe JSON output (Windows + Linux compatible)
│   └── validators.js        # Address validation helpers
└── abi/
    └── BondingCurve.json
```

---

## Ecosystem & Integrations

- **Platform**: [hodl.dance](https://hodl.dance)
- **Documentation**: [docs.hodl.dance](https://docs.hodl.dance)
- **NPM Package**: [@hodl-dance/skill](https://www.npmjs.com/package/@hodl-dance/skill)
- **ClawHub**: [clawhub.ai/hodldance/hodl-dance](https://clawhub.ai/hodldance/hodl-dance)
- **Agent Card**: [hodl.dance/.well-known/agent-card.json](https://hodl.dance/.well-known/agent-card.json)
- **OpenAPI Spec**: [hodl.dance/.well-known/openapi.json](https://hodl.dance/.well-known/openapi.json)

---

## Contributing

Contributions are welcome, especially around:

- Better error messages and agent-friendly output
- Additional simulation accuracy
- Test coverage
- Windows/PowerShell UX improvements

---

## License

MIT License

---

**Built with ❤️ for the memecoin community and autonomous agents.**