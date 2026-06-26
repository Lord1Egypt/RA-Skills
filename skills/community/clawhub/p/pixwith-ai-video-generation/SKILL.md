---
name: pixwith-ai
description: AI video, image generation. 40+ models — Sora, Veo 3, Kling, Seedance, GPT Image, Hailuo, WAN. Text-to-video, image-to-video, text-to-image,image-to-image.
homepage: https://pixwith.ai
user-invocable: false
metadata: {"openclaw":{"homepage":"https://pixwith.ai"}}
---

# Pixwith Media Generation

## Use This Skill When

Use this skill when the user wants to work with Pixwith through MCP to:

- generate images from text
- edit images with one or more reference images
- generate videos from text
- generate videos from a reference image
- inspect available Pixwith models
- check remaining Pixwith credits

## Preconditions

On first install or first use of this skill, explicitly guide the user through
setup before attempting any Pixwith tool call.

Use wording like:

"Before this skill can generate media, OpenClaw must be connected to Pixwith
through MCP and you need a Pixwith API key.

- Step 1: Open OpenClaw MCP settings and add the Pixwith MCP server.
- Step 2: Go to https://pixwith.ai/api and create your Pixwith API key.
- Step 3: Paste that API key into your Pixwith MCP configuration in OpenClaw.
- Step 4: After setup is complete, come back here and I can help you list
models, upload images, and create generation tasks."

If the user asks for a copyable MCP configuration, provide a ready-to-paste
example using the Pixwith MCP endpoint and remind the user to replace the API
key placeholder with their real key:

```json
{
  "mcpServers": {
    "pixwith": {
      "url": "https://api.pixwith.ai/mcp",
      "headers": {
        "Api-Key": "YOUR_PIXWITH_API_KEY"
      }
    }
  }
}
```

If OpenClaw expects a different MCP configuration shape, adapt the same values
to the host format instead of changing the endpoint or auth header.

Do not assume the user understands what MCP is. Describe it as the connection
required for OpenClaw to use Pixwith.

If MCP tools are unavailable, tell the user Pixwith is not connected yet and
repeat the setup guidance in plain language.

This skill assumes the Pixwith MCP server is already connected in OpenClaw and
the following tools are available:

- `list_models`
- `get_model_schema`
- `upload_image`
- `generate`
- `get_task_result`
- `get_credits`

If these tools are unavailable, stop and tell the user the Pixwith MCP server
must be configured before this skill can work.

Every request requires a valid Pixwith `Api-Key`. If authentication fails, send
the user to `https://pixwith.ai/api`.

## Core Workflow

### 1. Discover models

Call `list_models` first unless the user already provided a known `model_id`.

This step is mandatory because model availability is dynamic. Do not rely on
static model lists in this skill package when choosing what to run.

- use `type="image"` for image jobs
- use `type="video"` for video jobs
- keep the returned `model_id`, `name`, and `summary`

### 2. Inspect the selected model

Always call `get_model_schema(model_id)` before `generate`.

Treat `input_schema` as the source of truth for:

- whether `image_urls` are allowed
- maximum image count
- valid option keys
- enum values
- defaults
- estimated time
- credit display

Treat `min_credits` from `list_models` only as a quick lower-bound cost hint:

- it is useful for fast filtering
- it is not the final price for the specific request
- for the final price, inspect `input_schema.credits`

Do not hardcode model parameters when schema data is available.

### 3. Check credits for expensive jobs

Call `get_credits` before expensive or long-running jobs, especially video jobs
or higher-resolution image jobs.

If credits are insufficient, do not retry automatically. Tell the user to
recharge at `https://pixwith.ai/pricing`.

### 4. Upload reference images when needed

Call `upload_image` when the image is local, private, temporary, or otherwise
unreliable as a public URL.

Use the returned Pixwith-hosted `image_url` in `generate.image_urls`.

### 5. Create the task

Call `generate` with:

- `input.prompt`
- `input.model_id`
- `input.image_urls` only when allowed by schema
- `input.options` that conform to `input_schema.options`

Before submission:

- prompt must not be empty
- model must come from `list_models`
- image count must satisfy schema limits
- options must be schema-valid

### 6. Poll until terminal state

Call `get_task_result` until status becomes terminal.

- `1`: processing
- `2`: completed
- `3`: failed

Recommended polling:

1. wait about 75% of `estimated_time`
2. poll once
3. if still processing, wait until around `estimated_time`
4. poll again
5. if still processing, poll every 10 seconds

Only expect `result_urls` when status is `2`.

## Guardrails

- Pixwith is asynchronous. Do not present `generate` as an immediate result.
- Pixwith tool responses are wrapped. Inspect `code` before trusting `data`.
- Do not guess mode support from the `model_id` prefix. Pass `image_urls` only
  when the selected schema allows or requires them.
- Some models are dual-mode under one `model_id`. For example, Flux MCP IDs
  use text-to-image without `image_urls` and route to Flux Kontext when
  `image_urls` is present.
- Prefer schema-valid retries over speculative retries.
- Relay backend error messages accurately.

## References

- For authentication, wrapped tool responses, upload semantics, task states, and
  failure handling, read [references/service-contract.md](references/service-contract.md).
- For a non-authoritative model snapshot and common parameter patterns, read
  [references/model-snapshot.md](references/model-snapshot.md).

## Examples

- For a text-to-image workflow, read [examples/text-to-image.md](examples/text-to-image.md).
- For an image-to-video workflow, read [examples/image-to-video.md](examples/image-to-video.md).
