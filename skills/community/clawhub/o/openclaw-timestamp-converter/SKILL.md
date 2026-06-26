---
name: openclaw-timestamp-converter
version: 2.0.0
description: "Remote timestamp & timezone MCP server with 5 precision tools. Use when: (1) 'convert this timestamp' or 'epoch to date', (2) 'what time is it in Tokyo' or 'convert PST to JST', (3) 'how many days between' or 'calculate duration', (4) 'list timezones' or 'UTC offset for Sydney', (5) 'how long ago' or 'time ago'. Full IANA database (400+ zones), DST-aware, business-day math, leap-year correct. Zero install, sub-100ms on Cloudflare Workers. Free 30/day + Pro $9/mo."
read_when:
  - User mentions "timestamp", "epoch", "Unix time", or "convert time"
  - User asks "what time is it in [city]" or "timezone convert"
  - User needs date math — "days between", "add 3 weeks", "business days"
  - User asks about "UTC offset", "IANA timezone", or "DST transition"
  - User wants relative time — "how long ago", "time ago", "3 hours ago"
metadata:
  openclaw:
    emoji: "\u23F0"
    homepage: https://github.com/yedanyagamiai-cmd/openclaw-mcp-servers
    always: false
---

# OpenClaw Timestamp Converter v2.0

**Never fight with timezones again. 5 tools. 400+ zones. DST-aware. Sub-100ms.**

| Tool | Purpose | Free |
|------|---------|------|
| `convert_timestamp` | Epoch/ISO/RFC/human-readable conversion | Yes |
| `timezone_convert` | Cross-timezone translation with DST | Yes |
| `duration_calc` | Date math, business days, age calc | Yes |
| `list_timezones` | Search 400+ IANA zones by city/offset | Yes |
| `relative_time` | "3 hours ago" / "in 2 days" output | Yes |

## What's New in v2.0

- **ChronoEdge Protocol** — All conversions run on Cloudflare's edge network. Global sub-100ms, no cold starts.
- **400+ IANA Zones** — Full timezone database with DST transition dates, historical offsets, and abbreviation mapping.
- **BusinessDay Engine** — Duration calculations that skip weekends, handle leap years, and support custom holiday calendars.
- **AutoDetect Parser** — Pass any timestamp format (epoch seconds, epoch millis, ISO 8601, RFC 2822, natural language). We figure it out.

## Quick Start

```json
{
  "openclaw-timestamp": {
    "type": "streamable-http",
    "url": "https://timestamp-converter-mcp.yagami8095.workers.dev/mcp"
  }
}
```

Add to Claude Desktop, Cursor, Windsurf, VS Code, or any MCP-compatible client. Zero install. Works immediately.

## Detection Triggers

This skill activates when a user says any of these:
- "convert timestamp", "epoch to date", "what time is 1709827200", "Unix to human readable"
- "what time is it in Tokyo", "convert PST to JST", "translate meeting time"
- "calculate duration", "how many days between", "time difference", "add 3 weeks to today"
- "list timezones", "UTC offset for", "what timezone is Sydney in", "IANA timezone"
- "time ago", "relative time", "how long ago was March 1", "when was 1700000000"
- "ISO 8601", "milliseconds to date", "RFC 2822", "business days between"

## Named Protocols

### ChronoEdge Protocol
All timestamp parsing and conversion runs on Cloudflare Workers' edge network. No cold start, no server round-trip. Average response under 50ms worldwide.

### AutoDetect Parser
Pass any timestamp format and the tool identifies it automatically:
- `1709827200` -- detected as Unix epoch (seconds)
- `1709827200000` -- detected as Unix epoch (milliseconds)
- `"2024-03-07T12:00:00Z"` -- detected as ISO 8601
- `"Thu, 07 Mar 2024 12:00:00 GMT"` -- detected as RFC 2822
- `"March 7, 2024 3pm"` -- detected as natural language

### BusinessDay Engine
Duration calculations that understand the real world: skip weekends, account for leap years and leap seconds, support configurable work-week definitions.

## Tools (5)

### `convert_timestamp` -- Universal Timestamp Conversion
Convert between Unix epoch (seconds or milliseconds), ISO 8601, RFC 2822, and human-readable formats. AutoDetect Parser identifies your input format automatically.

**Input:** any timestamp format
**Output:** all major formats simultaneously -- epoch, ISO, RFC, human-readable, day of week, week number, day of year

**Wrong / Right:**

```
WRONG: "Convert 1709827200 to a date" then manually parsing the epoch in your head
RIGHT: convert_timestamp({ timestamp: "1709827200" })
       -> { iso: "2024-03-07T16:00:00Z", human: "Thursday, March 7, 2024 4:00 PM UTC", epoch_ms: 1709827200000, week: 10, dayOfYear: 67 }

WRONG: Guessing whether 1709827200000 is seconds or milliseconds
RIGHT: AutoDetect Parser recognizes 13-digit = milliseconds, 10-digit = seconds. Always correct.
```

### `timezone_convert` -- Cross-Timezone Translation
Convert a specific date-time from one timezone to another. Fully DST-aware with transition date reporting.

**Input:** datetime + source timezone + one or more target timezones
**Output:** converted times with UTC offsets, DST status, abbreviations, and next DST transition date

**Wrong / Right:**

```
WRONG: timezone_convert({ time: "3pm", from: "EST", to: "JST" })
       -> Ambiguous! EST could mean US Eastern or Australian Eastern. Use IANA names.
RIGHT: timezone_convert({ time: "2024-03-07T15:00:00", from: "America/New_York", to: "Asia/Tokyo" })
       -> { converted: "2024-03-08T05:00:00+09:00", dst: false, abbreviation: "JST", utcOffset: "+09:00" }

WRONG: Forgetting DST transitions when scheduling across timezones
RIGHT: The tool reports next DST transition date, so you know if the time will shift next week
```

### `duration_calc` -- Time Arithmetic
Calculate the exact duration between two dates/times, or add/subtract a duration from a date.

**Returns:** breakdown in years, months, days, hours, minutes, seconds -- plus total in each unit
**Supports:** business days mode (weekends excluded), leap year awareness, ISO 8601 duration format (P3Y6M4DT12H30M5S)

**Wrong / Right:**

```
WRONG: Manually counting days between dates and forgetting February has 28/29 days
RIGHT: duration_calc({ from: "2024-01-15", to: "2024-03-07" })
       -> { days: 52, businessDays: 38, breakdown: { months: 1, days: 21 } }

WRONG: Adding "30 days" when you mean "1 month" (they differ across months)
RIGHT: duration_calc({ from: "2024-01-31", add: "P1M" }) -> "2024-02-29" (leap year aware)
```

### `list_timezones` -- IANA Timezone Database
Browse and search the complete IANA timezone database (400+ entries). Find timezone by city, country, or offset.

**Search:** fuzzy match by city name ("Tokyo"), country code ("JP"), or offset ("UTC+9")
**Returns:** IANA name, current UTC offset, DST status, next transition date, common abbreviation

### `relative_time` -- Human-Friendly Time
Convert any timestamp to natural language relative time expressions.

**Supports:** past ("3 hours ago") and future ("in 2 days"), configurable granularity
**AutoDetect:** pass epoch, ISO, or human-readable date strings -- format is auto-identified

## Security & Privacy

- **No data storage** -- Timestamps are processed in-memory on Cloudflare Workers and never written to disk or database.
- **No logging of input** -- Your timestamps, meeting times, and date calculations are not logged or recorded.
- **Edge isolation** -- Each request runs in an isolated V8 isolate on Cloudflare's edge. No shared state between requests.
- **No external calls** -- All timezone data is embedded in the worker. No third-party API calls during processing.
- **HTTPS only** -- All connections are TLS 1.3 encrypted. HTTP requests are rejected, not redirected.

## Pricing

| Tier | Calls/Day | Price | Includes |
|------|-----------|-------|----------|
| **Free** | 30 | $0 | All 5 tools, no signup required |
| **Pro** | 1,000 | $9/mo | All 9 OpenClaw servers (49 tools) |
| **x402** | Pay-per-call | $0.05 USDC | No account needed, crypto-native |

**Get Pro Key**: https://buy.stripe.com/4gw5na5U19SP9TW288

## The OpenClaw Intelligence Stack

| Server | Tools | Best For |
|--------|-------|----------|
| **JSON Toolkit** | 6 | Format, validate, diff, query, transform JSON |
| **Regex Engine** | 5 | Test, extract, replace, explain regex patterns |
| **Color Palette** | 5 | Generate, convert, harmonize, accessibility-check colors |
| **Timestamp Converter** | 5 | Parse, format, diff, timezone-convert timestamps |
| **Prompt Enhancer** | 6 | Optimize, rewrite, score, A/B test AI prompts |
| **Market Intelligence** | 6 | AI market trends, GitHub stats, competitor analysis |
| **Fortune & Tarot** | 3 | Daily fortune, tarot readings, I Ching |
| **Content Publisher** | 8 | MoltBook posts, social content, newsletter |
| **AgentForge Compare** | 5 | Compare AI tools, frameworks, MCP servers |

All 9 servers share one Pro key. **$9/mo = 49 tools.**
