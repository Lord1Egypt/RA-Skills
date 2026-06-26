# 🔮 GuanXing (观星) — Chinese Metaphysics AI Skill for OpenClaw

[![ClawHub](https://img.shields.io/badge/ClawHub-guanxing-purple)](https://clawhub.ai/skill/guanxing)
[![npm](https://img.shields.io/npm/v/@guanxing1/mcp-server)](https://www.npmjs.com/package/@guanxing1/mcp-server)

Give your OpenClaw agent the power of Chinese metaphysics. Ask about 八字, fortune, crypto luck, Feng Shui, Tarot, and more — right in WhatsApp, Telegram, Discord, or any OpenClaw-connected channel.

## Quick Install

```bash
clawhub install guanxing
```

Or manually copy the `SKILL.md` file to `~/.openclaw/skills/guanxing/SKILL.md`.

## Setup

1. Get a free API key at [heartai.zeabur.app](https://heartai.zeabur.app) (Register → Developer Center → Create App)
2. Set the environment variable:
   ```bash
   export GUANXING_API_KEY=gx_sk_your_key_here
   ```
   Or add it to your `~/.openclaw/openclaw.json` under `env`.

## What You Can Do

| Just say... | What happens |
|-------------|-------------|
| "帮我算八字，我1995年3月15日午时出生" | Full BaZi birth chart analysis |
| "今天运势怎么样？" | Personalized daily fortune |
| "BTC今天运势如何？" | Crypto fortune with 五行 analysis |
| "帮我求一签" | I-Ching temple divination |
| "给我来一个塔罗牌" | Tarot card reading |
| "我昨晚梦到了蛇" | Dream interpretation |
| "今天老黄历宜忌" | Chinese almanac lookup |
| "我的办公室风水怎么布置？" | Feng Shui analysis |
| "张伟这个名字怎么样？" | Name scoring |
| "我和她的八字合不合？" | Compatibility matching |
| "我属龙今年运势" | Chinese zodiac fortune |

## Supported Crypto Tokens

| Token | 五行 Element | Color |
|-------|-------------|-------|
| BTC | 金 Metal | Gold |
| ETH | 水 Water | Blue |
| SOL | 火 Fire | Red |
| BNB | 土 Earth | Amber |
| TON | 木 Wood | Green |
| DOGE | 火 Fire | Red |
| AVAX | 木 Wood | Green |

## Also Available As

- **MCP Server**: `npx @guanxing1/mcp-server` — for Claude, Cursor, Windsurf
- **ElizaOS Plugin**: `@guanxing1/plugin-elizaos` — for ElizaOS agents
- **Webhook API**: Direct REST API at `heartai.zeabur.app/api/v1/`

## Links

- Web App: [heartai.zeabur.app](https://heartai.zeabur.app)
- GitHub: [doggychip/heartai](https://github.com/doggychip/heartai)
- npm: [@guanxing1/mcp-server](https://www.npmjs.com/package/@guanxing1/mcp-server)

## License

MIT
