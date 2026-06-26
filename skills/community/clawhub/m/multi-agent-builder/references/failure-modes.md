# Failure Modes and Recovery Playbook

Use this playbook when collaboration quality drops or setup execution fails.

## 1) Role overlap / ownership conflict
Symptoms:
- Two agents produce similar outputs
- Repeated rework or contradictory decisions

Action:
- Re-assign one clear owner per artifact
- Merge roles if boundaries remain ambiguous
- Update roster table and dependencies

## 2) Silent assignee (no response)
Symptoms:
- Delegated task not acknowledged in SLA window

Action:
- Retry once with compact context snapshot
- If still silent, escalate to lead
- Re-route task to fallback role if critical path is blocked

## 3) Delegation loops
Symptoms:
- Task bounces between agents without completion

Action:
- Enforce max handoff depth (e.g., 2)
- Require delegator to keep ownership of final artifact
- Stop loop and escalate to lead for manual reassignment

## 4) Channel binding failure
Symptoms:
- Agent cannot receive/send in target channel

Action:
- Verify identity mapping and credentials
- Validate permissions and routing
- Use alternate channel for smoke test
- Keep setup in "partially ready" status until fixed

## 5) Permission denied / scope insufficient
Symptoms:
- Tool invocation fails due to missing scope

Action:
- Identify exact missing permission
- request minimal additional scope only
- resume from last successful checkpoint

## 5.1) Skill security check failed
Symptoms:
- skill flagged with high-risk signals (e.g., suspicious shell execution, external data exfiltration path, unsafe download-and-execute)

Action:
- run `skill-vetter` protocol as primary check
- if scanner unavailable, run fallback scanner or manual checklist and document fallback
- mark skill as `blocked_for_review`
- do not auto-install flagged item
- continue provisioning remaining safe items
- include explicit risk note and replacement suggestion in final report

## 6) Output quality drift
Symptoms:
- Incomplete, off-format, or low-confidence deliverables

Action:
- Re-issue with explicit output template
- tighten acceptance criteria
- add peer-review role for final pass if repeated

## 7) Over-designed team
Symptoms:
- Too many roles, slow execution, high coordination overhead

Action:
- Collapse to core roles (<=5 preferred for first run)
- defer optional roles
- keep one lead for final consolidation

## 8) User-facing status policy
- Report only meaningful milestones:
  - setup started
  - blocker detected
  - setup ready / partially ready
- Never claim full readiness if any critical binding/check failed
