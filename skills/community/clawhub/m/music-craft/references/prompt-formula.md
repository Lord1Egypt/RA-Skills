# Prompt Formula

The single value this skill adds on top of a raw `music_generate` call is **prompt engineering**. The prompt you pass is not a restatement of the user's words — it is a structured production brief.

## The Formula

```
[Genre/subgenre], [mood], [voice type and language],
[instruments — list EVERY instrument explicitly],
[anti-sparse instruction],
[BPM] BPM in [key],
[structure description with tags],
[dynamic/arrangement instructions],
[production quality],
[things to avoid]
```

Read it as ten slots. Every slot is required unless the field is genuinely not applicable (for example, "voice type" is omitted for instrumentals).

## Slot-by-slot

### 1. Genre / subgenre

Be specific. `pop` is too broad; `modern synth-pop with retro 80s synthwave influences` is actionable.

### 2. Mood

Stack 2–3 adjectives. `melancholic romantic dramatic` works better than `sad`.

For specific emotional delivery, use the descriptors from the emotion recipes below. Vague moods like "emotional" or "moving" are too generic — the model defaults to a "neutral pleasant" register if you don't push it.

#### Emotion quick reference

| Target emotion | Vocal descriptors | Key | BPM |
|---|---|---|---|
| Joy | bright, energetic, smiling, celebratory | major | 110-130 |
| Desperation | strained, raw, falling intonation, urgent | minor | 70-90 |
| Melancholy | breathy, low, slow, wistful, intimate | minor | 60-80 |
| Triumph | powerful, building, declarative, celebratory | major | 100-130 |
| Yearning | breathy, high, sustained, longing | major or minor | 70-90 |
| Anger | aggressive, shouted, sharp, raw | minor | 110-150 |
| Vulnerability | whispered, fragile, intimate, hesitant | minor | 60-80 |
| Confidence | strong, clear, stable, direct | major | 110-130 |
| Nostalgia | warm, gentle, distant, wistful | major | 70-90 |
| Anxiety | tense, sharp, rapid, unstable | minor | 130-160 |
| Hope | bright, rising, ascending, optimistic, building | major | 90-120 |
| Tragic | doomed, fated, resigned, falling intonation, low | minor | 60-80 |
| Heroic | powerful, declarative, march rhythm, building | major | 100-120 |
| Tender | warm, gentle, soft, intimate, stable, affectionate | major | 60-80 |
| Sensual | breathy, low register, slow, sustained, warm, R&B | minor / modal | 60-85 |
| Lonely | breathy, isolated, single voice, low register, falling | minor | 60-80 |
| Playful | bright, bouncy, varied pitch, fun, mischievous | major | 100-130 |
| Haunting | breathy, low register, dissonant, sparse, dark | minor | 60-80 |
| Serene | soft, stable, slow, very low dynamic range, peaceful | major | 50-70 |
| Celebratory | bright, energetic, building, declarative, joyful | major | 110-130 |
| Bittersweet | MIXED: bright verses + dim chorus (or vice versa) | major with minor | 80-110 |

For each emotion, pair the descriptors with the matching lyrics structure and arrangement. The lyrics and arrangement amplify the mood — they don't replace it.

#### Worked example: despairing ballad

❌ Vague: `"Sad song, emotional"`

✅ Specific: `"Desperate, raw, falling intonation, with stretched vowels, building intensity, French chanson"` + lyrics with `"caaaan't goooo on"` + arrangement with `"dramatic strings, sparse piano, building to full band"`

The model receives three coordinated signals (prompt + lyrics + arrangement) that all point at the same emotion. That is what produces a generation that actually sounds desperate.

#### Anti-emotion-flat

The model tends to default to a "pleasant, slightly upbeat" register. To force a specific emotion:

- The model has a bias toward major-key cheerfulness. Explicitly state the target emotion AND the contrasting emotion it should NOT be: `"melancholic and somber, NOT cheerful, NOT uplifting"`.
- For low-energy songs, add the negative explicitly: `"intimate and restrained, NOT anthemic, NOT powerful"`.
- For high-energy anger, specify: `"aggressive and raw, NOT polished, NOT produced"`.

This negative framing is sometimes more effective than positive descriptors.

For the full 21-emotion recipe set with prompt + lyrics + arrangement templates, see the shared reference in [`music-craft-minimax/references/emotion-delivery.md`](../../music-craft-minimax/references/emotion-delivery.md). (This reference is shared between both skills, but lives in the MiniMax skill because the analysis pipeline that feeds it lives there.)

### 3. Voice type and language

For vocals: `passionate theatrical French male vocal`. For instrumentals: omit this slot and add `Instrumental only, no vocals` to the prompt body.

### 4. Instruments

List every instrument you want to hear. This is the most important slot. Anti-sparse rules depend on it.

Format: `accordion, upright bass, orchestral strings, piano, light percussion`. The order is the recommended mix priority (lead first, foundation last).

### 5. Anti-sparse instruction

Required text (vary the wording, keep the meaning):

```
ALL instruments ALWAYS playing throughout the entire song, NEVER go a cappella or silent at any point
```

### 6. BPM and key

`80 BPM in E minor`. Include only if known or confidently inferred from genre. If unsure, drop this slot.

### 7. Structure description

Describe the song shape. Tag-based:

```
intro-verse-pre chorus-chorus-verse-pre chorus-chorus-bridge-chorus-outro with dramatic 1-2 second pauses between sections
```

The corresponding `lyrics` body should use the matching section tags (`[Intro]`, `[Verse]`, `[Pre Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]`, `[Break]`).

### 8. Dynamic and arrangement instructions

How the song breathes. Examples:

- `wide dynamic contrast — quiet intimate verses building to powerful full choruses`
- `build intensity progressively through the song`
- `quiet sections: reduced to piano and bass only, still fully played`

### 9. Production quality

How it should sound. `full production, studio recording quality`. Avoid words like "demo" or "lo-fi in the bad sense".

### 10. Things to avoid

End with the explicit avoid list. Mandatory inclusions:

```
AVOID sparse minimal arrangements, AVOID a cappella sections, AVOID electronic sounds
```

Adapt the last clause (`AVOID electronic sounds`) to the genre — for a synth-pop track you would invert it.

## Prompt Lint

Before generating, sanity-check the prompt against the request:

- **Required production-sheet slots are present.** Genre/subgenre, mood, voice or instrumental mode, instruments, anti-sparse instruction, structure, dynamic/arrangement notes, production quality, and avoid list. If any slot is empty or relies on a missing field, fix the intake first, not the prompt.
- **The anti-sparse guard is explicit.** `ALL instruments ALWAYS playing, NEVER a cappella or silent` is in the prompt body, not implied.
- **Every mood word is grounded.** Each mood, energy, or emotion word is tied to at least one concrete production detail (instrument, rhythm, vocal delivery, arrangement, or mix). Ungrounded mood words are stripped before generation. See "Ground every mood word" in `SKILL.md` for the grounding table.
- **Language is consistent.** The four "languages" of the request must agree:
  - requested language (from the user's message)
  - prompt voice line (the `[voice type and language]` slot)
  - lyrics body language
  - section tag language (always English, e.g., `[Verse]`, not `[Verso]`)
  - Conflict example: user says "Spanish song", prompt says `male vocal in English`, lyrics body is in Spanish. Fix the prompt voice line, not the lyrics.
- **The lyric tags match the structure line.** If slot 7 says `intro-verse-chorus-...-outro`, the lyrics body must use the matching tags.
- **No vague placeholders remain.** Words like `emotional`, `cinematic`, `make it good`, `vibe`, `moody` without grounding, or `nice` are stripped. The model defaults to "neutral pleasant" when given only these.
- **No slot depends on a missing field.** If lyrics source is still `missing`, the prompt is premature. Ask the user, do not guess.
- **The user-provided lyrics are intact.** If the user supplied text, the lyrics body must be their words. Only section tags are added; no paraphrasing.

If any of those checks fail, fix the prompt before calling `music_generate`. If the helper script `music-craft-minimax/scripts/lint_music_request.py` is available in the workspace, use it for quick routing, missing-field, prompt-slot, and `mmx` flag conflict checks; still verify lyrics language, tag-to-structure alignment, and mood grounding manually because the linter is provider-agnostic and does not know the genre-specific rules.

## Worked Examples

### French chanson ballad (user-lyrics)

User request: *"Canción francesa melancólica, 80 BPM, con voz masculina teatral."*

```
French chanson ballad, melancholic romantic dramatic mood, passionate theatrical French male vocal,
accordion, upright bass, orchestral strings, piano, light percussion,
ALL instruments ALWAYS playing throughout the entire song, NEVER go a cappella or silent at any point,
80 BPM in E minor,
intro-verse-pre chorus-chorus-verse-pre chorus-chorus-bridge-break-chorus-outro with dramatic 1-2 second pauses between sections,
wide dynamic contrast — quiet intimate verses building to powerful full choruses, build intensity progressively,
full production, studio recording quality,
AVOID sparse minimal arrangements, AVOID a cappella sections, AVOID electronic sounds, AVOID synthetic textures
```

### Upbeat pop (auto-lyrics)

User request: *"Una pop alegre en español sobre el verano."*

```
Upbeat summer pop, feel-good optimistic mood, bright female vocal in Spanish,
electric guitar, synthesizers, drum machine, bass guitar, handclaps, maracas,
ALL instruments always playing throughout, never drop to a cappella,
120 BPM in C major,
intro-verse-pre chorus-chorus-verse-chorus-bridge-chorus-outro structure with catchy pre-chorus build,
modern radio mix, polished production quality,
AVOID sparse arrangements, AVOID minimalist sections, AVOID dark or moody tones
```

### Rock ballad (user-lyrics in Spanish)

User request: *"Una balada de rock en español, voz rasgada, sobre una ruptura."*

```
Emotional Spanish rock ballad, intense passionate mood, raspy male vocal in Spanish,
electric guitar, acoustic guitar, drums, bass, piano, strings in climax,
ALL instruments always present, never a cappella or silent,
76 BPM in D minor,
slow build from intimate verse to explosive chorus, wide dynamic range, raw emotional delivery,
studio quality recording, warm analog mix,
AVOID sparse, AVOID a cappella, AVOID minimalist
```

### Instrumental cinematic

User request: *"Necesito una intro cinematográfica para un vídeo de YouTube, 30 segundos, sin voz."*

```
Instrumental only, no vocals, no lyrics. Cinematic orchestral, epic and building,
full symphony orchestra with strings, brass, timpani, woodwinds, piano, French horn,
ALL instruments always playing, NEVER drop to silence or single instrument,
90 BPM in B minor, slow emotional build to thunderous climax,
wide cinematic soundscape, studio quality,
AVOID sparse, AVOID minimal, AVOID silence
```

## Failure Modes and Fixes

| Output looks like... | Fix |
|---|---|
| Sparse or a cappella mid-track | Reinforce slot 5 (anti-sparse) and slot 4 (instruments) — list them again with "ALWAYS playing" |
| Clipped vocals or distorted mix | Add `clean mix, no distortion` to slot 9 and remove any `raw`, `gritty`, `lo-fi` words |
| Wrong genre despite correct prompt | The provider may not support the genre. Switch to a closer supported style, or move to `music-craft-minimax` for finer control |
| Repeated chorus where it shouldn't | Check that the lyrics body has the right section tags and matches the structure description in slot 7 |
| Too short | Add more sections to the lyrics body. Most generators extend length with more tagged content |
| Too long | Trim sections from the lyrics body, or drop a `[Verse]` and `[Chorus]` repetition |

## Backend-Specific Prompt Length Limits

Keep prompts short enough for the selected backend:

- **MiniMax/mmx:** safest around 1000-1550 UTF-8 bytes; warn above 1800 bytes; shorten before 2000 bytes. Use `music-craft-minimax/scripts/lint_music_request.py` when that skill is available.
- **ACE-Step:** keep `prompt` as music tags and put lyrics in the separate `lyrics` field. If using `/format_input`, review the optimized result too because the LM can expand the text.
- **Stable Audio 3:** keep prompts concise and instrumental-focused; test exact limits when using local SA3.
- **MusicGen:** short natural-language descriptions work better than long production sheets.

When a prompt is too long, shorten by removing duplicate adjectives, moving lyrics to a lyrics field/file when supported, and keeping numeric facts in backend parameters (`bpm`, `key_scale`, `audio_duration`, `--bpm`, `--key`, `--structure`) instead of repeating them in prose.

If `music-craft-minimax` is installed, its `scripts/lint_music_request.py` helper is the canonical guard for mmx prompt size, missing fields, and prompt/flag conflicts.

## Boundaries

This formula is designed for the basic `music_generate` tool across providers. It packs everything into one prompt string. If the provider supports separate flags (BPM, key, structure, avoid), `music-craft-minimax` uses them as separate parameters for more precise control.
