# OpenClaw Gateway Protocol (Knods)

## Setup

1. Open Iris panel in Knods and click the gear icon.
2. Click `Add Connection`, set name/icon.
3. Copy `Gateway Token` and `Polling URL`.

## Polling Loop

Implement two HTTP calls in a loop.

### 1) Poll for messages

```http
GET {knods_url}/api/agent-gateway/{connectionId}/updates?token={gateway_token}
```

Response:

```json
{
  "messages": [
    {
      "messageId": "uuid",
      "message": "User message (first message includes node catalog context)",
      "history": [
        { "role": "user", "content": "..." },
        { "role": "assistant", "content": "..." }
      ]
    }
  ]
}
```

- Empty `messages` array means no work.
- Poll every 1-2 seconds.
- The first message in a conversation includes prepended context with the full node catalog and action rules. **Always prefer this context over any default catalog.**

### 2) Send streamed response

```http
POST {knods_url}/api/agent-gateway/{connectionId}/respond?token={gateway_token}
Content-Type: application/json
```

Send one or more chunk payloads:

```json
{ "messageId": "uuid", "delta": "Hello " }
{ "messageId": "uuid", "delta": "world!" }
```

Then completion payload:

```json
{ "messageId": "uuid", "done": true }
```

## Canvas Actions in Assistant Text

Knods parses action blocks embedded in assistant text:

### Single node

```text
[KNODS_ACTION]{"action":"addNode","nodeType":"FluxImage"}[/KNODS_ACTION]
```

### Multi-node flow

```text
[KNODS_ACTION]{"action":"addFlow","nodes":[{"id":"n1","nodeType":"FluxImage"},{"id":"n2","nodeType":"Output"}],"edges":[{"source":"n1","target":"n2"}]}[/KNODS_ACTION]
```

Rules:

- Use `"nodeType"` (not `"type"`) in node objects.
- Do NOT include `position` or `data` fields — Knods handles layout automatically.
- Include action blocks only when mutating canvas.
- Keep JSON valid and compact.
- End each flow with `Output`.
- Ensure every edge references an existing node id.
- Use EXACT PascalCase names from the catalog. Unknown node types are silently filtered out.

## Node Catalog (Default)

**Every generator node has a built-in prompt textarea.** Do NOT prepend a DocumentPanel to a single generator.

When the first message includes a node catalog context, **always use that list** over these defaults.

### Text Generators (output: text)
| Node Type | Provider | Accepts Input | Notes |
|-----------|----------|---------------|-------|
| `ChatGPT` | OpenAI | text + image | Best all-rounder |
| `Claude` | Anthropic | text + image | Great for reasoning and creative writing |

### Image Generators (output: image)
| Node Type | Provider | Accepts Input | Notes |
|-----------|----------|---------------|-------|
| `GPTImage` | OpenAI | text + image | Best at complex instructions, text rendering |
| `FluxImage` | Black Forest Labs | text + image | Industry-leading quality, fast |
| `ImagePrompt` | Google Gemini | text + image | Photorealistic, concept art |
| `ZImageTurbo` | — | text + image | Lightning-fast (<2s), rapid prototyping |
| `QwenImage` | Alibaba | text + image | Anime, illustrations, Asian aesthetics |
| `Seedream` | ByteDance | text + image | Dreamy/surreal, text rendering |
| `GrokImage` | xAI | text + image | Text-to-image and image editing |

### Video Generators (output: video)
All support text-to-video. Connect an ImagePanel for image-to-video.
| Node Type | Provider | Accepts Input | Notes |
|-----------|----------|---------------|-------|
| `Veo3FalAI` | Google | text + image | Cinematic, up to 8s, native audio. Best quality |
| `Sora2Video` | OpenAI | text + image | Realistic motion/physics, up to 12s |
| `Kling26Video` | Kling | text + image | Cinematic with audio, up to 10s |
| `KlingO3Video` | Kling | text + image | Latest gen, Standard/Pro quality, up to 10s |
| `Wan26Video` | Wan | text + image | Multi-shot, 720p/1080p, up to 15s |
| `LTXVideo` | LTX | text + image | High-fidelity cinematic, synced audio |
| `GrokVideo` | xAI | text + image | Video with native audio |

### Special Video Node
| Node Type | Accepts Input | Notes |
|-----------|---------------|-------|
| `WanAnimateVideo` | **video + image** | Character animation. Requires VIDEO (motion source) + IMAGE (character). No text prompt. Only for animating a character using motion from another video. |

### Input/Container Nodes
| Node Type | Output | Notes |
|-----------|--------|-------|
| `ImagePanel` | image | Upload/paste an image. Use for reference images or video starting frames |
| `DocumentPanel` | text | Shared text prompt. Only use when one prompt feeds multiple generators |
| `Output` | — | Displays results (text/image/video). Required at end of every flow |

## Flow Design Rules

1. Every generator has a built-in prompt textarea — never prepend DocumentPanel to a single generator.
2. DocumentPanel is only for sharing one prompt across multiple generators.
3. ImagePanel provides reference images or starting frames for image-to-video.
4. Always end flows with Output.
5. Never connect two generators directly — route through Output.
6. Flows go left to right: inputs → generators → Output.
7. WanAnimateVideo requires video + image input. Only for character animation from video motion.

## Flow Examples

```
# Single image (most common)
FluxImage → Output

# Image from reference photo
ImagePanel → GPTImage → Output

# Shared prompt → two generators
DocumentPanel → FluxImage → Output
DocumentPanel → GPTImage → Output

# Text-to-video
Veo3FalAI → Output

# Image-to-video
ImagePanel → Veo3FalAI → Output

# Character animation (WanAnimateVideo needs video + image)
ImagePanel → WanAnimateVideo → Output
[video source] → WanAnimateVideo

# Text generation
ChatGPT → Output
```

## Timeouts

- Unclaimed messages time out after about 2 minutes.
- Keep first response chunk fast.

## Authentication

- Use `gateway_token` query parameter (`token=...`) for gateway endpoints.
- Token format: `gw_` prefix, fixed-length token string.
- Regeneration invalidates previous token.

## Environment Configuration Patterns

Support both deployment patterns:

1. Full polling URL in env:
- `KNODS_BASE_URL=https://.../api/agent-gateway/<connectionId>/updates?token=<gateway_token>`

2. Base connection URL + separate token:
- `KNODS_BASE_URL=https://.../api/agent-gateway/<connectionId>`
- `KNODS_GATEWAY_TOKEN=<gateway_token>`

In both cases, use the same connection root for `/respond`.

## Restart Requirement After Env Changes

Bridge processes usually read env only at startup. After changing URL/token values, restart the bridge.

Example (systemd user service):

```bash
systemctl --user restart knods-iris-bridge.service
systemctl --user status knods-iris-bridge.service
```
