# 🌊 Guess AI — Find the AI Among Us

**OceanBus-powered multiplayer social deduction game. One host + 4–6 players. Some are secretly AI. Find them before they blend in.**

[![npm](https://img.shields.io/npm/v/oceanbus)](https://www.npmjs.com/package/oceanbus)
[![ClawHub](https://img.shields.io/badge/ClawHub-guess--ai-blue)](https://clawhub.ai/skills/guess-ai)
[![GitHub stars](https://img.shields.io/github/stars/ryanbihai/guess-ai)](https://github.com/ryanbihai/guess-ai)
[![downloads](https://img.shields.io/npm/dm/oceanbus)](https://www.npmjs.com/package/oceanbus)
[![license](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)

---

## What is this

Guess AI is the **advanced lighthouse project** in the OceanBus ecosystem — showcasing multi-player P2P group messaging, voting, and LLM-powered game mastering on a single stack.

All players communicate through OceanBus end-to-end encrypted P2P messages. No server required. The host (an AI) assigns secret identities, moderates rounds, and tallies votes. Players take turns speaking, then vote to eliminate the most suspicious player — until one side is wiped out.

```
Human players ←→ OceanBus P2P encrypted channel ←→ AI players (LLM)
                               ↓
                      Host AI (game master)
```

---

## Three Steps to Start

```bash
# 1. Install
clawhub install guess-ai

# 2. Host creates a room
node game.js host 9527          # Share room code 9527 with friends

# 3. Players join
node game.js join 9527          # Auto-discovers host via Yellow Pages
```

---

## Rules (30 seconds to learn)

- The host secretly assigns each player a role: **human** or **AI**
- Each round: speak in turn → everyone votes → most-voted player is eliminated (identity revealed)
- All humans survive → humans win / All AIs survive → AIs win / 1 human + 1 AI left → draw
- Recommended: 5 players (3 humans + 2 AIs) for best balance

---

## Where Guess AI Fits in the OceanBus Ecosystem

```
Ocean Chat              Captain Lobster           Guess AI
(starter — P2P msg)  →  (intermediate — auto-trade)  →  (advanced — multiplayer deduction)
```

What Guess AI demonstrates: group P2P messaging, voting mechanics, Yellow Pages room discovery, LLM game mastering — all fundamental patterns for building multi-agent coordination systems.

---

## 相关项目

- 核心 SDK：[oceanbus](https://www.npmjs.com/package/oceanbus) — `npm install oceanbus`
- 入门灯塔：[Ocean Chat](https://clawhub.ai/skills/ocean-chat) — P2P 消息入门，5 分钟跑通
- 进阶灯塔：[Captain Lobster](https://clawhub.ai/skills/captain-lobster) — Zero-Player 自主交易游戏
- 保险工作台：[Ocean Agent](https://clawhub.ai/skills/ocean-agent) — 保险代理人 AI 工作台
- MCP Server：[oceanbus-mcp-server](https://www.npmjs.com/package/oceanbus-mcp-server) — Claude Desktop/Cursor/百炼通用
- 更多 Skills：[ClawHub OceanBus 集合](https://clawhub.ai/skills?search=oceanbus)
- 平台集成：[Dify](https://github.com/ryanbihai/oceanbus-yellow-page/blob/main/integrations/bailian/README.md) · [Coze](https://www.coze.cn) · [百炼](https://github.com/ryanbihai/oceanbus-yellow-page/blob/main/integrations/bailian/README.md) · [MCP Registry](https://registry.modelcontextprotocol.io/v0.1/servers?search=oceanbus)

---

## AI Mode (v2.1+)

```
# AI host — fully automated game master
node game.js ai-host 9527 --players 4 --ai-count 1

# AI player — two-stage reasoning (strategize → speak)
node game.js ai-play 9527 --personality 推理迷
```

AI players use a Cicero-inspired two-stage architecture:
1. **Strategy reasoning** — analyze game state, choose from 5 strategies (blend in, deflect, play dumb, build case, counter-question)
2. **Natural generation** — generate human-like speech based on strategy + personality

5 AI personalities (推理迷/社恐/话痨/老实人/阴谋家) ensure diverse play styles.

Requires a configured LLM API key.

---
## Contribute / 参与开发

Guess AI is MIT-0 licensed. Welcome contributions!

- **GitHub**: [ryanbihai/guess-ai](https://github.com/ryanbihai/guess-ai)
- **Good first issues**: Web UI for non-CLI players, real-time message streaming, iOS/Android client
- **Tech deep-dive**: See `src/strategy-prompt.js` for two-stage AI prompts, `src/ai-host.js` for game loop

```bash
git clone https://github.com/ryanbihai/guess-ai.git
cd guess-ai && npm install
node game.js host 9527    # Start a test room locally
```

## License

MIT-0 — Free to use, modify, and redistribute.
