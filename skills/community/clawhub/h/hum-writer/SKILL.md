---
name: hum
description: Your AI content writer for X and LinkedIn. Hum handles the full content lifecycle: crawls your feed sources daily and sends a digest, brainstorms ideas grounded in real research across YouTube, X, Reddit, HN, and the web, then drafts posts in your voice using proven writing styles — from technical storytelling to contrarian takes. Every draft goes through a research → outline → approval loop before writing begins. Once approved, Hum publishes directly via API and manages engagement by drafting replies and suggesting accounts to follow.
---

1. **Init** — `/hum init` sets up the data directory with template files (VOICE.md, CONTENT.md, AUDIENCE.md, CHANNELS.md, knowledge/index.md) and folders. After running init.py, also run `bash setup.sh` from the repo root to create the venv and install Python dependencies. All subsequent scripts require the venv (`venv/bin/python3`).
3. **Refresh feed** — `/hum refresh-feed` fetches your X home feed (via Bird `filter:follows`), configured X profiles, Hacker News, YouTube, and knowledge sources (RSS, sitemaps, YouTube transcripts, podcasts from `knowledge/index.md`) — all via direct APIs with no browser automation. Ranks items, sends a digest to Telegram, saves aggregated data to `feeds.json`
4. **Crawl knowledge** — `/hum crawl` independently crawls knowledge sources defined in `knowledge/index.md`. Saves full articles to `knowledge/<source>/`. Also runs as part of refresh-feed.
5. **Manage sources** — `/hum sources` adds, removes, and lists social/ephemeral feed sources in `sources.json`
5. **Brainstorm** — `/hum brainstorm` researches each content pillar across YouTube, X, Reddit, Hacker News, Polymarket, and web, then saves ideas to `ideas.json`
6. **Learn** — `/hum learn` analyzes feed trends and platform algorithms, updates context files
7. **Manage ideas** — `/hum ideas` shows the pipeline as numbered plain text. Format: `1. ID · Title · platform · status`. One idea per line. No markdown tables, no bullet points, no code blocks.
8. **Review drafts** — `/hum content` lists current saved draft files and generated assets
⚠️ **Always use /hum create and read `VOICE.md` + `content-samples/` when drafting posts. Follow the create flow: research → outline → approval → draft. Do not produce a draft without an approved outline.**
9. **Draft posts** — `/hum create [platform] [type] [idea]` follows a strict 4-step process:
   - **Step 1 — Load context**: read VOICE.md, CHANNELS.md, content-samples/, knowledge/, the idea from ideas.json
   - **Step 2 — Research**: 3-5 web searches (core topic, stats, contrarian, examples, adjacents); build a fact base; present findings
   - **Step 3 — Propose outline**: style selection (with rationale) + hook/angle/structure + research summary; **do NOT write prose yet**; get user approval first; style must be named and justified using STYLES.md
   - **Step 4 — Write**: only after outline is approved; match user's voice from content-samples/; present draft; iterate until approved
   - ⚠️ **Never skip to drafting without research + outline approval** — the full CREATE.md process is mandatory
10. **Refine** — iterate on drafts until approved, then save
11. **Publish** — `/hum publish` posts approved drafts to LinkedIn or X via API scripts
12. **Engage** — `/hum engage` handles follow suggestions, outbound engagement plays, and replies/comments

## Configuration

The skill stores all data in a configurable directory. Set the `HUM_DATA_DIR` environment variable:

```bash
export HUM_DATA_DIR=~/Documents/hum
```

If not set, defaults to `~/Documents/hum`. When running inside OpenClaw, it also reads from `openclaw.json` → `skills.entries.hum.config.hum_data_dir` (or the legacy `data_dir` key for existing installs).

## Data Directory Structure

All user-owned data lives in `<data_dir>`:

| Path | Purpose |
|------|---------|
| `<data_dir>/VOICE.md` | Voice, tone, and writing guidelines |
| `<data_dir>/AUDIENCE.md` | Target audience definition |
| `<data_dir>/CHANNELS.md` | Publishing platforms and rules |
| `<data_dir>/CONTENT.md` | Content pillars with keywords for feed classification |
| `<data_dir>/ideas/ideas.json` | Brainstormed content ideas and brainstorm config |
| `<data_dir>/content/drafts/` | Unpublished drafts (outline → draft → ready) |
| `<data_dir>/content/published/` | Drafts moved here after successful publish |
| `<data_dir>/content/images/` | Generated images, cover art, diagrams |
| `<data_dir>/content-samples/` | Real posts from the user's social media — primary voice reference |
| `<data_dir>/knowledge/` | Reference material — auto-crawled from `knowledge/index.md` sources (RSS, sitemaps, YouTube transcripts, podcasts) plus user-curated notes |
| `<data_dir>/knowledge/index.md` | Knowledge source definitions (Key, Handler, Feed URL tables) |
| `<data_dir>/feed/feeds.json` | Aggregated feed — single source of truth for brainstorming |
| `<data_dir>/feed/raw/` | Per-source JSON crawl outputs |
| `<data_dir>/feed/sources.json` | Social/ephemeral feed sources (X accounts, YouTube creators, websites) — managed via `/hum sources` |
| `<data_dir>/feed/assets/` | Preference learning (rankings, feedback history, dedup tracker) |

## Writing Guidelines

- **Always read `content-samples/`** before drafting — these are real examples of the user's writing and the most authoritative reference for their voice.
- **Always read `knowledge/`** before drafting — any reference material the user has placed there should inform the content.
- **Always read `VOICE.md`** for tone and style rules.

## Post Types

Each post type has a defined structure. The `/hum create` command requires a platform and post type.

### X
| Post Type | Format |
|-----------|--------|
| **Tweet** | Single tweet, under 280 chars, hook-driven. Optional media. |
| **Thread** | Multiple numbered tweets, each under 280 chars. Hook in tweet 1. |
| **Article** | Long-form post, up to 25,000 chars. Premium subscribers only. Rich text formatting, cover image, published directly to the X feed. Functions like a mini blog post. Requires cover image. Draft in full prose with H2 section headers. |

### LinkedIn
| Post Type | Format |
|-----------|--------|
| **Post** | Under 200 words. Short paragraphs. Opens with observation, ends with reflection/question. |
| **Article** | Long-form, 600–1000 words. Section headers. Requires cover image and intro feed post. |

## Actions & Connectors

Actions live in `scripts/act/`, connectors in `scripts/act/connectors/` (one per channel):

- **Connectors** (`act/connectors/`):
  - `x.py` — X API v2 (requires `credentials/x.json` or `X_USER_ACCESS_TOKEN` env var)
  - `linkedin.py` — LinkedIn REST API (requires `credentials/linkedin.json` or env vars)
  - All connectors follow a uniform interface — see `act/connectors/__init__.py` for the `load(platform)` dispatcher
- **Actions** (`act/`):
  - `publish.py` — draft parsing, preview, and publishing via connectors
  - `engage.py` — follows, comments, replies
  - `analyze.py` — account insights and post analytics
- Browser-based actions (when API is unavailable) are handled by the agent via the browser tool.
- Never put secrets in the skill files. Read them from `credentials/x.json`, `credentials/linkedin.json`, or env vars.

## Image Generation

Images for posts are generated using the bundled image-gen library at `scripts/lib/image-gen/`. It provides a unified interface to multiple AI image providers:

| Provider | Model | Env Var |
|----------|-------|---------|
| **gemini** (default) | gemini-2.5-flash-image | `GEMINI_API_KEY` |
| **openai** | gpt-image-1 | `OPENAI_API_KEY` |
| **grok** | grok-2-image | `XAI_API_KEY` |
| **minimax** | image-01 | `MINIMAX_API_KEY` |

API keys are set as environment variables or in `openclaw.json` → `env.vars`. The active provider is configured in `openclaw.json` → `skills.entries.hum.config.image_model` (default: `gemini`) or via the `HUM_IMAGE_MODEL` env var.

When drafting, add `image_prompt` to the post. Calling `validate(post)` auto-generates the image and sets `media_path`. If `VOICE.md` has a `## Visual Style` section, it is automatically appended to the image prompt.

## Daily Loop

`/hum loop` runs the full morning workflow. See `LOOP.md` for the step-by-step instructions. Individual steps call scripts from `scripts/` where needed.
