---
name: lemma
description: "Lemma is an AI operating system platform for business teams. Use this as the single entrypoint when designing, provisioning, testing, or improving Lemma pods, datastores, integrations, functions, workflows, desks, assistants, agents, widgets, or workspace execution, then route to the matching module guide."
---

# Lemma

Use this as the main skill for the Lemma package.
This package is organized as one parent skill with domain modules under `modules/`.

Lemma helps teams build AI-powered operating systems around real business workflows.
Each pod combines data, logic, orchestration, and operator experiences in one bounded system.

## Required Routing Step

Before implementation, pick the module guide that matches the task and follow it.

- Platform design and sequencing: `modules/lemma-main/GUIDE.md`
- Integrations and operation discovery: `modules/lemma-integrations/GUIDE.md`
- Functions and backend patterns: `modules/lemma-functions/GUIDE.md`
- Datastore design and seed data: `modules/lemma-datastores/GUIDE.md`
- Workflow orchestration: `modules/lemma-workflows/GUIDE.md`
- Desk app architecture and implementation: `modules/lemma-desks/GUIDE.md`
- Assistant behavior and configuration: `modules/lemma-assistants/GUIDE.md`
- Agent design and task execution: `modules/lemma-agents/GUIDE.md`
- Workspace execution and troubleshooting: `modules/lemma-workspace/GUIDE.md`
- Inline widget work: `modules/lemma-widget/GUIDE.md`

## Cross-Module Convention

Use shared CLI drift notes from:
`modules/lemma-main/references/known-cli-behavior.md`

## Build Order Guardrail

For non-trivial end-to-end delivery, follow:

1. integrations
2. functions
3. workflows
4. desks

Do not start desk action wiring until upstream verification is green.
