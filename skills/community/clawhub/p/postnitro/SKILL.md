---
name: postnitro
description: Create on-brand social media carousels, single-image posts, and short videos, and schedule them to LinkedIn, Instagram, TikTok, and Threads from a single command. Turn a topic, article, or X thread into a finished multi-slide post, image, or video (with an optional audio track) — or import your own content — then publish or draft it automatically. Fully scriptable (JSON in, JSON out), so an AI agent can run the entire create-to-schedule workflow. Use this skill whenever the user wants to create a carousel, image post, video, reel, slide post, or multi-slide content, repurpose an article, blog post, or X thread into slides or a video, or automate and schedule social media posts. Use it to create and schedule content through PostNitro, not as a general social-media strategy advisor. Requires a PostNitro API key.
homepage: https://postnitro.ai
metadata: {"openclaw":{"emoji":"🎠","primaryEnv":"POSTNITRO_API_KEY","requires":{"bins":[],"env":["POSTNITRO_API_KEY"]}}}
---

# PostNitro — Create & Schedule Social Posts

PostNitro creates on-brand social media posts — multi-slide carousels, single images, and short videos — and schedules them across LinkedIn, Instagram, TikTok, and Threads. This skill drives it from the command line, so an agent can take a topic, article, or your own content and produce a finished, scheduled post in one workflow. Every command is JSON in / JSON out — safe to script and chain.

## Setup

1. Install the CLI:
   ```bash
   npm install -g @postnitro/cli
   ```
2. Sign up at https://postnitro.ai and subscribe to a plan — the Embed API requires a **paid subscription** (no free tier). Then generate an API key at account settings → **Embed** → Generate API Key.
3. Authenticate (in order of precedence: `--api-key` flag → env var → saved config):
   ```bash
   postnitro auth set-key pn-xxxx        # persists to ~/.postnitro-cli/config.json
   export POSTNITRO_API_KEY="pn-xxxx"    # or use an env var
   ```
4. Save defaults so you don't repeat template/brand/preset IDs on every call (the CLI's alternative to per-call flags — no env vars needed):
   ```bash
   postnitro defaults set --template-id <id> --brand-id <id> --preset-id <id> --response-type PDF
   ```

| Env var | Required | Purpose |
|---------|----------|---------|
| `POSTNITRO_API_KEY` | Yes* | API key (*unless passed via `--api-key` or saved with `auth set-key`) |

> **Key rule:** `carousel generate`/`import` return an **`embedPostId`** (the async job). To *schedule* the result you need its **`designId`** (from the `--wait` output or `carousel output`). Never pass an `embedPostId` to `schedule`.

> **Security:** `auth set-key` stores your API key in plaintext at `~/.postnitro-cli/config.json`. Restrict its file permissions and avoid shared or untrusted machines; run `auth clear` to remove it. This skill runs **no background processes, cron jobs, or startup scripts** — the only local state is the API key and saved defaults, both disclosed above.

> **When NOT to use:** as a general social-media strategy advisor when no content is being produced. *(PostNitro composes with other tools — e.g., create a carousel here, then schedule it elsewhere — so pairing it with another scheduler is fine.)*

## Core Workflow

Every create command is asynchronous — `--wait` handles the polling and returns the finished output (including `designId` and `editorUrl`) in one call.

### 1. Create a post

Two independent choices decide which command you run:

- **Post type** — a multi-slide `carousel`, a single `image`, or a `video`.
- **Content source** — let AI write it (`generate`) or supply your own (`import`).

That's six commands:

| | `generate` (AI writes it) | `import` (you supply content) |
|---|---|---|
| **`carousel`** (multi-slide) | `postnitro carousel generate` | `postnitro carousel import` |
| **`image`** (single) | `postnitro image generate` | `postnitro image import` |
| **`video`** (slides become scenes) | `postnitro video generate` | `postnitro video import` |

All six take `--template-id`/`--brand-id` (from flags or saved defaults) plus the modifiers in step 2, and every result includes the **`designId`** (needed to schedule) and an **`editorUrl`**.

#### AI-generated (`generate`)

```bash
postnitro carousel generate \
  --context "5 tips for growing your LinkedIn audience in 2026" \
  --type text \
  --instructions "Professional tone, actionable advice" \
  --wait

# Single image instead — same flags, just the image subcommand
postnitro image generate --context "Announce our new scheduling feature" --wait

# Video — same flags, plus the render length when you want the MP4 back
postnitro video generate --context "3 habits that make remote teams faster" \
  --response-type MP4 --video-duration 30 --wait
```

**`--type` values:**
- `text` — `--context` is the topic/text to turn into a post
- `article` — `--context` is an article URL to extract and convert
- `x` — `--context` is an X (Twitter) post/thread URL

`generate` also needs an AI preset (`--preset-id`, or a saved default).

#### Import your own content (`import`)

```bash
# Carousel — slides is an ARRAY of typed slides (inline --slides overrides --file)
postnitro carousel import --slides '{"slides":[
  {"type":"starting_slide","heading":"Your Title","description":"Intro text"},
  {"type":"body_slide","heading":"Key Point","description":"Details here"},
  {"type":"ending_slide","heading":"Take Action!","cta_button":"Learn More"}
]}' --wait
postnitro carousel import --file ./slides.json --wait

# Single image — slide is a SINGLE OBJECT (not an array), via --slide
postnitro image import --slide '{"heading":"Welcome!","sub_heading":"Subtitle","cta_button":"Learn more"}' --wait

# Video — same slide ARRAY as a carousel; each slide is a scene
postnitro video import --file ./scenes.json --response-type MP4 --video-duration 30 --wait
```

- **Carousel** (`--slides`, array): exactly 1 `starting_slide` (first), ≥1 `body_slide`, exactly 1 `ending_slide` (last); `heading` required on every slide. Run `postnitro carousel import-template` for the schema. Ready-to-use: [examples/import-default.json](examples/import-default.json), [examples/import-infographics.json](examples/import-infographics.json).
- **Image** (`--slide`, one object): fields `heading` (required), `sub_heading`, `description`, `cta_button`, `image`, `background_image` (plus infographic — see step 2). Sending an array here is rejected. Run `postnitro image import-template` for the schema.
- **Video** (`--slides`, array): the carousel rules exactly — each slide becomes a scene, in order. Run `postnitro video import-template` for the schema and the render settings.

### 2. Options for any create command

These layer onto any of the four commands above (and onto `generate-and-schedule`).

#### Output format — `--response-type PDF | PNG | DESIGN | MP4`

Default `PDF` (single file URL). `PNG` returns one URL per slide. `DESIGN` **skips rendering** — no file is produced; you get just the `designId` + `editorUrl`, the fastest option when you only need to schedule or edit.

`MP4` (single video URL) belongs to `video` only, and a video accepts **nothing but** `MP4` or `DESIGN` — never `PDF`/`PNG`. Video commands default to `DESIGN`, so pass `--response-type MP4` when you want the file. `MP4` also can't be stored via `defaults set`, since it would break carousel and image calls.

#### Video length & audio — `video` only

```bash
postnitro audio list                       # find an audio track's ID
postnitro video generate --context "..." --response-type MP4 --video-duration 30 --audio-id <audioId> --wait
```

- `--video-duration <seconds>` — the **whole video's** length, not per scene. At least 5 and under 60. **Required** with `--response-type MP4`; optional for `DESIGN` (set it later in the editor).
- `--audio-id <id>` — an audio **ID** from `postnitro audio list`, never a URL. Omit for a silent video. Uploading audio happens in the PostNitro app; the CLI can list (`audio list`) and delete (`audio delete <id> --yes`) but not upload.
- Rendering a video takes longer than a carousel — typically 15-45s with `--wait` and `MP4`, longer for designs with animations or GIFs.
- These same settings are reused automatically when the video is later scheduled as a reel.

#### AI image generation — `--generate-images` (any post type, any source)

Opt in to have AI generate images and bake them into the design before rendering. Works on **all six** create commands (and both one-shot commands) — carousels, images, and videos alike. Requires an `--image-context` brief:

```bash
postnitro carousel generate --context "How scheduling saves marketers time" \
  --generate-images --image-context "upbeat and professional, product-focused" \
  --image-placement auto --image-strategy all --wait
```

- `--image-context <text>` — **required** when generating images: a short visual brief for the image prompts
- `--image-placement auto|background|in-line` (default `auto` — AI decides per slide)
- `--image-strategy strategic|all` (`strategic` ≈ 50% of slides, default; `all` = every eligible slide)

**Best-effort:** the post still completes if images fail or aren't permitted. With `--wait`, the result carries an `imageGeneration` field (the `GENERATE_IMAGES` step); if its `status` is `FAILED`, its `message` explains why (e.g. free plan can't generate AI images, or the org is over its AI-image quota). AI images bill against the org's **separate AI-image quota**, not the post's slide credits, and add latency. Without `--wait`, the same step shows up in `status` logs.

#### Infographic layout — `import` only

On either `import` command, set `layoutType: "infographic"` on a slide (with a `layoutConfig`) to render data columns (max 3) instead of an image. Every column and content item needs a caller-provided `id`, and each item `description` is an HTML string. See `carousel import-template` / `image import-template` for the full schema.

### 3. Check status / get output (only if you didn't use `--wait`)

```bash
postnitro carousel status <embedPostId>   # progress + step logs; poll until COMPLETED
postnitro carousel output <embedPostId>   # final file URL(s) + designId + editorUrl
```
(`image status` / `image output` and `video status` / `video output` work identically for those post types.)

Output is a PDF (single URL), PNG (one URL per slide), or MP4 (single URL) in `data`, plus the `designId` and `editorUrl`. Those can be handed to another tool — e.g. a different scheduler — to publish on platforms PostNitro doesn't cover. With `--response-type DESIGN` there's no rendered file, so `data`/`mimeType`/`outputType` are omitted (you still get `designId` and `editorUrl`).

### 4. Schedule the design to social accounts

```bash
postnitro social list   # get account IDs + platforms

postnitro schedule create \
  --status SCHEDULED \
  --scheduled-at "2026-12-31T13:00:00Z" \
  --design-id <designId> \
  --selected-accounts '["<socialAccountId>"]' \
  --linkedin-post-settings '{"postType":"document","postTitle":"5–90 char title"}' \
  --post-content '{"common":"Caption with #hashtags"}'
```

### 5. One-shot: create + schedule

Create and schedule in a single call — `generate-and-schedule` (AI writes it) or `import-and-schedule` (your own content). Both accept the schedule flags from step 4, `--post-type CAROUSEL|IMAGE|VIDEO` (with `--video-duration`/`--audio-id` for a video), and the AI-image options from step 2. If creation succeeds but scheduling fails, the error returns the `designId` so you can retry `schedule create` without re-creating (or re-spending credits).

```bash
# AI-generated
postnitro generate-and-schedule \
  --context "topic" --type text \
  --status SCHEDULED --scheduled-at "2026-12-31T13:00:00Z" \
  --selected-accounts '["<socialAccountId>"]' \
  --linkedin-post-settings '{"postType":"document","postTitle":"..."}' \
  --post-content '{"common":"..."}'

# Your own content — --slides (carousel array) or --slide (single image); --slides-file for a file.
# (Here --file is the SCHEDULE body, so slides come from --slides / --slides-file.)
postnitro import-and-schedule \
  --slides '{"slides":[ ... ]}' \
  --status SCHEDULED --scheduled-at "2026-12-31T13:00:00Z" \
  --selected-accounts '["<socialAccountId>"]' \
  --post-content '{"common":"..."}'
```

## Common Patterns

### Pattern 1: LinkedIn thought-leadership carousel
```bash
postnitro carousel generate \
  --context "5 mistakes startups make with their LinkedIn strategy and how to fix each one" \
  --type text --instructions "Professional but conversational. One clear takeaway per slide." --wait
```

### Pattern 2: Repurpose a blog post
```bash
postnitro carousel generate --context "https://yourblog.com/posts/social-media-strategy-2026" \
  --type article --instructions "Extract the 5 most actionable points. Keep slide text concise." --wait
```

### Pattern 3: Repurpose an X thread
```bash
postnitro carousel generate --context "https://x.com/username/status/1234567890" \
  --type x --instructions "Maintain the original voice and key points" --wait
```

### Pattern 4: Data-driven infographic carousel
Import slides with `layoutType: "infographic"` body slides — see
[examples/import-infographics.json](examples/import-infographics.json).

### Pattern 5: Video reel with an audio track
```bash
AUDIO=$(postnitro audio list | jq -r '.audios[0].id')
postnitro video generate --context "3 habits that make remote teams faster" --type text \
  --response-type MP4 --video-duration 30 --audio-id "$AUDIO" --wait
```
A reel reuses the video's own duration and audio when scheduled, so `--post-settings` is
optional — omit it and the API fills it in (falling back to 30s with no audio).

### Pattern 6: Audit one account's schedule
```bash
LINKEDIN=$(postnitro social list | jq -r 'first(.accounts[] | select(.platform=="linkedin").id)')
postnitro schedule list --from 2026-09-01 --to 2026-09-30 --accounts "$LINKEDIN"
```
`--accounts` filters the **posts**, not the accounts inside them: a post targeting LinkedIn
and Instagram is returned when you filter by either, and it still lists both accounts.

### Pattern 7: Generate → schedule to LinkedIn
```bash
DID=$(postnitro carousel generate --context "5 remote work habits" --type text --wait | jq -r .designId)
LINKEDIN=$(postnitro social list | jq -r 'first(.accounts[] | select(.platform=="linkedin").id)')
postnitro schedule create --status SCHEDULED --scheduled-at "2026-12-31T13:00:00Z" \
  --design-id "$DID" --selected-accounts "[\"$LINKEDIN\"]" \
  --linkedin-post-settings '{"postType":"document","postTitle":"5 remote work habits"}' \
  --post-content '{"common":"New carousel 🚀 #remotework"}'
```

### Pattern 6: Batch scheduling
```bash
DATES=("2026-02-14T09:00:00Z" "2026-02-15T09:00:00Z")
TOPICS=("Monday motivation 💪" "Tuesday tips 💡")
for i in "${!DATES[@]}"; do
  postnitro generate-and-schedule --context "${TOPICS[$i]}" --type text \
    --status SCHEDULED --scheduled-at "${DATES[$i]}" \
    --selected-accounts '["<socialAccountId>"]' \
    --linkedin-post-settings '{"postType":"document","postTitle":"Daily post"}'
done
```

## Content Strategy Tips

- **LinkedIn**: professional tone, actionable insights, 6–10 slides, clear CTA. PDF carousels post as `postType: "document"` (needs a 5–90 char `postTitle`).
- **Instagram**: visual-first, concise text, 5–8 slides, storytelling arc. `postAsStory` for stories.
- **TikTok**: trendy, punchy, 4–7 slides, hook on slide 1.
- **X / Threads**: data-driven, 3–6 slides, provocative opening.

## Common Gotchas

1. **Not authenticated** — run `postnitro auth status`; set a key before anything else.
2. **Scheduling with `embedPostId`** — use the **`designId`** from `--wait`/`carousel output`, never the `embedPostId`.
3. **`Scheduled at is in the past`** — `--scheduled-at` must be a future ISO-8601 datetime with a trailing `Z`.
4. **Invalid inline JSON** — wrap JSON flags in single quotes; the CLI validates before any network call.
5. **`Missing --brand-id ... multiple candidates`** — pass the ID or save a default with `defaults set`.
6. **LinkedIn `document` rejected** — `postType:"document"` needs a 5–90 char `postTitle`.
7. **Empty post** — a scheduled post needs either `--design-id` or non-empty `--post-content`.
8. **Destructive commands** — `social disconnect` and `schedule delete` require `--yes`.
9. **`SCHEDULED` publishes live** — use `DRAFT` when unsure; confirm time/account with the user first.
10. **`responseType`** — the CLI defaults to `PDF` (pass `--response-type PNG` for individual slide images, or `DESIGN` to skip rendering and only create the design). Note: the underlying API now defaults to `DESIGN` when omitted, but the CLI always sends `PDF` explicitly, so CLI behavior is unchanged.
11. **Credits vary** — AI generation ≈ 2 credits/slide; content import ≈ 1 credit/slide. Warn before large batches.

## Credits & Pricing

The Embed API requires a **paid subscription** — there is no free tier, and free accounts cannot call the API. See **https://postnitro.ai/plans** for current plans and credit allowances.

Approximate usage cost (observed):
- Content import: ~1 credit per slide
- AI generation: ~2 credits per slide

## Supporting Resources

**In this skill:**
- [references/cli-reference.md](references/cli-reference.md) — complete command, platform-settings, and slide-schema reference
- [examples/EXAMPLES.md](examples/EXAMPLES.md) — ready-to-use import & schedule JSON (`import-default.json`, `import-infographics.json`, `schedule-post.json`)

**Full project docs (GitHub):**
- [README](https://github.com/postnitro/postnitro-agent#readme) — full command reference
- [QUICK_START.md](https://github.com/postnitro/postnitro-agent/blob/main/QUICK_START.md) — zero to a scheduled carousel in minutes
- [HOW_TO_RUN.md](https://github.com/postnitro/postnitro-agent/blob/main/HOW_TO_RUN.md) — install & run methods
- [PLATFORM_SETTINGS.md](https://github.com/postnitro/postnitro-agent/blob/main/PLATFORM_SETTINGS.md) — platform settings schemas
- [FEATURES.md](https://github.com/postnitro/postnitro-agent/blob/main/FEATURES.md) — full feature list
- Per-command help: `postnitro <command> <subcommand> --help`

## Quick Reference

```bash
# Auth (do this first)
postnitro auth set-key pn-xxxx | postnitro auth status | export POSTNITRO_API_KEY=pn-xxxx

# Discover + defaults
postnitro template list | brand list | preset list | social list
postnitro defaults set --template-id <id> --brand-id <id> --preset-id <id> --response-type PDF

# Create (async — use --wait; result has designId + editorUrl)
# --response-type PDF|PNG|DESIGN (DESIGN skips rendering; CLI default is PDF)
# Optional AI images (any generate/import): --generate-images --image-context "brief" [--image-placement auto|background|in-line] [--image-strategy strategic|all]
postnitro carousel generate --context "topic|url" --type text|article|x [--instructions "..."] --wait
postnitro carousel import (--slides '{"slides":[...]}' | --file ./slides.json) --wait
postnitro carousel status <embedPostId>        # if not using --wait
postnitro carousel output <embedPostId>        # file URLs + designId + editorUrl

# Single-image posts (mirror carousel; import takes ONE slide object, not an array)
postnitro image generate --context "topic|url" --type text|article|x --wait
postnitro image import (--slide '{"heading":"..."}' | --file ./slide.json) --wait

# Schedule (date REQUIRED + future; use designId, not embedPostId)
postnitro schedule create --status SCHEDULED|DRAFT --scheduled-at "<iso>" --design-id <id> \
  --selected-accounts '["<id>"]' --linkedin-post-settings '{"postType":"document","postTitle":"..."}' \
  --post-content '{"common":"caption"}'
postnitro schedule list --from "<date>" --to "<date>" | get <id> | delete <id> --yes

# One-shot: create + schedule (both take --post-type + AI-image flags)
postnitro generate-and-schedule --context "topic" --status SCHEDULED --scheduled-at "<iso>" ...
postnitro import-and-schedule --slides '{"slides":[...]}' --status SCHEDULED --scheduled-at "<iso>" ...   # or --slide for image
```

## Tips for the Agent

- Always confirm authentication (`postnitro auth status`) before running any other command. Never fabricate an API key — ask the user.
- Prefer `--wait` so one call returns the finished output and `designId`.
- Discover IDs with the `list` commands; save workspace defaults with `defaults set` so later calls stay short.
- **Schedule with the `designId`, not the `embedPostId`.**
- For `--type article`/`x`, `--context` must be a URL. For plain text, use `--type text`.
- `responseType` defaults to PDF in the CLI — pass `--response-type PNG` for individual slide images, or `DESIGN` to skip rendering when you only need the `designId`/`editorUrl` (e.g. for scheduling).
- `--scheduled-at` must be a **future** ISO-8601 datetime (trailing `Z`).
- `status: SCHEDULED` creates a **live** post that will publish — confirm the time and account with the user, or use `DRAFT` when unsure.
- Parse stdout as JSON; on failure read `.error.message` from stderr and fix the inputs.
- Warn about credit costs before large batches (AI generation is ~2× the cost of import).
- If the user doesn't specify a platform, suggest LinkedIn (most common carousel use case) and remember PDF carousels post there as `document`.
