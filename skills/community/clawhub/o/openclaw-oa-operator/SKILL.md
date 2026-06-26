---
name: openclaw-oa-operator
description: Install, configure, operate, and productize OA monitoring and self-heal workflows for OpenClaw workspaces. Use when Codex needs to set up or repair `oa-cli`, inspect or stabilize an `oa-project`, run or interpret `oa collect` and `oa serve`, explain G1-G5 metrics and self-heal signals, refine OA dashboards, or prepare the capability for ClawHub skill or plugin release.
---

# OpenClaw OA Operator

Use this skill to operate OA as an observability and self-heal layer for OpenClaw. Focus on stable workflows, explain what the data means, and keep public packaging separate from machine-specific local setup.

## Quick Start

- Inspect the workspace for `config.yaml`, `self_heal_rules.yaml`, `scripts/`, `patches/`, `pipelines/`, and any dashboard override such as `dashboard-zh/`.
- Determine whether the user wants local operations, dashboard refinement, or publishable packaging. Do not switch UI structure without explicit approval once the user picks a preferred layout.
- Prefer the simplest stable path: use upstream OA behavior unless the workspace already carries justified overrides.
- Run the smallest useful verification after each meaningful change: API check, script smoke check, or dashboard screenshot.
- Use `scripts/oa_workspace_smoke_test.sh` for a minimal end-to-end workspace check when OA is already configured.

## Operate OA Locally

1. Confirm the current OA surface.
   Use existing workspace scripts first if present, especially wrappers such as `scripts/start_oa_server.sh`, `scripts/stop_oa_server.sh`, and `scripts/manage_oa_launchd.sh`.
2. Verify the runtime before editing UI.
   Check that `oa collect` can populate data and that `oa serve` exposes the expected endpoints before diagnosing the dashboard.
3. Treat configuration files as policy.
   Read `config.yaml` for goals, thresholds, OpenClaw path, and agent scope. Read `self_heal_rules.yaml` before changing remediation behavior.
4. Keep verification concrete.
   Validate `/api/health`, `/api/goals`, `/api/team-health`, `/api/traces`, and any self-heal endpoints used by the current dashboard.

## Interpret Metrics And Self-Heal State

- Explain G1 and G2 first because they are usually the most stable built-ins: cron reliability and team health.
- Explain custom goals only after confirming their pipelines and metric sources exist in the workspace.
- Distinguish clearly between:
  - signal quality issues
  - pipeline failures
  - dashboard rendering issues
  - self-heal policy breaches
- For self-heal work, preserve the loop:
  - detect
  - fix
  - verify
  - learn
- Before running command-mode fixers, inspect the concrete command template, placeholders, and target paths. Prefer non-destructive fixers and keep fallback ticketing enabled when available.

## Refine Dashboards Safely

- Preserve the user's chosen layout once they say a version is clearer. Improve copy, density, and data mapping before changing structure.
- Prefer upstream OA layout when the user values clarity and comparability to the original repository.
- Use project-level overrides only when there is a clear need for localization, extra tabs, or richer diagnostics.
- After UI edits, verify both desktop and mobile views with real screenshots instead of assuming the layout works.

## Package For ClawHub

- Prefer a `skill` when the value is workflow knowledge: install OA, operate it, interpret metrics, and guide self-heal decisions.
- Prefer a `plugin` when the value is a long-running service, HTTP routes, background workers, or a productized dashboard experience.
- Remove machine-specific defaults before public packaging:
  - absolute paths
  - local ports and launchd labels
  - local agent rosters
  - user-specific ticket directories
  - local backup and artifact paths
- Package reusable instructions, checklists, and safe defaults. Do not package private workspace snapshots as public examples.
- Read `references/release-readiness.md` before preparing a public release.
- Read `references/smoke-test.md` before claiming the package is publish-ready.

## Deliverables

- For local operations, report what changed, how it was verified, and what remains risky.
- For release preparation, produce:
  - a public versus private diff
  - a publish-readiness checklist
  - proposed listing copy
  - a recommendation of `skill` versus `plugin`
