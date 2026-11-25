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

## Client selection and billing

The selection order is `--lv`, `LOVART_LV`, then an existing `~/tools/lovart-skill/lv`.
The fallback is `scripts/lovart_agent.py` with AK/SK from the environment or from
`~/.lovart/env` (override with `LOVART_ENV`). The shipped client path reads that file as text,
refuses group or other write access, and warns with `chmod 600` guidance if group or others can
read it. The optional example wrapper in the repository retains its owner-only requirements.
See [SETUP.md](../SETUP.md).

Use `node scripts/lovart.mjs --query-mode --json` to see `auth`, `billing_mode` and
`unlimited_models` without generating. The generation command checks mode before uploading
or generating and warns if mode is fast or the selected model is outside the unlimited
whitelist. Without `--require-free`, it proceeds and spends credits in those cases.
`--require-free` stops with `would_spend_credits`.
An unverifiable billing query stops with `billing_mode_unknown`. The script never switches
mode. The generation JSON identifies the client as `lv-wrapper` or `shipped-client` and
reports the queried billing mode.

During `chat`, if the remote project's current name is empty, `Untitled`, or a short prefix of the
project id, the client renames that project to the first 30 characters of the prompt. A project
that already has another name is left unchanged. `project-add` and `project-rename` update
`$HOME/.lovart/state.json` and, when access keys are present, also send a rename to Lovart. Do not
run those two commands unless the user asked to add or rename that project.

The underlying wrapper supports `lv query-mode`, `lv upload --file x.jpg` and
`lv chat --prompt ... --attachments <URL> --json --download --output-dir out/`.

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
