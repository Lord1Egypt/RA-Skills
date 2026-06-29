# Examples

> **Note on examples (v1.5.0+):** Language, locale, and singer-style
> attributes in these examples are placeholders. Always confirm the
> target language and vocal style with the user before applying them —
> do not infer language from the example text. Addresses audit SQP-3.

Use `music-craft-minimax` when the user provides audio, wants melody preservation, or needs the richer MiniMax-specific workflows.

For workflow details, see [`cover-workflow.md`](./cover-workflow.md), [`mashup-workflow.md`](./mashup-workflow.md), and [`emotion-analysis.md`](./emotion-analysis.md).

| Example | Use MiniMax because | First response/questions | Workflow shape |
|---|---|---|---|
| Cover from audio | The user wants the same melody with a new style, and they have source audio. | Ask for the local audio file, plus the target style and whether lyrics should change. | `analyze audio -> cover preprocess -> generate cover` |
| URL-based source (YouTube, JioSaavn, mx3.ch) | The user only has a streaming URL and wants to use it as source audio. | Explain that the published skill no longer downloads audio. Ask them to fetch the file with the private `music-source-fetch` skill and pass back the local path. | `fetch URL with music-source-fetch -> analyze local file -> cover preprocess -> generate cover` |
| Two-song mashup | The user wants Song A's content with Song B's style. | Ask which song is the content source, which is the style source, and whether either one is audio or name-only. | `analyze both sources -> extract lyrics/emotion/style -> build mashup prompt -> generate` |
| Lyrics API edit/generation | The user wants to rewrite, fix, translate, or generate lyrics before cover or standard generation. | Ask for the target language, section structure, and whether the lyrics are original, translated, or edited. | `generate or edit structured lyrics -> attach to cover or standard generation` |
| Emotion-analysis-to-prompt | The user wants the music to match a specific emotional arc from a vocal or song analysis. | Ask what emotion should lead the track and whether the arc should stay constant or evolve. | `analyze emotion -> convert to prompt descriptors -> apply to cover or standard generation` |
| Long lyric-heavy generation | The user requests a full-length3:00+ vocal track with dense lyrics. | Warn that MiniMax may return ~120–150s for lyric-heavy prompts; confirm they accept shorter output or switch to ACE-Step. | `lint -> warn on duration -> generate -> verify duration -> caveated delivery` |
| Linter catch: prompt BPM vs `--bpm` conflict | The prompt says `80 BPM` but the `mmx` flags file says `--bpm 120`. | Treat the flag as the authoritative value only if the user confirms it; otherwise fix the prompt or the flag so they match. | `lint prompt + flags -> resolve bpm conflict -> generate` |
| Linter catch: key conflict | The prompt says `E minor` but the flags file says `--key C major`. | Pick one source of truth (prompt for descriptive content, flags for numeric facts) and re-align. | `lint prompt + flags -> resolve key conflict -> generate` |
| Linter catch: conflicting cover/style transfer | The user asks for both "make it a cover" and "do a style transfer" in the same request. | Ask the user to pick one: cover preserves melody, style transfer replaces it. | `surface blocker -> clarify intent -> route to minimax_cover or minimax_style_transfer` |
| Revision after a weak generation | The first generation was muddy, lost the melody, or had a flat chorus. | Identify the failure signature (see SKILL.md "Output Verification") and apply the matching revision template. | `identify signature -> apply revision template -> regenerate -> re-verify` |

Notes:
- This skill is the right choice when audio analysis matters.
- If the user has no audio and only wants a fresh song from text, route to the base skill instead.
- Use [`../scripts/lint_music_request.py`](../scripts/lint_music_request.py) when prompt text and `mmx` flags need a quick conflict check before generation. The linter returns a `retry_guidance` array with one hint per conflict.

## Canonical `mmx` Prompt Schema

When you build a prompt and an `mmx` flag set for MiniMax generation, use the canonical schema below. The schema has ten fields, each with a clear role. The linter cross-checks the prompt text against the flag values; the schema is the contract both sides agree on.

```yaml
mmx_prompt:
  intent: "cover"           # cover | mashup | style_transfer | emotion_prompt | standard
  source:
    type: "audio_file"      # audio_file | song_name (v1.5.0+: URLs must be fetched via music-source-fetch first)
    path: "/tmp/song.wav"   # local file path or song name string
  target_style:
    genre: "french chanson"
    mood: "melancholic romantic"
    era: "1960s"
    reference: "Edith Piaf" # optional, for free-tool inference
  lyrics_policy: "original" # original | translated | rewritten | instrumental
  tempo: 80                 # BPM integer; aligns with --bpm
  key: "E minor"            # aligns with --key
  structure: "intro-verse-chorus-verse-chorus-bridge-chorus-outro"
                            # aligns with --structure
  vocal_delivery:
    mode: "vocal"           # vocal | instrumental
    timbre: "passionate"
    language: "french"
    range: "mezzo-soprano"  # optional
  mix:
    vocal_upfront: true
    stereo_width: "wide"
    density: "full"         # sparse | medium | full
    dynamics: "dynamic"     # monotone | medium | dynamic
  avoid: "sparse, a cappella, electronic, synth, autotune"
                            # aligns with --avoid
```

### Worked example: cover in a new style

```yaml
mmx_prompt:
  intent: "cover"
  source:
    type: "audio_file"
    path: "/tmp/source_audio.ogg"  # local file path; fetch URLs with music-source-fetch
  target_style:
    genre: "reggaeton"
    mood: "energetic dramatic"
    era: "modern"
  lyrics_policy: "translated"  # original language -> target language; confirm both with the user
  tempo: 95
  key: "A minor"
  structure: "intro-verse-prechorus-chorus-verse-prechorus-chorus-bridge-chorus-outro"
  vocal_delivery:
    mode: "vocal"
    timbre: "<vocal style as confirmed with the user>"
    language: "<target language as confirmed with the user>"
  mix:
    vocal_upfront: true
    stereo_width: "wide"
    density: "full"
    dynamics: "dynamic"
  avoid: "sparse, a cappella, ballad, soft, acoustic"
```

The corresponding `mmx` invocation:

```bash
python3 scripts/generate_with_retry.py \
  --output-path /tmp/cover_output.mp3 \
  -- \
  music cover \
  --prompt "Reggaeton cover, dembow rhythm, 808 sub-bass, synth pads, <vocal style as confirmed with the user>, 95 BPM, A minor, intro-verse-prechorus-chorus-verse-prechorus-chorus-bridge-chorus-outro, dynamic contrast" \
  --audio-file /tmp/source_audio.ogg \
  --lyrics "<lyrics in the target language as confirmed with the user>" \
  --genre "reggaeton" \
  --mood "energetic dramatic" \
  --vocals "<vocal style as confirmed with the user>" \
  --bpm 95 \
  --key "A minor" \
  --structure "intro-verse-prechorus-chorus-verse-prechorus-chorus-bridge-chorus-outro" \
  --avoid "sparse, a cappella, ballad, soft, acoustic" \
  --model music-cover \
  --out /tmp/cover_output.mp3
```

### Worked example: emotion-driven precision flags

```yaml
mmx_prompt:
  intent: "emotion_prompt"
  source:
    type: "audio_file"
    path: "/tmp/source.wav"
  target_style:
    genre: "synthwave"
    mood: "dark atmospheric hypnotic"
  lyrics_policy: "original"
  tempo: 110
  key: "A minor"
  structure: "intro-verse-prechorus-chorus-verse-chorus-bridge-chorus-outro"
  vocal_delivery:
    mode: "vocal"
    timbre: "<vocal style as confirmed with the user>"
    language: "<target language as confirmed with the user>"
  mix:
    vocal_upfront: false
    stereo_width: "wide"
    density: "full"
    dynamics: "medium"
  avoid: "sparse, a cappella, acoustic, bright, cheerful, organic"
```

The corresponding `mmx` invocation:

```bash
mmx music generate \
  --prompt "Dark synthwave, retro 80s neon, urban nightscape, atmospheric pulsing" \
  --vocals "<vocal style as confirmed with the user>" \
  --genre "synthwave" \
  --mood "dark atmospheric hypnotic" \
  --instruments "analog synth, drum machine, sub-bass, gated reverb drums, arpeggiator, pads" \
  --bpm 110 \
  --key "A minor" \
  --structure "intro-verse-prechorus-chorus-verse-chorus-bridge-chorus-outro" \
  --avoid "sparse, a cappella, acoustic, bright, cheerful, organic" \
  --model music-2.6 \
  --out /tmp/output.mp3
```

### Linter pass before generation

```bash
# 1. Save the prompt to a file
cat > /tmp/cover_prompt.txt <<'EOF'
Reggaeton cover, dembow rhythm, 808 sub-bass, synth pads, <vocal style as confirmed with the user>, 95 BPM, A minor, intro-verse-prechorus-chorus-verse-prechorus-chorus-bridge-chorus-outro, dynamic contrast
EOF

# 2. Save the flags to a JSON file
cat > /tmp/cover_flags.json <<'EOF'
{
  "bpm": 95,
  "key": "A minor",
  "structure": "intro-verse-prechorus-chorus-verse-prechorus-chorus-bridge-chorus-outro",
  "vocals": "<vocal style as confirmed with the user>",
  "language": "<target language as confirmed with the user>",
  "avoid": "sparse, a cappella, ballad, soft, acoustic"
}
EOF

# 3. Run the linter
python3 scripts/lint_music_request.py --prompt-file /tmp/cover_prompt.txt --mmx-flags /tmp/cover_flags.json
# -> route: minimax_cover
# -> flag_conflicts: []
# -> retry_guidance: []
```

If the linter reports conflicts, follow the matching `retry_guidance` hint, re-save the files, and re-run until `flag_conflicts` is empty.

## Confidence Map Example (MiniMax-Specific)

**Request:** *"Make me a cover of [Song X] in [target genre], translated into [target language]."*

```
clear:     source_audio=path, song_a=[Song X], target_style=[target genre],
            lyrics_decision=translated, target_language=[target language]
inferred:  vocal_mode depends on the source (solo / duet / choir)
missing:   output_location (which project folder? per-song subfolder?)
            vocal_register (full chest, head voice, whisper? — affects --vocals flag)
            confirmation of vocal style (gender, register) — never infer from the song name
```

**Request:** *"I have a streaming URL of an old song and want it as a [new style], with [target language] lyrics because the original is in [original language]."*

```
clear:     song_a=old_song, target_style=[new style],
            lyrics_decision=translated, target_language=[target language]
inferred:  vocal_mode depends on the source, ~3min
missing:   local audio file (URLs require music-source-fetch first)
            BPM/key from analysis output (will be filled in after analysis)
            output_location
            confirmation of vocal style (gender, register) — never infer from the song name
```
