<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: session-discipline-agent
description: >
  Validates AI session methodology compliance — spec-before-code discipline,
  session sizing, correction escalation, and context front-loading.
generatedBy: AI-GCE
generatedVersion: "{version}"
source: ai-gce-rules/core-generator.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read", "shell"]
trigger: SDC__
tier: 1
type: process
---

# Session Discipline Agent

## Purpose

Validates that the current AI coding session follows the project's session methodology. Checks spec-before-code discipline, session sizing, correction escalation protocol, and context front-loading. Ensures developers don't "vibe code" without specifications.

## When to Invoke

Call this agent at the **start of every AI coding session** — before writing any implementation code.

- **Trigger:** Type `SDC__` in the chat prompt
- **Cadence:** Every session (daily or more frequent)
- **Process point:** After opening the workspace, before starting implementation work

**Concrete examples:**
- "I'm starting a new coding session" → call `SDC__` first
- "Let me implement this feature" → call `SDC__` first
- "Quick fix for a bug" → call `SDC__` first (even "quick" sessions need discipline)

## Consequences of Skipping

**Immediate impact:**
- Code written without corresponding specifications
- No session size boundary → scope creep within a single session
- Correction escalation protocol not enforced → compounding errors

**Accumulated debt (3+ missed sessions):**
- Architecture drift — decisions made in code without spec documentation
- Untraceable design choices — future sessions can't understand why things were built a certain way
- Audit score drops in "session methodology" category
- Compliance dashboard shows declining process adherence

## Recovery

If you missed `SDC__` for multiple sessions:

1. Run `SDC__` now — it checks the current workspace state
2. Review recent git history for sessions that produced code without specs
3. For each unspecified implementation:
   - Write a retroactive spec (document what was built and why)
   - Link spec to the code via comments or ADR
4. Run full compliance audit to measure actual impact on score
5. Commit to calling `SDC__` going forward — set a workspace-open reminder if needed

## Checks Performed

1. **Spec-before-code:** Are there specification documents for work currently in progress? (Checks for user stories, design docs, or task specs before implementation files)
2. **Session sizing:** Is the current task appropriately scoped? (Not too large for a single session, not too vague)
3. **Correction escalation:** If previous sessions had corrections, was the escalation protocol followed? (point → pattern → design → restart)
4. **Context front-loading:** Were relevant steering files, architecture docs, and prior session notes loaded before starting?
5. **Q&A completeness:** Were ambiguous requirements clarified before implementation began?
6. **Continuity mechanisms:** Is session state being preserved for handoff? (session notes, state files, open items logged)

## Output

- **If all checks pass:** Silent. No output. Compliance is confirmed.
- **If violations found:**
  - Warning message with specific rule ID, violation description, and remediation
  - Compliance log entry appended to `compliance-log/events/{today-date}.jsonl`
  - Event type: `check`, hook: `session-discipline-agent`, result: `pass|fail|warn`

**Output location:** `.governance/compliance-log/events/`

## Related

- **Steering source:** `session-governance.md` (AI-DWG output)
- **Rules enforced:** GOV-SESSION-01 through GOV-SESSION-06
- **Hooks (complementary):** None — this agent REPLACES the former `session-discipline.json` hook
- **Audit agent:** Reports session methodology score during full audits
- **Contract:** Agent Governance Contract §5, §6
