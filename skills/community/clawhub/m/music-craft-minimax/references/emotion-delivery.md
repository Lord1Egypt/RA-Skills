# Emotional Delivery in Generation

The analysis side ([`emotion-analysis.md`](emotion-analysis.md)) tells us what the input audio sounds like. The challenge is making the **output** sound emotional. This file covers the generation side: how to construct prompts, lyrics, and arrangements that actually evoke the target emotion.

If you have run emotion analysis on input audio, use the detected features (vocal effort, breathiness, intensity curve, vocal speed) to drive the generation choices below. If you have no input, use the LLM's knowledge plus these recipes to evoke emotion from scratch.

> **v1.5.0 (audio-only):** the orchestrator is audio-only. The `image.*` and `video.*` rows in the v0.3.0 table below, the `--vlm` / `--ocr` / `--faces` flags, the `extract_video_features.py` and `analyze_image.py` scripts, and YouTube URL downloads have all been removed. See `references/changelog.md` for the full removal list. Current operating guidance starts at "The 'Emotion Recipe' Pattern" below.

## What's New in v0.3.0 (May 2026) — historical, pre-v1.5.0

v0.3.0 represents a major expansion of the analysis pipeline. The emotion
detection, beat tracking, melody analysis, instrument tagging, image
captioning, and source separation are all production-grade.

### New Scripts (8 new in v0.2-v0.3) — historical

| Script | Tool | What it does |
|---|---|---|
| `extract_stems.py` | Demucs (MIT, opt-in via `--use-demucs`) | Source separation: vocals / drums / bass / other. Dramatically improves vocal emotion on busy mixes. |
| `track_beats.py` | beat_this (MIT, ISMIR 2024 SOTA) | Beat + downbeat positions, BPM with confidence, time signature estimate |
| `extract_melody.py` | Spotify Basic Pitch (Apache-2.0) | Polyphonic audio → MIDI; MIDI-confirmed key + scale modes |
| `compute_audio_embedding.py` | MERT v1-330M (Apache-2.0) | 1024-dim music embedding; cosine similarity for "vibe" matching |
| `classify_instruments.py` | MIT AST (AudioSet 527-class) | Fine-grained instrument / genre tagging (rock, grunge, punk, ...) |
| `analysis_orchestrator.py` | (built in v0.1.0) | Single entry point; in v1.5.0 reduced to `--audio`, `--lyrics`, `--use-demucs` flags only |

### New Analysis Outputs (v0.3.0 additions) — historical

| Field | Source | Prompt effect |
|---|---|---|
| `beat_tracking.bpm_estimated` | beat_this | `"beat grid: 4/4 at 150 BPM (confidence 0.80)"` — overrides target_bpm if confidence > 0.8 |
| `beat_tracking.time_signature_estimate` | beat_this | "4/4" or "3/4" in the beat grid line |
| `melody_analysis.key_estimate_from_midi` | Basic Pitch | "melodic key from MIDI: E minor" — more reliable than chroma |
| `melody_analysis.scale_modes` | Basic Pitch | "modal character: pentatonic, blues" |
| `melody_analysis.interval_pattern` | Basic Pitch | "interval motion: mostly leaps" |
| `melody_analysis.monophonic_fraction` | Basic Pitch | proxy for vocal vs polyphonic character |
| `ast_classification.top_instruments` | MIT AST | "AST-detected sound palette: rock music (0.16), punk rock (0.14)" |
| `vocal_emotion.silence_gaps` (with `--use-demucs`) | Demucs vocal stem | "natural dramatic pauses detected at: 2s (11.7s pause), 20s (3.3s pause)..." |
| `vocal_emotion._demucs` | Demucs | Model + stem path metadata |
| 25-emotion `emotion_classification` (was 9) | per-section rules | "emotion signature: intense, triumphant, defiant, building" — more granular |
| Per-section `breathier_in_verse / strained_in_chorus` | phase-1 aggregation | "vocal texture in verse: breathier / more intimate than average" |
| `tempo_consistency` → "tight" / "loose" | new consumption | "rhythm: tight, on-beat delivery" |
| `onset_density` → "busy" / "spacious" | new consumption | "high note density — busy, intricate" |
| `brightness` → "dark" / "bright" | new consumption | "tonal character: dark warm tone, rolled-off highs" |
| `instrument_hints` → likely_* | new consumption | "instruments detected: electronic / synthetic textures" |
| `music_generation_hints[]` | now injected | "Vary arrangement density — fuller for peaks, reduced for valleys — but always keep at least 2 instruments active" |

> The `image.caption` / `image.text_in_image` / `image.faces` / `video.camera_motion` / `video.vlm_captions[]` rows from v0.3.0 are omitted here because the image and video pipelines were removed in v1.5.0.

### Mashup Improvements (cumulative)

- Key compatibility scoring (circle of fifths) — automatic
- BPM range scoring — identifies mashup candidates
- Transposition suggestions when keys clash
- `mashup compatibility:` line appended to final prompt
- `mashup_plan.style_notes` + `instrument_prompt_additions` now consumed

### Performance / Bug Fixes

- parselmouth 0.4.x: get_value_at_time / get_value_at_xy (was get_value_in_frame)
- ffmpeg 8.x image2 muxer: per-frame extraction workaround
- pylette 5.1+ capital-P package import
- open_clip 3.3 3-tuple return + get_tokenizer()
- demucs 4.x apply_model() entry point
- ffmpeg 8.x `--version` flag dropped: check_tool tries `-version` fallback

### What's New in v0.1.0 — historical, pre-v1.5.0

The emotion pipeline has been significantly extended. If you ran analysis on a previous version, re-run with the latest scripts to get the new fields.

### New Analysis Outputs (v0.1.0 baseline) — historical

| Field | What it means | Prompt effect |
|---|---|---|
| `chord_progression` | Auto-detected chord symbols (Am, F, C, G) | `"chord progression: Am - F - C - G"` |
| `loudness_profile.LRA` | Perceptual dynamic range in LU | "wide dynamic range" or "compressed wall-of-sound" |
| `song_structure` | Neural segment labels (intro/verse/chorus) | More accurate `[Verse]` / `[Chorus]` placement |
| `harmonic_percussive.classification` | Smooth vs percussive texture | "smooth melodic" or "driving rhythmic" |
| `vocal_quality.voice_quality` | Smooth vs rough vs pressed | "clean polished" or "raw gritty" |
| `emotion_sections[].vocal_register` | Chest / head / falsetto | "airy falsetto" / "full chest voice" per section |
| `emotion_sections[].rhythm_feel` | Swing / straight | "swing feel" / "straight eighth-note" per section |
| `emotion_sections[].harmony_quality` | Consonant / tense / rich | "consonant" / "dissonant" / "rich" per section |
| `clap_classification` | Zero-shot genre / mood / instruments | APPENDED to template defaults (not replaced) |
| `emotion_classification` (per section) | Top-3 detected emotions | "emotion signature from analysis: ..." |

### New Scripts (v0.1.0 baseline) — historical

- `extract_lyrics_whisper.py` — Whisper-based ASR with section tagging
- `analysis_orchestrator.py` — Single entry point; in v1.5.0 audio-only

> `extract_video_features.py` and `analyze_image.py` from v0.1.0 were removed in v1.5.0.

### Mashup Improvements (v0.1.0 baseline)

- Key compatibility scoring (circle of fifths) is now automatic
- BPM range scoring identifies mashup candidates
- Transposition suggestions when keys clash
- `mashup compatibility:` line appended to final prompt

## The "Emotion Recipe" Pattern

For each target emotion, the generation prompt and lyrics need four coordinated elements:

1. **Vocal descriptors**: 2-3 adjectives that evoke the emotion in the prompt's `prompt` field
2. **Lyrics formatting**: structural choices (elongation, repetition, pause placement) in the `lyrics` body
3. **Arrangement**: instrumentation density, dynamics, key, BPM
4. **Section-level instructions**: where the emotion peaks, where it releases

A complete recipe specifies all four. Using only one or two is what produces "emotionally flat" output.

## Quick Reference: Emotion → Descriptor Set

| Target emotion | Vocal descriptors | Key/BPM | Arrangement feel |
|---|---|---|---|
| Joy | bright, energetic, smiling, celebratory | major / 110-130 | dense, hand claps, bright synths |
| Desperation | strained, raw, falling, urgent | minor / 70-90 | slow build, dramatic strings, sparse→dense |
| Melancholy | breathy, low, slow, wistful | minor / 60-80 | sparse, piano+strings, low BPM |
| Triumph | powerful, building, declarative | major / 100-130 | full orchestra, choir in climax, building |
| Yearning | breathy, high, sustained, longing | major or minor / 70-90 | high register, sustained pads |
| Anger | aggressive, shouted, sharp, raw | minor / 110-150 | distorted, punchy drums, dense |
| Vulnerability | whispered, fragile, intimate, hesitant | minor / 60-80 | very sparse, single instrument |
| Confidence | strong, clear, stable, direct | major / 110-130 | punchy, driving, full band |
| Nostalgia | warm, gentle, distant, wistful | major / 70-90 | vintage feel, soft, faded |
| Anxious | tense, sharp, rapid, unstable | minor / 130-160 | irregular rhythm, dissonant |

## Full Recipes

### Recipe: Joy

**Vocal descriptors:** bright, energetic, smiling, upbeat, celebratory

**Lyrics formatting:**
- Short syllables, lots of repeated words
- Exclamations: `"oh!"`, `"hey!"`, `"yeah!"`
- Rising inflections on questions
- Examples:
  ```
  [Verse]
  Sun is shiiiiining
  And I'm feeliiiiing fine

  [Chorus]
  Oh oh oh! Yeah yeah yeah!
  This is my dayyy!
  ```

**Arrangement:**
- Key: major
- BPM: 110-130
- Instrumentation: bright synths or acoustic guitar, hand claps, tambourine
- All instruments always playing
- Section intensity: chorus is the highest, verses stay bright

**Section structure:**
- Intro: brief, bright hook
- Verses: bright but lower energy
- Pre-Chorus: build energy
- Chorus: maximum energy, hook
- Bridge: contrast (slight key change, drop)
- Final chorus: biggest energy

**Anti-sparse:** all instruments always playing, dense pop production, hand claps layer in.

---

### Recipe: Desperation

**Vocal descriptors:** strained, raw, falling intonation, urgent, with emotional weight

**Lyrics formatting:**
- Long stretched vowels in emotional words
- Repetition with increasing intensity
- Trailing downward vowels
- Examples:
  ```
  [Verse]
  I caaaan't goooo on with yoooou
  Nooooo, pleaseeee, don't leeeave

  [Pre Chorus]
  Don't youuuu, don't youuuu, don't youuuu goooo

  [Chorus]
  I'm beggiiiiiing, I'm beggiiiiiing
  Stay with meeeee
  ```

**Arrangement:**
- Key: minor
- BPM: 70-90
- Instrumentation: dramatic strings, sparse piano, building to dense
- Wide dynamic range
- Section intensity: climax at bridge or final chorus

**Section structure:**
- Intro: very sparse, single instrument
- Verses: restrained, low effort
- Pre-Chorus: build with strings
- Chorus: powerful, full effort
- Bridge: highest effort, raw
- Final chorus: explosive

**Anti-sparse:** even quiet sections have at least 2 instruments, never silent. The desperation lives in the VOCAL, not the arrangement density.

---

### Recipe: Melancholy

**Vocal descriptors:** breathy, low, slow, wistful, soft, intimate

**Lyrics formatting:**
- Simple words
- Lots of pauses (`[Break]`)
- Elongated vowels
- Quiet, almost whispered delivery
- Examples:
  ```
  [Verse]
  Stil hereee
  Waiting for yoooou

  [Break]

  [Verse]
  Counting the days
  That weee looost

  [Chorus]
  I miss yoooou... stil...
  Every night...
  ```

**Arrangement:**
- Key: minor
- BPM: 60-80
- Instrumentation: piano + strings + soft bass, very sparse
- Low dynamic range (no loud sections)
- Section intensity: maintains low energy throughout

**Section structure:**
- Intro: single instrument
- Verses: piano-led, breathy vocal
- Pre-Chorus: subtle build
- Chorus: slightly fuller but still restrained
- Bridge: most emotional moment, breathy
- Outro: fade to silence

**Anti-sparse:** explicit "quiet sections: piano and bass only, still fully played" — never a cappella, never silent. The melancholy is in the slowness, not the silence.

---

### Recipe: Triumph

**Vocal descriptors:** powerful, building, declarative, celebratory, wide dynamic range

**Lyrics formatting:**
- Declarations: "I", "We", "us", "now", "today"
- Climactic words at peaks: "rise", "stand", "fight", "win"
- Building intensity through repetition
- Examples:
  ```
  [Verse]
  We were broken
  We were down

  [Pre Chorus]
  But we stood up
  We held our ground

  [Build Up]

  [Chorus]
  WE WILL RISE
  WE WILL FIGHT
  THIS IS OUR NIGHT

  [Break]

  [Bridge]
  Nothing can stop us nowwww

  [Build Up]

  [Chorus]
  WE WILL RISE
  WE WILL FIGHT
  THIS IS OUR NIGHT
  ```

**Arrangement:**
- Key: major
- BPM: 100-130
- Instrumentation: full band or orchestra, choir in climax
- Building throughout
- Section intensity: starts restrained, biggest climax at final chorus

**Section structure:**
- Intro: minimal, building
- Verses: restrained, focused on the story
- Pre-Chorus: build energy
- Chorus: powerful, full band
- Bridge: brief reflective moment
- Final chorus: biggest, with choir/harmonies

**Anti-sparse:** all instruments always playing, layers added progressively throughout the song.

---

### Recipe: Yearning

**Vocal descriptors:** breathy, high register, sustained notes, longing, soft

**Lyrics formatting:**
- Questions: "where are you", "will you come back", "do you remember"
- Long vowels, ascending inflections
- Trailing upward vowels
- Examples:
  ```
  [Verse]
  Where are yoooou...
  Where have yoooou goooone...

  [Pre Chorus]
  Do youuuu think of meee
  When the niiight is looong

  [Chorus]
  I'm waitiiiiing... for yoooou...
  To come hoooome
  ```

**Arrangement:**
- Key: major or minor (lean minor for emotional depth)
- BPM: 70-90
- Instrumentation: high piano or strings, sustained pads
- Slow build
- Section intensity: maintains longing throughout, no resolution

**Section structure:**
- Intro: ethereal, sustained
- Verses: breathy, ascending
- Pre-Chorus: build the question
- Chorus: highest note, sustained
- Bridge: most vulnerable moment
- Outro: unresolved, fading

**Anti-sparse:** pad layers always sustaining, even if quiet. The yearning is in the sustained tension, not silence.

---

### Recipe: Anger

**Vocal descriptors:** aggressive, shouted, sharp, raw, intense, with strain

**Lyrics formatting:**
- Short, punchy words
- Exclamations: `"ENOUGH!"`, `"NO!"`, `"STOP!"`
- Repeated phrases for emphasis
- Capital letters (model often interprets as shouted)
- Examples:
  ```
  [Verse]
  Enough is enough
  No more lies

  [Pre Chorus]
  You think you can break me
  You think you can win

  [Chorus]
  NO! NO! NO!
  I won't take this anymore!
  GET OUT!
  ```

**Arrangement:**
- Key: minor
- BPM: 110-150
- Instrumentation: distorted guitars or aggressive synths, punchy drums, sharp dynamics
- Section intensity: chorus is explosive, verses build tension

**Section structure:**
- Intro: aggressive hook
- Verses: tense, building
- Pre-Chorus: rising tension
- Chorus: explosive, shouted
- Bridge: brief moment of clarity
- Final chorus: biggest, most aggressive

**Anti-sparse:** always dense, no quiet sections. The anger is in the volume and sharpness.

---

### Recipe: Vulnerability

**Vocal descriptors:** whispered, breathy, fragile, intimate, hesitant

**Lyrics formatting:**
- First person: "I", "me", "my"
- Intimate confessions
- Hesitation: ellipses, broken phrases
- Long stretched vowels
- Examples:
  ```
  [Verse]
  I... don't... knoooow...
  If i... caaaan...

  [Pre Chorus]
  I thought i was strooong
  But i'm... not...

  [Chorus]
  I need yoooou... please...
  Don't let me gooo
  ```

**Arrangement:**
- Key: minor
- BPM: 60-80
- Instrumentation: very sparse, single instrument + voice
- Whispered vocal effort
- Section intensity: stays vulnerable throughout, no climax

**Section structure:**
- Intro: barely there
- Verses: single instrument, breathy vocal
- Pre-Chorus: subtle build
- Chorus: slight fullness, still breathy
- Bridge: most exposed
- Outro: fade to near-silence

**Anti-sparse:** explicit "sparse but NOT a cappella, single instrument + voice". Keep the accompaniment, soften the voice. The vulnerability lives in the voice, not the absence of music.

---

### Recipe: Confidence

**Vocal descriptors:** strong, clear, stable, direct, with conviction

**Lyrics formatting:**
- Declarative: "I am", "I will", "I know"
- Short, punchy phrases
- Periods for finality
- No hesitation
- Examples:
  ```
  [Verse]
  I am the storm
  I am the fire

  [Pre Chorus]
  I know what I want
  I know who I am

  [Chorus]
  I will rise
  I will fight
  I will win
  ```

**Arrangement:**
- Key: major
- BPM: 110-130
- Instrumentation: punchy, driving, full band
- Section intensity: maintains high energy throughout

**Section structure:**
- Intro: strong hook
- Verses: clear, direct
- Pre-Chorus: build
- Chorus: full band, driving
- Bridge: brief break
- Final chorus: biggest

**Anti-sparse:** always dense, driving rhythm. The confidence is in the consistency and power.

---

### Recipe: Nostalgia

**Vocal descriptors:** warm, gentle, distant, wistful, soft

**Lyrics formatting:**
- Past tense: "we used to", "I remember", "back then"
- Gentle, reflective
- Long vowels
- Examples:
  ```
  [Verse]
  I remember when
  We used to walk these streets

  [Pre Chorus]
  Before the lights went out
  Before the world changed

  [Chorus]
  Those were the days
  Those were the ways
  I miss them now
  ```

**Arrangement:**
- Key: major
- BPM: 70-90
- Instrumentation: vintage feel, soft, faded (vinyl crackle effect, muted production)
- Section intensity: gentle throughout, slight build in chorus

**Section structure:**
- Intro: distant, faded
- Verses: warm, gentle
- Pre-Chorus: subtle build
- Chorus: warmest, fullest
- Bridge: most reflective
- Outro: fading, distant

**Anti-sparse:** keep instruments present but muted. Avoid sudden loud sections.

---

### Recipe: Anxious

**Vocal descriptors:** tense, sharp, rapid, unstable, on edge

**Lyrics formatting:**
- Short, sharp words
- Repetitive
- Quick delivery
- Examples:
  ```
  [Verse]
  Where where where
  Did you go
  When when when
  Will you come back

  [Pre Chorus]
  The clock is ticking
  The walls are closing in

  [Chorus]
  Now now now
  It has to be now
  I can't wait I can't wait I can't wait
  ```

**Arrangement:**
- Key: minor
- BPM: 130-160
- Instrumentation: irregular rhythm, dissonant, sharp
- Section intensity: tense throughout, no release

**Section structure:**
- Intro: tense
- Verses: rapid
- Pre-Chorus: accelerating
- Chorus: peak anxiety
- Bridge: brief moment of dread
- Final chorus: highest anxiety

**Anti-sparse:** always present, but the tension is in the irregularity, not the silence.

---

### Recipe: Hopeful

**Vocal descriptors:** bright, rising, ascending, with growing confidence, optimistic, ascending intonation

**Lyrics formatting:**
- Future tense: "we will", "tomorrow", "I believe", "someday"
- Ascending intonations, questions with upward inflections
- Building repetition
- Examples:
  ```
  [Verse]
  I see it now
  The light is breaking through

  [Pre Chorus]
  Maybe tomorrow
  Maybe today
  Maybe this moment

  [Build Up]

  [Chorus]
  I believe I believe I believe
  We will rise
  We will fly
  We will find our way
  ```

**Arrangement:**
- Key: major
- BPM: 90-120
- Instrumentation: building, light to dense, piano + strings + light percussion
- Section intensity: continuous build from verse to chorus, the chorus is the brightest moment

**Section structure:**
- Intro: bright, ascending
- Verses: growing confidence
- Pre-Chorus: build
- Chorus: brightest, most optimistic
- Bridge: reflective but still bright
- Final chorus: peak optimism

**Anti-sparse:** all instruments always playing, building intensity. Hope is in the brightness and growth, not silence.

---

### Recipe: Tragic

**Vocal descriptors:** doomed, fated, resigned, with falling intonation, low energy, low register

**Lyrics formatting:**
- Acceptance language: "the end", "fate", "destiny", "nothing I can do", "it was always going to end this way"
- Falling inflections
- Past tense or "it is" present
- Examples:
  ```
  [Verse]
  The stars have aligned against us
  As they always would

  [Pre Chorus]
  I tried to fight it
  I tried to hold on

  [Chorus]
  This is the end
  This was always the end
  I see it now
  I see it now
  ```

**Arrangement:**
- Key: minor
- BPM: 60-80
- Instrumentation: restrained, no climax, sustained low strings
- Section intensity: monotone, no peaks, all low

**Section structure:**
- Intro: ominous
- Verses: resigned
- Pre-Chorus: acceptance
- Chorus: most resigned, but NOT explosive — it stays restrained
- Bridge: acceptance
- Final chorus: same as chorus, no escalation

**Anti-sparse:** keep instruments present but low. The tragedy is in the LACK of escalation, not in silence.

**Note:** Tragic is different from desperate. Desperate is active struggle ("I caaaan't goooo on"). Tragic is acceptance ("this is the end"). The audio for tragic has FALLING pitch and DECREASING intensity. For desperate, see that recipe.

---

### Recipe: Heroic

**Vocal descriptors:** powerful, declarative, with march-like rhythm, building, wide range

**Lyrics formatting:**
- Declarations: "we", "we will fight", "we stand", "honor", "battle"
- March rhythm (regular, predictable)
- Building repetition
- Examples:
  ```
  [Verse]
  We march to the sound of the drums
  Our banners high in the morning light

  [Pre Chorus]
  They said we'd never stand a chance
  They said we'd fall

  [Build Up]

  [Chorus]
  WE STAND
  WE FIGHT
  WE RISE
  FOR HONOR
  FOR GLORY
  FOR US
  ```

**Arrangement:**
- Key: major
- BPM: 100-120 (march tempo)
- Instrumentation: full orchestra with brass (trumpets, trombones), timpani, marching drums, choir in climax
- Section intensity: building throughout, explosive climax

**Section structure:**
- Intro: brass fanfare
- Verses: march rhythm
- Pre-Chorus: build
- Chorus: full orchestra + choir
- Bridge: brief march interlude
- Final chorus: biggest, all instruments + choir

**Anti-sparse:** all instruments always playing, dense orchestral production. Heroic is in the FULLNESS, not the silence.

**Note:** Heroic is different from triumphant. Triumphant is personal victory ("I/We won"). Heroic is collective struggle for a cause ("We march for honor"). The audio for heroic has MARCH RHYTHM. For triumphant, see that recipe.

---

### Recipe: Tender

**Vocal descriptors:** warm, gentle, soft, intimate, with affection, low effort

**Lyrics formatting:**
- Soft language: "you", "we", "hold", "touch", "love", "always", "stay"
- First person
- Gentle, no exclamation
- Examples:
  ```
  [Verse]
  Stay with me
  Just a little longer
  The night is young

  [Pre Chorus]
  I feel your hand in mine
  Your breath against my skin

  [Chorus]
  I'm holding youuu
  I'm holding yoooou
  Never let me go
  ```

**Arrangement:**
- Key: major
- BPM: 60-80
- Instrumentation: warm, piano + acoustic guitar + soft bass, no drums (or very soft brushed drums)
- Section intensity: gentle throughout, slight build in chorus

**Section structure:**
- Intro: warm, intimate
- Verses: gentle vocal, soft backing
- Pre-Chorus: subtle build
- Chorus: warmest moment, still gentle
- Bridge: most intimate
- Outro: fade to warm silence

**Anti-sparse:** present but soft. Avoid loud sections. The tenderness is in the WARMTH, not the silence.

**Note:** Tender is different from vulnerable. Vulnerable is exposed and fragile ("I... don't... know..."). Tender is warm and intimate but stable ("I love you, hold me"). Both are low energy, but tender is STABLE while vulnerable is UNSTABLE.

---

### Recipe: Sensual / Seductive

**Vocal descriptors:** breathy, low register, slow, sustained, with warm timbre, intimate

**Lyrics formatting:**
- Physical/romantic imagery: "touch", "lips", "skin", "whisper", "close", "warmth", "sensation"
- Slow delivery
- Long vowels
- Examples:
  ```
  [Verse]
  Your voice is a whisper
  Against my skin

  [Pre Chorus]
  Closer now
  Closer still

  [Chorus]
  Don't stop don't stop
  I'm not ready to let goooo
  Tonight tonight tonight
  Is ours
  ```

**Arrangement:**
- Key: minor (or modal — Dorian works well)
- BPM: 60-85
- Instrumentation: low register, breathy voice, sustained pads, R&B/soul feel, deep bass, no high-pitched instruments
- Section intensity: maintains low-mid energy, no explosive peaks

**Section structure:**
- Intro: breathy, slow
- Verses: breathy vocal, low pads
- Pre-Chorus: build subtly with bass
- Chorus: most intense moment, still low register
- Bridge: most intimate
- Outro: fade to breath

**Anti-sparse:** present but low. Avoid loud sections. The sensuality is in the LOW register and the BREATHY delivery, not the silence.

---

### Recipe: Lonely

**Vocal descriptors:** breathy, low energy, single voice, low register, isolated, with falling intonation

**Lyrics formatting:**
- Isolation: "alone", "empty", "no one", "silence", "I", "here"
- First person
- Long pauses
- Examples:
  ```
  [Verse]
  I'm sitting here
  In this empty room
  No one to talk to
  No one to call

  [Break]

  [Verse]
  The silence is deafening
  The night is long

  [Chorus]
  I'm alone
  I'm alone
  Does anyone hear me
  Does anyone care
  ```

**Arrangement:**
- Key: minor
- BPM: 60-80
- Instrumentation: very sparse, single instrument (piano OR acoustic guitar OR strings) + voice
- Section intensity: very low throughout, no climax

**Section structure:**
- Intro: single instrument
- Verses: voice + single instrument
- Pre-Chorus: subtle build with another instrument
- Chorus: most exposed, but still sparse
- Bridge: most alone
- Outro: fade to single instrument

**Anti-sparse:** present but minimal. The loneliness is in the SINGLE VOICE and the EMPTY SPACE around it, not in the absence of music.

**Note:** Lonely is different from vulnerable. Vulnerable is fragile but in the presence of someone. Lonely is alone entirely. The audio for lonely has SINGLE VOICE (no choir, no harmony). For vulnerable, see that recipe.

---

### Recipe: Playful

**Vocal descriptors:** bright, bouncy, energetic, with varied pitch, fun, mischievous

**Lyrics formatting:**
- Fun language: "let's", "fun", "play", "dance", "ha ha", "hey", "wheee", "yay"
- Short syllables
- Exclamations
- Examples:
  ```
  [Verse]
  Hey hey hey
  What's the time
  It's party time

  [Pre Chorus]
  Dancing on the table
  Dancing on the chair
  Dancing everywhere

  [Chorus]
  YEAH YEAH YEAH
  We don't care
  YEAH YEAH YEAH
  We're not going anywhere
  ```

**Arrangement:**
- Key: major
- BPM: 100-130
- Instrumentation: bouncy, syncopated, ukulele or glockenspiel, light drums, bass, claps
- Section intensity: maintains high energy with playful variation

**Section structure:**
- Intro: bouncy hook
- Verses: light, fun
- Pre-Chorus: build with syncopation
- Chorus: catchiest, most fun
- Bridge: contrast (e.g., a silly solo or rap)
- Final chorus: biggest fun

**Anti-sparse:** all instruments always playing, but the instrumentation is LIGHT (not heavy). Playful is dense but not heavy.

---

### Recipe: Haunting / Eerie

**Vocal descriptors:** low register, breathy, falling, with dark timbre, sparse, isolated

**Lyrics formatting:**
- Eerie imagery: "ghost", "shadow", "memory", "silence", "the walls", "alone", "dark"
- Slow, deliberate
- Long pauses
- Examples:
  ```
  [Verse]
  The walls are closing in
  I hear the whispers in the dark

  [Pre Chorus]
  Something is here
  Something is watching

  [Chorus]
  Stay with me
  Don't let go
  The night is looong
  And I am alone
  ```

**Arrangement:**
- Key: minor
- BPM: 60-80
- Instrumentation: very sparse, low pads, minor 2nds or tritones (dissonant intervals), breathy voice
- Section intensity: low throughout, no climax

**Section structure:**
- Intro: dissonant pad
- Verses: breathy vocal, sparse backing
- Pre-Chorus: subtle build
- Chorus: most eerie moment, still sparse
- Bridge: most haunted
- Outro: fade to dissonant silence

**Anti-sparse:** present but very sparse. Dissonance is in the INTERVALS, not the silence.

---

### Recipe: Serene / Tranquil

**Vocal descriptors:** very soft, stable, low register, slow, with no effort, peaceful

**Lyrics formatting:**
- Nature / peace imagery: "still", "calm", "peace", "breath", "water", "wind", "sky", "tree"
- Very few words
- Long pauses
- Examples:
  ```
  [Verse]
  The water is still
  The wind is soft

  [Break]

  [Verse]
  The sky is clear
  The air is cool

  [Chorus]
  Breathe... breathe...
  Let it go... let it go...
  All is well... all is well...
  ```

**Arrangement:**
- Key: major
- BPM: 50-70
- Instrumentation: ambient, pad-based, NO percussion, soft piano, soft strings
- Section intensity: very low throughout, no peaks, very low dynamic range

**Section structure:**
- Intro: long pad
- Verses: very few words, long gaps
- Pre-Chorus: subtle
- Chorus: still very quiet
- Bridge: most peaceful
- Outro: long fade

**Anti-sparse:** present but at the LOWEST possible level. The serenity is in the ABSENCE OF DYNAMICS, not the absence of music.

---

### Recipe: Celebratory

**Vocal descriptors:** bright, energetic, building, declarative, with wide dynamic range, joyful exclamations

**Lyrics formatting:**
- Togetherness: "we", "tonight", "celebrate", "joy", "us", "all of us"
- Exclamations
- Building repetition
- Examples:
  ```
  [Verse]
  The night is young
  And we are together

  [Pre Chorus]
  Raise your hands
  Raise your voice
  Raise your heart

  [Build Up]

  [Chorus]
  CELEBRATE! CELEBRATE!
  Tonight is ours!
  CELEBRATE! CELEBRATE!
  We are alive!
  ```

**Arrangement:**
- Key: major
- BPM: 110-130
- Instrumentation: full band, horns, choir, dense production
- Section intensity: builds throughout, biggest climax at final chorus

**Section structure:**
- Intro: bright hook
- Verses: building energy
- Pre-Chorus: build
- Chorus: full band + horns
- Bridge: brief reflective moment
- Final chorus: biggest, all instruments + choir

**Anti-sparse:** all instruments always playing, dense production. Celebratory is in the FULLNESS and the BUILD.

**Note:** Celebratory is different from joyful. Joyful is personal ("I'm happy"). Celebratory is collective ("We're celebrating together"). Celebratory uses horns, choir, and dense production; joyful can be sparse or dense.

---

### Recipe: Bittersweet (Emotion Combination)

**Vocal descriptors:** mixed — bright in some sections, falling in others; or stable vocal with falling delivery at key phrases

**Lyrics formatting:**
- Juxtaposition: "happy" language with sad imagery (or vice versa)
- Mixed tenses: "I remember" + "I hope" + "I miss"
- Examples:
  ```
  [Verse]  (bright, joyful delivery)
  The sun is shiiining
  The birds are siiinging
  It was the best day of my life

  [Pre Chorus]  (transitioning)

  [Chorus]  (dim, melancholic delivery)
  And now it's over
  And now you're gone
  And I'm still here... alone
  ```

**Arrangement:**
- Key: major (with minor chords mixed in) OR key changes mid-song
- BPM: 80-110
- Instrumentation: bright in verse (synths, acoustic guitar), dim in chorus (piano, strings)
- Section intensity: varies — high in bright sections, low in dim sections

**Section structure:**
- Intro: ambiguous
- Verses: bright delivery, possibly sad lyrics
- Pre-Chorus: transition
- Chorus: dim delivery, possibly happy lyrics
- Bridge: either polarity
- Final chorus: depends on which emotion wins

**Anti-sparse:** all instruments always playing, but DENSITY varies. Bright sections are dense, dim sections are sparse.

**Detection tip:** Bittersweet is detected when one section has `joyful` features and another has `melancholic` features. Use Demucs (per [`advanced-audio-analysis.md`](advanced-audio-analysis.md)) to separate vocal from accompaniment and analyze each for emotion contrast.

---

## Common Mistakes in Emotional Delivery

These are the recurring failures observed in generations. The fix for each:

| # | Mistake | Why it fails | Fix |
|---|---|---|---|
| 1 | Asking for emotion but not specifying HOW | "Sing with passion" is vague | Use specific descriptors from the recipes ("vocal effort: high, with strained delivery, falling intonation") |
| 2 | Anti-sparse rules clashing with emotion | "Intimate" prompts want to go sparse | Always reinforce "intimate but full" or "sparse but present" |
| 3 | Wrong lyrics structure for the emotion | Desperate song with short punchy syllables | Match lyrics structure to the emotion (desperate = stretched, joyful = short exclamations) |
| 4 | Wrong arrangement for the emotion | Joyful song in minor key with sparse arrangement | Match key, BPM, and density to the emotion |
| 5 | Ignoring the dynamics curve | Melancholic song with sudden loud chorus | Match dynamics to the emotional arc |
| 6 | Missing `[Break]` tags before the chorus | Chorus hits without anticipation | Add `[Break]` before the first chorus and before the final chorus |
| 7 | Wrong BPM for the emotion | Triumphant song at 60 BPM | Use the BPM range from the recipe |
| 8 | Same vocal effort throughout | Real emotional songs vary effort | Mix whispered verses with shouted choruses |
| 9 | Same vocal descriptors for all sections | Real emotional songs evolve | Add section-level instructions in the prompt |
| 10 | Using `breathy` for high-intensity songs | Breathy = intimate, low energy | Match breathiness to the emotion, not against it |
| 11 | Forgetting that the model defaults to happy | Model may add its own cheerfulness | Explicitly state the emotion: "melancholic, NOT joyful" |
| 12 | Using vague adjectives like "emotional" or "moving" | Too generic to act on | Use 2-3 specific descriptors ("desperate, raw, falling") |

## The Iteration Loop

Generating emotionally resonant music usually takes multiple attempts. The skill should iterate, not generate once and call it done.

### Standard iteration pattern

1. **First attempt**: Use the analysis output (or LLM knowledge) to build a first prompt. Generate.
2. **Listen and compare**: Which emotions are present? Which are missing? Which are exaggerated?
3. **Re-analyze if possible**: Run `analyze_vocal_emotion.py` on the generated audio. Compare features to the target.
4. **Identify the gap**: Which feature is off? Use the Common Mistakes table.
5. **Adjust one variable at a time**: Add a descriptor, change a lyric, move a `[Break]`.
6. **Regenerate**: One targeted change per iteration.
7. **Repeat**: Until the output matches the target emotion.

### Common first-attempt problems and fixes

| Problem | Likely cause | Fix |
|---|---|---|
| Output is emotionally flat | Prompt didn't emphasize emotion enough | Add 2-3 specific descriptors from a recipe |
| Output is over-the-top | Prompt was too intense | Soften descriptors, add "controlled", "measured" |
| Output emotion doesn't match request | Wrong emotion selected | Check the recipe, use the correct one |
| Output emotion correct but weak | Anti-sparse over-corrected | Reduce "always playing" emphasis, add variation cues |
| Output has emotion in verses but not chorus | Section-level instructions missing | Add per-section instructions in the prompt |
| Output pauses are wrong | `[Break]` tags in wrong places | Review lyrics structure, add `[Break]` before chorus |
| Output BPM doesn't match emotion | BPM is wrong for the emotion | Check the recipe's BPM range |
| Output energy is monotone | No dynamics curve | Add crescendo/decrescendo/wave pattern |
| Output is in wrong language | Prompt didn't specify language | Add explicit language: "in Spanish", "en français" |
| Output vocal is wrong gender | `vocals` flag not used (with `mmx`) | Use `--vocals "passionate French male vocal"` |

### Re-analysis Workflow

If the first generation has the wrong emotion:

```bash
# Step 1: Convert the output to WAV for analysis
ffmpeg -i /tmp/output.mp3 -ar 44100 /tmp/output.wav

# Step 2: Run emotion analysis on the OUTPUT
python3 scripts/analyze_vocal_emotion.py /tmp/output.wav --output /tmp/output_emotion.json

# Step 3: Compare the output's emotion to the target
# (LLM can do this comparison by reading both JSONs)

# Step 4: Identify the gap
# (LLM: "The output has 'joyful' emotion but the target was 'desperate'")

# Step 5: Adjust the prompt to address the gap
# (LLM: "Replace 'bright, energetic' with 'strained, raw, falling'")

# Step 6: Regenerate
mmx music generate \
  --prompt "<new prompt with desperate descriptors>" \
  --lyrics "..." \
  --model music-2.6 \
  --out /tmp/output_v2.mp3
```

### When to Stop Iterating

- 3+ iterations with no improvement: the prompt may be wrong, not just the parameters. Start over with a different recipe.
- The output matches the target emotion in 1-2 attempts: the prompt is good, no need to keep tweaking.
- The user is happy: stop.

### Comparison with Input (For Cover / Mashup)

If the input has audio and the goal is to preserve the emotion:

1. Run emotion analysis on the INPUT: `python3 scripts/analyze_vocal_emotion.py /tmp/input.wav --output /tmp/input_emotion.json`
2. Generate the OUTPUT.
3. Run emotion analysis on the OUTPUT: `python3 scripts/analyze_vocal_emotion.py /tmp/output.wav --output /tmp/output_emotion.json`
4. Compare:
   - Are the top emotions the same?
   - Is the intensity curve shape similar?
   - Are the per-section vocal_effort and breathiness values close?
5. If not, adjust the prompt to bring the output closer to the input's emotional profile.

This is the most rigorous way to preserve emotion in covers and mashups.

## Emotion + Style Combinations

Some combinations work better than others. Common pairings:

| Style | Best emotions | Avoid |
|---|---|---|
| French chanson | melancholy, yearning, desperation, passion | anger, joy |
| Rock | anger, defiance, confidence, triumph | vulnerability, melancholy |
| Pop | joy, love, confidence, nostalgia | anxiety, desperation |
| Ballad | vulnerability, yearning, love, melancholy | anger, defiance |
| Electronic | yearning, anxiety, confidence | melancholy, vulnerability |
| Acoustic | nostalgia, vulnerability, melancholy, love | anger, defiance |
| Hip-hop / rap | confidence, anger, defiance, anxiety | vulnerability, yearning |
| Blues | melancholy, yearning, desperation | joy, triumph |
| R&B | love, vulnerability, passion | anger, defiance |
| Country | nostalgia, love, melancholy | anger, anxiety |

For each style, the BPM, key, and instrumentation in the recipe are pre-aligned with the appropriate emotions.

## When to Skip Emotional Delivery

- The user wants an instrumental track (no vocals, so emotion is in arrangement only)
- The user is making sound design / ambient (emotion is abstract)
- The user wants a specific technical output (e.g., test the model's capabilities, not art)

For these, the emotion recipes are less relevant. Use the style categories and arrangement patterns instead.
