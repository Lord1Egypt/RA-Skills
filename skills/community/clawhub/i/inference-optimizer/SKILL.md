---
name: inference-optimizer
description: Audit OpenClaw runtime health first, then optimize inference speed and token usage with approval. Use /audit for analyze-only and /optimize for analyze + action flow.
license: MIT
metadata:
  version: "0.3.4"
  openclaw:
    author: vitalyis
    emoji: "⚡"
    os:
      - linux
    requires:
      bins:
        - bash
        - python3
    cliHelp: |
      Install (ClawHub): clawhub install inference-optimizer
      Manual: git clone https://github.com/vitalyis/inference-optimizer.git ~/clawd/skills/inference-optimizer
      Preview: bash ~/clawd/skills/inference-optimizer/scripts/setup.sh
      Apply: bash ~/clawd/skills/inference-optimizer/scripts/setup.sh --apply
      Verify: bash ~/clawd/skills/inference-optimizer/scripts/verify.sh
    config:
      stateDirs:
        - ~/.openclaw
        - ~/clawd/skills/inference-optimizer
        - ~/openclaw-purge-archive
      example: "Required skill-specific env vars: none (no API keys). Reads local OpenClaw state under ~/.openclaw; skill files live under ~/clawd/skills/inference-optimizer when installed as documented. Preflight may archive ~/.openclaw and workspace trees—treat backups as potentially sensitive."
    links:
      repository: https://github.com/vitalyis/inference-optimizer
      homepage: https://github.com/vitalyis/inference-optimizer
---

![Inference Optimizer](https://raw.githubusercontent.com/vitalyis/inference-optimizer/main/social-preview.png)

# Inference Optimizer

Audit OpenClaw runtime health first. Optimize inference speed and token usage second.

## Commands

| Command | Behavior |
|--------------|----------|
| `/preflight` | Install checks, backup, audit, and setup preview |
| `/audit` | Analyze-only; check runtime health before suggesting tuning |
| `/optimize` | Audit + propose remediation or optimization actions with per-step approval |
| `purge sessions` | After audit, if user approves, archive stale sessions; use `--delete` for immediate removal |

> These instructions guide agent behavior. Platform and system prompts take precedence; they cannot be enforced programmatically.

## Installation

**ClawHub:**
```bash
clawhub install inference-optimizer
```

**Manual:**
```bash
git clone https://github.com/vitalyis/inference-optimizer.git ~/clawd/skills/inference-optimizer
bash ~/clawd/skills/inference-optimizer/scripts/setup.sh        # preview
bash ~/clawd/skills/inference-optimizer/scripts/setup.sh --apply  # apply after review
```

**Verify:** `<skill_dir>/scripts/verify.sh`

## Workflow

### Audit and remediation branch

1. **`/preflight`**: Exec `<skill_dir>/scripts/preflight.sh`. Append `--apply-setup` only if the user asks to apply setup.
2. **`/audit`**: Exec `<skill_dir>/scripts/openclaw-audit.sh`. Use the script output plus direct environment checks to inspect this order:
   - gateway ownership and duplicate supervisors
   - restart loops or failed services
   - resolved `openclaw` binary path and install type
   - workspace command wiring for the installed skill path
   - updater status and allowlist coverage for the resolved path
   - plugin provenance and unused local extensions
   - only then context pressure, stale sessions, cache-trace, pruning, and concurrency
3. **Diagnosis rule**: Do not conclude from warnings alone. If process output is partial or truncated, report the result as inconclusive and verify installed version, service state, and logs before naming a cause.
4. **No helper-shell prelude**: For `/audit` and `/optimize`, do not run shell helper commands like `ls`, `rg`, `find`, `openclaw status`, or `openclaw gateway status` before the main audit script. If you need context first, use `read` on `MEMORY.md` or `memory_search`. The first shell exec in the optimize flow should be the audit script itself.
5. **Approval semantics**: If exec returns `allowlist miss` or `exec denied`, that is a hard deny, not a pending approval. Do not tell the user to send `/approve ...` unless the tool output explicitly contains a real approval request with an ID. If there is no ID, say there is no approval request to approve and the fix must be on the bot side.
6. **VPS gateway ownership**: On this VPS, `openclaw-gateway.service` is the authoritative gateway owner. Keep `clawdbot.service` disabled, and preserve `pass-cli run --env-file /etc/clawdbot.env.pass` inside the user service itself.

### Optimization branch

1. **`/optimize`**: Run the audit flow first, include the script output in the response, then propose next actions with approval before each file-changing step.
2. **Purge**: Only on explicit approval, run `<skill_dir>/scripts/purge-stale-sessions.sh`. It archives to `~/openclaw-purge-archive/<timestamp>/` by default. Use `--delete` for immediate removal without archive.
3. **Full optimization (Tasks 1-5)**: Read `optimization-agent.md` and follow its flow. Ask approval before every file-changing step.

## Path Resolution

Scripts live at `~/clawd/skills/inference-optimizer/scripts/` or wherever the skill is installed. Always resolve `<skill_dir>` to the actual install path before exec.

## Security and Allowlist

Prefer **path-specific** `exec-approvals.json` entries for the script paths themselves: one line per script under your real `<skill_dir>` (resolve with `readlink -f` if the path is a symlink). Example shape after substituting the install path:

```text
/home/ubuntu/clawd/skills/inference-optimizer/scripts/preflight.sh
/home/ubuntu/clawd/skills/inference-optimizer/scripts/openclaw-audit.sh
/home/ubuntu/clawd/skills/inference-optimizer/scripts/setup.sh
/home/ubuntu/clawd/skills/inference-optimizer/scripts/purge-stale-sessions.sh
/home/ubuntu/clawd/skills/inference-optimizer/scripts/verify.sh
```

`setup.sh` invokes `python3` for idempotent workspace block edits; allow that binary only if your platform uses it (for example `/usr/bin/python3`).

Before editing any allowlist:

- Resolve the real executable path with `which`, `command -v`, or `readlink -f`.
- Prefer exact paths or bounded wildcards for versioned NVM installs, for example `/home/ubuntu/.nvm/versions/node/*/bin/openclaw *`.
- Do not assume basename-only rules such as `openclaw` are sufficient.
- Do not add `/usr/bin/bash *` or `/usr/bin/bash **`; they grant far more shell than this skill needs.
- If you keep optional read-only helper commands available, allowlist only narrow read-only patterns actually used by this skill, for example the exact memory listing command under `workspace-whatsapp` and exact `openclaw status` variants. Do not rely on generic `ls *` or `rg *` coverage.

For purge via agent exec, add path-specific patterns only. Optional wider patterns and trade-offs are discussed in `SECURITY.md`. See also `README.md` and `SECURITY.md` for operational detail.
