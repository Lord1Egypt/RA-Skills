# lovart engine details

Lovart is a design agent that plans, picks models and calls tools by itself. This skill runs
`scripts/lovart_agent.py`. HTTP calls are in `scripts/lovart_client.py` and the local project list
is in `scripts/lovart_state.py`. Those files are the readable v1.1.1 client from the official MIT
project [lovartai/lovart-skill](https://github.com/lovartai/lovart-skill), split so each file can be
reviewed. Standard library only. It talks to `lgw.lovart.ai` with AK/SK signatures. Trust only that
upstream project and `www.lovart.ai/docs`; the "API docs" on `lovart.pro` and `lovart.info` are
AI-generated imitations.

## Usage

```bash
node scripts/lovart.mjs --out cat.png --prompt "a cyberpunk cat in neon city" --json
node scripts/lovart.mjs --out shot.png --aspect 2:3 --ref product.jpg --prompt "Re-photograph this exact build on linen, macro, warm light" --json
```

`--ref` uploads to the Lovart CDN and attaches the URL; `--mode thinking` uses the deeper mode;
`--lv` points at an optional wrapper. Failure `error_kind` values: `invalid_args`, `not_configured`
(no client or credentials), `timeout`, `no_image` (text reply only), `error`.

## Wrapper

`scripts/lovart.mjs` runs `scripts/lovart_agent.py`. It reads the file `$HOME/.lovart/env` (or
`LOVART_ENV`) as text and checks that the file is owner-only. Only `LOVART_ACCESS_KEY`,
`LOVART_SECRET_KEY`, and `LOVART_BASE_URL` are kept. A mode such as `644` is refused; `600` is
accepted. When the mode cannot be read, the client still runs, so a real "no credits" response is
not hidden behind a failed permission check. An optional wrapper,
`examples/lovart-lv.example.sh` in the git repository (not shipped in the installed skill), runs the same entry file and copies only those three
names. It does not source the file. It uses `stat -c %a` when GNU stat is available, and
`stat -f %Lp` otherwise. Do not clone or execute a remote copy. See [SETUP.md](../SETUP.md).

During `chat`, if the remote project's current name is empty, `Untitled`, or a short prefix of the
project id, the client renames that project to the first 30 characters of the prompt. A project
that already has another name is left unchanged. `project-add` and `project-rename` update
`$HOME/.lovart/state.json` and, when access keys are present, also send a rename to Lovart. Do not
run those two commands unless the user asked to add or rename that project.

Underlying CLI: `lv query-mode` (check the key and billing mode), `lv upload --file x.jpg`, `lv chat
--prompt ... --attachments <URL> --json --download --output-dir out/`, `lv set-mode
--fast|--unlimited`.

## Credits

`fast` mode spends credits and never queues. `unlimited` mode is free only for whitelisted models
and queues; some whitelist entries expire within a day, so do not plan around them. Nano Banana Pro
costs about 14 credits per image.

## Models

Default `generate_image_nano_banana_pro` (2K). Others: `generate_image_nano_banana_2`,
`generate_image_seedream_v4_5`, `generate_image_gpt_image_2`, `generate_image_midjourney`,
`generate_image_flux_2_max`, `generate_image_ideogram_v4`, `generate_image_qwen_image3_pro`. The
full list is in the repo README or `alias_list` from `lv query-mode`.

## Tested pitfalls

- There is no aspect-ratio parameter; `--aspect` only goes into the prompt, so check the size
  afterwards when it matters.
- One thread runs one job at a time and a second submit returns 409; the script opens a new thread
  every call, so calls can run in parallel.
- `status: done` can come back without an image (moderation, timeout, no tool call); trust
  `generation_succeeded`.
- Rate limits: chat/send 60 per minute and 600 per hour; queries 300 per minute.
- Image-to-image replaces third-party brand cards and watermarks in the reference, which helps
  product reshoots.
