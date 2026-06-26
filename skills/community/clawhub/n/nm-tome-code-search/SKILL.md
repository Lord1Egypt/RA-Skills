---
name: code-search
description: Searches GitHub for existing implementations, libraries, or patterns
version: 1.9.8
triggers:
  - github
  - code
  - search
  - finding code examples or prior art on a topic during a research session
metadata: {"openclaw": {"homepage": "https://github.com/athola/claude-night-market/tree/master/plugins/tome", "emoji": "\ud83e\udd9e"}}
source: claude-night-market
source_plugin: tome
---

> **Night Market Skill** — ported from [claude-night-market/tome](https://github.com/athola/claude-night-market/tree/master/plugins/tome). For the full experience with agents, hooks, and commands, install the Claude Code plugin.


# Code Search

## When To Use

- Finding existing implementations or libraries on GitHub
- Part of a `/tome:research` session or standalone search

## When NOT To Use

- Searching local codebase (use Grep or Explore agent)
- Academic literature (use `/tome:papers`)

Search GitHub for implementations of a given topic.

## Usage

Invoked as part of `/tome:research` or standalone.

## Workflow

1. Build search queries using
   `tome.channels.github.build_github_search_queries()`
2. Execute queries via WebSearch
3. Parse results via `parse_github_result()`
4. Optionally use GitHub API via
   `build_github_api_search()` for richer metadata
5. Rank via `rank_github_findings()`
6. Return Finding objects
