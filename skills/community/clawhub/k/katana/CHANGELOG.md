# Changelog

## 1.0.3

### Added
- `q-naifu-a3b` text model — imgnAI fully uncensored Agentic Model (Private tier, 262K context, vision + file input)
- `naifu` / `q-naifu` model alias mapping to `q-naifu-a3b`
- Text polling for long-running models — submit with `?wait=false`, poll via `GET /v1/generation-requests/{id}`
- Audio output docs for video models — which models generate audio, how to strip it
- Three-tier privacy documentation — Anonymized, Private, E2EE Private with attestation details
- Error codes quick reference table
- Agent-agnostic terminology glossary
- Non-OpenClaw setup guide in README

### Changed
- Claude alias now points to `claude-opus-4-8`; added `claude-fast` for `claude-opus-4-8-fast`
- Poll timeout guard: 10 min for image/text, 100 min for video (matches API limits)
- Persistence file supports `KATANA_STATE_DIR` to separate state from credentials
- Cache write column formatting fixed for models with no cache write pricing

### Fixed
- Text submission auth: curl commands now use single `&&`-chained line (fixes failures on some agents)
- Payload temp files are now cleaned up after each request
- Header auth bug: submit and poll now use consistent two-header format
- `gpt-image-2-max` reference image count: 12 → 10
- `***` literal removed from header format strings

## 1.0.2

### Added
- `grok-build-0-1` — Grok Build 0.1, xAI coding model (256K ctx)
- `claude-opus-4-8` and `claude-opus-4-8-fast` text models
- Flux 1.1 Ultra, Flux Kontext Max/Pro, GPT-5.4/5.5, Claude Opus 4.7/Sonnet 4.6/Haiku 4.5, Grok 4.20/4.20 Multi-Agent, DeepSeek V4 Flash/Pro
- Video media input rules (`video_image_data` fields documented)
- Video custom rules glossary (12 rules from API)
- Common failure cases section
- Text/LLM notes: streaming, vision/multimodal, billing, attestation, refund policy
- Image generation notes: auto aspect ratio, fast/UHD modes, prompt assist
- `thumbnail_silent_video_mp4_url` and `final_frame_image_url` to response handling
- Cache read pricing for 11 models (8 private + qwen3-6-flash, qwen3-6-max-preview, qwen3-6-plus, qwen3-7-max)

### Changed
- Full models.md rebuild with canonical dashed keys throughout
- All model keys migrated to canonical format (e.g. `seedance2` → `seedance-2-0`)
- Price cuts: qwen3-7-max (-50%), deepseek-v4-flash (-30%), qwen3-6-flash (-25%), glm-5-1 (-12%), kimi-k2-6 (-9%), minimax-m2-7 (-13%), qwen3-6-35b-a3b (-7%)

## 1.0.1

### Added
- `pink-image` model — 1 credit, high-speed generalist
- `qwen3-7-max` text model — flagship Qwen, 1M context
- `gemini-3-5-flash` text model — near-Pro at Flash cost, multimodal
- `gpt-image-2-max` image model — MAX variant, 28 cr, QHD output
- `gemini-omni` video model — Google video, 4-10s, 5 ref images
- `gemini-omni-v2v` video model — V2V with `video_list` input
- Text alias `qwen-max`, `gemini-35-flash`; video aliases `gemini-omni`, `gemini-v2v`
- V2V (video-to-video) workflow section in `workflows/video.md`
- Custom rules: `video_required`, `video_offset_allowed`, `input_video_drives_length`
- `video_image_data.video_list` parameter for V2V models
- Text workflow note: API defaults to 16K max_tokens when omitted
- Video continuation workflow (chain videos from last frame)
- Streaming, E2EE, and audio input support documented
- Image editing trigger phrases

### Changed
- Removed `katana.sh` — skill is now pure markdown with inline curl patterns
- Migrated to canonical model keys (e.g. `gpt-image-2` instead of `gpt2image`)
- DRY cleanup — pricing, aliases, and protocols in single source files
- Uniform `.` source credential loading — single method for all agent platforms
- Security: concurrency guard (one request in flight, concurrent needs approval)
- Security: upstream errors are terminal with suggest/approve flow
- Security: credential security rules — never display secrets in tool output
- `python3` added to required bins
- `image_urls` vs `reference_assets` warning — `reference_assets` silently ignored on image requests
- ffmpeg `-c copy` compat warning — stream copy preserves source codec, may break playback
- Pre-publish DRY: removed duplicate alias table from `workflows/text.md`, deduplicated pre-submission paragraphs
- `seedance-lite` canonical key fix (was `seedance-lite-seedancelite`)

### Removed
- `bash` requirement (only `curl` needed now)
- Duplicated alias tables from workflow files
- `katana.sh` helper script (VirusTotal false positive)

## 1.0.0

### Added
- Initial public release
