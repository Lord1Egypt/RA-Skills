# paper-workflow

A reusable orchestration skill for turning existing project assets into a submission-ready academic paper.

This skill is designed for AI coding agents that support the `skills` ecosystem. It helps the agent coordinate paper planning, asset inventory, abstract selection, outline expansion, drafting, reviewer-style quality gates, figure planning, submission packaging, and post-submission archiving.

## What This Skill Does

`paper-workflow` is not a domain-specific writing template. It is a general paper-production workflow for projects that already have source assets such as code, technical documents, screenshots, pilot notes, or internal summaries.

It is especially useful when the paper task includes:

- aligning to a CFP, page limit, or template
- turning fragmented project materials into a coherent paper narrative
- separating real evidence from future work
- planning publication-quality figures
- catching reviewer-facing issues early instead of only at the end
- packaging metadata and submission-ready deliverables

## Companion Skills

This skill coordinates three companion skills:

- `academic-research-writer`
  - used for academic drafting and rewrite passes
- `paper-validator`
  - used for reviewer-style critique, claim-evidence checks, and readiness gates
- `prompt-to-drawio`
  - used for architecture, workflow, sequence, and state diagrams

## Installation

Install this skill from GitHub with the `skills` CLI:

```bash
npx skills add https://github.com/lzfxxx/paper-workflow
```

If your agent expects owner/repo shorthand, use:

```bash
npx skills add lzfxxx/paper-workflow
```

## Install Companion Skills

### academic-research-writer

Curl `https://lobehub.com/skills/neversight-skills_feed-academic-research-writer/skill.md`, then follow the instructions to set up LobeHub Skills Marketplace and install the skill. Once installed, read the `SKILL.md` file in the installed directory and follow its instructions to complete the task.

### paper-validator

Curl `https://lobehub.com/skills/minhuw-claude-writer-paper-validator/skill.md`, then follow the instructions to set up LobeHub Skills Marketplace and install the skill. Once installed, read the `SKILL.md` file in the installed directory and follow its instructions to complete the task.

### prompt-to-drawio

Install from GitHub with the skills CLI:

```bash
npx skills@latest add lzfxxx/prompt-to-drawio-skill
```

After installation, read the installed `SKILL.md` and follow its instructions.

## Quick Usage

After installation, invoke the skill with a direct task prompt such as:

```text
Use paper-workflow to turn this existing project into a submission-ready conference paper. First inventory the assets, freeze the paper type and evidence levels, then propose three abstract options.
```

A second good entry prompt is:

```text
Use paper-workflow on this draft. Run reviewer-style quality gates, identify claim-evidence mismatches, and tell me which figures should be redrawn with draw.io.
```

## Typical Workflow

1. Confirm venue constraints: CFP, paper type, page limit, template, dates, metadata.
2. Inventory assets: code, docs, experiments, pilot notes, screenshots, previous summaries.
3. Normalize and scope: separate core contribution from extensions and real evidence from planned work.
4. Produce abstract options and select one direction.
5. Expand to outline and section-level claim/evidence mapping.
6. Draft the manuscript with academic writing support.
7. Plan and build figures with clear claim coverage.
8. Run reviewer-style gates throughout drafting.
9. Compress and package the final submission.
10. Archive the submission state.

## Core Quality Rules

- Freeze the paper type early.
- Freeze evidence levels early.
- Do not present planned evaluation as finished results.
- Every figure must support a concrete section claim or research question.
- Keep metadata, module naming, and terminology consistent across text and figures.
- Treat UI screenshots as evidence, not marketing material.

## Example Prompts

- `Use paper-workflow to turn this prototype into a conference paper.`
- `Inventory these project assets and propose three paper abstracts.`
- `Plan the figures for this system paper and tell me which ones should be draw.io vs screenshots.`
- `Run reviewer-style gates on this draft before submission.`
- `Package this manuscript for submission and list remaining blockers.`

## Repository Layout

```text
.
├── SKILL.md
├── references/
│   ├── paper-production-workflow.md
│   ├── review-quality-gates.md
│   └── figure-planning-guide.md
├── README.md
├── LICENSE
└── .gitignore
```

## License

MIT. See `LICENSE`.
