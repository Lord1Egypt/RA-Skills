# Changelog

Skill package versions. The API contract version is separate and lives in
`SKILL.md` as `metadata.api_version` — a skill release does not move it.

## 1.4.1

- Restrict authenticated requests to the official HTTPS service and refuse redirects.
- Correct image-edit arguments, reference labels, image formats, pricing and model guidance.
- Preserve structured error diagnostics and report incomplete streams as failures.
- Isolate account task records and serialize atomic updates; provide explicit recovery commands.
- Clean up cancelled jobs, preserve list output compatibility and validate malformed responses.
- Bound upload memory, support JSON reference URL arrays and clarify model-specific controls.

## 1.4.0 — 2026-11-15 (API v1.3.0)

- Add LLM chat: Qwen3.8 27B (`qwen3.8-27b`) through the OpenAI-compatible `POST /api/v1/chat/completions`.
- New `chat` command: system prompt, full message arrays, up to 2 images, JSON mode, tool calling, thinking and streaming.
- Document accepted fields, limits, per-token pricing, streaming usage and error handling for agents.
- H3: optional `unrestricted_enhancement` flag (CLI `--unrestricted-enhancement`).

## 1.3.12 — 2026-11-14 (API v1.2.5)

- Document English API diagnostics independently of UI and browser language.
- Explain maintenance rejection, status checks, retry advice and 429 rejection reasons.
- Require agents to explain errors in the user's language without automatically resubmitting rejected tasks.

## 1.3.11 — 2026-11-10 (API v1.2.5)

- Remove obsolete preview expansion controls and clarify H3-only parameter boundaries.
- Expose the existing optional model-limit adaptation flag in the CLI; mandatory processing remains automatic.
- Correct legacy Turbo 768p notes to match the existing pricing table.

## 1.3.10 — 2026-11-09 (API v1.2.5)

- Require automatic prompt processing for every H3 submission, including structured input.
- Remove customer-facing debug switches and preview bypass instructions; retain the separate model-limit adaptation option.

## 1.3.9 — 2026-11-05 (API v1.2.4)

- Prepare H3 Turbo 768p output and reference-video pricing at USD 0.012/second (0.12 credits/second).
- Generate H3 price sections from the selected release configuration; retain 480p, Standard, free-image allowance and free audio.
- Explain actual combined reference-video duration, rounding and unchanged historical charges.

## 1.3.8 — 2026-11-04 (API v1.2.4)

- Add LTX discovery, CLI example and frame-based price qualifications.
- Clarify configured prices versus open models and separate business price surfaces.
- Keep GPT Image 2 single-image billing explicit; document unverified Turbo availability.

## 1.3.7 — 2026-10-27 (API v1.2.4)

- Add H3 prompt guidance for dialogue, silence, reference roles, camera planning and enhancement troubleshooting.

## 1.3.6 — 2026-10-21 (API v1.2.4)

- Discovery: lead the package quick start and model map with MiniMax H3 Standard and Turbo.
- Documentation: add the Turbo Reference-to-Video model ID to the public model table and make the first copy-paste video commands use explicit H3 IDs.
- Packaging: bump the skill package version; the gateway API version is unchanged.

## 1.3.5 — 2026-10-21 (API v1.2.4)

- Pricing: MiniMax H3 Turbo (`text-to-video/turbo`, `image-to-video/turbo`, `reference-to-video/turbo`) is now $0.006/s at 480p and $0.009/s at 768p; Turbo reference video is billed at the same per-second rate. Reference images: first 5 free, then $0.0025 each (unchanged).
- History / request details: `prompt` and `original_prompt` return the prompt exactly as you submitted it. Older requests whose original input was not saved return `prompt: null` with `original_prompt_unavailable: true`.
- Includes 1.3.4 (not published separately): `negative_prompt` is not supported by `minimax/h3/*` models and is ignored if provided.

## 1.3.4 (2026-10-12)

- Docs: note that `negative_prompt` is not supported by `minimax/h3/*` models (the parameter is ignored if provided). No behavior change.

## 1.3.2 — 2026-09-25 (API v1.2.2)

`minimax/h3/reference-to-video/turbo` is available as MiniMax H3 Turbo

- Requests to `minimax/h3/reference-to-video/turbo` are supported with the Turbo pricing shown in the API reference
- Use `minimax/h3/reference-to-video` instead — same inputs and pricing structure
- `reference-to-video` (non-turbo) is unaffected
- API contract version v1.2.2: a model id was removed; no other endpoints or parameters changed

## 1.3.1 — 2026-09-24 (API v1.2.1)

Reference-to-Video limits and pricing

- Reference caps, both 480p and 768p: 9 images when sending only images, 5 images when
  videos or audio are also present, 3 reference videos, 3 reference audios
- Total reference video length is 15.1s across all reference videos
- `reference-to-video` now uses the same rates as the rest of H3: 480p $0.0045/s,
  768p $0.012/s, reference images $0.0075 each after the first 5
- Bundled client validation and version string updated to match
- API contract version v1.2.1: Reference-to-Video limits and pricing changed; no new endpoints or parameters

## 1.3.0 — 2026-09-22 (API v1.2.0)

Reference metadata and H3 limits

- Reference labels are forwarded in the same order as image, video, and audio URLs
- 768p Ref2VA supports the same 9 image-only, 4 mixed-image, and 3 video caps as 480p
- Correct the bundled client's stale 768p validation and 15-second video budget

## 1.2.0 — 2026-09-13 (API v1.2.0)

Reference-to-Video

- Total reference video length raised from 10s to 15s, across all reference
  videos combined. `reference-to-video/turbo` is unchanged at 10s.
- No other caps moved, and pricing is unchanged.

## 1.2.0 — 2026-09-10

Pricing

- MiniMax H3 (T2V / I2V / Ref2VA / Ref2VA Turbo) now shares one per-output-second
  rate regardless of clip length: 480p $0.0045/s, 768p $0.012/s (previously 0.02 / 0.04 USD
  for T2V/I2V and 0.025 / 0.063 USD for Ref2VA)
- Ref2VA reference inputs: the first 5 reference images are free, then $0.0075 each
  (previously 0.01 USD from the first image); reference audio is free (previously 0.01 USD);
  reference video stays at the output tier rate
- `GET /api/v1/pricing/config` adds `reference_image_free_count`; the built-in
  client's price table and estimate formula follow it

Reference-to-Video Turbo

- `minimax/h3/reference-to-video/turbo` added to the model table with its own reference
  caps and 768p usage guidance (stay at or below 3 images, or 2 images plus 1 video)

Client and docs

- Environment section and `--base-url` help use placeholders instead of a specific host
- `studio-layouts` on a self-hosted deployment reads `PHOSOR_WEB_BASE_URL` for the web
  front instead of guessing ports
- Code comments in `phosor_client.py` are English throughout

## 1.1.0 — 2026-09-03

New models

- MiniMax H3: text-to-video, image-to-video with an optional closing frame,
  and Reference-to-Video, which takes reference images, videos and audio in
  one request. 480p and 768p, 4-15 seconds, billed per output second
- GPT Image 2 text-to-image, at five sizes: 1024x1024, 1920x1072 / 1072x1920
  and 2560x1440 / 1440x2560
- FLUX.2-dev text-to-image and image edit
- Z-Image Turbo text-to-image and image-to-image, with LoRA
- Qwen3-TTS text-to-speech, billed per character, minimum $0.003 per request

New surface

- Image Studio, for e-commerce product and model photography: product suites,
  clothing and on-model suites, selling-point layouts, A+ content, white
  background, scene variation, and one-off tools for background removal,
  inpainting and image translation. Async throughout: POST returns a
  request_id, then poll until done

Client

- Advertises all five GPT Image 2 sizes; the previous release listed only
  1024x1024 and rejected the other four valid sizes
- `--version` now prints the real package version

Packaging

- The package and its zip are named phosor-ai-skills, matching the folder it
  unpacks into and this skill's slug
- Two version numbers, on purpose: the skill version covers this package
  (commands, docs, bundled client), `metadata.api_version` covers the gateway
  contract. Either can move without forcing the other
- A stray compiled .pyc no longer rides along inside the archive

Docs

- `references/api.md` covers every endpoint the skill calls, with limits and
  live pricing pointers. Prices are never hardcoded — call the pricing
  endpoints for current numbers

## 1.0.2 / 1.0.1 — 2026-05

Published without changelog entries; both carried the 1.0.0 text. Recorded
here so the gap is visible rather than implied.

## 1.0.0 — 2026-03-23 — Initial release

- AI content generation platform, supporting Wan 2.2 14B text-to-video and
  image-to-video
- Upload and use custom LoRA models for style customization
- 16 CLI commands for job submission, uploads, status, results, and model
  listing
- Supports preset resolutions (480p/720p/1080p), frame alignment rules, and
  usage quotas
