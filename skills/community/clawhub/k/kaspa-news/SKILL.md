---
name: kaspa-news
description: "Kaspa News — let your Claw know everything about Kaspa in one place: latest news, core development updates, ecosystem launches, community talks, and weekly reports summary. Use when someone asks what’s happening with Kaspa now, including dev/builder activity, top tweets, videos, and Reddit updates. No API keys needed."
metadata: {"clawdbot":{"requires":{"bins":["python3","jq"]}}}
---

# Kaspa News Skill

Query the public kaspa.news API for Kaspa ecosystem intelligence. No API keys needed.

## Quick Start

```bash
SCRIPT="~/.openclaw/workspace/skills/kaspa-news/scripts/kaspa-news.sh"

$SCRIPT focused           # Curated community tweets
$SCRIPT builders           # Ecosystem/builder tweets
$SCRIPT top                # Most viewed tweets
$SCRIPT developers         # Core dev tweets (includes replies)
$SCRIPT videos             # YouTube videos
$SCRIPT reddit             # r/kaspa posts
$SCRIPT pulse              # Latest AI pulse report
```

## Requirements

- `python3` with `requests` module
- `jq`
- Internet access to `https://kaspa.news/api`
- **No API keys, no tokens, no auth** — all endpoints are public

---

## Commands Reference

### `focused` — Curated Community Tweets
Community-curated tweets. Excludes replies. Best for "what's the Kaspa community talking about?"

```bash
$SCRIPT focused              # Latest 10
$SCRIPT focused -n 5         # Latest 5
$SCRIPT focused --since 12   # Last 12 hours only
```

### `builders` — Ecosystem/Builder Tweets
Projects building on Kaspa (labeled "Ecosystem" on kaspa.news frontend). Excludes replies.

```bash
$SCRIPT builders             # Latest 10
$SCRIPT builders -n 20       # Latest 20
```

### `top` — Highest Engagement Tweets
Sorted by view count (most views first). **This is the only command that shows view counts** (👁️).

```bash
$SCRIPT top                  # Top 10 by views
$SCRIPT top -n 3             # Top 3
```

### `developers` — Developer Tweets
Tweets from known Kaspa core developers. **Includes replies** (unlike other tweet commands). Shows dev discussions and technical debates.

The script has a built-in list of known dev usernames, but **this is only for the default `developers` command filter**. Per-user searches (see below) work for ANY username.

```bash
$SCRIPT developers           # Latest 10 dev tweets
$SCRIPT developers -n 15     # Latest 15
```

### `videos` — YouTube Videos
Latest Kaspa-related YouTube videos with view/like counts.

```bash
$SCRIPT videos               # Latest 10
$SCRIPT videos --since 48    # Last 2 days
```

### `reddit` — Reddit Posts
Latest posts from r/kaspa with upvote scores.

```bash
$SCRIPT reddit               # Latest 10
$SCRIPT reddit -n 5          # Latest 5
```

### `pulse` — AI Pulse Report
AI-generated intelligence report summarizing recent Kaspa ecosystem activity. Single latest report.

```bash
$SCRIPT pulse                # Latest report (text summary)
$SCRIPT pulse --sources      # With clickable source links to tweets
$SCRIPT pulse --json         # Full JSON (for custom parsing)
```

---

## Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `-n, --limit N` | Number of items to show | 10 |
| `--since HOURS` | Only items from last N hours | all |
| `--json` | Raw JSON output (for scripting/parsing) | off |
| `--sources` | Show source links in pulse reports | off |
| `-h, --help` | Show help text | — |

---

## Script Output Format

The script outputs **plain text**. Here's exactly what each command produces:

### Tweet Commands (focused, builders, developers)

```
🎯 Focused Tweets

📝 @DailyKaspa (1h)
Nearly $10 million in short positions are stacked around the 0.037 level...
[SOURCE](https://x.com/DailyKaspa/status/2024047412226978031)

💬 @KaspaHub (10h)
Better late than never, I guess.
[SOURCE](https://x.com/KaspaHub/status/2023918673216311580)

↩️ @hashdag (1h)
@asaefstroem @maxibitcat could be, not ruling that out...
[SOURCE](https://x.com/hashdag/status/2024050945718399078)
```

### Top Command (includes view counts)

```
🔥 Top Tweets

📝 @BSCNews (23h) — 👁️ 22179
🚨JUST IN: $KAS, $PI, $ASTER AMONG PROJECTS WITH MOST BULLISH SENTIMENT...
[SOURCE](https://x.com/BSCNews/status/2023709720901534048)

💬 @kaspaunchained (14h) — 👁️ 10663
Private messaging on Kaspa L1. Encrypted payloads riding the BlockDAG...
[SOURCE](https://x.com/kaspaunchained/status/2023845437577257447)
```

### Videos

```
📺 Kaspa Videos

📺 Kaspa Crypto Prediction | Why We Went Bearish?
  📡 Crypto MindSet | 👁️ 80 | ❤️ 3 | 6h
  🔗 https://youtube.com/watch?v=NgO5iW1B_t4
```

### Reddit

```
🟠 Kaspa Reddit

🟠 Did Fred Thiel Dump his Kaspa Bag?
  👤 u/Weekly-Fudge1909 | ⬆️ 10 | 2h
  🔗 https://reddit.com/r/kaspa/comments/1r7o9oi
```

### Pulse

```
📊 Kaspa Pulse Reports

[REPORT HERE](https://kaspa.news/pulse/d6167911-21ab-4135-bccb-a4baf4e4480f)

📊 From Silverscript to TangFi...
  🕐 13h | 🤖 gpt-5.2

  Silverscript compiler goes live on Testnet 12, delivering first high-level
  contract language for Kaspa...
```

---

## 🎨 PRESENTATION RULES (MANDATORY FOR ALL AGENTS)

The script outputs plain text. When you present this to a user, follow these rules **exactly**. This is the approved format — do not deviate.

### Tweet Type Emojis

| Emoji | Meaning |
|-------|---------|
| 📝 | Regular tweet |
| 💬 | Quote tweet (user's own comment only — NOT the quoted source tweet) |
| ↩️ | Reply |

### What the Script Already Does (don't redo these)
- ✅ Picks correct emoji (📝/💬/↩️)
- ✅ Shows relative time ("10h", "1d", "5m" — no "ago")
- ✅ Expands t.co links to real URLs
- ✅ Strips trailing t.co image links
- ✅ Decodes HTML entities (&amp; → &, &gt; → >)
- ✅ Truncates at 300 chars
- ✅ Adds [SOURCE](url) link on every tweet
- ✅ Shows 👁️ views ONLY on `top` command

### What YOU (the presenting agent) Must Do

#### X/Twitter Linkification
Convert plain text @handles, #hashtags, and $CASHTAGS into clickable links:

- `@username` → `[@username](https://x.com/username)` — links to X profile
- `#hashtag` → `[#hashtag](https://x.com/search?q=%23hashtag)` — links to X search
- `$KAS` → `[$KAS](https://x.com/search?q=%24KAS)` — links to X search

**Important:**
- Only linkify REAL handles/hashtags/cashtags
- `#2`, `#4`, `#10BPS` (numbers) are NOT hashtags — leave as-is
- `@` inside email addresses are NOT handles — leave as-is
- Link to **x.com** (NOT twitter.com, NOT Telegram)

#### Pulse Report Formatting
When presenting pulse reports, reformat the summary into grouped sections:

```
📊 **Latest Kaspa Pulse Report** (date)

**"Report Title Here"**

━━━ Core Development ━━━

🔧 **Silverscript** — First high-level smart contract language, live on TN12.

📐 **Covenants** — Enable programmable spending conditions on UTXO.

━━━ Ecosystem ━━━

💵 **TangFi** — Bridging stablecoins (USDT/USDC) to Kaspa L1.

🔐 **Private Messaging** — Encrypted payloads on BlockDAG at 10 BPS.

━━━ Milestones ━━━

📈 600M total transactions on Kaspa mainnet.
```

**Pulse formatting rules:**
- Group by category with `━━━ Category ━━━` separators
- Bold project/feature names
- One line per item, max 1-2 sentences
- Use emojis as bullet prefixes (🔧💵🔐💬🌉⚡🏦📊📈💎🎤📱)
- Key people to name: @hashdag (Yonatan Sompolinsky), @michaelsuttonil (Michael Sutton), @OriNewman (Ori Newman)

---

## 🔍 Per-User Tweet Search

When someone asks for tweets from a **specific person** (e.g., "show me @michaelsuttonil tweets from last 2 weeks"), this works for **ANY username** — not limited to the 9 built-in dev names.

### How to Query

Fetch ALL endpoints and merge (always go wide):

```bash
# Fetch all 4 tweet sources
$SCRIPT focused --json -n 999 > /tmp/focused.json
$SCRIPT builders --json -n 999 > /tmp/builders.json
$SCRIPT top --json -n 999 > /tmp/top.json
$SCRIPT developers --json -n 999 > /tmp/devs.json

# Merge, deduplicate by url, filter by username + date range (safe)
TARGET_USER="michaelsuttonil"
cat /tmp/*.json | jq -s --arg user "$TARGET_USER" 'add | unique_by(.url) | [.[] | select(.author_username == $user)]'
```

Or use the `--json` output and filter with jq/python inline.

**Security note:** never interpolate raw user input directly into jq programs. Always pass user values via `--arg` / `--argjson`.

### How to Present Per-User Results

Group by date (newest first). Standalone posts first, then replies.

```
📅 Feb 17 — Smart contracts and Silverscript progress

📝 @michaelsuttonil
Full tweet text here exactly as-is...
[SOURCE](https://x.com/michaelsuttonil/status/123)

💬 @michaelsuttonil
Quote comment here (user's own words only)...
[SOURCE](https://x.com/michaelsuttonil/status/456)

↩️ To @hashdag: "Reply text shown in quotes..."
[SOURCE](https://x.com/michaelsuttonil/status/789)

---

📅 Feb 16 — TN12 testing and validator discussion

📝 @michaelsuttonil
Another tweet...
[SOURCE](url)
```

**Per-user format rules:**
- `📅 Feb 17` date headers with em dash + brief theme summary
- `---` separator between date groups
- Standalone posts first (📝/💬), replies below (↩️)
- Replies: `↩️ To @recipient: "quoted reply text..."`
- Omit trivial replies ("100%", "sure", "thanks") unless notable
- End with brief editorial summary of themes across the period
- **Always search the FULL time range asked** — never shorten it
- **Show everything found** — don't pre-filter or narrow results

---

## ❌ DO NOT (hard rules)

These are locked rules. Violating any of these = wrong output.

| Rule | Why |
|------|-----|
| ❌ Don't edit, trim, rewrite, or summarize tweet text | Show user's exact words |
| ❌ Don't merge same-author tweets together | Every tweet is separate |
| ❌ Don't show the quoted tweet's source text | Quote tweets show ONLY the user's own comment |
| ❌ Don't show sentiment percentages (bullish/bearish %) | User explicitly forbids this |
| ❌ Don't show "N tweets analyzed" counts | User explicitly forbids this |
| ❌ Don't show model name in pulse output to users | Internal detail |
| ❌ Don't add bold to @usernames in tweet output | Script format is final |
| ❌ Don't add extra emojis or separator lines to tweets | Script format is final |
| ❌ Don't add "(latest N)" to section headers | Clean headers only |
| ❌ Don't add type labels like "— 📝 Tweet" after time | Emoji prefix is enough |
| ❌ Don't use markdown tables for tweets | Use the line-by-line format |
| ❌ Don't say "according to the pulse report" | Just present the info directly |
| ❌ Don't add engagement metrics (❤️/🔁) to any command except `top` | Only `top` shows 👁️ |
| ❌ Don't link @handles to Telegram | Always link to x.com |
| ❌ Don't strip [SOURCE] links | They're always shown |

---

## ✅ DO (best practices)

| Practice | Detail |
|----------|--------|
| ✅ Run the script, present its output | Don't fabricate or cache old data |
| ✅ Linkify @handles → x.com profiles | `[@user](https://x.com/user)` |
| ✅ Linkify #hashtags → x.com search | `[#kaspa](https://x.com/search?q=%23kaspa)` |
| ✅ Linkify $CASHTAGS → x.com search | `[$KAS](https://x.com/search?q=%24KAS)` |
| ✅ Group pulse reports by category | Use ━━━ separators |
| ✅ Bold project names in pulse | Makes scanning easy |
| ✅ Keep it scannable on mobile | Short lines, emojis, no walls of text |
| ✅ For per-user search: go wide | Search ALL endpoints, full time range |
| ✅ Use `--json` for custom filtering | Then format manually |

---

## Trigger Phrases

Use this skill when the user says anything like:
- "kaspa news", "what's happening in kaspa", "kaspa tweets"
- "kaspa pulse", "kaspa report", "kaspa update"
- "kaspa devs", "what are kaspa developers saying"
- "kaspa videos", "kaspa youtube"
- "kaspa reddit"
- "show me tweets from @someone" (per-user search)
- "top kaspa tweets", "trending kaspa"
- Any mention of kaspa.news

---

## Architecture Notes

- **API base**: `https://kaspa.news/api` (fixed; no env override)
- **API returns cached data** — query params like `?limit=` are ignored server-side
- **All filtering is client-side** — script fetches full dataset, filters with jq
- **No auth needed** — all endpoints are public, no API keys
- **No runtime env vars required**
- **Script outputs plain text** — the presenting agent handles linkification
- **FORMAT_LOCK.md** in the skill directory is the canonical format specification
