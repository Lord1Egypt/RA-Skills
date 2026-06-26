---
name: promo-video-maker
description: "Single front-door skill for video production work. Use when a user wants to create a promo video, teaser, explainer, ad, short-drama episode, comic episode, storyboard-driven video, or project-based multi-episode production flow. This skill should internally orchestrate writing, character design, scene design, storyboard, voice, BGM, edit planning, generation, and project handoff without exposing sub-skills."
---

# Promo Video Maker

This is the only public entrypoint for video production work.

The user should feel like one production team has taken over:
- understanding the brief
- quoting the cost
- deciding whether this is one-shot or project work
- producing the right assets
- handing off either final outputs or a web project workspace

Do not split this into multiple public skills.
Do not ask the user to choose internal roles.

## Front-Door Rule

Use this skill when the user asks for any of these outcomes:
- promo video
- launch video
- teaser
- explainer
- ad script
- storyboard pack
- short-drama episode
- comic episode
- multi-episode video project
- "帮我做一个视频"
- "帮我做一个短剧项目"

If the user names `promo-video-maker`, do not reroute.

## Two Modes

This skill supports two operating modes.

### `one-shot`

Use when the user wants a single output:
- one image or image edit
- one short video
- one script or outline
- one voice clip
- one BGM track
- one storyboard pack

Rules:
- do not force project creation
- do not force workspace writeback
- return the result, task status, cost, and optional upgrade-to-project path

### `project`

Use when the user is building an ongoing production:
- multi-episode short drama
- comic episode pipeline
- "继续这个项目"
- "写到工作台里"
- "给我 web 链接"

Rules:
- project context is required
- outputs should be persisted to cloud project state
- project assets and canvas should be updated
- return project summary and workspace access

Read `references/mode-routing.md` before changing mode behavior.

## Control Room Contract

When the work is non-trivial, always show a short status block:

- `Stage`
- `Current Owner`
- `Current Gate`
- `Current Artifact`
- `Estimated Credits`
- `Running Jobs`
- `Project`
- `Blocker`
- `Next Action`

Use the role names from `references/control-room.md`.
Use the stage rules from `references/team-gates.md`.

## Intake

Do not turn this into a long questionnaire.

Collect or infer the minimum that changes the production path:
- objective
- output type
- target platform and aspect ratio
- target duration or episode count
- tone / genre / audience
- whether this is `one-shot` or `project`
- whether source materials already exist

If the request is vague, produce the smallest useful first step and keep moving.

Before starting any paid execution, the skill must produce a quote.

## Internal Team

This skill internally orchestrates these roles:

- `Showrunner`
- `Head Writer`
- `Character Director`
- `Scene Director`
- `Storyboard Director`
- `Voice Director`
- `Music Director`
- `Edit Director`
- `Pipeline Operator`

Read `references/worker-playbooks.md` to decide which role owns the current stage.

## Workflow

Default control flow:

1. detect mode
2. intake
3. quote
4. plan the next production stage
5. execute the relevant capability or project phase
6. poll long-running jobs when needed
7. hand back either outputs or project/workspace access

### `one-shot` path

Typical stage sequence:
- `intake`
- `quote`
- `execute`
- `poll`
- `handoff`

### `project` path

Typical stage sequence:
- `intake`
- `project-select-or-create`
- `quote`
- `story`
- `character`
- `scene`
- `storyboard`
- `audio`
- `video`
- `assembly`
- `review`
- `handoff`

Do not jump into generation before the quote step passes.

## Quote-First Rule

Every paid action must be priced before execution.

For `one-shot`, return a single-action quote.
For `project`, return either:
- a phase quote
- or a full-project estimate with line items

The quote should be shown in credits. If the backend also returns USD, treat that as backend settlement detail.

Read `references/pricing-and-approval.md` before changing quote behavior.

## Project Access

Users may have multiple projects.

In `project` mode, the skill must support:
- list my projects
- inspect one project summary
- continue an existing project
- create a new project
- get a web workspace link

If the user asks to continue previous work, do not create a new project until the skill has checked whether a suitable existing project already exists.

Read `references/project-access.md` before changing project retrieval or handoff rules.

## Hub Execution

This public skill is not the backend.

Use the Maliang Hub / Nano API surface as the execution layer:
- atomic capabilities for writing, design, audio, image, and video
- project persistence for project mode
- task polling for long-running jobs
- workspace link generation for web handoff

Read `references/hub-execution.md` before changing execution routing.

## Helper Scripts

This package may use lightweight helper scripts for transport:
- `scripts/bootstrap.sh`
- `scripts/hub-api.sh`
- `scripts/quote.sh`
- `scripts/poll-task.sh`
- `scripts/encode-file.sh`

These scripts should reuse the same cloud account and API key flow as the Hub product layer.

## Expected Outputs

The skill should produce one of two public outcomes.

### `one-shot` outcome

- result or task receipt
- credit quote / actual cost
- artifacts or URLs when available
- optional "save into project" upgrade path

### `project` outcome

- project id or selected project
- current project summary
- current stage result
- active task receipts
- workspace link
- recommended next director action

Detailed artifact contracts live in `references/artifact-contracts.md`.

## Public Package Boundary

This package should contain only:
- workflow contract
- agent metadata
- references
- lightweight helper scripts

Do not put backend implementation code in this package.

## Guardrails

- do not expose sub-skills to the user
- do not make the user choose internal workers
- do not skip quote for paid execution
- do not force project mode for one-shot requests
- do not default to one-shot when the user is clearly building a multi-episode project
- do not hide the current stage or current owner on non-trivial work
- do not create duplicate projects without first checking for an existing project when the user asks to continue work
- do not promise final composition if only storyboard or generation tasks exist
- do not confuse temporary local state with canonical cloud project state

## References

- Read `references/mode-routing.md` for one-shot vs project routing.
- Read `references/control-room.md` for status block and role ownership.
- Read `references/worker-playbooks.md` for role-specific operating rules.
- Read `references/team-gates.md` for stage transitions and readiness.
- Read `references/pricing-and-approval.md` for quote and approval behavior.
- Read `references/project-access.md` for multi-project handling and workspace access.
- Read `references/director-mode.md` for project-mode expectations.
- Read `references/hub-execution.md` for backend execution mapping.
- Read `references/artifact-contracts.md` for output shapes.
- Read `references/video-formats.md` when structure, placement, or runtime format matters.
- Read `references/production-brief.md` when preparing a shot list, production pack, or editor handoff.
