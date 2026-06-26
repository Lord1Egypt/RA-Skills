---
name: linkedin-page-publisher
description: Publish posts programmatically to a LinkedIn Company Page via the versioned Posts API (/rest/posts), including text posts, single-image posts, multi-image carousels, video posts, and article link previews. Handles the full multi-step media upload flow (initializeUpload → PUT binary → wait for LinkedIn to finish processing → reference URN in the post). Use this skill whenever the user wants to post to LinkedIn, publish to a Company Page, automate LinkedIn content, cross-post to LinkedIn from another system, build a LinkedIn publishing bot or scheduler, or upload images or videos to LinkedIn programmatically — even when they don't say "API" explicitly. Also use it when the user mentions errors from the LinkedIn Posts API, w_organization_social scope, urn:li:organization URNs, UGC posts, or /rest/images and /rest/videos endpoints.
---

# LinkedIn Page Publisher

Publishes content to a LinkedIn Company Page through LinkedIn's versioned REST API (`/rest/posts`). The skill ships a Python CLI (`scripts/publish.py`) that also works as an importable library, plus a one-time OAuth helper (`scripts/get_token.py`) to obtain the initial access token.

## When to reach for what

- **User just wants to post something** → run `scripts/publish.py` directly with the right subcommand (see "Publishing" below).
- **User is setting this up for the first time and doesn't have a token yet** → walk them through `references/setup.md`, which covers creating the LinkedIn Developer app, requesting Community Management API access, and running `scripts/get_token.py` to complete the 3-legged OAuth flow.
- **User hits a cryptic API error** → consult `references/troubleshooting.md` before guessing. LinkedIn's error messages are often misleading (e.g., "unauthorized" frequently means "wrong scope" or "not a page admin," not "bad token").
- **User wants to extend the skill** (schedule posts, add analytics, wrap it in a web service, etc.) → import from `scripts/lib/` rather than shelling out to the CLI. The library layer is the contract; the CLI is just one consumer of it.

## Environment variables

These three cover every use case. Don't invent a config file — env vars compose better with cron, CI, and shell scripts.

| Variable | Required | What it is |
|---|---|---|
| `LINKEDIN_ACCESS_TOKEN` | yes | OAuth 2.0 access token with `w_organization_social` scope. Valid for 60 days; refresh tokens last 365 days. |
| `LINKEDIN_ORG_ID` | yes | Numeric organization ID only (e.g. `5515715`), not the full URN. The script prepends `urn:li:organization:`. Find it at `https://www.linkedin.com/company/<slug>/admin/` — the URL shows the numeric ID once you're in the admin view. |
| `LINKEDIN_API_VERSION` | no | YYYYMM format, e.g. `202602`. Defaults to `202602` (February 2026). LinkedIn supports each version for a minimum of one year, so bump this deliberately when new features ship. |

## Publishing

`scripts/publish.py` exposes five subcommands. Every subcommand accepts `--text` (post commentary, up to 3,000 characters) and `--dry-run` (prints the request body without calling the API — useful for debugging).

### Text-only post
```bash
python scripts/publish.py text --text "Announcing our Q1 roadmap. Three big bets this year: ..."
```

### Single image
```bash
python scripts/publish.py image path/to/photo.jpg \
  --text "At the AI builders meetup in Lima last night" \
  --alt "Twelve people seated around a conference table with laptops open"
```
`--alt` is required. Accessible alt text is also what LinkedIn's ranking signals care about, so don't skip it.

### Multi-image carousel (2–20 images)
```bash
python scripts/publish.py multi-image img1.jpg img2.jpg img3.jpg \
  --text "Recap from OpenClaw's monthly hackathon" \
  --alt "Photo of attendees" "Photo of winning demo" "Group photo at the end"
```
Pass one `--alt` per image, in order. If the count doesn't match, the CLI errors out before hitting the API.

### Video
```bash
python scripts/publish.py video path/to/demo.mp4 \
  --text "Demo of our new agent flow" \
  --title "Agent flow walkthrough"
```
Video uploads take longer. The script auto-detects file size and uses single-part upload under 200 MB or multipart upload above. It polls LinkedIn's video status endpoint until the asset reaches `AVAILABLE` before creating the post — posting against a still-processing video produces a post with a broken player.

### Article link preview
```bash
python scripts/publish.py article https://example.com/my-blog-post \
  --text "Wrote up how we built this — thoughts welcome"
```
LinkedIn scrapes the URL's OpenGraph metadata to render the preview card. If the target page's OG tags are missing or wrong, the preview will look bad — that's a site issue, not an API issue. The CLI prints the article URN in the response so the user can verify.

## Using the library from other Python code

```python
from scripts.lib.client import LinkedInClient
from scripts.lib.posts import post_text, post_image, post_video, post_article, post_multi_image

client = LinkedInClient()  # reads env vars

# Text
post_text(client, "Hello, page followers!")

# Image
post_image(client, "photo.jpg", text="At the meetup", alt="Group photo")

# Video (handles small and multipart automatically)
post_video(client, "demo.mp4", text="Quick demo", title="Demo")

# Article
post_article(client, "https://example.com/post", text="Worth a read")
```

All post functions return the post URN (e.g. `urn:li:share:7045020441609936898`) on success and raise on failure. Don't swallow exceptions — the error messages carry the LinkedIn response body, which is the only useful debugging signal.

## Why the upload flow has so many steps

LinkedIn's media upload is a three-step handshake:

1. **Register** — `POST /rest/images?action=initializeUpload` (or `/rest/videos?action=initializeUpload`). LinkedIn returns an upload URL (or several, for multipart) and a pre-assigned URN (`urn:li:image:...` or `urn:li:video:...`).
2. **Upload** — `PUT` the binary bytes to the returned upload URL(s). No auth header on these PUT calls — the URL itself is pre-signed.
3. **Reference** — create the post with the URN in `content.media.id`.

For videos, there's an implicit fourth step: LinkedIn processes the video asynchronously. If you create the post immediately after the PUT, the video may not be ready and the post will be broken. The library polls `GET /rest/videos/{urn}` until `status == AVAILABLE` before returning the URN. Multipart video uploads also need a `finalizeUpload` call with the ETags from each part — the library handles this.

This is why the skill bundles upload helpers rather than expecting callers to reimplement them — the edge cases (async processing, multipart, alt text on multi-image) are where naive implementations break.

## Rate limits and scope

- **Personal token limit**: roughly 100 calls/day/member. Respect this when building schedulers.
- **Scope required**: `w_organization_social`. The authenticating user must be an admin of the Company Page — being an employee is not enough.
- **Post character limit**: 3,000. The API returns HTTP 422 if exceeded. The library checks locally before calling so the failure is cheaper.
- **Access token lifetime**: 60 days. Refresh tokens last 365 days and can be used to mint new access tokens without re-prompting the user. `get_token.py` saves both.

## What LinkedIn's API cannot do (as of 2026)

Don't promise the user these — they require manual work in LinkedIn's web UI:

- **Long-form articles** (the Medium-style ones with a title, cover, and body) — web UI only.
- **Newsletters** — web UI only.
- **Document posts / PDF carousels** — no API support.
- **Polls** — no API support.
- **@mentions of people or companies in post text** — no API support. The text will publish, but the mention won't be a link.
- **Native scheduling** — the API posts immediately. Build scheduling with cron or a queue.

If the user asks for any of the above, say so upfront rather than trying to hack around it.

## Debugging etiquette

When the user reports an error, ask for:
1. The exact command they ran (redacting the token).
2. The full response body LinkedIn returned — the `serviceErrorCode` and the `message` fields carry the real signal.
3. Whether the token still works for a simple `GET /rest/posts?author=urn:li:organization:<id>&q=author`. If this 401s, the token is the problem, not the post.

Then check `references/troubleshooting.md` against the specific error code before guessing.
