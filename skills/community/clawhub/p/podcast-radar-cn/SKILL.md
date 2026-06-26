---
name: podcast-radar-cn
description: Discover, compare, and curate trending Chinese podcasts or episodes from 中文播客榜. Use for hot or recent show discovery, creator benchmarking, curation lists, competitor research, or podcast distribution leads. Prefer ranking fields and title signals first, and only do small-scale Xiaoyuzhou enrichment when needed.
homepage: https://github.com/XiaohuoluFM/xhlfm-skills/tree/main/skills/podcast-radar-cn
metadata: {"openclaw":{"emoji":"🎙️","homepage":"https://github.com/XiaohuoluFM/xhlfm-skills/tree/main/skills/podcast-radar-cn","requires":{"anyBins":["python3","python"]},"install":[{"id":"brew-python","kind":"brew","formula":"python","bins":["python3"],"label":"Install Python 3 (brew)","os":["darwin"]}]}}
---

# Podcast Radar CN

Use this skill when the user wants to discover, compare, or curate Chinese podcasts or podcast episodes based on current ranking data.

This skill is strongest at:

- listener discovery
- creator benchmarking
- curation and distribution research

It is not a general web scraping skill. Its default posture is ranking-first and title-first.

## Skill Root Rule

Treat the directory containing this `SKILL.md` as the skill root.

- In OpenClaw, prefer `{baseDir}` when calling files inside this skill.
- In other hosts or manual installs, use the same paths relative to the skill root, for example `scripts/fetch_xyz_rank.py`.
- Examples below use `python3`; if the host only exposes `python`, swap the binary name.

## Quick Start

Choose one of the four ranking lists:

- `hot-episodes`
- `hot-podcasts`
- `new-podcasts`
- `new-episodes`

Fetch a candidate set first:

```bash
python3 {baseDir}/scripts/fetch_xyz_rank.py --list hot-episodes --limit 20
```

Filter by genre, freshness, or query when the user already has a direction:

```bash
python3 {baseDir}/scripts/fetch_xyz_rank.py \
  --list new-episodes \
  --limit 12 \
  --genre 社会与文化 \
  --freshness-days-max 30
```

If and only if you truly need extra context for a small set of candidates, enrich a few Xiaoyuzhou URLs:

```bash
python3 {baseDir}/scripts/enrich_xiaoyuzhou.py \
  --episode-url https://www.xiaoyuzhoufm.com/episode/69bf524c2d318777c9169361
```

## Workflow

1. Classify the request as one of:
   - listener discovery
   - creator benchmarking
   - curation/distribution research
2. Interpret the user's wording before choosing the list:
   - if the user says `热门播客`, `最近播客`, `值得听的播客`, or similar casual Chinese phrasing, default to episode-level results
   - if the user explicitly asks for `播客频道`, `播客栏目`, `节目主页`, `show-level`, `频道级`, or wants a creator benchmark list, use podcast-level results
3. Pick the most relevant ranking list.
   - default listener-discovery wording usually maps to `hot-episodes` or `new-episodes`
   - explicit channel / show / benchmark wording usually maps to `hot-podcasts` or `new-podcasts`
4. Fetch enough candidates to support filtering; do not stop at the first 5 unless the user asked for 5.
5. Use ranking fields and title signals first.
6. Only if the answer would otherwise be weak, enrich a small set of Xiaoyuzhou pages.
7. Return a task-shaped result, not raw JSON.

## Query Interpretation Rule

In Chinese product usage, users often say `播客` when they really mean `最近值得点开的内容`.

Default behavior:

- `热门播客`
- `最近热门播客`
- `最近值得听的播客`
- `推荐几个热门播客`

Treat these as requests for episode-level recommendations unless the wording clearly asks for show/channel-level objects.

Switch to podcast-level results only when the user explicitly asks for things like:

- `播客频道`
- `播客栏目`
- `播客节目主页`
- `频道级榜单`
- `栏目级榜单`
- show-level benchmark or channel list

When in doubt:

- listener-oriented wording -> episode-first
- benchmark / channel / host / show-portfolio wording -> podcast-first

## Title-First Rule

Before reaching for Xiaoyuzhou pages, inspect:

- `title`
- `podcastName` / `name`
- `primaryGenreName`
- `rank`
- `playCount` / `avgPlayCount`
- `commentCount` / `avgCommentCount`
- freshness fields

The fetch script also extracts title signals such as:

- episode markers like `S8E9`, `EP03`, `Vol132`
- guest hints like `A×B`, `对话某某`
- format hints like `对谈`, `访谈`, `复盘`, `盘点`
- topic keywords inferred from the title

If those signals are enough, do not enrich.

Read [references/title-signals.md](references/title-signals.md) when you need examples or interpretation guidance.

## Xiaoyuzhou Enrichment Rule

Xiaoyuzhou enrichment is allowed only for narrow, necessary follow-up work.

Hard rules:

- never bulk-enrich by default
- never enrich just to complete every field
- never enrich more than 20 URLs in one run
- if a request implies short-window bulk access, refuse enrichment and stay at ranking level

Use enrichment when:

- a short list needs better recommendation reasons
- you need the real Xiaoyuzhou `pid` from an episode page
- you need a podcast brief or episode description for a handful of finalists

The enrichment script enforces the cap for you.

## Output Modes

Use one of these result shapes:

- Listener Discovery: what episode is worth hearing now, and why
- Creator Benchmarking: which shows are worth studying or comparing against
- Curation and Distribution: which shows or episodes are worth packaging, recommending, or developing into downstream ideas

Read [references/output-modes.md](references/output-modes.md) when you need concrete formatting guidance.

## Data Caveats

- 中文播客榜 is weekly, not minute-by-minute real time
- the data is not full-platform coverage
- `primaryGenreName` is often missing on new lists
- `openRate` / `avgOpenRate` can exceed `1`; treat these as internal ranking signals, not literal rates

Read [references/api.md](references/api.md) when you need field notes or endpoint details.

## Scripts

- `scripts/fetch_xyz_rank.py`
  Purpose: fetch and normalize ranking data, with basic filters and title-signal extraction
- `scripts/enrich_xiaoyuzhou.py`
  Purpose: enrich a small set of Xiaoyuzhou pages with brief/description/shownotes context, under a strict cap

## What To Avoid

- dumping raw fields without synthesis
- pretending the ranking is a real-time universal truth
- using Xiaoyuzhou enrichment for large-page traversal
- over-explaining `openRate` as if it were a clean probability
