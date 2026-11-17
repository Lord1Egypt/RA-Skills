---
name: code-search
description: Searches GitHub for existing implementations, libraries, or patterns
version: 1.10.3
triggers:
  - github
  - code
  - search
  - finding code examples or prior art on a topic during a research session
metadata: {"openclaw": {"homepage": "https://github.com/athola/claude-night-market/tree/master/plugins/tome", "emoji": "\ud83e\udd9e"}}
source: claude-night-market
source_plugin: tome
---

> **Night Market Skill**: ported from [claude-night-market/tome](https://github.com/athola/claude-night-market/tree/master/plugins/tome). For the full experience with agents, hooks, and commands, install the Claude Code plugin.


# Code Search

## When To Use

- Finding existing implementations or libraries on GitHub
- Part of a `/tome:research` session or standalone search

## When NOT To Use

- Searching local codebase (use Grep or Explore agent)
- Academic literature (use `Skill(tome:papers)`)

Search GitHub for implementations of a given topic.

## Usage

Invoked as part of `/tome:research` or standalone.

## Workflow

1. Build search queries using
   `tome.channels.github.build_github_search_queries()`
2. Execute queries via WebSearch
3. Parse results via `parse_github_result()` (returns `None` for a
   result with no URL, which the caller drops)
4. Optionally use GitHub API via
   `build_github_api_search()` for richer metadata
5. Rank via `rank_github_findings()`
6. Return Finding objects

## Exit Criteria

- [ ] At least one GitHub search query built and executed via
      WebSearch for the requested topic
- [ ] Results parsed into Finding objects containing repo metadata
      (name, URL, stars) and a relevance score
- [ ] Findings returned from `rank_github_findings()` sorted by
      relevance score descending
- [ ] If no results are found for the query, this is reported
      explicitly rather than returning an empty list silently
