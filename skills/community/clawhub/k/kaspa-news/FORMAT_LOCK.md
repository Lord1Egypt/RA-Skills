# FORMAT_LOCK.md — DO NOT CHANGE THIS FORMAT

Approved by vyte on 2026-02-18. Match 1:1 for ALL commands. No additions, no removals, no "improvements".

## Tweet Format (all tweet commands: focused, builders, top, developers)

```
📝 @username (10h)
Full tweet text — user's own words only
[SOURCE](https://x.com/user/status/id)

💬 @username (10h)
User's own comment text only — NOT the quoted tweet's text
[SOURCE](https://x.com/user/status/id)
```

## Rules
- 📝 = regular tweet, 💬 = quote tweet
- Time: short format "10h", "1d", "5m" — NO "ago"
- Full tweet text, NOT summarized, NOT truncated (unless >300 chars)
- Quote tweets: show ONLY the user's own text (their comment). Do NOT show the source quoted tweet text
- Every tweet is separate — never merge/group by author
- SOURCE always shown as `[SOURCE](url)` — renders as clickable "SOURCE" in Telegram
- Strip trailing t.co image links
- Decode HTML entities (&gt; → >, &lt; → <)
- Section headers: title case with category emoji (🔨 Ecosystem Tweets)

## X Links (presentation layer — LLM does this when presenting)
- @handles → `[@handle](https://x.com/handle)` (X profile, NOT Telegram)
- #hashtags → `[#tag](https://x.com/search?q=%23tag)` (X search)
- $CASHTAGS → `[$KAS](https://x.com/search?q=%24KAS)` (X search)
- Only real hashtags — `#2`, `#4` are numbers, NOT hashtags
- Script output stays plain text. LLM adds links at presentation time.

## Per-User Tweet Search (e.g. "show me @michaelsuttonil tweets from last 2 weeks")

When someone asks for tweets from a specific username over a time period:

### How to query
Use ALL public tweet endpoints (go wide):
- `https://kaspa.news/api/developer-tweets`
- `https://kaspa.news/api/focused-tweets`
- `https://kaspa.news/api/builder-tweets`
- `https://kaspa.news/api/kaspa-tweets` (top/engagement feed)

Then:
- Merge and de-duplicate by tweet `id`
- Filter locally by `author.username` + `createdAt` range (jq/python)
- Always use the FULL time range asked — never shorten it
- Show everything found, don't pre-filter

### How to format
Group by date (newest first). Within each date, show standalone posts (📝/💬) first, then notable replies (↩️).

```
📅 Feb 17 — [short description of the day's themes]

📝 @username
Full tweet text...
[SOURCE](url)

💬 @username
Quote tweet text...
[SOURCE](url)

↩️ To @other_user: "Reply text shown in quotes..."
[SOURCE](url)

---

📅 Feb 16 — [description]

📝 @username
...
```

### Rules
- `📅 Feb 17` date headers with em dash + brief theme summary
- `---` separator between date groups
- Standalone posts first (📝/💬), replies below (↩️)
- Replies: `↩️ To @recipient: "quoted reply text..."` — shows who they're replying to
- Replies with just context/people mentioned: `↩️ On [topic] with @user: "text..."`
- Short/trivial replies (e.g. "100%", "Perfect", "sure") can be omitted unless they're funny or notable
- At the end, add a brief editorial summary of the arc/themes across the period
- X linkification still applies (LLM adds @handle, #tag, $CASHTAG links)

## DO NOT
- EDIT, TRIM, SHORTEN, OR REWRITE tweet text — show it EXACTLY as the script outputs it
- Summarize tweets into one-liners
- Add bold formatting to usernames
- Change emoji positions or add extra emojis
- Add separator lines (━━━)
- Add "(latest N)" to headers
- Show the quoted tweet's source text
- Merge same-author tweets together
- Add type labels like "— 📝 Tweet" after the time
- Strip or modify the full tweet text
