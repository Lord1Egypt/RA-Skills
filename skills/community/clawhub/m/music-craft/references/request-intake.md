# Request Intake and Output Layout

Full intake protocol (required fields, output location, confidence maps,
language consistency, ambiguous-phrase routing) and the per-song output
file layout (slug rules, version prefixes, reference layout). Load this
when taking a new request or setting up output folders.

## Request Intake

Before asking any question or writing any prompt, run a two-pass intake on the user's request: extract the required fields, then label each one's confidence.

### Required fields checklist

Every request, after auto-detect, should land on this list. Mark each field as one of: **clear**, **inferred**, **missing**, **conflicting**.

| # | Field | What to look for |
|---|---|---|
| 1 | Language | The language of the lyrics and the vocals |
| 2 | Genre / subgenre | Pop, rock, lofi, reggaeton, synthwave, etc. — be specific |
| 3 | Mood | Emotional tone (sad, joyful, dark, hopeful, ...) |
| 4 | Theme | Topic or story (love, summer, road trip, heartbreak) |
| 5 | Vocal mode | Solo vocal, choir, instrumental, spoken word |
| 6 | Lyric source | User-provided, auto-generated, or instrumental-only |
| 7 | Duration | Seconds or minutes; jingle (~30s), standard (~3min), epic (~6min) |
| 8 | Structure | Number and order of sections (intro/verse/chorus/bridge/outro) |
| 9 | References | Named artists, songs, eras, or visual references |
| 10 | **Output location** | Where the audio file (and analysis files) should be saved |

### Output location — ask once, use forever

The output path is part of the intake, not an afterthought. Confirm it before calling `music_generate` and let the user pick a **per-song subfolder** so the project does not end up as a flat folder of 30 MP3s called `final_v3_take2.mp3`.

Default question (ask only if the request is missing it):

> Where should I save this and any analysis files? Two common shapes:
>
> - **Per-song subfolders** (recommended when you are producing multiple versions or songs): `~/Music mix/<project>/<song-slug>/`
>   - Inside the subfolder: the MP3, the analysis JSON (if you used `music-craft-minimax`), the prompt `.txt`, the lyrics `.txt`
>   - Each version of the same song lives in its own subfolder, or stacked under one subfolder with a version suffix on the MP3
> - **Single folder, single file**: a flat path like `~/Music mix/<project>/<song-slug>.mp3`
>
> If you do not have a strong preference, the default is `~/Music mix/<project>/<song-slug>/<song-slug>.mp3` (per-song subfolder).

Conventions the LLM should follow when picking paths itself:

- Slug = lowercase, dash-separated, ASCII-only, ≤ 60 chars (e.g. `two-paths`, `family-acoustic`, `when-you-bleed`)
- Never use a slug starting with `openclaw-` (protected namespace on ClawHub)
- When generating multiple versions of the same song (cover, mashup, style transfer, v2 polished), prefer **stacked** subfolders with versioned MP3s over a single shared folder. Example: `~/Music mix/demo-project/two-paths/M1_synthwave.mp3` and `M2_indiefolk.mp3`
- When the user gives no project name, fall back to the song slug as the project root

If any field is `missing`, that is a question to ask. If any field is `conflicting`, pause and resolve before prompting. If everything is `clear` or `inferred`, the request is ready to translate.

### Confidence map examples

**Request:** *"Canción francesa melancólica, 80 BPM, con voz masculina teatral."*

```
clear:     language=fr, genre=chanson, mood=melancholic, vocal_mode=solo_male, bpm=80
inferred:  theme=romantic, duration=~3min, structure=standard
missing:   lyrics_source
```

**Request:** *"Make a sad Spanish pop song but with upbeat energy."*

```
conflicting: mood (sad vs upbeat)
            → pause, ask: "Sad lyrics with an upbeat tempo, or sad throughout?"
```

**Request:** *"Use these lyrics" (followed by user text)*

```
clear:     lyrics_source=user_provided
inferred:  language (from text), structure (from text length)
missing:   genre, mood, vocal_mode, duration
```

### Language consistency check

The four "languages" of a music request must not contradict each other:

1. **Requested language** — what the user asked for in their message
2. **Lyric language** — the language of the lyrics body
3. **Chorus language** — the language of the chorus (if different from verses, must be intentional)
4. **Tag language** — the section tags like `[Verse]`, `[Chorus]` (always English by convention)

Conflict examples that mean a regeneration is needed:

- User says "Spanish song" but the prompt and lyrics are in English
- Verses are in English and the chorus is in Spanish with no bilingual intent
- The prompt describes French but the lyrics body is Portuguese

Quick check before `music_generate`:

- [ ] Prompt voice line says the same language as the lyric body
- [ ] Chorus language matches verse language unless the song is intentionally bilingual
- [ ] Tags are in English (`[Verse]`, not `[Verso]`)
- [ ] If the user wrote the request in Spanish, the prompt can be in English but the lyrics must be in Spanish

### Routing for ambiguous phrases

Some common phrases hide the real intent. Match the phrase to a route before asking follow-ups.

| User says... | Route | First question to ask (if any) |
|---|---|---|
| "Make a song like X" | Text-only style reference | "Anything from X you want me to lean on — vocals, instruments, era, all of it?" |
| "Use these lyrics" | User-provided lyrics | "What style and voice should it have?" |
| "Instrumental only" / "no vocals" / "background music" | Instrumental / jingle | "What duration and use case?" |
| "Turn this image into music" / "vibe like this" | URL/image enrichment | (analyze the image first, ask only if mood/genre still unclear) |
| "Cover this song" / "in the style of this track" with audio | Audio cover — redirect | "That needs cover / style transfer from audio. Switching to `music-craft-minimax`." |
| "Make a song" / "something for my project" with no other info | Vague request | "Genre, mood, language, or theme you have in mind? Or want me to surprise you?" |

Always enrich before asking when the input is an image or URL. Fetch the page or analyze the image, then route based on what was extracted.

For the full nine input shapes (description, user-lyrics, audio file, YouTube audio, song name, lyrics URL, YouTube metadata, image, genre/cultural) and their routing rules, see [`input-workflows.md`](input-workflows.md).

## Output File Layout (Per-Song Subfolders)

A generation should never land as a stray MP3 at the project root. Always save inside a per-song subfolder so the analysis, the prompt, the lyrics, and every version stay grouped and reviewable.

When an existing song folder contains `info.txt`, use it as prompt-seed context
for BPM, key, instrumentation, source links, and prior prompt history. When it
contains `lyrics_whisper_medium.json`, treat the JSON as a valid transcript
source and use segment timestamps to place section tags when helpful. Cleanup
rules live in [`lyrics-cleanup.md`](lyrics-cleanup.md).

### Recommended layout (per project, per song)

```
<project-root>/                          e.g. ~/Music mix/demo-project/
└── <song-slug>/                        e.g. two-paths/
    ├── <version-prefix>_<style>.mp3    e.g. M1_synthwave.mp3, M2_indiefolk.mp3
    ├── <song-slug>_analysis.json      (only when using music-craft-minimax)
    ├── <song-slug>_lyrics.txt
    ├── <song-slug>_synthwave.txt       (the prompt that generated M1)
    └── <song-slug>_indiefolk.txt       (the prompt that generated M2)
```

### Slug rules

- lowercase, dash-separated, ASCII-only
- ≤ 60 chars
- derived from the song title or filename, not from the analysis run
- never starts with `openclaw-` (ClawHub protected namespace)

### Version prefix convention

When generating multiple versions of the same song (cover, mashup, style transfer, prompt revision), prefix the MP3 with a short label so the user can scan the folder:

| Prefix | When to use |
|---|---|
| `A_` | First attempt, base skill only |
| `B_` | First revision with a different style |
| `C_` | Cover version of an existing track |
| `M1_`, `M2_` | Mashup / mixed source (Song A + Song B) |
| `N1_`, `N2_` | Style transfer to a target style |
| `v2_`, `v3_` | Polish / second take of a previous version |

### Reference project layout (example)

```
~/Music mix/demo-project/
├── first_song/       (7 versions: A, B1, C, M1, M2, N1, N2)
├── acoustic_sketch/  (2 versions: cinematic + base_skill)
├── two_paths/        (2 versions: M1_synthwave, M2_indiefolk)
└── final_theme/      (2 versions: M3_industrial, M4_postpunk)
```

This is the structure the LLM should aim for by default. Ask the user before deviating.
