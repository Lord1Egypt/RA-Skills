---
name: Hum2Song
description: Hum2Song turns a hummed or sung melody into a complete song with local audio processing, MIDI extraction, and optional AI-assisted arrangement, without uploading sensitive recordings to third-party services.
---

# Hum2Song

Turn a hummed melody into a complete song with local audio processing, without uploading sensitive recordings to third-party services.

---

## Overview

This skill converts user humming or singing into complete songs using local AI models. The entire pipeline runs on your machine - no audio data is sent to external services.

**Pipeline:**
1. 🎤 Audio Input → 2. 🎵 MIDI Extraction → 3. 🎼 Music Generation → 4. 🎧 Complete Song

---

## Triggers

Use this skill when the user:
- Hums or sings a melody and wants to turn it into a full song
- Has an audio recording of humming/singing
- Wants to create music from their own melodic ideas
- Asks to "turn my humming into a song"

---

## Requirements

### System Dependencies

```bash
# macOS
brew install ffmpeg fluidsynth

# Ubuntu/Debian
sudo apt-get install ffmpeg fluidsynth

# Python packages
pip install basic-pitch pretty_midi librosa soundfile numpy
```

### Optional: ACE-Step for Music Generation (User Choice)

ACE-Step is an optional local AI. Users decide whether to install it.

```bash
# User manually installs if they want AI generation
# Otherwise, default SoundFont synthesis works without AI
git clone https://github.com/ace-step/ace-step.git
pip install -r ace-step/requirements.txt
```

**Note:** First use downloads ~4GB model weights to local cache. No automatic downloads.

---

## Core Workflow

### Step 1: Extract MIDI from Audio

Use Basic Pitch (Spotify's open source tool) to convert humming to MIDI:

```python
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

# Convert audio to MIDI
model_output, midi_data, note_events = predict("humming.wav")
midi_data.write("extracted.mid")
```

### Step 2: Enhance MIDI Structure

Clean and enhance the extracted MIDI:

```python
import pretty_midi

# Load extracted MIDI
pm = pretty_midi.PrettyMIDI("extracted.mid")

# Quantize notes to fix timing
for instrument in pm.instruments:
    for note in instrument.notes:
        note.start = round(note.start * 4) / 4  # Quantize to 16th notes
        note.end = round(note.end * 4) / 4

# Save enhanced MIDI
pm.write("enhanced.mid")
```

### Step 3: Generate Full Song

**Option A: ACE-Step (Local AI, Optional)**

Only if user has manually installed ACE-Step:

```python
from ace_step import MusicGenerator

# Load model (runs locally, downloads weights on first use)
generator = MusicGenerator.from_pretrained("ace-step/base")

# Generate music from MIDI
audio = generator.generate_from_midi(
    midi_path="enhanced.mid",
    style="pop",
    mood="upbeat",
    duration=120
)

# Save result
audio.save("complete_song.mp3")
```

**Option B: MIDI + SoundFont (No AI)**

```python
import pretty_midi

# Load MIDI
pm = pretty_midi.PrettyMIDI("enhanced.mid")

# Synthesize with high-quality SoundFont
audio_data = pm.fluidsynth(fs=44100, sf2_path="path/to/good_soundfont.sf2")

# Save as WAV
import soundfile as sf
sf.write("complete_song.wav", audio_data, 44100)
```

---

## Usage

### Quick Start

```bash
# Run the complete pipeline
python ~/.openclaw/skills/hum2song/scripts/hum2song.py \
  --input my_humming.wav \
  --style pop \
  --mood upbeat \
  --output my_song.mp3
```

### Parameters

| Parameter | Description | Options |
|-----------|-------------|---------|
| `--input` | Input audio file | Any audio format |
| `--style` | Music style | pop, rock, jazz, classical, electronic |
| `--mood` | Song mood | upbeat, calm, energetic, melancholic |
| `--duration` | Target duration (seconds) | 30-300 |
| `--output` | Output file path | .mp3, .wav, .mid |

---

## Response Format

### When User Provides Audio

```
🎵 I'll convert your humming into a complete song!

**Processing Pipeline:**
1️⃣ Extracting melody from your audio...
2️⃣ Converting to MIDI notation...
3️⃣ Generating full arrangement...
4️⃣ Rendering final song...

⏱️ Estimated time: 2-5 minutes

**Settings:**
• Style: {style}
• Mood: {mood}
• Duration: {duration}s

Processing now... 🎧
```

### When Complete

```
✅ Your song is ready!

📁 Output: {output_path}
🎼 Format: {format}
⏱️ Duration: {actual_duration}s

**What was done:**
• Extracted {note_count} notes from your humming
• Generated {instrument_count} instrument tracks
• Applied {style} style with {mood} mood

💡 You can:
• Adjust style/mood and regenerate
• Export as MIDI for editing in DAW
• Try different AI models for variation
```

---

## Example Interactions

### Example 1: User Hums Audio
```
User: [uploads humming audio]

AI: 🎵 I'll convert your humming into a complete song!

**Processing Pipeline:**
1️⃣ Extracting melody from your audio...
2️⃣ Converting to MIDI notation...
3️⃣ Generating full arrangement...
4️⃣ Rendering final song...

⏱️ Estimated time: 2-5 minutes

What style would you like?
• Pop (default)
• Rock
• Jazz
• Classical
• Electronic
```

### Example 2: User Specifies Style
```
User: Turn this humming into a jazz song

AI: 🎷 Jazz transformation incoming!

Processing your humming with jazz style:
• Swing rhythm
• Walking bass line
• Piano chords
• Brush drums

[Processing...]

✅ Your jazz song is ready!
📁 Output: ~/Music/hum2song_jazz_20240321.mp3
```

### Example 3: User Wants MIDI Output
```
User: Can I get the MIDI file to edit myself?

AI: 🎼 Absolutely!

I'll generate:
• Extracted MIDI (raw melody)
• Enhanced MIDI (quantized, cleaned)
• Full arrangement MIDI (all instruments)

All files will be in: ~/Music/hum2song_export/
```

---

## Technical Details

### Audio Processing

**Input Formats:** WAV, MP3, M4A, FLAC, OGG
**Sample Rate:** Automatically converted to 44.1kHz
**Channels:** Mono/Stereo → Mono for processing

### MIDI Extraction

**Model:** Basic Pitch (Spotify, ICASSP 2022)
**Pitch Range:** C1 to C8
**Note Detection:** Polyphonic capable
**Timing Resolution:** 10ms

### Music Generation

**ACE-Step Model:**
- Size: 1B parameters (base), 3B (large)
- Training: Licensed music dataset
- Output: 44.1kHz stereo
- Latency: ~1s per second of audio on M1 Mac

**SoundFont Synthesis:**
- No AI required
- Real-time synthesis
- High-quality instrument sounds
- Deterministic output

---

## Limitations

- Requires local Python environment setup
- ACE-Step needs ~4GB RAM for base model
- Processing time: 2-5 minutes for a 2-minute song
- Quality depends on humming clarity
- Complex harmonies may not be fully captured

---

## Privacy & Security

✅ **All processing is local** - Your audio never leaves your machine
✅ **No cloud services** - No API keys or external uploads
✅ **Open source tools** - Basic Pitch, ACE-Step, Pretty MIDI
✅ **No data collection** - Nothing is logged or transmitted

---

## References

- `basic-pitch.md` - Audio to MIDI extraction
- `ace-step.md` - AI music generation
- `pretty_midi.md` - MIDI processing
- `librosa.md` - Audio analysis utilities

---

## Technical Information

| Attribute | Value |
|-----------|-------|
| **Name** | Hum2Song |
| **Slug** | hum2song |
| **Version** | 3.0.4 |
| **Category** | Audio / Music Generation |
| **Tags** | music, audio, midi, ai-generation, local-processing |
| **License** | MIT-0 |

---

**Note:** This skill requires local setup of Python dependencies. All audio processing happens on your device for maximum privacy.
