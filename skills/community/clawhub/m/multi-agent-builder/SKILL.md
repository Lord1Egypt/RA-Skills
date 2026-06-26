---
name: multi-agent-builder
description: Build a reusable multi-agent team in OpenClaw from a user goal (e.g., "create a product-engineering team", "build a marketing ops team"). Use when the user wants role analysis, role confirmation, agent-by-agent creation plan, collaboration protocol, handoff flow, and channel-binding checklist. Mirror the user's language (English/Chinese/other) throughout the interaction and outputs.
---

# Team Builder

## Overview
Design and bootstrap a multi-agent team with clear roles, dependency-aware workflow, and reliable collaboration rules. Start with role discovery, confirm scope with the user, then produce an implementation-ready team plan.

## Workflow

### 1) Mirror language and capture mission
- Detect and mirror the user's language.
- Follow minimal-question strategy from `references/dialog-flow.md`.
- Ask only missing items: team objective, expected outputs, constraints (timeline, tools, compliance), preferred channels.
- If user intent is broad, propose a default operating model first, then refine.
- Reuse language prompts from `references/language-templates.md`.

### 2) Propose a complete role set (then let user prune)
- Generate a comprehensive but practical role catalog for the mission.
- Always include `team-leader` as mandatory core role.
- Apply auto-completion and anti-overdesign rules from `references/dialog-flow.md`.
- Apply split/merge criteria from `references/splitting-principles.md`.
- Mark roles as:
  - **Core** (required)
  - **Optional** (context-dependent)
  - **Not needed now** (defer)
- During role confirmation, use user language and show role names/functions only (no agent IDs at this stage).
- Ask user to confirm additions/removals before any build steps.
- For role suggestions, use `references/role-catalog.md` as baseline patterns.
- Only in the final creation report show: role name + agent ID + responsibilities.

### 3) Define each agent contract
For each confirmed role, define:
- Agent ID (stable, short, lowercase-hyphen)
- team-leader id must be team-prefixed (e.g., `<team>-team-leader`)
- Role mission
- Inputs consumed
- Outputs produced
- Decision authority
- Upstream/downstream dependencies
- Escalation target

Use the table format in `references/output-templates.md`.

### 4) Define collaboration protocol (must be explicit)
Do not rely on vague "work together" instructions. Specify:
- Task delegation envelope (goal, context, deliverable, deadline)
- Status states (`accepted`, `blocked`, `done`)
- Completion callback requirement (explicit return to delegator)
- Long-task update cadence
- Timeout/retry/escalation policy
- No-raw-bulk-output rule (summary + artifact path only)
- Mid-process visibility: show who is working on what at each stage

Use `references/collaboration-protocol.md`.

### 5) Produce implementation + provisioning bundle
Return a concrete package for execution:
1. Team roster and responsibilities
2. Agent interaction flow (ordered steps)
3. Collaboration protocol summary
4. Files to create/update (SOUL/AGENTS/IDENTITY guidance snippets)
5. Provisioning plan (tools/skills/permissions per role)
6. Team creation report (mandatory; includes stage deliverables+paths and security-check summary)
7. Channel binding blueprints (provided automatically after the report)
8. Smoke-test script (simple end-to-end validation prompt)

Mandatory execution path (programmatic, not prompt-only):
- run single entrypoint: `scripts/create_team.mjs`
- this entrypoint must internally execute materialize -> validate -> emit_report
- if validate != ready, must return partially_ready/blocked and stop

Mandatory: run post-creation materialization checks via `references/materialization-checklist.md`.
Do not mark team as ready if role files are still placeholders.

Use:
- `references/capability-matrix.md`
- `references/permission-profiles.md`
- `references/provisioning-playbook.md`
- `references/final-deliverable-sample.md`
- `references/channel-binding-blueprints.md`
- `references/materialization-checklist.md`

### 6) Safe execution guardrails
Before any external-effect action, apply this confirmation policy:
- No confirmation needed for internal deterministic setup:
  - creating/updating agents in openclaw.json
  - setting A2A/subagents permissions
- Confirmation required for channel/bot credential binding and other irreversible external effects.

For skill installation, run security pre-check first and block high-risk items.
Never auto-restart gateway during creation flow. If restart is required, ask user first or provide manual restart instruction.
If anything is ambiguous, pause and ask.

### 7) Failure handling and recovery
When setup/collaboration fails, apply `references/failure-modes.md`.
Prioritize fast recovery with minimal blast radius:
- preserve completed work
- recover from last checkpoint
- keep user status accurate (ready vs partially ready)
- never auto-install skills that fail security checks

## Quality bar
- Prefer fewer roles with crisp boundaries over many overlapping roles.
- Every role must have a measurable output.
- Every dependency must have a return path.
- Deliverables must be immediately actionable by an operator.
- Role docs must be rich enough to represent domain-expert behavior (not one-line placeholders).
- `team-leader` must orchestrate only and must not produce specialist implementation deliverables.
- All specialist outputs must be saved under team shared directory.
- Reuse patterns from `references/examples.md` when user goals match known team archetypes.

## Creation phase details
After role confirmation, follow `references/create-playbook.md` exactly.
Use `references/snippet-templates.md` to produce reusable SOUL/AGENTS append snippets.
Format final user handoff using `references/final-deliverable-sample.md`.

## Resources
- `references/role-catalog.md`: cross-domain role starter sets.
- `references/role-display-mapping.json`: locale-based role display names for confirmation stage.
- `references/dialog-flow.md`: minimal-question discovery flow and auto-completion rules.
- `references/language-templates.md`: bilingual/locale-aware prompt templates.
- `references/splitting-principles.md`: when to split/merge roles during discovery.
- `references/examples.md`: end-to-end examples for common team archetypes.
- `references/channel-binding-blueprints.md`: Single-Bot vs Multi-Bot Group binding plans and group config guidance.
- `references/capability-matrix.md`: role-to-tools/skills mapping baselines.
- `references/permission-profiles.md`: least-privilege profiles.
- `references/provisioning-playbook.md`: auto install + permission setup flow (with skill-vetter-first security scanning).
- `references/security-report-schema.md`: machine-readable security report and install decision schema.
- `references/collaboration-protocol.md`: explicit multi-agent coordination protocol.
- `references/output-templates.md`: final output templates and checklists.
- `references/create-playbook.md`: execution-ready creation sequence.
- `references/snippet-templates.md`: reusable injection/confirmation snippets.
- `references/role-soul-blueprints.md`: expert-level SOUL depth blueprint per role.
- `references/team-leader-template.md`: fixed team-leader SOUL template (copied at creation).
- `references/team-leader-agents-template.md`: fixed team-leader AGENTS template (copied at creation).
- `references/final-deliverable-sample.md`: standardized user handoff format.
- `references/failure-modes.md`: failure scenarios and recovery actions.
- `references/materialization-checklist.md`: post-creation role-file completion gate.
- `references/config-materialization-checklist.md`: mandatory openclaw.json agent/binding/A2A completion gate.
