# `thepit/moat-trader` — package README

**Developer-oriented notes for the `thepit-skill` monorepo package.**
For user-facing install + usage docs, see [`SKILL.md`](./SKILL.md).
For the security audit, see [`SECURITY.md`](./SECURITY.md).

This directory is a standalone OpenClaw skill published to ClawHub
at the slug `thepit/moat-trader`. Users install it via:

```bash
openclaw skills install thepit/moat-trader
```

## Package layout

```
packages/thepit-skill/
├── SKILL.md               ← User-facing skill documentation
├── README.md              ← This file — package dev notes
├── SECURITY.md            ← Audit trail for security-minded users
├── CHANGELOG.md           ← Semver release notes
├── PUBLISHING.md          ← How to publish a new version to ClawHub
├── package.json           ← Monorepo marker (not npm-published)
├── clawhub.json           ← ClawHub publish manifest
├── install.sh             ← One-time interactive setup
├── heartbeat.sh           ← Per-minute cron-invoked decision loop
├── prompt-template.md     ← LLM prompt with mustache placeholders
├── config.example.json    ← Template for ~/.thepit/config.json
├── personas/              ← Preset SOUL.md personality templates
│   ├── presets.json
│   ├── momentum-scalper/SOUL.md
│   ├── contrarian-counter/SOUL.md
│   └── social-follower/SOUL.md
└── submissions/           ← Drafts for community distribution
    ├── README.md          ← Submission status tracker
    ├── awesome-openclaw-skills.md
    ├── awesome-openclaw-agents.md
    ├── discord-announcement.md
    └── hacker-news-show-hn.md
```

## Coupling with the rest of the monorepo

This skill is **designed to be self-contained** — when it ships to
ClawHub, only these files go. But during development two points of
contact exist:

1. **API register endpoint** (`apps/api/src/routes/external.ts`)
   consumes the same preset metadata that lives in
   `personas/presets.json`. The server-side copy lives at
   `apps/api/src/lib/persona-presets.ts` with the SOUL.md bodies
   inlined. When you add or edit a preset, update BOTH:
   - `packages/thepit-skill/personas/<slug>/SOUL.md` (source of truth)
   - `packages/thepit-skill/personas/presets.json` (index)
   - `apps/api/src/lib/persona-presets.ts` (server cache)

2. **Register UI** (`apps/web/app/moat/register/_components/persona-picker.tsx`)
   fetches presets from `GET /external/personas` so it stays in sync
   with the server. If that endpoint is unreachable, the UI falls
   back to a hardcoded `FALLBACK_PRESETS` list — keep that in sync
   too (small metadata only, no SOUL.md body).

Future cleanup: extract presets into a shared package
(`@thepit/personas`?) that both the skill, the API, and the web import.
Not a priority at v0.1 since presets rarely change.

## Developing

There's no build step. All files in this directory are consumed
as-is by:

- Users' OpenClaw installs (via ClawHub download)
- Our `/moat/register` UI (via the API endpoint)
- Our external API (via inlined persona-presets.ts)

To validate a local edit:

```bash
# 1. Shell scripts pass shellcheck
shellcheck install.sh heartbeat.sh

# 2. JSON manifests parse
jq . clawhub.json
jq . personas/presets.json

# 3. SOUL.md files stay under the 4000-char SOUL.md cap
wc -c personas/*/SOUL.md

# 4. Presets.json matches the on-disk SOUL.md files
for slug in $(jq -r '.presets[].slug' personas/presets.json); do
  test -f "personas/$slug/SOUL.md" || echo "MISSING: $slug"
done
```

## Publishing a new version

See [`PUBLISHING.md`](./PUBLISHING.md) for the full flow. Summary:

1. Bump `version` in `clawhub.json` + `package.json`.
2. Update `CHANGELOG.md` with the release notes.
3. Run `clawhub skill publish . --slug thepit/moat-trader
   --version X.Y.Z --tags trading,solana,latest`.
4. Tag the monorepo commit: `git tag thepit-skill-vX.Y.Z`.

## Community distribution

Skill discoverability is driven by a few external lists — see
[`submissions/`](./submissions/) for PR drafts we maintain to keep
them up to date.

## License

MIT. See LICENSE in the repo root.
