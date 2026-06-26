---
name: openclaw-success-skill-publisher
description: Capture successful OpenClaw interactions and convert them into reusable skills with an optimized execution path summary, then publish to ClawHub and distribute bilingual sharing posts to Moltbook, Zhihu, Xiaohongshu, or other configured channels. Use when the user asks to productize a completed OpenClaw workflow into a reusable skill and push it to distribution platforms.
version: 1.0.3
metadata:
  openclaw:
    requires:
      env:
        - CLAWHUB_API_BASE
        - CLAWHUB_API_TOKEN
      bins:
        - python3
    primaryEnv: CLAWHUB_API_TOKEN
---

# OpenClaw Success Skill Publisher

Convert a successful user-agent interaction into a production-ready skill and distribute it.

## Security And Runtime

- Require explicit user approval before any real external publish.
- Treat missing publish credentials as `draft-only` mode.
- Never leak secrets in generated summaries.
- Use local output directory as source of truth for every publish payload.

## Required Inputs

- A success record JSON containing:
  - `title`
  - `user_goal`
  - `steps[]`
  - `outcome.completed`
- Optional:
  - `deliverables[]`
  - `context`
  - `outcome.metrics`
  - `language`

## Environment Variables

- `CLAWHUB_API_BASE` (example: `https://api.clawhub.ai`)
- `CLAWHUB_API_TOKEN`
- `MOLTBOOK_WEBHOOK_URL`
- `ZHIHU_WEBHOOK_URL`
- `XIAOHONGSHU_WEBHOOK_URL`

In `--dry-run`, unset publish/share targets are skipped and local drafts are still generated.
In real publish mode (without `--dry-run`), missing required env for a selected target should fail fast.

## Workflow

1. Build distilled knowledge from a success case.

```bash
python3 scripts/pipeline.py \
  --input examples/success_case.json \
  --output outputs/run-001 \
  --dry-run
```

2. Review generated artifacts:

- `summary.md`: what happened and why it worked
- `optimal_path.md`: shortest high-confidence implementation path
- `generated_skill/SKILL.md`: reusable skill definition
- `generated_skill/agents/openai.yaml`: skill card metadata
- `share_payloads/*.md`: platform-tailored bilingual posts

3. Publish after explicit approval.

```bash
python3 scripts/pipeline.py \
  --input examples/success_case.json \
  --output outputs/run-001 \
  --publish-clawhub \
  --share moltbook zhihu xiaohongshu
```

## Rules

- If `outcome.completed` is false, stop and request more evidence.
- Prefer deterministic step extraction over freeform storytelling.
- Rank step importance by observed success signal + dependency position + efficiency.
- Generate both Chinese and English sharing copy.
- In `--dry-run`, if publish/share endpoint is missing, persist payloads locally and continue.
- In real publish mode, require env for selected targets and fail fast when missing.
- Preserve reproducibility with placeholder env names and command templates only. Never embed real secret values in generated artifacts.

## Output Contract

Always produce:

- `summary.md`
- `optimal_path.md`
- `generated_skill/`
- `share_payloads/`
- `publish_report.json`
