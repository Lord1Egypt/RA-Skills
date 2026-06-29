# Advanced Audio Analysis with Free Tools

The base emotion analysis in [`emotion-analysis.md`](emotion-analysis.md) uses `librosa` + `parselmouth` (Praat) + `scipy` to extract per-section features. Those cover the core 30 emotions. This file covers **advanced free tools** that go deeper: more accurate pitch, source separation, note transcription, music theory, and pre-trained emotion / genre / mood classifiers.

All tools listed here are **open source** (BSD, MIT, Apache, or GPL). All can be installed via `pip` (some need system dependencies like `ffmpeg`). They are **optional** — the base skill works without them. Install only what you need.

---

## Currently Implemented Advanced Features (v0.1.0)

The following advanced analysis features **are now implemented** in the MiniMax layer. Each is available as an optional dependency and is used in the prompt pipeline to enrich generation prompts with precise audio characteristics.

| Feature | Library | What it detects | Pip package |
|---|---|---|---|
| **tempogram_ratio** | librosa | Swing / groove feel ( eighth-note swing ratio ) | `librosa` (already in base) |
| **tonnetz** | librosa | Tonal harmony quality — diatonic/chromatic, consonant/dissonant | `librosa` (already in base) |
| **spectral_contrast** | librosa | Valley-to-peak energy ratio per frequency band (timbre) | `librosa` (already in base) |
| **HPSS** | librosa.effects.hpss | Harmonic-percussive source separation | `librosa` (already in base) |
| **Formant analysis** | parselmouth | Vocal register detection — chest / head / falsetto | `parselmouth` (already in base) |
| **HNR** | parselmouth | Harmonics-to-noise ratio — breathiness vs clarity | `parselmouth` (already in base) |
| **Jitter / Shimmer** | parselmouth | Microperturbations in pitch and amplitude — voice stability | `parselmouth` (already in base) |
| **LUFS / LRA** | pyloudnorm | Perceptual loudness (integrated LUFS) and loudness range (LRA) | `pyloudnorm` |
| **Chord progression** | autochord | Automatic chord symbol extraction | `autochord` |
| **Song structure** | allin1 | Neural structure segmentation — intro / verse / chorus / bridge / outro | `allin1` |
| **CLAP classification** | transformers | Zero-shot genre / mood / instrument / era classification | `transformers` |

### tempogram_ratio (librosa)

Detects swing and groove by measuring the deviation of note onsets from a perfectly regular grid. A ratio near 1.0 is straight; above ~1.2 indicates a noticeable swing feel.

**Pipeline use**: When the user wants "groovy" or "laid-back" output, `tempogram_ratio` quantifies the swing intensity to pass a precise BPM/swing hint to `mmx`.

```python
import librosa

y, sr = librosa.load('/tmp/song.wav')
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
oenv = librosa.onset.onset_strength(y=y, sr=sr, feature_mode='spectral')
tempogram = librosa.feature.tempogram(oenv=oenv, sr=sr)
# Ratio of beat-strength deviations indicates swing
```

### tonnetz (librosa)

Computes the tonal centroid features (Tonnetz) representing harmonic relationships in the circle-of-fifths space. High diatonic weight = consonant; high chromatic weight = more tension/dissonance.

**Pipeline use**: Maps directly to "consonant/dissonant", "epic/tense", or "warm/dark" style cues in the generation prompt.

```python
y, sr = librosa.load('/tmp/song.wav')
chrom = librosa.feature.chroma_cqt(y=y, sr=sr)
tonnetz = librosa.feature.tonnetz(chroma=chrom)
# tonnetz shape: (6, frames) — dims represent 5ths, minor/major
```

### spectral_contrast (librosa)

Measures the energy ratio between spectral peaks (high energy frequency bands) and valleys (low energy bands) across octave bands. High contrast = bright/drill; low contrast = dark/mellow.

**Pipeline use**: Feeds the "bright/dark" and "warm/cold" timbre dimension in prompt construction.

```python
y, sr = librosa.load('/tmp/song.wav')
contrast = librosa.feature.spectral_contrast(y=y, sr=sr, n_bands=6)
# contrast shape: (7, frames) — 6 bands + overall valley mean
```

### HPSS — Harmonic-Percussive Separation (librosa.effects.hpss)

Decomposes audio into a harmonic component (melody/harmony) and a percussive component (drums/transients). Useful for isolating the vocal melody from rhythmic masking.

**Pipeline use**: Before running pitch or emotion analysis, HPSS can clean the vocal to reduce rhythmic interference.

```python
y, sr = librosa.load('/tmp/song.wav')
harmonic, percussive = librosa.effects.hpss(y=y)
```

### Formant analysis (parselmouth)

Extracts formant frequencies (F1, F2, F3) and their trajectories to detect vocal register — chest voice (low F1, high F2), head voice (high F1, low F2), falsetto (very high F1, very low F2).

**Pipeline use**: Feeds vocal register cues ("chesty belt", "head voice mix", "falsetto float") to `mmx --vocal-style`.

```python
import parselmouth

sound = parselmouth.Sound('/tmp/vocal.wav')
formants = sound.to_formant_burg()
# F1/F2 at voiced segments indicate register
```

### HNR — Harmonics-to-Noise Ratio (parselmouth)

Ratio of harmonic energy to noise energy. High HNR = clear/clean voice; low HNR = breathy/aspirate. Range: 0–30 dB typical.

**Pipeline use**: Maps to "breathy" vs "focused" vocal quality descriptors in the prompt.

```python
import parselmouth

sound = parselmouth.Sound('/tmp/vocal.wav')
hnr = sound.to_harmonicity()
```

### Jitter and Shimmer (parselmouth)

- **Jitter**: cycle-to-cycle variation in fundamental frequency (pitch instability)
- **Shimmer**: cycle-to-cycle variation in amplitude (volume instability)

Both measure voice quality stability. High jitter/shimmer = unstable, tense, or emotional voice; low = steady, controlled.

**Pipeline use**: Contributes to "controlled/emotional" and "steady/wavering" vocal quality cues.

```python
import parselmouth

sound = parselmouth.Sound('/tmp/vocal.wav')
point_process = sound.to_point_process()
jitter = point_process.get_jitter()
shimmer = point_process.get_shimmer()
```

### LUFS and LRA (pyloudnorm)

- **Integrated LUFS**: overall perceived loudness (EBU R128 standard)
- **LRA (Loudness Range)**: dynamic range in LUFS — difference between loud and quiet sections

**Pipeline use**: LUFS informs the "loudness feel" (quiet/quiet, loud/dynamic); LRA informs the "dynamic range" descriptor in the prompt (e.g., "wide LRA — lots of contrast between verse and chorus").

```python
import pyloudnorm as pyln

meter = pyln.Meter(44100)  # create BS.1770 meter
loudness = meter.integrated_loudness('/tmp/song.wav')
# For LRA, use pyloudnorm's full workflow with anchored loudness
```

### Chord progression (autochord)

Automatically detects chord symbols (roman numerals and chord types) from audio using a pre-trained CNN/RNN model.

**Pipeline use**: Extracts "I-V-vi-IV" or "i-bVII-bVI-bVII" style progressions to include as harmonic context in the prompt.

```python
import autochord

chords = autochord.recognize('/tmp/song.wav')
# Returns list of (timestamp, chord_symbol)
```

### Song structure (allin1)

Neural network-based structural segmentation. Detects: intro, verse, pre-chorus, chorus, bridge, outro. Also returns segment boundaries with confidence scores.

**Pipeline use**: Feeds the `mmx --structure` flag with accurate segment timing instead of generic defaults.

```python
from allin1 import StructuralAnalysis

analyzer = StructuralAnalysis()
segments = analyzer.analyze('/tmp/song.wav')
# Returns: [{'label': 'chorus', 'start': 15.2, 'end': 30.1, 'confidence': 0.94}, ...]
```

### CLAP classification (transformers)

Zero-shot audio classification using the CLAP (Contrastive Language-Audio Pretraining) model. Can classify genre, mood, instrument, and era without training data for the specific labels.

**Pipeline use**: Provides genre/mood tags as soft constraints for the prompt builder ("80s pop", "melancholic indie folk", "aggressive metal").

```python
from transformers import pipeline
import torch

clap = pipeline("audio-classification", model="laion/clap-htsat-unfused")
# Zero-shot labels
results = clap('/tmp/song.wav', candidate_labels=["pop", "rock", "jazz", "classical", "hip-hop"])
```

---

## Future / Roadmap

The following tools are **roadmap items** for upcoming phases of the analysis pipeline.

| Tool | License | Phase | What it adds | When to use |
|---|---|---|---|---|
| **Demucs** | MIT | Phase 2 | Source separation: vocals / drums / bass / other | When you need to analyze the vocal track WITHOUT the accompaniment masking it (huge for emotion analysis). Opt-in via `--use-demucs` flag on the orchestrator. |
| **Basic Pitch** | Apache-2.0 | Phase 3.2 | Convert audio to MIDI notes | When you need the melody as MIDI for comparison (e.g., cover similarity) or MIDI-confirmed key/scale detection. |
| **beat_this** | MIT | Phase 3.1 | ISMIR 2024 SOTA beat + downbeat tracker (transformer-based) | Replaces `librosa.beat.beat_track` for more accurate downbeats. Used for prompt-level timing cues. |
| **MERT v1-330M** | Apache-2.0 | Phase 3.3 | Music SSL embeddings, complementary to CLAP | Use for "vibe similarity" scoring between two songs (mashup). |
| **PANNs / AST** | MIT | Phase 3.4 | 527-class instrument classification via AudioSet | Second opinion to CLAP for instrument detection (oud, sitar, bouzouki, etc.). |
| **OpenCLIP** | MIT | Phase 4.1 | Image zero-shot style classification | Album art → "this is synthwave / indie / metal" classification. |
| **RapidOCR** | Apache-2.0 | Phase 4.2 | On-device OCR via ONNX | Album-art text / on-screen video subtitles. |
| **DeepFace / MediaPipe** | MIT / Apache-2.0 | Phase 4.3 | Face detection + emotion | Album art with a face → "warm, joyful" mood. |
| **Qwen3-VL** | Apache-2.0 | Phase 4.5 / 5.4 | Multi-modal vision-language model | Image / video captioning (free-form description). GPU-only, opt-in. |
| **InternVideo2** | Apache-2.0 | Phase 5.5 | Video action recognition | Music video → "concert / dance / performance" classification. |

### Already implemented (v0.1.0+)

- **Whisper** (MIT, `extract_lyrics_whisper.py`) — lyrics extraction with section tagging. Auto-wired into the orchestrator via `--lyrics` flag.

### Will NOT be added (license / maintenance)

| Tool | Why not |
|---|---|
| **Essentia** (AGPL-3.0) | AGPL is not compatible with clean skill distribution. |
| **YOLO Ultralytics** (AGPL-3.0) | Same. Use OpenCLIP / MediaPipe instead. |
| **ImageBind** (CC-BY-NC 4.0) | Non-commercial weights; not safe for distributed skills. |
| **audiocraft / MusicGen weights** (CC-BY-NC) | Non-commercial. EnCodec encoder code (MIT) is fine to use. |
| **madmom** | Unmaintained since 2019; `beat_this` is the replacement. |
| **Spleeter** | Unmaintained since 2020; Demucs is the replacement. |

## Essentia

Essentia is the most comprehensive open source audio analysis library. It has pre-trained classifiers for mood, genre, and danceability.

### Install

```bash
# Ubuntu / Debian (Essentia needs ffmpeg and other system deps)
apt install ffmpeg libfftw3-dev libyaml-dev libsamplerate0-dev libtag1-dev
pip install essentia

# macOS
brew install pkg-config ffmpeg libyaml libsamplerate taglib
pip install essentia
```

### What it gives you

Essentia provides hundreds of audio features, but the most useful for emotion analysis are:

| Feature | What it measures | Use |
|---|---|---|
| `danceability` | 0–1, how suitable the track is for dancing | Energy + rhythm regularity |
| `arousal` | 0–1, intensity of emotion (low = calm, high = excited) | Maps to overall energy |
| `valence` | 0–1, positivity (low = sad, high = happy) | Maps to joy / melancholy |
| `mood_classifier` | Pre-trained, outputs `happy` / `sad` / `aggressive` / `relaxed` | Direct emotion label |
| `genre_classifier` | Pre-trained on 8 genres | Genre inference |
| `key` and `scale` | Detected key and mode (major / minor) | Maps to mood |
| `bpm` | Tempo | Direct BPM |
| `loudness` | Integrated loudness in LUFS | Production quality |

### Usage example

```python
import essentia.standard as es

# Load audio
audio = es.MonoLoader(filename='/tmp/song.wav', sampleRate=44100)()

# Mood classification
mood_classifier = es.MusicExtractor()(audio)
print(f"Valence: {mood_classifier['valence']}")
print(f"Arousal: {mood_classifier['arousal']}")
print(f"Danceability: {mood_classifier['danceability']}")
print(f"BPM: {mood_classifier['bpm']}")
print(f"Key: {mood_classifier['key_key']} {mood_classifier['key_scale']}")
```

The pre-trained mood classifier outputs one of: `happy`, `sad`, `aggressive`, `relaxed`. Map these to the 25+ emotion set in [`emotion-analysis.md`](emotion-analysis.md):

| Essentia mood | Maps to |
|---|---|
| `happy` | joyful, triumphant, celebratory, confident |
| `sad` | melancholic, yearning, vulnerable, lonely, tragic |
| `aggressive` | angry, defiant, desperate, anxious |
| `relaxed` | serene, tender, nostalgic, calm |

### When to use

- You want a quick automated mood label (saves LLM inference)
- You're processing many tracks and need a consistent classifier
- You want a confidence score for the mood (Essentia gives probabilities)
- You want a valence-arousal 2D space mapping (useful for "mood is between sad and angry")

### Limitations

- License is AGPL-3 — if you distribute the skill, you may need to comply. For personal use, fine.
- The mood classifier is trained on Western pop/rock/electronic. Less accurate on jazz, classical, world music.
- Valence / arousal is a 2D reduction — misses nuances (e.g., "angry" and "joyful" can both have high arousal but very different valence).

## Demucs

Demucs (by Facebook Research) separates audio into stems: vocals, drums, bass, and other. This is huge for emotion analysis because the vocals carry the emotion, but the accompaniment masks it.

### Install

```bash
pip install demucs
# First run downloads the pre-trained model (~2 GB)
```

### What it gives you

Four stems: `vocals.wav`, `drums.wav`, `bass.wav`, `other.wav` (instruments other than drums/bass, like guitar, keys, synths).

By separating vocals from accompaniment, you can:

- Run emotion analysis on the isolated vocal track (cleaner features, no masking)
- Run a separate analysis on the drums (for rhythm / energy features)
- Compare vocal emotion vs accompaniment energy (a song can have sad vocals over a happy beat = bittersweet)

### Usage example

```bash
# Separate stems (writes to /tmp/separated/htdemucs/<song_name>/)
python3 -m demucs --two-stems vocals /tmp/song.wav

# Output:
# /tmp/separated/htdemucs/song/vocals.wav   ← clean vocal
# /tmp/separated/htdemucs/song/no_vocals.wav ← accompaniment only
```

For four-stem separation:

```bash
python3 -m demucs /tmp/song.wav
# /tmp/separated/htdemucs/song/{vocals,drums,bass,other}.wav
```

Then run emotion analysis on the isolated vocal:

```bash
python3 scripts/analyze_vocal_emotion.py \
  /tmp/separated/htdemucs/song/vocals.wav \
  --output /tmp/vocal_emotion.json
```

### When to use

- The input is a full mix and emotion analysis on the mix is inaccurate
- You want to detect "sad vocals over happy beat" (bittersweet) — analyze each separately
- You want to extract just the vocal for use as a reference (e.g., to sing-along)
- You're building a karaoke version of the song

### Performance note

Demucs is slow on CPU (1–5 minutes per song). On GPU, much faster (10–30 seconds). It also downloads a 2GB model on first use.

For a small VPS, prefer the `--two-stems vocals` mode (faster, smaller model) over the full 4-stem separation.

## Basic Pitch

Basic Pitch (by Spotify) converts audio to MIDI notes. Useful for melody comparison (e.g., how similar is the input's melody to the output).

### Install

```bash
pip install basic-pitch
# Or for GPU:
pip install basic-pitch[onnx]
```

### What it gives you

- Note events with onset, offset, pitch, confidence
- MIDI file output
- Useful for: melody comparison, cover analysis, harmonic analysis

### Usage example

```python
from basic_pitch import ICASSP_2021_MODEL_PATH
from basic_pitch.inference import predict as bp_predict
from basic_pitch import build_output

model_output, midi_data, note_events = bp_predict(
    '/tmp/song.wav',
    onset_threshold=0.5,
    frame_threshold=0.3,
    minimum_note_length=50,
    minimum_frequency=80,
    maximum_frequency=1000
)

# Save as MIDI
build_output.write_midi(
    note_events,
    '/tmp/song.midi'
)

# note_events is a list of (start_time, end_time, pitch_midi, velocity, [pitch_bend])
```

### When to use

- You want to compare melodies between the input and the output (cover accuracy)
- You want to extract the input's melody to use in a new composition
- You're building music theory analysis (chord progressions, scales)
- You want a MIDI representation of an audio input for use in a DAW

## Music21

Music21 is a Python toolkit for music theory analysis. It can detect key, chord progressions, scales, and intervals.

### Install

```bash
pip install music21
# Music21 uses LilyPond for rendering (optional, only if you want visual output)
# It also has a corpus of public-domain scores
```

### What it gives you

- Key detection (more sophisticated than chroma-based)
- Chord progression extraction
- Roman numeral analysis (I, IV, V, vi, etc.)
- Scale / mode detection (major, minor, dorian, phrygian, ...)
- Interval analysis
- Score comparison

### Usage example

```python
from music21 import converter, analysis

# Convert audio to MIDI first (via basic_pitch)
# Then load the MIDI
score = converter.parse('/tmp/song.midi')

# Key analysis
key = score.analyze('key')
print(f"Key: {key.tonic} {key.mode}")

# Chord analysis (if the score has chords)
for chord in score.chordify():
    print(f"Chord at {chord.offset}: {chord.pitches}")
```

### When to use

- You want to know the exact chord progression of the input
- You want to suggest a chord progression for the output (e.g., vi-IV-I-V in C major)
- You're analyzing a piece in a non-Western scale (music21 supports many)
- You want to compare two pieces' harmonic content

### Limitations

- Music21 works best with symbolic input (MIDI, MusicXML). Converting audio to MIDI first (via Basic Pitch) loses some fidelity.
- Chord detection on converted MIDI is approximate — drums and non-pitched instruments confuse it.

## CREPE

CREPE is a monophonic pitch detection model (CNN-based). More accurate than librosa's `pyin` for vocals but requires GPU for fast inference.

### Install

```bash
pip install crepe
# Or for the latest version:
pip install git+https://github.com/marl/crepe.git
```

### What it gives you

- Frame-level pitch detection (every 10ms) with high accuracy
- Confidence per frame
- Useful for: detailed pitch contour analysis, vibrato detection, pitch bend precision

### Usage example

```python
import crepe
from scipy.io import wavfile

sr, audio = wavfile.read('/tmp/song.wav')
time, frequency, confidence, activation = crepe.predict(
    audio, sr, viterbi=True, model_capacity='full'
)
```

### When to use

- You need very accurate pitch detection (e.g., for detailed vibrato analysis)
- The vocal is monophonic (one singer at a time)
- You're OK with the GPU requirement (CPU is too slow for full songs)

For most use cases, parselmouth (already in the base skill) is enough. CREPE is the next level when you need frame-level precision.

## Whisper (already in OpenClaw)

Whisper is OpenAI's speech-to-text model. The OpenClaw runtime has it (per TOOLS.md).

### Usage example

```bash
whisper /tmp/song.wav --language en --model medium --output_format srt
# Output: /tmp/song.srt with timestamps
```

Or use the OpenAI API directly for programmatic access.

### When to use

- You need lyrics extraction from audio (for cover workflow ASR)
- The cover workflow's two-step path uses ASR-extracted lyrics (correctable in the second step)
- The user provides audio but no lyrics (extract the lyrics, then use as Input Type 2)

Whisper is already in the runtime, so no install needed.

## Integration Patterns

### Pattern 1: Clean vocal emotion analysis

```bash
# Step 1: Separate vocals (Demucs)
python3 -m demucs --two-stems vocals /tmp/song.wav

# Step 2: Analyze clean vocal
python3 scripts/analyze_vocal_emotion.py \
  /tmp/separated/htdemucs/song/vocals.wav \
  --output /tmp/vocal_emotion.json

# Step 3: Optional — analyze accompaniment for energy
python3 scripts/analyze_audio.py \
  /tmp/separated/htdemucs/song/no_vocals.wav \
  > /tmp/accompaniment.json

# Step 4: Compare vocal emotion vs accompaniment energy
# (LLM: "vocal_emotion = melancholic, accompaniment = high energy → bittersweet")
```

### Pattern 2: Mood + genre classification

```python
import essentia.standard as es

audio = es.MonoLoader(filename='/tmp/song.wav', sampleRate=44100)()
features, _ = es.MusicExtractor()(audio)

mood = features['highlevel.mood_classifier']['value']
valence = features['valence']
arousal = features['arousal']
genre = features['highlevel.genre_classifier']['value']
```

### Pattern 3: MIDI + theory for harmonic context

```bash
# Step 1: Convert audio to MIDI
python3 -c "from basic_pitch.inference import predict; predict('/tmp/song.wav')"

# Step 2: Analyze the MIDI
python3 -c "
from music21 import converter
score = converter.parse('/tmp/song.midi')
key = score.analyze('key')
print(f'Key: {key.tonic} {key.mode}')
"
```

### Pattern 4: Cover accuracy via pitch comparison

```python
# Step 1: Extract melody from input
from basic_pitch.inference import predict
_, _, input_notes = predict('/tmp/input.wav')

# Step 2: Extract melody from output
_, _, output_notes = predict('/tmp/output.wav')

# Step 3: Compare (custom logic — note overlap, timing offset, etc.)
# (LLM does the high-level comparison)
```

## When to Use Which Tool

| Goal | Best tool combo |
|---|---|
| Quick mood label (without LLM) | Essentia |
| Clean vocal emotion analysis | Demucs + librosa/parselmouth |
| Melody comparison (cover accuracy) | Basic Pitch + custom comparison |
| Chord progression extraction | Basic Pitch + Music21 |
| Very accurate pitch tracking | CREPE (GPU) or parselmouth (CPU) |
| Lyrics extraction from audio | Whisper (already in runtime) |
| Source separation (for karaoke, etc.) | Demucs |
| Genre classification | Essentia |

## When NOT to Use These

These tools are enhancements, not requirements. Skip them if:

- The base analysis (librosa + parselmouth) is enough
- You can't install new dependencies
- You're working with very short clips (< 5 seconds) — the analysis is unreliable
- You don't have GPU and the tool is GPU-only (CREPE)

## Installation Best Practices

For the Pre-Flight Check, list the new tools as OPTIONAL with the right install commands. The full per-platform table:

| Tool | Linux (apt) | macOS (brew) | Windows (winget) | Pip alternative |
|---|---|---|---|---|
| Essentia | `apt install ffmpeg libfftw3-dev libyaml-dev libsamplerate0-dev libtag1-dev && pip install essentia` | `brew install ffmpeg libyaml libsamplerate taglib && pip install essentia` | (use conda or WSL) | — |
| Demucs | (system deps via pip) | (system deps via brew) | (use WSL) | `pip install demucs` |
| Basic Pitch | (system deps via pip) | (system deps via brew) | (use WSL) | `pip install basic-pitch` |
| Music21 | `pip install music21` | `pip install music21` | `pip install music21` | `pip install music21` |
| CREPE | (needs TensorFlow, complex) | (needs TensorFlow) | (needs WSL) | `pip install crepe` |

For the most common case (Ubuntu/Debian), the install command is:

```bash
# Install all advanced tools
apt install ffmpeg libfftw3-dev libyaml-dev libsamplerate0-dev libtag1-dev
pip install essentia demucs basic-pitch music21
```

This adds ~5 minutes to the install time and ~3GB of disk space (mostly Demucs models).

## License and Distribution Notes

- **Essentia** is AGPL-3. If you distribute the skill with Essentia integrated, the AGPL may apply. For personal use, fine.
- **Demucs, Basic Pitch, Music21, CREPE** are MIT / Apache / BSD — permissive, no copyleft concerns.
- **Whisper** is MIT — fine.

For ClawHub distribution, document the dependencies clearly. If AGPL is a concern, Essentia can be moved to "optional, off by default" and the user enables it explicitly.

## Confidence Levels

The following conventions apply to all analysis scripts, including the optional tools documented above.

Every numeric or categorical detection in the analysis must carry a confidence value so weak detections do not get treated as facts.

| Confidence | Numeric range | Interpretation |
|---|---|---|
| `clear` | n/a | The detection is unambiguous (e.g. user-supplied text, MIDI-confirmed key). |
| `high` | `>= 0.75` | Strong evidence from multiple sources or models. |
| `medium` | `0.5 - 0.74` | Reasonable evidence but alternative interpretations exist. |
| `low` | `< 0.5` | Weak signal; treat as a hint, not a fact. |
| `inferred` | n/a | Not measured directly; derived from context (e.g. lyrics from a YouTube URL). |
| `missing` | n/a | Not available; the analysis did not run or did not find evidence. |

When feeding analysis into a prompt, prefix any `low` or `medium` detection with a hedge like "around" or "approximately", and never include `missing` values as if they were facts.

## Fallback Behavior for Missing Optional Dependencies

The advanced analysis scripts depend on optional packages (librosa, parselmouth, transformers, demucs, beat_this, basic_pitch, etc.). Each script must:

1. Try to import the optional dependency at the top of the function.
2. On `ImportError`, return a JSON object that includes `{"error": "install with pip install X", "summary": {}}` instead of raising.
3. Never let a missing optional dependency crash the whole workflow.

The orchestrator at [`../scripts/analysis_orchestrator.py`](../scripts/analysis_orchestrator.py) collects per-script results and continues even if some scripts failed. The combined `summary` simply omits keys whose underlying analysis could not run. The linter, prompt builder, and generation step all read the summary and skip missing keys without erroring.

This means a user without `demucs` installed can still get tempo, key, and structure analysis from the base pipeline. The only loss is the per-stem vocal analysis, which is opt-in via `--use-demucs`.
