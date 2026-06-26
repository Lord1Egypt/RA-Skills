---
name: openai-deep-research-skill
description: Execute multi-step deep research with the OpenAI Responses API, including question decomposition, evidence gathering with web search, contradiction tracking, and final cited report synthesis. Use when Codex must investigate complex or high-stakes topics (market analysis, policy tracking, technical due diligence, vendor comparison, risk assessment) and deliver structured artifacts (`plan.json`, `findings.json`, `report.md`) rather than ad-hoc answers.
---

# OpenAI Deep Research

## Overview

Run a deterministic research workflow that separates planning, evidence collection, and report synthesis.
Generate reusable research artifacts under an output directory for auditability and iteration.

## Workflow

1. Define research scope.
2. Run the script to generate plan, findings, and report artifacts.
3. Evaluate report quality with the checklist.
4. Rerun with adjusted depth/model/tool settings when gaps remain.

## Quick Start

Install dependencies:

```bash
cd openai-deep-research-skill
python3 -m pip install -r scripts/requirements.txt
```

Run a real research job:

```bash
python3 scripts/deep_research.py "中国AI Agent市场2026年商业化路径" \
  --language zh-CN \
  --depth 6 \
  --research-depth deep \
  --max-total-output-tokens 20000 \
  --parallel 3
```

Run a local dry-run without API calls:

```bash
python3 scripts/deep_research.py "sample topic" --dry-run
```

## Runtime Inputs

Set `OPENAI_API_KEY` before running real jobs.
Use `OPENAI_BASE_URL` only when routing through a compatible gateway.

Tune key flags:

- `--depth`: Control breadth of decomposition (2-12).
- `--research-depth`: Control per-question evidence depth (`shallow|standard|deep`).
- `--parallel`: Control concurrent evidence runs (1-8).
- `--planner-model`: Choose planning model.
- `--research-model`: Choose evidence model.
- `--writer-model`: Choose synthesis model.
- `--planner-max-output-tokens`: Cap planner response size.
- `--research-max-output-tokens`: Cap each sub-question research response size.
- `--writer-max-output-tokens`: Cap final report synthesis response size.
- `--max-total-output-tokens`: Hard limit for estimated run output tokens.
- `--disable-web-search`: Disable web tool for internal-data-only runs.
- `--web-tool-type`: Override tool type when endpoint uses a non-default web-search tool name.

## Artifact Contract

Write one run directory per execution: `outputs/<timestamp>-<topic-slug>/`.
Produce these files:

- `run_meta.json`: runtime parameters and metadata.
- `plan.json`: normalized sub-question plan.
- `plan_raw.txt`: raw planner model output.
- `findings.json`: per-question evidence summaries.
- `research_raw.json`: raw responses per sub-question.
- `report.md`: final cited report.

## Quality Gate

Apply all checks before accepting `report.md`:

1. Verify each sub-question has explicit evidence or explicit gap notes.
2. Verify source links are absolute URLs and point to relevant content.
3. Verify contradictory evidence is surfaced in `Contradictions and Uncertainty`.
4. Verify recommendation statements are specific and actionable.
5. Verify weak-confidence sections are marked clearly.
6. Verify all required top-level sections exist in Markdown (`Executive Summary`, `Key Findings`, `Evidence by Sub-question`, `Contradictions and Uncertainty`, `Recommendations`, `Sources`).

Use [references/research-quality.md](references/research-quality.md) for scoring rubric and iteration guidance.

## Troubleshooting

If execution fails with missing package errors, install dependencies from `scripts/requirements.txt`.
If JSON parsing fails, rerun with the same topic and lower `--depth`, then inspect `plan_raw.txt` or `research_raw.json`.
If web-search tool type is rejected, pass a compatible value via `--web-tool-type` or disable web search.
