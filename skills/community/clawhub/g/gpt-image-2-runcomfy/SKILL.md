---
name: gpt-image-2-runcomfy
displayName: "🫧 GPT Image 2 — Pro Pack on RunComfy"
description: >
  GPT Image 2 on RunComfy. GPT Image 2 (OpenAI ChatGPT Images 2.0) is
  the strongest text-rendering image model available — embedded text,
  logos, signage, multilingual typography, and high-fidelity layout.
  This skill calls GPT Image 2 through the RunComfy CLI: `runcomfy run
  openai/gpt-image-2/text-to-image` (or `/edit`). GPT Image 2 has 3
  fixed sizes and supports up to 10 reference images on the GPT Image 2
  edit endpoint. Triggers on "gpt image 2", "gpt-image-2", "ChatGPT
  Images 2", "ChatGPT Image 2", "OpenAI Image 2", "GPT Image", or any
  explicit ask to generate or edit with GPT Image 2.
emoji: "🫧"
homepage: https://www.runcomfy.com
license: MIT
clawdis:
  requires:
    bins:
      - runcomfy
    env:
      - RUNCOMFY_TOKEN
    config:
      - ~/.config/runcomfy
---

# 🫧 GPT Image 2 — Pro Pack on RunComfy

[runcomfy.com](https://www.runcomfy.com/?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy) · [GPT Image 2 text-to-image](https://www.runcomfy.com/models/openai/gpt-image-2/text-to-image?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy) · [GPT Image 2 edit](https://www.runcomfy.com/models/openai/gpt-image-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy) · [docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy)

**GPT Image 2** is OpenAI's ChatGPT Images 2.0 model. This skill generates and edits images with GPT Image 2 hosted on the RunComfy Model API — `runcomfy run openai/gpt-image-2/<endpoint>` from your terminal, no OpenAI API key required.

## What GPT Image 2 is

GPT Image 2 (also called ChatGPT Image 2 or just Image 2) is the second-generation OpenAI image model behind ChatGPT's Image feature, exposed here as a standalone API. Three properties make GPT Image 2 distinct:

- **GPT Image 2 directive precision.** GPT Image 2 follows multi-element prompts, layout cues, and embedded-text instructions more reliably than peers in 2026. When you tell GPT Image 2 to render a specific headline at a specific position, GPT Image 2 does it. This makes GPT Image 2 the right model when **what's on the canvas matters more than how stylized it looks**.
- **GPT Image 2 in-image typography.** GPT Image 2 is the strongest text-rendering image model in the catalog. GPT Image 2 reproduces quoted characters at high fidelity — short headlines, brand marks, multilingual signage (Latin, Cyrillic, Japanese kana, Arabic, etc.). When GPT Image 2 sees `"AURA"` in the prompt, GPT Image 2 renders the literal word.
- **GPT Image 2 composition stability across iterations.** GPT Image 2 holds layout stable when you change one descriptor and keep the rest of the prompt verbatim. This makes GPT Image 2 ideal for refining a single brand asset across rounds without redrafting from zero.

GPT Image 2 has two endpoints in this skill:

- **GPT Image 2 text-to-image** — generate a fresh image from a prompt.
- **GPT Image 2 edit** — modify a reference image (or compose from up to 10 references), with natural-language preservation language ("keep face identity unchanged", "keep the brand mark").

## When GPT Image 2 is the right choice

Pick GPT Image 2 when any of these is true:

- The image needs **embedded text** — labels, signage, headlines, multilingual typography. GPT Image 2 is the strongest option.
- You're producing **brand-safe e-commerce / ad / UI mockup imagery**. GPT Image 2 directive precision shines here.
- You're doing **iterative refinement on a single image** — change one knob, keep composition stable. GPT Image 2 holds layout across rounds.
- You're producing **brand-asset localization** — same source asset, many language variants of the same headline. GPT Image 2 multilingual text rendering makes this fast.
- The user explicitly asked for **GPT Image 2** / **ChatGPT Image 2** / **Image 2** / **OpenAI Image 2** — route to this GPT Image 2 skill regardless.

## Prerequisites

1. **RunComfy CLI** — `npm i -g @runcomfy/cli`
2. **RunComfy account** — `runcomfy login` opens a browser device-code flow.
3. **CI / containers** — set `RUNCOMFY_TOKEN=<token>` instead of `runcomfy login`.

## Endpoints + input schema

GPT Image 2 has two endpoints, same model.

### `openai/gpt-image-2/text-to-image`

The GPT Image 2 generation endpoint.

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `prompt` | string | yes | — | Positive prompt for GPT Image 2. |
| `size` | enum | no | `1024_1024` | GPT Image 2 supports only three sizes: `1024_1024` (1:1), `1024_1536` (2:3 portrait), `1536_1024` (3:2 landscape). |

### `openai/gpt-image-2/edit`

The GPT Image 2 edit endpoint.

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `prompt` | string | yes | — | Natural-language edit instruction for GPT Image 2. |
| `images` | string[] | yes | — | Up to **10 reference images** for GPT Image 2 edit (publicly fetchable HTTPS URLs). |
| `size` | enum | no | `auto` | `auto` (preserve input ratio) or one of the three GPT Image 2 fixed sizes. |

`size=auto` on GPT Image 2 edit preserves input aspect ratio — strongly recommended unless you explicitly want GPT Image 2 to reframe.

## How to invoke GPT Image 2

**GPT Image 2 text-to-image:**

```bash
runcomfy run openai/gpt-image-2/text-to-image \
  --input '{"prompt": "<GPT Image 2 prompt>", "size": "1024_1536"}' \
  --output-dir <absolute/path>
```

**GPT Image 2 edit (single reference):**

```bash
runcomfy run openai/gpt-image-2/edit \
  --input '{
    "prompt": "<GPT Image 2 edit instruction>",
    "images": ["https://..."]
  }' \
  --output-dir <absolute/path>
```

**GPT Image 2 edit (multi-reference, up to 10):**

```bash
runcomfy run openai/gpt-image-2/edit \
  --input '{
    "prompt": "compose subject from image 1 into the room from image 2; match the lighting of image 2",
    "images": ["https://...subject.jpg", "https://...room.jpg"]
  }' \
  --output-dir <absolute/path>
```

The CLI submits the GPT Image 2 request, polls every 2s, fetches the GPT Image 2 result, and downloads any `*.runcomfy.net` / `*.runcomfy.com` URL into `--output-dir`.

For pipe-friendly GPT Image 2 usage:

```bash
runcomfy --output json run openai/gpt-image-2/text-to-image \
  --input '{"prompt":"..."}' --no-wait | jq -r .request_id
```

## Prompting GPT Image 2 — what works

GPT Image 2 responds to specific prompting patterns better than naive prose. Apply these for sharper GPT Image 2 output. Same patterns work on both GPT Image 2 text-to-image and GPT Image 2 edit.

**Be explicit with subject + setting + mood for GPT Image 2.** "A close-up of a matte ceramic water bottle on warm linen, soft window light, neutral background" — three concrete directives — beats "nice product photo of a bottle". GPT Image 2 reads concrete directives well.

**Quote embedded text exactly for GPT Image 2.** GPT Image 2 is the strongest text-rendering model in this class — but only when you put the literal characters in quotes. Long blocks of text degrade GPT Image 2 output. For multilingual typography, name the script: "Japanese kana", "Cyrillic", "Arabic right-to-left". GPT Image 2 will render accordingly.

**Use compositional cues directly.** "rule of thirds", "close-up", "aerial view", "centered subject", "shallow depth of field" — GPT Image 2 understands these as real directives.

**Iterate one attribute at a time on GPT Image 2.** When refining, change one thing per iteration (lighting OR background OR pose OR text) and keep the rest of the GPT Image 2 prompt verbatim. GPT Image 2 holds composition stable across iterations when only one knob moves.

**Don't conflict GPT Image 2 instructions.** "no text" + "the word 'AQUA+' on the label" is incoherent — GPT Image 2 will pick one and you don't control which.

**Don't pile up styles in a GPT Image 2 prompt.** "ukiyo-e + watercolor + 8K + cinematic + minimalist" cancels out in GPT Image 2 output. Pick one or two style anchors max.

For GPT Image 2 **edit** specifically:

- **State preservation goals to GPT Image 2.** "**keep** the person's pose and face identity unchanged", "**keep** the brand mark and typography on the package", "**keep** the overall framing". GPT Image 2 needs to know what NOT to change.
- **Use directional language for GPT Image 2 spatial edits.** "Move the headline from top-right to bottom-center", not "reposition the headline".
- **Multi-ref GPT Image 2**: number the images in the prompt — "subject from image 1, lighting and background from image 2" — and GPT Image 2 will route the cues correctly.

## Where GPT Image 2 shines

| Use case | Why GPT Image 2 |
|---|---|
| **E-commerce product photography** | GPT Image 2 reliable text on labels, brand-safe lighting, consistent across SKUs |
| **High-conversion ads** | GPT Image 2 headline + visual integration in one pass |
| **Brand asset localization** | One source asset → many language variants of the same headline via GPT Image 2 |
| **Signage, posters, packaging mock-ups** | GPT Image 2 text rendering accuracy at multiple scales |
| **UI mockups, scientific illustrations** | GPT Image 2 layout precision and label legibility |

## Sample GPT Image 2 prompts (verified to produce strong results)

**GPT Image 2 text-to-image — product hero:**

```
A minimal hero product still life: a matte ceramic water bottle on warm linen,
soft window light, the word "AQUA+" in clean sans-serif on the label,
subtle rim highlights, e-commerce ready, 8K detail, neutral background
```

**GPT Image 2 text-to-image — multilingual signage:**

```
A small Tokyo café storefront at dusk, warm interior glow,
the sign reads "コーヒー" in bold Japanese kana on a wooden plaque,
shallow depth of field, rule of thirds, cinematic
```

**GPT Image 2 edit — background swap with preservation:**

```
Turn the background into a bright minimal white-to-soft-gray studio sweep
with gentle floor shadow; add a large headline in-image that reads
"OPEN STUDIO" in a bold clean sans-serif, high contrast, centered;
keep the main person or product, pose, and face identity unchanged
```

## GPT Image 2 FAQ

**What sizes does GPT Image 2 support?** Only three: `1024_1024` (1:1), `1024_1536` (2:3 portrait), `1536_1024` (3:2 landscape). Extreme aspect ratios are auto-resized to the nearest supported GPT Image 2 size.

**How many reference images can GPT Image 2 edit take?** Up to 10. The first image is the primary reference for GPT Image 2; the rest provide auxiliary cues (lighting, background, style).

**Can GPT Image 2 render text in any language?** GPT Image 2 handles Latin, Cyrillic, Japanese kana, Korean Hangul, Arabic, Chinese, and most major scripts. Name the script in the GPT Image 2 prompt for best fidelity.

**Is GPT Image 2 the same as DALL-E?** No. GPT Image 2 is the successor model behind ChatGPT's Image feature; DALL-E was the predecessor line. GPT Image 2 has stronger directive precision and stronger in-image typography than the DALL-E generation.

**How does GPT Image 2 compare to GPT Image (v1)?** GPT Image 2 is the second-generation model. GPT Image 2 has higher fidelity, stronger text rendering, and better composition stability than GPT Image v1.

**Does GPT Image 2 generate at very high resolution?** GPT Image 2 outputs at the three documented sizes only. For higher-resolution upscaling, post-process the GPT Image 2 output through a separate upscaler.

**How do I reproduce a GPT Image 2 output?** GPT Image 2 doesn't expose a `seed` parameter on this endpoint. For reproducible variants, lock the prompt and re-run.

## Limitations of GPT Image 2

- **GPT Image 2 has only 3 fixed sizes** on text-to-image (and the same 3 + `auto` on GPT Image 2 edit).
- **GPT Image 2 prompt length** caps at a few thousand tokens. Long blocks of embedded text degrade GPT Image 2 output.
- **GPT Image 2 edit multi-image** support is "guidance from up to 10 refs", not ControlNet-style stacks.
- **Photorealism on portraits** is not GPT Image 2's strongest suit — for hyperrealistic portraits, route to a different model.

## Exit codes

The `runcomfy` CLI uses sysexits-style codes:

| code | meaning |
|---|---|
| 0  | GPT Image 2 generation succeeded |
| 64 | bad CLI args |
| 65 | bad input JSON for GPT Image 2 / schema mismatch (e.g. `size: "2048_2048"` would 422) |
| 69 | upstream 5xx |
| 75 | retryable: timeout / 429 |
| 77 | not signed in or token rejected |

Full reference: [docs.runcomfy.com/cli/troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy).

## How it works

1. The skill invokes `runcomfy run openai/gpt-image-2/<endpoint>` with a JSON body matching the GPT Image 2 schema.
2. The CLI POSTs to `https://model-api.runcomfy.net/v1/models/openai/gpt-image-2/<endpoint>` with the user's bearer token.
3. The Model API returns a `request_id`; the CLI polls `GET .../requests/<id>/status` every 2 seconds.
4. On terminal status, the CLI fetches the GPT Image 2 result and downloads any `.runcomfy.net` / `.runcomfy.com` URL into `--output-dir`.
5. `Ctrl-C` while polling cancels the GPT Image 2 request via `POST .../requests/<id>/cancel`.

## What this skill is not

Not a direct OpenAI API client. Not a capability grant — depends on a working RunComfy account.

## Security & Privacy

- **Token storage**: `runcomfy login` writes the API token to `~/.config/runcomfy/token.json` with mode 0600.
- **Input boundary**: the GPT Image 2 prompt is passed as JSON via `--input`. No shell injection.
- **Third-party content**: image URLs are fetched by the RunComfy server. Treat external URLs as untrusted.
- **Outbound endpoints**: only `model-api.runcomfy.net` and `*.runcomfy.net` / `*.runcomfy.com`.
- **Generated-file size cap**: 2 GiB.
