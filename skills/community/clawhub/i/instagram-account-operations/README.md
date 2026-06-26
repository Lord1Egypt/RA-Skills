# Instagram Account Operations

> Operating doctrine for Instagram automation — careful creator + business pattern via Meta Business Suite, role separation, action-block awareness (24h/7d/permanent), comment + DM ops, reply qualification, hashtag-shadowban discipline, and recovery patterns.

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](#changelog)

A Claude Code / OpenClaw skill for running Instagram brand accounts safely. Battle-tested in a regulated-field operation, ported to be domain-agnostic.

**Why most Instagram automation triggers action blocks**: it scripts `instagram.com` directly, ignoring Meta Business Suite. This doctrine doesn't — MBS is the canonical surface.

---

## What's in the box

- **3-role mental model** for any IG account (`ig-post` / `ig-engage` / `ig-stealth`)
- **MBS-first doctrine**: every reactive op (DMs, comments) goes through `business.facebook.com`, not `instagram.com` directly — fewer iframes, Playwright `click + type + Enter` works, link previews auto-generated
- **Action-block-phased posting**: Phase A (account < 30d, recent block, or < 500 followers) → Phase B (full doctrine) — with **manual override path** for grandfathered businesses
- **Zero-outgoing-link policy** in comments (max 1 URL in DMs, only the `<PRIMARY_CTA>`)
- **The known MBS comment-Reply navigation bug + workaround** (use `@username` prefix + page-level textarea + send-arrow click)
- **Strict reply qualification**: skip Reel-shares-without-question, recognize existing clients (no prospect CTA), 7-day per-user cap
- **Hard quotas** calibrated under IG's observed action-block thresholds (follow/unfollow, DMs to non-followers, likes per hour)
- **Anti-spam triggers**: same-opening-phrase ban, shorteners ban, "DM me + WhatsApp me + click here" stacked-CTA ban
- **Hashtag-state tracking**: registry for shadowbanned tags, no over-tagging (3-5 max)
- **Full recovery playbook**: action blocks, soft logouts, "Reauthenticate" banner, shadowban suspicion, automod removals
- **Memory file inventory** for stateful agents
- **Mandatory recap pattern** (alert channel + memory)

---

## Install

### Via ClawHub

The skill is designed to be published on ClawHub — install in one click from your agent once published.

### Manual copy

```bash
mkdir -p ~/.claude/skills/instagram-account-operations
cp SKILL.md ~/.claude/skills/instagram-account-operations/
```

Or for OpenClaw:

```bash
mkdir -p ~/.openclaw/skills/instagram-account-operations
cp SKILL.md ~/.openclaw/skills/instagram-account-operations/
```

---

## Quick start

1. Open `SKILL.md` and fill the placeholders in **Section 0** (brand, domain, handle, `<META_BUSINESS_ID>`, `<META_ASSET_ID>`, browser profile, port, niche keywords, primary CTA, workspace dir).
2. Confirm your IG account is **Business** or **Creator** AND linked to a Meta Business Suite asset.
3. Extract `<META_BUSINESS_ID>` and `<META_ASSET_ID>` from the MBS URL once you're logged in.
4. Wire your crons (e.g. DM check `*/15`, comment check `10,25,40,55`, browser-health `hourly`).
5. **Start in Phase A** until account_age ≥ 30 days AND followers ≥ 500 AND no recent action block. Don't shortcut.
6. Daily check on `Account Status` (MBS → Settings → Account Status): **green / no warning**.

Shell snippets in the skill use the [OpenClaw](https://openclaw.ai) browser CLI as an example automation stack. Swap them for Playwright (Node or Python), Puppeteer, Chrome MCP, or any CDP-capable tool — the doctrine is stack-agnostic.

---

## Who is this for

Any niche where the brand needs to be a *background* signal behind genuinely useful posts and DMs:

- **Legal services** (origin of the doctrine — works under strict bar association rules)
- **Medical / health** practitioners with public-content strategies
- **Financial advisors** subject to compliance constraints
- **SaaS / B2B founders** doing community-led growth
- **Creators / agencies** managing brand accounts on behalf of clients

Anywhere action-block = reach death.

---

## Repository structure

```
instagram-account-operations/
├── SKILL.md         # the skill (full doctrine)
├── README.md        # this file
├── LICENSE          # MIT-0
└── CHANGELOG.md     # version history (TBD)
```

---

## Companion skills

- **facebook-account-operations** — same MBS backbone, FB-Page-specific doctrine.
- **tiktok-account-operations** — for TikTok ops (separate browser-suite surface).
- **whatsapp-account-operations** — for BSP-API-driven WhatsApp Business ops (the downstream conversion channel).
- **[reddit-account-operations](https://github.com/AlexBloch-IA/reddit-account-operations)** + **[twitter-account-operations](https://github.com/AlexBloch-IA/twitter-account-operations)** — same doctrine family on other platforms.

---

## License

Released under **MIT-0** (MIT No Attribution). Use, fork, adapt, redistribute. No attribution required.
