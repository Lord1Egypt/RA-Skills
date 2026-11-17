<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: sprint-governance-agent
description: >
  Validates sprint governance at boundaries — sprint plan completeness,
  goal definition, capacity allocation, retro action follow-through, and velocity tracking.
generatedBy: AI-GCE
generatedVersion: "{version}"
source: ai-gce-rules/core-generator.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read", "shell"]
trigger: SGV__
tier: 2
type: process
---

# Sprint Governance Agent

## Purpose

Validates sprint governance compliance at sprint boundaries. Checks sprint plan completeness, goal definition, capacity allocation, retrospective action follow-through, and velocity measurement. Ensures the team's sprint cadence produces traceable, governed delivery.

## When to Invoke

Call this agent at **sprint start and sprint end** — the two boundary ceremonies.

- **Trigger:** Type `SGV__` in the chat prompt
- **Cadence:** Every sprint boundary (typically every 1-2 weeks)
- **Process points:**
  - Sprint planning (start) — validates plan quality
  - Sprint review/retro (end) — validates completeness and follow-through

**Concrete examples:**
- "We're starting Sprint 4" → call `SGV__` to validate sprint plan
- "Sprint 3 is done, doing retro" → call `SGV__` to check completion and retro actions
- "Mid-sprint check" → call `SGV__` for a progress health check (optional but encouraged)

## Consequences of Skipping

**Immediate impact:**
- Sprint goals undefined or unmeasured
- Capacity not allocated → overcommitment or underutilization
- Retro actions from previous sprint not followed through
- No velocity data for forecasting

**Accumulated debt (3+ missed sprints):**
- Sprint velocity is unmeasurable — forecasting becomes guesswork
- Retro actions pile up unresolved → same problems recur
- Governance registers (Action, Issue) become stale
- Audit score drops in "sprint governance" category
- Stakeholder visibility into progress erodes

## Recovery

If you missed `SGV__` for multiple sprints:

1. Run `SGV__` now — it checks current sprint state
2. Reconstruct sprint history from git log (commits per sprint, stories completed)
3. For each missed sprint:
   - Document sprint goals retroactively (even if "unknown at the time")
   - Log retro actions that were identified verbally but not tracked
4. Update velocity metrics based on reconstructed data
5. Run full compliance audit to measure governance health
6. Commit to sprint-boundary invocations going forward

## Checks Performed

1. **Sprint plan exists:** Is there a documented sprint plan for the current sprint? (backlog items selected, acceptance criteria defined)
2. **Sprint goal defined:** Is there a single, clear sprint goal statement? (not just a list of tasks)
3. **Capacity allocated:** Are team members assigned with realistic capacity? (accounts for leave, meetings, maintenance)
4. **Previous retro actions:** Were retro actions from the PREVIOUS sprint followed through? (check action register)
5. **Velocity tracked:** Is velocity being measured? (story points completed vs. planned)
6. **Impediments logged:** Are blockers documented in the Issue register?
7. **Sprint boundary artifacts:** Do sprint start/end ceremonies have documented outcomes?

## Output

- **If all checks pass:** Brief summary — "Sprint N governance: ✅ all checks pass. Velocity: X pts."
- **If violations found:**
  - Warning per violation with rule ID and remediation suggestion
  - Compliance log entry appended to `compliance-log/events/{today-date}.jsonl`
  - Event type: `check`, hook: `sprint-governance-agent`, result: `pass|fail|warn`

**Output location:** `.governance/compliance-log/events/`

## Related

- **Steering source:** `project-governance.md`, `TEAM_AGREEMENTS.md` (AI-DWG output)
- **Rules enforced:** GOV-SPRINT-01 through GOV-SPRINT-07
- **Hooks (complementary):** None — this agent REPLACES the former `sprint-governance.json` hook
- **Registers affected:** Action Register (retro actions), Issue Register (impediments)
- **Contract:** Agent Governance Contract §5, §6
