# Platform adapters

This skill is provider-neutral. The artistic contract stays unchanged; only the handoff mechanism differs. Do not claim a named platform supports image generation without checking its active model/tool configuration.

## Capability-first adapter

| Environment state | What to do |
| --- | --- |
| Native image generation/editing tool is available | Pass one source photo to the tool as the reference image and use the master prompt. Run one generation job per photo. |
| Agent can call a configured image provider through MCP, API, or a local command | Use the provider's documented image-reference/upload field. Keep the source-to-output mapping explicit in the request. |
| Agent can write prompts but cannot access an image model | Output a separate ready-to-paste prompt for each photo; do not fabricate image outputs. |
| Provider accepts text only | Ask the user to upload/provide the source photo to an image-reference-capable endpoint, or create a text-only interpretation only if they explicitly allow loss of visual fidelity. |

## Host conventions

### Codex

If an image-generation tool is enabled, call it directly with the current photo as the reference. Otherwise give the user the per-image bilingual prompt and identify the missing capability. Save each generated file independently; do not make a preview sheet.

### OpenClaw

Treat image generation as a configured channel/tool capability, not a built-in guarantee. Inspect the active model/tool configuration first. Send each source image and its prompt as a separate tool invocation, then return separate media items in source order.

### Claude Code

Claude Code may be connected to different tools/providers depending on installation. Detect a configured image tool, MCP server, script, or API before use. If none exists, provide the generated prompts and a concrete provider-agnostic handoff, rather than implying native image output.

### Hermes, DeepSeek, Honeycomb, and other agent harnesses

Use the harness's already-authorized image tool or image-capable routed model. Keep the task as a per-reference loop: inspect reference -> compose variables -> call image generator -> visually validate -> emit one result. If routing selects a text-only model, stop at prompt delivery unless the user authorizes/configures an image endpoint.

## Portable pseudocode

```text
for each source_photo in attachments:
    orientation = portrait ? "9:16" : "16:9"
    variables = inspect(source_photo)  # subject, pose, relationship, <=4 colors
    prompt = master_prompt(orientation, variables)
    poster = image_generate(reference=source_photo, prompt=prompt)
    verify(poster, independent=true, source_mapped=true, layout=true, material=true)
    return poster as its own output
```

## Model/tool handoff template

Use this when configuring a generic image endpoint:

```json
{
  "reference_image": "<one source photo>",
  "prompt": "<English or Chinese master prompt with filled variables>",
  "aspect_ratio": "9:16 or 16:9",
  "output_count": 1
}
```

Field names are illustrative. Replace them with the active provider's documented schema; never expose keys, tokens, or credentials in prompts or logs.
