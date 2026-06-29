# mmx CLI Flag Reference

The `mmx` CLI exposes MiniMax Music 2.6 parameters as separate flags, giving finer control than packing everything into a single prompt string. This is the full reference.

## Installation and Auth

```bash
# Check installation
mmx --version
mmx music generate --help

# Check auth
mmx auth status

# Login with API key
mmx auth login --api-key "$MINIMAX_API_KEY"

# Set region (if needed)
mmx config set --key region --value global
```

## Command: Standard Generation

```bash
mmx music generate \
  --prompt "..." \
  --lyrics "..." \
  --vocals "..." \
  --genre "..." \
  --mood "..." \
  --instruments "..." \
  --bpm <number> \
  --key "..." \
  --structure "..." \
  --avoid "..." \
  --model music-2.6 \
  --out /tmp/song.mp3
```

## All Flags

| Flag | Required | Description | Example |
|------|----------|-------------|---------|
| `--prompt` | Yes | Music style description, max 2000 chars | `"French chanson, melancholic"` |
| `--lyrics` | One of lyrics/instrumental/optimizer | Song lyrics with structure tags, max 3500 chars | `"[Verse]\nJ'ai trouvé..."` |
| `--lyrics-file` | Alt to `--lyrics` | Read lyrics from file | `song.txt` or `-` for stdin |
| `--instrumental` | Alt to `--lyrics` | No vocals | (flag only) |
| `--lyrics-optimizer` | Alt to `--lyrics` | Auto-generate lyrics from prompt | (flag only) |
| `--vocals` | Optional | Vocal style | `"passionate French male vocal"` |
| `--genre` | Optional | Music genre | `"french chanson"` |
| `--mood` | Optional | Mood/emotion | `"melancholic romantic dramatic"` |
| `--instruments` | Optional | Featured instruments | `"accordion, piano, strings"` |
| `--tempo` | Optional | Tempo description | `"slow"`, `"moderate"`, `"fast"` |
| `--bpm` | Optional | Exact BPM | `80` |
| `--key` | Optional | Musical key | `"E minor"`, `"C major"` |
| `--avoid` | Optional | Elements to avoid (comma-separated) | `"sparse, a cappella, electronic sounds"` |
| `--use-case` | Optional | Context | `"background music for film"` |
| `--structure` | Optional | Song structure | `"verse-chorus-bridge-chorus"` |
| `--references` | Optional | Reference artists or tracks. In batch work, inline concise references in `--prompt` if this flag appears flaky. | `"similar to Édith Piaf"` |
| `--extra` | Optional | Additional requirements | `"wide dynamic contrast"` |
| `--model` | Optional | Model name | `music-2.6` (paid) or `music-2.6-free` (lower RPM) |
| `--output-format` | Optional | `hex` (default) or `url` (24h expiry) | `hex` |
| `--out` | Optional | Output file path | `/tmp/song.mp3` |
| `--stream` | Optional | Stream raw audio to stdout | (flag only) |
| `--seed` | Optional | Reproducible seed (0–1,000,000) | `42` |
| `--timeout` | Optional | CLI request timeout | `--timeout 600` for long generations |
| `--cover-feature-id` | Optional | Use a preprocessed cover (two-step workflow) | (from preprocess call) |

## Structure Tags (in `--lyrics`)

```
[Intro]        Opening section
[Verse]        Main verse
[Pre Chorus]   Build before chorus
[Chorus]       Main hook
[Interlude]    Instrumental break
[Bridge]       Contrast section
[Outro]        Closing section
[Post Chorus]  After-chorus
[Transition]   Connective passage
[Break]        Dramatic pause or silence
[Hook]         Catchy repeated motif
[Build Up]     Tension building before climax
[Inst]         Instrumental section
[Solo]         Instrument solo
```

**Rules:**

- Tags must be clean — no descriptions inside brackets (they get sung).
- Separate sections with blank lines.
- Use `\n` for line breaks in `--lyrics` flag.

Full tag reference with timing and effects: see [`../music-craft/references/structure-tags.md`](../../music-craft/references/structure-tags.md).

## Anti-Sparse Flags

The `--avoid` flag is the primary anti-sparse lever. Recommended text:

```
--avoid "sparse, a cappella, minimal arrangement, electronic sounds, synthetic textures"
```

For sparse-friendly genres (ambient, ballad, lofi), add explicit instruments in `--instruments` to compensate:

```bash
--instruments "piano, soft pads, sustained strings, gentle bass, light percussion, ambient textures" \
--avoid "sparse, a cappella, minimal, silence" \
--extra "quiet sections: reduced to piano and bass only, still fully played, NEVER silent"
```

## Worked Example: French Chanson Ballad

```bash
mmx music generate \
  --prompt "French chanson ballad, melancholic romantic mood, passionate theatrical French male vocal, accordion, upright bass, orchestral strings, piano, light percussion — ALL instruments ALWAYS playing throughout, NEVER go a cappella or silent, dramatic 1-2s pauses between sections, wide dynamic contrast, build from quiet verses to powerful choruses, full production, studio recording quality" \
  --lyrics "[Intro]
[Break]

[Verse]
J'ai trouvé ta lettre
Mais je n'ai pas vraiment vérifié

[Pre Chorus]
Non, je ne veux pas connaître les raisons

[Build Up]

[Chorus]
Je sais que je, je sais que je, je ne peux pas continuer avec toooooou

[Break]

[Verse]
Depuis que je t'ai vu
Je savais que tu ne me conviendrais pas

[Pre Chorus]
Non, je ne veux pas connaître les raisons

[Build Up]

[Chorus]
Je sais que je, je sais que je, je ne peux pas continuer avec toooooou

[Bridge]
Et je voulais toujours que tu partes pendant que je dormais
Il n'y a pas de sortie facile

[Break]

[Chorus]
Je sais que je, je sais que je, je ne peux pas continuer avec toooooou

[Outro]
Non, je ne regrette rieeeen" \
  --vocals "passionate theatrical French male vocal" \
  --genre "french chanson" \
  --mood "melancholic romantic dramatic" \
  --instruments "accordion, upright bass, orchestral strings, piano, light percussion" \
  --bpm 80 \
  --key "E minor" \
  --structure "intro-verse-pre-chorus-chorus-verse-pre-chorus-chorus-bridge-break-chorus-outro" \
  --avoid "sparse, a cappella, minimal arrangement, electronic sounds, synthetic textures" \
  --model music-2.6 \
  --out /tmp/song.mp3
```

## When to Use `--seed`

The `--seed` flag makes the generation reproducible. Same prompt + same seed = same output. Use when:

- iterating on a prompt and you want to compare versions with one variable changed
- debugging — a "bad" output is reproducible so you can adjust
- teaching — students can replay the same example

For exploratory generation, omit the seed and let MiniMax surprise you.

## When NOT to Use `mmx`

Use `mmx` when you need fine control over specific parameters. Use the `music_generate` tool with prompt-only when:

- the runtime already configures MiniMax with sensible defaults
- you do not need separate `--bpm`, `--key`, `--structure` flags
- the user does not care about exact BPM (just "slow" or "fast")
- you want the workflow to be portable across providers (skill 1 path)

Both produce equivalent results if the prompt and flags are aligned. The difference is in how the parameters are expressed, not in the output quality.

## Song Length (`--length` Is a Hint, Not a Guarantee)

Unlike `music-craft`'s ACE-Step backend (which takes `audio_duration` as a strict parameter), `mmx music generate --length` accepts milliseconds as a **duration hint**. It is useful, but it is not precise. Output length is determined by:

- **Lyrics length** (primary): each `[Verse]`/`[Chorus]` section takes ~15-30 seconds depending on word count and singing pace. A typical 3:30 song has ~150-200 lyrics words across 2 verses + 2 choruses + bridge.
- **Structure tags**: `[Intro]`, `[Instrumental Break]`, `[Outro]` add silent/sparse sections that extend total length without lyrics.
- **`--length` and prompt hints** (secondary): `--length 180000` and phrases like "3 minute song" nudge the model toward that length.
- **BPM and section count** (minor effect): faster BPMs and more sections tend to produce slightly longer outputs.

**Practical recipe for a full 3:30 song:**
1. Lyrics: ~150-200 words with `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[Verse 2]`, `[Bridge]`, `[Outro]` tags (full song structure, not just one chorus)
2. Prompt: include structure hints like `"full 3-minute song with intro, 2 verses, 2 choruses, bridge, and outro"` or use `--structure "intro-verse-pre_chorus-chorus-verse-chorus-bridge-chorus-outro"`
3. Check output length — if it's a 1-minute hook, the lyrics are probably too short
4. If output is too short: regenerate with longer lyrics (the model can't add sections that aren't in the lyrics)
5. If output is too long: trim lyrics to ~120 words or add `[Instrumental Break]` tags to control pacing

**Don't expect mmx to hit 3:30 exactly.** In the 2026-06-12 field run, cloud outputs ranged from 57-135% of requested duration: 12/18 truncated, 3/18 close, and 3/18 extended. If you need precise length, ACE-Step is the right tool (it has `audio_duration`). If you want MiniMax's speed and the song length is flexible, mmx is fine.

For the full local-vs-cloud duration table, see [`minimax-generation-caveats.md`](minimax-generation-caveats.md).

## mmx Music Generation — verified patterns (June 2026)

End-to-end verified invocation patterns. Save outputs into a per-song folder such as `~/Music mix/<project>/<song-slug>/`.

For reliability during standard cloud batches, prefer prompts under about 500
characters and inline reference artists in the prompt. See
[`short-prompt-recipes.md`](short-prompt-recipes.md).

### Pattern A — Full Song with Detailed Prompt + 6 Metas (Production-Grade Output)

```bash
mmx music generate \
  --prompt "dream pop reimagining, shoegaze-influenced indie rock turned ethereal and cinematic.
My Bloody Valentine meets Slowdive meets Radiohead.
Male lead vocal, breathy and vulnerable, double-tracked with slight detuning and tape warmth.
Wall of clean electric guitars with heavy chorus pedal and tremolo picking.
Shimmering washes of reverb, sub-bass synth pad foundation, soft brushed electronic drums.
Glockenspiel and celesta melody line high above the mix.
Organ pads swelling at choruses, reversed guitar samples between sections.
Heavy reverb and analog warmth throughout, lo-fi texture.
Emotional arc: hazy drifting opening building wave confusion overwhelming beautiful climax fading dreamlike denouement outro.
Avoid: sharp percussive agresivo distortion clear upfront vocals minimal sparse.
Tempo 96 BPM in D major, dreamlike half-time feel.
Suitable as a slow-burn alt-pop anthem, melodic and textural, intimate verses and soaring choruses.
Modern production, polished mix, atmospheric vocal production where vocals sit among the instruments rather than above them." \
  --lyrics-file gen1_lyrics.txt \
  --model music-2.6 \
  --vocals "breathy vulnerable male lead, double-tracked with slight detuning" \
  --genre "dream pop, shoegaze-influenced indie" \
  --mood "hazy confusion building to overwhelming beautiful release, then dreamlike fade" \
  --instruments "wall of clean electric guitars with heavy chorus pedal, sub-bass synth pad, soft brushed electronic drums, glockenspiel, celesta, organ pads, reversed guitar samples" \
  --bpm 96 \
  --key "D major" \
  --structure "intro-verse-pre_chorus-chorus-post_chorus-verse2-chorus-repeat-outro" \
  --use-case "slow-burn alt-pop anthem, suitable for late-night listening" \
  --avoid "sharp percussive agresivo distortion, clear upfront vocals, minimal sparse arrangement" \
  --out M1_dreampop_shoegaze.mp3
```

Output: 167.9s MP3, 5.4 MB, -8.8 LUFS, 5.7 LRA (good dynamics).

### Pattern B — Crazy Combo: Opera Vocals + Heavy Metal Music (for Fun Experiments)

```bash
python3 scripts/generate_with_retry.py -- music generate \
  --prompt "extreme dramatic contrast: powerful operatic tenor vocals over heavy metal instrumentation.
Like Freddie Mercury fronting Metallica. Epic, theatrical, over the top.
Thunderous double bass drums, distorted electric guitars with palm-muted chugging,
guttural rhythm section, blast beats, tremolo picking, minor key riffing.
Operatic vocals soaring above the metal wall of sound, belting high notes with vibrato.
Gothic theatrical atmosphere, dramatic dynamic shifts from whisper-quiet verses
to explosive metal choruses. Anthem-like, stadium-ready." \
  --lyrics-file gen2_lyrics.txt \
  --model music-2.6 \
  --vocals "operatic tenor, powerful Freddie Mercury style, vibrato, theatrical belting" \
  --genre "symphonic metal" \
  --mood "dramatic, theatrical, anthemic, intense" \
  --instruments "distorted electric guitars, double bass drums, blast beats, orchestral strings" \
  --tempo "fast" \
  --bpm 160 \
  --key "D minor" \
  --structure "verse-pre_chorus-chorus-verse-pre_chorus-chorus-outro" \
  --use-case "epic music experiment" \
  --avoid "pop, soft, gentle, acoustic, slow" \
  --out M2_opera_metal.mp3
```

Output: 155.8s MP3, 5.0 MB, -9.6 LUFS, 4.3 LRA (compressed but still has dynamics).

### Model Selection

| Model | When to use | Cost |
|---|---|---|
| `music-2.6` (default) | Production work, full quality | Token Plan / paid |
| `music-2.6-free` | Free tier, lower RPM, "unlimited" quota for some plans | Free |
| `music-2.5+` | Older model, still good quality | Token Plan / paid |
| `music-2.5` | Legacy | Token Plan / paid |
| `music-cover` | Cover/re-interpretation of source audio (one-step) | Token Plan / paid |
| `music-cover-free` | Free cover variant | Free |

`music-2.6-free` is the **default for most users** — same model, free tier. The mmx CLI uses it as the default when no `--model` is specified.

### `is_instrumental` and `lyrics_optimizer` Flags (MiniMax-Specific Paths)

The mmx CLI exposes two important flags that bypass the `--lyrics` requirement:

| Flag | What it does | When to use |
|---|---|---|
| `--instrumental` | Generate music without vocals (no lyrics needed) | When user wants BGM, intro, soundtrack, loop |
| `--lyrics-optimizer` | Auto-generate lyrics from the prompt (no `--lyrics` needed) | When user says "make me a song about X" but doesn't have lyrics |

**Examples:**

```bash
# Pure instrumental (no vocals)
python3 scripts/generate_with_retry.py -- music generate \
  --prompt "Instrumental only, no vocals, no lyrics. Loopable coffee shop background, soft piano, brushed drums, 90 BPM, C major" \
  --instrumental \
  --length 180000 \
  --out coffee_bgm.mp3

# Auto-generated lyrics from prompt
python3 scripts/generate_with_retry.py -- music generate \
  --prompt "Upbeat indie folk, melancholic but hopeful, male vocal, acoustic guitar, 100 BPM" \
  --lyrics-optimizer \
  --out indie_folk.mp3
```

Note: `mmx music generate` with `--length` uses **milliseconds** (the example shows `--length 180000` for roughly 3 minutes). Treat this as a hint, not a guarantee; lyrics length and structure still drive duration.

### Prompt Length Safety

Observed production runs succeeded with prompts around **1072-1540 UTF-8 bytes** and failed at **2079 bytes** with `invalid params, prompt length not valid`. For standard cloud batches, the v1.3.0 operator recommendation is stricter: keep prompts under about **500 characters** when possible and save detailed production sheets for the local ACE-Step route. Run `scripts/lint_music_request.py` before generation:

- `>1800` bytes: warning — shorten if possible
- `>2000` bytes: blocker — shorten before calling `mmx`

Shorten by removing duplicate adjectives, moving lyrics to `--lyrics-file`, and keeping facts in flags (`--bpm`, `--key`, `--structure`) instead of repeating them in prose.

### URL Expiration Warning

`mmx music generate` returns a `saved:` path. If you ever use `--output-format url` (the official API default), the URL **expires after 24 hours**. Download immediately. The mmx CLI auto-downloads to `--out` so this is not a problem when using `--out` directly.

See also: the `Troubleshooting` table (the `Output URL expired` row) for recovery when a URL has already expired.

### Output Format

Observed cloud outputs are MP3, stereo, 44.1 kHz, about 256 kbps. There are no
documented `mmx music generate` flags for FLAC, 48 kHz, or bitrate selection in
the verified v1.3.0 field run.

## Rate Limits and Token Plan

- **RPM:** 120 per minute (documented)
- **Concurrent:** 20 connections
- **Output URL:** 24h expiry
- **Token Plan 3.0:** credit-based unified pool, 5h rolling + weekly window

See the base skill's `Rate Limits` section for the full details.

## Troubleshooting

| Issue | Fix |
|---|---|
| `mmx: command not found` | Install via the MiniMax install guide, or skip `mmx` features and use `music_generate` |
| `401 Unauthorized` | Re-run `mmx auth login --api-key "$MINIMAX_API_KEY"` |
| Sparse output | Add `--avoid` with the canonical anti-sparse text + explicit `--instruments` |
| Lyrics too long (>3500 chars) | Shorten or split into sections |
| Wrong region | `mmx config set --key region --value global` |
| `429 Too Many Requests` | Wait 60s, check Token Plan usage, reduce concurrency |
| Output URL expired | Download the file within 24h of generation, or use `--output-format hex` for local saving |
