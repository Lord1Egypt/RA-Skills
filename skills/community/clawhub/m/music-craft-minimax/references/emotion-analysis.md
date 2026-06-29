# Emotion Analysis

The signature feature of `music-craft-minimax` is **emotion-driven prompt engineering**: analyzing the emotional arc of input audio and using it to construct a production-sheet prompt that captures the dynamics, not just the surface style.

This file covers the **analytical side**: what we detect, the pipeline, the scripts. For the **generation side** (how to use the analysis to evoke emotion in the OUTPUT, emotion recipes, iteration loop), see [`references/emotion-delivery.md`](emotion-delivery.md).

## What It Detects

Emotion analysis extracts per-section features from input audio:

| Feature | Description | Music Generation Use |
|---------|-------------|---------------------|
| `avg_intensity` | Loudness (RMS energy) | Dynamic range control |
| `pitch_range_hz` | Pitch variation width | Emotional intensity |
| `pitch_trend` | rising / falling / steady | Build-up vs release |
| `vocal_effort` | low / medium / high | Vocal intensity and strain |
| `pitch_stability` | 0–1 (1 = very stable) | Controlled vs raw delivery |
| `breathiness` | 0–1 (from spectral features) | Intimate vs full-voice |
| `spectral_centroid` | Average brightness | Timbre matching |
| `emotion_classification` | List of emotions | Mood keywords for prompt |
| `vocal_speed` | Syllables per second | Elongation cues |
| `pitch_bends` | Slides at phrase endings | Emotional emphasis |

## Intensity Curve Patterns

The most powerful output of emotion analysis is the **intensity curve**: how the song's energy changes over time. Five patterns are detected:

| Pattern | Shape | Arrangement Strategy |
|---------|-------|---------------------|
| `crescendo` | Builds to climax | Start sparse → add layers progressively |
| `decrescendo` | Starts intense, fades | Full arrangement → strip back |
| `wave` | Multiple peaks | Vary density per section, no single peak |
| `climax_late` | Peak near end | Restrained first 2/3, explosive ending |
| `climax_early` | Peak at start | Powerful opening, reflective rest |

When the analysis detects a pattern, the generated prompt includes arrangement instructions that match:

```json
{
  "section_prompts": [
    {"section_label": "intro", "arrangement_density": "sparse", "instruction": "INTRO: quiet, intimate — sparse arrangement"},
    {"section_label": "chorus", "arrangement_density": "full", "instruction": "CHORUS: loud, powerful — full arrangement, building tension"}
  ]
}
```

## Pause and Intensity Patterns

The user (and music generally) cares a lot about WHEN the song breathes. Two related patterns:

### Dramatic Pauses (Driven by `[Break]` Tags)

Dramatic pauses (silence or near-silence) create tension, release, or emotional impact. They are detected by sudden drops in intensity. The analysis tells you WHERE pauses already exist in the input; the generation side adds pauses via `[Break]` tags in the lyrics.

| Pause location | Effect | Use case |
|---|---|---|
| Before first chorus | Build anticipation | Standard pop structure |
| After climactic moment | Let the impact land | Emotional peaks |
| Before bridge | Reset before contrast | Standard pop structure |
| Before final chorus | Build to the biggest moment | Standard pop structure |
| Between short phrases | Intimacy, breath | Slow ballads, R&B |

In MiniMax generation, use `[Break]` structure tags to indicate pauses. The model creates 1–2s of silence or near-silence at those points.

### Where to Add `[Break]` Tags in Lyrics (Quick Reference)

| Section transition | Should have `[Break]`? | Why |
|---|---|---|
| Intro → Verse | Optional | Depends on style |
| Verse → Pre-Chorus | No | Build should be continuous |
| Pre-Chorus → Chorus | **Yes** | Creates anticipation |
| Chorus → Verse | No | Verse starts lower energy |
| Verse → Bridge | **Yes** | Signals contrast |
| Bridge → Chorus | **Yes** | Especially before final chorus |
| Chorus → Outro | Optional | Depends on fade |
| Final chorus → Outro | **Yes** | Lets the final note land |

If the user is having pause problems, the most common cause is missing `[Break]` tags before the chorus. Add them and the pauses appear.

### Intensity Dynamics Across the Song

The analysis tracks intensity at multiple granularities:

- **Per-section average**: a single number per detected section (verse, chorus, etc.)
- **Intensity curve**: 20 sample points across the song's duration
- **Per-frame intensity**: every ~10ms (used internally for feature extraction)

When translating to a prompt, the section-level granularity is what matters most. Use the intensity curve to inform the arrangement (crescendo, decrescendo, wave).

## Emotion Classifications (25+)

The classifier outputs a list of emotions detected across the song. The expanded set covers the full emotional spectrum commonly used in music:

### Core 9 (from the original skill)

| Emotion | Triggers (audio signature) | Music Prompt Effect |
|---------|----------------------------|---------------------|
| `intense` | High overall intensity | Loud, full arrangement |
| `calm` | Low overall intensity | Sparse, intimate |
| `dramatic` | Wide pitch range + dynamic shifts | Theatrical dynamics |
| `desperate` | High effort + unstable pitch + falling trend | Raw, urgent, stretched delivery |
| `passionate` | Medium-high effort + stable + warm | Heartfelt, powerful, sustained |
| `restrained` | Low effort + controlled | Gentle, measured |
| `building` | Rising pitch trend + increasing intensity | Tension building |
| `releasing` | Falling pitch trend + decreasing intensity | Relaxation, release |
| `breathy` | High ZCR (zero crossing rate) + low energy | Intimate, whispered |

### Extended 16+ (added for richer coverage)

| Emotion | Triggers (audio signature) | Music Prompt Effect |
|---------|----------------------------|---------------------|
| **`joyful`** | High energy + stable pitch + bright spectral centroid + high BPM | Upbeat, bright, major key, smiling, energetic delivery |
| **`triumphant`** | High intensity + rising pitch + stable + building | Powerful, building, celebratory, wide dynamics, choir in climax |
| **`melancholic`** | Low energy + falling pitch + breathy + slow | Sad, minor key, intimate, slow, low register |
| **`angry`** | High effort + unstable + sharp dynamics + distorted | Aggressive, shouted, distorted guitars, punchy drums |
| **`yearning`** | High pitch + breathy + unstable + sustained notes | Longing, sustained, high register, "where are you" |
| **`nostalgic`** | Low energy + slow + falling + vintage timbre | Wistful, gentle, soft, vintage feel |
| **`anxious`** | Unstable + fast + breathy + irregular rhythm | Tense, urgent, sharp, rapid, irregular |
| **`confident`** | High energy + stable + falling trend | Strong, controlled, clear, direct |
| **`vulnerable`** | High breathiness + low stability + low register | Fragile, intimate, exposed, soft |
| **`defiant`** | High effort + high intensity + dramatic + falling | Rebellious, powerful, confrontational |
| **`hopeful`** | Rising pitch trend + building intensity + stable + mid-bright spectral centroid | Uplifting, ascending, building, future-focused, brightening |
| **`tragic`** | Falling pitch + decreasing intensity + low effort + monotone energy | Doomed, fated, resigned, low register, no climax |
| **`heroic`** | Wide pitch range + high intensity + building + march-like rhythm | Powerful, declarative, marching, brass, building, honor |
| **`tender`** | Warm spectral centroid + low vocal effort + low-mid intensity + slow + breathy + stable | Warm, gentle, intimate, slow, affectionate, "you/we/hold" |
| **`sensual`** | Low register + high breathiness + slow + warm spectral centroid + sustained | Seductive, breathy, low register, sustained, R&B feel, "touch/whisper" |
| **`lonely`** | Low energy + high breathiness + sparse (single voice vs choir) + falling + low-mid register | Isolated, sparse, single voice, low register, empty, "alone/silence" |
| **`playful`** | High energy + irregular rhythm + mid-uptempo + bright + varied pitch | Bouncy, syncopated, fun, light, "let's/hey/ha" |
| **`haunting`** | Low energy + sparse + dissonant (minor 2nds, tritones) + falling + dark spectral centroid + breathy | Eerie, spectral, low pads, dissonant, sparse, "ghost/shadow/silence" |
| **`serene`** | Very low intensity + no peaks + very slow + low-mid pitch + stable + very low dynamic range | Tranquil, ambient, pad-based, no percussion, nature, "still/calm/breath" |
| **`celebratory`** | High energy + bright + climax_late + major key + dense + full band | Festive, jubilant, full band, dense, horns, choir, exclamations |
| **`bittersweet`** | MIXED: some sections bright + stable (joy), other sections dim + breathy + falling (melancholy). Same song, different emotions across sections. | Mixed: bright verses, dim chorus (or vice versa). Major key with minor chords. "Happy melody, sad lyrics" or vice versa. |

The detected emotions are translated to mood adjectives in the final prompt. For the full mapping from detected emotion to generated output, see [`references/emotion-delivery.md`](emotion-delivery.md) → "Emotion Recipes".

## Per-Emotion Detection Cookbook

This section tells the LLM (or the classifier) HOW to detect each emotion from the audio features. The base analysis outputs raw features (`vocal_effort`, `breathiness`, `pitch_trend`, `pitch_stability`, `pitch_range_hz`, `spectral_centroid`, `avg_intensity`, `vocal_speed`, `pitch_bends`). The LLM (or the script) maps these to emotions.

### Detection rules per emotion

| Emotion | Detection rule (which features indicate this emotion) |
|---|---|
| `intense` | `avg_intensity` above 0.1; high BPM (> 120); dense arrangement |
| `calm` | `avg_intensity` below 0.05; low BPM (< 90); sparse arrangement |
| `dramatic` | `pitch_range_hz` above 200; `vocal_effort` varies across sections; wide intensity range |
| `desperate` | `vocal_effort` = high + `pitch_stability` < 0.5 + `pitch_trend` = falling |
| `passionate` | `vocal_effort` = high + `pitch_stability` > 0.7 + warm `spectral_centroid` |
| `restrained` | `vocal_effort` = low + `pitch_stability` > 0.7 + low intensity variation |
| `building` | `pitch_trend` = rising + intensity curve = `crescendo` |
| `releasing` | `pitch_trend` = falling + intensity curve = `decrescendo` |
| `breathy` | `breathiness` > 0.5 + low `vocal_effort` |
| `joyful` | `avg_intensity` high + `pitch_stability` > 0.7 + bright `spectral_centroid` + BPM > 110 + `vocal_speed` normal-to-fast |
| `triumphant` | `avg_intensity` high + `pitch_trend` = rising + `pitch_stability` > 0.7 + intensity curve = `climax_late` |
| `melancholic` | `avg_intensity` low + `pitch_trend` = falling + `breathiness` > 0.4 + BPM < 90 + `vocal_speed` slow |
| `angry` | `vocal_effort` = high + `pitch_stability` < 0.5 + sharp intensity changes (per-section avg varies > 30%) |
| `yearning` | high `pitch_range_hz` + `breathiness` > 0.5 + `pitch_stability` < 0.6 + sustained notes (`vocal_speed` < 3 syl/sec in chorus) |
| `nostalgic` | `avg_intensity` low + `vocal_speed` slow + `pitch_trend` = falling + low spectral centroid |
| `anxious` | `pitch_stability` < 0.4 + high BPM (> 130) + `breathiness` > 0.3 + irregular rhythm (per-section intensity varies erratically) |
| `confident` | `avg_intensity` high + `pitch_stability` > 0.8 + `pitch_trend` = falling or steady |
| `vulnerable` | `breathiness` > 0.7 + `pitch_stability` < 0.5 + low `pitch_range_hz` (low register) |
| `defiant` | `vocal_effort` = high + `avg_intensity` high + `pitch_range_hz` wide + dramatic dynamics |
| `hopeful` | `pitch_trend` = rising + intensity curve = `crescendo` + `pitch_stability` > 0.6 + bright `spectral_centroid` |
| `tragic` | `pitch_trend` = falling + intensity curve = `decrescendo` + monotone energy (low per-section variation) + low `vocal_effort` |
| `heroic` | `pitch_range_hz` > 250 + `avg_intensity` high + building intensity + march-like rhythm (regular onset intervals) |
| `tender` | warm `spectral_centroid` (> 1500 Hz but not bright) + `vocal_effort` = low + `breathiness` > 0.3 + slow + `pitch_stability` > 0.7 |
| `sensual` | low `pitch_range_hz` (< 200) + `breathiness` > 0.6 + slow + warm spectral centroid + sustained notes |
| `lonely` | `avg_intensity` very low + `breathiness` > 0.5 + `vocal_speed` slow + single voice (vs choir) + falling |
| `playful` | high `avg_intensity` + irregular rhythm (onset intervals vary) + bright `spectral_centroid` + BPM 100-130 + varied pitch |
| `haunting` | `avg_intensity` low + dissonant (minor 2nd / tritone intervals) + `breathiness` > 0.4 + low `spectral_centroid` (< 1500) + falling |
| `serene` | `avg_intensity` very low (< 0.03) + very low dynamic range + `vocal_speed` slow + no peaks in intensity curve + `pitch_stability` very high |
| `celebratory` | `avg_intensity` high + bright `spectral_centroid` + intensity curve = `climax_late` + dense + full band energy |
| `bittersweet` | MIXED SIGNALS across sections: some sections have `joyful` features, others have `melancholic` features. Look for the contrast, not any single section. |

### When classification is uncertain

- The audio features are ambiguous (e.g., moderate intensity, stable pitch, mid-range spectral centroid) — could be `calm`, `restrained`, or `serene`. Pick the most specific: if very low intensity, `serene`; if moderate, `calm`; if controlled, `restrained`.
- The audio has clear primary emotion but ambiguous secondary — report the primary with high confidence, secondary with low.
- The audio doesn't fit any 25+ emotion well — report as "neutral" or describe with custom adjectives.

### Using the cookbook with the LLM

The cookbook rules are designed to be applied by the LLM (or by the script) AFTER the raw features are extracted. The flow:

1. Run `analyze_vocal_emotion.py` to get raw features (vocal_effort, breathiness, etc.)
2. Apply the cookbook rules to derive emotion candidates with confidence
3. Pass the emotion list (with confidence) to `emotion_to_prompt.py` for the final prompt
4. The LLM can also override the classification based on context (e.g., the lyrics content)

The LLM is the final arbiter. The cookbook is a guide, not a hard rule.

## Emotion Combinations

Some songs carry TWO primary emotions — a juxtaposition that is itself a creative choice. The skill supports this by detecting combinations.

### Common combinations

| Combination | What it sounds like | Lyrics strategy |
|---|---|---|
| `bittersweet` = `joyful` + `melancholic` | Happy melody, sad lyrics (or vice versa) | Major key with minor chords; bright verses, dim chorus (or vice versa) |
| `tender aggression` = `tender` + `angry` | Soft, gentle vocal over hard, distorted instruments | Quiet delivery with loud backing |
| `defiant hope` = `defiant` + `hopeful` | Rebellious optimism | "I/we will fight" + building intensity + uplifting |
| `lonely triumph` = `lonely` + `triumphant` | Alone but victorious | "I did it" + sparse verses, dense climax |
| `nostalgic joy` = `nostalgic` + `joyful` | Warm memories of happy times | Past tense + bright delivery |
| `anxious hope` = `anxious` + `hopeful` | Worried but believing in better | Tense verses, resolving chorus |
| `vulnerable confidence` = `vulnerable` + `confident` | Exposed but sure | "I am" + breathy vocal + strong arrangement |
| `playful defiant` = `playful` + `defiant` | Fun rebellion | Humorous + rebellious (e.g., punk pop) |

### How to detect a combination

The LLM should look for the contrast across sections:

- **Verses have emotion A, chorus has emotion B** → combination of A and B
- **Vocal has emotion A, accompaniment has emotion B** → combination of A and B (analyze vocal and accompaniment separately for this)
- **Lyrics suggest emotion A, delivery suggests emotion B** → combination of A and B

When a combination is detected, the prompt should include BOTH emotion sets in the mood slot, and the arrangement should support both.

Example prompt for `bittersweet`:

```
Bittersweet, joyful verses with melancholic chorus, happy-sad, major key with minor chords,
bright vocal in verses, falling intonation in chorus,
strings + piano, light percussion, building then releasing,
ALL instruments always playing throughout,
120 BPM in C major
```

For the full combinations table, see [`references/emotion-delivery.md`](emotion-delivery.md) → "Emotion Combinations".

## Pre-Trained Classifiers (Optional)

For automated classification (without LLM inference), the skill can use pre-trained models. See [`references/advanced-audio-analysis.md`](advanced-audio-analysis.md) for Essentia's `mood_classifier` and `valence / arousal` predictions.

- **Essentia mood classifier**: outputs `happy` / `sad` / `aggressive` / `relaxed` directly. Map to the 25+ emotion set.
- **Essentia valence + arousal**: 2D continuous space. Map to emotion quadrants.
- **Custom CNN models**: train your own on labeled emotion data (out of scope for the skill, but possible).

## Vocal Effort → Prompt Mapping

The `vocal_effort` feature (low / medium / high) directly maps to specific prompt wording. Use this to evoke the right intensity in the generated output.

| Effort | Audio signature | Prompt wording |
|---|---|---|
| `low` | Quiet, breathy, low spectral centroid, low RMS | "soft vocal", "whispered delivery", "delicate", "intimate", "tender" |
| `medium` | Balanced, stable, mid-range, mid RMS | "clear vocal", "controlled delivery", "expressive but measured" |
| `high` | Loud, strained, wide pitch range, high RMS | "powerful vocal", "shouted delivery", "raw", "strained", "intense" |

For the same emotion, the effort can vary by section. Example: a desperate song might have `low` effort in verses (whispered) and `high` effort in the final chorus (shouted). The analysis captures this per section.

## Breathiness → Prompt Mapping

The `breathiness` feature (0.0–1.0) controls how intimate vs projected the voice sounds.

| Breathiness | Audio signature | Prompt wording |
|---|---|---|
| `0.0–0.2` (none) | Clear, projected, full voice | "clear vocal", "full voice", "projected" |
| `0.2–0.5` (low) | Slight breath, controlled | "warm vocal", "natural delivery" |
| `0.5–0.8` (medium) | Audible breath, intimate | "breathy vocal", "close-mic", "ASMR-like softness" |
| `0.8–1.0` (high) | Whispery, fragile, very close | "whispered", "extremely intimate", "fragile", "delicate" |

Breathiness interacts with anti-sparse rules: a high-breathiness voice is often sparse (whispered delivery, single instrument). The "intimate but not a cappella" anti-sparse phrasing handles this — keep the accompaniment, soften the voice.

## Repetitive Intensification

When a phrase repeats with increasing intensity across repetitions (common in choruses), the analysis detects and quantifies it:

```json
{
  "detected": true,
  "confidence": 0.75,
  "increase_ratio": 1.45,
  "description": "Detected intensifying repetition — energy increases 1.5x across repetitions",
  "music_generation_note": "Increase dynamics and layer density with each repetition"
}
```

This translates to: "Chorus repeats with increasing intensity, each version adds layers (bass, then drums, then strings, then choir)".

## Emotional Shifts

Transitions between sections are classified as sudden or gradual:

```json
{
  "at_seconds": 145.2,
  "type": "sudden",
  "from_effort": "low",
  "to_effort": "high",
  "description": "Sudden shift at 145.2s"
}
```

A sudden shift translates to: "At [section], the arrangement suddenly goes from [X] to [Y], creating dramatic contrast". A gradual shift translates to: "Build from [X] to [Y] over [N] seconds".

## Vocal Speed and Elongation

The most distinctive feature: **vocal speed / syllable elongation**. Detects word stretching and tempo changes per section.

```json
{
  "pattern": "decelerating",
  "description": "Vocals progressively slow down, especially at the end — emotional elongation pattern",
  "average_syllables_per_second": 4.46,
  "deceleration_detected": true,
  "final_sections_slowed": true,
  "sections": [
    {"structural_label": "intro", "syllables_per_second": 5.01, "speed_classification": "normal"},
    {"structural_label": "verse", "syllables_per_second": 6.69, "speed_classification": "accelerated"},
    {"structural_label": "outro", "syllables_per_second": 2.21, "speed_classification": "slowed"}
  ]
}
```

| Pattern | Meaning | Music Generation Effect |
|---------|---------|------------------------|
| `decelerating` | Vocals progressively slow down | Stretch syllables per section, elongated ending |
| `late_elongation` | Final sections are much slower | Slow delivery for final chorus/bridge |
| `gradual_slowing` | Steady deceleration throughout | Progressive rubato |
| `accelerating` | Vocals speed up | Urgent, driving delivery |
| `steady` | Consistent speed | Even pacing |

The translation to the prompt: instructions to stretch specific syllables (`"with emotionally elongated delivery in the final chorus"`) plus lyrics modifications (`"reduce to ~5 syllables per line in the outro"`).

For specific elongation examples by emotion (joy, desperation, melancholy, etc.), see [`references/emotion-delivery.md`](emotion-delivery.md) → "Emotion Recipes" and [`../music-craft/references/structure-tags.md`](../../music-craft/references/structure-tags.md) → "Vocal Effects Through Lyrics".

## Pitch Bends at Phrase Endings

Detects monotonic pitch slides (rising or falling) at the ends of vocal phrases — a hallmark of emotional delivery:

```json
{
  "start_seconds": 42.1,
  "end_seconds": 43.8,
  "direction": "falling",
  "pitch_range_hz": 85.3,
  "duration_seconds": 1.7
}
```

This is hard to translate directly to a MiniMax prompt (the model does not have a "pitch bend" parameter), but it informs the prompt's mood and style choices: "with emotionally expressive vocal delivery, falling pitch slides at phrase endings".

For lyrics that evoke pitch bends, use:
- Trailing vowels at the end of phrases: `"...goodbyeee"` (falling)
- Rising inflections on questions: `"Will you stay?^^"` (upward inflection)
- Wordless vocalizations: `"oohhh"`, `"aaahhh"`, `"mmm"`

## The Analysis Pipeline

```
Audio file (WAV)
  → analyze_vocal_emotion.py
    → emotion JSON (per-section features, intensity curve, vocal speed, pitch bends)
      → emotion_to_prompt.py
        → production-sheet prompt (with arrangement plan, vocal speed cues, mood keywords)
          → music_generate
            → output song
```

The full Python helpers are in [`../scripts/`](../scripts/):

> **v1.5.0:** the published skill is audio-only. The video, image, and YouTube download scripts were removed — use the private `music-source-fetch` skill to acquire a local audio file first, then run the orchestrator on that path.

- [`../scripts/analysis_orchestrator.py`](../scripts/analysis_orchestrator.py) — single entry point (audio only)
- [`../scripts/analyze_vocal_emotion.py`](../scripts/analyze_vocal_emotion.py) — the main emotion extractor
- [`../scripts/analyze_audio.py`](../scripts/analyze_audio.py) — basic features (BPM, key, energy)
- [`../scripts/emotion_to_prompt.py`](../scripts/emotion_to_prompt.py) — converts emotion JSON to prompt
- [`../scripts/analyze_two_songs.py`](../scripts/analyze_two_songs.py) — two-song comparison
- [`../scripts/extract_lyrics_whisper.py`](../scripts/extract_lyrics_whisper.py) — Whisper-based lyrics extraction

## Quick Start

```bash
# Step 1: Convert to WAV if needed
ffmpeg -i /tmp/song.mp3 -ar 44100 /tmp/song.wav

# Step 2: Run emotion analysis
python3 scripts/analyze_vocal_emotion.py /tmp/song.wav --output /tmp/emotion.json

# Step 3: Convert to prompt
python3 scripts/emotion_to_prompt.py \
  --emotion /tmp/emotion.json \
  --style /tmp/style.json \
  --language english \
  --output /tmp/mashup_prompt.json

# Step 4: Extract the final prompt
PROMPT=$(jq -r '.final_prompt' /tmp/mashup_prompt.json)

# Step 5: Generate
mmx music generate \
  --prompt "$PROMPT" \
  --lyrics "..." \
  --model music-2.6 \
  --out /tmp/output.mp3
```

## Local-Only Path (When MiniMax Is Unavailable)

`emotion_to_prompt.py` calls the MiniMax cloud, so it fails when MiniMax API access is unavailable or no key is set. In that case build the prompt locally from the analysis JSON without that script: take the extracted BPM and key/scale as explicit metadata fields; turn the energy curve and spectral brightness into texture words; turn the emotion classification and intensity curve into mood words and dynamic section tags; and feed transcribed lyrics (full-mix Whisper) as the lyric body. This is the same data, assembled by the agent instead of the cloud helper, and it feeds any backend (including a local model).

## emotion_to_prompt.py Output

The conversion script produces a structured JSON with everything needed for generation:

```json
{
  "style_category": "french_chanson",
  "target_bpm": 80,
  "target_duration_seconds": 180,
  "final_prompt": "french chanson style, 1960s Paris café atmosphere, accordion...",
  "structured_lyrics_template": {
    "template": "[Intro]\n(Instrumental)\n\n[Break]\n(1-2 second dramatic pause)\n\n[Build Up]\n(Tension building)\n\n[Chorus]\n(powerful delivery)\n{lyrics_here}",
    "sections_count": 8,
    "silence_gaps_used": 2,
    "note": "Fill placeholders with actual lyrics, preserve structure tags"
  },
  "workflow_recommendation": {
    "workflow": "cover_two_step",
    "model": "music-cover",
    "reasoning": "Original audio available → cover workflow for melody preservation",
    "steps": ["1. Preprocess audio", "2. Edit lyrics", "3. Generate cover"]
  },
  "section_prompts": [
    {"section_label": "intro", "arrangement_density": "sparse", "instruction": "INTRO: quiet, intimate — sparse arrangement"},
    {"section_label": "chorus", "arrangement_density": "full", "instruction": "CHORUS: loud, powerful — full arrangement, building tension"}
  ],
  "arrangement_plan": {
    "intro": "sparse: accordion only",
    "chorus": "full arrangement: accordion, strings, piano, bass",
    "final_chorus": "maximum intensity: all instruments + backing harmonies"
  },
  "vocal_speed_patterns": {
    "detected": true,
    "pattern": "late_elongation",
    "prompt_additions": ["final sections feature emotionally stretched syllables"],
    "lyrics_modifications": [{"section": "outro", "instruction": "Reduce to ~5 syllables per line", "example": "I caaan't goooo on with yoooou"}],
    "section_cues": [{"section": "outro", "prompt_cue": "outro: slow, emotionally stretched delivery, hold last syllable"}]
  }
}
```

Use `final_prompt` directly with `mmx music generate` or `music_generate`. Use the `section_prompts` and `arrangement_plan` for guidance when constructing the lyrics with section tags.

The `vocal_speed_patterns.prompt_additions` and `lyrics_modifications` are particularly important for emotional delivery — they translate the detected vocal speed pattern into concrete instructions.

## When NOT to Use Emotion Analysis

- The user has no audio input (skip the analysis, use standard generation)
- The input is instrumental only (vocal emotion analysis requires vocals)
- The input is very short (< 10 seconds) — analysis is unreliable
- The input is heavily processed (synth, electronic) — pitch detection struggles
- The user wants a quick draft — emotion analysis takes 10–60 seconds

## Anti-Sparse from Emotion Analysis

The arrangement plan from emotion analysis includes anti-sparse by default — quiet sections are still "fully played, NOT silent". If you see sparse output despite this, the analysis may have been over-confident. Run it again with `--no-parselmouth` to use librosa's pitch detection (less accurate but more conservative).

For the deeper anti-sparse treatment specific to emotional delivery (which is inherently lower-intensity), see [`references/emotion-delivery.md`](emotion-delivery.md) → "Common Mistakes in Emotional Delivery".

## Limitations

- **Emotion detection is approximate** — based on audio features, not semantic understanding
- **Pitch detection can struggle** with heavily processed or distorted vocals
- **Style inference is a best guess** — manual override is always better
- **Repetitive detection requires ≥ 3 repetitions** with consistent increase
- **Vocal speed detection is ±20% accurate** — syllable count is estimated, not true phoneme alignment
- **MiniMax has no "vocal speed" parameter** — elongation is achieved via lyrics formatting (fewer syllables, repeated vowels) and prompt cues
- **MiniMax has no "pitch bend" parameter** — pitch slides are evoked via trailing vowels and wordless vocalizations
- **MiniMax has no "vocal effort" parameter** — effort is evoked via prompt wording ("shouted", "whispered", "raw")
- **The model can flatten emotional cues** if the prompt is vague. Always use the emotion recipes in [`references/emotion-delivery.md`](emotion-delivery.md).
