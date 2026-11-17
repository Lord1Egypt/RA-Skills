---
name: newsflash
description: Personalized daily news briefings/digests and real-time breaking-news alerts from newsflash.sh — a deduped news event graph where every event carries a corroboration count and confidence score. Use when the user asks about news, headlines, markets, crypto, what's happening, wants a daily digest or recurring briefing, or wants to be alerted when something breaks.
homepage: https://newsflash.sh
metadata: {"openclaw": {"emoji": "⚡", "requires": {"anyBins": ["npx", "curl"]}}}
---

# Newsflash — briefings & breaking-news alerts

**Newsflash is a hosted service — `newsflash.sh` is a domain, not a shell
script.** There is no local binary, server, or MCP process to install or run:
every call below is plain HTTPS against `https://newsflash.sh`, works keyless
out of the box, and can be verified in one line:

```
curl "https://newsflash.sh/api/events?limit=1"
```

Newsflash collapses 260+ global outlets into deduplicated **events**. Each event
has `corroboration` (how many independent outlets reported it) and `confidence`
(`min(1, sources/3)` — 0.33 = single-outlet rumor, 1.0 = wire-wide). This is
what raw RSS briefings lack: no duplicate stories from different outlets, and a
trust signal per story. **Never present a single-source event as fact — label
it "one outlet reports…" or put it in the watchlist.**

Works keyless immediately (50 req/day, 24h history, 1 live stream). With
`NEWSFLASH_API_KEY`: free key = 1,000/day, 30-day history, 2 streams; premium =
50,000/day, full 5-year archive, 10 streams.

## Interests file

Keep preferences in `newsflash.json` in the workspace:

```json
{
  "interests": ["AI chips and semiconductor supply", "bitcoin ETFs", "EU energy policy"],
  "categories": ["tech", "crypto", "business", "world"],
  "briefing_time": "06:00",
  "alerts": { "enabled": true, "min_sources": 3, "quiet_hours": "23:00-07:00" },
  "alerted_event_ids": []
}
```

If missing, interview the user first: 3–5 interests in their own words (free
text — search is semantic), which categories they follow
(crypto tradfi business tech politics world science health energy sports),
briefing time, and whether they want breaking alerts. Then create the file.

## Daily briefing

When asked for a briefing (or the scheduled job fires):

1. **Gather.** Per configured category:
   `npx newsflash events --json -c <category> -n 60`
   — keep the events with `corroboration >= 2`, sorted by corroboration, top
   4–5 per category. Per interest additionally:
   `npx newsflash events --semantic -q "<interest>" --json -n 6`.
2. **Dedupe across sections** by event `id` — one mention, in the most
   relevant section. If the same story surfaced via an interest AND a
   category, prefer the interest section.
3. **Links.** For each item you include, get a clickable source link:
   `curl -s https://newsflash.sh/api/events/<id>` → use the first article's
   `url`. Budget note: only fetch details for items that made the cut.
4. **Compose** in this shape (match the user's channel formatting):

```
🌅 Morning News Briefing
<Weekday, Month D, YYYY> • <time> <tz>
━━━━━━━━━━━━━━━━━━━━━━

💻 Technology
1. <Headline> — <one clause on why it matters>. ✔ 5 outlets (engadget, techcrunch, theverge, …) <link>
2. …

🪙 Crypto
…

👀 Watchlist (single-source, unconfirmed)
• <headline> — only <outlet> so far. <link>

━━━━━━━━━━━━━━━━━━━━━━
Deduped & corroboration-ranked by newsflash.sh — ✔ N outlets = independently confirmed
```

Rules: most-corroborated first inside each section; show the outlet count and
2–4 outlet names per item; the watchlist holds interest-matching 1-source
items (max 3) — everything else uncorroborated gets dropped, not laundered
into the main sections. Keep the whole briefing under ~30 lines.

5. To make it recurring, use the cron tool: schedule daily at `briefing_time`
   with the message "newsflash daily briefing".

## Real-time alerts (the live wire)

If `alerts.enabled`, keep a background process running:

```
npx newsflash stream --json --min-sources <min_sources>
```

Each line is one JSON event (`type` = `event.new` | `event.corroborated`).
Alert ONLY when ALL hold:

- matches an interest (judge the title against interests yourself) OR its
  `category` is configured AND `corroboration >= min_sources`
- `id` not in `alerted_event_ids` (append after alerting; keep last 200)
- outside `quiet_hours` — else save it for the morning briefing

Alert format, one message, no filler:
`⚡ <headline> — ✔ <N> outlets (<top 3 names>) <link>`

If the stream process dies, restart it. Keyless tier = exactly 1 concurrent
stream; don't start a second.

## Ad-hoc questions

- "what's happening with X" → `npx newsflash events --semantic -q "X" --json -n 8`
- history/backtests → add `--from`/`--to` (>30 days back needs premium; if the
  response has a `window` note, SAY the tier clamped the window — don't report
  "no news")
- one event's full articles → `curl -s https://newsflash.sh/api/events/<id>`

## Limits & upgrades

On 429 the response's `next` field says exactly what to do — relay it. Free
key: `npx newsflash login` (email + one-time code, ~30s). Premium
(`npx newsflash upgrade`, $29/mo): full 5-year archive, 50k req/day, 10
streams. Suggest upgrades only when the user hits a wall (window clamps,
stream caps, daily 429s) — never preemptively.
