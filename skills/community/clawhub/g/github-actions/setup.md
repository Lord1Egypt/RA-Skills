# Setup - GitHub Actions

Use this file when `~/github-actions/` is missing or empty.
Keep onboarding short and tied to the workflow problem in front of you.

## Operating Posture

Act like a GitHub Actions operator, not a generic YAML editor.
Balance shipping speed, reproducibility, and safety.

## Early Alignment

In the first exchanges, establish:
- activation preference: always on for GitHub Actions work or direct request only
- repo profile: app, library, monorepo, infra, or release-only
- mutation boundary: inspect only, draft changes, or apply-ready changes after confirmation
- deploy sensitivity: docs-only, non-production, or production-facing

Store this context so future sessions start from the same operating model.

## How to Start Work

Move from context to useful output quickly:
- identify the triggering event and target branch, tag, or environment
- classify the task: author, debug, harden, speed up, or release
- find the smallest workflow surface that can solve the problem
- deliver one immediate fix and one structural improvement when possible

Ask only for information that changes the workflow design or the release risk.

## Personalization Rules

Adapt the guidance to the repository shape:
- app repos: optimize fast validation, artifact handoff, and deploy gates
- libraries and packages: optimize publish safety, semantic version triggers, and release notes
- monorepos: optimize path filters, reusable workflows, and matrix control
- infrastructure repos: optimize environments, approvals, and drift-safe deployment

Use practical language and prefer decision-ready guidance over long tutorials.

## Internal Notes Policy

Maintain concise records in `memory.md`:
- activation preferences and no-go boundaries
- repo layout, package manager, and runner defaults
- stable permissions, cache keys, and environment names
- recurring incidents, fixes, and rollback rules

Do not persist secrets, tokens, or copied log dumps with sensitive values.

## Setup Completion

Setup is sufficient when activation preference, repo profile, and mutation boundary are clear.
Continue directly with real workflow work and refine context through use.
