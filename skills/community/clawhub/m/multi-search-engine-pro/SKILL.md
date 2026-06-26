---
name: multi-search-engine
description: Build auditable search URLs across Chinese and global engines with region/language filters, advanced operators, time scopes, privacy-first options, compare mode, and no API keys.
version: 2.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      config:
        - config.json
        - resources/engine-catalog.json
    install: []
    emoji: "🔎"
    homepage: https://clawhub.com/skills/multi-search-engine
---

# Multi Search Engine v2.1.0

A search orchestration skill for OpenClaw that helps the agent **choose engines, build safe search URLs, compare results across engines, and explain why a given engine is appropriate**.

This version turns the skill from a static engine list into a **reusable toolkit** with:

- engine aliases and region-aware selection
- advanced operator composition (`site:`, `filetype:`, exact phrase, exclusion, OR groups)
- time scopes where the engine supports them
- compare mode for multi-engine research
- privacy-first presets
- command-line helper script that outputs `json`, `markdown`, or plain `text`
- explicit safety guidance for direct web access

## When to use this skill

Use this skill when the user wants to:

1. search the same query on multiple engines
2. bias toward Chinese vs global engines
3. use privacy-first engines
4. build advanced search operators reliably
5. compare engine coverage before opening pages
6. prepare direct `web_fetch` or browser URLs without needing an API key

## Recommended workflow

1. Normalize the user's research intent:
   - broad web search
   - China-focused search
   - privacy-first search
   - docs / code / paper / file search
   - calculation / fact query

2. Pick engines deliberately:
   - **China / local web**: Baidu, Sogou, 360, Toutiao, WeChat
   - **Global general**: Google, Bing INT, Brave, Yahoo
   - **Privacy-first**: DuckDuckGo, Startpage, Brave, Qwant
   - **Knowledge / computation**: WolframAlpha
   - **Community / niche finance**: Jisilu

3. Build the query using operators only when they help:
   - `site:` for source restriction
   - `filetype:` for PDFs / docs
   - quotes for exact phrase
   - `-term` for exclusion
   - `OR` for alternatives

4. Prefer compare mode for research-sensitive tasks:
   - one privacy engine
   - one mainstream engine
   - one region-specific engine if relevant

5. Open only the most promising result pages after inspecting generated URLs.

## Direct script usage

```bash
python3 scripts/build_search_urls.py --query "openclaw skills" --engine google
python3 scripts/build_search_urls.py --query "量化投资" --preset cn-research --time week --format markdown
python3 scripts/build_search_urls.py --query "react hooks" --site github.com --exact "useEffect" --compare google,ddg,brave
python3 scripts/build_search_urls.py --query "100 USD to CNY" --engine wolframalpha --format json
```

## Typical OpenClaw usage

```text
User asks for recent AI papers as PDFs
→ build a Google / Brave compare query
→ add filetype:pdf and time scope
→ inspect URLs before opening pages
```

## Security and privacy

- This skill does **not** require API keys.
- It does **not** execute remote code.
- It only generates deterministic search URLs from local templates.
- Network access happens only when the agent explicitly opens the generated URLs.
- Search engines may log requests; use privacy presets when that matters.

## Files

- `SKILL.md` — primary instructions and metadata
- `README.md` — install, scenarios, examples, FAQ, risks
- `scripts/build_search_urls.py` — URL builder and compare helper
- `resources/engine-catalog.json` — engine definitions, aliases, capabilities
- `resources/search-operator-cheatsheet.md` — operator reference
- `examples/example-prompt.md` — prompt patterns for agents
- `tests/smoke-test.md` — manual smoke coverage
- `SELF_CHECK.md` — self-audit and release checklist
