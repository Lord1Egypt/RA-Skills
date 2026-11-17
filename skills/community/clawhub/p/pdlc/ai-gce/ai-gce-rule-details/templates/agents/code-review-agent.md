<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: code-review-agent
description: >
  Validates code review compliance — reviewer-author separation, trust spectrum adherence,
  per-layer review focus, and review evidence completeness before PR approval.
generatedBy: AI-GCE
generatedVersion: "{version}"
source: ai-gce-rules/core-generator.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read", "shell"]
trigger: CRV__
tier: 2
type: audit
---

# Code Review Agent

## Purpose

Validates code review governance compliance before a pull request is approved. Checks reviewer-author separation (role isolation), trust spectrum adherence per code type, per-layer review focus areas, and that review evidence is complete and traceable. Prevents self-approved PRs and ensures the right expertise reviews the right code.

## When to Invoke

Call this agent **before approving any pull request** — after the review is done but before the merge.

- **Trigger:** Type `CRV__` in the chat prompt
- **Cadence:** Every PR review cycle
- **Process point:** After reviewing code, before clicking "Approve" or "Merge"

**Concrete examples:**
- "I've reviewed this PR, ready to approve" → call `CRV__` first
- "PR #42 needs a second look" → call `CRV__` to check if the right reviewer is assigned
- "Self-merging this small fix" → call `CRV__` — it will flag if self-approval violates trust spectrum

## Consequences of Skipping

**Immediate impact:**
- Self-approved PRs may violate segregation of duties
- Wrong expertise reviewing critical code (e.g., junior developer approving security changes)
- Review evidence missing from audit trail
- Trust spectrum violations go undetected

**Accumulated debt (5+ missed reviews):**
- Role isolation compliance drops — audit flags systematic self-approval
- Security-critical code changes lack appropriate sign-off
- Compliance score drops in "PR governance" category
- External audit findings: "insufficient separation of duties"
- Cannot prove review rigor for SOX/regulatory compliance

## Recovery

If you missed `CRV__` for multiple PRs:

1. Run `CRV__` now for the current PR — it's never too late for active PRs
2. For already-merged PRs: **cannot undo the merge**
3. Recovery steps:
   - Run full compliance audit → identifies PRs that violated review rules
   - Log each violation as an exception in `compliance-log/events/`
   - For security-critical violations: consider a post-merge review + ADR documenting the gap
   - Update CODEOWNERS if assignment patterns were wrong
4. Implement branch protection rules to enforce reviewer requirements at platform level (defense-in-depth)

## Checks Performed

1. **Reviewer ≠ Author:** The person approving is NOT the person who wrote the code (segregation of duties — GOV-ROLE-01)
2. **Trust spectrum compliance:** Does the code type match the required review trust level?
   - High trust (logging, docs) → any team member can approve
   - Medium trust (business logic) → domain expert required
   - Low trust (API contracts, integrations) → tech lead or architect required
   - Zero trust (financial calculations, security, auth) → designated reviewer MUST approve
3. **Per-layer review focus:** Is the reviewer checking the right things for the layer?
   - Presentation layer → UX patterns, input validation, error messages
   - Application layer → business rules, error handling, transaction boundaries
   - Domain layer → model integrity, invariants, ubiquitous language
   - Infrastructure layer → connection handling, retry logic, security
4. **Review evidence:** Is there a review comment or approval record? (not just a silent approve)
5. **PR template compliance:** Does the PR follow the project's PR template? (description, testing, linked stories)
6. **CODEOWNERS alignment:** Is the reviewer listed as an owner for the affected files/modules?

## Output

- **If all checks pass:** Silent. No output.
- **If violations found:**
  - Warning with rule ID, specific violation (e.g., "Self-approval detected on security-critical file"), remediation
  - Compliance log entry appended to `compliance-log/events/{today-date}.jsonl`
  - Event type: `check`, hook: `code-review-agent`, result: `pass|fail|warn`
  - For zero-trust violations: result is `fail` (blocking recommendation)

**Output location:** `.governance/compliance-log/events/`

## Related

- **Steering source:** `git-workflow.md`, `role-isolation.md`, `TEAM_AGREEMENTS.md`, `CODEOWNERS` (AI-DWG output)
- **Rules enforced:** GOV-PR-01 through GOV-PR-06, GOV-ROLE-01
- **Hooks (complementary):** `pre-pr-checklist.json` (fires automatically pre-PR — checks template compliance)
- **Contract:** Agent Governance Contract §5, §6
