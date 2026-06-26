---
name: knods
description: Build and modify Knods visual AI workflows using either the OpenClaw Gateway polling protocol or the Knods headless flows API. Use for Knods polling payloads with fields like messageId/message/history, or for direct flow discovery/execution tasks like listing flows, reading input schemas, starting runs, polling status, cancelling runs, and retrieving outputs programmatically.
metadata:
  openclaw:
    emoji: "🔌"
    homepage: "https://github.com/alesys/openclaw-skill-knods"
    os: ["linux"]
    requires:
      bins: ["python3", "bash", "openclaw", "systemctl"]
      env: ["KNODS_BASE_URL"]
---

# Knods

## Overview

Handle two Knods modes:

1. Interactive canvas chat via the polling gateway
2. Headless flow execution via the REST API

Use the polling bridge for Knods Iris/chat payloads. Use the headless API when the task is to discover a flow, inspect inputs, run it, wait, cancel, or fetch outputs programmatically.

## Mode Selection

- Use **polling gateway mode** when input arrives as a Knods chat envelope with `messageId`, `message`, and `history`, and the response must stream back with optional `[KNODS_ACTION]...[/KNODS_ACTION]`.
- Use **headless API mode** when the user wants to:
  - list flows
  - search flows by name/description
  - inspect a flow's input schema
  - start a run
  - poll until completion
  - cancel a run
  - retrieve outputs programmatically

## Workflow

### A. Polling Gateway Flow

1. Parse incoming payload fields.
- Treat `message` as the primary request.
- Use `history` for continuity.
- On first turn in a conversation, expect prepended context in `message` describing node types and action rules. **Always prefer the node catalog from this context over the defaults below.**
- Use `messageId` to map all response chunks to the correct message.

2. Choose whether to emit a canvas action block.
- Use `addNode` for single-node additions.
- Use `addFlow` for multi-node workflows or any request requiring edges.
- If the user only asks a question, respond with normal text and no action block.

3. Build strict action JSON.
- Wrap each action exactly as:
  - `[KNODS_ACTION]{"action":"addNode","nodeType":"FluxImage"}[/KNODS_ACTION]`
  - `[KNODS_ACTION]{"action":"addFlow","nodes":[...],"edges":[...]}[/KNODS_ACTION]`
- Use `"nodeType"` (not `"type"`) in node objects. Do NOT include `position` or `data` fields — Knods handles layout automatically.
- For `addFlow`, ensure every edge `source` and `target` references an existing node id.
- Always end flows with an `Output` node.
- Never connect two generator nodes directly; route through `Output`.
- Use stable node IDs (for example `n1`, `n2`, `n3`) so follow-up edits are easy.
- Avoid unknown keys in action JSON.

4. Stream response back to Knods.
- Send assistant text as delta chunks to `/respond` for the same `messageId`.
- Send `{"messageId":"...","done":true}` when complete.
- Keep first chunk quick to avoid timeout perception.

### B. Headless API Flow

1. Discover candidate flows.
- Run:
  - `python3 {baseDir}/scripts/knods_headless.py list`
  - or `python3 {baseDir}/scripts/knods_headless.py resolve --query "<text>"`

2. Inspect the selected flow.
- Run:
  - `python3 {baseDir}/scripts/knods_headless.py get --flow-id "<flowId>"`
- Read `inputs` and preserve every `nodeId` exactly.

3. Start a run.
- Build `inputs` as JSON array with `nodeId`, `content`, and `type`.
- Run:
  - `python3 {baseDir}/scripts/knods_headless.py run --flow-id "<flowId>" --inputs-json '[...]'`

4. Poll until terminal state.
- Prefer:
  - `python3 {baseDir}/scripts/knods_headless.py wait --run-id "<runId>"`
- Or use:
  - `python3 {baseDir}/scripts/knods_headless.py run-wait --flow-id "<flowId>" --inputs-json '[...]'`

5. Handle result.
- On `completed`, read `outputs`
- On `failed`, surface `error.message` and `error.nodeId` if present
- On timeout, optionally cancel the run

## Output Rules

- Return normal assistant text; do not wrap the full reply in a custom envelope.
- Include `[KNODS_ACTION]...[/KNODS_ACTION]` inline only when a canvas mutation is intended.
- Do not mention internal polling URLs/tokens in user-facing text.
- Keep action JSON valid and compact.

## Node Catalog

**IMPORTANT:** Every generator node listed below has a built-in prompt textarea. Do NOT add a DocumentPanel before a single generator — just connect the generator directly to an Output. Only use DocumentPanel when one shared prompt feeds multiple generators in parallel.

When the first message includes a node catalog context, **always use that list** over these defaults. The context catalog is always more up-to-date.

### Text Generators (output: text)
All text generators accept text + image input and have a built-in prompt textarea.
- `ChatGPT` — OpenAI models. Best all-rounder.
- `Claude` — Anthropic models. Great for reasoning and creative writing.

### Image Generators (output: image)
All image generators have a built-in prompt textarea and accept optional image input for image-to-image editing.
- `GPTImage` — OpenAI. Best at following complex instructions and text rendering.
- `FluxImage` — FLUX by Black Forest Labs. Industry-leading quality for portraits and artistic styles. Fast.
- `ImagePrompt` — Google Gemini. Great for photorealistic images and concept art.
- `ZImageTurbo` — Lightning-fast (<2 seconds). Best for rapid prototyping.
- `QwenImage` — Alibaba Qwen. Strong at anime, illustrations, and Asian-inspired aesthetics.
- `Seedream` — ByteDance. Dreamy, surreal compositions. Good at text rendering in images.
- `GrokImage` — xAI. Text-to-image and image editing.

### Video Generators (output: video)
All video generators below have a built-in prompt textarea and support both text-to-video and image-to-video (connect an ImagePanel for image-to-video).
- `Veo3FalAI` — Google Veo 3.1. Cinematic video up to 8s with native audio. Best overall quality.
- `Sora2Video` — OpenAI Sora 2. Realistic motion and physics, up to 12s.
- `Kling26Video` — Kling 2.6 Surreal Engine. Cinematic with audio, up to 10s.
- `KlingO3Video` — Kling 3.0. Latest generation, Standard/Pro quality, up to 10s.
- `Wan26Video` — Wan 2.6. Multi-shot videos, 720p/1080p, up to 15s.
- `LTXVideo` — LTX-2 Pro. High-fidelity cinematic with synchronized audio.
- `GrokVideo` — xAI. Video with native audio.

### Special Video Node
- `WanAnimateVideo` — Character animation. **REQUIRES two inputs**: a VIDEO (motion reference) + an IMAGE (character to animate). Does NOT have a text prompt. Only use when user wants to animate a character image using motion from another video.

### Input/Container Nodes
- `ImagePanel` — Upload or paste an image. Output: image. Use when user wants to provide a reference image or a starting frame for image-to-video.
- `DocumentPanel` — Editable text container. Output: text. Use ONLY when one shared prompt feeds multiple generators in parallel.
- `Output` — Displays generated results (text, image, video). REQUIRED at the end of every flow.

## Flow Design Rules

1. **Every generator has a built-in prompt textarea.** Never prepend a DocumentPanel to a single generator.
2. **Use DocumentPanel only** for one shared prompt feeding multiple generators in parallel.
3. **Use ImagePanel** when user wants to provide a reference image, a starting frame for video, or an image input for WanAnimateVideo.
4. **Always end flows with an Output node.**
5. **Never connect two generators directly.** Route through an Output node if chaining.
6. **Flows go left to right:** inputs → generators → Output.
7. **Use EXACT PascalCase node names** from the catalog. Do NOT invent node names.
8. **WanAnimateVideo** is the only node that requires a video input. Only suggest it when the user specifically wants to animate a character image using motion from a video.
9. Add `initialData` only when user intent clearly implies parameters.
10. Build the smallest flow that satisfies the request.

## Flow Examples

Single image generator (most common):
```
FluxImage → Output
```

Image from reference photo:
```
ImagePanel → GPTImage → Output
```

One prompt feeding two image generators:
```
DocumentPanel → FluxImage → Output
DocumentPanel → GPTImage → Output
```

Text-to-video:
```
Veo3FalAI → Output
```

Image-to-video (animate a still image):
```
ImagePanel → Veo3FalAI → Output
```

Character animation from video motion (WanAnimateVideo needs both video + image):
```
ImagePanel → WanAnimateVideo → Output
[video source] → WanAnimateVideo
```

Text generation:
```
ChatGPT → Output
```

## Gateway Behavior Constraints

- Poll interval target: about 1-2 seconds.
- Message claim timeout: about 2 minutes.
- Always preserve `messageId` across all chunk posts for a turn.
- Gateway auth uses `gw_...` token via query parameter `token`; never require Supabase JWT in this flow.

## Runtime Operations

When running a persistent poller service/process:

- Support either configuration style:
  - `KNODS_BASE_URL` already includes `/updates?token=...`
  - or `KNODS_BASE_URL` points to connection base and token is supplied separately (`KNODS_GATEWAY_TOKEN`)
- Derive `/respond` from the same connection root as `/updates`.
- Log handled `messageId` values and transport errors for debugging.

For headless API operations:

- Prefer `KNODS_API_BASE_URL` + `KNODS_API_KEY`
- `KNODS_API_BASE_URL` should look like `https://<instance>/api/v1`
- `KNODS_API_KEY` must have `knods:read` and `knods:run`
- If the API base URL is omitted, the packaged client can derive it from the same host as `KNODS_BASE_URL`

### Packaged Runtime (required)

This skill ships the runtime bridge and installer:

- `scripts/knods_iris_bridge.py`
- `scripts/knods_headless.py`
- `scripts/install_local.sh`

Install/deploy from the skill folder:

```bash
bash /home/rolf/.openclaw/skills/knods/scripts/install_local.sh
```

The installer deploys:

- `~/.openclaw/scripts/knods_iris_bridge.py`
- `~/.config/systemd/user/knods-iris-bridge.service`

Then runs:

- `systemctl --user daemon-reload`
- `systemctl --user enable --now knods-iris-bridge.service`

### Environment Variables

Set these in `~/.openclaw/.env`:

- Required for polling gateway mode:
  - `KNODS_BASE_URL`
- Required when `KNODS_BASE_URL` does not already include `?token=...`:
  - `KNODS_GATEWAY_TOKEN`
- Required for headless API mode:
  - `KNODS_API_KEY`
- Preferred for headless API mode:
  - `KNODS_API_BASE_URL`
- Optional:
  - `OPENCLAW_AGENT_ID` (default: `iris`)
  - `OPENCLAW_BIN` (default: `openclaw` on `PATH`)

### Service Operations

- Status:
  - `systemctl --user status knods-iris-bridge.service`
- Restart:
  - `systemctl --user restart knods-iris-bridge.service`
- Logs:
  - `journalctl --user -u knods-iris-bridge.service -f`

### Config Change Lifecycle (required)

After changing gateway URL/token env values, restart the running bridge process so it reloads config.

- Generic service form:
  - `systemctl --user restart <knods-bridge-service>`
- Generic process form:
  - stop old process
  - start poller again with updated env

Do not assume env changes are picked up live without restart.

## Reference

- Read `references/protocol.md` for canonical polling endpoints, payload schemas, and action examples.
- Read `references/headless-api.md` for the direct run/list/poll/cancel flow execution API.
