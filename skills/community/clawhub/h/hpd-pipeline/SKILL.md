---
name: hpd-pipeline
description: Use when the HPD lab needs a repeatable Planner -> Designer -> conditional Developer -> Tester flow for an approved idea, with Lobster-first and sequential fallback behavior.
metadata: { "openclaw": { "emoji": "🧪" } }
---

# hpd-pipeline

Follow the stage contract in `{baseDir}/references/project-pipeline.md`.

## Preferred mode

- If the `lobster` CLI is available on `PATH`, prefer a Lobster workflow.
- If `lobster` is unavailable, run the same stages sequentially in one turn and mark `lobster_ready: false`.

## Required output sections

- `brief`
- `cost_estimate`
- `bom`
- `assembly_plan`
- `render_prompt`
- `software_spec` when needed
- `tester_report`
- `artifact_manifest`
- `completion_summary`

## Optional artifact fields

Use these when real outputs exist. If they do not exist, say so explicitly instead of implying they were produced.

- `render_image`
- `cad_step_path`
- `cad_stl_paths`
- `assembly_doc_path`
- `source_code_path`
- `firmware_build_path`

## Rules

- Keep outputs Notion-first.
- Do not claim STEP/STL or validated firmware unless it was actually produced.
