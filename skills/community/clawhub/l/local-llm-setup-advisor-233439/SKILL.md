---
name: local-llm-setup-advisor
description: >-
  Help users with Validated demand: Builders need guidance for running useful AI and LLM workflows locally on consumer CPU or family GPU hardware without depending on cloud-only systems. This requirement is supported by 12 separate online signals across 3 source families, so it represents broader demand rather than a single isolated request.. Use when a user asks for software-and-data, local llm, consumer gpu, cpu inference, llama.cpp, or needs a practical workflow, artifact, checklist, analysis, or implementation support for this requirement.
---

# Local LLM Setup Advisor

## Requirement

Use this skill to help developers, researchers, privacy-conscious users, hobbyists, and small teams who want local AI workflows on ordinary home machines with:

> Validated demand: Builders need guidance for running useful AI and LLM workflows locally on consumer CPU or family GPU hardware without depending on cloud-only systems. This requirement is supported by 12 separate online signals across 3 source families, so it represents broader demand rather than a single isolated request.

Demand score: 98/100 (`70/70` demand, `28/30` local feasibility).
Evidence: 12 signals across 3 source families.

Read `references/requirement-plan.md` when source evidence, planning details, or review criteria are needed.

## Workflow

1. Restate the user's outcome, constraints, available inputs, and success criteria.
2. Inspect technical constraints, propose implementation steps, and include test or verification commands when code or data is involved.
3. Ask only for missing information that materially changes the output; otherwise make reasonable assumptions and continue.
4. Keep the implementation local-hardware friendly: prefer scripts, templates, checklists, and small-model or CPU-safe workflows over cloud-only or large-training approaches.
5. Produce the requested artifact, workflow, checklist, analysis, code change, or decision support.
6. Validate the output against the success criteria and list any remaining risks or follow-up work.

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

Keywords: `software-and-data`, `local llm`, `consumer gpu`, `cpu inference`, `llama.cpp`, `privacy`

Example trigger sentences:

- `Help me Builders need guidance for running useful AI and LLM workflows locally on consumer CPU or family GPU hardware without de.`
- `I need a practical workflow for Builders need guidance for running useful AI and LLM workflows locally on consumer CPU or family GPU hardware without de.`
- `Use $local-llm-setup-advisor to handle Builders need guidance for running useful AI and LLM workflows locally on consumer CPU or family GPU hardware without de.`
