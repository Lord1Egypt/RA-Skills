# Artifacts

## Purpose
Define the smallest useful artifact shape for the MVP of `openclaw-consensus`.

The artifact model should be simple, inspectable, and easy to explain publicly.

## Run directory
Each run should create one local run root containing:
- the original brief
- run metadata
- round-1 outputs
- round-2 outputs
- final synthesis

Suggested shape:

```text
runs/<timestamp>-<slug>/
├── brief.md
├── run.json
├── round-1/
│   ├── <model-a>.md
│   ├── <model-b>.md
│   └── <model-c>.md
├── round-2/
│   ├── <model-a>.md
│   ├── <model-b>.md
│   └── <model-c>.md
└── final.md
```

## Required artifacts
### `brief.md`
Contains:
- original user brief
- optional label

### `run.json`
Contains structured run metadata such as:
- timestamp
- run label
- original brief path
- selected models
- orchestrator model
- round count
- status
- stop reason

Suggested MVP fields:
```json
{
  "run_id": "2026-04-29T03-35-00Z-example-brief",
  "label": "optional-human-label",
  "created_at": "2026-04-29T03:35:00Z",
  "brief_path": "brief.md",
  "selected_models": [
    "anthropic/claude-sonnet-4-6",
    "openai/gpt-5.5",
    "xai/grok-3"
  ],
  "orchestrator_model": "openai-codex/gpt-5.4",
  "round_count": 2,
  "status": "completed",
  "stop_reason": "STOP_AT_ROUND_2",
  "artifacts": {
    "round_1_dir": "round-1",
    "round_2_dir": "round-2",
    "final": "final.md"
  }
}
```

### `round-1/<model>.md`
Contains the independent first-pass output from one selected model.

### `round-2/<model>.md`
Contains the reconciled second-pass output from the same selected model after seeing all round-1 outputs.

### `final.md`
Contains orchestrator synthesis with explicit sections for:
- brief summary
- models used
- consensus
- disagreements
- unresolved uncertainty
- escalation points
- final synthesis

## Artifact rules
- artifacts must stay human-readable
- file names should be deterministic and stable enough for debugging
- the run should remain understandable without hidden state
- disagreement should be preserved in artifacts, not flattened away
- failed runs should still preserve whatever artifacts were successfully written

## MVP simplicity rule
Do not over-schema the artifacts in v1.

The MVP artifact shape should prioritize:
- clarity
- debuggability
- truthful traceability
- easy future explanation in the README

## Expansion note
If later validation proves useful, structured records can expand — but MVP should start with the smallest artifact shape that honestly supports the workflow.
