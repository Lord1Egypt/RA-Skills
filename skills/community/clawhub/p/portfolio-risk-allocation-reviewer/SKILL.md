---
name: portfolio-risk-allocation-reviewer
description: >-
  Help users with Validated demand: Investors and advisors need local workflows for reviewing portfolio allocation, concentration risk, fees, rebalancing needs, and plain-language investment policy notes from brokerage exports. This requirement is supported by 12 separate online signals across 2 source families, so it represents broader demand rather than a single isolated request.. Use when a user asks for business-and-operations, portfolio allocation, risk review, rebalancing, brokerage export, or needs a practical workflow, artifact, checklist, analysis, or implementation support for this requirement.
---

# Portfolio Risk Allocation Reviewer

## Requirement

Use this skill to help individual investors, financial advisors, analysts, and family-office operators who review portfolios from CSV exports or brokerage statements with:

> Validated demand: Investors and advisors need local workflows for reviewing portfolio allocation, concentration risk, fees, rebalancing needs, and plain-language investment policy notes from brokerage exports. This requirement is supported by 12 separate online signals across 2 source families, so it represents broader demand rather than a single isolated request.

Demand score: 90/100 (`70/70` demand, `30/30` local feasibility).
Evidence: 12 signals across 2 source families.

Read `references/requirement-plan.md` when source evidence, planning details, or review criteria are needed.

## Workflow

1. Restate the user's outcome, constraints, available inputs, and success criteria.
2. Turn the operational problem into a repeatable process, checklist, template, or lightweight analysis.
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

Keywords: `business-and-operations`, `portfolio allocation`, `risk review`, `rebalancing`, `brokerage export`, `investment policy`

Example trigger sentences:

- `Help me Investors and advisors need local workflows for reviewing portfolio allocation, concentration risk, fees, rebalancing ne.`
- `I need a practical workflow for Investors and advisors need local workflows for reviewing portfolio allocation, concentration risk, fees, rebalancing ne.`
- `Use $portfolio-risk-allocation-reviewer to handle Investors and advisors need local workflows for reviewing portfolio allocation, concentration risk, fees, rebalancing ne.`
