---
name: makemidas
description: Generate AI images and short videos with the MakeMidas CLI (Nano Banana, GPT Image, Seedream, Flux, Seedance, Kling, Veo, Wan…), from a prompt, reference images or a first and last frame, and save them to disk; and render exact-text layouts from MakeMidas HTML templates (Open Graph / link preview images, quote cards, announcement posts, product promos, stat cards, video title cards, lower thirds) as PNG, WebP, MP4 or transparent MOV. Use when the user asks to generate, draw or render an image, illustration, photo, product shot, cover or mockup, to make an OG image, quote card, title card or lower third, to animate a picture, or to make a short video clip, and wants files on their computer; also for "生成图片", "画一张", "做个视频", "图生视频", "做封面图", "字幕条". Spends the user's MakeMidas credits; the first template images each day are free.
license: MIT
metadata:
  openclaw:
    requires:
      bins:
        - node
    homepage: https://makemidas.com/developers
---

# Generate images and videos with MakeMidas

The `makemidas` CLI sends a prompt to the user's MakeMidas account, waits for
the result and saves the files where you run it. Results (file paths) go to
stdout, progress to stderr. Every command takes `--json`.

## 1. Make sure the CLI runs

```bash
makemidas --version
```

If it isn't installed, use `npx -y @makemidas/cli` in place of `makemidas`
everywhere below (Node.js 20+). Ask the user before running
`npm i -g @makemidas/cli`.

## 2. Make sure the user is signed in

```bash
makemidas auth status --json
```

Exit code 3 means not signed in. Either:

- run `makemidas auth login`: it opens the browser, where the user signs in
  and allows "MakeMidas CLI", and waits up to 5 minutes. Tell the user to
  approve it in the browser; if your shell times out sooner, run it in the
  background and check `auth status` after; or
- ask the user for an API key (Settings → API keys on makemidas.com) and run
  with `MAKEMIDAS_API_KEY` set in the environment. Never write the key into
  files or the conversation.

## 3. Check credits and pick a model

```bash
makemidas credits --json
makemidas models --json            # or --kind image / --kind video
```

Every generation costs credits. Unless the user asks for something else:
one output, the default (cheapest usable) model, `1:1` for images. Tell the
user what a run will cost when it is more than a few credits (videos,
4K, several outputs). Free accounts get 10 credits a day, the free models
only and watermarked images; videos need a plan or credit pack.

## 4. Generate

```bash
makemidas image "a red fox in fresh snow, golden hour, 35mm film" --aspect 3:2 --json
makemidas image "same fox as a watercolor" --ref fox.png --model <id> --json
makemidas video "the fox looks up and the snow starts falling" --ref fox.png --duration 5 --json
```

- `--model <id>` from `makemidas models`; `--aspect`, `--resolution`
  (`1K|2K|4K` for images, `480p|720p|1080p` for videos), `--count 1-4`.
- `--ref <file|url>` adds a reference image (repeat for more). For videos one
  image is the first frame, two are the first and last frame; `--frame-mode
  reference` uses them as references instead (Seedance).
- `--duration <s>` and `--audio` for videos; `--style <id>` (photo,
  cinematic, film, anime, …); `--enhance` lets MakeMidas expand a short
  prompt.
- `--out <dir>` picks the folder (default: current directory). Files are
  named `makemidas-<id>-<n>.<ext>`; existing files are kept unless `--force`.
- `--no-download` prints signed links (valid one hour) instead of saving.

Images come back in under a minute. Videos take one to several minutes; the
CLI waits (up to `--timeout` minutes, default 15). To avoid blocking your
shell:

```bash
makemidas video "…" --no-wait --json        # prints the id, exit code 7
makemidas get <id> --wait --json            # run in the background
```

With `--json`, `image`, `video` and `get` print the generation
(`{ id, kind, model, status, credits, watermarked, outputs, files }`), where
`files` are the saved paths.

## 5. Exact text layouts: HTML templates

Use a template instead of `makemidas image` when the picture is mostly set
text that has to read exactly as given: a link preview (Open Graph) image, a
quote card, an announcement post, a product promo with price and badge, a
stat card, a video title card or a lower third (a name bar on a transparent
background, to lay over video). AI models misspell text; templates don't.
They render in seconds, take the user's default brand (colors, fonts, logo)
and are never watermarked.

| Template id | For | Sizes | Video |
|---|---|---|---|
| `quote-card` | a quote and its author | square, portrait, story | yes |
| `announcement` | headline, text, button, optional photo | square, portrait, story, landscape | no |
| `og-image` | link preview image (Open Graph) | og, landscape | no |
| `product-promo` | product photo, name, price, sale badge | square, portrait, story | no |
| `title-card` | title screen for videos, chapters, slides | landscape, square, story | yes |
| `lower-third` | name and role bar, transparent | landscape, story | yes |
| `stat-card` | one big number, what it means, its source | square, portrait, story, landscape | yes |

Sizes in pixels: square 1080x1080, portrait 1080x1350, story 1080x1920,
landscape 1920x1080, og 1200x630.

**Price.** Each account renders 10 template images free every UTC day (100
once it has a plan or has bought a credit pack); after that each image costs
1 credit. Template videos have no free allowance: 1 credit per started 5
seconds (2-15 seconds, so 1-3 credits).

The CLI has no template command yet. Use either:

- **MCP**, if the MakeMidas MCP server is connected: `list_templates`
  (fields, sizes, free renders left today), `render_template_image`,
  `render_template_video`, then `get_generation` until a video is done; or
- **the REST API** with `MAKEMIDAS_API_KEY` set (see section 2). Never read
  the CLI's credentials file to get a token.

```bash
H="Authorization: Bearer $MAKEMIDAS_API_KEY"
# Templates, their fields and defaults, and the free renders left today
curl -s -H "$H" "https://makemidas.com/api/v1/templates?category=web"
# Render an image: 201 { generation, credits, quota }
curl -s -H "$H" -H 'Content-Type: application/json' \
  https://makemidas.com/api/v1/renders \
  -d '{"templateId":"og-image","size":"og","values":{"title":"How we cut our cloud bill in half","site":"example.com"}}'
# Render a video: 202 { generation, credits } while it renders
curl -s -H "$H" -H 'Content-Type: application/json' \
  https://makemidas.com/api/v1/video-renders \
  -d '{"templateId":"lower-third","size":"landscape","seconds":6,"format":"mov","values":{"name":"Alex Morgan","role":"Head of Design"}}'
```

- `category` filters the list: `social`, `web`, `promo` or `video`.
  `GET /api/v1/templates/<id>` returns one template.
- `values` maps field ids (from the list) to values; fields left out keep
  their default and `null` clears one. Text, color (`#rrggbb`) and choice
  fields take strings; image fields take `{ "assetId": … }` (from
  `makemidas assets`) or `{ "generationId": …, "index": 0 }` (an image
  generated earlier, e.g. with `makemidas image`).
- Images: `size` is one of the template's sizes (its first when left out),
  or `width` and `height` (200-2048); `scale: 2` doubles the pixels;
  `format` is `png` (default) or `webp`.
- Videos: only templates whose `video` is set; `seconds` 2-15 (the
  template's default when left out); `format` is `mp4` (default) or, for a
  transparent template (`lower-third`), `mov` (ProRes 4444 that keeps the
  transparency). A transparent template in an MP4 sits on `matte`
  (`#rrggbb`, chroma green by default).
- `brandId` picks a brand; left out, the user's default brand applies;
  `null` applies none.
- Download with `makemidas get <generation id> --json` (add `--wait` for a
  video), or fetch `generation.outputs[].url` (signed, valid one hour).
  Errors come back as `{ "error": { "code", "message" } }`; 402 means not
  enough credits, 429 too many at once.

## 6. Use the result

Show the user the saved files (open or embed them if your environment can).
`makemidas list --json` lists recent generations and ids; `makemidas get <id>`
downloads one again.

## Exit codes

| Code | Meaning | What to do |
|---|---|---|
| 0 | done | |
| 2 | bad input (unknown model, unsupported ratio or size, bad file) | fix the command; check `makemidas models` |
| 3 | not signed in or sign-in expired | `makemidas auth login`, or `MAKEMIDAS_API_KEY` |
| 4 | not enough credits, paid model on a free plan, or too many running | show `makemidas credits`; plans at https://makemidas.com/pricing |
| 5 | the model could not make it (credits refunded) | show the error; change the prompt or model before retrying |
| 6 | network or server error | retry once, then report |
| 7 | video still rendering | `makemidas get <id> --wait` |

## Rules

- Generations spend the user's credits. Don't run batches, 4K or videos the
  user didn't ask for; ask first when the cost is unclear.
- Don't generate images of real people without their consent, or content the
  user would not want stored in their MakeMidas account.
- Never print, log or copy tokens, `MAKEMIDAS_API_KEY` or the credentials
  file (`~/.config/makemidas/credentials.json`).
- In ChatGPT, Claude or another MCP client, the MakeMidas MCP server
  (`https://makemidas.com/api/mcp`) does the same without the CLI.
