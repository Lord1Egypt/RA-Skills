# HowToUseHumans heartbeat

Lightweight checklist for humans and agents maintaining this collection or the site. Run or review on a rhythm that fits your risk tolerance (weekly for active development, monthly for stable installs).

## Collection integrity

- After adding or renaming a skill under `skills/<slug>/`, run `npm run build:skills` (or full `npm run build`) so `src/data/skills.generated.ts` and `public/skills/` stay in sync. The same run refreshes the ClawHub slug list in `skills/howtousehumans/SKILL.md` (between the `HOWTOUSEHUMANS_SKILL_CATALOG` HTML comments).

## Publish paths

- ClawHub: from repo root, `npm run skills:prepare` then `npm run clawhub:dry-run` / `npm run clawhub:publish` as documented in [DEVELOPMENT.md](../../DEVELOPMENT.md). Prefer `clawhub:publish-missing` when you only need new skills on the registry.
- GitHub mirror: `npm run github:skills-mirror` (or via `skills:prepare`) and sync `dist/github-skills/` to the public skills repo if that is part of your release.

## Site and automation

- Hit [howtousehumans.com](https://howtousehumans.com) and a few skill detail URLs; confirm `sitemap.xml` and `robots.txt` look sane if you changed routing or env base URLs.
- If you use cron or serverless jobs (for example skill tweets), verify required secrets in the host environment and that scheduled routes still return success in logs.

## Install smoke test

- From a clean machine or container: `npx clawhub install howtousehumans` and confirm you receive this pack’s `SKILL.md` and `heartbeat.md` alongside the rest of the collection layout your client expects.
