---
name: news-fetcher
description: Install, configure, validate, and run the news-fetcher Python CLI for aggregating RSS/Atom and HTML news sources with deduplication, clustering, ranking, source diversity, summaries, and GitHub project discovery. Use when an agent needs to fetch news, create or validate a config, troubleshoot installation, discover GitHub projects worth attention today, or produce JSON/Markdown/CSV/RSS output from multiple sources.
---

# News Fetcher

Use this skill to get a working `news-fetcher` installation and run it correctly.

Release marker: `news-fetcher-skill-0.1.8-debug-a`

## Important

- Installing the ClawHub skill does **not** install the Python package.
- Install the Python package separately with `pip`.
- Put global options **before** `run`.

Correct:

```bash
news-fetcher --config config.yaml --limit 10 run
```

Wrong:

```bash
news-fetcher run --config config.yaml --limit 10
```

## Minimal working install

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install "git+https://github.com/miniade/news-fetcher.git@v0.1.8"
news-fetcher version
```

Expect `news-fetcher version 0.1.8`.

## Minimal working config

Generate a starter config:

```bash
news-fetcher config example > config.yaml
```

Or create one manually:

```yaml
sources:
  - name: BBC News
    url: http://feeds.bbci.co.uk/news/rss.xml
    weight: 1.0
    type: rss

  - name: Reuters Tech
    url: https://www.reutersagency.com/feed/?best-topics=tech
    weight: 1.2
    type: rss

  - name: Example HTML Source
    url: https://example.com/news
    weight: 0.9
    type: html
    selector: main article

thresholds:
  similarity: 0.8
  min_score: 0.3
  cluster_size: 2
  max_per_source: 3

weights:
  content: 0.6
  source: 0.2
  publish_time: 0.2
```

Validate it:

```bash
news-fetcher config validate config.yaml
```

## Common commands

Run with a config:

```bash
news-fetcher --config config.yaml --limit 20 run
```

Write Markdown output:

```bash
news-fetcher --config config.yaml --format markdown --output news.md run
```

Filter by time:

```bash
news-fetcher --config config.yaml --since 2026-03-01T00:00:00 run
```

Raise the score threshold:

```bash
news-fetcher --config config.yaml --min-score 0.5 run
```

Override sources directly from the CLI:

```bash
news-fetcher --sources "http://feeds.bbci.co.uk/news/rss.xml,https://news.ycombinator.com/rss" --limit 10 run
```

## GitHub project discovery

Minimal config example:

```yaml
sources:
  - name: GitHub Trending
    url: https://github.com/trending
    type: html
    source_type: github_project_discovery
    candidate_strategy: project_discovery

thresholds:
  similarity: 0.8
  min_score: 0.0
  cluster_size: 2
  max_per_source: 3
```

This path discovers projects from GitHub Trending, enriches repository metadata, ranks projects with GitHub-specific signals, and emits selected repositories as normal news items.

## HTML sources

For `type: html` sources, set `selector` when the site does not use clean `<article>` blocks.

Example:

```yaml
sources:
  - name: Example HTML Source
    url: https://example.com/news
    type: html
    selector: .story-card
```

## Troubleshooting

If `news-fetcher` is missing after installing the skill, install the Python package:

```bash
pip install "git+https://github.com/miniade/news-fetcher.git@v0.1.8"
```

If config validation fails, run:

```bash
news-fetcher config validate config.yaml
```

If results are too sparse, lower `thresholds.min_score` or raise `thresholds.max_per_source`.

## References

- Tagged source install: `pip install "git+https://github.com/miniade/news-fetcher.git@v0.1.8"`
- PyPI (optional, if published): https://pypi.org/project/news-fetcher/
- Source: https://github.com/miniade/news-fetcher
- Version targeted by this skill: 0.1.8
