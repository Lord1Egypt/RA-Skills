---
name: politicians-stock-tracker
description: "Track congress stock trades and politician stock trades: Pelosi tracker, senate stock trades, House trades, congress trades by ticker, and STOCK Act disclosures sourced from House Clerk and Senate eFD filings. Use for congress stock trades, politician stock tracker, Pelosi stock trades, senate trading disclosures, what stocks is congress buying, STOCK Act filings by ticker. Read-only. No trading, no purchases, no write operations, no wallet access."
homepage: https://sentisense.ai
primaryEnv: SENTISENSE_API_KEY
metadata:
  openclaw:
    primaryEnv: SENTISENSE_API_KEY
    envVars:
      - name: SENTISENSE_API_KEY
        required: false
        description: "SentiSense API key, optional to install. Get one free at https://app.sentisense.ai/get-api-key, or with no key follow the No key yet steps in the 0-sentisense-onboarding skill for a temporary free one with no signup. Used only to authenticate read-only data calls; no write or trading scope."
---
# Politicians Stock Tracker (SentiSense)

Track what the U.S. Congress is buying and selling. This skill reads congressional STOCK Act disclosures, the trades that Senators and Representatives are legally required to report, through the read-only SentiSense API: recent trades across all members, the trading history for a single stock, the most active politicians, and a full per-member profile. Amounts, chambers, parties, and the gap between when a trade happened and when it was disclosed all come straight from the official filings.

Read-only educational data interface. Output is informational context, never a personalized buy or sell recommendation.

## When to Use

Reach for this skill when the question is about congressional or political trading activity:

- "What did Congress buy this week?" or "recent congressional stock trades"
- "Has any senator or representative traded $NVDA?" (per-ticker congressional history)
- "Show me Nancy Pelosi's stock trades" or any single member's activity
- "Which politicians trade the most?" (most active members by trade count)
- "Did a politician disclose a buy right before the stock moved?" (disclosure-delay context)

This skill pairs naturally with `institutional-13f-tracker` and `insider-trading-tracker`: cross-reference a congressional buy against institutional 13F accumulation or insider Form 4 buying on the same ticker. High-conviction reads come from convergence across sources, not from any one signal in isolation.

Do not use it for order entry, portfolio management, or personalized advice. It has no write, trading, or wallet surface; every endpoint is a GET.

## What this data actually is (read before interpreting)

- **Amounts are ranges, not exact values.** STOCK Act filings disclose a dollar band (for example "$1,001 - $15,000"). The API returns the raw `amountRange` string plus parsed `amountMin` / `amountMax`. Never present a single precise dollar figure.
- **"Recent" means recently disclosed, not recently traded.** The law asks for a filing within 45 days of the transaction, but late filings exist and some trail the trade by months or more, so read `disclosureDelayDays` on every row rather than assuming a ceiling. Each trade carries both `transactionDate` and `disclosureDate`, plus `disclosureDelayDays`. Always state which date you are quoting.
- **Chambers are `SENATE` and `HOUSE`.** Each trade also carries `party` (a word, such as `Republican` or `Democrat`), `state`, and `owner`, the filing's own text for whose account it was. Values seen include an empty string and `Self` (both the member), `Spouse`, `Joint` (the member with a spouse) and `Dependent`.
- **Source:** official House Clerk and Senate eFD filings, updated daily.

## Prerequisites

- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. Send it on every call: a request without a valid key gets at most a shaped crawler-facing preview slice, never the dataset, and that fallback is not a contract you can build on. No key yet? Follow "No key yet" in the `0-sentisense-onboarding` skill: one POST returns a temporary free key the agent can use right away and a link the user opens to keep it.
- Any HTTP client. Plain `curl` works, or Python 3.8+ using only the standard library (`urllib`, `json`); no third-party packages required. On macOS python.org installs can raise `CERTIFICATE_VERIFY_FAILED` (missing CA certs): run the bundled `Install Certificates.command`, use the system `/usr/bin/python3`, or use `curl`.
- Network access to `https://app.sentisense.ai`.
- Read-only scope. Every endpoint here is a GET. Nothing this skill does can place a trade, move money, or modify account state.

| Tier | Quota | Rate | Congressional data |
|------|-------|------|--------------------|
| Free | 1,000 requests/month | 30 requests/min | preview slice (top N per endpoint) |
| PRO ($15/mo) | Unlimited | 300 requests/min | full history and full lists |

A free key runs every workflow below at preview depth: preview-gated endpoints return the newest or most active few rows of a real response, and `totalCount` gives the size of the whole window. The member lookup in workflow 3 goes through `/politicians/directory`, which a free key gets in full.

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: none required.
- Files: none.

## How to Run

The REST recipe in this file is the primary path. A maintained command-line client is available as the separate `sentisense-cli` skill for hosts that prefer one.

Issue HTTP GET requests to `https://app.sentisense.ai` and synthesize the JSON into a concise, sourced answer. Authenticate every request with the `X-SentiSense-API-Key` header; keep the key in the shell environment and never place it in a query string or in user-facing output.

The politician endpoints return the wrapped envelope `{ isPreview, previewReason, data }`. For `/activity`, `/filings/{ticker}`, and `/members`, `.data` is a **list**; for `/member/{slug}`, `.data` is an **object** `{ profile, recentTrades, topTickers }` (read those keys, do not iterate it as a list). When `isPreview` is true, say so ("showing the free preview slice").

**A preview is a slice, not the window.** When `isPreview` is true and `totalCount` is larger than the rows returned, the rows are the newest (or most active) few of `totalCount`. Label them that way ("newest 5 of 80 disclosures, free preview"), never tally them as the window, and never infer absence from them: five rows with no purchase is not "Congress did not buy". A free key is never served rows past the preview: on `/activity` and `/member/{slug}` an `offset` at or beyond 5 returns an empty page with `isPreview` true, so do not page on a free key; report `totalCount` as the window size and the rows as the preview. A free request whose `limit` fits inside the preview (5 or fewer) comes back with `isPreview: false`, yet it is still only the head of the window, so compare `totalCount` with the rows you hold rather than trusting the flag alone.

A rate-limited call returns `429` with a `Retry-After` header; back off for the indicated seconds rather than serving a stale value.

```python
rows = raw.get("data", []) if isinstance(raw, dict) else raw
```

## Endpoints

- **`GET /api/v1/politicians/activity`** : recent congressional trades across all members, sorted by disclosure date (most recently disclosed first). Query `lookbackDays` (1-365, default 90) to control the window. Free: the newest 5 rows of the window; PRO: pages the whole window. **This feed is paged**: query `limit` (default 200, max 500; above 500 is clamped) and `offset`, and read `totalCount` for the size of the whole window. `totalCount` sits on the envelope next to `isPreview`, not inside `data`, and on PRO `offset + data.length < totalCount` means another page is waiting (on a free key it never does; see the preview rule above). One call is one page, not the window: a 30-day window runs to several hundred trades and a full year to several thousand, so page any window wider than about a week before counting, ranking or saying who traded what. Each trade: `politicianName`, `firstName`, `lastName`, `chamber`, `party`, `state`, `bioguideId`, `imageUrl`, `ticker`, `assetDescription`, `assetType` (`Stock`, `ETF`, or `Stock Option`), `assetMetadata` (`null`, or `{kind:"OPTION", optionType, strikePrice, expirationDate}`), `transactionType` (`PURCHASE` / `SALE` / `EXCHANGE` / `OTHER`), `transactionDate`, `disclosureDate`, `disclosureDelayDays`, `amountRange`, `amountMin`, `amountMax`, `owner`, `urlSlug`. `amountMin` and `amountMax` can be null on the odd row whose band did not parse; quote the raw `amountRange` there and sort it last.
- **`GET /api/v1/politicians/filings/{ticker}`** : congressional trades for one stock, most recently disclosed first. Query `lookbackDays` (1-365, default 90) to set the window. Free: the newest 3 rows plus `totalCount` for the whole window; PRO: the full list in one response, not paged.
- **`GET /api/v1/politicians/members`** : current members of Congress with trading summaries, sorted by total trade count. Free: the 5 most active members plus `totalCount`; PRO: the full list in one response. This answers "who trades the most"; it is not a name lookup on a free key, because almost every member sits outside its top 5. Use the returned `urlSlug` to drill into a member.
- **`GET /api/v1/politicians/directory`** : every tracked member of Congress and the `urlSlug` that identifies them, including members who have left (`former: true`, `servedUntil`). Query `q` (case-insensitive match on name, state or slug), `limit` (default 50, max 200) and `offset`. Summary only, no trade data. Not tier-gated, so a free key gets the same full response as PRO, and it does not count against the monthly quota. Response: `{ isPreview, previewReason, data: { members, totalCount } }` (here `totalCount` sits inside `data`); each member carries `urlSlug`, `displayName`, `chamber`, `party`, `state`. This is the way to turn a name into a slug on any tier.
- **`GET /api/v1/politicians/member/{slug}`** : one politician's profile: summary stats, recent trades, and top tickers. Free: the full `profile` and `topTickers`, but only the newest 5 `recentTrades`; PRO: full detail. `recentTrades` is one page, newest transaction first: query `limit` (default 200, max 500) and `offset` to walk it, and read `totalCount` for the size of the whole history. `totalCount` sits on the envelope next to `isPreview`, not inside `data`. On PRO most members fit in one default page, so the default request usually returns their complete history. Check `totalCount` before you summarize anyway, because the tail is extreme: a few dozen members exceed one page and the heaviest single filer has disclosed over twelve thousand trades. `profile` and `topTickers` describe the whole history whatever page you request, on either tier.

## Workflows

**1. This week's congressional trades**

**Identify your client.** Send a `User-Agent` naming your agent runtime and this skill, for
example `OpenClaw/1.4 (politicians-stock-tracker)` or `ClaudeCode/2.1 (politicians-stock-tracker)`. Substitute your own runtime and
version if neither matches. You can also volunteer what your agent is called by adding an
`agent/<your-agent-name>` token inside the same parentheses, as in
`OpenClaw/1.4 (politicians-stock-tracker; agent/research-desk)`. All of it is optional, and it is what tells
us this skill has real integrations behind it, so it gets prioritized and you get notice before it
changes.

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/politicians/activity?lookbackDays=7"
```

**Output template:**
```
CONGRESS · LAST {days}d · {n} disclosures
─────────────────────────────────────────
{transactionDate}  {member} ({party}-{state})  {ticker}  {PURCHASE|SALE}  {amountRange}  +{disclosureDelayDays}d
{transactionDate}  {member} ({party}-{state})  {ticker}  {PURCHASE|SALE}  {amountRange}  +{disclosureDelayDays}d

MOST ACTIVE  {member} ({trades})   MOST TRADED  {ticker} ({trades})
```

Order the rows by the top of the `amountRange` band, largest first, and keep the delay column on every row. `party` arrives as a word, so shorten it to its initial for the `{party}-{state}` column. The two footer counts are tallied from the rows you actually received, so say how many that was rather than implying the whole week; on a free key that is the newest 5 of `totalCount`, so print the header as "newest 5 of {totalCount} disclosures (free preview)" and leave the footer tallies out.

**2. Has Congress traded a specific stock?**

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/politicians/filings/NVDA"
```
Report purchases vs sales (`transactionType`), which members and parties, and the transaction-to-disclosure gap.

**3. A specific politician's activity**

```bash
# resolve the name to a slug (works in full on a free key; read data.members[].urlSlug)
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/politicians/directory?q=pelosi"
# then pull their profile and history
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/politicians/member/{slug}"
```

When `q` matches more than one member, pick by `displayName`, `chamber` and `state`, or ask. On PRO, compare `totalCount` with `recentTrades.length` and page with `offset` when the history runs past one page. On a free key the profile and `topTickers` are whole but `recentTrades` is the newest 5 of `totalCount`: report the profile totals and top tickers as the full picture, and the trades as "newest 5 of {totalCount}". For "which politicians trade the most", use `/politicians/members` instead, which ranks by trade count (top 5 on a free key).

**4. Follow the convergence.** When a congressional buy lines up with institutional 13F accumulation (`institutional-13f-tracker`) or insider buying (`insider-trading-tracker`) on the same ticker, that agreement is the signal worth surfacing. Say so explicitly and cite each source.

## Answering well

- Always distinguish `transactionDate` (when they traded) from `disclosureDate` (when it was reported), and mention the delay.
- Quote the `amountRange` band, never a single invented number.
- Attribute party, chamber, and state; flag when `owner` is `Spouse`, `Joint` or `Dependent` rather than the member alone (an empty `owner` and `Self` both mean the member).
- Report only what the API returns. Do not infer trades, amounts, or motives that are not in the data, and do not frame any of it as advice. This is public-disclosure data presented for education.

## Going further

Free covers every workflow above at a preview depth. **PRO ($15/mo)** lifts the monthly cap (no monthly limit, just a 300/min rate) and returns full congressional history and full member lists, plus institutional flows, insider detail, and AI insights across the SentiSense API. Apply coupon `AGENTS` at checkout for a builder launch discount: https://app.sentisense.ai/pricing?coupon=AGENTS

For the full REST reference on every endpoint this skill touches, install the `sentisense` skill; for the complete CLI command set, install `sentisense-cli`.

**ClawHub Skill:** [clawhub.ai/TheSentiTrader/politicians-stock-tracker](https://clawhub.ai/TheSentiTrader/politicians-stock-tracker)

---

*SentiSense is a read-only financial intelligence API. This data is for informational and educational purposes only, not investment advice.*
