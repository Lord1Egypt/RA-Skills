# OpenClip reference

Quick lookup for the OpenClip skill. All verified against the real MCP tools + Integration API.

## Status values

**Submission status** (`get_video_status` → `status`):
`pending` → `downloading` → `processing` → `completed` (terminal) | `failed` (terminal).
Also `pending_credits` (team out of credits). Only call `list_clips` once `completed`.

**Video processing status** (nested `video.status`): `downloading`, `download_failed`,
`uploaded`, `pending_credits`, `processing`, `completed`, `failed`.
`video.viral_moments_count` appears when the video is `completed`.

**`video.progress` is COARSE**, it is NOT a smooth percentage. It is derived from the status:
roughly 0 (failed) / single-digit while pre-processing (downloading, pending_credits) /
~10 (uploaded) / ~20 during `processing` / 100 (completed). Treat it as a hint only; use
`status`, not `progress`, for any fine-grained control flow or "how close to done" decisions.

**Free tool job status** (`get_tool_job_status` → `status`): `queued` → `processing`
(in-flight, poll every 5-10s) → `completed` (returns permanent CDN `outputs` URL per
format + `result_meta`) | `failed` (returns `error`). Transcription usually finishes
within a minute or two.

**UGC job status** (`get_ugc_job_status` → `status`): `queued` → `rendering` (in-flight,
poll every 10-15s) → `completed` (returns `video_url` + `result_meta`: duration, dims,
fps, seed) | `failed` (returns `error`). Renders can take a couple of minutes.

## Free tool operation params

- `edit_video` operations: crop (`aspect` "1:1"|"9:16"|"16:9"|"4:5" OR `x`,`y`,`width`,`height`),
  trim (`start_ms`, `end_ms` required), rotate (`degrees` 90|180|270 and/or `flip`
  none|horizontal|vertical), resize (`width`, `height`), compress (`target_mb` OR `crf` 18-32),
  mute.
- `convert_media` targets (`to`): mp4, webm, mov, mkv, gif (optional `fps` default 12,
  `width` default 480), mp3, aac, wav, flac.
- `extract_thumbnails`: `count` 1-10 (default 1), optional `width`; output is a zip of frames.
- `edit_image` operations: compress (`quality` 1-100 default 80, `format` jpg|png|webp),
  resize (`width`, `height`), crop (`aspect` OR coords), each with optional `format`.
- `remove_background`: no params beyond `file`; returns a transparent PNG.
- `transcribe`: optional `language` (omit to auto-detect), `diarize` (default true);
  outputs json/srt/vtt.
- `generate_ugc`: `brief_name` (server preset) OR inline `brief` object of creative string
  fields (`character`, etc.; structured fields, not a prose prompt). Free accounts: one
  generation per day; paid: credit-metered by rendered seconds.
- Free tools take a `file`/`video` id from `create_upload` (PUT bytes first, do NOT
  `complete_upload`) or an existing video from `list_videos`.

## Caption preset keys (`list_caption_presets`)

`default`, `dan`, `dan-reveal`, `pop`, `mozi`, `kendrick`, `sara`, `lucy`, `tayo`, `beast`.
(Always confirm with `list_caption_presets`, keys can evolve. That call also returns the full
caption-style property schema and caption position options for custom styling.)

## Clip / viral moment shape (`list_clips`)

Each moment: `id` (hashid, pass to `render_clip`), `title`, `hook`, `category`,
`start_time_ms`, `end_time_ms`, `duration_ms`, `virality_score` (0-10),
`viral_score_details` (sub-scores 0-100: hook strength, shareability, rewatchability,
surprise, emotional impact), `thumbnail_url`, `quote`, `social_copy`, `platforms`, and assets:
`clip` `{url, size_bytes, type}` (downloadable), `clip_watermarked`, `rendered_clip`
`{url, size_bytes}` (present after a successful `render_clip`).

## Account shape (`get_account`)

`user_id` (hashid), `email`, `credits_remaining` (int), `client` `{name, type}`,
`abilities` (the granted scopes/abilities of the current connection), `rate_limit_per_minute`.
**Over MCP, `client.type` is ALWAYS `personal`**, the MCP `get_account` tool hardcodes it
(the connection always acts as the signed-in user via their owner-bound personal client). The
`partner` type only appears on the REST Integration API, never through the MCP server.

## Auth & server URL

- The OpenClip MCP server is **remote over HTTP**, production URL `https://openclip.app/mcp`
  (shown on the connect page).
- **Primary, OAuth one-click:** paste the server URL into your client and sign in with your
  OpenClip account (the connector runs OAuth 2.1 in the browser; access token carries scope
  `mcp:use`). No token to copy.
- **Alternative, manual Bearer token:** for header-only / programmatic clients, mint a token
  (ability `mcp:use`) on the connect page (openclip.app/settings/connect → "Generate MCP token")
  and connect to the **`/mcp/key`** endpoint with it in the `Authorization: Bearer …` header.
- Self-hosting/dev: run the local stdio server with `php artisan mcp:start openclip`.

## Errors (MCP tool results, not HTTP)

Tool failures are returned in-band as a tool result with `isError: true` and a plain-text
message, there are NO HTTP 401/402/403/422 codes or JSON error envelopes. Exact messages:
`"Not authenticated. Reconnect your OpenClip token."` (reconnect / re-mint token),
`"Job not found."` (wrong/expired job id), `"Viral moment not found."` (wrong moment id),
`"Video not yet available. Check get_video_status for progress."` (keep polling), and
validation messages (e.g. bad `url` / unknown `caption_preset`) returned as the message text.
Subscription/credit problems are NOT errors, they surface as `get_video_status` `status`
(`failed` = no subscription, `pending_credits` = out of credits). See SKILL.md "Error handling".

## Known limitation

The pipeline (download → transcript → viral-moment detection → render) runs on external
processing services. A self-hosted instance must have those configured
(`RUNPOD_DOWNLOADER_ENDPOINT`, `RUNPOD_API_TOKEN`, etc.) and the team needs credits + an active
subscription, or submissions terminate as `failed`. The hosted openclip.app has these set.
There is no projects/folders concept in this API.
