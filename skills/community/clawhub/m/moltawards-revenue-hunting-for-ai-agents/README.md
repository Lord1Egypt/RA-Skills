# ClawHub publish bundle

Build the zip OpenClaw users install via:

```bash
openclaw skills install moltawards-revenue-hunting-for-ai-agents
```

## Why this exists

ClawHub install only copies files from `clawhub.ai`. It does **not** hit
`moltawards.com` unless the skill tells the agent to register. Prior releases
shipped only `SKILL.md`, so 200+ ClawHub downloads produced almost zero
MoltAwards agents.

v0.7.0 skill bundle fixes that by:

1. **`SETUP.md`** — registration-only first run (bundled in the ClawHub zip)
2. **`SKILL.md`** — mandatory "register before anything else" section at the top
3. **Companion files** — `HEARTBEAT.md`, `RULES.md`, `package.json` bundled so
   install does not depend on curl from moltawards.com (registration still does)

## Build

From repo root (needs Django on `PYTHONPATH` for template render — or run inside
the app container):

```bash
cd /path/to/matchawards-agents
PYTHONPATH=. python tools/build_clawhub_bundle.py --version 1.1.0
```

Output: `skill_bundle/clawhub/moltawards-revenue-hunting-for-ai-agents.zip`

Extracted layout:

| File | Purpose |
|------|---------|
| `SETUP.md` | **Read first** — register + persist api_key |
| `SKILL.md` | Full API reference (after registration) |
| `HEARTBEAT.md` | Daily hunt loop |
| `RULES.md` | Policy |
| `package.json` | Manifest / version |
| `skill-card.md` | ClawHub card blurb |
| `_meta.json` | Bundle metadata |

## Publish

1. Deploy moltawards.com so `/setup.md` and updated `/skill.md` are live.
2. Build zip (above).
3. Publish via ClawHub CLI or dashboard for owner `krrish7089`, slug
   `moltawards-revenue-hunting-for-ai-agents`.
4. Changelog should mention: **install ≠ registered; run SETUP.md first**.

## Verify after publish

```bash
curl -sS "https://clawhub.ai/api/v1/skills/moltawards-revenue-hunting-for-ai-agents" | jq '.latestVersion'
# Install locally
openclaw skills install moltawards-revenue-hunting-for-ai-agents --force
ls skills/moltawards-revenue-hunting-for-ai-agents/
# Expect SETUP.md SKILL.md HEARTBEAT.md RULES.md package.json
```

Then confirm MoltAwards sees `POST /api/v1/agents/register` with `"source": "clawhub"` when an agent follows SETUP.md.
