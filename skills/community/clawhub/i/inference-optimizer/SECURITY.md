# Security

Security posture, third-party scan context, and remediation history for `inference-optimizer`. Routine release bullets also appear in [CHANGELOG.md](CHANGELOG.md).

## Reporting a vulnerability

Use [GitHub Security Advisories](https://github.com/vitalyis/inference-optimizer/security/advisories/new) for private reports, or open an issue for non-sensitive questions.

## VirusTotal, ClawHub, and GitHub Security

- **ClawHub** runs **VirusTotal** (and other checks) on published skill packages. The listing for this skill: [inference-optimizer on ClawHub](https://clawhub.ai/vitalyis/inference-optimizer). New publishes can change scan results; re-scan after fixes.
- **v0.2.0** in this repo was shipped as **security remediation following a VirusTotal-oriented review** of the skill contents (see git history: `v0.2.0: Security remediation per VirusTotal audit`).
- **Ongoing remediation:** Dependency alerts, Dependabot, and the dependency/security overview for the repository are tracked on [**GitHub → Security**](https://github.com/vitalyis/inference-optimizer/security). Several follow-up passes have been applied there after publish.

## Current posture

- **Runtime before tuning:** Audit gateway ownership, services, resolved `openclaw` path, workspace wiring for this skill, updater/allowlist coverage, plugin signals, then session/context behavior—before inference or token tuning.
- **Audit is read-only:** `/audit` inspects and reports; it does not purge, rewrite workspace files, deploy, or restart services.
- **Diagnosis:** Warnings are not root cause by themselves; partial or truncated output is inconclusive until version, service state, and logs are verified.
- **Allowlists:** Match resolved paths (`which`, `command -v`, `readlink -f`). Prefer bounded NVM patterns over basename-only `openclaw` entries. For this skill’s scripts, prefer `/usr/bin/bash` plus **one approval line per script path** under `<skill_dir>/scripts/` (see `SKILL.md`). Avoid `/usr/bin/bash *` and `/usr/bin/bash **` in allowlists—they are broader than required and are not recommended here.

```text
/home/ubuntu/.nvm/versions/node/*/bin/openclaw
/home/ubuntu/.nvm/versions/node/*/bin/openclaw *
```

Use a second line only when your gateway requires separate entries for subcommands; keep wildcards as narrow as possible.

- **Purge:** `purge-stale-sessions.sh` archives by default to `~/openclaw-purge-archive/<timestamp>/`; use `--delete` only for intentional immediate removal.
- **Setup:** `setup.sh` is preview-first; `--apply` changes workspace instruction files and agent-facing behavior.
- **Data:** Audit scripts aim for metadata in outputs; do not paste secrets; use `<redacted>` (or equivalent placeholders) in examples.

## v0.3.0 addendum

This release keeps the command surface unchanged, but tightens how the skill should diagnose and recommend fixes in production OpenClaw environments.

### What changed

- The skill now audits runtime health before suggesting inference tuning.
- The audit order now checks:
  1. gateway ownership and duplicate supervisors
  2. restart loops and failed services
  3. resolved `openclaw` binary path and install type
  4. workspace command wiring for the installed skill path
  5. updater status and allowlist coverage for the resolved path
  6. plugin provenance and unused local extensions
  7. only then context pressure, stale sessions, cache-trace, pruning, and concurrency
- Updater/process diagnosis now has stricter rules:
  - warnings are not root cause by themselves
  - partial or truncated output is inconclusive
  - installed version, service state, and logs must be checked before naming a cause
- Allowlist guidance now explicitly prefers resolved executable paths and bounded NVM wildcards over basename-only rules.
- `README.md` was simplified, with more operational detail kept here instead of the landing page.
- `openclaw-audit.sh` now checks runtime health, workspace command wiring, allowlist coverage, plugin provenance signals, and then token/session overhead.
- `openclaw-audit.sh` now emits a `Recommended next steps` section so the audit produces actionable follow-up instead of raw metrics only.
- `setup.sh` now updates a managed workspace block idempotently and removes legacy references such as:
  - `~/clawdbot/code/scripts/openclaw-audit.sh`
  - `~/clawdbot/code/scripts/purge-stale-sessions.sh`
  - `/clawd/skills/public/inference-optimizer/...`
- `verify.sh` now fails when stale install paths or legacy workspace wiring are still present.

### Why this matters

The March 14, 2026 VPS remediation exposed failure modes that pure token optimization guidance missed:

- duplicate gateway supervisors caused the largest live instability
- updater commands failed from chat because the allowlist covered the wrong path
- warning text from an untracked plugin was incorrectly treated as the updater failure cause
- the docs promised runtime-first checks before the shipped scripts actually performed them

This release updates the skill so those conditions are checked before tuning recommendations are made, and it adds install-time verification so dead VPS paths are caught immediately.

## v0.2.1 addendum

**Report:** Pre-scan still flagged "return raw output" and prescriptive phrasing ("return output"). Skill instructs agent to follow a workflow that could coerce behavior. Enforcement of redaction/metadata rules relies on the agent.

**Changes:**

- Replaced "return raw output" and "return output" with passive phrasing: "the script produces metadata that may be relayed"; "include the script's output in your response."
- Added disclaimer in `SKILL.md` that these are workflow instructions, not system-prompt overrides.
- Added a pre-install checklist to the old README structure.
- Manual install showed preview before `--apply`.
- Added script reference guidance for reviewer inspection.

## v0.2.0 remediation summary (VirusTotal-oriented)

### 1. Instruction scope and system-prompt override

Prescriptive prohibitions were replaced with descriptive workflow wording so the skill reads as guidance rather than a system override.

### 2. Sensitive data handling

- Audit outputs metadata only.
- Rewrites must never surface secrets; use `<redacted>` when examples require placeholders.

### 3. Purge and allowlist safety

- Purge archives by default instead of deleting immediately.
- Broad wildcard allowlist guidance was removed in favor of manual execution or path-specific patterns.

### 4. Setup confirmation

- `setup.sh` became preview-first.
- `--apply` became the explicit write path.

## Summary

- Runtime-first audit guidance and stricter updater/process diagnosis.
- Resolved-path allowlist guidance (bounded NVM patterns).
- Archive-first cleanup; preview-first setup changes.
- Metadata-oriented audit output; explicit distinction from system-prompt overrides.
