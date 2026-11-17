---
name: huajing-image-gen
description: >-
  Generate images through a local Huajing (AI Image Studio) server. Use when
  the user asks to create or generate an image, polish an image prompt, or
  look up previously generated images. Supports text-to-image with polling,
  batch count, size, negative prompt, and provider/model selection. Requires
  the local Huajing server (default http://127.0.0.1:4173) and Node 18+.
metadata:
  openclaw:
    requires:
      bins:
        - node
---

# Huajing Image Generation

Drive a locally running [Huajing (AI Image Studio)](https://gitee.com/starry-sea-1412/ai-image-studio) server
to generate images. Huajing manages your own image-model providers (OpenAI-compatible
relays, chat-based image adapters, etc.) and stores every generated image in a local
gallery, so generation is cheap to retry and fully auditable.

## Setup

1. Start the Huajing server (single instance per machine):
   - Windows: run `start.bat` in the Huajing repo, or `npm start`.
   - Any OS: `npm start` (listens on `127.0.0.1:4173` by default).
2. Add at least one image provider in the Huajing UI (Service & Models page):
   base URL + API key + image model.
3. Optional environment overrides:
   - `HUAJING_BASE_URL` — server base URL, default `http://127.0.0.1:4173`.
   - `HUAJING_DATA_DIR` — Huajing `data/` directory; when set, results include
     absolute local file paths instead of only HTTP URLs.

## Usage

All commands print JSON on stdout and human-readable diagnostics on stderr.
Exit codes: `0` success, `1` generation failed, `2` server unreachable, `3` bad usage.

Check the server before doing anything else:

```bash
node {baseDir}/scripts/huajing.mjs health
```

Generate an image (blocks until the image is done, polling internally):

```bash
node {baseDir}/scripts/huajing.mjs generate \
  --prompt "a tiny red paper crane on a wooden desk, soft window light" \
  --size 1024x1024 --count 1 --timeout 300
```

Options: `--prompt` (required), `--size` (WxH, default `1024x1024`),
`--count` (1–4), `--provider` (provider id or case-insensitive name; default:
first enabled provider with an image model), `--model` (override the provider's
default image model), `--negative` (negative prompt), `--timeout` seconds (default 300),
`--plain` (human-readable output instead of JSON).

Polish a rough prompt into a richer one using the provider's prompt model:

```bash
node {baseDir}/scripts/huajing.mjs polish --prompt "一只纸鹤" --provider <id-or-name>
```

Search the local gallery for previously generated images:

```bash
node {baseDir}/scripts/huajing.mjs gallery --limit 5 --query "crane"
```

## Notes

- If `generate` exits with code `2`, the server is not running — tell the user
  to start it with `start.bat` / `npm start` in the Huajing repo.
- If generation fails with a provider error (exit code `1`), the error text from
  the upstream model service is included in the JSON `error` field; retrying with
  a different `--provider` usually helps.
- All generated images are kept in the local gallery (`gallery` subcommand), so
  you can re-reference earlier results without regenerating.
