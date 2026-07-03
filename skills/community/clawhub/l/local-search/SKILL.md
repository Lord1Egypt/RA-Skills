---
name: local-search
description: Local web search skill that runs entirely on the user's machine. Scrapes DuckDuckGo / Bing / Google HTML directly with automatic engine fallback (DDG -> Bing -> Google). Use whenever the user needs real-time web information, latest news, or content beyond the knowledge cutoff. Returns structured results (url / name / snippet / host_name / rank / date / favicon) plus source_engine, raw_html, score extensions. Supports --num, --recency-days, --locale (BCP-47), --json, --output. No API key, no SDK, no cloud hop.
license: MIT
---

# Local Search Skill

> **Local web search with automatic engine fallback.**
> Direct HTML scraping of DuckDuckGo / Bing / Google · resilient to rate-limiting · canonical result schema.

[![ClawHub](https://img.shields.io/badge/ClawHub-%40Sakurakilove%2Flocal--search-red)](https://clawhub.ai/@Sakurakilove/local-search)
[![Version](https://img.shields.io/badge/version-1.6.2-blue)](https://github.com/Sakurakilove/local-search)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Sakurakilove/local-search/blob/main/LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org/)

This skill calls the public search engines directly from your machine. **No API key, no SDK, no network hop.** If one engine is rate-limiting you, the orchestrator silently falls through to the next — so the call usually succeeds on the first try, even from datacenter IPs where Google is blocked.

Each result is a `SearchFunctionResultItem` with the canonical 7 fields (`url`, `name`, `snippet`, `host_name`, `rank`, `date`, `favicon`) plus three optional extension fields: `source_engine`, `raw_html`, `score`. Consumer code written against any similarly-shaped web-search skill works here without changes.

## ✨ Highlights

- **Zero cloud SDK dependency** — only `cheerio` (HTML parser) and Node's built-in `fetch`.
- **Three engines, automatic fallback** — DuckDuckGo → Bing → Google when `engine: "auto"` (default).
- **Locale-aware** — `--locale en-US` / `zh-CN` / `ja-JP` / any BCP-47 tag. Critical for non-US IPs where Bing otherwise serves localized results even for English queries.
- **Recency filter** — `--recency-days 7` restricts to past-week results. DDG supports exact N days; Bing/Google use day/week/month buckets.
- **Canonical result schema** — `url` / `name` / `snippet` / `host_name` / `rank` / `date` / `favicon` fields, identical in shape to other web-search skills in the ClawHub registry.
- **CLI + SDK** — use `tsx bin/web-search.ts <query>` for one-offs, or `import { search } from "local-search"` in code.
- **Pure TypeScript ESM** — runs on Node 18+ via `tsx`, or zero-config via `bun`.

## 🚀 Quick Start

**One-line install** (ClawHub CLI):

```bash
npx clawhub install @Sakurakilove/local-search
```

**Manual setup** (clone + npm install):

```bash
# 1. Install (one runtime dep: cheerio)
cd skills/local-search && npm install

# 2. Search (auto-fallback across DDG → Bing; Google excluded from auto chain)
tsx bin/web-search.ts "artificial intelligence"

# 3. Pin a specific engine + locale
tsx bin/web-search.ts "machine learning" --engine bing --locale en-US --num 5

# 4. Recent news as JSON
tsx bin/web-search.ts "AI breakthroughs" --recency-days 7 --json -o ai_news.json
```

Programmatic use:

```typescript
import { search } from "local-search";

const outcome = await search("What is the capital of France?", { num: 5 });
if (outcome.success) {
  console.log(`Answered by ${outcome.engine} in ${outcome.elapsedMs}ms`);
  outcome.results.forEach(r => console.log(`- ${r.name}\n  ${r.url}`));
}
```

## 🎯 When to Use This Skill

Use `local-search` whenever the user needs information that lives on the public web — beyond what's in the model's training data:

- **Real-time information**: current news, stock prices, weather, sports scores
- **Latest documentation**: framework release notes, API changes, recently published papers
- **Fact-checking**: verify a claim against live web sources
- **Research**: gather multiple sources on a topic, compare perspectives
- **Content discovery**: find tutorials, blog posts, recent talks
- **Competitive / market analysis**: competitor announcements, industry trends
- **Academic lookup**: find papers, citations, author pages

## 🔄 Engine Comparison

| Engine | Endpoint | API key | Residential IP | Datacenter IP | Recency |
|---|---|---|---|---|---|
| **DuckDuckGo** | `html.duckduckgo.com/html/` (GET) | none | ✅ high | ⚠️ rate-limits under load | `df=d<N>` (exact days) |
| **Bing** | `www.bing.com/search` | none | ✅ high | ✅ high | `freshness=d1\|w1\|m1` (bucketed) |
| **Google** | `www.google.com/search` | none | ⚠️ medium | ❌ low (enablejs wall) | `tbs=qdr:d\|w\|m\|y` (bucketed) |

`engine: "auto"` tries them in order **DuckDuckGo → Bing → Google**, returning the first non-empty result set. From a datacenter IP the effective chain is DDG → Bing (Google is usually blocked); from a residential IP all three are viable. Edit `AUTO_ENGINE_ORDER` in `src/engines/index.ts` to change priority.

## 📦 Installation Path

**Recommended Location**: `{project_path}/skills/local-search`

Extract this skill package to the above path in your project.

## Prerequisites

- **Node.js >= 18** (uses the built-in global `fetch`).
- **One npm dependency**: `cheerio` (HTML parser).
- A working internet connection — the skill calls the public search engines directly.

Install once in the skill directory:

```bash
cd {project_path}/skills/local-search
npm install            # or: bun install / pnpm install
```

> The skill is pure TypeScript ESM. You can run it via `tsx` (recommended, dev-friendly) or `bun` (zero-config). A runtime-agnostic `node --experimental-strip-types bin/web-search.ts` also works on Node 22+.

## Why Local?

| Aspect | Cloud-search skills | This skill (`local-search`) |
|---|---|---|
| Search backend | Cloud function / API | Direct HTTP to DuckDuckGo / Bing / Google |
| API key / SDK | Required | None |
| Network path | Client → cloud → search engine | Client → search engine |
| Failure handling | SDK-dependent | Auto-fallback across 3 engines |
| Result schema | `SearchFunctionResultItem` (7 fields) | Same 7 fields + 3 optional extension fields |
| CLI | SDK-specific | `tsx bin/web-search.ts` |

## Architecture

```
local-search/
├── SKILL.md                 ← you are here
├── LICENSE.txt
├── package.json             ← declares the `cheerio` dep
├── tsconfig.json
├── bin/
│   └── web-search.ts        ← CLI entry
├── src/
│   ├── index.ts             ← public SDK exports
│   ├── search.ts            ← orchestrator with auto-fallback
│   ├── types.ts             ← SearchFunctionResultItem + options
│   └── engines/
│       ├── _shared.ts       ← fetch / parse helpers
│       ├── duckduckgo.ts    ← POST https://html.duckduckgo.com/html/
│       ├── bing.ts          ← GET https://www.bing.com/search
│       ├── google.ts        ← GET https://www.google.com/search
│       └── index.ts         ← engine registry + AUTO_ENGINE_ORDER
└── scripts/
    └── web_search.ts        ← quick-start example
```

The only runtime dependency is `cheerio` (HTML parser), declared in `package.json`. Node 18+'s built-in `fetch` covers the network layer — no other SDK is imported anywhere in this package.

## CLI Usage

The CLI lives at `bin/web-search.ts`. Run it via `tsx`, `bun`, or any TS-aware runner.

### Basic Search

```bash
# Default: auto engine, 10 results, human-readable output
tsx bin/web-search.ts "artificial intelligence"

# Limit number of results
tsx bin/web-search.ts "machine learning" --num 5
# (short option works too)
tsx bin/web-search.ts "machine learning" -n 5
```

### Pin a Specific Engine

```bash
# Force DuckDuckGo only
tsx bin/web-search.ts "latest tech news" --engine duckduckgo
# Force Bing only
tsx bin/web-search.ts "latest tech news" --engine bing
# Force Google only (highest quality, most likely to be rate-limited)
tsx bin/web-search.ts "latest tech news" --engine google
# Default — try DDG → Bing → Google, return first non-empty
tsx bin/web-search.ts "latest tech news" --engine auto
```

### Recency Filter

```bash
# Results from last 7 days
tsx bin/web-search.ts "cryptocurrency news" --num 10 --recency-days 7
# (short option)
tsx bin/web-search.ts "cryptocurrency news" -r 7
```

### Save Results to JSON

```bash
# Write JSON to a file (human-readable banner is suppressed)
tsx bin/web-search.ts "climate change research" --num 5 --json -o search_results.json

# Or pipe JSON to stdout
tsx bin/web-search.ts "AI breakthroughs" --num 3 --recency-days 1 --json > ai_news.json
```

### Quiet Mode (Scripts / Piping)

```bash
# Suppress the "engine / timing" banner — just print the results
tsx bin/web-search.ts "react hooks" --quiet
```

### CLI Parameters

| Flag | Short | Description |
|---|---|---|
| `--num <N>` | `-n` | Number of results (default: 10, max: 50) |
| `--engine <id>` | `-e` | `duckduckgo` \| `bing` \| `google` \| `auto` (default: `auto`) |
| `--recency-days <N>` | `-r` | Restrict to results from last N days (default: 0 = no filter) |
| `--timeout <ms>` | — | Per-engine timeout in ms (default: 8000) |
| `--json` | — | Emit JSON instead of human-readable output |
| `--output <path>` | `-o` | Write JSON to file instead of stdout |
| `--pretty` | — | Pretty-print JSON (default on; pass `--no-pretty` to disable — not yet supported, omit `--json` instead) |
| `--quiet` | `-q` | Suppress engine-info banner |
| `--help` | `-h` | Show help |

### Search Result Structure

Each result item is a `SearchFunctionResultItem`:

```typescript
interface SearchFunctionResultItem {
  // ----- Canonical fields (shared shape across ClawHub web-search skills) -----
  url: string;          // Full URL of the result
  name: string;         // Title of the page
  snippet: string;      // Preview text / description
  host_name: string;    // Domain name (e.g. "en.wikipedia.org")
  rank: number;         // 1-indexed ranking within the engine's result set
  date: string;         // Publication / update date; "N/A" when unknown
  favicon: string;      // Favicon URL (Google S2)

  // ----- Extension fields (new in local-search) -----
  source_engine: "duckduckgo" | "bing" | "google";
  raw_html?: string;    // Original HTML of the snippet element (optional)
  score?: number;       // Heuristic relevance score [0, 100] (optional)
}
```

## SDK Usage

If you're writing TypeScript/JavaScript code (not running the CLI), import from `src/index.ts`:

### Simple Search

```typescript
import { search } from "local-search";

const outcome = await search("What is the capital of France?", { num: 5 });

if (outcome.success) {
  console.log(`Engine used: ${outcome.engine}`);
  console.log(`Tried in order: ${outcome.enginesTried.join(" → ")}`);
  console.log(`Elapsed: ${outcome.elapsedMs}ms`);
  for (const item of outcome.results) {
    console.log(`- ${item.name}  [${item.source_engine}]`);
    console.log(`  ${item.url}`);
    console.log(`  ${item.snippet}`);
  }
} else {
  console.error("Search failed:", outcome.error);
  if (outcome.errors) {
    // Auto mode: see which engines tried and what they reported
    for (const e of outcome.errors) {
      console.error(`  ${e.engine}:`, e.error);
    }
  }
}
```

### Throw-on-Failure Variant

```typescript
import { searchOrThrow, AllEnginesFailedError } from "local-search";

try {
  const results = await searchOrThrow("JavaScript frameworks", { num: 10 });
  console.log(results);
} catch (err) {
  if (err instanceof AllEnginesFailedError) {
    console.error("All engines failed:", err.errors);
  } else {
    console.error("Single-engine error:", err);
  }
}
```

### Pin a Specific Engine

```typescript
import { search } from "local-search";

// Skip the fallback chain — only use DuckDuckGo.
const outcome = await search("quantum computing applications", {
  num: 8,
  engine: "duckduckgo",
});
```

### Recency Filter

```typescript
const outcome = await search("genomics research", {
  num: 5,
  recency_days: 30, // past 30 days
});
```

### Custom Fetch (Tests / Edge Runtimes)

```typescript
const outcome = await search("hello world", {
  fetchImpl: myMockFetch, // any WhatWG-fetch-compatible function
  userAgent: "my-bot/1.0",
  timeoutMs: 5000,
});
```

## Engine Backends

### DuckDuckGo (`duckduckgo`)

- **Endpoint**: `https://html.duckduckgo.com/html/` (POST form `q=...`)
- **No API key**. Subject to rough rate limits — sustained hammering returns empty result sets.
- **Recency**: `df=d<N>` form field.
- **Best for**: default first try; rarely blocked outright; respects privacy.

### Bing (`bing`)

- **Endpoint**: `https://www.bing.com/search?q=...&count=...`
- **No API key**. HTML layout is stable and easy to parse.
- **Recency**: `freshness=d1` / `w1` / `m1` bucket (Bing has no arbitrary-N-days URL filter).
- **Best for**: second fallback; good English-language results; occasional locale quirks (mitigated by `ensearch=1`).

### Google (`google`)

- **Endpoint**: `https://www.google.com/search?q=...&num=...`
- **No API key**, BUT Google is the most aggressive at blocking scrapers. From **datacenter / cloud IPs** Google typically returns a "please enable JS" redirect page (`/httpservice/retry/enablejs`) with zero parseable results — the engine surfaces this as a soft failure and the auto chain falls through. From **residential IPs**, Google HTML scraping often works fine.
- **Recency**: `tbs=qdr:d|w|m|y` bucket.
- **Best for**: last-resort fallback on residential IPs; will usually fail on cloud IPs (where DDG+Bing already cover the need).

### Auto-Fallback Strategy

When `engine: "auto"` (the default), the orchestrator tries engines in this order:

1. **DuckDuckGo** — least aggressive blocking, finest-grained date filter
2. **Bing** — usually stable from any IP, including datacenter
3. **Google** — best result quality when reachable; often blocked on datacenter IPs

It returns the first engine that yields ≥ 1 result. If all three fail, the outcome is `{ success: false, errors: [...] }` with every engine's error attached — or, in `searchOrThrow` mode, an `AllEnginesFailedError`.

**Practical reliability table** (observed during testing):

| Caller IP type | DDG | Bing | Google | Effective auto chain |
|---|---|---|---|---|
| Residential | high | high | medium | DDG → Bing → Google (3 viable) |
| Datacenter / cloud | medium (rate-limits under load) | high | low (enablejs wall) | effectively DDG → Bing |

The order is defined in `src/engines/index.ts` (`AUTO_ENGINE_ORDER`); edit that array if you want a different priority.

## Common Use Cases

1. **Real-time Information Retrieval**: Current news, stock prices, weather
2. **Research & Analysis**: Gather information on specific topics
3. **Content Discovery**: Find articles, tutorials, documentation
4. **Competitive Analysis**: Research competitors and market trends
5. **Fact Checking**: Verify information against web sources
6. **SEO & Content Research**: Analyze search results for content strategy
7. **News Aggregation**: Collect news from various sources
8. **Academic Research**: Find papers, studies, and academic content

## Troubleshooting

**Issue**: `Required dependency 'cheerio' is not installed`
- **Fix**: `cd skills/local-search && npm install cheerio`

**Issue**: `All search engines failed` (auto mode)
- **Diagnosis**: The outcome's `errors` array lists each engine's failure. Common causes:
  - No internet connection
  - All three engines rate-limiting you (rare, but happens under sustained load)
  - Corporate proxy / firewall blocking search domains
- **Fix**: Wait a minute and retry; or pin a single engine to get a clearer error.

**Issue**: DuckDuckGo returns "No results parsed"
- **Cause**: DDG silently serves an empty page when rate-limited. The skill surfaces this as a soft failure so `auto` mode can fall through to Bing.
- **Fix**: Switch to `--engine bing` or wait.

**Issue**: Google returns "consent / captcha page"
- **Cause**: Google is blocking your IP / region.
- **Fix**: Use DuckDuckGo or Bing. Google is the most fragile backend by design.

**Issue**: Results from a single engine look stale / inconsistent
- **Cause**: Each engine ranks results differently. The `auto` chain returns whichever engine answered first — not a merged set.
- **Fix**: If you want merged & deduplicated results across engines, post-process `results` from multiple `search()` calls (one per engine).

**Issue**: `Cannot find module 'local-search'` when importing as SDK
- **Fix**: Either add the skill to your project's `package.json` workspaces, or import via a relative path: `import { search } from "./skills/local-search/src/index.js"`.

## Performance Tips

1. **Reuse the process**: Each `search()` call is stateless, but process startup (TS compile via `tsx`) costs ~200ms. For batch jobs, write a small Node script that loops over queries instead of spawning the CLI per query.
2. **Pin a single engine** when you don't need fallback — saves the latency of probing multiple engines.
3. **Lower `num`**: Each engine over-fetches then truncates; smaller `num` means slightly less parsing work.
4. **Parallel independent queries**: Use `Promise.all([...search(q1), search(q2), search(q3)])` — they hit different engines / endpoints concurrently.
5. **Result filtering client-side**: All engines return ~10 results even if you ask for 5; the orchestrator truncates, but if you want richer filtering (domain, date range, snippet length), do it in your code.

## Security Considerations

1. **Input Validation**: Sanitize user search queries before passing them in (the engines handle URL encoding, but your downstream code should still validate).
2. **Rate Limiting**: The skill itself does not rate-limit. If you wrap it in a service, add a rate limiter at that layer.
3. **No API Key Storage**: There are no API keys to leak. The only secret-like thing is your IP address.
4. **Privacy**: Your queries go directly to the chosen search engine. Whether that's more or less private than routing through a cloud function depends on your threat model.
5. **URL Validation**: Validate `result.url` before redirecting end users (the skill returns the engine's raw URL; some engines occasionally surface tracking redirects).
6. **User-Agent Spoofing**: The skill sends a Chrome desktop User-Agent by default. Override with `userAgent` if your use case requires honesty.

## Reference Scripts

A minimal example lives at `scripts/web_search.ts`:

```bash
# Default query
tsx scripts/web_search.ts

# Custom query + num
tsx scripts/web_search.ts "your query" 5
```

It's intentionally tiny — a smoke-test you can eyeball, not a feature showcase.

## Remember

- **Zero cloud SDK dependency** — only `cheerio` and Node's built-in `fetch`.
- **Canonical result schema** — `url` / `name` / `snippet` / `host_name` / `rank` / `date` / `favicon` fields, plus three optional extension fields (`source_engine`, `raw_html`, `score`).
- **Auto-fallback across DuckDuckGo → Bing → Google** when `engine: "auto"` (the default).
- **CLI**: `tsx bin/web-search.ts <query> [--num N] [--engine auto|duckduckgo|bing|google] [--recency-days N] [--json] [-o file.json]`.
- **SDK**: `import { search, searchOrThrow } from "local-search"`.
- **First-time setup**: `cd skills/local-search && npm install`.
- **Quick test**: `tsx scripts/web_search.ts`.

## Acknowledgements

The canonical `SearchFunctionResultItem` shape was inspired by [`z-ai-web-dev-sdk`](https://www.npmjs.com/package/z-ai-web-dev-sdk)'s MIT-licensed `web-search` skill. All engine backend code in this package is original.
