---
name: image-generation-agent
description: "Image Generation Agent: Google Gemini-powered image generation tool (Nano Banana / Gemini 2.5 & 3 Flash Image). Use this to generate images from a text prompt, produce low-cost draft previews, or render high-resolution finals at 0.5K, 1K, 2K, or 4K. Use when an agent needs image generation agent, ai image generation, nano banana image creation, google gemini image api, text to image, generate budget image, prompt, aspect ratio through AgentPMT-hosted remote tool calls."
version: 1.0.1
homepage: https://www.agentpmt.com/marketplace/image-generation-agent
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/image-generation-agent"}}
---
# Image Generation Agent

## Freshness
Last updated: `2026-06-09`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
AI image generator powered by Google Gemini 3 Flash Image and  "Nano Banana". Create photorealistic product photography, marketing creative, social graphics, app icons, concept art, hero images, and brand assets from a single text prompt — or edit an existing image by passing up to four reference photos for style, subject, or scene guidance. Choose your output tier: a low-cost budget draft for ideation, or crisp 0.5K, 1K, 2K, and 4K final renders for print, ads, e-commerce, and presentation use. Supports 14 aspect ratios including 1:1, 16:9, 9:16, 21:9, 4:5, and ultra-wide 8:1 banner formats. Every generated image is auto-saved to AgentPMT File Manager with a 7-day signed download URL, file_id, width, height, MIME type, and size bytes — ready to drop into chat, hand off to another tool, or pull into a workflow. Built for designers, marketers, e-commerce sellers, content creators, and AI agents that need on-demand visuals without leaving the conversation.

## Product Instructions
### AI Image Creator

Create images from prompts, or edit an image by adding reference images. Generated images are saved to File Manager and returned with a signed URL that users can open or download directly, plus `file_id`, MIME type, size, width, and height.

#### Choosing an action

- `generate_budget_image`: Lower-cost drafts, previews, simple assets, or 1024px-class output.
- `generate_image_0_5k`: Small high-efficiency output.
- `generate_image_1k`: Standard final images.
- `generate_image_2k`: Higher-resolution social, presentation, or product assets.
- `generate_image_4k`: Highest-resolution final assets.

#### Inputs

- `prompt` is required for every generation action.
- `aspect_ratio` defaults to `1:1`.
- `reference_images` is optional and accepts up to 4 images.
- Reference image formats: PNG, JPEG, or WebP.
- Reference image sources:
  - `{"source_kind":"file_id","file_id":"<file-id>"}`
  - `{"source_kind":"url","url":"https://example.com/image.png"}`
  - `{"source_kind":"base64","base64_data":"<base64>","mime_type":"image/png"}`
- `filename` is optional. The final extension is inferred from the generated image.
- `expiration_days` defaults to 7 and must be from 1 to 7.
- Generated image bytes are not returned inline. Use the signed URL to open or download the file.

Only use reference images you have the right to use.

#### Aspect ratios

`generate_budget_image` supports:
`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`.

High-resolution actions support:
`1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9`.

#### Examples

Budget text-to-image:

```json
{
  "action": "generate_budget_image",
  "prompt": "A clean blue circle icon on a white background, flat vector style",
  "aspect_ratio": "1:1"
}
```

High-resolution text-to-image:

```json
{
  "action": "generate_image_2k",
  "prompt": "A polished product mockup of a reusable water bottle on a white studio sweep",
  "aspect_ratio": "16:9",
  "filename": "water-bottle-product-mockup"
}
```

Reference-image edit from File Manager:

```json
{
  "action": "generate_image_1k",
  "prompt": "Keep the subject and pose. Replace the background with a bright minimalist studio scene.",
  "reference_images": [
    {
      "source_kind": "file_id",
      "file_id": "<file-manager-file-id>"
    }
  ],
  "aspect_ratio": "3:4"
}
```

#### Output

Successful calls return:

```json
{
  "success": true,
  "action": "generate_image_1k",
  "tier": "1k",
  "model_tier": "standard",
  "aspect_ratio": "1:1",
  "image_size": "1K",
  "reference_image_count": 0,
  "images": [
    {
      "file_id": "...",
      "filename": "...png",
      "signed_url": "https://...",
      "signed_url_expires_in": 604800,
      "content_type": "image/png",
      "size_bytes": 123456,
      "width": 1024,
      "height": 1024
    }
  ],
  "text_parts": [],
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "total_tokens": 0
  }
}
```

## When To Use
- Use this skill for `Image Generation Agent` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: image generation agent, ai image generation, nano banana image creation, google gemini image api, text to image, generate budget image, prompt, aspect ratio.
- Supported action names: `generate_budget_image`, `generate_image_0_5k`, `generate_image_1k`, `generate_image_2k`, `generate_image_4k`.

## Use Cases
- AI image generation
- Nano Banana image creation
- Google Gemini image API
- text-to-image
- image editing with reference photos
- product photography mockups
- hero banner generation
- social media graphics for Instagram and TikTok and LinkedIn
- e-commerce product visuals
- concept art
- app and product icon design
- marketing campaign creative
- ad creative generation
- brand asset production
- style transfer with reference images
- photoshoot replacement

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`) - Use this companion skill to inspect, download, upload, and manage files referenced by this product.

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `5`.
x402 availability: not enabled for this product.

- `generate_budget_image` (action slug: `generate-budget-image`): Create or edit a lower-cost image from a prompt and optional reference images. Use for drafts, previews, and standard 1024px-class outputs. Price: `8` credits. Parameters: `aspect_ratio`, `expiration_days`, `filename`, `prompt`, `reference_images`.
- `generate_image_0_5k` (action slug: `generate-image-0-5k`): Create or edit a high-efficiency 0.5K image from a prompt and optional reference images. Price: `10` credits. Parameters: `aspect_ratio`, `expiration_days`, `filename`, `prompt`, `reference_images`.
- `generate_image_1k` (action slug: `generate-image-1k`): Create or edit a 1K image from a prompt and optional reference images. Price: `15` credits. Parameters: `aspect_ratio`, `expiration_days`, `filename`, `prompt`, `reference_images`.
- `generate_image_2k` (action slug: `generate-image-2k`): Create or edit a 2K image from a prompt and optional reference images. Price: `25` credits. Parameters: `aspect_ratio`, `expiration_days`, `filename`, `prompt`, `reference_images`.
- `generate_image_4k` (action slug: `generate-image-4k`): Create or edit a 4K image from a prompt and optional reference images. Price: `40` credits. Parameters: `aspect_ratio`, `expiration_days`, `filename`, `prompt`, `reference_images`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "image-generation-agent"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "image-generation-agent"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "image-generation-agent"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "image-generation-agent"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "image-generation-agent"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "image-generation-agent"
  }
}
```

## Call This Tool
Product slug: `image-generation-agent`

Marketplace page: https://www.agentpmt.com/marketplace/image-generation-agent

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Image-Generation-Agent",
    "arguments": {
      "action": "generate_budget_image",
      "aspect_ratio": "1:1",
      "expiration_days": 1,
      "filename": "example filename",
      "prompt": "example prompt",
      "reference_images": [
        {
          "base64_data": "example base64 data",
          "file_id": "example file id",
          "mime_type": "image/png",
          "source_kind": "file_id",
          "url": "https://example.com"
        }
      ]
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "image-generation-agent",
  "parameters": {
    "action": "generate_budget_image",
    "aspect_ratio": "1:1",
    "expiration_days": 1,
    "filename": "example filename",
    "prompt": "example prompt",
    "reference_images": [
      {
        "base64_data": "example base64 data",
        "file_id": "example file id",
        "mime_type": "image/png",
        "source_kind": "file_id",
        "url": "https://example.com"
      }
    ]
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `generate_budget_image` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/image-generation-agent
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
