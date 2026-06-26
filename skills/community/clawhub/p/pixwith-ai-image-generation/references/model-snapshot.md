# Current Model Snapshot

This file is a code-derived snapshot from the Pixwith MCP backend. It is useful
for planning and orientation, but `list_models()` remains authoritative.

Maintenance note:

- if new models are added but the MCP workflow stays the same, this file is the
  primary place to refresh static documentation
- `SKILL.md` usually does not need changes unless tools, response shapes,
  authentication, upload behavior, or task semantics change
- examples only need updates when a new model introduces a materially new usage
  pattern worth demonstrating

## Enabled Models

### Image

- `0-1`: Flux Dev
- `0-2`: Flux Pro
- `0-3`: Flux Pro Ultra
- `0-4`: ChatGPT Image
- `0-5`: Imagen 4
- `0-6`: Ideogram V3 Turbo
- `0-7`: MidJourney Fast
- `0-8`: MidJourney Relax
- `0-9`: MidJourney Turbo
- `0-10`: Nano Banana
- `0-19`: Grok Image
- `0-23`: Nano Banana Pro
- `0-24`: Qwen Image
- `0-28`: Flux 2 Dev
- `0-29`: Flux 2 Pro
- `0-30`: Seedream V4
- `0-31`: Z-Image
- `0-32`: Seedream 4.5
- `0-34`: Kling O1 Image
- `0-37`: ChatGPT Image 1.5
- `0-41`: Nano Banana 2

### Video

- `2-1`: Kling 2.5
- `2-3`: Hailuo 02
- `2-4`: Luma Ray 2
- `2-8`: WAN 2.2 Lite
- `2-9`: WAN 2.2 Pro
- `2-10`: WAN 2.2 Fast
- `2-11`: Veo 3.1 Fast
- `2-12`: Veo 3.1 Pro
- `2-13`: Sora 2
- `2-14`: WAN 2.5 Fast
- `2-15`: WAN 2.5
- `2-16`: Hailuo 2.3 Standard
- `2-17`: Hailuo 2.3 Pro
- `2-18`: Sora 2 Pro
- `2-19`: Grok Video
- `2-20`: Seedance 1.0 Lite
- `2-21`: Seedance 1.0 Pro
- `2-22`: Seedance 1.0 Pro Fast
- `2-25`: Runway Gen-4 Turbo
- `2-26`: Pika 2.2
- `2-27`: Pixverse V5
- `2-33`: Kling 2.6
- `2-35`: Kling O1
- `2-36`: WAN 2.6
- `2-38`: Seedance 1.5 Pro
- `2-39`: Kling 3.0
- `2-40`: Kling 3.0 Pro
- `2-42`: WAN 2.6 Flash

## Common Parameter Patterns

These patterns are common across the currently enabled models. Verify them with
`get_model_schema(model_id)` before submitting any request.

- image models may support optional reference-image editing mode
- video models may support pure text-to-video or image-to-video mode
- `aspect_ratio`, `resolution`, `duration`, and `prompt_optimization` are common option families
- video credit cost and `estimated_time` can depend on both resolution and duration
- image models differ substantially in max input image count and resolution options
- `min_credits` from `list_models()` is only a quick lower-bound cost hint
- `input_schema` is the exact schema source for prompt, images, options, and price tables

## Agent Guidance

- do not guess support for `image_urls`; read `input_schema`
- do not guess allowed enum values; read the schema
- do not assume a model remains enabled just because it appears in this file
- prefer `get_credits` before higher-cost video jobs
