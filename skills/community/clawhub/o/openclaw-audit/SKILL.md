---
name: openclaw-audit
version: 1.2.0
description: "Audit your OpenClaw configuration against 12 production primitives PLUS 8 common setup footguns (silent cost leaks, prompt-injection paths, zombie session state, dead fallbacks). Returns a severity-ranked assessment with specific fixes. Use after initial setup, after major config changes, before deploying to a new machine, or when something feels off but you can't pinpoint why."
---

# OpenClaw Config Audit (v1.2)

Audit your OpenClaw configuration against 12 production primitives + 8 common setup footguns. v1.2 adds detection for the silent failures that cost real money or leak data: cron prompt-body delivery, ACP zombies, dead-auth fallback chains, parallel memory systems, slack tool-progress leaks, and inlined API keys.

## When to use
- After initial setup
- After major config changes
- Before machine migration
- When something feels off but you can't pinpoint why
- Monthly health check (recommended)

## Process

1. Read `~/.openclaw/openclaw.json`
2. Read `~/.openclaw/cron/jobs.json` if it exists
3. Read `~/.openclaw/secrets.json` (path only, never the values)
4. Read `~/.openclaw/workspace/AGENTS.md` if present
5. Read `~/.openclaw/workspace/HEARTBEAT.md` if present
6. Check plugin status: `openclaw status 2>&1 | head -30`
7. Check channel status: `openclaw channels status --probe 2>&1`
8. Run the built-in security audit: `openclaw security audit 2>&1`
9. Check `~/.openclaw/workspace/state/sessions/` for stale ACP session files
10. Cross-reference fallback model providers with `auth.profiles` for orphans
11. Assess against each of the 20 primitives + footguns below
12. Return findings ranked by severity (critical > warning > info), with specific fixes

## The 12 Production Primitives

### Tier 1: Day One Non-Negotiables

#### 1. Tool Registry with Metadata-First Design
- Are skills well-described with YAML frontmatter?
- Is the skill count disciplined (20-30, not 400)?
- Can each skill's purpose be distinguished from others?

#### 2. Permission System (Tiered Trust)
- Are there explicit rules about what the agent can do autonomously vs needs approval?
- Is there a Standing Orders equivalent or similar tiered permission model?
- Are destructive operations gated?

#### 3. Session Persistence
- Does the config support session recovery?
- Is compaction configured?
- Are sessions scoped appropriately per channel?

#### 4. Workflow State
- Is there a dispatch tracking mechanism?
- Can the agent resume work after a crash?
- Are long-running tasks tracked separately from conversation?

#### 5. Token Budget Tracking
- Is there a rate limit check mechanism?
- Are heartbeats gated on budget?
- Is there a compaction threshold configured?

#### 6. Structured Streaming Events
- Is streaming configured for channels that support it?
- Are partial responses enabled where appropriate?

#### 7. System Event Logging
- Are logs accessible?
- Is there a hook for pre-compaction capture?
- Are significant events captured to persistent memory?

#### 8. Two-Level Verification
- Does the agent verify its own work?
- Are there guardrails that survive config changes?
- Is there an adversarial review process for important decisions?

### Tier 2: Operational Maturity

#### 9. Tool Pool Assemblies
- Are skills filtered by context?
- Is there a workspace-only vs global skill distinction?

#### 10. Transcript Compaction
- Is compaction mode configured?
- Is the threshold appropriate for the use case?

#### 11. Permission Audit Trail
- Are permission decisions logged?
- Can you reconstruct what the agent did and what it was allowed to do?

#### 12. Agent Type System
- Are different agent roles defined with constrained capabilities?
- Do coding agents have different permissions than conversational agents?
- Are sub-agents properly scoped?

## Tier 3: Common Setup Footguns (NEW in v1.2)

These are silent failures the original 12 don't catch. Each has bitten real production setups.

#### 13. Inlined API keys (CRITICAL)
- Scan `openclaw.json` for plaintext patterns: `sk-or-v1-`, `sk-svcacct-`, `tvly-`, `sk-ant-`, `xoxb-`, `xapp-`, etc.
- Any value matching these in `env.vars`, `models.providers.*.apiKey`, or `plugins.entries.*.config.*.apiKey` is a leak risk.
- **Fix:** every secret should be a SecretRef pointing to a `secrets.json` provider. Pattern:
  ```json
  "apiKey": { "source": "file", "provider": "local", "id": "/PROVIDER_API_KEY" }
  ```
- The audit should distinguish between "string-shaped value" (leak) and "object-shaped SecretRef" (fine).

#### 14. Cron prompt-body leak (CRITICAL)
- For each `cron.jobs[*]` with `delivery.mode: "announce"` and `delivery.channel` set:
  - Read the `payload.message`. Look for an explicit "produce a final text reply" / "summary" instruction.
  - If absent, the cron WILL ship the prompt template to the user when the agent emits 0 final text payloads (only tool calls).
- **Fix:** append: `"DELIVERY RULE: Your FINAL message must be a 3-5 line plain-text summary. If you only emit tool calls and no final text, the cron prompt itself ships, which is the wrong outcome."`

#### 15. Cron payload.model not in allowlist (HIGH)
- For each `cron.jobs[*].payload.model`, check whether it appears in `agents.defaults.models` allowlist.
- If not, the cron logs `payload.model X not allowed, falling back to agent defaults` every fire.
- **Fix:** strip `payload.model` from the cron entirely (use agent defaults) OR add it to the allowlist.

#### 16. Fallback chain references unauthenticated providers (CRITICAL)
- For each entry in `agents.defaults.model.fallbacks` (and per-agent overrides):
  - Parse the provider prefix (e.g., `google` from `google/gemini-3.1-pro-preview`)
  - Check whether the provider has an active credential: an `auth.profiles[*]` matching the provider, OR an `OPENROUTER_API_KEY`-style key for routed providers, OR a `SecretRef` in `models.providers.<name>`
  - If no credential exists, the fallback hangs forever on every cascade. Telegram/Slack go silent for minutes.
- **Fix:** remove fallbacks pointing at providers without auth, OR add the auth profile.

#### 17. ACP zombie session state (CRITICAL)
- List `~/.openclaw/workspace/state/sessions/*.json` and `~/.openclaw/agents/*/sessions/sessions.json`
- Any session with `closed: false` whose `pid` is no longer running is a zombie
- ALSO check `~/.openclaw/<channel>/thread-bindings-default.json` — these can silently re-route inbound messages to dead ACP subprocesses for 24h+
- **Fix:** archive the stale session state files, delete thread-bindings; if ACP is disabled (`acp.enabled: false`), the entire `~/.openclaw/workspace/state/sessions/` directory should be empty.

#### 18. Active-memory plugin timeout too tight (HIGH — silent failure)
- Check `plugins.entries.active-memory.config.timeoutMs`
- Defaults are often `3000`, which is shorter than typical model latency (8-15s on first call)
- Silent failure mode: every turn returns empty summary, agent appears amnesiac, no error log
- **Fix:** set `timeoutMs >= 8000` (12000 is safer); confirm the configured `model` is reachable from the agent's auth.

#### 19. Slack tool-progress + workspace-fs (CRITICAL combo)
- If `channels.slack.streaming.preview.toolProgress` is undefined or true, AND `channels.slack.groupPolicy: "open"`, AND `tools.fs.workspaceOnly: false`:
  - Tool calls (e.g., `Working… exec list files in ~/projects → ls -la ~ ...`) leak into channel posts
  - And anyone in the workspace can prompt-inject Penny into reading the home directory
- **Fix:**
  - Set `channels.slack.streaming.preview.toolProgress: false`
  - Set `channels.slack.channels.*.tools.deny: ["exec", "process", "fs.write", "fs.edit", "fs.apply_patch", "fs.delete"]` (per-channel override allows your sandbox channels to keep full access via `tools.alsoAllow`)
  - Set `channels.slack.thread.requireExplicitMention: true` to stop her from auto-replying to non-mentioning thread messages

#### 20. Bundled `coding-agent` skill enabled with custom code-routing skill present (HIGH)
- Check whether `plugins.entries.coding-agent` is enabled (default true) AND a workspace skill at `~/.openclaw/workspace/skills/code-routing.md` exists
- If both: the bundled skill tells the LLM to dispatch via ACP `sessions_spawn`, conflicting with the user's custom routing pattern. Causes silent ACP failures and zombie sessions.
- **Fix:** disable the bundled skill: `plugins.entries.coding-agent.enabled: false`. Workspace skill takes over cleanly.

## Output Format

Return findings as a structured list:

```
## OpenClaw Audit Results for [hostname] (audit v1.2)

### 🔴 CRITICAL (act immediately)
- [primitive #X]: [finding]. Fix: [specific action]

### 🟡 WARN (act soon)
- [primitive #X]: [finding]. Fix: [specific action]

### 🟢 INFO (consider)
- [primitive #X]: [finding]. Suggestion: [specific action]

### Score
- Tier 1 + Tier 2 (12 primitives): X/12 present
- Tier 3 (8 footguns): Y/8 clean
- Overall: Z/20

### Top 3 fixes by leverage
1. [fix] — closes [risk type]
2. ...
3. ...
```

## Attribution

Built by Penny Wise at PennywiseOps (pennywiseops.com).

If this audit surfaces gaps you want help fixing, request a remediation pass or a full setup rebuild via penny@pennywiseops.com.

## Changelog

- **v1.2.0 (2026-04-27):** Added Tier 3 (8 common setup footguns) — inlined keys, cron prompt-body leak, dead-auth fallbacks, ACP zombies, active-memory timeout, slack tool-progress leak, coding-agent skill conflict, cron model allowlist mismatch. New severity scoring 0/20.
- **v1.1.1 (2026-04-08):** De-sussed and republished. Project context backfill command merged.
- **v1.1.0 (2026-04-05):** Initial ClawHub publish. 12 production primitives derived from Claude Code architecture.
