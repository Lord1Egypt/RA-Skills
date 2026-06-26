# Hopola (ClawHub Release)

## Overview

Hopola is an end-to-end skill pipeline for:

- web research
- image generation
- video generation
- 3D model generation
- logo design
- product image generation
- asset upload
- Markdown report delivery

## Architecture

- Main orchestrator: `SKILL.md`
- Version file: `VERSION.txt`
- Subskills: 8 focused units under `subskills/`
- Design intake playbook: `playbooks/design-intake.md`
- Scripts: release validation and packaging under `scripts/`
- Assets: logo, cover, flow chart under `assets/`

## Secure Key Design

- Users must provide `OPENCLOW_KEY` via environment variable.
- If `OPENCLOW_KEY` is missing, the workflow must stop at `precheck` with `GATEWAY_KEY_MISSING` before any Gateway generation call.
- Upload policy endpoint uses `MAAT_TOKEN_API` (default `https://strategy.stariidata.com/upload/policy`).
- Legacy endpoint envs (`MEITU_TOKEN_API`, `NEXT_PUBLIC_MAAT_TOKEN_API`, `NEXT_PUBLIC_MEITU_TOKEN_API`) remain backward-compatible.
- `MAAT_TOKEN_API_ALLOWED_HOSTS` constrains trusted upload policy hosts and includes `strategy.stariidata.com` by default.
- `OPENCLAW_REQUEST_LOG` is disabled by default (`0`) and should be enabled only for temporary debugging.
- `config.template.json` keeps only `key_env_name` and an empty `key_value`.
- Release validation blocks packaging if plaintext keys are detected.

## Quick Start

```bash
cd .trae/skills/Hopola
python3 scripts/check_tools_mapping.py
python3 scripts/validate_release.py
python3 scripts/build_release_zip.py
```

## Routing Policy

- Generation tasks use preferred fixed tool first.
- If unavailable, fallback discovery uses `/api/gateway/mcp/tools`.
- If users provide only session-uploaded images (without public URLs), Hopola resolves them first via upload subskill and backfills accessible URLs before cutout/product-image/3D stages.
- In product-image stage, when `product_image_url` is non-URL input (local path, attachment reference, markdown image source), Hopola must upload first and block generation until URL backfill succeeds.
- Product-image stage requires `source_image_confirmed=true`, and the source must be user-provided or explicitly user-confirmed as the real product image; otherwise return `PRODUCT_IMAGE_UNCONFIRMED_SOURCE` and stop before tool call.
- Before product-image generation call, Hopola runs prechecks for tool availability, source URL accessibility, and required args completeness (`image_list`, `prompt`, `output_format`, `size`).
- For product-image generation, `image_list` must contain only the confirmed `product_image_url`; placeholder, proxy, or generated substitutes are forbidden.
- If any precheck fails, Hopola returns unified `structured_error` (`code`, `stage`, `message`, `details`, `retry_suggestions`) for direct OpenClaw retry handling.

## Upload Policy

- Upload stage uses MAAT direct upload only via `scripts/maat_upload.py`.
- Gateway upload endpoint is not used as primary or fallback in current strategy.
- Returned URLs are validated for accessibility and only stable reachable links are delivered.
- Endpoint resolution follows `MAAT_TOKEN_API > legacy envs > default endpoint` with host-level allowlist checks.
- Audit output records endpoint source and host without leaking token/policy/signature values.

## Release Deliverables

- `Hopola-Skills/hopola-clawhub-v<version>-*.zip`
- `README.zh-CN.md`
- `README.en.md`
- `RELEASE.md`
