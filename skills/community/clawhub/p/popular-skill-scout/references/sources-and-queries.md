# Sources And Queries

Use ClawHub first, then GitHub, then ClawHub CLI, then broader directories, and only then general web search.

## Media priority

1. ClawHub website pages
   - Best for popularity, installs, stars, suspicious flags, and detail-page review
2. GitHub website pages
   - Best for source verification and maintenance checks
3. ClawHub CLI
   - Best when browser access is awkward or when quick keyword expansion is needed
4. Other directories and marketplaces
   - Best for discovery fallback and candidate expansion
5. General web search
   - Fallback only when the first four do not provide enough signal

## ClawHub

Base browse page:

- `https://clawhub.ai/skills?nonSuspicious=true`

Useful query patterns:

- `https://clawhub.ai/skills?nonSuspicious=true&q=file`
- `https://clawhub.ai/skills?nonSuspicious=true&q=repo`
- `https://clawhub.ai/skills?nonSuspicious=true&q=github`
- `https://clawhub.ai/skills?nonSuspicious=true&q=search`
- `https://clawhub.ai/skills?nonSuspicious=true&q=browser`
- `https://clawhub.ai/skills?nonSuspicious=true&q=document`

Sort passes to run:

1. Relevance for the specific use case
2. Installs for adoption
3. Stars for endorsement
4. Recently updated for freshness

On each promising result page, inspect:

- summary quality
- install count
- stars
- security flag
- runtime requirements
- whether the detail page explains what the skill actually does

Do not finalize a recommendation from search-list snippets alone. Open the detail page for every final candidate.

## GitHub

Use GitHub to verify that a candidate is real and maintained.

Useful searches:

- `site:github.com "SKILL.md" "openclaw"`
- `site:github.com "SKILL.md" "clawhub.ai"`
- `site:github.com "SKILL.md" "Use when"`
- `site:github.com "SKILL.md" "description:"`

If the skill already has a ClawHub page, search GitHub for:

- repo name
- author handle
- exact skill name in quotes

Repository review checklist:

- `SKILL.md` exists and is not placeholder text
- repository has recent activity
- installation story is clear
- skill scope is focused
- docs and code agree with the claimed behavior

## Decision rule

If ClawHub and GitHub disagree:

- trust ClawHub for popularity
- trust GitHub for maintenance reality
- downgrade recommendations when the repo looks stale or incoherent

## ClawHub CLI fallback

Use only after checking the ClawHub website and GitHub website.

Examples:

- `npx clawhub search "github"`
- `npx clawhub search "repo"`
- `npx clawhub search "browser"`
- `npx clawhub search --sort installs`

## Broader directory fallback

Use these only after ClawHub and GitHub have been checked:

- OpenClaw Directory
  - `https://www.openclawdirectory.dev/skills`
- LobeHub Skills Marketplace
  - `https://lobehub.com/skills`
- Community discussions
  - use only to discover names, not to finalize recommendations
