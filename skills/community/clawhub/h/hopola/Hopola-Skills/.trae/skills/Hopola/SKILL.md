---
name: "Hopola"
description: "Runs web research and orchestrates image/video/3D generation, logo and product visuals, upload, and Markdown reporting. Use when users need an end-to-end multimodal production and delivery workflow."
required_credentials:
  - OPENCLOW_KEY
required_permissions:
  - network:http
  - local_file:read
---

# Hopola

## Purpose
Hopola turns "web research → image/video/3D generation → result upload → report output" into a reusable workflow, supporting both one-shot end-to-end execution and stage-based execution.

## When to Use
- The user needs content production based on web information and also needs visual outputs and delivery.
- The user wants one-pass execution for research, generation, upload, and consolidated reporting.
- The user only needs a specific stage (search only / generation only / upload only / report only).
- The user needs video or 3D outputs included in the same report.

## Prerequisites
- `web-access` is available for web search and page reading.
- OpenClaw Gateway is reachable.
- `OPENCLOW_KEY` is configured in the runtime environment.
- Upload policy endpoint uses `MAAT_TOKEN_API` (compatible with `MEITU_TOKEN_API` / `NEXT_PUBLIC_MAAT_TOKEN_API` / `NEXT_PUBLIC_MEITU_TOKEN_API`).
- `MAAT_TOKEN_API_ALLOWED_HOSTS` controls trusted upload policy hosts (comma-separated, includes `strategy.stariidata.com` by default).
- `OPENCLAW_REQUEST_LOG` defaults to `0` and should be enabled only for temporary debugging.
- If `OPENCLOW_KEY` is missing, stop at precheck and return `structured_error.code=GATEWAY_KEY_MISSING`; do not call Gateway tools.

## ClawHub Release Structure
- `SKILL.md`: Main orchestration and strategy
- `subskills/search/SKILL.md`: Search subskill
- `subskills/generate-image/SKILL.md`: Image generation subskill
- `subskills/generate-video/SKILL.md`: Video generation subskill
- `subskills/generate-3d/SKILL.md`: 3D generation subskill
- `subskills/logo-design/SKILL.md`: Logo design subskill
- `subskills/product-image/SKILL.md`: Product image subskill
- `subskills/cutout/SKILL.md`: Product cutout subskill
- `subskills/upload/SKILL.md`: Upload subskill
- `subskills/report/SKILL.md`: Report subskill
- `playbooks/design-intake.md`: Design intake template and proposal framework
- `scripts/`: Release validation and packaging scripts
- `assets/`: Logo, cover, and flow diagram
- `README.zh-CN.md` / `README.en.md`: Bilingual documentation

## Execution Modes

### Mode A: Single-Entry Full Pipeline
Execute in order:
1. Intake & Normalize: Collect explicit URLs plus session-uploaded images and normalize them into upload-ready assets.
2. Search: Invoke the search subskill to extract usable facts.
3. Discover: Query Gateway MCP tools and identify image/video/3D tools.
4. Generate: Invoke the corresponding generation subskill by task type.
5. Upload: Invoke the upload subskill to submit images or result links.
6. Report: Invoke the report subskill to output a Markdown report.

### Mode B: Stage-Based Execution
Execute only one stage based on user instruction:
- SearchOnly
- GenerateImageOnly
- GenerateVideoOnly
- Generate3DOnly
- GenerateLogoOnly
- GenerateProductImageOnly
- CutoutOnly
- UploadOnly
- ReportOnly

## Standard Inputs
- `query`: Search topic or target question.
- `search_scope`: Search scope and constraints (optional).
- `image_prompt`: Prompt for image generation (optional, required in GenerateImageOnly).
- `video_prompt`: Prompt for video generation (optional, required in GenerateVideoOnly).
- `model3d_prompt`: Prompt for 3D generation (optional, required in Generate3DOnly).
- `logo_prompt`: Prompt for logo generation (optional, required in GenerateLogoOnly).
- `product_prompt`: Prompt for product image generation (optional, required in GenerateProductImageOnly).
- `product_image_url`: Source product image URL (optional in input, mandatory before product-image generation tool call).
- `image_url`: Source image URL for cutout (optional, required in CutoutOnly).
- `session_uploaded_images`: Session-level uploaded image references (optional; local file path, attachment handle, or markdown image source).
- `auto_upload_session_images`: Whether to auto-upload session-uploaded images first (default `true`).
- `normalized_source_images`: Internal normalized image list produced by intake stage (optional internal field).
- `primary_source_image_url`: First available uploaded URL after normalization (optional internal field).
- `cutout_mode`: Cutout mode for edge handling (optional, default `auto`).
- `output_background`: Background mode after cutout (optional, default `transparent`).
- `desired_scenes`: Requested product image scenes list (optional, required before generation).
- `product_info_confirmed`: Whether product information is confirmed before generation (optional, default `false`).
- `source_image_confirmed`: Whether the source product image is explicitly provided or confirmed by user (optional, default `false`; mandatory before product-image generation).
- `image_style`: Style preference (optional).
- `image_size`: Image size (optional).
- `video_ratio`: Video aspect ratio (optional).
- `video_duration`: Video duration (optional).
- `model3d_quality`: 3D quality level (optional).
- `upload_enabled`: Whether to upload results (default `true`).
- `report_format`: Fixed as `markdown`.
- `mode`: `pipeline` or `stage`.
- `task_type`: `image|video|3d|logo|product-image`.
- `stage`: When `mode=stage`, use one of `search|generate-image|generate-video|generate-3d|generate-logo|generate-product-image|cutout|upload|report`.
- `gateway_base_url`: Default `https://hopola.ai`.
- `openclaw_key_env`: Default `OPENCLOW_KEY`.
- `response_language`: Optional explicit output language code (`en`, `zh-CN`, `ja`, etc.); if omitted, infer from the latest user message.

## Standard Output (Markdown)
The report must include at least:
1. Summary of search findings
2. Generation outputs (image/video/3D)
3. Upload results
4. Security status and error alerts
5. Final conclusion and next-step suggestions

## Configuration Placeholders
- `GATEWAY_BASE_URL`: Gateway domain
- `GATEWAY_MCP_TOOLS_ENDPOINT`: `/api/gateway/mcp/tools`
- `GATEWAY_MCP_CALL_ENDPOINT`: `/api/gateway/mcp/call`
- `GATEWAY_KEY_HEADER`: `X-OpenClaw-Key`
- `MAAT_UPLOAD_SCRIPT_PATH`: `scripts/maat_upload.py`
- `IMAGE_PREFERRED_TOOL_NAME`: Preferred fixed tool for image generation
- `VIDEO_PREFERRED_TOOL_NAME`: Preferred fixed tool for video generation
- `MODEL3D_PREFERRED_TOOL_NAME`: Preferred fixed tool for 3D generation
- `MODEL3D_SECONDARY_PREFERRED_TOOL_NAME`: Secondary preferred tool for 3D generation
- `LOGO_PREFERRED_TOOL_NAME`: Preferred fixed tool for logo generation
- `PRODUCT_IMAGE_PREFERRED_TOOL_NAME`: Preferred fixed tool for product image generation
- `IMAGE_MCP_TOOL_MATCH_RULES`: Auto-discovery rules for image tools
- `VIDEO_MCP_TOOL_MATCH_RULES`: Auto-discovery rules for video tools
- `MODEL3D_MCP_TOOL_MATCH_RULES`: Auto-discovery rules for 3D tools
- `IMAGE_MCP_ARGS_SCHEMA`: Argument mapping schema for image tools
- `VIDEO_MCP_ARGS_SCHEMA`: Argument mapping schema for video tools
- `MODEL3D_MCP_ARGS_SCHEMA`: Argument mapping schema for 3D tools
- `LOGO_MCP_ARGS_SCHEMA`: Argument mapping schema for logo tools
- `PRODUCT_IMAGE_MCP_ARGS_SCHEMA`: Argument mapping schema for product image tools
- `REQUEST_TIMEOUT_MS`: Request timeout
- `RETRY_MAX`: Max retries
- `MAAT_TOKEN_API`: Upload policy endpoint (default `https://strategy.stariidata.com/upload/policy`)
- `MAAT_TOKEN_API_ALLOWED_HOSTS`: Trusted hosts for upload policy endpoint
- `OPENCLAW_REQUEST_LOG`: Request log switch (`0` by default)

## Execution Rules
- In the search stage, prioritize strategic online retrieval with `web-access`; combine search and page reading when necessary.
- Before routing, normalize natural-language intent first: if user asks for product visuals such as 商品图/主图/详情图/场景图 or equivalent expressions, force `task_type=product-image` and `stage=generate-product-image`.
- For `task_type=product-image` or `stage=generate-product-image`, if no usable source image is present (`product_image_url` missing and `session_uploaded_images` empty/unresolvable), only return inquiry guidance asking user to upload product image or provide public URL; do not call any product-image generation tool.
- Before any stage requiring image URL input (`product_image_url`, `image_url`, `model3d_image_url`), run intake normalization:
  - Merge explicit URL fields with `session_uploaded_images`.
  - If an item is a local/session file, attachment reference, or markdown image source, invoke `subskills/upload/SKILL.md` to upload first.
  - Write uploaded links back to corresponding URL fields; if multiple links exist, use the first as `primary_source_image_url` and keep all in `normalized_source_images`.
- When required URL fields are missing but session-uploaded images are available, auto-fill from normalized uploaded URLs and continue workflow.
- For `task_type=product-image`, if explicit `product_image_url` is not a public `http(s)` URL, force upload normalization first and block generation until URL backfill succeeds.
- For `task_type=product-image`, source normalization origin must be traceable as one of `user_public_url|uploaded_from_session|uploaded_from_local|uploaded_from_markdown|uploaded_from_non_public_url`.
- If `auto_upload_session_images=true` and upload fails, stop the dependent generation stage and return structured missing/failed inputs with retry suggestions.
- For generation tasks, use "preferred fixed tool first; auto-discovery fallback if unavailable"; product-image follows stricter fixed-tool-only rules in `subskills/product-image/SKILL.md`.
- For logo design, default to `aiflow_nougat_create`; for product image, default to `image_praline_edit_v2`.
- For product-image generation, always choose `image_praline_edit_v2` as the first and default call target; do not switch to other image-edit tools when `image_praline_edit_v2` is available.
- For `task_type=product-image` or `stage=generate-product-image`, routing must enter `subskills/product-image/SKILL.md` as the only orchestration entry.
- For `task_type=product-image` or `stage=generate-product-image`, do not bypass `subskills/product-image/SKILL.md` to call product-image tools directly.
- For `task_type=product-image` or `stage=generate-product-image`, first execute mandatory user inquiry and confirmation before any product-image tool call.
- Product-image detailed execution rules (source confirmation, non-URL upload normalization, prechecks, confirmation card, error mapping) are defined only in `subskills/product-image/SKILL.md`.
- For product-image generation, source image must be user-provided or explicitly user-confirmed in current context; otherwise stop before any tool call.
- If source confirmation precheck fails or `image_list` does not use the confirmed source URL, return `structured_error.code=PRODUCT_IMAGE_UNCONFIRMED_SOURCE` and stop before tool call.
- Logo tasks must invoke an actual generation tool and return image links, not text-only plans.
- For 3D generation, default to `3d_hy_image_generate`; for single-image input, prioritize `fal_tripo_image_to_3d`.
- In the discover stage, call `GET /api/gateway/mcp/tools` first and build arguments from returned `tool_schema`.
- Gateway tool list may appear under `data.list` or `tools`; for product-image task, resolve tool identity by `tool_name|skill_name|name` and require exact match `image_praline_edit_v2`.
- If both `image_praline_edit_v2` and similarly named tools appear, always select `image_praline_edit_v2`.
- In the generate stage, call `POST /api/gateway/mcp/call` with `tool_name` and `args`.
- In the upload stage, invoke `subskills/upload/SKILL.md` and return stable accessible URLs for all local/session images.
- Session-uploaded local images must follow the same upload stage constraints (format/size/accessibility validation and failed-upload retry guidance).
- All Gateway requests must include `X-OpenClaw-Key` in headers, and keys must be read only from environment variables.
- Before any Gateway call, precheck `OPENCLOW_KEY`. If missing, return `structured_error` with `code=GATEWAY_KEY_MISSING`, `stage=precheck`, and actionable retry suggestions.
- The report stage must output Markdown consistently and explicitly mark missing fields.
- For product-image tasks, never use local/offline image synthesis fallback (for example PIL scripts or local compositing) to replace Gateway + subskill execution.
- For product-image generation responses, include execution evidence fields: `tool_name_used`, `source_image_url_used`, `source_image_origin`, `precheck_report`, and non-sensitive call receipt fields from Gateway response.

## Language Policy
- All conversational text must follow `response_language` when provided; otherwise infer from the latest user message.
- If language inference is uncertain, follow the language used in the latest user instruction in the current turn.
- Do not output Chinese by default; Chinese is allowed only when user language is Chinese.
- Do not mix multiple natural languages in one response, except for immutable technical tokens (API paths, field names, tool names).
- Confirmation prompts, error messages, report sections, and suggestions must all use the same target language.
- If any upstream subskill returns text in a different language, rewrite it into the target language before returning.

## Failure Handling
- Intra-stage failure: Retry by configuration, up to `RETRY_MAX`.
- Inter-stage degradation: If one stage fails, continue producing available outputs and document failure reasons in the report.
- Traceability: Record failed stage, input summary, and retry conclusion in the report.
- Product-image precheck failures must return unified `structured_error` with `code`, `stage`, `message`, `details`, `retry_suggestions`.
- Product-image precheck `code` must use one of `PRODUCT_IMAGE_TOOL_UNAVAILABLE|PRODUCT_IMAGE_SOURCE_NOT_ACCESSIBLE|PRODUCT_IMAGE_MISSING_ARGS|PRODUCT_IMAGE_UPLOAD_REQUIRED|PRODUCT_IMAGE_UPLOAD_FAILED|PRODUCT_IMAGE_UNCONFIRMED_SOURCE|PRODUCT_IMAGE_CREATE_TOOL_FORBIDDEN`.
- Permission interception: If response is `403` with `code=403001`, return `data.redirect_url` directly and prompt the user to activate membership.
- Tool unavailable: If the fixed tool is missing, automatically enable discovery fallback and record the fallback path, except product-image which must follow `subskills/product-image/SKILL.md` fixed-tool policy.

## Security and Compliance
- Never expose keys, tokens, or cookies in outputs.
- Validate image format and size before upload (max 20MB).
- Return only necessary results and publicly accessible links.
- Run the release security validation script before packaging to detect plaintext keys and block packaging.
