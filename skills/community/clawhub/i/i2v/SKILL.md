---
name: "i2v"
description: Placeholder skill for image-to-video workflows on skills.video. Use when the user is asking about i2v generation and the concrete API contract has not been implemented yet.
---

# i2v

## Overview
Use this as a placeholder skill for image-to-video generation on `skills.video`.
This file is intentionally incomplete and should not be treated as a production workflow.

## Current status
- No verified i2v OpenAPI contract has been wired into this skill yet.
- No default endpoint, payload template, or helper command is defined yet.
- The skill should surface this limitation clearly instead of guessing request fields.

## Temporary behavior
When this skill is invoked before implementation is completed:

1. Tell the user that `i2v` is currently a placeholder.
2. Check whether a model-specific `openapi.json` or docs page exists for the requested provider/model.
3. Avoid inventing undocumented image input fields or upload semantics.
4. Ask for the exact model or endpoint only if it is necessary to continue.
5. Once the API contract is confirmed, promote this placeholder into a real workflow similar to `video-generation`.

## Implementation checklist
- Confirm which providers/models support i2v on `skills.video`
- Identify the create endpoint and terminal status flow
- Document image input format such as URL, file upload, or asset ID
- Document supported motion, duration, and aspect-ratio parameters
- Add request-template extraction steps from OpenAPI
- Add execution examples and fallback polling behavior if applicable
- Add runtime error handling guidance

## Related skills
- `video-generation`: generic video generation flow
- `i2i`: image-to-image placeholder flow
- `v2v`: video-to-video placeholder flow
