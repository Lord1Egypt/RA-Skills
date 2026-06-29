---
name: llm-api-provider-integration-helper
description: >-
  Help users with Feature Request: Support Response API for MiniMax Provider. Use when a user asks for software-and-data, enhancement, feature, request, support, or needs a practical workflow, artifact, checklist, analysis, or implementation support for this requirement.
---

# LLM API Provider Integration Helper

## Requirement

Use this skill to help maintainers and users asking for software improvements with:

> Feature Request: Support Response API for MiniMax Provider

Read `references/requirement-plan.md` when source evidence, planning details, or review criteria are needed.

## Workflow

1. Restate the user's outcome, constraints, available inputs, and success criteria.
2. Inspect technical constraints, propose implementation steps, and include test or verification commands when code or data is involved.
3. Ask only for missing information that materially changes the output; otherwise make reasonable assumptions and continue.
4. Produce the requested artifact, workflow, checklist, analysis, code change, or decision support.
5. Validate the output against the success criteria and list any remaining risks or follow-up work.

## Expected Outputs

- A tailored answer or artifact for the user's immediate situation.
- A reusable checklist or workflow when the task is repeatable.
- A verification note showing how the result was checked.

## Validation

- The output directly addresses the discovered requirement.
- The user can act on the result without reading the original source post.
- Assumptions, limits, and required inputs are visible.
- The final response includes a short usage or next-step note when helpful.

## Triggers

Keywords: `software-and-data`, `enhancement`, `feature`, `request`, `support`, `response`, `api`, `minimax`, `provider`

Example trigger sentences:

- `Help me Feature Request: Support Response API for MiniMax Provider.`
- `I need a practical workflow for Feature Request: Support Response API for MiniMax Provider.`
- `Use $llm-api-provider-integration-helper to handle Feature Request: Support Response API for MiniMax Provider.`
