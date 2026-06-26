---
name: hkipo-orchestrator
description: Coordinate the end-to-end Hong Kong IPO workflow across discovery, snapshot extraction, personalization, scoring, and review optimization. Use when the user wants one skill to choose the next step across the full HK IPO research loop.
version: 0.1.0
metadata: {"openclaw":{"emoji":"🧭","requires":{"bins":["uv"],"config":["~/.hkipo-next/config/profile.json","~/.hkipo-next/config/watchlist.json","~/.hkipo-next/data/hkipo.db"]},"install":[{"id":"install-uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv with Homebrew","os":["darwin","linux"]}]}}
---

# HK IPO Orchestrator

Use this skill when the request spans multiple stages and you need to route the work to the right HK IPO skill.

## Companion Skill Map

- `$hkipo-calendar-monitor`: discover near-term IPO events
- `$hkipo-snapshot-extractor`: extract one-symbol facts and quality signals
- `$hkipo-profile-watchlist-manager`: manage personalized settings and watchlists
- `$hkipo-parameter-manager`: tune scoring rules and active versions
- `$hkipo-decision-engine`: produce scores, decision cards, and batches
- `$hkipo-review-optimizer`: update actual outcomes and process suggestions

## Default Flow

1. Discover the market.
2. Extract structured facts for shortlisted symbols.
3. Ensure profile and watchlist state is ready when the task is personalized.
4. Ensure an active parameter version exists before scoring.
5. Produce score or decision outputs.
6. Close the loop later with review and suggestions.

## Operating Rules

- Prefer JSON between machine steps and concise text or markdown for final user-facing output.
- Surface degraded or partial data instead of hiding it.
- Warn before mutating profile, watchlist, parameter, or review history when that side effect matters.
- Do not run repeated score or batch jobs casually, because those commands create review records.
