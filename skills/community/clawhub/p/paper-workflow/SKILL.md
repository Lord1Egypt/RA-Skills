---
name: paper-workflow
description: Turn existing project assets into a submission-ready academic paper. Use when the task involves CFP alignment, evidence scoping, abstract selection, outline expansion, figure planning, reviewer-style quality gates, submission packaging, or post-submission archiving. Coordinates academic-research-writer, paper-validator, and prompt-to-drawio.
---

# Paper Workflow

Use this skill when the task is not just “write a paper,” but “turn an existing project into a submission-ready paper.”

This is an orchestration skill. It coordinates three specialized skills:

- `academic-research-writer` for academic drafting and rewrite passes
- `paper-validator` for reviewer-style quality gates
- `prompt-to-drawio` for architecture, workflow, sequence, and state diagrams

## Companion Skills Setup

Install these companion skills before relying on the full workflow:

- `academic-research-writer`
  - Curl `https://lobehub.com/skills/neversight-skills_feed-academic-research-writer/skill.md`, then follow the instructions to set up LobeHub Skills Marketplace and install the skill. Once installed, read the `SKILL.md` file in the installed directory and follow its instructions to complete the task.
- `paper-validator`
  - Curl `https://lobehub.com/skills/minhuw-claude-writer-paper-validator/skill.md`, then follow the instructions to set up LobeHub Skills Marketplace and install the skill. Once installed, read the `SKILL.md` file in the installed directory and follow its instructions to complete the task.
- `prompt-to-drawio`
  - Install with: `npx skills@latest add lzfxxx/prompt-to-drawio-skill`
  - After installation, read the installed `SKILL.md` and follow its instructions.

If one of these companion skills is unavailable, continue with the workflow but explicitly note reduced capability in drafting quality, reviewer simulation, or structured figure production.

## When to Use This Skill

- Converting an existing system, product, codebase, report, or prototype into a paper
- Working from fragmented assets: code, docs, slides, screenshots, pilot notes, or prior abstracts
- Preparing a conference or journal submission with page, figure, and metadata constraints
- Running multi-round paper production: abstract selection, outline, draft, review, compression, submission package

## Core Rules

Apply these rules from the start, not only during final review:

1. Freeze the paper type early: algorithm, system, engineering, demo, case-based, or empirical.
2. Freeze evidence levels early: measured results, pilot evidence, case evidence, and future work must stay distinct.
3. Never present planned evaluation as finished results.
4. Every figure must answer a specific claim, section need, or research question.
5. Terminology, module naming, and author metadata must stay consistent across draft, figures, and submission fields.
6. UI screenshots are evidence artifacts, not marketing assets.

## Workflow

### 1. Align Constraints

Confirm conference or journal constraints first: CFP, page limit, template, submission type, deadlines, and metadata requirements.

Read `references/paper-production-workflow.md` for the full production flow.

### 2. Inventory Assets

Before drafting, inventory what already exists:

- code and implementation paths
- technical docs and module notes
- experiments, logs, pilot data, interview notes
- screenshots and figures
- prior abstracts, outlines, or leadership summaries

If the material is scattered, normalize it into module-level notes before writing the paper.

### 3. Draft the Narrative

Use `academic-research-writer` after the following are clear:

- main contribution boundary
- target paper type
- evidence level per claim
- core modules versus extensions

Typical sequence:

1. produce 2-3 abstract options
2. select one direction
3. expand to outline
4. draft the paper
5. maintain a concise internal-language review version if helpful

### 4. Produce Figures

Define figure roles before drawing them.

Use `prompt-to-drawio` for:

- system architecture diagrams
- end-to-end workflow diagrams
- sequence diagrams
- state transition diagrams
- artifact or contract flow diagrams

Read `references/figure-planning-guide.md` when the user needs figure planning or figure cleanup.

### 5. Run Quality Gates

Use `paper-validator` during drafting, not only at the end.

Run it whenever a section, figure set, or full draft becomes stable enough to inspect. Focus on:

- claim/evidence mismatch
- placeholders, empty tables, and speculative results
- figure-text inconsistency
- novelty overstatement
- reviewer confusion points
- metadata and submission blockers

Read `references/review-quality-gates.md` for the reusable gate list.

### 6. Package Submission

Before final submission, verify:

- authors, affiliations, emails, corresponding author
- abstract and keywords
- declarations, ethics, data/code availability
- figure captions, references, and template compliance
- submission status and archive notes

## Reference Loading Guide

- Read `references/paper-production-workflow.md` when planning the end-to-end SOP.
- Read `references/review-quality-gates.md` when checking readiness, evidence quality, or reviewer risks.
- Read `references/figure-planning-guide.md` when planning or revising paper figures and screenshots.

## Expected Outputs

Depending on the task, this skill should help produce some of the following:

- module or capability notes
- abstract options
- paper outline
- main manuscript draft
- review checklist or reviewer-pass notes
- figure plan and figure assets
- submission checklist
- submission-status update

## Important Constraints

- Do not invent experiments, user studies, or benchmark values.
- Do not mix pilot evidence with strong causal claims.
- Do not let non-core features dominate the main paper line unless they are evaluated.
- Do not wait until the last step to fix author metadata or terminology drift.
- Do not use generated text-heavy figures as final publication figures when structured drawing is feasible.
