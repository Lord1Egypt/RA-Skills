# Automation Template

Use this when the user wants a recurring gold sentiment update that is ready before they ask for it.

## Goal

Refresh a cached gold-news snapshot, then write one concise sentiment report that the skill can reuse quickly.

## Freshness Policy

- treat `data/latest_sentiment.md` as fresh for 6 hours by default
- if it is older than 6 hours, regenerate it
- if the latest fetch fails, keep the old report only if it is clearly marked stale

## Recommended Automation Prompt

```markdown
Use $gold-news-sentiment to refresh the gold market snapshot.

Steps:
1. Run `python3 scripts/update_snapshot.py --hours 48 --limit 50`.
2. Read `data/latest_digest.md` and `data/latest_news.json`.
3. Produce one fresh gold sentiment report with:
   - top-line conclusion: 看涨, 看跌, or 观望
   - 短线 and 中线 bias
   - confidence
   - 3 to 5 core drivers
   - 3 to 5 most relevant recent news items with links
   - what could invalidate the view
4. Write the final report to `data/latest_sentiment.md`.
5. If the snapshot has zero usable items or retrieval failed badly, write a short report that says data is insufficient rather than guessing.
```

## Suggested Report Shape

```markdown
# Gold Sentiment Snapshot

- generated_at_utc: <timestamp>
- freshness_window_hours: 6
- top_line: 观望
- short_term: 偏多
- medium_term: 中性
- confidence: 中

## Core Drivers
- <driver>
- <driver>

## Key News
1. [<title>](<url>) - <why it matters>
2. [<title>](<url>) - <why it matters>

## Why Not A Stronger Call
- <reason>

## Invalidation Risks
- <risk>
```

## Skill Behavior

When this automation exists, the skill should:

1. check whether `data/latest_sentiment.md` exists and is still fresh
2. use it first for fast answers
3. only rerun retrieval when the user asks for a refresh or the cached report is stale
