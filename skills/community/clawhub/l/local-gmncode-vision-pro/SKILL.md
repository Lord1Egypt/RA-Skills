---
name: local-gmncode-vision-pro
description: Advanced local vision infrastructure for agents when built-in image tools are unavailable or unreliable. Use for batch image analysis, structured JSON output, screenshot/UI understanding, character/style classification, retryable workflows, and resilient image-processing pipelines backed by GMNCODE. Trigger when a user wants a paid/professional-grade version of local-gmncode-vision, production-ready visual automation, or reusable vision infrastructure for teams and agent systems.
---

# local-gmncode-vision-pro

Use this skill when basic single-image fallback is not enough and the task needs production-grade image understanding.

## Core scripts

- Batch processing:
  `/home/ubuntu/.openclaw/workspace/skills/local-gmncode-vision-pro/scripts/vision_batch.py`
- Structured JSON output:
  `/home/ubuntu/.openclaw/workspace/skills/local-gmncode-vision-pro/scripts/vision_json.py`

## Workflow

1. Prefer the built-in `image` tool if it is healthy and available.
2. If `image` fails or needs more control, use the Pro scripts.
3. For multi-image work, use `vision_batch.py`.
4. For agent/tool pipelines, use `vision_json.py` to get machine-readable output.
5. If results are uncertain, say so explicitly and return best-effort ranked hypotheses.

## Dependencies

- Environment variable: `GMNCODE_API_KEY`
- Model route: `gpt-5.4`

## Read when needed

Read this file for packaging, pricing, and promotion:
`/home/ubuntu/.openclaw/workspace/skills/local-gmncode-vision-pro/references-go-to-market.md`

## Output principles

- Be explicit about uncertainty.
- Separate confirmed observations from inference.
- Prefer structured output for automation.
- Do not overclaim exact character identity when only style-level evidence exists.
