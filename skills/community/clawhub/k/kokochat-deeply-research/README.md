# kokochat-deeply-research

OpenClaw skill for the KokoChat **Deeply** mini-app's "深度调研课程" entry.
When the user fills in a topic from the "定制课程" sheet, the deeply agent
runs this skill to do Phase A: a real research pass + a `notes` fenced block.
KokoChat then runs Phase B separately to turn those notes into a course outline.

The skill is **prompt-only** — it has no `bin/`. Search goes through the
shared `kokochat-search` wrapper skill, which calls KokoChat's hosted
search proxy (`https://deeply.plus/deeply/search`). Fetching result pages still
uses OpenClaw's built-in `web_fetch`.

## Install / update

Run from the repo root:

```bash
pnpm openclaw:install
```

This copies `kokochat-deeply-research` and `kokochat-search` into
`~/.openclaw/agents/deeply/workspace/skills/`, adds both skills to the deeply
agent's allowlist, and writes the deeply agent's tool config
(`profile=minimal`, allowlisted `exec`, and `web_fetch`). Then restart the
gateway so config + skill text get reloaded:

```bash
launchctl kickstart -k "gui/$(id -u)/ai.openclaw.gateway"
```

## Search provider

Deeply research does not depend on the user's `tools.web.search.provider`.
KokoChat-hosted search is configured on the `deeply.plus` server (Brave-backed
in production), so users do not need to store a Brave API key in their own
OpenClaw config.

If hosted search returns no results or errors out, the agent is instructed
to be honest with the user in its narration — it won't hallucinate URLs
to fill the `sources` array.

## Output schema

The agent's job per `SKILL.md` is to:

1. Narrate the research process in flowing Chinese (with `〔KP〕` sentinel
   at the end of each prose paragraph — see SKILL.md for why).
2. Call `kokochat-search/bin/search.mjs` 1–3 times (and optionally
   `web_fetch` on key URLs) to gather real sources.
3. End the reply with exactly one fenced block tagged
   `koko.deeply.research.notes` containing a JSON `{ topic, synthesis,
   sources }`. Every `url` in `sources` must come from a real hosted search /
   `web_fetch` result.

The KokoChat client parses that notes block, runs Phase B (`inferOnce`) to
produce `koko.deeply.research.outline`, writes the outline + sources to
mini-app storage, flips bootstrap to `ready`, and the user flows into normal
mainline lecture mode.
