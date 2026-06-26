---
name: linux-riscv-contribute
description: Orchestrate an OpenClaw multi-agent pipeline to close Linux RISC-V gaps versus ARM/x86 (Linux tree + KVM lore), create and manage GitHub issues, generate design plans with Claude Code, implement/verify with Codex, and prepare upstream patch emails. Use when users ask to automate or run RISC-V kernel contribution workflows, gap analysis, issue-driven execution, or patch submission preparation.
---

# Linux RISC-V Contribute

## Overview

Use this skill to run a repeatable `discover -> issue -> plan -> implement -> patch` pipeline with OpenClaw as orchestrator and ACP agents (`claude-code`, `codex`) as workers.

Keep humans at exactly three gates:
1. Confirm gap triage and priorities.
2. Approve implementation plan.
3. Approve final patch email before sending.

## Workflow

### Step 0: Bootstrap workspace

Run `scripts/bootstrap_openclaw_workflow.sh <docs_repo_root> <linux_repo_path>` to create/update:
- `kernel/openclaw/config/workflow.yaml`
- `kernel/openclaw/state/{gap_registry.yaml,issue_map.yaml,run_history/}`
- `kernel/openclaw/{plans,patches,logs}`

If files already exist, do not overwrite without explicit user approval.

### Step 1: Discover RISC-V gaps

Collect evidence from:
- Linux source tree (`arch/riscv`, `arch/arm64`, `arch/x86`, `virt/kvm`)
- KVM lore (`https://yhbt.net/lore/kvm/`)

Write structured entries to `state/gap_registry.yaml` with:
- `gap_id`, `type` (`feature|performance|maintainability`), `summary`
- `evidence` (paths, commits, lore URLs)
- `severity` (`P0|P1|P2`), `confidence` (`high|medium|low`)
- `acceptance_hint`

Pause for **Gate-1** human triage before creating issues.

### Step 2: Sync GitHub issues

For each approved gap:
- Create/update issue in configured repo.
- Add labels from severity/type.
- Save `gap_id -> issue_number` mapping to `state/issue_map.yaml`.

Use one issue per gap; avoid duplicate issues by matching `gap_id`.

### Step 3: Plan with Claude Code (ACP)

Spawn ACP session explicitly:
- `runtime: "acp"`
- `agentId: "claude-code"`

Ask for:
- file-level design
- test matrix (`kselftest`, `kvm-unit-tests`, perf)
- rollback/risk notes
- upstreaming strategy

Save outputs under `kernel/openclaw/plans/issue-<id>-plan.md`.
Pause for **Gate-2** human plan approval.

### Step 4: Implement and verify with Codex (ACP)

Spawn ACP session explicitly:
- `runtime: "acp"`
- `agentId: "codex"`

Run iterative loop until pass or policy limit:
1. Implement approved plan.
2. Build and run configured tests.
3. Parse failures and patch.

Record each iteration in `state/run_history/*.json`.
If max iterations reached, return to Step 3 with failure summary.

### Step 5: Generate patch and email package

Produce:
- `git format-patch` series
- `checkpatch` result
- suggested `To/Cc` (`get_maintainer.pl`, lore context)
- cover letter draft

Save artifacts in `kernel/openclaw/patches/`.
Pause for **Gate-3** human send approval.

Only send to mailing lists after explicit approval.

## OpenClaw execution rules

- Prefer ACP `sessions_spawn` for agent work; set `agentId` explicitly.
- Limit parallel issues to 2-3 unless user changes policy.
- Never auto-send external email without user confirmation.
- Preserve auditability: every stage must have file artifacts.

## Quick command prompts for operator

Use these ready prompts in OpenClaw chat:

1. `按 workflow.yaml 执行 Step-1，更新 gap_registry.yaml，并生成 Gate-1 审核表。`
2. `基于已批准 gap 执行 Step-2，同步 issue 并输出映射表。`
3. `对 issue #<n> 用 claude-code 执行 Step-3，生成详细方案和测试矩阵。`
4. `对 issue #<n> 用 codex 执行 Step-4，直到验证通过或达到迭代上限。`
5. `对 issue #<n> 执行 Step-5，先 dry-run 生成 patch 和发信草案，等待我确认。`

## References

- Workflow template: `references/workflow-template.yaml`
- Issue template: `references/issue-template.md`
- Human gate checklist: `references/gate-checklist.md`
