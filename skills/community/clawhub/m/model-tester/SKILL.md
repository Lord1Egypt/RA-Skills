---
name: model-tester
version: 1.0.0
description: "Test agents or models against predefined test cases to validate model routing, performance, and output quality. Use when: (1) verifying a specific agent or model works correctly, (2) debugging model fallback chains, (3) testing model selection behavior, (4) validating extraction/reasoning/classification across different models, or (5) verifying a model actually got used after routing. Supports --agent, --model, --case parameters with structured JSON output."
---

Use `scripts/model_tester.py` to run repeatable test prompts and compare requested vs actual model usage from OpenClaw logs.

## Run

From the skill directory (or pass absolute paths):

```bash
python3 scripts/model_tester.py --agent menial --case extract-emails
python3 scripts/model_tester.py --model openai/gpt-4.1 --case math-reasoning
python3 scripts/model_tester.py --agent chat --model openai/gpt-4.1 --case all --out /tmp/model-test.json
```

## Inputs

- `--agent <name>`: Target agent (chat, menial, coder, etc.)
- `--model <name>`: Requested model alias/name to test
- `--case <id|all>`: Case from `references/test-cases.json` or `all`
- `--timeout <sec>`: Per-case timeout (default `120`)
- `--out <file>`: Optional JSON output file

Require at least one of `--agent` or `--model`.

## What the runner does

1. Load test cases from `references/test-cases.json`.
2. Start `openclaw logs --follow --json` in parallel.
3. Run `openclaw agent --json` with a bounded test prompt (asks agent to use a subagent for the task).
4. Parse response + tailed logs.
5. Emit machine-readable JSON and a short human summary.

## Output format

Top-level JSON:

- `tool`
- `timestamp`
- `agent`
- `requested_model`
- `results[]`

Each result entry returns:

- `test_case`
- `agent`
- `requested_model`
- `actual_model` (parsed from logs when available)
- `status` (`ok`/`error`)
- `result_summary`
- `runtime_seconds`
- `tokens` (when discoverable)
- `errors[]`

## Privacy & Safety

The tester spawns isolated subagent tasks with **predefined test prompts only** — no user data is passed to models. It tails OpenClaw logs to extract:
- which model was actually selected (routing validation)
- token usage statistics
- runtime metrics

Log extraction uses regex patterns to find model/token fields. No personally identifiable information or arbitrary log content is captured — only structured fields related to the test execution.

## Notes

- Model extraction and token extraction are best-effort because log fields may vary by OpenClaw/provider version.
- If `openclaw` config is invalid or gateway is unavailable, the script returns `status=error` with stderr details.
- Edit `references/test-cases.json` to add custom prompts for your benchmark set.
- All test cases are generic; no workspace or user data is baked in.
