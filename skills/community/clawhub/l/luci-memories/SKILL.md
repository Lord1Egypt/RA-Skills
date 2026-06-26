---
name: luci-memory
description: "Search personal video memory — media content (videos, images, keyframes, transcripts) and portrait data (traits, events, relationships, speeches). Use when the user asks about their videos, what happened, what was said, who they know, or their personality."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"],"env":["MEMORIES_AI_KEY"]},"primaryEnv":"MEMORIES_AI_KEY"}}
---

# luci-memory

## Setup

Requires an `MEMORIES_AI_KEY`. On first use, if no key is found, the script will error and ask for one.

When the user provides their key, save it to `{baseDir}/.env`:

```
MEMORIES_AI_KEY=sk-their-key-here
```

After that, everything just works — the key is loaded automatically from `.env` on every run.

## Timezone

**All timestamps in Luci-memory are stored and returned in UTC.** Skill output labels them with " UTC" so this is unambiguous. The user's local timezone is in `USER.md` (e.g. `Asia/Shanghai`). You are responsible for converting in both directions:

1. **Reading results.** When presenting `captured_time` to the user, convert from UTC to the user's local timezone. Never show raw UTC labels to the user.

2. **Writing filters.** `--after` and `--before` are interpreted as UTC. If the user says relative dates like "yesterday" or "this morning", convert their local-time intent to a UTC range before passing the dates.

**Example** (user in `Asia/Shanghai`, UTC+8, asks "what did I do yesterday" on 2026-04-08):
- Local intent: 2026-04-07 00:00 → 2026-04-08 00:00 (Asia/Shanghai)
- UTC range to pass: `--after 2026-04-06T16:00:00 --before 2026-04-07T16:00:00`

If `USER.md` has no timezone and the user uses relative dates, ask them first.

Unified search across personal media and portrait data from the Luci-memory API.

The user's videos go through two processing pipelines that produce different data:
- **Media content** (personal): video summaries, audio transcripts, visual transcripts, keyframes, images
- **People & knowledge** (portrait): traits, events with participants, relationships, speeches attributed to speakers

## When to use
- User asks to find or search videos, images, recordings, or photos
- User asks what was said or shown in a video or recording
- User asks to list recent videos, images, or recordings
- User asks about media at a specific location or time
- User asks about audio recordings or what was recorded
- User asks about traits, personality, hobbies, interests
- User asks what events happened, or events involving specific people
- User asks about relationships between people
- User asks about what someone said
- User mentions "luci memory" or wants to use their video memory

## Choosing the right type

- **About content** (what happened, what was said/shown, find media) → use media types (`search_video`, `query_audio`, `search_recording`, etc.)
- **About recordings** (standalone audio recordings, not video soundtracks) → use `search_recording` / `query_recording`. Recordings are separate from video audio transcripts — they are independent audio captures with their own IDs and transcripts.
- **About people** (who, traits, relationships, named individuals) → use portrait types (`traits`, `events`, `speeches`, etc.)
- **Ambiguous questions** like "What happened with Alice last week?" → use **both**: portrait types to identify the person and events, media types to get detailed video content and transcripts.
- **Person name fallback:** Portrait data only exists for people who have appeared in at least 5 videos AND been named by the user in the app. If a portrait query by person name returns no results, fall back to media types — search video summaries, audio transcripts, or visual transcripts for mentions of that name instead.

## Relevance guidelines
- There is no rerank process — retrieved results may contain items irrelevant to the user's actual intent.
- **Always verify relevance**: after receiving results, check each item against the user's original query. Only present results that are relevant. Discard anything that doesn't match.
- **Refine and retry**: if results seem off or too broad, retry with a more specific query, narrower date range, or additional filters. Do not just dump low-quality results to the user.
- **Ask the user**: if the query is ambiguous or too vague to produce good results, ask the user for more specific conditions before searching. It is better to clarify than to return noise. Do this no more than 1 time.

## No hallucination — ground every claim in retrieved data
- **Never fabricate** what the user did, said, or experienced. Every detail in your answer must come from actual search results.
- **Multi-step retrieval**: for questions like "what did I do and say at XXX", do NOT answer from a single broad search. Follow this pattern:
  1. **Locate**: search broadly (search_video, search_recording, search_events) to find relevant video_ids, recording_ids, or event_ids.
  2. **Retrieve**: once you have IDs, prefer **query_audio / query_visual** with `--video-ids` or **query_recording** with `--recording-ids` to get complete transcripts. You can also use **search_audio / search_visual** scoped to those video IDs to find specific moments — use both flexibly as needed.
- **Do not stuff keywords into search queries.** Each semantic search query should be a short, coherent natural-language query, rather than stacking multiple possible words. You are encouraged to try different ones and query various times though.
- **If data is missing, say so.** Do not fill gaps with plausible-sounding guesses. "I couldn't find transcript data for that video" is always better than making something up.

## How to invoke

Note: `--after` / `--before` are **UTC**. Convert from the user's local timezone first (see Timezone section above).

## Returning Images/Keyframes to User

Image and keyframe results include `bucket` and `blob` fields. To send an image in chat, fetch the bytes from the Luci-memory image proxy endpoint, then forward via OpenClaw:

1. **Download** the image bytes from the proxy endpoint:
   ```bash
   curl -sL -o /path/to/workspace/image.jpg \
     "https://skills.memories.ai/luci-memory/personal/image?bucket=<bucket>&blob=<blob>"
   ```
2. **Send** via OpenClaw message CLI:
   ```bash
   openclaw message send --channel <channel> --target <chat_id> --media /path/to/workspace/image.jpg --message "caption"
   ```
3. **Cleanup** the file after sending:
   ```bash
   rm /path/to/workspace/image.jpg
   ```

⚠️ Always quote the URL — it contains `&` and the blob may have `/` characters.
⚠️ Do NOT use `/tmp` or paths outside the workspace — some tools block external paths.
⚠️ The image tool only analyzes images — it cannot send them to the user. Use `openclaw message send --media` instead.

# ============ Media content (personal) ============

# --- Video ---
bash {baseDir}/run.sh --query "cooking in kitchen" --type search_video
bash {baseDir}/run.sh --query "what did I do" --type search_video --location "Heze"
bash {baseDir}/run.sh --query "meeting" --type search_video --after 2025-12-01 --before 2026-01-01
bash {baseDir}/run.sh --type query_video
bash {baseDir}/run.sh --type query_video --location "Suzhou" --after 2025-12-01

# --- Image ---
bash {baseDir}/run.sh --query "sunset" --type search_image
bash {baseDir}/run.sh --query "food" --type search_image --location "Beijing"
bash {baseDir}/run.sh --type query_image

# --- Audio Transcripts (what was said) ---
bash {baseDir}/run.sh --query "talking about work" --type search_audio
bash {baseDir}/run.sh --query "budget" --type search_audio --video-ids VI123,VI456
bash {baseDir}/run.sh --type query_audio --video-ids VI123,VI456

# --- Visual Transcripts (what was shown) ---
bash {baseDir}/run.sh --query "walking in park" --type search_visual
bash {baseDir}/run.sh --type query_visual --video-ids VI123,VI456

# --- Keyframes ---
bash {baseDir}/run.sh --query "person waving" --type search_keyframe
bash {baseDir}/run.sh --type query_keyframe --video-ids VI123,VI456

# --- Recordings (standalone audio captures, not video soundtracks) ---
bash {baseDir}/run.sh --query "discussing project" --type search_recording
bash {baseDir}/run.sh --query "meeting notes" --type search_recording --after 2025-12-01 --before 2026-01-01
bash {baseDir}/run.sh --type query_recording --recording-ids VI123,VI456

# ============ People & knowledge (portrait) ============

# --- Traits ---
bash {baseDir}/run.sh --type traits
bash {baseDir}/run.sh --type traits --person "Alice"
bash {baseDir}/run.sh --query "outdoor activities" --type search_traits

# --- Events ---
bash {baseDir}/run.sh --type events
bash {baseDir}/run.sh --type events --person "Alice"
bash {baseDir}/run.sh --type events --person "Alice,Bob"
bash {baseDir}/run.sh --type events --after 2025-12-01 --before 2026-01-01
bash {baseDir}/run.sh --query "cooking in kitchen" --type search_events
bash {baseDir}/run.sh --query "meeting" --type search_events --person "Bob" --after 2025-12-01

# --- Relationships ---
bash {baseDir}/run.sh --type relationships
bash {baseDir}/run.sh --type relationships --person "Alice"

# --- Speeches ---
bash {baseDir}/run.sh --type speeches
bash {baseDir}/run.sh --type speeches --person "Alice"
bash {baseDir}/run.sh --type speeches --event-ids EVT123,EVT456
bash {baseDir}/run.sh --type speeches --person "Alice" --event-ids EVT123
```

## Parameters

| Flag | Short | Description |
|------|-------|-------------|
| `--query` | `-q` | Search term (required for `search_*` types) |
| `--type` | `-t` | Operation type (default: `search_video`) |
| `--top-k` | `-k` | Max results (default: 10) |
| `--location` | `-l` | Filter by location name, geocoded via Google Maps (e.g. "Suzhou") |
| `--after` | | Only results after this date (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`) |
| `--before` | | Only results before this date |
| `--video-ids` | | Comma-separated video IDs (media types) |
| `--recording-ids` | | Comma-separated recording IDs (recording types) |
| `--person` | `-p` | Filter by person name(s), comma-separated (portrait types). Use `user` for self. |
| `--event-ids` | | Comma-separated event IDs (portrait types) |

## Image bytes

Image and keyframe results return `bucket` and `blob` (no signed URLs). To get the actual image bytes, hit the proxy endpoint — see "Returning Images/Keyframes to User" above. The endpoint streams the JPEG bytes directly with no expiration or auth on the client side.

## Types reference

### Media search types (require `--query`)
| Type | What it searches | Supports |
|------|-----------------|----------|
| `search_video` | Video summaries by meaning | `--location`, `--after/before` |
| `search_image` | Image descriptions by meaning | `--location`, `--after/before` |
| `search_audio` | Audio transcripts by meaning | `--video-ids`, `--after/before` |
| `search_visual` | Visual transcripts by meaning | `--video-ids`, `--after/before` |
| `search_keyframe` | Keyframe images by meaning | `--video-ids`, `--after/before` |
| `search_recording` | Recording transcripts by meaning | `--after/before` |

### Media query types (list/filter)
| Type | What it returns | Requires | Supports |
|------|----------------|----------|----------|
| `query_video` | Recent videos | — | `--location`, `--after/before` |
| `query_image` | Recent images | — | `--location`, `--after/before` |
| `query_audio` | Audio transcripts for videos | `--video-ids` | `--after/before` |
| `query_visual` | Visual transcripts for videos | `--video-ids` | `--after/before` |
| `query_keyframe` | Keyframes for videos | `--video-ids` | `--after/before` |
| `query_recording` | Full recording transcripts | `--recording-ids` | `--after/before` |

### Portrait query types (list/filter)
| Type | What it returns | Supports |
|------|----------------|----------|
| `traits` | Personality traits, hobbies, interests | `--person` |
| `events` | Events with participants | `--person`, `--after/before`, `--event-ids` |
| `relationships` | How user relates to people | `--person` |
| `speeches` | What people said | `--person`, `--event-ids` |

### Portrait search types (semantic, require `--query`)
| Type | What it searches | Supports |
|------|-----------------|----------|
| `search_events` | Events by meaning | `--person`, `--after/before` |
| `search_traits` | Traits by meaning | — |
