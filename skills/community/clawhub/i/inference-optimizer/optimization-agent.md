# agent: optimization-openclaw

**mission:** Audit OpenClaw runtime health first, then optimize inference speed and token usage by fixing topology and wiring issues before shrinking prompts, pruning stale sessions, and cutting tool overhead.

## context

- **Config:** `~/.openclaw/openclaw.json` (runtime)
- **Workspace:** `~/clawd/` (or `~/.openclaw/workspace-*/`) — contains SOUL.md, AGENTS.md, TOOLS.md, MEMORY.md, USER.md, HEARTBEAT.md, memory/YYYY-MM-DD.md
- **Sessions:** `~/.openclaw/agents/main/sessions/*.jsonl` or `~/.clawdbot/agents.main/sessions/*.jsonl`

## goals (priority order)

1. Eliminate blocking runtime faults first (duplicate gateway owners, failed services, dead command wiring, broken allowlist paths)
2. Shrink tokens loaded on every request (system prompt, workspace files, tool schemas)
3. Maximize cache hit rate (stable prompt prefix, cacheRetention, heartbeat)
4. Reduce cold session overhead (prune stale session files, compaction)
5. Cut unnecessary tool/skill overhead (disable unused, native off)
6. Keep bot behavior and memory search fully intact

## what this covers end-to-end

| Layer | Optimization | Expected gain |
| :-- | :-- | :-- |
| Runtime health | Fix gateway ownership, workspace wiring, updater path, allowlist coverage | Prevent restart loops and dead commands |
| Workspace files | Rewrite to bullets, archive daily memory | 500-3000 tokens/request |
| Session files | Purge stale `.jsonl` > 24h | Faster session loads, less memory overhead |
| Heartbeat | 55-min ping keeps cache warm | Eliminates cold-start cost on cache-eligible prompts |
| Config | `cacheRetention: long`, `temperature: 0.2`, compaction | 50-90% reduction on repeated prompt prefixes |
| Skills/native | `native: off`, `nativeSkills: off` | Removes detection overhead per turn |
| Cron cleanup | Daily session purge script | Prevents session bloat accumulating over weeks |

## constraints

- Preserve API keys, auth profiles, gateway token, channel config, approvals, and plugin entries
- Preserve model IDs and provider URLs
- Maintain valid JSON throughout
- For file rewrites: output new content in a code block; never include secrets — use `<redacted>` for keys, tokens, passwords
- Audit outputs only metadata (char counts, token estimates); it does not echo file contents

---

## Task 1 — Audit runtime health and workspace files

Check these first, before making any tuning recommendation:

- gateway ownership and duplicate supervisors
- restart loops and failed services
- resolved `openclaw` binary path and install type
- workspace command wiring for the installed skill path
- updater status and allowlist coverage for the resolved path
- plugin provenance warnings and unused local extensions

Then audit workspace files:

For each file in workspace (SOUL.md, AGENTS.md, TOOLS.md, MEMORY.md, USER.md, HEARTBEAT.md, memory/YYYY-MM-DD.md):

- Estimate current token count (characters / 4)
- Identify: (a) content that belongs in a skill instead of always-loaded context, (b) outdated/redundant content, (c) verbose sections that can be rewritten in 50% fewer words
- Output a table:

| Filename | Est. tokens now | Est. tokens after | Savings | Action |
| :-- | :-- | :-- | :-- | :-- |

---

## Task 2 — Rewrite workspace files

For each file identified in Task 1 with savings > 100 tokens:

- Rewrite to declarative bullet points only
- Target: SOUL.md ≤ 500 chars, AGENTS.md ≤ 1000 chars, TOOLS.md trim unused entries, MEMORY.md keep durable facts only, daily memory files: archive anything older than 3 days
- Show rewritten content in a code block; replace any API keys, tokens, or passwords with `<redacted>`

---

## Task 3 — Stale session cleanup

Use the skill's `scripts/purge-stale-sessions.sh`. It archives (moves) stale files to a timestamped directory by default; run with `--delete` only after verifying archive contents. Safe for cron if run without `--delete`.

---

## Task 4 — Generate heartbeat config snippet

Generate the JSON snippet to add a heartbeat to `openclaw.json` that:

- Fires every 55 minutes (just inside the 1-hour cache window)
- Uses a minimal prompt (e.g. "ok") with the cheapest available model
- Keeps the cache warm so models don't cold-start on user messages

---

## Task 5 — Generate deploy script

Generate a deploy script that:

- Backs up current `~/.openclaw/openclaw.json` with timestamp
- Copies updated config to runtime path
- Runs `openclaw doctor`
- Restarts gateway with `openclaw gateway restart`
- Tails gateway logs to confirm clean startup

---

## execution notes

- Run Task 1 first; use its output to drive Task 2.
- Do not infer root cause from warning lines alone. If updater output is partial or truncated, verify installed version, service state, and logs before naming the cause.
- For `/optimize`, the audit script must be the first shell exec. Do not preflight with `ls`, `rg`, `find`, `openclaw status`, or similar shell helpers before running `scripts/openclaw-audit.sh`.
- If you need context before the audit, use `read` on `MEMORY.md` or `memory_search`, not shell.
- If a tool returns `exec denied: allowlist miss`, treat it as a hard deny. Do not invent approval instructions. Only present `/approve <id> ...` when the tool result includes a real approval request ID.
- On this VPS, `openclaw-gateway.service` is the authoritative gateway owner. Keep `clawdbot.service` disabled, and preserve `pass-cli` secret injection inside the user unit.
- Task 3–5 produce artifacts; verify generated scripts before execution.
- Session path may be `~/.openclaw/agents/main/sessions/` or `~/.clawdbot/agents.main/sessions/` depending on install; check at runtime.
- Heartbeat config keys must match the OpenClaw version's schema; validate before deploy.

---

## companion: openclaw-audit.sh

Run before optimization to establish baseline. Path: `scripts/openclaw-audit.sh` (in this skill).

**Usage:** `/preflight` in chat → run install checks (`scripts/preflight.sh`). `/audit` in chat → analyze only (run audit script and return output). `/optimize` in chat → run audit, then execute approved optimization actions. For purge, only run after user approval: `scripts/purge-stale-sessions.sh`.
