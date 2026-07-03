# local-search

> **Languages**: [English](./README.md) · [简体中文](./README.zh-CN.md)

[![ClawHub](https://img.shields.io/badge/ClawHub-%40Sakurakilove%2Flocal--search-red?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxwYXRoIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTV6eiIvPjwvc3ZnPg==)](https://clawhub.ai/@Sakurakilove/local-search)
[![Version](https://img.shields.io/badge/version-1.6.2-blue)](https://github.com/Sakurakilove/local-search/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4-blue.svg?logo=typescript)](https://www.typescriptlang.org/)
[![GitHub stars](https://img.shields.io/github/stars/Sakurakilove/local-search?style=social)](https://github.com/Sakurakilove/local-search)
[![GitHub last commit](https://img.shields.io/github/last-commit/Sakurakilove/local-search)](https://github.com/Sakurakilove/local-search/commits/main)

Web search skill that runs entirely on the user's machine. Scrapes the public SERPs of **DuckDuckGo / Bing / Google** directly over HTTP, with automatic engine fallback when one backend is rate-limiting or unreachable.

Each result is a `SearchFunctionResultItem` with `url`, `name`, `snippet`, `host_name`, `rank`, `date`, `favicon`, plus three extension fields: `source_engine`, `raw_html`, `score`.

## Quick Start

**One-line install** (ClawHub CLI):

```bash
npx clawhub install @Sakurakilove/local-search
```

**Manual setup** (clone this repo):

```bash
# 1. install the one runtime dependency
cd local-search
npm install           # or: bun install

# 2. run the example
tsx scripts/web_search.ts

# 3. or use the CLI directly
tsx bin/web-search.ts "artificial intelligence" --num 5
tsx bin/web-search.ts "AI news" --recency-days 1 --json -o ai_news.json
```

## Why?

- **No API key** — calls the public search engines directly.
- **No network hop** — your machine → engine, nothing in between.
- **Transparent** — every result carries a `source_engine` field so you can see who answered.
- **Resilient** — if DDG is rate-limiting you, the orchestrator silently falls through to Bing. Google is excluded from the auto chain (it almost always returns a JS-required wall from datacenter IPs); pass `--engine google` explicitly if you need it.
- **Locale-aware** — locale is **auto-detected from the query** (CJK → zh-CN, kana → ja-JP, hangul → ko-KR, Cyrillic → ru-RU, etc.; Latin/default → en-US). Override with `--locale <BCP-47>` if needed. Critical for non-English queries — Bing's `ensearch=1` flag (English SERP) returns garbage for CJK queries, so we only set it for English locales.

## Files

```
local-search/
├── SKILL.md             # full documentation (read this first)
├── package.json         # declares cheerio as the only runtime dep
├── tsconfig.json
├── LICENSE.txt
├── bin/
│   └── web-search.ts    # CLI: tsx bin/web-search.ts <query> [opts]
├── src/
│   ├── index.ts         # SDK exports
│   ├── search.ts        # orchestrator with auto-fallback
│   ├── types.ts         # SearchFunctionResultItem + options
│   └── engines/
│       ├── _shared.ts   # fetch/parse helpers
│       ├── duckduckgo.ts
│       ├── bing.ts
│       ├── google.ts
│       └── index.ts     # engine registry + AUTO_ENGINE_ORDER
└── scripts/
    └── web_search.ts    # quick-start example
```

## Programmatic Usage

```typescript
import { search } from "local-search";

const outcome = await search("What is the capital of France?", { num: 5 });
if (outcome.success) {
  console.log(`Engine: ${outcome.engine}  (${outcome.elapsedMs}ms)`);
  for (const item of outcome.results) {
    console.log(`- ${item.name}\n  ${item.url}\n  ${item.snippet}\n`);
  }
} else {
  console.error(outcome.error);
}
```

## CLI Usage

```bash
tsx bin/web-search.ts <query> [options]

Options:
  --num, -n <N>          Number of results (default: 10)
  --engine, -e <id>      duckduckgo | bing | google | auto  (default: auto)
  --recency-days, -r <N> Restrict to results from last N days
  --locale <BCP-47>      Result locale (default: auto-detect from query;
                          e.g. en-US, zh-CN, ja-JP, ko-KR, ru-RU)
  --timeout <ms>         Per-engine timeout (default: 8000)
  --json                  Emit JSON
  --output, -o <path>     Write JSON to file
  --quiet, -q             Suppress banner
  --help, -h              Show help
```

## Engines

| Engine | Endpoint | API key | Residential IP | Datacenter IP | Recency support |
|---|---|---|---|---|---|
| DuckDuckGo | `https://html.duckduckgo.com/html/` (GET) | none | high | medium (rate-limits under load) | `df=d<N>` (exact days) |
| Bing | `https://www.bing.com/search` | none | high | high | `freshness=d1\|w1\|m1` (bucketed) |
| Google | `https://www.google.com/search` | none | medium | low (enablejs wall) | `tbs=qdr:d\|w\|m\|y` (bucketed) |

`engine: "auto"` (the default) tries them in the order DuckDuckGo → Bing, returning the first non-empty result set. **Google is excluded from the auto chain** — from datacenter IPs it almost always returns a "please enable JS" wall with zero parseable results, so including it just wastes 8s before failing. From a residential IP you can still pass `--engine google` explicitly.

The chain is configurable — edit `AUTO_ENGINE_ORDER` in `src/engines/index.ts`.

## Verify Your Install

After `npm install`, run the included e2e test to confirm everything works on your network:

```bash
tsx scripts/test.ts
```

Expected output: 12 tests pass. The suite doesn't just check "did the engine return *something*" — it checks "did at least one result mention a query term" (Test 9 / 10 / 11), which catches the relevance regressions that pure "any-results-returned" tests miss.

## Acknowledgements

The result schema and original skill structure were inspired by [`z-ai-web-dev-sdk`](https://www.npmjs.com/package/z-ai-web-dev-sdk)'s `web-search` skill. That project's MIT-licensed design shaped the `SearchFunctionResultItem` shape used here; all engine backend code in this package is original.

## License

MIT. See [`LICENSE.txt`](./LICENSE.txt).
