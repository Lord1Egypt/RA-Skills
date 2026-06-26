# Music Generator

Generate AI music, BGM, or lyrics from natural language with a single command. This skill auto‑detects intent and supports:
- Vocal song (lyrics + vocals)
- Instrumental background music (BGM)
- Lyrics only
- Task status update

It submits the request, polls progress automatically, and returns a preview first, then the final downloadable audio when ready. By default, the service returns TWO candidates (two task ids). Each candidate follows a two‑stage flow (preview → full).

## Installation
1. Place this skill in your OpenClaw workspace: `~/.openclaw/workspace/skills/musicful-music-generator/`
2. Create a `.env` file in the skill folder
3. Get your key at https://www.musicful.ai/api/authentication/interface-key/ and add it as `MUSICFUL_API_KEY` in `.env`
4. Reload or restart OpenClaw if needed
5. Run `/music_generator "Write a pop song about distance and memory"` to test

---

## What This Skill Does
- One command: `/music_generator` (with optional `mode`)
- Two‑stage polling: `status=2` preview first → `status=0` full mp3 later
- Two candidates: for song/BGM generation you typically get two task ids and must report each candidate (preview + full) separately

Common request types:
1) Vocal Song — Full song with lyrics and vocals
2) BGM — Instrumental‑only background music
3) Lyrics Only — Generate lyrics without audio
4) Status Query — Check current progress of a previously submitted task

---

## What You Can Ask It To Do (Natural Language)
- “Write a dreamy pop song about missing someone”
- “Create cinematic background music for a travel video”
- “Generate dark electronic lyrics about city loneliness”
- “Check the status of task_id 123456”

---

## Command: /music_generator
You can pass the main prompt directly after the command, or with `prompt=`.

Preferred
```
/music_generator "Write an emotional pop song about distance and memory"
```
Also Supported
```
/music_generator prompt="Write an emotional pop song about distance and memory"
```

### Modes
- `mode=normal` (default)
  - Generate & show lyrics → submit generation → two‑stage return (preview then full)
- `mode=bgm`
  - Pure instrumental (instrumental=1), no lyrics → two‑stage return
- `mode=lyrics`
  - Lyrics only; return text immediately

### Parameters
| Name       | Required | Default  | Description                                  |
|------------|----------|----------|----------------------------------------------|
| prompt     | Yes      | –        | Natural language request (can be inline)     |
| mode       | No       | normal   | normal | bgm | lyrics                        |
| style      | No       | Pop      | Music style                                  |
| mv         | No       | MFV2.0   | Model version (allowed: MFV2.0, MFV1.5X, MFV1.5, MFV1.0) |
| gender     | No       | male     | Vocal preference for song generation         |

### Quick Examples
- Generate a vocal song
```
/music_generator "Write an emotional pop song about distance and memory"
```
- Generate background music (BGM)
```
/music_generator mode=bgm style="Lo-fi" "Create relaxing lo-fi background music for studying"
```
- Generate lyrics only
```
/music_generator mode=lyrics "Write poetic indie lyrics about late-night city loneliness"
```
- Check a task status
```
/music_generator "Check the status of task_id 123456"
```

---

## How It Works
1) Submit request (vocal song / BGM / lyrics only)
2) Auto polling
   - status=2 → preview ready (audio_url is preview)
   - status=0 → full ready (audio_url is final mp3)
3) Return results per candidate (TWO candidates expected)
   - For each task id: first preview, then full

Lyrics‑only requests return text immediately.

---

## Result Format (Recommended)
Song/BGM generation (two candidates)
- Song 1
  - title: <title>
  - prompt: <original prompt>
  - lyrics: <full lyrics or empty if BGM>
  - preview: <status=2 audio_url>
  - full: <status=0 audio_url>
- Song 2
  - title: <title>
  - prompt: <original prompt>
  - lyrics: <full lyrics or empty if BGM>
  - preview: <status=2 audio_url>
  - full: <status=0 audio_url>

Lyrics‑only
- title: <optional>
- lyrics: <text>

Status query
- task id(s), current status per id
- preview/full links if available

---

## Key Purchase & Configuration (Required)
Before using this skill, you must configure a valid interface key.
1) Get/purchase your key: https://www.musicful.ai/api/authentication/interface-key/
2) Put it into the skill’s `.env` file (this skill reads ONLY the `.env` in the actual skill folder resolved at runtime):
```
<skill_root>/.env  # e.g., ~/.openclaw/workspace/skills/musicful-music-generator/.env
MUSICFUL_API_KEY=YOUR_KEY
MUSICFUL_BASE_URL=https://api.musicful.ai  # optional (default)
```
Notes:
- If you move or copy the skill to a different folder, update that folder’s .env accordingly.
- Optionally, an environment variable MUSICFUL_API_KEY (export) will also be honored if set.

IMPORTANT: If MUSICFUL_API_KEY is missing, the server may respond with HTTP 500. This strongly indicates an auth/config issue.

---

## Suggested Usage Tips
- Be specific about mood, genre, and theme
- Use `mode=bgm` for instrumental‑only output
- Use `mode=lyrics` when you only need text
- Add `style` for stronger genre control
- Add `gender` for vocal songs

Examples of more detailed prompts:
- “Create a nostalgic dream‑pop song about faded photographs”
- “Generate orchestral background music for a fantasy trailer”
- “Write soulful R&B lyrics about regret and forgiveness”

---

## Notes
- Natural language supported; no complex syntax needed
- Song generation is asynchronous; preview may arrive earlier than full
- If a request is ambiguous, the skill may ask for clarification

---

## Files & Endpoints (for reference)
- Two‑stage polling behavior: status=2 (preview), status=0 (full)
- Typical endpoints used under the hood:
  - Generate song/BGM: `POST {BASE_URL}/v1/music/generate`
  - Generate lyrics: `POST {BASE_URL}/v1/lyrics`
  - Task status: `GET {BASE_URL}/v1/music/tasks?ids=<id[,id2,…]>`
- This skill lives in your workspace at:
```
~/.openclaw/workspace/skills/musicful-music-generator/
```
