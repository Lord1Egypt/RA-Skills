---
name: product-mockup-studio
description: "Product Mockup Studio: Create branded product mockup images, refine approved stills, and animate them into short videos. Use when an agent needs product mockup studio, ai product photography from phone photos, shopify and woocommerce product page hero images, amazon and etsy listing photos on clean white backgrounds, lifestyle product scenes without a photoshoot, animate product mockup, source task id, source file id through AgentPMT-hosted remote tool calls."
version: 1.0.2
homepage: https://www.agentpmt.com/marketplace/product-mockup-studio
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/product-mockup-studio"}}
---
# Product Mockup Studio

## Freshness
Last updated: `2026-09-29`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Photograph your product with your phone and get back pictures you can actually sell with. Tell your agent what you want in plain words, like put my candle on a sunlit marble counter, give me a plain white version for Amazon, or make it vertical for Reels, and it creates the shot. Don't like something? Say so. Lighter background, softer shadow, move the eucalyptus, different angle, and it fixes just that while the product stays exactly the same. When a picture looks right, turn it into a short product video with a slow zoom, a turntable spin, an orbit, or a light sweep, sized for Shopify, Amazon, Etsy, Instagram Reels, TikTok, and YouTube Shorts. Tell it the exact words printed on your label and the details that must not change, and it holds onto them. Your agent handles the rest: the sizes, the formats, the revisions, and saving the finished files for you to download. AI product photography and product videos without a studio, a photographer, or editing software.

## Product Instructions
### Product Mockup Studio

Create a polished product still from reference photos, refine an approved still, or animate it into a short product clip. Inputs and outputs use AgentPMT File Manager IDs.

#### Recommended workflow

1. Upload one to five clear product images to File Manager.
2. Call `create_product_mockup` in `draft` mode.
3. Poll `get_mockup_job` until the image is `completed` or `failed`.
4. Visually review logos, text, dimensions, colors, and product details. Generated media always requires review.
5. Use `refine_product_mockup` for a focused revision, or create a fresh render with `image_provider: "nano_banana"` to compare providers.
6. Animate only an approved still, then poll the new video job.

The tool creates the output filename and uses the platform's fixed seven-day File Manager retention. There are no filename or expiration inputs.

#### Image provider behavior

- `auto` prefers ElevenLabs. With no mask and no more than four references, it falls back to Nano Banana only when ElevenLabs definitively rejects the submission for credentials, access, quota, rate limit, or invalid parameters. It does not retry or fall back after an ambiguous network failure because that could duplicate a paid generation.
- `elevenlabs` forces ElevenLabs image generation.
- `nano_banana` forces the approved centralized Google image connection.
- A successfully generated but visually weak image does not switch providers automatically. Review it, then explicitly refine it or create a new render with the other provider.
- Masked generation uses the ElevenLabs final route; masks are not accepted with `nano_banana`.

#### Actions

##### `create_product_mockup`

Required: `product_file_ids`, `scene_prompt`.

Useful optional fields: `product_description`, `mockup_style`, `camera_view`, `style_reference_file_ids`, `image_provider`, `render_mode` (`draft|final`), `aspect_ratio`, `mask_file_id`, and `brand_constraints`.

```json
{"action":"create_product_mockup","product_file_ids":["file_id"],"scene_prompt":"Premium studio hero shot on warm stone with soft side lighting","render_mode":"draft","image_provider":"auto"}
```

##### `refine_product_mockup`

Required: `source_task_id`, `instruction`. The source must be a completed image job from this tool in the same budget.

```json
{"action":"refine_product_mockup","source_task_id":"task_id","instruction":"Keep the package unchanged; make the background pale gray and soften the contact shadow","render_mode":"final"}
```

##### `animate_product_mockup`

Provide exactly one of `source_task_id` or `source_file_id`. Video uses ElevenLabs only. Optional controls include `motion_preset`, `motion_prompt`, `duration_seconds` (`4|6|8`), `aspect_ratio` (`16:9|9:16`), `resolution`, `render_mode` (`preview|final`), `generate_audio`, `end_frame_file_id`, `negative_prompt`, and `seed`.

When `aspect_ratio` is omitted it follows the still's orientation: a portrait still animates as `9:16` and every other still as `16:9`. The chosen value is returned as `aspect_ratio` on the create response.

A still that does not already match the video aspect is center-cropped before it is sent, because the video model otherwise pads the mismatch with black bars. The response reports the crop as `start_frame_adjustment`. To control the framing yourself, refine the still to the video aspect first, then animate that task.

```json
{"action":"animate_product_mockup","source_task_id":"completed_image_task_id","motion_preset":"slow_push_in","duration_seconds":6,"render_mode":"preview"}
```

##### `get_mockup_job`

Required: `task_id`. Polling an ElevenLabs job also imports a completed provider output into File Manager. Wait at least 2 seconds between image polls and 10 seconds between video polls. Once the task is completed, later polls return the stored output rather than importing it again.

```json
{"action":"get_mockup_job","task_id":"task_id"}
```

##### `list_mockup_jobs`

Lists jobs in the current budget. Optional: `media_kind`, `status`, `page_size`, and `cursor`.

#### Output

Creation actions return a `task_id` immediately. Completed jobs contain an `outputs` array with the provider, model, media kind, and a managed File Manager object containing `file_id`, generated `filename`, `content_type`, size, and signed preview URL. Still images are normalized to PNG; videos are MP4.

## When To Use
- Use this skill for `Product Mockup Studio` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: product mockup studio, ai product photography from phone photos, shopify and woocommerce product page hero images, amazon and etsy listing photos on clean white backgrounds, lifestyle product scenes without a photoshoot, animate product mockup, source task id, source file id.
- Supported action names: `animate_product_mockup`, `create_product_mockup`, `get_mockup_job`, `list_mockup_jobs`, `refine_product_mockup`.

## Use Cases
- AI product photography from phone photos
- Shopify and WooCommerce product page hero images
- Amazon and Etsy listing photos on clean white backgrounds
- Lifestyle product scenes without a photoshoot
- Packaging and label mockups that keep exact brand text
- Flat-lay and in-hand product shots for social media
- Vertical product videos for Instagram Reels and TikTok
- Turntable and orbit product clips for launch pages
- Ad creative in square vertical and widescreen sizes
- Fixing the background lighting or props on a product photo

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `5`.
x402 availability: not enabled for this product.

- `animate_product_mockup` (action slug: `animate-product-mockup`): Turn an approved product still into a short ElevenLabs MP4 product clip. Price: `10` credits. Parameters: `aspect_ratio`, `duration_seconds`, `end_frame_file_id`, `generate_audio`, `motion_preset`, `motion_prompt`, `negative_prompt`, `render_mode`, plus 4 more.
- `create_product_mockup` (action slug: `create-product-mockup`): Create one product-focused PNG mockup from File Manager product photos and a scene brief. Price: `25` credits. Parameters: `aspect_ratio`, `brand_constraints`, `camera_view`, `image_provider`, `mask_file_id`, `mockup_style`, `product_description`, `product_file_ids`, plus 3 more.
- `get_mockup_job` (action slug: `get-mockup-job`): Check one mockup job and import a completed PNG or MP4 into File Manager. Price: `1` credits. Parameters: `task_id`.
- `list_mockup_jobs` (action slug: `list-mockup-jobs`): List budget-scoped product mockup jobs without exposing unrelated provider generations. Price: `1` credits. Parameters: `cursor`, `media_kind`, `page_size`, `status`.
- `refine_product_mockup` (action slug: `refine-product-mockup`): Revise a completed mockup while preserving its product identity and approved composition. Price: `25` credits. Parameters: `aspect_ratio`, `brand_constraints`, `image_provider`, `instruction`, `mask_file_id`, `render_mode`, `source_task_id`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "product-mockup-studio"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "product-mockup-studio"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "product-mockup-studio"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "product-mockup-studio"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "product-mockup-studio"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "product-mockup-studio"
  }
}
```

## Call This Tool
Product slug: `product-mockup-studio`

Marketplace page: https://www.agentpmt.com/marketplace/product-mockup-studio

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
    "name": "Product-Mockup-Studio",
    "arguments": {
      "action": "animate_product_mockup",
      "aspect_ratio": "16:9",
      "duration_seconds": 4,
      "end_frame_file_id": "example end frame file id",
      "generate_audio": true,
      "motion_preset": "slow_push_in",
      "motion_prompt": "example motion prompt",
      "negative_prompt": "example negative prompt",
      "render_mode": "preview"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "product-mockup-studio",
  "parameters": {
    "action": "animate_product_mockup",
    "aspect_ratio": "16:9",
    "duration_seconds": 4,
    "end_frame_file_id": "example end frame file id",
    "generate_audio": true,
    "motion_preset": "slow_push_in",
    "motion_prompt": "example motion prompt",
    "negative_prompt": "example negative prompt",
    "render_mode": "preview"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `animate_product_mockup` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/product-mockup-studio
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
