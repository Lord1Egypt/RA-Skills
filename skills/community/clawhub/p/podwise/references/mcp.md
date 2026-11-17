# Podwise MCP Tool Reference

Podwise capabilities are exposed through the remote MCP server at `https://mcp.podwise.ai/mcp`. Use these tools to search episodes, process media, retrieve AI artifacts, manage subscriptions, browse history, and ask questions across podcast transcripts.

Verify the connection before running any workflow:

- `get_me` — returns the account email, plan, and remaining AI processing credits.

> **Naming:** hosts often prefix tool names with the server name, e.g. `podwise_get_me`. The base names below are what the server exposes; use whatever the host shows.

## Identifier rules

Every tool identifies content by a **numeric seq**, never by URL.

| Content | Where it comes from | Link format |
| --- | --- | --- |
| Episode | `episodeSeq`, or the trailing integer of an episode URL | `https://app.podwise.ai/dashboard/episodes/<seq>` |
| Podcast | `podcastSeq`, or the trailing integer of a podcast URL | `https://app.podwise.ai/dashboard/podcasts/<seq>` |

When the user pastes a Podwise URL, strip it to the trailing integer. Search results already return seqs.

---

## Tools

### get_me

Get the connected account: email, plan, remaining AI processing credits. Use to verify the connection and to check quota before processing.

---

### search_episodes

Find episodes by keyword.

- `query` (string, required)
- `page` (0-based, default 0)
- `pageSize` (1–30, default 10)

Returns each match's `seq`, title, podcast, publish time, and `transcribed` (whether summary and transcript are available).

### search_podcasts

Find shows by name.

- `query` (string, required)
- `page`, `pageSize` (1–30, default 10)

Returns each show's `seq`, name, owner, and last publish time.

Use `search_*` to locate content by keyword. Use `ask_podwise` — not search — when the user wants a synthesized answer from transcript content.

---

### get_popular_episodes

List what is trending on Podwise.

- `limit` (1–100, default 20)

---

### list_followed_episodes

New episodes from podcasts the user follows.

- `days` (1–30, default 7)
- `endDate` (`YYYY-MM-DD`, default today)

Returns episodes with read status.

### list_followed_podcasts

Podcasts the user follows that published within the range.

- `days` (1–30, default 7)
- `endDate` (`YYYY-MM-DD`, default today)

### list_podcast_episodes

Episodes of one podcast within a date range.

- `podcastSeq` (integer, required)
- `days` (1–365, default 7)
- `endDate` (`YYYY-MM-DD`, default today)

### list_my_episodes

The user's listening / reading activity, newest first.

- `type` (`"played"` | `"read"`, required) — `played` = listened, `read` = opened in Podwise
- `page` (0-based, default 0)
- `pageSize` (1–50, default 20)

---

### set_podcast_follow

Follow or unfollow a show.

- `podcastSeq` (integer, required)
- `follow` (boolean, required)

### set_episode_read

Mark an episode read or unread.

- `seq` (integer, required)
- `read` (boolean, required)

---

### process_episode

Start AI processing (transcription, summary, outline) for an episode that is not yet transcribed.

- `seq` (integer, required)

**Consumes AI processing credits. Always confirm with the user before calling.** Processing runs asynchronously — poll `get_episode` until it is done.

> `process_episode` only accepts an episode that already exists in Podwise. To bring in a YouTube, Xiaoyuzhou, or local file, see **import_episode** and the upload tools below.

### import_episode

Import a single episode from Xiaoyuzhou or YouTube and return its `seq`. Importing does **not** start processing — call `process_episode` afterwards (with confirmation).

- `url` (Xiaoyuzhou episode URL or YouTube URL, required)
- `private` (boolean, default false)

### start_audio_upload / complete_audio_upload

Process a **local** audio or video file.

1. `start_audio_upload` with `fileName` and `contentType` (e.g. `audio/mpeg`). It returns an `uploadId`, an `uploadUrl` + `uploadHeaders` (PUT the bytes directly with `curl`), and a `browserUploadUrl` (for the user to upload in a browser).
2. Upload the file bytes to `uploadUrl` with the given headers, or hand the `browserUploadUrl` to the user.
3. `complete_audio_upload` with the `uploadId` and optional `title`, `description`, `speakers`, `keywords`, `durationSeconds`.

**Consumes AI processing credits on completion. Confirm with the user first.**

---

### get_episode

Get processing status and progress for an episode. Poll this after `process_episode` / `complete_audio_upload`.

- `seq` (integer, required)

### get_episode_summary

The single call for all AI-generated artifacts of an episode:

- overview, key takeaways, chapters, highlights, Q&A, keywords, and mind map.

- `seq` (integer, required)
- `language` (optional translation language)

There are no separate `get_chapters` / `get_highlights` / `get_qa` / `get_mindmap` / `get_keywords` tools in the remote server. If the episode is not yet transcribed, offer to run `process_episode`.

### get_episode_transcript

The full transcript with timestamps and speakers, paginated by segment.

- `seq` (integer, required)
- `language` (optional translation language)
- `limit` (1–500, default 200)
- `offset` (0-based, default 0)

Prefer `get_episode_summary` unless exact wording or quotes are needed. Transcripts are token-intensive.

> For a subtitle file, use `export_episode_srt` (see Export below) instead of rebuilding one from segments.

---

### ask_podwise

Ask a question and get a transcript-grounded answer synthesized across Podwise's corpus. Returns the answer **with cited source clips** (episode seq, speaker, timestamps).

- `question` (string, ≤1000, required)

**Counts against the user's Ask quota.** Allow up to 60 seconds; do not cancel early. Do not use it to locate episodes by keyword — use `search_episodes`.

### get_ask_history

- Without `hash`: list questions asked within a date range (`days` 1–30 default 7, `endDate`).
- With `hash`: get the full answer and sources of one question.

---

### translate_episode

Request an AI translation of a transcribed episode (runs asynchronously).

- `seq` (integer, required)
- `language` (required): English, Chinese, Traditional Chinese, Japanese, Korean, Czech, French, German, Hindi, Polish, Portuguese, Russian, Spanish

### list_episode_translations

List the translations of an episode and the status of each. Poll this, then read with `get_episode_summary` / `get_episode_transcript` using the same `language`.

---

### Clips

- `create_clip` — save a key moment. `episodeSeq`, `pointSeconds`.
- `get_clip` — one clip with content, takeaways, and a temporary media URL. `clipId`.
- `list_clips` — clips of an episode (`episodeSeq`), or the user's recent clips (`page`, `pageSize`).
- `delete_clip` — permanently delete one of the user's clips. `clipId`. **Confirm with the user first.**
- `export_clips_markdown` — all ready clips of an episode as one Markdown document. `episodeSeq`.
- `send_clips` — send one clip (`clipId`) or all ready clips (`episodeSeq`) to `notion` or `readwise`. Integration must be connected in Podwise settings.

### Export

- `export_episode_markdown` — summary, outline, and transcript of a transcribed episode as Markdown. `seq`; optional `language`, `dialect` (`common` | `obsidian` | `logseq`), `mixOutlines`, `mixWithOriginLanguage`. Returns the note text — the agent writes the file to disk.
- `export_episode_srt` — transcript of a transcribed episode as SRT subtitles. `seq`; optional `language` (translation), `mixWithOriginLanguage` (bilingual: keep the original alongside the translation), `translationFirst` (bilingual only: put the translation above the original). Short exports return inline; long ones return a download link valid for 10 minutes — share it with the user.
- `send_episode` — send summary and notes to `notion` or `reader` (`target`). Optional `language`, `mixOutlines`, `mixWithOriginLanguage`; Reader-only: `location` (`new` | `later` | `archive`), `shownotes`, `mindmap`; Notion-only: `transcripts` (default true).

Integration must already be connected in Podwise settings.

---

### Enterprise tools

`enterprise_process_audio`, `enterprise_get_status`, `enterprise_get_result`, `enterprise_query_results`, `enterprise_translate`, `enterprise_get_translation`, `enterprise_export`, `enterprise_get_usage` are for Enterprise-plan API usage. If a tool reports that a Pro or Enterprise plan is required, relay the upgrade link to the user instead of retrying.

---

## Artifact → Tool

| Artifact | Tool |
| --- | --- |
| Transcript | `get_episode_transcript` |
| Summary & takeaways | `get_episode_summary` |
| Chapters | `get_episode_summary` |
| Highlights | `get_episode_summary` |
| Q&A | `get_episode_summary` |
| Mind map | `get_episode_summary` |
| Keywords | `get_episode_summary` |

---

## Intent → Tool

| User wants to… | Tool |
| --- | --- |
| Verify connection / check credits | `get_me` |
| Find episodes about a topic | `search_episodes` |
| Find a podcast by name | `search_podcasts` |
| See what's trending | `get_popular_episodes` |
| See new episodes from followed shows | `list_followed_episodes` |
| Explore a specific show's episodes | `list_podcast_episodes` |
| See listening history | `list_my_episodes type=played` |
| See reading history | `list_my_episodes type=read` |
| Get a synthesized answer from transcripts | `ask_podwise` |
| Summarize an episode | `get_episode_summary` |
| Get the full transcript | `get_episode_transcript` |
| Follow / unfollow a show | `set_podcast_follow` |
| Mark an episode read | `set_episode_read` |
| Process a Podwise episode | confirm → `process_episode` |
| Import a YouTube / Xiaoyuzhou episode | `import_episode` → confirm → `process_episode` |
| Transcribe a local file | confirm → `start_audio_upload` → upload → `complete_audio_upload` |
| Translate an episode | `translate_episode` → `list_episode_translations` |
| Export episode notes to Notion / Readwise | `send_episode` |
| Export episode notes as Markdown / Obsidian / Logseq | `export_episode_markdown` |
| Export subtitles as SRT | `export_episode_srt` |
| List my clips for an episode | `list_clips` |
| Export clips to Markdown | `export_clips_markdown` |
| Send clips to Readwise / Notion | `send_clips` |

---

## Common Failure Cases

- **Tools unavailable / auth error**: the MCP server is not connected or not authorized. Load [installation.md](installation.md).
- **`get_episode_summary` says "not processed"**: run `process_episode` first (confirm — credits are consumed).
- **"Pro or Enterprise plan required"**: report it and relay the upgrade link. Do not retry or fabricate output.
- **`ask_podwise` returns a quota error**: report it directly. Do not fabricate an answer.
- **SRT export returns a download link**: long transcripts are not sent inline — share the link with the user (valid for 10 minutes).
- **`process_episode` / `complete_audio_upload` run without confirmation**: always wrong — both consume quota.
- **URL passed where a seq is expected**: extract the trailing integer from the URL first.
- **`send_episode` / `send_clips` fail**: the Notion / Readwise integration is not connected in Podwise settings.
