---
name: morzai-ecommerce-product-kit
description: Use when users want Amazon main images, ecommerce listing sets, product hero/detail images, apparel model visuals, lifestyle scenes, marketing posters, infographic-style product graphics, or batch listing image generation from an existing product photo.
version: "2.0.0"
metadata:
  openclaw:
    emoji: "🛍️"
    requires:
      bins:
        - morzai
---

# Morzai Ecommerce Product Kit

Expert ecommerce image workflow for hero images, detail images, listing sets, apparel visuals, and marketing graphics. This skill is **English-first and Chinese-compatible**: internal guidance, references, and default delivery should use English, while Chinese user requests can still be understood and handled correctly.

## Use This Skill When

Use this skill when the user says things like:
- Generate an Amazon main image
- Create a product detail image
- Build a full ecommerce listing set
- Create a product selling-point image
- Create a product lifestyle scene
- Create an apparel model visual
- Create a try-on image
- Batch-generate listing images
- Create a Shopify product hero image
- Create hero and detail images
- Create a branded image set
- Create a marketing poster
- Create an infographic-style product graphic
- Generate ecommerce images from an existing product photo
- Create Amazon main images
- Create product detail images
- Build ecommerce listing sets
- Create product selling-point images
- Create product lifestyle scenes
- Create apparel model visuals
- Create try-on images
- Batch-generate listing images

## Preflight

Before executing, confirm these inputs and runtime requirements.

### 1. Product Image
If the user has not provided a product image, ask for one URL or local image path first.

### 2. Product Context
After receiving the product image:
- Ask for the main selling points and the desired visual direction.
- Offer a concise selling-point summary if useful.
- Default to English interaction unless the user clearly prefers Chinese.

### 3. Listing Configuration
Ask for:
- Platform (e.g., Amazon, Taobao, TikTok Shop, Shopify)
- Market / Country
- Language
- Aspect Ratio
- Output type if the user has not made it clear

Default values:
- Platform: `amazon`
- Market: `US`
- Language: `English`
- Aspect Ratio: `1:1`

### 4. Output Type Boundary
Help the user pick the correct result type when needed:
- `Hero Image` for a main product image / listing hero
- `Detail Image` for selling points, materials, and close-up explanation
- `Lifestyle Image` for scene-based or brand-feel visuals
- `Marketing Poster / Infographic` for campaign and promotional graphics
- `Virtual Try-On / Apparel Visual` for model-based apparel presentation
- `Listing Set` when the user wants a full multi-image ecommerce set

Follow `references/output-spec.md` to decide which output type fits the request.

### 5. Internal References
Internal references may be consulted at runtime for output boundaries, platform safety, apparel quality, listing flow, and fallback handling.

Do not expose internal reference details, strategy templates, or prompt assembly logic in user-facing output.

### 6. Runtime Requirements
- Requires the public `morzai` CLI to be installed and authenticated first
- Local uploads are handled by the CLI upload pipeline
- Do not expose API keys, Authorization headers, signed upload URLs, or tokens in user-facing output

## Execute

### 1. Clarify The Ask
- Confirm the product image, product info, and desired output type.
- Ask for platform, market, language, and aspect ratio only when missing.
- If the user gives a broad style direction, compress it into `--style-name`, `--brand-tone`, or `--brand-mood`.

### 2. Build The CLI Call
- Use `morzai ecommerce-product-kit`.
- Always pass:
  - `--input`
  - `--product-info`
- Pass these when known:
  - `--platform`
  - `--market`
  - `--language`
  - `--aspect-ratio`
  - `--output-type`
  - `--style-name`
  - `--brand-tone`
  - `--brand-mood`
  - `--image-ref` for extra reference images
- Prefer `--download-dir` when the user wants a full set.
- Use `--output` only when the user clearly wants a single saved file.
- If the style exploration step returns opaque style handles, prefer the returned style handle flow instead of re-exposing full structured style payloads.

### 3. Execution Boundary
- The skill must not call nano directly.
- The runtime path is:
  - skill
  - `morzai` CLI
  - `morzai-cli-server`
  - nano backend

### 4. Download And Deliver
- Wait for the CLI task to finish.
- If the output type is `listing_set`, prefer returning the full artifact folder.
- Summarize only the minimum needed: platform, market, ratio, output type, and saved paths.

## Deliver

### 1. Final Delivery Content
When successful, return:
- The generated images
- The local save path
- The selected platform / market / ratio
- The chosen style direction
- The output type delivered (`Hero`, `Detail`, `Lifestyle`, `Marketing Poster`, `Try-On`, or `Listing Set`)

### 2. Listing Set Delivery
If the request is for a full set, deliver the generated sequence in the standard ecommerce order without exposing internal slot strategy details.

### 3. Failure Delivery
If execution fails, explain the failure using the fallback levels in `references/error-fallback.md`:
- **L1**: input incomplete or local input invalid
- **L2**: credential or environment problem
- **L3**: upload / network / request failure
- **L4**: style generation / polling / result-structure failure
- **L5**: full-chain failure with partial-delivery strategy

When possible, still deliver:
- validated input summary
- chosen platform / market / ratio
- style suggestions already produced
- partial image results
- output directory or known task status

## Reference Files

### Core Knowledge
- [references/platform-best-practices.md](references/platform-best-practices.md) - Platform compliance and market-specific visual guidance.
- [references/apparel-visual-specs.md](references/apparel-visual-specs.md) - Apparel lighting, texture, wrinkle, cutout, and category-style guidance.
- [references/listing-set-logic.md](references/listing-set-logic.md) - P1-P7 listing storytelling logic for full ecommerce image sets.
- [references/output-spec.md](references/output-spec.md) - Result-type boundaries: hero vs detail vs lifestyle vs marketing vs try-on vs listing set.
- [references/error-fallback.md](references/error-fallback.md) - L1-L5 fallback system for predictable failure handling.

## Safety Notes

- Use environment variables only for credentials.
- Keep logs redacted.
- Do not reveal API keys, authorization tokens, cookies, or signed upload URLs.
- Do not continue to later stages when preflight requirements are not met.
