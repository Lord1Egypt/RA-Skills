---
name: news-collect
description: Run a repo-local scan through `skills/news-aggregator-skill`, then normalize the result into a local report contract for the collect layer. Use when Codex needs a broad overseas or domestic media scan, wants a repeatable `news-report.md`, or needs raw JSON archived under `content-production/inbox/raw/news/`.
---

# News Collect

Use the repo-local `news-aggregator-skill` as a dependency, but always write outputs using this project's collect-layer contract. The report now includes lightweight写作决策字段 for recommended topics.

## Quick Start

Run the default command:

```bash
.venv/bin/python -m skill_runtime.cli run-skill news-collect --input content-production/inbox/20260405-ai-news-request.md
```

## Prepare Input

Pass a markdown request file with YAML frontmatter.

Supported fields:

- `profile`: `mixed_daily` / `global_latest` / `global_ai` / `cn_media` / `custom`
- `sources`: only used when `profile=custom`
- `keyword`
- `limit`
- `deep`
- `title`

Example:

```markdown
---
profile: mixed_daily
keyword: AI,Agent
limit: 8
deep: true
title: AI 每日资讯扫描
---

补充说明：更关注能延展成公众号观点文的题目。
```

## Follow Collection Workflow

1. Read the request frontmatter and resolve the source profile.
2. Call `skills/news-aggregator-skill/scripts/fetch_news.py` with `--no-save`.
3. Save the raw JSON to the local inbox raw directory.
4. Rewrite the result into a stable markdown report for人工选题与后续深研。
5. For recommended items, also emit写作价值判断、推荐切口、推荐框架与标题方向。

## Write Output

Write the report to:

```text
content-production/inbox/YYYYMMDD-<slug>-news-report.md
```

Write the raw JSON to:

```text
content-production/inbox/raw/news/YYYY-MM-DD/<slug>.json
```

## Respect Constraints

- Only read the repo-local dependency under `skills/news-aggregator-skill/`
- Do not save outputs back into the vendor skill directory
- Keep the wrapper contract stable even if the vendor skill adds new sources later

## Read Related Files

- Runtime entry: `skill_runtime/engine.py`
- Wrapper runtime: `skills/news-collect/runtime.py`
- Vendor dependency: `skills/news-aggregator-skill/`
- Data contract: `docs/data-contracts.md`
