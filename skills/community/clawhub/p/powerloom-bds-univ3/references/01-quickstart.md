# Quickstart (~10 minutes)

1. **Get an API key** — **CLI / API:** metering origin [bds-metering.powerloom.io](https://bds-metering.powerloom.io) (`bds-agent signup`; see [agent guide](https://github.com/powerloom/bds-agent-py/blob/main/docs/USER_GUIDE.md)). **Browser:** signup and top-ups at [bds-metering.powerloom.io/metering](https://bds-metering.powerloom.io/metering).
2. **Export** `POWERLOOM_API_KEY=sk_live_...` in the environment OpenClaw uses (or your shell profile).
3. **Optional** — default MCP URL is `https://bds-mcp.powerloom.io/sse`. Override with `POWERLOOM_MCP_URL` if directed.
4. **Check credits**: `node scripts/ensure-credits.mjs` — should print balance JSON and exit 0.
5. **OpenClaw / cron** — for **one-shot schedulers** (recommended), use **`node scripts/whale-cron.mjs`** and the full copy-paste flow in **`references/08-openclaw-one-shot.md`**. For a **fixed pool list** and local poll loop, use **`whale-radar.mjs`** (per-pool snapshots only).
6. **Run a recipe** (stdout first):
   - Whale cron (bounded, all pools): `node scripts/whale-cron.mjs`
   - Whale Radar (fixed pools, poll): `node scripts/whale-radar.mjs`
   - Token-Flow: `node scripts/token-flow.mjs`
   - DeFi Analyst (one round, cron): `node scripts/defi-analyst.mjs`
7. **Telegram** — set `POWERLOOM_TELEGRAM_BOT_TOKEN` and `POWERLOOM_TELEGRAM_CHAT_ID`, set `dispatch.channel` to `telegram` in the recipe yaml.
