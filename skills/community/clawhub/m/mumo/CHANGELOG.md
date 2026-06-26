# Changelog

## 0.4.0 — 2026-06-19

Skill triggering + prompt-voice updates.

- Triggering: dropped the "contested" gate — the description now leads with pre-implementation review (esp. anything touching auth, security, tokens, payments, data exposure, or migrations), not "contested decisions only."
- Author-bias counter (When to use): if you authored the plan or code under review, that's a reason FOR a panel — the author is the worst-positioned reviewer of their own work.
- New "Prompt voice" section: write the prompt first-person as the operator, not "You are X" case-study framing.
- Surface `claim_map_url` after each round so the user can open the claim map directly.

## 0.1.2 — 2026-05-22

README update.

## 0.1.1 — 2026-05-06

License switched from standard MIT to MIT-0 (MIT No Attribution) to match ClawHub's published-skill license requirement. MIT-0 is strictly more permissive than MIT — drops the "must include copyright notice" clause; everything else identical. Doesn't affect runtime, install, or distribution.

## 0.1.0 — 2026-05-06

Initial release. OpenClaw skill + MCP config for mumo's multi-model deliberation server.

- `SKILL.md` — kernel teaching the deliberation loop, snippet doctrine, claim-map reading, when-to-invoke triggers, verification discipline (real session IDs are UUIDs; verify with `list_sessions` if uncertain), and a **"Framing prompts for the panel"** section that tells the agent NOT to pass user role-instructions verbatim — translate to first-person moderator context so panel models advise the agent rather than roleplaying it. AgentSkills-compatible frontmatter (single-line per OpenClaw's parser; `metadata` as single-line JSON).
- `config/mumo.example.json` — reference payload for `openclaw mcp set mumo` (named `.example.json` to telegraph "OpenClaw does not auto-load this file; it's the JSON shape to paste into the CLI"). Streamable HTTP transport against `https://mumo.chat/api/mcp` with literal Bearer auth in the `headers` map (OpenClaw's MCP client doesn't support env-var pointers for HTTP headers; users paste the `mmo_live_*` key directly into the JSON).
- `playbooks/` — four cognitive-shape playbooks: `contested-decision`, `design-review`, `uncertainty-expansion`, `red-team`.
- `references/` — five reference docs: `claim-maps`, `snippets`, `model-selection`, `synthesis`, `operating-notes`. OpenClaw's auto-loader doesn't care about the directory name, only `SKILL.md`.
- README install steps: `openclaw mcp set mumo` for the server, `git clone … ~/.openclaw/skills/mumo` for the skill, restart OpenClaw, run the first deliberation.

Tool naming note: OpenClaw exposes MCP tools to the agent as `<server>__<tool>` (double underscore). So mumo's seven tools surface as `mumo__create_deliberation`, `mumo__wait_for_round`, etc. The SKILL.md uses canonical (unprefixed) tool names since the prefix is OpenClaw-specific; the agent maps them automatically.
