---
name: openclaw-novelai
description: 'NovelAI creative workflows for OpenClaw: fiction context, chapter planning, image prompting, V5/V4.5 generation, img2img, inpainting, Vibe/Director tools, cost-aware execution, same-session billing-profile reuse, bounded transient retries, and secret-safe asset records.'
version: 0.1.3
metadata: {"openclaw":{"os":["win32","linux","darwin"],"requires":{"env":["NOVELAI_TOKEN"],"bins":["python"]},"primaryEnv":"NOVELAI_TOKEN","homepage":"https://github.com/techotaku39/openclaw-novelai"}}
---

# OpenClaw NovelAI

Use this skill when the user wants a NovelAI-assisted story workflow in OpenClaw: long-form writing, chapter context, character consistency, advanced image generation, image editing, or asset tracking. It may reuse a verified billing profile in the same conversation when billing-affecting parameters remain unchanged.

This skill is an orchestration guide. It does not contain or request a NovelAI credential. It assumes that the operator has configured a NovelAI text provider and, for image operations, an MCP server exposing the NovelAI Image MCP tools.

The reference deployment pins the image MCP server to `novelai-image-mcp==0.4.0`. Do not silently upgrade it during a user operation; check the compatibility notes and run the smoke suite before changing the pin.

The included 2026-09-05 API test confirmed that Xialong completion and GLM-4.6 streaming work with the configured text endpoint, while GLM-4.6 non-streaming returned an empty `text` field despite HTTP 200. Prefer streaming for GLM-4.6 and report the limitation if the host forces `stream:false`. The same test found the advertised dedicated `upscale_image` route returning 404 on both current NovelAI image hosts; do not claim dedicated upscaling succeeded unless the active server returns an image.

## Security rules

- Never ask the user to paste a NovelAI token, password, cookie, or bearer header into chat.
- Never place a credential in a prompt, command argument, URL, generated file, log, or generation metadata.
- Treat every third-party MCP server, CLI, package, and skill as untrusted until the operator has reviewed and approved it.
- Do not auto-install packages. Explain the prerequisite and wait for operator approval.
- Before a batch or expensive operation, show the planned model, size, steps, sample count, and estimated Anlas when the estimate tool is available.
- Never claim that a generation or edit succeeded until the tool returns an output file or image content.

## Capability discovery

Before using NovelAI image tools, inspect the configured MCP catalog. Tool names may be namespaced by the configured server name.

Expected NovelAI Image MCP tools include:

- `generate_image`
- `image_to_image`
- `inpaint`
- `upscale_image`
- `director_tool`
- `annotate_image`
- `suggest_tags`
- `encode_vibe`
- `get_subscription`
- `get_user_data`
- `estimate_anlas_cost`

If a requested tool is not present, report that it is unavailable. Do not substitute a different provider silently.

For OpenClaw code-mode agents, inspect the active MCP catalog and the tool signatures exposed by the current host before calling a tool. Do not assume a tool name, namespace, or parameter shape from this document. The reference server currently advertises V3/V4/V4.5/V5 generation, but Vibe support is limited to V4/V4.5 in its published tool summary. Verify the server's current tool schema before using a model-specific feature.

## Text workflow

NovelAI text generation should be selected as the active OpenClaw model provider, not simulated by an image tool. Use the provider/model selected by the operator, such as `novelai/xialong-v1` or another model actually exposed by the current provider. For `glm-4-6`, keep streaming enabled; a non-streaming HTTP 200 is not sufficient evidence of usable text because the current endpoint can return an empty `choices[0].text`.

Use the local project helper to assemble bounded context before asking the text model to write:

```text
python {baseDir}/scripts/project_state.py init --root <workspace>/novelai-projects --name <project>
python {baseDir}/scripts/project_state.py compose --project-dir <project-dir> --task <task> --max-chars 30000
```

The project layout is:

```text
<project>/
  canon.md
  memory.md
  lorebook.md
  style.md
  chapters/
  images/
  metadata/generations/
```

Recommended text actions:

- `outline`: produce or revise a chapter outline.
- `continue`: continue from the latest chapter or supplied excerpt.
- `rewrite`: rewrite a bounded excerpt while preserving selected facts.
- `review`: identify continuity, pacing, and character problems without overwriting canon.
- `summarize`: update `memory.md` or `canon.md` only after showing the proposed change.

Do not assume that a NovelAI text model supports ordinary instruction-following behavior. Prefer a clear continuation prompt and include the relevant context files.

## Session-scoped billing profile and retry policy

When a current tool schema provides account or cost information, keep only a redacted billing profile in memory for the current OpenClaw conversation after a successful verification or exact cost estimate. Never store prompts, image bytes, paths, balances, account identifiers, or credentials. Reuse the profile indefinitely in the same conversation when the operation type, model, dimensions, Steps, image count, sampler/scale/noise, base image, mask, reference, Vibe, and Director operation remain unchanged; a prompt change alone may reuse it when the provider does not price prompt text separately.

Invalidate the profile on a new conversation, OpenClaw/MCP restart, any billing-affecting parameter change, tool error, account warning, an ambiguous result that may mean the provider already accepted the request, or an explicit request to recheck cost. Reuse never bypasses a user confirmation requirement, a paid-operation warning, or a provider-specific restriction.

For each user-requested image operation, allow up to 3 sequential retries after the initial attempt, for at most 4 tool calls total. Retry the exact same parameters only for transient `429`, transient `5xx`, connection reset, MCP reconnect, an explicitly incomplete timeout, or a failed response with no output and no billing/account signal. Do not retry `400`, `401`, `402`, explicit charges, account/Usage Limit warnings, or ambiguous cases where the request may already have been accepted. Use brief increasing backoff; never retry in parallel or turn a retry into a batch.

## Image workflow

### Text to image

Use `generate_image` for a new image. Ask for or infer only the parameters needed by the user's request:

- current model ID;
- positive prompt;
- undesired/negative prompt;
- width and height;
- steps, scale, sampler, and seed;
- sample count;
- character prompts and positions when supported;
- reference or Vibe settings when supported by the selected model.

Example user intents:

```text
根据第三章生成 3 个关键场景，固定主角的角色提示词，记录每张图的 seed。
```

```text
使用当前角色参考图，保持脸部和服装一致，生成雨夜街道的 4 个变体。
```

For a V5 request, use a current V5 model ID returned by the tool or current provider configuration. Do not reuse a V4.5-only Vibe workflow for V5.

### Image to image

Use `image_to_image` when the user provides a source image and asks to change its style, clothing, pose, lighting, or background. Preserve the source file and write the result to a new asset path. Explain that lower strength normally keeps more of the source composition.

### Inpainting

Use `inpaint` only when both a source image and a mask are available. Confirm which mask convention the tool advertises before calling it. Save the result separately and keep the original unchanged.

### Vibe and character references

Use `encode_vibe` or the server's reference-image parameters only when the server schema supports them. Store reference paths and strength values in generation metadata, but never store the token.

### Director tools and post-processing

Use `director_tool` for line art, sketch, background removal, declutter, colorize, and emotion changes when the server advertises those operations. Use `upscale_image` for a dedicated 2x/4x upscale only after checking that the active server actually returns an image; the pinned server's legacy endpoint currently returns 404 in the reference test. If the user accepts a regenerated result, explain the difference and use `image_to_image` at a larger supported resolution, or use a local upscaler. Use `annotate_image` only when a ControlNet annotation is specifically requested.

## Batch chapter illustration workflow

When the user asks to illustrate a chapter:

1. Read the chapter and project context with the file tools.
2. Produce a short scene list and ask for confirmation if the requested image count is ambiguous.
3. Generate or refine prompts, optionally using `suggest_tags`.
4. Use `estimate_anlas_cost` if available. For a batch, report total estimated cost before generation.
5. Call the image tool one scene at a time unless the tool explicitly supports safe batching.
6. Save each result with a stable chapter/scene filename.
7. Record model, seed, prompt, negative prompt, dimensions, and tool name:

```text
python {baseDir}/scripts/project_state.py record --project-dir <project-dir> --kind image --model <model> --seed <seed> --prompt <prompt> --asset <asset-path> --metadata-file <safe-json-file>
```

8. Send the generated files through the available messaging/media tool only after verifying that they exist.

## Cost and confirmation policy

The following may consume NovelAI resources depending on the account and model: image generation, image-to-image, inpainting, Vibe encoding, Director tools, and upscaling. A user request to perform the operation is authorization for a single small operation; ask before an ambiguous batch, a high-resolution request, or retries beyond the automatic three-retry budget.

Account and cost tools are informational and do not replace the user's responsibility to check current NovelAI pricing and subscription rules.

## Failure handling

Map failures to an actionable explanation:

- `401`: credential missing, expired, or invalid; do not request the credential in chat.
- `402`: subscription or Anlas limitation; do not retry automatically.
- `400`: model, parameter, image, or mask mismatch; report the rejected field if returned.
- `429`: rate/concurrency limit; retry the exact same request sequentially up to 3 times after the initial attempt with brief backoff; stop afterward.
- `404` from `/ai/upscale`: the dedicated upscaler route is unavailable on the active NovelAI host; do not retry blindly, and offer larger-resolution img2img or local upscaling as a different operation.
- timeout/network error: preserve the original input and retry up to 3 times only when the provider clearly reports that the request was not completed; if it may already have been accepted, treat it as ambiguous and check status before any further retry.
- missing tool: report MCP configuration or tool allowlist issue; do not fall back silently.

After every successful generation, record metadata without secrets. After every failed generation, do not claim that an asset was produced.
