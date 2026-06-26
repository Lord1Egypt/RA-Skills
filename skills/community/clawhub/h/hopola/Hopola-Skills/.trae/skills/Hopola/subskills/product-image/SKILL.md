---
name: "hopola-product-image"
description: "Primary product-image generation subskill. Must be invoked whenever `task_type=product-image` or `stage=generate-product-image`, after inquiry and confirmation are completed."
---

# Hopola Product Image

## Purpose
Handle e-commerce product-image inquiry, visual planning, and batch generation for deployable assets.

## Trigger
- User needs hero images, detail visuals, or scene visuals for a product.
- User needs background replacement, stronger selling-point visuals, or unified visual style.
- Main skill sets `task_type=product-image` or stage `generate-product-image`.
- This subskill is the mandatory execution target for product-image generation requests.

## Inputs
- `product_name`
- `product_category`
- `product_selling_points`
- `product_image_url`
- `session_uploaded_images`
- `auto_upload_session_images`
- `target_channel`
- `target_audience`
- `desired_scenes`
- `product_info_confirmed`
- `visual_style`
- `background_style`
- `product_ratio`
- `source_image_confirmed`
- `key`
- `response_language`

## Outputs
- `product_image_urls`
- `visual_solution_summary`
- `tool_name_used`
- `source_image_url_used`
- `source_image_origin`
- `fallback_used`
- `product_confirmation_card`
- `precheck_report`
- `structured_error`

## Fixed Workflow
1. Ask for product information and target scenes.
   - If upstream input is natural language only, convert it into structured inquiry first and return `product_confirmation_card`; do not generate in this round.
   - If no usable source image exists (`product_image_url` missing and no resolvable `session_uploaded_images`), return missing-image inquiry guidance only and stop before any tool call.
2. Normalize source image by priority:
   - Keep explicit `product_image_url` only if it is a public `http(s)` URL.
   - If explicit `product_image_url` is non-URL input (local path, attachment handle, markdown image source, session reference), invoke upload subskill first and backfill `product_image_url` with uploaded URL.
   - If explicit `product_image_url` is a non-public/intranet URL, invoke upload subskill first and backfill `product_image_url` with uploaded URL.
   - If `product_image_url` is missing but `session_uploaded_images` exists, invoke upload subskill to auto-upload and backfill `product_image_url`.
   - If upload fails at any step, terminate generation and return `structured_error` with `code=PRODUCT_IMAGE_UPLOAD_FAILED` plus executable retry suggestions.
3. Validate required fields.
4. Return `product_confirmation_card` and wait for user confirmation.
5. Run prechecks before every generation call:
   - Tool availability (`image_praline_edit_v2` must exist).
   - Input URL accessibility (`product_image_url` must be reachable by HEAD/GET).
   - Source confirmation (`source_image_confirmed=true` and explicit user confirmation in current context).
   - Required generation args completeness (`image_list`, `prompt`, `output_format`, `size`).
6. Build `image_list=[product_image_url]` from the resolved confirmed source URL only.
7. Call generation tools only after explicit user confirmation intent, `product_info_confirmed=true`, `source_image_confirmed=true`, and precheck pass.
8. Resolve candidate tools from Gateway list fields (`data.list` or `tools`) and always select exact `image_praline_edit_v2` by `tool_name|skill_name|name`.

## Scene Field Rules
- `desired_scenes` must include at least 1 scene.
- Recommend 3 default scenes:
  - Pure white hero image
  - Lifestyle scene image
  - Selling-point infographic

## Inquiry Checklist
- What is the product (name, category, core selling points)?
- Which channel is targeted (marketplace, social commerce, DTC site)?
- Who is the target audience (persona, price band, purchase motivation)?
- Which image scenes are required (hero, lifestyle, selling-point)?
- Any prohibited elements or compliance constraints?
- Is a source product image URL available for fidelity-preserving generation?

## Confirmation Card Template
```markdown
## Product Information Confirmation Card
- Product Name: {product_name}
- Product Category: {product_category}
- Core Selling Points: {product_selling_points}
- Channel: {target_channel}
- Target Audience: {target_audience}
- Source Product Image: {product_image_url}
- Source Image Confirmed: {source_image_confirmed}
- Desired Scenes: {desired_scenes}
- Compliance Constraints: {compliance_constraints}

Please confirm the details above. Generation starts only after explicit confirmation.
```

## Rules
- Prefer `image_praline_edit_v2` by default.
- For every generation round, `tool_name_used` must be `image_praline_edit_v2` when this tool is available.
- Mandatory inquiry dimensions: product, channel, audience, scenes, selling points, price band, competitor comparison, and compliance constraints.
- Generation gate: confirm product information before calling any product-image tool.
- Required confirmation fields: `product_name`, `product_category`, `product_selling_points`, `target_channel`, `target_audience`, `product_image_url`, `desired_scenes`.
- `product_image_url` may come from explicit URL or auto-uploaded session image URL, but the confirmation card must show the final resolved URL.
- `product_image_url` must represent the user-provided or user-confirmed real product source image; no proxy placeholder or generated substitute is allowed.
- Source origin must be recorded as one of `user_public_url|uploaded_from_session|uploaded_from_local|uploaded_from_markdown|uploaded_from_non_public_url`.
- Non-URL image inputs are not allowed to enter generation directly; they must be uploaded and converted to accessible URL first.
- `key` can be used only as task identity metadata and must not bypass source confirmation, prechecks, or required fields.
- If `product_info_confirmed != true` or any required field is missing, return only `product_confirmation_card` and continue inquiry; do not call `image_praline_edit_v2`.
- If `source_image_confirmed != true`, return `structured_error` with `code=PRODUCT_IMAGE_UNCONFIRMED_SOURCE` and do not call any generation tool.
- If source image is missing after normalization, return missing-image inquiry guidance in `response_language` and do not call any generation tool.
- Enter generation only when user gives explicit confirmation intent in their own language and `product_info_confirmed=true`.
- `source_image_confirmed=true` is mandatory and cannot be inferred from `product_info_confirmed`.
- Product-image generation must never call text-to-image create tools such as `image_praline_create_*`; only edit-toolchain calls are allowed.
- Product-image generation must never use local/offline image processing fallback (including PIL/local compositing) as a replacement execution path.
- Every call attempt in the same task must repeat source confirmation and argument prechecks; confirmation cannot be reused across changed source inputs.
- Before calling `image_praline_edit_v2`, always build and validate:
  - `image_list`: array containing only the resolved confirmed `product_image_url`.
  - `prompt`: generation intent for product visuals.
  - `output_format`: output format (for example `jpg`/`png`).
  - `size`: target output size or ratio config accepted by tool.
- If `image_list` contains anything other than the confirmed `product_image_url`, return `structured_error` with `code=PRODUCT_IMAGE_UNCONFIRMED_SOURCE` and stop before tool call.
- For every successful generation response, always include `tool_name_used=image_praline_edit_v2`, `source_image_url_used=<resolved product_image_url>`, `source_image_origin=<resolved origin>`, and `precheck_report`.
- If prechecks fail, stop before tool call and return `structured_error` in unified format:
  - `code`: one of `PRODUCT_IMAGE_TOOL_UNAVAILABLE`, `PRODUCT_IMAGE_SOURCE_NOT_ACCESSIBLE`, `PRODUCT_IMAGE_MISSING_ARGS`, `PRODUCT_IMAGE_UPLOAD_REQUIRED`, `PRODUCT_IMAGE_UPLOAD_FAILED`, `PRODUCT_IMAGE_UNCONFIRMED_SOURCE`, `PRODUCT_IMAGE_CREATE_TOOL_FORBIDDEN`.
  - `stage`: fixed value `precheck`.
  - `message`: concise user-facing failure summary in `response_language`.
  - `details`: machine-readable object including `missing_fields`, `source_input_type`, `http_status`, `failed_step`.
  - `retry_suggestions`: executable next actions.
- First generation round should output at least 3 scene variants: pure white hero image, lifestyle scene image, and selling-point infographic.
- If fixed tool is unavailable, only retry with the same `image_praline_edit_v2` toolchain.
- If resolved tool is not exactly `image_praline_edit_v2` while `image_praline_edit_v2` is available, stop and return `PRODUCT_IMAGE_TOOL_UNAVAILABLE` with mismatch details.
- Inquiry questions, confirmation cards, and all replies must follow `response_language` or inferred user language.
- Do not output Chinese unless user language is Chinese.
- Never use generated/proxy/placeholder images as source replacement for product-image generation.
