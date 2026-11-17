---
name: discourse
description: Scans HN, Lobsters, Reddit, and tech blogs for community experience reports
version: 1.10.3
triggers:
  - hackernews
  - reddit
  - lobsters
  - blogs
  - discourse
  - gathering practitioner opinions on a technology or approach
metadata: {"openclaw": {"homepage": "https://github.com/athola/claude-night-market/tree/master/plugins/tome", "emoji": "\ud83e\udd9e"}}
source: claude-night-market
source_plugin: tome
---

> **Night Market Skill**: ported from [claude-night-market/tome](https://github.com/athola/claude-night-market/tree/master/plugins/tome). For the full experience with agents, hooks, and commands, install the Claude Code plugin.


# Discourse Search

## When To Use

- Gathering community opinions on a technology or approach
- Finding experience reports from HN, Reddit, or Lobsters

## When NOT To Use

- Academic research (use `Skill(tome:papers)`)
- Code examples (use `Skill(tome:code-search)`)

Scan community channels for discussions on a topic.

## Channels

- **Hacker News**: Algolia API at hn.algolia.com
- **Lobsters**: WebSearch with site:lobste.rs
- **Reddit**: JSON API (append .json to URLs)
- **Tech blogs**: WebSearch targeting curated domains

## Workflow

1. Build search URLs/queries per channel using
   `tome.channels.discourse.*` functions
2. Execute via WebFetch (APIs) or WebSearch (fallback)
3. Parse responses into Finding objects
4. Merge across sources with source attribution

## Exit Criteria

- [ ] At least two community channels (HN, Lobsters, Reddit, or
      tech blogs) queried per invocation
- [ ] HN results fetched via Algolia API at `hn.algolia.com`
      (WebFetch); WebSearch used as fallback if the API is
      unreachable
- [ ] Each Finding object includes a `source` field identifying
      which channel (HN, Lobsters, Reddit, or blog) it came from
- [ ] If all WebFetch and WebSearch calls fail for every channel,
      the failure is reported explicitly rather than returning
      fabricated or empty findings
