---
name: creator-watch
description: Manage and analyze a curated watchlist of Twitter/X creators for learning and research. Tracks solopreneurs, thought leaders, AI researchers, and content creators. Scrape their content, import to a database, and analyze patterns. Triggers on "creator watchlist", "scrape creators", "update creator database", "who should I follow", "analyze creator", "track influencer", or any creator monitoring request.
metadata: {"category": "research-intelligence", "platform": "twitter-x", "features": ["watchlist-management", "batch-scraping", "database-import", "engagement-analysis", "pattern-recognition"]}
---

# Creator Watchlist Skill

Manage a curated list of Twitter/X creators worth learning from. Batch scrape their content, import to a database, and extract patterns from high-performing posts.

---

## Watchlist

### Tier 1: Solopreneur / Indie Hacker (Priority)

| Username | Followers | Domain | Tags |
|----------|-----------|--------|------|
| `thedankoe` | 804K | Personal growth / creator economy | writing, philosophy |
| `levelsio` | 795K | Indie Hacker | nomad, shipping, bootstrapped |
| `naval` | 3M | Philosophy / investing | philosophy, wealth, startups |
| `thejustinwelsh` | 560K | Solopreneur | linkedin, one-person-business |
| `AlexHormozi` | 1M | Business / fitness | offers, sales |
| `ShaanVP` | 458K | Podcast / startups | ideas, newsletter |
| `arvidkahl` | 188K | Bootstrapping | audience, zero-to-sold |
| `tibo_maker` | 178K | Maker | product, distribution |
| `tdinh_me` | 176K | Indie Hacker | saas, products |
| `noahkagan` | 170K | Marketing | growth, appsumo |
| `dannypostma` | 167K | AI Products | maker, ai-tools |
| `yongfook` | 147K | SaaS | bootstrapped, design |
| `nathanbarry` | 146K | Creator Economy | newsletters, convertkit |
| `thepatwalls` | 134K | Startups | interviews, stories |
| `csallen` | 68K | Community | indie-hackers, founder |

### Tier 2: Tech / AI Thought Leaders

| Username | Followers | Domain | Tags |
|----------|-----------|--------|------|
| `karpathy` | 1.6M | AI education | deep-learning, youtube |
| `lexfridman` | 4.5M | Podcast / AI | interviews, research |
| `ylecun` | 1M | AI Research | meta, deep-learning |
| `DrJimFan` | 351K | AI Research | embodied-ai, nvidia |
| `lilianweng` | 183K | AI Research | openai, blog |
| `mattpocockuk` | 230K | TypeScript | tutorials, ts |

### Tier 3: Writing / Content

| Username | Followers | Domain | Tags |
|----------|-----------|--------|------|
| `SahilBloom` | 1M+ | Writing / investing | threads, frameworks |
| `JamesClear` | 2M+ | Habits / productivity | habits, atomic |
| `dickiebush` | 400K | Writing instruction | writing, ship30 |
| `david_perell` | 500K | Writing | essays |

---

## Quick Commands

### Scrape One Creator

```bash
# Using rnet_twitter.py (async Twitter GraphQL client)
python twitter_scraper.py <username> --limit 200
python db_import.py storage/twitter/<username>.json
```

### Scrape Batch by Tier

```bash
# Tier 1: Solopreneur / Indie Hacker (Priority)
TIER1="thedankoe levelsio naval thejustinwelsh AlexHormozi ShaanVP arvidkahl tibo_maker tdinh_me noahkagan dannypostma yongfook nathanbarry thepatwalls csallen"

# Tier 2: Tech / AI
TIER2="karpathy lexfridman ylecun DrJimFan lilianweng"

# Tier 3: Writing
TIER3="SahilBloom JamesClear dickiebush david_perell"

for user in $TIER1; do
  echo "=== Scraping @$user ==="
  python twitter_scraper.py $user --limit 200
  python db_import.py storage/twitter/$user.json
  echo "Waiting 30s to avoid rate limit..."
  sleep 30
done
```

---

## Scraping Schedule

| Frequency | Creators | Why |
|-----------|----------|-----|
| Weekly | thedankoe, naval, SahilBloom | High volume, trending content |
| Bi-weekly | AlexHormozi, JamesClear | Medium volume |
| Monthly | Others | Reference / archive |

---

## Database Schema

```sql
CREATE TABLE twitter_content (
  id TEXT PRIMARY KEY,
  username TEXT NOT NULL,
  text TEXT,
  created_at TIMESTAMPTZ,
  likes INTEGER DEFAULT 0,
  retweets INTEGER DEFAULT 0,
  replies INTEGER DEFAULT 0,
  views BIGINT,
  url TEXT,
  is_retweet BOOLEAN DEFAULT FALSE,
  imported_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_twitter_content_username ON twitter_content(username);
```

---

## Analysis Queries

### Top Performing Tweets by Likes

```sql
SELECT username, text, likes, retweets, url
FROM twitter_content
WHERE likes > 1000
ORDER BY likes DESC
LIMIT 20;
```

### Engagement Rate by Creator

```sql
SELECT
  username,
  COUNT(*) as tweets,
  AVG(likes) as avg_likes,
  AVG(retweets) as avg_retweets,
  MAX(likes) as top_tweet_likes
FROM twitter_content
GROUP BY username
ORDER BY avg_likes DESC;
```

### Find Viral Threads (High Engagement)

```sql
SELECT username, text, likes, retweets, views, url
FROM twitter_content
WHERE likes > 5000
  AND text NOT LIKE 'RT @%'
ORDER BY likes DESC;
```

### Content Patterns (Time Analysis)

```sql
SELECT
  EXTRACT(DOW FROM created_at) as day_of_week,
  EXTRACT(HOUR FROM created_at) as hour,
  AVG(likes) as avg_likes
FROM twitter_content
GROUP BY day_of_week, hour
ORDER BY avg_likes DESC
LIMIT 10;
```

### Topic Frequency (Simple Text Search)

```sql
-- Find posts mentioning a topic
SELECT username, text, likes, url
FROM twitter_content
WHERE text ILIKE '%indie hacker%'
ORDER BY likes DESC
LIMIT 20;
```

---

## Adding New Creators

To add a creator to the watchlist:

1. **Research first** — Check follower count, content quality, posting frequency
2. **Test scrape** — `python twitter_scraper.py <username> --limit 50`
3. **Add to watchlist** — Update the table in this file with tier, follower count, domain, tags
4. **Import** — `python db_import.py storage/twitter/<username>.json`

### Criteria for Watchlist

- 100K+ followers (established audience)
- Consistent posting (at least weekly)
- High engagement rate (likes/followers > 0.1%)
- Content relevant to: creator economy, solopreneurship, personal growth, writing, AI, or technical building

---

## Analysis Workflow

### When user says "analyze [creator]":

1. Query database for that creator's recent tweets
2. Find top-performing content (sorted by likes)
3. Identify patterns:
   - **Topics**: What subjects get the most engagement?
   - **Formats**: Threads vs single tweets vs lists
   - **Timing**: What day/hour performs best?
   - **Hook types**: Questions, contrarian takes, stats, stories
4. Summarize insights with specific examples

**Analysis output format:**
```
## @[username] Content Analysis

### Top Performing Formats
1. [Format] — avg [X] likes
2. [Format] — avg [X] likes

### Highest Engagement Topics
1. [Topic] — [N] posts, avg [X] likes
2. [Topic] — [N] posts, avg [X] likes

### Best Posting Times
- [Day] at [Hour] — avg [X] likes

### Hook Patterns That Work
- [Hook type]: "[example]" ([X] likes)
- [Hook type]: "[example]" ([X] likes)

### Key Takeaways
- [Insight 1]
- [Insight 2]
- [Insight 3]
```

### When user says "update creator database":

1. Check which creators have not been scraped recently (> 7 days for Tier 1)
2. Run scrape for each with 30-second delay between users
3. Import each to database
4. Report summary: creators updated, tweets imported, any errors

---

## Current Status Tracking

Track scrape status in this format:

| Username | Status | Tweets | Last Scraped |
|----------|--------|--------|--------------|
| @thedankoe | Done | 200 | 2026-01-27 |
| @levelsio | Done | 200 | 2026-02-05 |
| @naval | Done | 200 | 2026-02-05 |
| @thejustinwelsh | Done | 200 | 2026-02-05 |
| @AlexHormozi | Partial | 18 | 2026-02-05 (rate limited) |
| @karpathy | Pending | — | — |

**Status values:**
- `Done` — Full scrape completed
- `Partial` — Rate limited, partial data
- `Pending` — Not yet scraped
- `Error` — Scrape failed, needs investigation

---

## Rate Limiting Strategy

Twitter/X has aggressive rate limiting. Follow these rules:

- **30-second delay** between user scrapes in batch mode
- **Max 10 users** per scraping session
- If rate limited mid-batch, wait 15 minutes before continuing
- Prefer scraping during off-peak hours (early morning or late night)
- Do not run two scraping sessions simultaneously

---

## Cross-Creator Pattern Analysis

To find patterns across the entire watchlist:

```sql
-- What topics go viral across all creators?
SELECT
  -- extract common words/phrases manually or with NLP
  username,
  text,
  likes
FROM twitter_content
WHERE likes > 5000
  AND is_retweet = FALSE
ORDER BY likes DESC
LIMIT 50;

-- Which creator has the most consistent engagement?
SELECT
  username,
  AVG(likes) as avg_likes,
  STDDEV(likes) as stddev_likes,
  AVG(likes) / NULLIF(STDDEV(likes), 0) as consistency_score
FROM twitter_content
GROUP BY username
ORDER BY consistency_score DESC;
```

---

## Insight Applications

Use creator analysis to:

1. **Content inspiration** — Find angles that work in your niche
2. **Hook formulas** — Extract winning opening lines to adapt
3. **Posting timing** — Learn optimal days/hours for your audience
4. **Topic validation** — See which topics get traction before writing
5. **Competitive intelligence** — Understand what resonates in your market
