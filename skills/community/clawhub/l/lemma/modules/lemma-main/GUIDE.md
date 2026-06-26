---
name: lemma-main
description: "Use for top-level Lemma platform design: frame the business use case, choose the right resource mix, route to specialized skills, and only provision after the design is clear and approved."
---

# Lemma Main

Lemma is a platform for building AI-powered operating systems for business teams.

Use this skill as the top-level orchestrator for Lemma work.
Its job is to:

- understand the business use case
- define the right pod scope
- choose the right resource mix
- decide what must be designed before anything is provisioned
- route to specialized skills for deep implementation work

Default principle:

**Design first. Provision second.**

## When To Use This Skill

Use `lemma-main` when the request is about any of the following:

- turning a business workflow into a pod design
- deciding whether to use tables, files, functions, agents, workflows, assistants, or desks
- scoping a pod
- defining the data model and ownership model
- deciding what should be synchronous vs asynchronous
- deciding whether the user needs an assistant, a desk, or both
- planning changes to an existing pod before implementation

Do not use this skill for deep resource-specific implementation once the design direction is clear. Route to the appropriate specialized skill.

## Default Output

When this skill is the primary driver, produce a design-oriented answer that includes:

- proposed pod scope and boundaries
- recommended resource map
- ownership model
- key execution flows
- open questions that still block correct design
- next specialized skill or skills to use
- whether provisioning should wait for approval

If the request is implementation-ready and consistent with an already-approved design, state that clearly and move to the relevant specialized skill.

## Core Platform Model

### Organization

The top-level workspace that owns members, pods, and integrations.
All pods live inside an organization.
Organization membership is the master people pool.

### Pod

A pod is a bounded operating system for one business use case.
A pod owns its data, logic, automation, and user surfaces.
A well-scoped pod may contain multiple workflows, automations, assistants, or desks, as long as they all serve the same core operating job.

Good pod scope:

- one team
- one primary operating job or domain
- one set of core data
- multiple workflows are fine if they all support the same operating system
- multiple user surfaces are fine if they serve the same job to be done

Bad pod scope:

- multiple unrelated teams or operational domains mixed together
- one pod combining finance, support, hiring, and sales without a clear shared operating loop

Examples:

- `expense-ops`
- `sales-copilot`
- `support-triage`
- `hiring-pipeline`

## Resource Choice Rules

Choose the simplest resource that correctly matches the job.

### Table

Use for durable structured business data the pod must track over time.
Examples: tickets, expenses, leads, applications, approvals.

### Record operations

Use direct record operations for simple single-table CRUD.
Do not create a function just to insert or update one table row.

### File

Use for unstructured documents, attachments, and knowledge that agents or assistants may retrieve.
Examples: manuals, contracts, reports, playbooks.

### Function

Use for deterministic typed backend logic.
Use a function when the action:

- spans multiple tables
- requires validation and coordinated writes
- calls external systems
- must return a typed output

Execution modes:

- `API` for fast synchronous execution
- `JOB` for long-running asynchronous execution

### Agent

Use for judgment-heavy work such as:

- drafting
- classification
- summarization
- extraction
- research

Agents should not be treated as direct callable helpers. They run through tasks.

### Task

Use a task to execute an agent with structured input and inspect completion output.

### Workflow

Use for orchestration across steps, time, triggers, branching, or loops.
Use workflows when the process has multiple stages or handoffs.

### Assistant

Use when conversation is the primary user interaction model.
An assistant can answer questions, trigger actions, and coordinate work using granted resources.

### Desk

Use when humans need a real application with navigation, screens, forms, queues, detail views, and repeatable actions.
A desk is not a one-page poster.
A desk should cover the end-to-end operator workflow.

### Integration

Use when the pod must read from or write to external systems.
Examples: Gmail, Slack, GitHub, Salesforce.

## Fast Selection Matrix

| Need | Use |
| --- | --- |
| Single-table CRUD | `record create/update/bulk-create/bulk-update` |
| Multi-table writes, validation, or external calls | `function` |
| Drafting, classification, summarization, research | `agent` via `task` |
| Multi-step orchestration with branching or scheduling | `workflow` |
| User-facing chat | `assistant` |
| Full operator application with navigation and forms | `desk` |
| Unstructured documents and knowledge retrieval | `file` |
| Team roster and assignment context | `pod member` APIs |

## Non-Negotiable Guardrails

### Pod scope guardrail

Do not mix unrelated operating systems into one pod.
A pod should stay bounded to one business use case.

### Membership guardrail

Do not create `users`, `members`, `team_members`, or `assignees` tables to mirror pod membership.
Organization membership is the master pool.
Pod membership is the team roster for the pod.

For collaborative business records, store explicit ownership fields such as:

- `creator_user_id`
- `assignee_user_id`
- `owner_user_id`
- `reporter_user_id`

Resolve names, emails, and roles from pod member APIs when rendering.
Do not denormalize member identity data into business tables unless there is a specific approved reason.

Use RLS `user_id` only for personal per-user tables.

Valid extra tables include real business concepts such as:

- `support_queues`
- `territories`
- `on_call_rotations`
- `approval_groups`

### Function guardrail

Do not create a function for a single-table insert or update.
Use record operations directly unless business logic truly requires a function.

### Desk guardrail

Do not design a desk as a single landing page or static poster.
Design it as a real multi-screen product for operators.

### Provisioning guardrail

Do not provision non-trivial resources before discovery and design are complete.

## Trivial Changes Rule

A full design document is usually required for new pods, new workflows, new desks, new assistants, new integrations, or any change that affects the data model or ownership model.

For narrow edits that are clearly consistent with an already-approved design, do a short design check instead of forcing a full redesign. Examples:

- add one column to an existing table
- adjust a function config value
- update an assistant instruction
- patch a desk screen without changing the operating model

If there is real ambiguity about scope, ownership, or resource choice, stop and design first.

## Required Workflow

For non-trivial Lemma work, follow this sequence.

### 1. Discover the operating system

Understand:

1. what business event starts the process
2. what durable facts must be stored
3. which steps are deterministic vs judgment-heavy
4. what must happen synchronously vs asynchronously
5. who interacts via assistant vs desk vs workflow form
6. what external systems require integrations
7. what the ownership model is

During discovery, ask one clear question at a time when a missing detail blocks correct design.

### 2. Write the design before provisioning

For any meaningful pod build or edit, produce a design document that covers:

- scope and boundaries
- resource map
- data model
- ownership model
- execution flows
- permissions
- rollout plan

Show the design for approval before provisioning.

### 3. Provision from bundles, not ad hoc drift

For meaningful changes, work from bundle files rather than scattered one-off CLI mutations.

### 4. Enforce the backend build-order checkpoint

Enforce this sequence for non-trivial pods:

1. integrations
2. functions
3. workflows
4. desk

Sequence shorthand: `integrations -> functions -> workflows -> desk`.

Block desk work until upstream checks are green.
Required checkpoint before desk wiring:

1. integration smoke tests pass with saved schema and sample response artifacts
2. function smoke tests pass for every desk-triggered action
3. workflow runs pass for every workflow the desk starts or resumes

### 5. Verify with real execution

Import success is not enough.
Every important resource must be validated with realistic test execution.

## Provisioning Patterns

### New pod

1. create the pod
2. inspect with `lemma pod describe --pod-id <pod-id>`
3. build a bundle from the approved design
4. provision tables and folders first
5. configure integrations and run smoke tests with saved artifacts
6. provision functions and agents next
7. run function and agent smoke tests with realistic data
8. provision workflows
9. run workflow tests end to end
10. block desk work until integrations, functions, and workflows are green
11. build or update desks
12. dry-run import with `--dry-run --upsert`
13. fix every issue
14. run the real import with `--upsert`
15. verify each important resource with real execution

### Existing pod edits

1. inspect the live pod state
2. export to a local bundle
3. edit the bundle files
4. change backend resources before user surfaces whenever possible
5. re-verify integrations and save smoke artifacts when app calls changed
6. test function changes first
7. update workflows next if needed
8. test workflows
9. block desk edits until integration, function, and workflow tests pass
10. dry-run import
11. real import with `--upsert`
12. re-verify edited resources

## Recommended Provisioning Order

For most non-trivial pods, use this order:

1. tables
2. folders and files structure
3. integrations with smoke-test artifacts
4. functions
5. agents
6. backend verification
7. workflows
8. workflow verification
9. assistants
10. desks after upstream readiness gate passes
11. final end-to-end verification

Default stance:

- do not build a desk against an unstable backend
- do not start desk work until integrations, functions, and workflows are all green
- do not design workflows before the functions and agents they depend on exist
- do not treat the desk as the first proof that the pod works

## Verification Rules

Always verify behavior, not just import status.

- functions: run with realistic input and inspect output
- agents: run a realistic task and inspect quality
- assistants: send real messages and confirm flow
- workflows: trigger a test run and inspect graph behavior
- desks: build, load, and test real UI behavior

If verification fails:

1. update the bundle
2. dry-run again
3. re-import with `--upsert`
4. re-test

## Pod Member Rule

For any team-based workflow such as assignment, ownership, queue routing, or reviewer selection, start with:

```bash
lemma pod member-list --pod-id <pod-id>
```

Use `user_id` from pod membership when populating ownership fields on business records.
Do not create membership mirror tables.

## Routing To Specialized Skills

After the design direction is clear, route to the relevant skill:

| Area | Skill |
| --- | --- |
| Tables, records, files | `lemma-datastores` |
| Functions | `lemma-functions` |
| Agents and tasks | `lemma-agents` |
| Workflows | `lemma-workflows` |
| Assistants | `lemma-assistants` |
| Desks | `lemma-desks` |
| Integrations | `lemma-integrations` |
| Workspace execution, browser, Playwright | `lemma-workspace` |
| Inline visual widgets | `lemma-widget` |

Do not assume payload shapes or provisioning behavior without reading the relevant specialized skill.
Desk setup and bundling must follow `lemma-desks`.

## CLI Reference

Use these commands as quick entry points, not as a substitute for design.

```bash
# Global snapshot
lemma ls
lemma ls --org-id <org-id> --pod-id <pod-id>

# Organization
lemma organization list
lemma organization member-list --org-id <org-id>

# Pod
lemma pod list --org-id <org-id>
lemma pod create <name> --org-id <org-id> --description "..." [--icon-url <url>]
lemma pod get --pod-id <pod-id>
lemma pod describe --pod-id <pod-id>
lemma pod member-list --pod-id <pod-id>
lemma pod member-add --pod-id <pod-id> --organization-member-id <org-member-id> --role POD_EDITOR
lemma pod member-update-role --pod-id <pod-id> --member-id <user-id> --role POD_ADMIN
lemma pod member-remove --pod-id <pod-id> --member-id <user-id>

# Inspect resource schema before provisioning
lemma operation show table.create
lemma operation show function.create
lemma operation show agent.create
lemma operation show workflow.create
lemma operation show assistant.create
lemma operation show desk.create

# Bundle
lemma pod import <bundle-dir> --pod-id <pod-id> --dry-run --upsert
lemma pod import <bundle-dir> --pod-id <pod-id> --upsert
lemma pod export --pod-id <pod-id> <bundle-dir>
```

Use `lemma <resource> --help` and `lemma <resource> <command> --help` before running commands when flags or payload expectations matter.

## Known CLI Behavior

Use [`references/known-cli-behavior.md`](references/known-cli-behavior.md) as the shared source of command-shape quirks.
Do not duplicate these quirks across every skill; link to this file from specialized skills.

## Context Resolution

CLI resolves in this order:

1. explicit flag
2. environment variable
3. config
4. error

Key env vars:

- `LEMMA_TOKEN`
- `LEMMA_BASE_URL`
- `LEMMA_AUTH_URL`
- `LEMMA_ORG_ID`
- `LEMMA_POD_ID`

Key flags:

- `--org-id`
- `--pod-id`

If `LEMMA_ORG_ID` is missing, run `lemma organization list`, ask once which organization to use, then set config.

File indexing is asynchronous.
Uploaded files may remain `PENDING` before search becomes available.

## Default Operating Stance

When working in Lemma:

- prefer clear pod boundaries
- prefer the simplest resource that fits
- prefer direct record operations for simple CRUD
- prefer explicit ownership fields on collaborative records
- prefer workflows for orchestration
- prefer bundles over ad hoc drift
- prefer real verification over assumed success

Always keep the platform honest to its central rule:

**Design first. Provision second.**
