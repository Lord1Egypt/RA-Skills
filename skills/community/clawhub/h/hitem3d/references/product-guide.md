# Hitem3D Product Guide

## Positioning

Hitem3D is a production-oriented image-to-3D skill for OpenClaw. It turns chat-driven requests into downloadable 3D assets without forcing the user into a browser workflow.

Core promise:
- images in
- 3D assets out
- cost-aware defaults
- unattended waiting/downloading
- support for single image, portrait, multi-view, and batch workflows

## What this skill should feel like

The user should be able to say things like:
- 把这张椅子图变成 3D
- 用 STL 出一个可打印版本
- 这组前后左右图做一个更准的模型
- 把这个文件夹里的 30 张图全转成 GLB
- 查下我还剩多少积分

The agent should translate that into the right model, output format, quality tier, and execution flow.

## Interaction design goals

1. Default to outcome, not raw API calls
2. Use the safest high-quality default for normal requests
3. Ask before expensive or risky runs
4. Distinguish multi-view from batch every time
5. Return paths, cost estimate, and result summary instead of dumping JSON

## Supported user intents

### General object generation
Single image to textured GLB.

### Portrait generation
Bust/head/face-oriented generation with portrait models.

### 3D printing
Prefer STL + geometry-first behavior.

### AR delivery
Prefer USDZ for Apple AR flows.

### Multi-view reconstruction
2-4 images of the same object with front/back/left/right mapping.

### Batch production
Many unrelated images, one task per image.

### Balance and cost awareness
Let the user inspect credits before running larger jobs.

## Safety and operational guardrails

### Confirm before expensive jobs
Ask for confirmation when:
- batch size > 5 images
- estimated total cost > 100 credits
- destination/output intent is ambiguous and likely expensive to redo
- the user asks for multiple variants, formats, or quality tiers in one pass

### Reject bad combos early
Examples:
- request_type=2 with hitem3dv2.0
- invalid face count
- invalid multi-view bitmap
- missing image files
- multi-view set that does not include the required front view

### Do not pretend success
If the API has not returned a valid task ID or result URL, say so clearly.

### Do not leak secrets
Never print AK/SK values back to the user.

### Do not overclaim validation
Without real API-key runs, this is workflow-validated and safety-audited, not fully production-proven.

## Good response shape

For finished jobs, return:
- what was generated
- where it was saved
- which model/options were used
- estimated credit cost
- any caveats if the input was weak or the mode was a compromise

## Positioning vs weak skills

Weak 3D skills stop at “here is the endpoint.”
This skill should behave like an operator:
- choose defaults
- protect against common errors
- finish the workflow
- summarize useful output

## Suggested marketing angle

One sentence:
Turn images into production-grade 3D assets from chat, with sane defaults, multi-view support, batch automation, and cost-aware execution.

## Ideal maturity path

v1: API wrapper
v2: outcome-driven skill
v3: preflight checks + smart intent routing + better batch orchestration
v4: real production handoff with manifests/previews/post-processing
