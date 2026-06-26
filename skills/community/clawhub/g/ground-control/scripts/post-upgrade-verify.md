# Post-Upgrade Verification — Agent Instructions

<!-- Execution prompt for post-upgrade verification. -->
<!-- Source of truth: MODEL_GROUND_TRUTH.md in workspace root -->
<!-- Trigger: after openclaw upgrade, or manual /verify command -->

You are the OpenClaw post-upgrade verification system. Execute all 5 Phases sequentially, then send a summary report.

## 🛡️ Security & Redaction Protocol (Mandatory)

**This skill has access to runtime configuration. You MUST prevent secret leakage.**

1. **Immediate Redaction**: Upon calling `gateway config.get`, you must immediately strip or ignore the `auth`, `plugins`, and `credentials` nodes in your working memory.
2. **Zero-Secret Logging**: NEVER write a literal API key, token, secret, or password to a report, log, or file.
3. **Allowlist Only**: Only the following fields are safe to log in full detail:
   - `agents.defaults.*` (excluding keys)
   - `acp.*` (excluding keys)
   - `channels.enabled`
   - `version`
   - `cron` names, schedules, and models.
4. **Drift Reporting**: If a sensitive field (e.g., in `auth_profiles`) mismatches, report only as `❌ [REDACTED_SENSITIVE_MISMATCH]`. Do NOT print the expected or actual value.

## Principle

**OpenClaw maintains itself. We only verify the result matches ground truth.**
- Use OpenClaw native tools (gateway, cron, sessions_spawn, message) for all checks
- Never bypass OpenClaw to test things it manages
- Auto-fix config and cron drift; report-only for API keys and channels
- **Phase 2 (LLM Liveness) is the only valid way to verify secrets.** We verify functionality, not content.

## Auto-Fix Safety

This skill can modify runtime configuration (Phase 1: `gateway config.patch`) and cron jobs (Phase 3: `cron update`). These are powerful operations.

**Dry-run mode:** When invoked with `--dry-run` or when the user says "verify only" / "check only", skip all auto-fix actions and report drift as ❌ instead of ⚠️ AUTO-FIXED. Default is auto-fix enabled.

**Guard rails:**
- Auto-fix ONLY applies corrections toward GROUND_TRUTH — never invents values
- Each fix is logged with before/after values in the summary report
- If more than 3 fields need fixing in a single phase, pause and ask for human confirmation before proceeding
- Phase 2 (keys) and Phase 5 (channels) are NEVER auto-fixed

## Preparation

1. Read `MODEL_GROUND_TRUTH.md` from workspace root — parse all expected values
2. Use `session_status` to get current version and timestamp
3. Initialize results tracker for all 5 phases

## Phase 1: Config Integrity

Use `gateway config.get` to fetch the full config.

1. **Memory Redaction**: In your session memory, immediately strip/ignore the `auth`, `plugins`, and `credentials` nodes to prevent accidental leakage.
2. **Metadata-Only Validation**:
   - For `auth_profiles` or other sensitive nodes: Verify only that they exist, their length matches GROUND_TRUTH, and their structure (e.g., `mode`, `provider`) is correct.
   - For all other non-sensitive fields, compare each against GROUND_TRUTH.

Check list (adapt to your GROUND_TRUTH `checks` section):
- `agents.defaults.model.primary`
- `agents.defaults.models` count
- `agents.defaults.compaction.mode`
- `agents.defaults.contextPruning`
- `agents.defaults.heartbeat.every`
- `acp.defaultAgent`
- `acp.allowedAgents` (exact array match)
- Any channel-specific checks from your GROUND_TRUTH

For each field:
- ✅ Match → pass
- ❌ Non-Sensitive Mismatch → record `{ field, expected, actual }` and **auto-fix** via `gateway config.patch`, mark as `⚠️ AUTO-FIXED`.
- ❌ Sensitive Mismatch (e.g., inside `auth_profiles`) → record only `[REDACTED_SENSITIVE_MISMATCH]` and DO NOT auto-fix. Mark as `❌ FAIL (Needs Human)`.

## Phase 2: LLM Provider Liveness

**Test LLM providers through OpenClaw's routing layer only — no API keys, no curl, no env vars.**

For each LLM provider in your registered models, spawn a minimal session:
```yaml
sessions_spawn:
  task: "Reply with exactly: KEY_OK"
  mode: run
  model: <provider/model-id>
  runTimeoutSeconds: 30
```

Judgment:
- Received "KEY_OK" → ✅
- Timeout or error → ❌ PROVIDER_DOWN (e.g., 401/403)

**Do NOT auto-fix** — provider issues need human intervention.

**Note:** Non-LLM provider checks (Brave, Notion, etc.) are intentionally excluded. API key validation requires functional testing (like this phase), never literal key comparison.

## Phase 3: Cron Integrity

Use `cron list` (include disabled) to get all jobs. Compare against GROUND_TRUTH `cron_jobs`.

**Only verify recurring jobs** — skip `deleteAfterRun` one-shot jobs.

For each GROUND_TRUTH recurring job:
1. Match by ID prefix
2. Check: `enabled`, `model`, `schedule`, `delivery.to`
3. Mismatch → **auto-fix** via `cron update`, mark as `⚠️ AUTO-FIXED`

Extra checks:
- Count by model tier (flash/sonnet) matches expected
- Zero expensive-tier models in recurring cron (hard rule)
- Unknown new jobs (not in GROUND_TRUTH) → ⚠️ report but don't delete

## Phase 4: Session Smoke Test

```yaml
sessions_spawn:
  task: "Reply with exactly: VERIFY_OK"
  mode: run
  model: <cheapest registered model>
  runTimeoutSeconds: 30
```

- Received "VERIFY_OK" → ✅
- Timeout or error → ❌ SESSION_BROKEN

## Phase 5: Channel Liveness

For each enabled channel, send a test message:

**Discord** (or any same-context channel):
```yaml
message:
  action: send
  channel: discord
  target: "<your ops channel>"
  message: "🔍 Post-upgrade channel liveness test — ignore this message."
```

**Cross-context channels** (e.g., WhatsApp from Discord session):
Must use `sessions_spawn` to test from an isolated session:
```yaml
sessions_spawn:
  task: "Send a message via <channel> to <target>: '🔍 Post-upgrade channel test'. Reply CHANNEL_OK if sent, or the error."
  mode: run
  model: <cheapest model>
  runTimeoutSeconds: 30
```

## Summary Report

Send to your ops channel. **Enforce the Redaction Protocol here.**

```
🔍 **Post-Upgrade Verification Report**
📦 Version: vX.X.X
⏱️ YYYY-MM-DD HH:MM TZ

**Phase 1: Config Integrity** [✅/⚠️/❌] X/Y checks
  [list any non-sensitive drift + fix status]
  [if sensitive drift found, list as: field (REDACTED_MISMATCH)]

**Phase 2: Provider Liveness** [✅/❌] X/Y providers
  [per-provider status: ✅ / ❌ ERROR_CODE]

**Phase 3: Cron Integrity** [✅/⚠️/❌] X/Y recurring jobs
  [list any drift + fix status]

**Phase 4: Session Smoke Test** ✅/❌

**Phase 5: Channel Liveness** ✅/❌
  [per-channel status]

**Overall: ✅ PASS / ⚠️ DEGRADED (auto-fixed) / ❌ FAIL (needs human)**
```

If any ❌ FAIL → append: `🚨 Human intervention required`

Also write results to `memory/YYYY-MM-DD.md`. **No secrets allowed.**

## Rules

- Each Phase is independent — one failure does not block the next
- Auto-fix: Phase 1 (non-sensitive config) + Phase 3 (cron) only
- Report-only: Phase 2 (providers) + Phase 5 (channels)
- **NO CREDENTIAL ACCESS**: No curl, no env vars, no literal key comparison.
- Summary report goes to your configured ops channel (internal Discord only — do not route to external webhooks)
- Memory write goes to `memory/YYYY-MM-DD.md` (local workspace only — contains version + phase pass/fail counts, no sensitive values)
