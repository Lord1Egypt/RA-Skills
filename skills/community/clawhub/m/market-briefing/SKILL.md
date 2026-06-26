---
name: market-briefing
description: Scheduled market intelligence briefing workflow for A-shares, HK stocks, US markets, macro policy, and geopolitical news. Activate when: (1) running as a cron/scheduled job to push hourly market updates, (2) user asks to collect or summarize market news, (3) user mentions A股, 港股, 恒指, 特朗普, 地缘政治, 军事, or related investing topics. Delivers time-aware briefings (morning/intraday incremental/closing) with deduplication. Uses Tavily Search via mcporter + web_fetch fallback, delivers via Feishu message tool. NOT for: deep financial modeling, backtesting, or individual stock analysis unrelated to news collection.
---

# Market Briefing

Time-aware market intelligence workflow. Detects current time → selects briefing mode → searches news → deduplicates → delivers via Feishu.

## Prerequisites

- `mcporter` CLI with `tavily-remote-mcp` MCP server configured
- Feishu `message` tool available
- Workspace `memory/` directory writable

## Step 1 — Detect Time & Select Mode

Get current Beijing time and select mode:

| Time | Mode |
|---|---|
| 09:00 | **Morning briefing** — overnight US markets + today's investment direction |
| 10:00–15:00 | **Incremental update** — new items only, skip duplicates |
| 16:00 | **Closing daily report** — full-day recap + tomorrow's outlook |

## Step 2 — Read Today's Dedup Log

```bash
cat /path/to/your/workspace/memory/reported-news-$(date +%Y-%m-%d).txt 2>/dev/null || echo "First run today"
```

> ⚠️ **Use absolute paths, not `~`**: cron jobs run in an isolated environment where `~` may expand to an unexpected home directory. Always use the full absolute path to your workspace (e.g. `/Users/yourname/.openclaw/workspace-invest/memory/`).

This file contains summaries of already-pushed items. Use it to filter duplicates in Step 4.

## Step 3 — Search Latest News

Run all 6 searches sequentially (Tavily rate limits make parallel risky):

```bash
mcporter call tavily-remote-mcp.tavily_search query="A股 今日行情 最新" time_range=day
mcporter call tavily-remote-mcp.tavily_search query="港股 恒生指数 今日" time_range=day
mcporter call tavily-remote-mcp.tavily_search query="特朗普 最新动态" time_range=day
mcporter call tavily-remote-mcp.tavily_search query="中国军事 地缘政治 最新" time_range=day
mcporter call tavily-remote-mcp.tavily_search query="美股 道指 纳指 标普 最新" time_range=day
mcporter call tavily-remote-mcp.tavily_search query="中国经济政策 最新" time_range=day
```

Supplement with `web_fetch` for real-time data:
- `https://www.cls.cn/telegraph` — 财联社电报
- `https://www.jin10.com/` — 金十数据

## Step 4 — Deduplicate

Compare results against Step 2 log. Skip items where core facts/keywords overlap >70% with already-reported items. Only keep genuinely new information.

If running incremental mode (10:00–15:00) and nothing new: reply `「本时段暂无重要增量信息，市场平稳运行中。」` and skip delivery.

## Step 5 — Compose Briefing by Mode

See `references/briefing-template.md` for full format templates. Summary:

**Morning (09:00):** Overnight US markets → key overnight news → today's investment direction (sectors to watch, risks, 1–2 stock references)

**Incremental (10:00–15:00):** Only new items, grouped by category (A股/港股/特朗普政策/军事地缘). No repeats.

**Closing (16:00):** Full-day recap for A股+港股+US markets + Trump/policy/military summaries → tomorrow's outlook with 2–3 stock references.

## Step 6 — Update Dedup Log

Append pushed items to the log (one line per item):

```bash
# Use absolute path — avoid ~ in cron environments
echo "[HH:MM] 消息摘要（30字以内）" >> /path/to/workspace/memory/reported-news-$(date +%Y-%m-%d).txt
```

## Step 7 — Deliver via Feishu

Send to the configured Feishu target using the `message` tool. Target is either a direct user or a group chat — configure in your workspace `MEMORY.md` or `TOOLS.md`.

```
channel: feishu
target: chat:<chat_id>   # or omit for default DM
message: <briefing content>
```

## Configuration

| Setting | Where | Notes |
|---|---|---|
| Feishu target chat | workspace `MEMORY.md` | Group chat ID or omit for DM |
| Topics / search queries | `references/topics.md` | Add/remove/translate topics |
| Briefing templates | `references/briefing-template.md` | Format per mode |
| Schedule | `openclaw cron add` | Recommended: `cron 0 9-16 * * 1-5` (Asia/Shanghai) |

## Fallback

If `mcporter` / Tavily unavailable, use `web_fetch`:
- `https://finance.sina.com.cn` — A股
- `https://www.aastocks.com` — 港股
- `https://www.caixin.com` — 宏观/政策

## Notes

- Never include personal portfolio holdings or account tokens in shared configs.
- All content is for reference only; does not constitute investment advice (⚠️ always append disclaimer).
