# logos-node — AI agent skill for Logos Blockchain

[![AgentSkills](https://img.shields.io/badge/AgentSkills-compatible-blue)](https://agentskills.io)
[![Works with Claude Code](https://img.shields.io/badge/Claude_Code-supported-orange)](https://claude.ai/code)
[![Works with Copilot](https://img.shields.io/badge/GitHub_Copilot-supported-blue)](https://github.com/features/copilot)

An AI agent skill that helps you **install, update, and operate a Logos Blockchain testnet validator node** on Linux x86_64.

The skill always fetches the latest release information from GitHub at runtime — no manual updates needed when a new Logos version ships.

---

## What this skill does

| Command | Action |
|---|---|
| `/logos-node install` | Fresh node installation: binary, circuits, systemd service, faucet |
| `/logos-node update` | Breaking upgrade: wipe state, re-init, restart with new binary |
| `/logos-node status` | Check sync mode, peers, block height, wallet balance |

---

## Requirements

- Linux `x86_64` server (no ARM support in current Logos releases)
- `glibc ≥ 2.39` (Ubuntu 24.04+, Debian 12+)
- `≥ 64 GB` free storage
- `curl`, `tar`, `systemctl` on the server
- Root or sudo access for systemd setup

---

## Installation

### Option 1 — npx (no install required)

```bash
# Install for current project
npx @citizenweb3/ai-integrations logos-node

# Install globally (available in all projects)
npx @citizenweb3/ai-integrations logos-node --global
```

### Option 2 — npm global install

```bash
npm install -g @citizenweb3/ai-integrations
ai-integrations logos-node
```

### Option 3 — Claude Code plugin marketplace

```
/plugin marketplace add citizenweb3/ai-integrations
/plugin install logos-node@citizenweb3
```

### Option 4 — OpenClaw / ClawHub

```bash
npx clawhub@latest install citizenweb3/logos-node
```

### Option 5 — Bash (no npm)

```bash
curl -fsSL https://raw.githubusercontent.com/citizenweb3/ai-integrations/logos-node/install.sh | bash
```

---

## Supported agents

| Agent | Skill path |
|---|---|
| Claude Code | `~/.claude/skills/logos-node/` |
| GitHub Copilot | `.agents/skills/logos-node/` |
| Gemini CLI | `.gemini/skills/logos-node/` |
| OpenAI Codex CLI | `.agents/skills/logos-node/` |
| opencode | `.opencode/skills/logos-node/` |
| OpenClaw | `~/.openclaw/skills/logos-node/` |

---

## Usage

After installing, activate the skill in your agent:

```
/logos-node install
/logos-node update
/logos-node status
```

The skill will:
1. Fetch the current Logos release from GitHub API (live — no hardcoded version)
2. Check prerequisites for your server
3. Walk you through each step with exact commands
4. Verify success before declaring done

---

## About

Part of [citizenweb3/ai-integrations](https://github.com/citizenweb3/ai-integrations) — AI agent skills for blockchain node operators.

Built by [CitizenWeb3](https://github.com/citizenweb3) as a public contribution to the Logos ecosystem.

- [Logos Blockchain](https://github.com/logos-blockchain/logos-blockchain)
- [Logos Testnet Dashboard](https://testnet.blockchain.logos.co/web/)
- [AgentSkills Standard](https://agentskills.io)
