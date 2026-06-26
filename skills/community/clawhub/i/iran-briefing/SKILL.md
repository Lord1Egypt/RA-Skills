---
name: iran-briefing
description: Real-time geopolitical intelligence — Iran crisis briefing, Trump Truth Social feed, prediction markets, 800+ tracked entities.
metadata: {"openclaw":{"emoji":"🇮🇷","requires":{},"api_path":"iran"}}
user-invocable: true
---

# Capduck Intelligence — Decision Support Skill

## When to use

- **Iran:** conflict, US-Iran tensions, Israel-Iran, Middle East geopolitics, oil/Hormuz, prediction markets, IRGC, IDF, ceasefire
- **Trump:** Truth Social posts, trade/tariff policy, Iran-war signals, energy, China, executive orders

## Base URL

```
https://skill.capduck.com/{topic}/{feed}
```

Available topics: `iran`, `trump`

## How to think — the decision loop

**Always start from the briefing. Let the data guide your next call.** Do NOT call all endpoints.

### Step 1: Assess — get the big picture

```
curl -s "https://skill.capduck.com/iran"
```

The briefing contains situation assessment (tension 1-10, direction, key deltas), perspective summaries (with evidence strength), active threads (with signals and drill-down hints), and top events (impact >= 8, last 24h). Each section tells you where to look next.

### Step 2: Investigate — follow the scent

- A thread mentions linked events -> `/events?category=CONFLICT` to read the evidence chain
- A claim has weak evidence -> `/posts?source_type=osint` to see if OSINT confirms
- Mainstream narrative unclear -> `/news?region=us` to see how US outlets frame it
- A thread links to prediction markets -> `/polymarket` for probability and trend
- Trump posted about Iran -> `/trump?tags=iran-war` to see his exact words

### Step 3: Cross-reference — triangulate

- Compare official sources vs OSINT vs mainstream: `/posts?source_type=state_media` vs `osint` vs `/news`
- Use `/notable` to understand who a source is and which camp they belong to
- Use `/entities?q=name` to check credibility of an unfamiliar source
- Check `source_count` in events — 1 source = rumor, 5+ sources = confirmed
- Use `/signals?ids=id1,id2` to batch-lookup raw data for thread signals

### Step 4: Project — what happens next

- Look at **Watch** items in Active Threads: likelihood direction (rising/stable/falling), next milestones, decision makers
- Check `/polymarket` for market-implied probabilities and trend direction
- When polymarket diverges from briefing assessment, one of them is wrong — that's where investigation value is highest

---

## Iran Endpoints

All paths below are relative to `https://skill.capduck.com`.

### `/{topic}` — Briefing (default)

AI-generated situation briefing, updated hourly. Contains:
- **Situation Assessment** — tension level (1-10), direction, 24h comparison, key deltas
- **Perspective Summaries** — 4 viewpoints with evidence strength (strong/moderate/weak)
- **Active Threads** — 3-5 issue threads with linked signals, watch items, polymarket refs
- **Top Events** — impact >= 8 from last 24h, with source attribution

### `/{topic}/events` — Event timeline

Structured events with impact scoring and multi-source attribution.

| Param | Description | Default |
|-------|-------------|---------|
| `impact` | Minimum impact score (1-10) | 0 |
| `category` | CONFLICT, DIPLOMACY, POLITICS, ECONOMY, PROTESTS | all |
| `hours` | Rolling window in hours | 48 |
| `since` | ISO 8601 timestamp (overrides hours) | — |
| `limit` | Max results | 50 |

Each event includes: `id`, `impact`, `confidence`, `sentiment`, `category`, `title` / `title_zh`, `summary` / `summary_zh`, `source_details[]` (with `display_name`, `entity_slug`, `platform`, `url`), `source_count`, `published_at`.

### `/{topic}/posts` — Social feed

Unified Twitter + Telegram posts with entity enrichment.

| Param | Description | Default |
|-------|-------------|---------|
| `source_type` | news_agency, state_media, osint, gov_military, journalist, think_tank, other | all |
| `category` | Author category text filter | all |
| `platform` | twitter, telegram | all |
| `event` | Event UUID -> linked posts via source URLs | — |
| `since` | ISO 8601 timestamp | 48h ago |
| `limit` | Max results | 30 |

### `/{topic}/news` — Mainstream media

Coverage from 18+ major outlets (Reuters, AP, CNN, NYT, Bloomberg, Guardian, BBC, Al Jazeera, etc.).

| Param | Description | Default |
|-------|-------------|---------|
| `region` | intl, us, mideast, israel, persian, asia, russia, china, other | all |
| `language` | en, fa | all |
| `event` | Event UUID -> linked articles | — |
| `since` | ISO 8601 timestamp | 48h ago |
| `limit` | Max results | 30 |

### `/{topic}/polymarket` — Prediction markets

Current probabilities, trend direction, and historical price ranges for Iran-related prediction markets.

Each condition includes: `label`/`label_zh`, `yes_price` (0-1), trend arrow with % change, historical min-max range.

### `/{topic}/notable` — Curated key entities

~90 curated key sources grouped by role:

| Group | What it represents |
|-------|-------------------|
| Iran Official | Khamenei.ir, IRNA, Fars, Tasnim — the regime's voice |
| Israel & Military | IDF, Netanyahu, Haaretz, Jerusalem Post — Israeli perspective |
| US Government | State Dept, CENTCOM, White House, Trump — US policy signals |
| International Organizations | IAEA, NATO, UN — multilateral stance |
| Key Media — Wire & Global | Reuters, AP, Bloomberg, NYT, Guardian — baseline narrative |
| Key Media — Regional & Specialist | Iran International, Al-Monitor, Bellingcat — specialist depth |
| OSINT & Prediction | Sentdefender, OSINT613, Polymarket — real-time ground truth |
| Think Tanks | Atlantic Council, Brookings, CFR — analytical framing |
| Key Activists & Opposition | Masih Alinejad, Reza Pahlavi, NCRI — diaspora/opposition voice |

### `/{topic}/entities` — Full source directory

800+ tracked entities. Also accessible via alias `/sources`.

| Param | Description | Default |
|-------|-------------|---------|
| `category` | Filter by entity category | all |
| `q` | Text search (name + description) | — |
| `limit` | Max results | 100 |

---

## Trump Endpoint

**`/trump`** — Full Trump Truth Social feed, auto-tagged by topic.

| Param | Description | Default |
|-------|-------------|---------|
| `tags` | Comma-separated topic filter (iran-war, energy, trade, china, executive-order, etc.) | all |
| `limit` | Max results | 50 (max: 200) |
| `since` | ISO 8601 or Unix timestamp | — |
| `cursor` | Pagination cursor (from `meta.next_cursor`) | — |
| `lang` | zh or en | zh |
| `offset` | Pagination offset | 0 |

Each post includes: `id`, `author_name`, `author_handle`, `content` (EN), `content_zh`, `tags[]`, `source_url`, `platform` (truth-social), `media_url`, `published_at`.

---

## Key dictionaries

**Event category:** `CONFLICT` · `DIPLOMACY` · `POLITICS` · `ECONOMY` · `PROTESTS`

**Event sentiment:** `NEGATIVE` · `POSITIVE` · `NEUTRAL` · `MIXED`

**source_type** (on posts): `news_agency` · `state_media` · `osint` · `gov_military` · `journalist` · `think_tank` · `other`

**News region:** `intl` · `us` · `mideast` · `israel` · `persian` · `asia` · `russia` · `china` · `other`

**Post platform:** `twitter` · `telegram` · `truth-social` (Trump only)

**Trump tags:** `iran-war` · `energy` · `trade` · `china` · `executive-order` · (auto-generated, non-exhaustive)

## Entity relationships

```
Briefing -> thread.signals[].id -> Event ID -> /posts?event={id} or /news?event={id}
Event -> source_details[].entity_slug -> /entities or /notable
Post -> source_type (mapped from author_category)
Thread -> polymarket_ref -> /polymarket
Trump -> tags[] -> cross-reference with /events or /posts
```

**Key investigation paths:**

1. **Briefing -> Thread -> Event -> Sources -> Entity**: "This thread claims X" -> check linked events -> how many sources? -> who are they? -> what camp?
2. **Event -> Posts/News**: use `/posts?event={id}` or `/news?event={id}` to find original content linked to a specific event
3. **Thread -> Polymarket**: thread has polymarket_ref -> check `/polymarket` -> does market probability align with AI assessment?
4. **Weak evidence -> Cross-reference**: claim has weak evidence -> check `/news` for mainstream coverage -> check `/posts?source_type=osint` -> if neither confirms, flag as unverified
5. **Trump signal -> Iran impact**: `/trump?tags=iran-war` -> check if events corroborate -> `/events?category=DIPLOMACY` -> assess real impact vs rhetoric

## Usage scenarios

**"What's the latest on Iran?"** — Call `/iran` -> summarize situation assessment + top 2-3 threads. Keep it under 300 words. Lead with tension level and direction.

**"What did Trump just say about Iran?"** — Call `/trump?tags=iran-war&limit=5` -> then cross-check `/events?category=DIPLOMACY&hours=6` to see if rhetoric matches real developments.

**"Is this source credible?"** — Call `/notable` first (fast, curated). If not found, fall back to `/entities?q=name`. Report which camp they belong to and their category.

**"What are the markets saying?"** — Call `/polymarket` -> compare market-implied probability with briefing's thread assessment. Flag divergences explicitly.

**"Deep dive on a specific event"** — Get event ID from briefing or `/events` -> call `/posts?event={id}` and `/news?event={id}` -> triangulate source count and source types.

## Output guidelines

- **Lead with judgment, then evidence.** Don't dump raw data — synthesize first, cite after.
- **Mark confidence.** Use "confirmed (N sources)" / "reported but unverified (single source)" / "rumor" based on `source_count`.
- **Flag weak evidence.** If a claim has only 1 source or comes from entertainment/social accounts, say so explicitly.
- **Keep it concise.** Default to 200-400 words unless the user asks for detail.
- **Bilingual when helpful.** Key terms and quotes can include both English and Chinese where the data provides translations.
- **Never present AI analysis as fact.** The briefing is AI-generated — frame it as "the briefing assesses..." not "the situation is...".

## Key principle

**The briefing is the map. The other endpoints are the territory.** Don't dump all data on the user — use the briefing to identify what matters, investigate only what's relevant, and synthesize a judgment.

## Notes

- Data from iranmonitor.org (800+ sources), Polymarket CLOB API, Truth Social
- AI analysis hourly, data feeds every 5 minutes
- All responses are Markdown with Chinese translations where available
- 48-hour rolling data window with deduplication by event/post ID
- Trump feed: auto-tagged by topic, bilingual (EN + ZH)
