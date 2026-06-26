---
plan_id: custodian-repair
name: Custodian Escalated Issue Repair
version: 1.0.0
description: Multi-step investigation and repair for Tier 3 escalated issues that Custodian could not auto-fix.
parameters:
  issue_id:
    type: string
    required: true
    description: The issue_id from Custodian's issues.jsonl to investigate and repair.
steps:
  - id: read-issue
    name: Read Escalated Issue
    skill: ocas-custodian
    command: custodian.issues.list
    on_failure: abort
  - id: read-fix-history
    name: Read Fix Effectiveness History
    skill: ocas-custodian
    command: custodian.status
    on_failure: skip
  - id: read-search-history
    name: Read Search History
    skill: ocas-custodian
    command: custodian.status
    on_failure: skip
  - id: diagnose
    name: Research and Diagnose Issue
    skill: ocas-sift
    command: sift.research.start
    on_failure: skip
  - id: propose-repair
    name: Propose Structured Repair
    skill: ocas-mentor
    command: mentor.project.create
    on_failure: abort
  - id: notify
    name: Notify User of Proposal
    skill: ocas-dispatch
    command: dispatch.draft
    on_failure: skip
---

## Step 1: read-issue

**Skill:** ocas-custodian
**Command:** custodian.issues.list

**Inputs:**
- Filter `issues.jsonl` at `~/openclaw/data/ocas-custodian/issues.jsonl` for record matching `issue_id: {{params.issue_id}}`

**Outputs:**
- `issue_record`: the full issue object including fingerprint, tier, status, recurrence_count, search_history

**On failure:** abort
**Notes:** If no matching issue_id found, abort with clear error message.

## Step 2: read-fix-history

**Skill:** ocas-custodian
**Command:** custodian.status

**Inputs:**
- Read `~/openclaw/data/ocas-custodian/fix_effectiveness.jsonl` for entries matching `fingerprint: {{steps.read-issue.issue_record.fingerprint}}`

**Outputs:**
- `fix_history`: array of fix effectiveness records for this fingerprint, showing attempts, successes, failures, recurrence

**On failure:** skip
**Notes:** Missing fix history means no prior auto-fix attempts were made for this fingerprint.

## Step 3: read-search-history

**Skill:** ocas-custodian
**Command:** custodian.status

**Inputs:**
- Extract `search_history` from `{{steps.read-issue.issue_record}}`

**Outputs:**
- `search_history`: array of prior web search attempts with queries used and results
- `already_tried_queries`: list of query strings already attempted

**On failure:** skip
**Notes:** Empty search history means no web searches have been attempted for this issue.

## Step 4: diagnose

**Skill:** ocas-sift
**Command:** sift.research.start

**Inputs:**
- Research goal: diagnose root cause of `{{steps.read-issue.issue_record.fingerprint}}`
- Context: issue description from `{{steps.read-issue.issue_record}}`
- Exclude queries already tried: `{{steps.read-search-history.already_tried_queries}}`
- Fix history showing what has already been attempted: `{{steps.read-fix-history.fix_history}}`

**Outputs:**
- `diagnosis`: structured research findings including probable root cause, recommended fix approach, and confidence level
- `sources`: list of sources consulted

**On failure:** skip
**Notes:** If Sift is not installed, this step is skipped. The proposal step will work with available information only.

## Step 5: propose-repair

**Skill:** ocas-mentor
**Command:** mentor.project.create

**Inputs:**
- Issue record: `{{steps.read-issue.issue_record}}`
- Fix history: `{{steps.read-fix-history.fix_history}}`
- Diagnosis: `{{steps.diagnose.diagnosis}}`

**Outputs:**
- `repair_proposal`: structured repair plan written to `~/openclaw/data/ocas-custodian/reports/repair-{{params.issue_id}}.md`

**On failure:** abort
**Notes:** The proposal must include: root cause assessment, recommended repair steps, risk evaluation, and rollback plan. Write the proposal as a Markdown file in the Custodian reports directory.

## Step 6: notify

**Skill:** ocas-dispatch
**Command:** dispatch.draft

**Inputs:**
- Proposal path: `~/openclaw/data/ocas-custodian/reports/repair-{{params.issue_id}}.md`
- Summary: "Custodian repair proposal ready for {{params.issue_id}}"

**Outputs:**
- `notification_sent`: boolean indicating whether the user was notified

**On failure:** skip
**Notes:** If Dispatch is not installed, log to `decisions.jsonl` instead. The proposal file is the primary deliverable regardless of notification.
