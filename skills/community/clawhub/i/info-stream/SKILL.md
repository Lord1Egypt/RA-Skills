---
name: daily-news-collector
description: Daily tech news collection and distribution system. Automated methodology for collecting, curating, and distributing industry news via scheduled cron jobs. Use when setting up automated daily news digests, creating tech news roundups, or building scheduled content delivery workflows. Triggers on "daily news", "news digest", "tech roundup", "industry news collection", "automated newsletter", "news cron".
---

# Daily News Collector

Automated methodology for collecting, curating, and distributing industry news.

## Architecture: Collect → Cache → Distribute

Separate collection (slow) from distribution (fast) using a file cache.

```
07:00  Collect news → Write to weekly file (slow, ~3-5 min)
08:00  Read file → Push to chat (instant, <10 sec)
```

**Key insight**: Collection and distribution happen the same morning. News is at most ~1 hour old when delivered, not 9+ hours.

## Setup Steps

### 1. Create Weekly File

Create a markdown file for the current week: `weekly-news-YYYY-WNN.md`

### 2. Collection Cron (daily, 07:00)

Schedule an isolated `agentTurn` cron job that:

1. Checks if today's report already exists in the weekly file (anti-duplication)
2. Searches news sources via two methods:
   - **Tavily API** (~80% weight): Broad search across multiple keyword groups
   - **web_fetch** (~20% weight): Deep crawl of core technical blogs
3. Selects top 10-15 stories, grouped by category
4. Writes formatted report to weekly file with today's date

### 3. Distribution Cron (daily, 08:00)

Schedule an isolated `agentTurn` cron job that:

1. Reads the weekly file
2. Finds today's report by date header
3. Pushes content to chat
4. If not found, notifies user instead of generating new content

**Timing**: 1 hour gap between collection and distribution ensures collection completes before push.

## Search Strategy

### Layer 1: AI Search API (Broad Discovery, ~80% weight)

Use Tavily API (or similar) with keyword groups tailored to your domain. Example for browser/AI news (7 groups, ~27 candidates):

- Group 1: `browser Chrome Firefox Safari Edge news 2026` (5 results, topic: news)
- Group 2: `AI machine learning LLM technology news March 2026` (5 results, topic: news)
- Group 3: Local language keywords for regional coverage — e.g. `中国科技 AI 浏览器 最新消息` (5 results, topic: news)
- Group 4: `Web standards W3C WHATWG V8 JavaScript new features 2026` (3 results, topic: news)
- Group 5: Platform-specific keywords — e.g. `Android Chrome mobile browser development 2026` (3 results, topic: news)
- Group 6: Chinese AI media keywords — e.g. `APPSO 机器之心 量子位 AI 人工智能 最新` (3 results, topic: news)
- Group 7: Chinese tech industry keywords — e.g. `虎嗅 雷科技 科技行业 消费电子` (3 results, topic: news)

See [references/tavily-setup.md](references/tavily-setup.md) for Tavily API setup.

### Layer 2: Core Blog Crawl (Deep Coverage, ~20% weight)

Use `web_fetch` to directly crawl authoritative blogs. These guarantee coverage of domain-specific news that AI search might miss.

Example sources for browser/AI domain:
- WebKit Blog: `https://webkit.org/blog/`
- V8 Blog: `https://v8.dev/blog`
- Mozilla Hacks: `https://hacks.mozilla.org/`
- Chromium Blog: `https://blog.chromium.org/`

### Layer 3: Aggregator Check (Community Pulse)

Check community aggregators for trending discussions:
- Hacker News: `https://news.ycombinator.com`

### Three-Layer Information Source Model

| Layer | Weight | Purpose | Speed | Depth |
|-------|--------|---------|-------|-------|
| AI Search API | ~80% | Broad discovery | Fast (1-3s/query) | Medium |
| Core blogs | ~20% | Domain authority | Slow (5-10s/source) | Deep |
| Aggregators | Optional | Community trends | Fast | Shallow |

Each layer should contribute 2-3 stories minimum to ensure balanced coverage.

## Report Format

### Title
```
## YYYY.M.D Report Title | Day N
```

### Categories (ordered by priority)
Use domain-specific categories. Examples:
- `### 🔧 Browser Engine & Web Standards`
- `### 🦊 Firefox / Mozilla`
- `### 🤖 AI & Browser Tech`
- `### 🇨🇳 Regional Tech`
- `### 📱 Mobile / Web Dev`

### Story Format
```
N. emoji **Title** — Description (2-3 sentences with specific details like version numbers, data, impact)
   - Source: full clickable URL
```

### Insights Section
```
#### 💡 Analyst Insights

💡 **Insight Title** — Analysis (2-3 sentences with actionable perspective)
```

### Footer
```
*Sources: Source1 · Source2 · Source3*
*Collected: YYYY-MM-DD HH:MM TZ*
```

## Anti-Duplication Rules

**Critical**: Multiple cron sessions may run simultaneously and cause conflicts.

1. **Collection cron**: Before writing, scan file for today's date header (## YYYY.M.D). If found, output "Report exists, skipping" and exit. Do NOT overwrite.
2. **Distribution cron**: Read-only. Never search, never write. If report missing, only notify user.
3. **Strict division**: Collection writes, distribution reads. Never cross.

## Quality Control

- Select for technical depth and impact, not quantity
- "Better 8 great stories than 15 mediocre ones"
- Cross-reference: prefer the original source when story appears in multiple feeds
- Each story must have a clickable URL
- Insights must add analysis, not just repeat the news

## Tavily Search Script (tavily-search.js)

Save this as `tavily-search.js` and run with: `node tavily-search.js "query" [max_results] [topic] [search_depth]`

Requires `TAVILY_API_KEY` environment variable.

```javascript
#!/usr/bin/env node
/**
 * Tavily Search — AI-optimized search API wrapper for news collection
 * Usage: node scripts/tavily-search.js "query" [max_results] [topic] [search_depth]
 *
 * Env: TAVILY_API_KEY required
 * Output: JSON with results array (title, url, content, score)
 */

const https = require('https');

const API_KEY = process.env.TAVILY_API_KEY;
if (!API_KEY) {
  console.error('Error: TAVILY_API_KEY environment variable not set');
  process.exit(1);
}

const query = process.argv[2];
const maxResults = parseInt(process.argv[3]) || 5;
const topic = process.argv[4] || 'general';
const searchDepth = process.argv[5] || 'basic';

if (!query) {
  console.error('Usage: node tavily-search.js "query" [max_results] [topic] [search_depth]');
  process.exit(1);
}

const payload = JSON.stringify({
  query,
  max_results: maxResults,
  topic,
  search_depth: searchDepth,
  include_answer: true,
  include_raw_content: false,
});

const req = https.request({
  hostname: 'api.tavily.com',
  path: '/search',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`,
  },
}, (res) => {
  let body = '';
  res.on('data', (chunk) => body += chunk);
  res.on('end', () => {
    try {
      const data = JSON.parse(body);
      const output = {
        query: data.query,
        answer: data.answer || null,
        results: (data.results || []).map(r => ({
          title: r.title,
          url: r.url,
          content: r.content?.substring(0, 500),
          score: r.score,
        })),
      };
      console.log(JSON.stringify(output, null, 2));
    } catch (e) {
      console.error('Parse error:', e.message);
      console.error('Raw:', body.substring(0, 500));
      process.exit(1);
    }
  });
});

req.on('error', (e) => {
  console.error('Request error:', e.message);
  process.exit(1);
});

req.write(payload);
req.end();
```

## References

- [references/usage-guide.md](references/usage-guide.md) — Beginner-friendly usage guide with FAQ
- [references/tavily-setup.md](references/tavily-setup.md) — Tavily API setup and configuration
- [references/sources.md](references/sources.md) — Curated information source list by domain
