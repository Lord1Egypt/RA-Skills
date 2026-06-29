# Cover Workflow

Cover workflow preserves the original song's melody while applying a different style. This is the feature that lets you turn a rock track into a French chanson version, a reggaeton track into a ballad, or any other style transfer while keeping the original recognisable.

## When to Use Cover

- The user has reference audio (a local file) and wants to keep the melody
- The user wants to change style, era, or genre of an existing song
- The user wants a "what if" reimagining (what if Bohemian Rhapsody was bossa nova?)

## When NOT to Use Cover

- The user wants to write a new song inspired by another (use standard generation with references)
- The user wants to combine two songs into one (use mashup workflow)
- The user only wants to change tempo or key (use standard generation with those parameters)
- The user does not have reference audio and just describes a style (use standard generation)

## Two Cover Backends

> **Two cover backends exist — pick by what's available:**
> - **MiniMax cloud cover** (this skill): run `music cover` through
>   `scripts/generate_with_retry.py`, melody-preserving via MiniMax's
>   `music-cover` model. Needs `MINIMAX_API_KEY` and network access to MiniMax.
> - **Local ACE-Step cover** (in [`music-craft`](../../music-craft/)): `task_type=cover` with the
>   source audio uploaded (multipart) and `audio_cover_strength` controlling how far to restyle.
>   Fully local, no cloud, follows the source melody/structure. Caveat: a full-length cover is
>   slow and VRAM-heavy on a ~12 GB GPU and can hit the server's 600 s generation timeout —
>   cover a shorter segment or raise `ACESTEP_GENERATION_TIMEOUT`. See music-craft's
>   "ACE-Step Audio-Conditioned Generation" section.
>
> So if MiniMax is unavailable (no key, CLI missing, or API access unavailable), you can **still do a
> melody-aware cover locally** with ACE-Step — it is not cloud-only. Only pure text-prompt
> generation (no source audio) is a "reimagining" rather than a cover.

## Cloud Transmission Consent

> ⚠️ **Both cover backends may transmit your audio to MiniMax.** The
> cloud `music cover` path uploads the source file; the local ACE-Step
> path stays on your machine. Before running a cloud cover with
> sensitive, private, or third-party-owned audio, confirm:
>
> 1. You have the right to upload this audio to MiniMax.
> 2. You accept that MiniMax may retain derived features (`cover_feature_id`,
>    extracted lyrics, structure metadata) for up to 24 hours.
> 3. The audio is not subject to a license that prohibits cloud processing.
>
> If any of these are unclear, use the local ACE-Step cover path instead.

## Two Paths: One-Step vs Two-Step

### One-Step (Quick)

```bash
python3 scripts/generate_with_retry.py \
  --output-path /tmp/cover.mp3 \
  -- \
  music cover \
  --prompt "French chanson, accordion, strings, passionate French vocal, 80 BPM" \
  --audio-file /tmp/original.ogg \
  --out /tmp/cover.mp3
```

**What happens:**

1. MiniMax loads the local audio file you point at.
2. Extracts lyrics via ASR (automatic speech recognition).
3. Detects the structure (verse / chorus / bridge).
4. Applies the target style while preserving the melody.
5. Returns the cover.

Run one cover at a time. If you need multiple variants, use
`scripts/batch_cover.py --dry-run` first, then execute the sequential batch.

**Limitations:**

- ASR may mis-hear lyrics, especially in noisy or non-English audio.
- The detected structure may not match the user's intent.
- No way to edit lyrics before generation.

### Two-Step (More Control)

**Step 1: Preprocess the audio**

The preprocess step returns a `cover_feature_id` (valid 24 hours) plus the auto-extracted `formatted_lyrics` and a `structure_result` with section timestamps.

```bash
curl --request POST \
  --url https://api.minimax.io/v1/music_cover_preprocess \
  --header "Authorization: Bearer $MINIMAX_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "music-cover",
    "audio_url": "file:///tmp/original-song.mp3"
  }'
```

Note: in v1.5.0+ `audio_url` must point to a local file the MiniMax API can read (e.g. `file:///tmp/...`). Public streaming URLs (YouTube, JioSaavn, mx3.ch) are no longer accepted — download the file with the private `music-source-fetch` skill first, then reference it here.

The response includes:

- `cover_feature_id` — valid 24 hours, use in step 2
- `formatted_lyrics` — editable, with structure tags
- `structure_result` — JSON with section timestamps

Note: do NOT use `mmx music cover` here. The mmx cover subcommand is the one-step path. For two-step, you must call `music_cover_preprocess` directly to get the `cover_feature_id` for step 2.

**Step 2: Generate cover with modified lyrics**

```bash
curl --request POST \
  --url https://api.minimax.io/v1/music_generation \
  --header "Authorization: Bearer $MINIMAX_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "music-cover",
    "cover_feature_id": "ID_FROM_STEP_1",
    "lyrics": "[Verse]\nModified French lyrics here\n\n[Chorus]\nMore lyrics",
    "prompt": "French chanson, accordion, strings, passionate vocal",
    "output_format": "url",
    "audio_setting": { "sample_rate": 44100, "bitrate": 256000, "format": "mp3" }
  }'
```

**What the two-step path gives you:**

- Edit the ASR'd lyrics before generation (fix errors, change wording, add structure tags)
- Use a different language (translate the original lyrics to the target language)
- Use no lyrics at all (just preserve the melody, instrumental cover)
- Use external lyrics (the user provided their own)

## Lyrics Strategies for Cover

### Same Lyrics, New Style

The user wants the same words, different style. Workflow:

1. Use one-step or two-step.
2. Pass the prompt for the new style.
3. Let MiniMax extract the lyrics (one-step) or use the user's lyrics (two-step with `--lyrics`).

### New Lyrics, Same Melody

The user wants different words in the same melody. Workflow:

1. Use two-step (you need to provide the new lyrics).
2. Preprocess to get the `cover_feature_id`.
3. Provide the new lyrics in the generation call.

Example: Take the melody of "Yesterday" by the Beatles and set new lyrics in Spanish about a modern-day break-up.

### Translated Lyrics

The user wants the original lyrics in a different language. Workflow:

1. Use two-step.
2. Translate the original lyrics yourself (or with the LLM).
3. Pass the translated lyrics in the generation call.

### No Lyrics (Instrumental Cover)

The user wants the melody as an instrumental. Workflow:

1. Use one-step with `--instrumental` flag, or
2. Use two-step with empty lyrics in the generation call.

## Style Transfer Without Melody Preservation

If the user wants the *style* of Song A applied to *new* lyrics (not preserving the melody), use standard generation with the style as a reference:

```bash
mmx music generate \
  --prompt "Style: similar to Bohemian Rhapsody (epic rock, multi-section, choir, dramatic dynamics), but with original lyrics in Spanish about leaving home" \
  --lyrics "..." \
  --model music-2.6 \
  --out /tmp/song.mp3
```

This is NOT a cover — the melody is new, the style is borrowed.

## Cover Workflow with a Local File

The source for a cover must be a local audio file path. URLs are not
accepted in v1.5.0+.

If your source is a YouTube/JioSaavn/mx3.ch URL, download it first with
the private `music-source-fetch` skill, then pass the resulting local
file to this workflow.

## Audio Input Limits

- **Minimum length:** 6 seconds
- **Maximum length:** 6 minutes
- **Maximum file size:** 50 MB
- **Supported formats:** mp3, wav, flac, ogg, m4a, and others

If the input is too long, trim it. If too large, convert to a lower bitrate.

## Cover Feature ID Lifecycle

`cover_feature_id` is valid for 24 hours from the preprocess call. After that, you need to re-preprocess.

If you need to regenerate the same cover multiple times (e.g., to iterate on the prompt), cache the `cover_feature_id` and reuse it.

## Quality Verification for Covers

After generating a cover, check:

1. **Melody recognisability** — Would a friend say "That's [Song X]"?
2. **Style application** — Would a friend say "but it sounds like [style Y]"?
3. **Lyrics alignment** — Are the lyrics recognisable (either the original or the new ones)?
4. **Structure preservation** — Does the new version follow the original's structure (verse-chorus-verse-chorus-bridge-chorus)?
5. **No a cappella or sparse drops** — Same anti-sparse rules as standard generation

If 3+ of these fail, adjust the prompt or try the two-step path for more control.

## Anti-Sparse for Covers

The anti-sparse rules apply even more strictly to covers, because the cover is changing style and the model can interpret "intimate ballad version" as "remove all instruments".

Always include in the cover prompt:

```
ALL instruments ALWAYS playing throughout, NEVER go a cappella or silent,
quiet sections: reduced to [specific instruments] only, still fully played
```

And in `--avoid`:

```
sparse, a cappella, minimal, silence, electronic sounds (unless desired)
```

## Errors and Recovery

| Error | Cause | Fix |
|---|---|---|
| `audio_url unreachable` | Local file path is wrong, file is unreadable, or it was a streaming URL | Confirm the file exists and is readable; if you only had a streaming URL, fetch it first with `music-source-fetch` |
| `audio too long` | Source > 6 minutes | Trim with `ffmpeg -ss <start> -t <duration>` |
| `audio too large` | Source > 50 MB | Convert to lower bitrate with `ffmpeg` |
| ASR extracted wrong lyrics | Noisy audio, accented vocals, non-English | Use two-step with manual lyrics |
| Output melody is unrecognisable | Style transfer too aggressive | Reduce the prompt's style intensity, or use a less dramatic target style |
| Output is sparse | Anti-sparse rules not applied | Add explicit instruments and "ALL instruments ALWAYS playing" |

## Worked Example: Rock to Chanson

User request: "Take this rock anthem I wrote and turn it into a French chanson."

Workflow:

1. Get the audio file (user upload, or a local file fetched with `music-source-fetch` from a URL).
2. Preprocess:
   ```bash
   python3 scripts/generate_with_retry.py \
     --output-path /tmp/chanson_cover.mp3 \
     -- \
     music cover \
     --prompt "French chanson, accordion, upright bass, orchestral strings, piano, light percussion, 80 BPM in E minor, passionate French male vocal, melancholic romantic dramatic" \
     --audio-file /tmp/rock_track.mp3 \
     --lyrics "[Verse]\nJ'ai trouvé ta lettre\nMais je n'ai pas vraiment vérifié\nCe mot unique que tu as écrit\nL'histoire est déjà terminée\n\n[Pre Chorus]\nNon, je ne veux pas connaître les raisons\nCar l'amour n'a pas besoin de raison pour exister\n\n[Chorus]\nJe sais que je, je sais que je, je ne peux pas continuer avec toooooou" \
     --out /tmp/chanson_cover.mp3
   ```
3. Verify melody is recognisable.
4. If sparse, retry with explicit anti-sparse text.
5. Deliver the cover.
