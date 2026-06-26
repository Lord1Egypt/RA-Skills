# Changelog

## 0.4.0

**Post scheduling.** Two new endpoints. `POST /posts/{id}/schedule` queues a draft to auto-publish at a given `scheduled_at` time (max 60 days out, workspace cap of 100 scheduled posts). `POST /posts/{id}/cancel-publish` reverts a scheduled or in-progress publish back to draft, as long as no item has started posting yet.

**Analytics.** `GET /post-items/{id}/analytics` returns views, likes, comments, and `fetched_at` for a single published post item. Metrics refresh roughly daily for up to 90 days after posting. `metrics` is `null` until the first poll lands.

**Granular API key scopes.** The old two-tier `read_write` / `read_draft` model is replaced by 14 fine-grained scopes (`content:generate`, `posts:publish`, `analytics:read`, etc.). The skill now documents the required scope under each endpoint, plus a scopes reference table. Dashboard presets (full access, draft only, read only) map cleanly to the old behavior, but a 403 now means a missing scope.

**Image model rename.** `gpt-image-1.5` is now `gpt-image-2`. Same role (most photorealistic), updated to the current model. The size matrix is unchanged: square, portrait, and landscape — no `feed`.

**Other changes:**
- `posts` status enum now includes `scheduled` (alongside `draft`, `publishing`, `published`, `failed`).
- Fixed: the publish response shape no longer includes a `credits_used` field. Credits are charged per item in the background; check the credit balance after publishing to see what was spent.
- Removed the `status: "planned"` field from calendar entry responses (it was never returned by the API).
- New "Required scope" line under each endpoint.

## 0.3.0

**Content calendar.** Five new endpoints for calendar entries (list, create, get, update, delete). You can plan posts with a date, time, target platforms, and notes.

## 0.2.0

**Video generation.** Two new endpoints for creating AI videos from text or images. Three models to pick from (Kling 3.0 Pro, Veo 3.1, Runway Gen-4.5) with configurable duration, size, and audio. Polls every 10 seconds since video takes longer than images.

**Source URLs.** Content generation now accepts a `source_urls` field — pass up to 10 URLs and the AI scrapes them for research context before writing captions. Private URLs are filtered out automatically.

**Dynamic credit costs.** Removed all hardcoded credit amounts from the docs. Costs now come from the API response (`credits_used`, `remaining_credits`) so the skill stays accurate when pricing changes.

**Other changes:**
- Prompt max length bumped from 500 to 2,000 characters for content generation
- Polling strategy now distinguishes content/images (60 polls max) from video (120 polls max)
- Updated clawhub.json tags and description
- README updated with video and source URL examples

## 0.1.1

First-run setup flow, direct URLs to settings pages, fixed broken links in the skill doc.

## 0.1.0

Initial release. Content generation, image generation, media upload, post creation, and publishing across Instagram, TikTok, X, YouTube, Facebook, and LinkedIn.
