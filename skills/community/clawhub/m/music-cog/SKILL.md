---
name: music-cog
description: "AI music generation powered by CellCog. Original instrumental and vocal tracks, 5 seconds to 10 minutes. Cinematic scores, background tracks, podcast intros, game soundtracks, ambient soundscapes, jingles, lo-fi beats, orchestral compositions, songs with lyrics. Royalty-free."
metadata:
  openclaw:
    emoji: "🎶"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---
# Music Cog - Original Music, Fully Yours

Music generation — 5 seconds to 10 minutes. Instrumental and vocal tracks with high-quality AI vocals.

Generated tracks are royalty-free for commercial use per CellCog's terms of service — YouTube, podcasts, apps, games, ads, films, streaming.

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
print(result["message"])
```


---

## Two Ways to Create Music

### Simple Prompt (Use This 99% of the Time)

Just describe what you want. The model handles the rest — genre, arrangement, instrumentation, dynamics, and even lyrics:

> "Compose a 90-second cinematic score. Start with solo piano, layer in strings at 30 seconds, build to a full orchestral swell, then resolve softly. Mood: bittersweet turning hopeful."

> "Create a 3-minute lo-fi hip-hop track with soft piano, vinyl crackle, and mellow drums. 75 BPM. Study vibes."

> "Write a 2-minute upbeat pop song with female vocals about starting fresh on a Monday morning. Catchy chorus, feel-good energy."

The model is exceptionally sophisticated — it handles any genre, genre fusion, songs with lyrics, complex arrangements, and mood transitions from a simple description.

### Composition Plan (For Precise Timing Control)

Only use this when you need **exact section durations** — for example, syncing music to specific video segments or presentation slides:

> "I need music that syncs with my video:
> - Intro: exactly 10 seconds, soft ambient
> - Build: exactly 20 seconds, energy rising
> - Climax: exactly 15 seconds, full orchestra
> - Outro: exactly 10 seconds, gentle fade"

This mode gives precise timing control per section but should only be used when timing accuracy matters for syncing with other media.

---

## What Music You Can Create

### Instrumental

| Type | Example |
|------|---------|
| **Cinematic scores** | Epic orchestral, tense thriller, emotional piano, sci-fi ambient |
| **Background tracks** | Lo-fi beats, corporate background, cafe jazz, ambient soundscapes |
| **Podcast intros/outros** | 5-10 second branded stings, transitions, bumpers |
| **Game soundtracks** | Battle themes, exploration music, boss fights, menu themes |
| **Jingles** | Ad jingles, notification sounds, reveal stingers |
| **Ambient** | Meditation, nature soundscapes, focus music |

### Vocal Tracks

CellCog generates songs with **perfect AI vocals** — just describe the lyrical theme:

| Type | Example |
|------|---------|
| **Pop songs** | Catchy hooks, verse-chorus structure, radio-ready |
| **Ballads** | Emotional, piano-driven, storytelling |
| **Hip-hop/Rap** | Rhythmic vocals, beats, flow |
| **Rock** | Guitar-driven, powerful vocals |
| **R&B/Soul** | Smooth, melodic, groove |

---

## Specs

| Parameter | Range |
|-----------|-------|
| **Duration** | 5 seconds to 10 minutes |
| **Output** | MP3 (44.1kHz, 128kbps) |
| **Vocals** | Instrumental or with AI vocals |
| **Licensing** | Royalty-free per CellCog terms of service |

---

## Chat Mode

**Use `chat_mode="agent"`** for music generation. Music executes well in agent mode.

---

## Example Prompts

**Cinematic score:**
> "Compose a 2-minute cinematic score for a nature documentary finale. Begin with solo cello (melancholic), layer in strings and piano at 40 seconds, build to a hopeful orchestral swell, resolve with gentle piano. Think Planet Earth meets Interstellar."

**Lo-fi background:**
> "Create 5 minutes of lo-fi study beats. Soft piano, mellow drums, vinyl crackle, gentle bass. 75 BPM. Warm and unobtrusive — good for focus."

**Podcast intro + outro:**
> "Create a podcast intro (8 seconds) and outro (6 seconds). Show is a tech startup podcast. Intro: energetic, modern electronic with a hook. Outro: same vibe but mellower wind-down. Should feel like the same show."

**Song with vocals:**
> "Write a 3-minute upbeat indie pop song with female vocals. Theme: the excitement of moving to a new city. Catchy chorus, acoustic guitar foundation, builds with drums and synth. Feel-good, sing-along energy."

**Game soundtrack:**
> "Compose a 2-minute boss battle theme for a fantasy RPG. Intense orchestral with choir, driving percussion, escalating tension. Think Dark Souls meets Final Fantasy."

---

## Tips

1. **Describe the feeling, not just the genre**: "Music that makes a startup pitch feel like the future" works better than "electronic music."

2. **Specify duration**: "45 seconds" vs "3 minutes" changes composition structure significantly.

3. **Reference moods, not copyrighted songs**: "Hans Zimmer-style epic" and "ChilledCow lo-fi vibes" work well. Do not reference specific copyrighted songs.

4. **For vocals**: Set the lyrical theme and mood. The model writes lyrics that fit. Or provide specific lyrics you want sung.

5. **Energy arc matters**: "Starts quiet, builds at midpoint, resolves softly" gives clear compositional structure.

6. **For video background music**: If the music is for a CellCog video, mention it in your video prompt instead — CellCog handles music as part of video production automatically.

---

## If CellCog is not installed

Run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool) to install and authenticate.
**OpenClaw users:** Run `clawhub install cellcog` instead.
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.
