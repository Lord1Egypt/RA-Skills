---
name: music-generator
description: |
  Generate AI music or lyrics from natural language with a single sentence. The system auto-detects
  whether to create a vocal song or pure instrumental BGM, and automatically polls the task: it
  returns a preview link first, then the final downloadable audio link.
author: Musicful
---

# Music Generator Skill (Full SOP)

## Capability Overview
This skill supports the following intents:
1) Generate a full song with lyrics
2) Generate pure background music (BGM)
3) Generate lyrics only (no audio)
4) Query music generation task status

Users can describe the music they want in plain language. The system auto-determines the mode and
handles parameter inference and task tracking.

---

## Triggers and Natural Language Examples
The following natural language requests will trigger this skill:
- Generate a romantic love song
- Write lyrics about the night sky
- Create electronic music suitable for short‑video background
- Check my music generation progress
- I want a cheerful background music track

---

## Execution (SOP Step‑by‑Step)

### Preflight Check (Mandatory)
- Read MUSICFUL_API_KEY from the skill folder’s .env (resolved at runtime via the running script path): <skill_root>/.env
  - If not configured (empty/missing), immediately inform the user:
    - "MUSICFUL_API_KEY is not configured. Please visit https://www.musicful.ai/api/authentication/interface-key/
      to obtain/purchase an interface key, then write the KEY into <skill_root>/.env under MUSICFUL_API_KEY."
  - Stop subsequent calls and wait for the user to complete configuration before continuing.

The execution flow is intent‑based and incorporates a two‑stage return and a "lyrics‑first" UX:
- Single command entry: /music_generator, with mode branch control:
  - mode=normal (default): generate and show lyrics → submit generation → return preview (status=2) →
    return final (status=0)
  - mode=bgm: pure music (instrumental=1), no lyrics → preview first → then final
  - mode=lyrics: return lyrics text immediately
- When using the "custom lyrics" path (built into the normal flow or future extensions): submit generation
  directly and poll (preview first, then final)

---

## Scenario A: Generate a Full Song with Lyrics
Typical user inputs:
- Generate a romantic electronic song
- Write a sad rock song and generate audio
- Here are some lyrics, please use them to create the song: [...user‑provided lyrics...]

### Detailed Flow
**Step 1: Intent Recognition**
- If the user provides complete lyrics, treat it as lyrics‑provided generation;
- Otherwise, assume lyrics need to be generated automatically and then used to synthesize the song.

**Step 2: Lyrics Handling**
- If lyrics are provided → use them directly;
- If not provided → call the V1 Lyrics API to generate lyrics content;

**Step 3: Submit Music Generation Task**
- POST {BASE_URL}/v1/music/generate
- body: `{ action: "custom", lyrics: "<lyrics>", style: "<inferred from user>", mv: "<default to latest high‑quality model>" }`

**Step 4: Automatic Task Polling (Two Stages)**
- GET {BASE_URL}/v1/music/tasks?ids=<task_id[,task_id2,…]>
- Status semantics (key):
  - status = 2 → preview stage complete (returns `audio_url` as preview link)
  - status = 0 → full audio complete (returns `audio_url` as downloadable final link)
  - others → processing or failed (use `fail_code`/`fail_reason`)
- Polling strategy:
  1) On first status=2: immediately announce "preview is ready" and return `audio_url` for listening;
  2) Continue polling until status=0: then return "final audio is ready" with `audio_url` (download/publish).

**Step 5: Return Results to the User (Two‑Stage × Two Songs)**
- The system by default generates two songs/two task_ids (e.g., ids=[id1,id2]). For each id, perform the
  two‑stage return independently:
  - Stage 1: when this id reaches status=2 → return the preview link (audio_url)
  - Stage 2: keep polling this id → when status=0 → return the full mp3 download link (audio_url)
- Recommended output format (one block per song):
  - title: <title>
  - prompt: <original user description>
  - lyrics: <full lyrics for lyric mode; empty for BGM>
  - preview: <preview link (status=2)>
  - full: <final mp3 (status=0)>

---

## Scenario B: Generate Pure Background Music
:white_check_mark: Typical user inputs:
- Generate a piece of pure background music
- I want an electronic instrumental suitable for video background

### Detailed Flow
**Step 1: Intent Recognition**
- Detect semantics like "pure music/background music/accompaniment" → enter the pure BGM flow.

**Step 2: Submit Music Generation Task**
- POST {BASE_URL}/v1/music/generate
- body: `{ action: "auto", style: "<inferred from user>", mv: "<default latest model>", instrumental: 1 }`

**Step 3: Automatic Task Polling (Two Stages)**
- Same as Scenario A: status=2 → preview; status=0 → full

**Step 4: Return Preview & Final Links (Two Steps)**
- Stage 1: preview link (status=2)
- Stage 2: final link (status=0)

---

## Scenario C: Generate Lyrics Only
:white_check_mark: User inputs:
- Write lyrics about a summer beach
- I only need lyrics, about a rainy day

### Process
- POST {BASE_URL}/v1/lyrics body: `{ prompt: "<user description>" }`
- Return: `{ lyrics: "<AI‑generated lyrics>" }`

---

## Scenario D: Query Music Generation Task Status
:white_check_mark: User inputs:
- Check the progress of task_id=abc123
- See how far my song generation has progressed

### Detailed Flow
1. Extract task_id from the user input;
2. GET {BASE_URL}/v1/music/tasks?ids=<task_id>
3. Return task status and audio information.

---

## Parameter Inference Rules
| Parameter       | Source                   | Default/Notes                  |
|-----------------|--------------------------|--------------------------------|
| `style`         | Inferred from user input | Default to Pop/general if none |
| `mv`            | Default high‑quality     | Prefer latest high‑quality     |
| `instrumental`  | Set to 1 for BGM         | Otherwise 0                    |
| `lyrics`        | User‑provided / auto     | —                              |
| `title`         | Inferred or auto‑named   | —                              |

> BASE_URL and API Key:
> - MUSICFUL_BASE_URL (default: https://api.musicful.ai)
> - MUSICFUL_API_KEY (read from the skill folder’s .env; environment variable MUSICFUL_API_KEY is also honored if set)
> - Entry points: scripts/musicful_api.py, CLI: scripts/run_musicful.py / scripts/dispatch_music_generator.py
> - Important: ensure MUSICFUL_API_KEY is configured before calling; if missing, the server may respond with HTTP 500 (helps pinpoint auth/config issues quickly).

---

## Error Handling and Fallback
1. If the request is unclear (e.g., "generate music" without clarifying lyrics vs BGM) → ask a follow‑up;
2. If the API call fails → return clear failure reason and suggestions;
3. If polling times out → prompt the user to wait or retry.

---

## Unified Return Format
Success:
```json
{ "status": "success", "data": { ... } }
```
Error:
```json
{ "status": "error", "message": "<reason>" }
```

## Example Dialogues
- User: Generate a sad rock song
- Skill: Shows generated lyrics → submits job → returns preview link → returns full mp3 link

- User: An ambient BGM for a quiet night
- Skill: Submits job (instrumental=1) → returns preview → returns full

- User: Write lyrics about the night sky
- Skill: Returns generated lyrics
