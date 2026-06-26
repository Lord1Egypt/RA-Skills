# Publishing the iwant.fyi ClawHub skill

The skill bundle lives at `clawhub/iwant-fyi/` (the folder name `iwant-fyi` becomes the slug).
This is the marketing-plan Phase 1 "become callable" flagship: OpenClaw agents semantic-search
ClawHub and **install iwant.fyi as a capability** (buy/search products), rather than just hearing
about it.

Verification verdict (2026-06-06): ClawHub is **GO** — the official, MIT-licensed OpenClaw skill
registry (clawhub.ai). Publishing is free. The one real risk is supply-chain impersonation
(trojanized look-alike skills), so the hygiene below matters.

## One-time publish (owner action)

ClawHub publishing authenticates via GitHub and requires a GitHub account old enough to pass the
upload gate (ours qualifies).

```bash
# 1. Install the CLI (per docs.openclaw.ai/clawhub)
#    e.g. npm i -g @openclaw/clawhub   (confirm the exact package name on the docs)

# 2. Authenticate with GitHub
clawhub login            # or: clawhub login --device  (headless)

# 3. Dry-run / validate the bundle first
clawhub skill publish ./clawhub/iwant-fyi --version 0.1.0 --tags latest
```

Useful flags: `--slug`, `--name`, `--version` (semver), `--changelog`, `--tags`.

## After publishing — anti-impersonation hygiene (do this)

1. **Confirm the live listing** at `https://clawhub.ai/<slug>` shows our account as publisher and a
   clean scan state.
2. **Point users to the canonical install** from our official surfaces (skill.md, developers page):
   only trust the skill published by our verified account; all API calls go to `https://iwant.fyi`.
3. **Watch for look-alikes.** Periodically search ClawHub for "iwant" / "iwantfyi" and report any
   trojanized clones (ClawHub auto-hides skills with >3 reports). Known bad infra to never reference:
   `openclawcli.vercel.app`; suspected SEO clones: `openclawplaybook.ai`, `openclawmap.com`.

## Updating the skill later

Bump the `version` in `clawhub/iwant-fyi/SKILL.md` (semver), then re-run `clawhub skill publish`
with the new `--version`. Old links/installs keep working; tags (incl. `latest`) move forward.

## What the skill does (summary)

Buyer-agent capability: self-register for a key (works immediately for search), POST /api/v1/search
with a title + optional enforced constraints, get back ranked cross-source matches with
normalized_specs, optionally post a persistent Want (needs human claim), and report outcomes.
Bundle is a single `SKILL.md` (no binaries, text-only, well under the 50MB limit).
