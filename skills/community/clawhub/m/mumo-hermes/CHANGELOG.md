# Changelog

## 0.6.3 — 2026-09-09

Credential-hygiene guidance. `config/mumo.yaml` now references `${MUMO_API_KEY}` in the `Authorization` header instead of carrying a `mmo_live_YOUR_KEY_HERE` placeholder for the user to overwrite, and the key belongs in `~/.hermes/.env` — the file Hermes designates for secrets. This also closes a gap in the hub install: Hermes already prompted for `MUMO_API_KEY` and wrote it to `.env`, but the shipped config ignored that value and asked for a literal instead, so the stored key went unused.

README and SKILL.md setup steps updated to match, and the README no longer says a hub install "handles the MCP server registration" — Hermes prompts for the key and saves it; the `mcp_servers` block is still added by hand.

The `.env` step creates and `chmod 600`s the file before the key goes in, and tells you to edit it rather than append from the shell — a command carrying the literal key lands in shell history, and a second run stacks a duplicate entry. A new verification step runs `hermes mcp test mumo` — a real connection that lists the tools — before the first deliberation; `hermes mcp list` only reports saved config and cannot show whether the key resolved.

## 0.6.2 — 2026-09-08

Registry-only: the ClawHub display name is `mumo (Hermes Agent)` again (the 0.6.1 publish omitted `--name`), and the install command uses the `clawhub/mumo-hermes` form the Hermes skills catalog generates.

## 0.6.1 — 2026-09-08

Distribution correction. There is no separate "HermesHub" registry: the Hermes CLI's Skills Hub resolves `hermes skills search mumo` to ClawHub, where the bare `mumo` slug is the OpenClaw skill. This skill is now published on ClawHub as `mumo-hermes`, and the README and `SKILL.md` setup notes point at `hermes skills install mumo-hermes` instead of "HermesHub". No tool or loop changes.

## 0.6.0 — 2026-09-08

Coordinated client release rendered from the mumo-mcp 0.6.0 baseline.

- `config/mumo.yaml` `tools.include` gains `share_session` — the tool was registered on the server but filtered out by the allowlist until now.
- `SKILL.md` (frontmatter `version: 0.6.0`): `share_session` in the tools table; `wait_for_round` taught in its one-id form (`session_id` alone resolves to the round in flight; `round_id` only for an earlier round); intro names the current model families and the typed cross-model reactions.
- `references/operating-notes.md` re-synced with the baseline (the `/progress` diagnostic-polling section).
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

## 0.1.6 — 2026-05-22

CHANGELOG update.

## 0.1.5 — 2026-05-22

Cosmetic alignment to the conventions used by approved optional skills in the `NousResearch/hermes-agent` catalog (sampled `dcf-model`, `kanban-video-orchestrator`, `concept-diagrams`). No functional changes.

- **`version` unquoted** — `version: "0.1.4"` → `version: 0.1.5`. YAML parses both as the same string; matches the unquoted style every approved optional skill uses.
- **Tags lowercased** — `Deliberation`, `Decision-Support`, `Multi-Model`, `Design-Review`, `Architecture-Review`, `Plan-Review`, `MCP` → `deliberation`, `decision-support`, `multi-model`, `design-review`, `architecture-review`, `plan-review`, `mcp`. Tags are author-defined free text; lowercase is the source-of-truth convention. (Title-Case in earlier samples was just the docs-site display rendering.)
- **`required_environment_variables` + `metadata.hermes.requires_tools` retained.** Neither field appears in the optional-skill samples we checked, but both are per the canonical `creating-skills` developer-guide doc. Keeping them means: hub-installed users get the interactive `MUMO_API_KEY` prompt (if Hermes honors the field) and the skill auto-hides when mumo MCP isn't registered. Both should be harmlessly ignored by parsers that don't recognize them.

## 0.1.4 — 2026-05-21

Re-categorized, frontmatter realigned to canonical Hermes schema, and SKILL.md content refreshed against the canonical docs (creating-skills, mcp-config-reference, skills user-guide) and real bundled-skill frontmatter (`claude-code`, `native-mcp`, `mcporter`, `fastmcp`).

- **Re-categorized to `software-development/`.** Install path is now `~/.hermes/skills/software-development/mumo`. The `autonomous-ai-agents/` cluster is for skills that delegate to another autonomous agent. mumo is a tool the native Hermes agent calls to run a deliberation panel — the structured-methodology-before-acting cousin of `writing-plans`, `plan`, and `requesting-code-review`.
- **Frontmatter cleanup.** `author` moved back to top-level (v0.1.3 had it under `metadata.author`; real hub skills like `claude-code` and `native-mcp` use top-level). Dropped `compatibility` and `metadata.hermes.category: agents` — neither is in the canonical schema. Added `platforms: [linux, macos, windows]`, `required_environment_variables` for `MUMO_API_KEY` (enables the interactive install prompt for hub installs), and `metadata.hermes.related_skills: [writing-plans, plan, requesting-code-review]`.
- **`metadata.hermes.requires_tools: [mcp_mumo_create_deliberation]`** — hides the skill from all discovery surfaces (system prompt index, `skills_list()`, `/mumo` slash command) when mumo's MCP server isn't registered. Prevents users from seeing a skill they can't use.
- **Tags restructured** to 7 Title-Case keywords matching real-world hub-skill style: `Deliberation`, `Decision-Support`, `Multi-Model`, `Design-Review`, `Architecture-Review`, `Plan-Review`, `MCP`. The `[Category, Subcategory, Keywords]` positional convention from the dev docs turned out to be aspirational — real skills use flat capitalized lists.
- **Description rewritten** to lead with a WHAT verb and explicit "Use when..." clause. Drops the "Requires the mumo MCP server to be configured" tail since `requires_tools` handles that precondition structurally.
- **MCP config polish** (`config/mumo.yaml`): added `supports_parallel_tool_calls: true`; explicit `connect_timeout: 60` + `timeout: 180` aligned with `wait_for_round` defaults.
- **README rewritten** around the new positioning. `hermes skills install mumo` from HermesHub is the recommended install (prompts for `MUMO_API_KEY` automatically); git-clone fallback documented with the new path. `/mumo` slash-command invocation called out — Hermes skills are explicitly invoked, never auto-triggered.
- **`reference/` → `references/`** (plural). Added `recap.md` covering the `recap_round` / `recap_session` flags from the recent MCP server iteration.

## 0.1.3 — 2026-05-05

Frontmatter aligned with HermesHub conventions after sampling existing hub skills (notion-integration, api-builder, agent-hardening, synapse-swarm). v0.1.2 used the generic agentskills.io shape; this matches what the hub actually ships.

- **`version`** now string-quoted (`"0.1.3"`).
- **`author`** moved under `metadata.author` (hub convention; top-level `author` is non-canonical for hermeshub).
- **`compatibility`** field added — pointer to `mumo.chat/settings/api-keys` for the platform key.
- **`metadata.hermes.category: agents`** — same bucket as synapse-swarm and paperclip (multi-agent collaboration).
- **Tags** rewritten in flow style to match hub convention.

## 0.1.2 — 2026-05-05

Frontmatter cleanup ahead of HermesHub submission. No body changes.

- **Frontmatter completed** — added `version`, `author`, `license`, and `metadata.hermes.tags` (deliberation, multi-model, mcp, decision-support, ai-tooling) per Hermes' creating-skills guide. Brings v0.1.x in line with hub frontmatter conventions.

## 0.1.1 — 2026-05-05

Skill refinements from first real Hermes deliberation, plus a layout fix. The v0.1.0 skill produced clean end-to-end behavior (real tool calls, auto-chained wait, confident synthesis); these edits sharpen the framing.

- **Repo restructured** — root is now the skill root (was `skills/mumo/`). Cloning the repo into `~/.hermes/skills/<category>/mumo/` now places `SKILL.md` at the canonical path Hermes' scanner expects, instead of one level too deep.
- **"When to use" reframed** around the three conditions Hermes' own synthesis identified: wide solution space + hidden failure space; medium-high confidence + anchoring risk; irreversible consequences. The longer trigger taxonomy stays as supporting detail. Added the "cognitive load balancer" framing to position mumo against your reasoning, not as a replacement for it.
- **Long-wait guidance** in basic loop step 3: 15–120s is normal, 60+ seconds isn't a failure signal. Tell the user upfront so the wait doesn't feel broken.
- **Recovery section** for lost session context: use `list_sessions` to find your latest session by prompt match, then `get_session` or `wait_for_round` instead of starting a duplicate deliberation.
- **Terminology section** distinguishing panel/models/participants (what mumo invokes on its backend) from subagent (your own delegation infrastructure). Hermes' first synthesis conflated the two; this section heads off the category error in future synthesis.

## 0.1.0 — 2026-05-05

Initial release. Hermes Agent skill for mumo's MCP server.

- `skills/mumo/SKILL.md` — kernel teaching the deliberation loop, snippet doctrine, claim-map reading, when-to-invoke triggers, and the verification discipline (real session IDs are UUIDs; verify with `list_sessions` if uncertain).
- `skills/mumo/playbooks/` — four cognitive-shape playbooks: `contested-decision`, `design-review`, `uncertainty-expansion`, `red-team`.
- `skills/mumo/reference/` — five reference docs: `claim-maps`, `snippets`, `model-selection`, `synthesis`, `operating-notes`.
- `config/mumo.yaml` — MCP server entry to merge into `~/.hermes/config.yaml` with `tools.include` allowlist scoping mumo to its seven tools.
- README install steps: clone repo into `~/.hermes/skills/`, add YAML config, restart Hermes.
