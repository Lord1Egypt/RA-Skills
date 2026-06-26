---
name: mbti-analyzer
description: Analyze a user's MBTI from authorized OpenClaw memory, session history, and workspace notes. Use when the user asks for MBTI analysis, personality inference without a questionnaire, an evidence-backed personality report, or a structured type hypothesis from historical conversations.
version: 0.4.0
triggers:
  - "MBTI"
  - "personality analysis"
  - "type me"
  - "分析我的 MBTI"
  - "性格分析"
  - "人格报告"
metadata:
  openclaw:
    commands:
      - command: mbti-report
        description: Generate an MBTI report from authorized historical data.
  clawdbot:
    emoji: "🧠"
    requires:
      bins: ["python3"]
---

# MBTI

Generate an evidence-backed MBTI report from authorized OpenClaw history and workspace notes.

## Quick Start

This package is a **skill**. The public handoff line for other agents lives in `README.md`.

Primary entry points:

- trigger phrases: `MBTI`, `personality analysis`, `type me`
- skill command: `mbti-report`

Minimal runtime requirement:

- `python3`

Local install for development or manual setup:

```bash
ln -s /absolute/path/to/mbti "$CODEX_HOME/skills/mbti"
```

Start an analysis by invoking the skill in chat:

```text
Analyze my MBTI using only my authorized memory and session history
```

For agents and maintainers:

- read this page top to bottom before running any script
- use the existing pipeline scripts below as implementation steps
- do not skip the authorization step
- do not infer MBTI directly from raw history

## At A Glance

What this skill produces:

- `report.html`: primary deliverable
- `report.md`: compact summary
- `analysis_result.json`: type hypothesis, confidence, follow-up questions
- `evidence_pool.json`: scored and traceable evidence

What the first interaction should do:

1. Discover candidate source categories.
2. Show the user what is available.
3. Ask which categories are authorized.
4. Run the extraction → evidence → inference → report pipeline.

## Core Rule

Always separate the workflow into two layers:

1. **Full extraction** from authorized sources into structured records and an evidence pool.
2. **MBTI inference** only from the evidence pool and source summary.

Do **not** infer MBTI directly from the full raw history.

## When To Use

Use this skill when the user wants:

- MBTI analysis from existing conversations or memory
- personality inference without filling out a questionnaire
- a professional-looking personality report with evidence
- a structured summary of likely type, adjacent alternatives, and uncertainties

Do not use this skill for clinical diagnosis or mental-health assessment.

## Authorization First

Before reading any source content:

1. Run source discovery.
2. Show the user which source categories are available.
3. Explain that the report may quote short excerpts unless quoting is disabled.
4. Ask the user to confirm which source categories are allowed.

Default candidate categories:

- workspace long-term memory: `MEMORY.md`
- workspace daily memory: `memory/*.md`
- OpenClaw sessions: `~/.openclaw/agents/*/sessions/*.jsonl`
- OpenClaw memory index: `~/.openclaw/memory/main.sqlite`
- OpenClaw task metadata: `~/.openclaw/tasks/runs.sqlite`
- OpenClaw cron metadata: `~/.openclaw/cron/runs/*.jsonl`

Default exclusions:

- `.env`
- `credentials/*`
- `identity/*`
- device files
- approval files
- generic config files
- gateway and runtime logs

## Execution Flow

If the user does not provide an output directory, write results to:

```text
./.mbti-reports/<timestamp>/
```

Recommended order:

### 1. Discover Candidate Sources

```bash
python3 {baseDir}/scripts/discover_sources.py \
  --workspace-root . \
  --openclaw-home ~/.openclaw \
  --output /tmp/mbti-source-manifest.json
```

Use the manifest to explain what can be analyzed. Do not read content yet.

### 2. Ingest Authorized Sources

```bash
python3 {baseDir}/scripts/ingest_all_content.py \
  --manifest /tmp/mbti-source-manifest.json \
  --approved-source-types workspace-long-memory,workspace-daily-memory,openclaw-sessions \
  --output-dir ./.mbti-reports/<timestamp>
```

This creates:

- `raw_records.jsonl`
- `source_summary.json`

### 3. Build Evidence Pool

```bash
python3 {baseDir}/scripts/build_evidence_pool.py \
  --raw-records ./.mbti-reports/<timestamp>/raw_records.jsonl \
  --source-summary ./.mbti-reports/<timestamp>/source_summary.json \
  --output ./.mbti-reports/<timestamp>/evidence_pool.json
```

This stage should:

- keep recall high
- remove obvious tool noise
- flag pseudo-signals
- merge repeated facts
- retain traceable evidence references

### 4. Infer MBTI From Evidence Pool

```bash
python3 {baseDir}/scripts/infer_mbti.py \
  --evidence-pool ./.mbti-reports/<timestamp>/evidence_pool.json \
  --source-summary ./.mbti-reports/<timestamp>/source_summary.json \
  --output ./.mbti-reports/<timestamp>/analysis_result.json
```

Inference rules:

- use four preferences as the primary decision layer
- use type dynamics and cognitive functions only as a consistency check
- weigh independent strong evidence above repeated weak signals
- keep counterevidence visible
- generate follow-up questions when margins are weak

If `analysis_result.json` contains `needs_followup: true` and the user is available to answer, ask the follow-up questions before finalizing the report.

### 5. Apply Follow-Up Answers And Rerun

After the user answers the low-confidence questions, rerun the pipeline with the answers incorporated as additional user evidence:

```bash
python3 {baseDir}/scripts/apply_followup_answers.py \
  --raw-records ./.mbti-reports/<timestamp>/raw_records.jsonl \
  --source-summary ./.mbti-reports/<timestamp>/source_summary.json \
  --analysis ./.mbti-reports/<timestamp>/analysis_result.json \
  --output-dir ./.mbti-reports/<timestamp> \
  --answer "S/N=<user answer>" \
  --answer "J/P=<user answer>"
```

This updates:

- `raw_records.jsonl`
- `source_summary.json`
- `followup_answers.json`
- `evidence_pool.json`
- `analysis_result.json`
- `report.md`
- `report.html`

If the user declines to answer, keep the current report and surface the uncertainty explicitly.

### 6. Render Final Reports

```bash
python3 {baseDir}/scripts/render_report.py \
  --analysis ./.mbti-reports/<timestamp>/analysis_result.json \
  --evidence-pool ./.mbti-reports/<timestamp>/evidence_pool.json \
  --output-dir ./.mbti-reports/<timestamp> \
  --quote-mode summary \
  --open
```

Add `--open` to automatically open the HTML report in the default browser after rendering.

This creates:

- `report.md`
- `report.html`

### 7. Render A Standalone HTML Preview

When you only need to tune layout, CSS, spacing, or badge/theme behavior, use the built-in preview mode instead of rerunning discovery, ingestion, evidence construction, and inference:

```bash
python3 {baseDir}/scripts/render_report.py \
  --debug-preview \
  --debug-type INTP \
  --output-dir /tmp/mbti-preview
```

This creates a fully populated `report.html` and `report.md` from a bundled fixture so report debugging does not depend on prior pipeline artifacts.

## Stage Testing

When you want to test one stage in isolation, prepare a synthetic fixture for that stage and then run the real stage script against those files.

Prepare fixture inputs:

```bash
python3 {baseDir}/scripts/prepare_stage_fixture.py \
  --stage infer \
  --output-dir /tmp/mbti-stage-infer
```

Then run the stage you actually want to inspect:

```bash
python3 {baseDir}/scripts/infer_mbti.py \
  --evidence-pool /tmp/mbti-stage-infer/evidence_pool.json \
  --source-summary /tmp/mbti-stage-infer/source_summary.json \
  --output /tmp/mbti-stage-infer/analysis_result.json
```

Supported fixture stages:

- `discover`: generates synthetic workspace and OpenClaw source files
- `ingest`: adds `source_manifest.json`
- `evidence`: adds `raw_records.jsonl` and `source_summary.json`
- `infer`: adds `evidence_pool.json`
- `render`: adds `analysis_result.json`
- `followup`: adds `answers_input.json` for `apply_followup_answers.py`

Smoke-test all stage entrypoints with:

```bash
python3 -m unittest tests.test_stage_smoke
```

## Report Rules

The HTML report is the primary artifact. The chat reply should only provide:

- the most likely type
- confidence level
- 2-4 key observations
- the output file paths

Do not freestyle the full report in chat if `report.html` already exists.

## Evidence Rules

Treat the following as high-risk pseudo-signals:

- requests about how the assistant should behave
- formatting preferences
- tool and workflow instructions without self-descriptive context
- command output, logs, stack traces, or copied machine text

Treat the following as stronger evidence:

- repeated self-descriptions
- stable decision-making patterns
- recurring work and reflection habits
- conflict between desired structure and actual behavior
- cross-source consistency

Read these references when needed:

- [analysis_framework.md](references/analysis_framework.md)
- [evidence_rubric.md](references/evidence_rubric.md)
- [report_copy_contract.md](references/report_copy_contract.md)
- [report_structure.md](references/report_structure.md)

## Output Discipline

- Keep tone rigorous and non-clinical.
- Do not use emoji in the final report.
- Present the result as a best-fit hypothesis, not a fixed truth.
- Always include at least one "why not the adjacent type" section.
