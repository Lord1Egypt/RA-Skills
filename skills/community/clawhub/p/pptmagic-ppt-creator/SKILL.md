---
name: pptmagic-ppt-creator
description: Use Banana Slides / pptmagic-compatible project APIs to create, continue, and export presentation decks from an idea, outline, or page-by-page description. Trigger when users ask to make a PPT with pptmagic, Banana Slides, or a compatible deployed service.
metadata: {"openclaw":{"homepage":"https://openclaw-nopass.pptmagic.tech/","emoji":"🪄"}}
---

# PPTMagic PPT Creator

Use the existing PPT project workflow exposed by a Banana Slides / pptmagic-compatible deployment. Prefer the service API over directly calling model providers.

## Use this skill when

- The user asks to make a PPT with `pptmagic`, Banana Slides, or a compatible deployed service.
- The user provides a topic, outline, or detailed per-page description and wants a generated deck.
- The user wants to continue a partially generated project, regenerate images, or export `pptx` / `pdf` / editable `pptx`.

If the user only wants help writing slide copy or structure, you do not need to call the API.

## Configuration and privacy

Use this fixed service base URL:

- `https://openclaw-nopass.pptmagic.tech/`

This skill sends presentation prompts, outlines, page descriptions, and any uploaded template assets to that external deployment in order to generate PPT projects.
Do not use the default public endpoint for sensitive, regulated, or confidential content unless you trust the operator and data handling policy.
If the source material may contain sensitive details, first ask the user whether to redact, summarize, or generalize the content before sending it to the public endpoint.

Optional controlled access:

- `PPTMAGIC_ACCESS_CODE`

If the deployment operator provides an access code, use it as a scoped service credential for controlled access. If no code is provided, the skill can still use the public no-password endpoint when available.

Default API headers:

- `Content-Type: application/json`

Only add `X-Access-Code` when `PPTMAGIC_ACCESS_CODE` is explicitly available. Let the deployment manage any internal device identification automatically.

## Workflow

1. Choose entry mode:
   - Topic only -> create `idea` project
   - Outline available -> create `outline` project
   - Detailed per-page descriptions -> create `descriptions` project
2. Create the project.
3. Upload a template image if the user supplied one.
4. For `idea` / `outline` projects, generate outline.
5. Generate descriptions.
6. Generate images.
7. Poll async tasks until complete.
8. Read final project state.
9. Export the requested format.

Use `references/api-workflow.md` for request/response details.
Use `references/curl-examples.md` for concrete examples.

## Execution rules

- Do not add undocumented auth headers to requests.
- Use `X-Access-Code` only when the operator explicitly provided `PPTMAGIC_ACCESS_CODE`.
- If a step fails, inspect current project state before recreating work.
- If only some pages failed image generation, retry only those pages.
- Before export, confirm the project has the expected pages and generated assets.

## Output to the user

Always report:

- `project_id`
- current completion state
- number of pages generated
- export URL or download URL
- failure stage and next step if something breaks

If export returns JSON with a real file URL, send the real URL to the user instead of downloading the JSON response as if it were a `.pptx` file.
