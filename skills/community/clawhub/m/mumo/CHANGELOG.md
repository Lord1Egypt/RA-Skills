# Changelog

## 0.6.2 — 2026-09-09

Credential-hygiene guidance. The registration payload now references `${MUMO_API_KEY}` in the `Authorization` header instead of carrying a `mmo_live_YOUR_KEY_HERE` placeholder for the user to overwrite, and the key belongs in `~/.openclaw/.env`. OpenClaw resolves the reference at connect time and names a missing variable in a startup config warning, so a rotated or unset key surfaces as a named warning rather than a silent 401. Rotation no longer means re-registering the server.

Also corrects the skill install location: `openclaw skills install mumo` installs into the active workspace's `skills/` directory (`--agent <id>` targets another), not `~/.openclaw/skills/mumo/`. The git-clone path is what puts it at a fixed location.

The `.env` step creates and `chmod 600`s the file before the key goes in, and tells you to edit it rather than append from the shell — a command carrying the literal key lands in shell history, and a second run stacks a duplicate entry. New step 5 verifies the connection with a real, free `mumo__list_models` call through the agent before the first deliberation — `openclaw mcp list` and `mcp show` only report saved config and never open a connection.

## 0.6.1 — 2026-09-08

Registry-only release: the ClawHub display name is `mumo` again (the 0.6.0 publish omitted `--name`, and the CLI derived "Mumo Openclaw" from the folder). No skill content changes.

## 0.6.0 — 2026-09-08

Coordinated client release rendered from the mumo-mcp 0.6.0 baseline.

- `SKILL.md`: `share_session` in the tools table (OpenClaw sets no tool allowlist, so the tool was already reachable — this is the documentation catching up); `wait_for_round` one-id form; intro names the current model families and the typed cross-model reactions.
- `references/operating-notes.md` re-synced with the baseline.
- README tool list and intro updated.

## 0.5.0 — 2026-07-04

Reaction-visibility model + per-round Takeaway.

- New "Reactions are in the ledger, responses are on the record" section: participants never see each other's reactions — each model weaves its own prior reactions into its next response, and the claim map is the moderator's privileged preview. Moderator snippets are the one path that puts ledger content directly in front of the panel.
- Pacing note in "When to continue": positions develop across rounds — a reaction gets woven into the next round's prose, which draws reactions of its own a round later.
- Takeaway: `takeaway: true` (create + append) generates `round_takeaway` (`bottom_line` + `items[]`), the per-round summary. New `references/takeaway.md` (replaces `references/recap.md`).

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
