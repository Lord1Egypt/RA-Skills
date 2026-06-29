---
name: local-llm-setup-advisor
description: >-
  Help users with [Feature Request] Support for Remote llama.cpp Server via URL Endpoint. Use when a user asks for work-productivity, feature, request, support, remote, or needs a practical workflow, artifact, checklist, analysis, or implementation support for this requirement.
---

# Local LLM Setup Advisor

## Requirement

Use this skill to help maintainers and users asking for software improvements with:

> [Feature Request] Support for Remote llama.cpp Server via URL Endpoint

Read `references/requirement-plan.md` when source evidence, planning details, or review criteria are needed.

## Workflow

1. Restate the user's outcome, constraints, available inputs, and success criteria.
2. Create a concise work plan, template, automation outline, or decision aid that reduces manual coordination.
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

Keywords: `work-productivity`, `feature`, `request`, `support`, `remote`, `llama`, `cpp`, `server`, `via`

Example trigger sentences:

- `Help me [Feature Request] Support for Remote llama.cpp Server via URL Endpoint.`
- `I need a practical workflow for [Feature Request] Support for Remote llama.cpp Server via URL Endpoint.`
- `Use $local-llm-setup-advisor to handle [Feature Request] Support for Remote llama.cpp Server via URL Endpoint.`
