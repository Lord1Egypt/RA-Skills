---
name: mangadex-cli
version: 0.1.2
description: MangaDex CLI skill for search, manga/chapter lookup, follow-feed checks, and recommendations.
allowed-tools: Bash
emoji: 📖
metadata:
  openclaw:
    install:
      - kind: node
        package: "@mtsku/mangadex-cli"
        bins: [mangadexcli]
    requires:
      bins: [node]
---

# MangaDex CLI Skill

Use this skill for direct MangaDex CLI workflows. This guide is for LLM/agent execution only.

## Installation Check

1. Check availability:
   - `command -v mangadexcli`
2. If missing, install:
   - `npm install -g @mtsku/mangadex-cli`
3. Verify:
   - `mangadexcli --help`

## Command Map

- Discovery/search:
  - `mangadexcli search manga "<query>"`
  - `mangadexcli search author "<query>"`
  - `mangadexcli search group "<query>"`
  - `mangadexcli works author "<author_uuid_or_name>"`
  - `mangadexcli works group "<group_uuid_or_name>"`
- Manga/chapter info:
  - `mangadexcli manga details <manga_uuid>`
  - `mangadexcli manga chapters <manga_uuid> --lang en -n 30`
  - `mangadexcli manga latest <manga_uuid> --lang en -n 10`
  - `mangadexcli chapter meta <chapter_uuid>`
- Follow feed:
  - `mangadexcli feed updates --window 24h --lang en`
  - `mangadexcli feed updates --window 7d`
- Recommendations:
  - `mangadexcli recommend suggest --tags "action,mystery" -n 10`
  - `mangadexcli recommend suggest --from-followed --exclude-library --window 7d -n 10`

## Auth Setup

- Personal client login:
  - `mangadexcli auth set-client <client_id> <client_secret>`
  - `mangadexcli auth login <username> <password>`
- Token-only:
  - `mangadexcli auth set-token <access_token>`
- Authorization code exchange:
  - `mangadexcli auth exchange --code <code> --redirect-uri <uri> [--code-verifier <verifier>]`
  - `mangadexcli auth refresh`
- Verify auth:
  - `mangadexcli whoami`
  - `mangadexcli auth where`

## Output Mode

- Use `--json` for machine-readable output.
- Public read endpoints work without auth.
- Feed updates and library-aware recommendation exclusions require auth.
