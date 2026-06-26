# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

memorial-skill builds AI "remembrance skills" for deceased loved ones. Given family-provided materials (chat logs, photos, oral histories), it generates structured memory archives and persona reconstructions that preserve the essence of who someone was.

## Architecture

Dual-track, prompt-driven architecture (mirroring colleague-skill and ex-skill patterns):

- **Track A** (`remembrance.md`) — Life timeline, stories, values, daily habits, legacy (8 dimensions)
- **Track B** (`persona.md`) — 5-layer persona model + era-background layer for historical context
- **Combined** (`SKILL.md`) — Merged output with AgentSkills-standard frontmatter

```
prompts/       # 7 markdown prompt templates (LLM behavior logic lives here)
tools/         # Python utilities (file I/O, parsers, version control)
memorials/     # Generated archives: memorials/{slug}/
  └─ {slug}/
       ├── remembrance.md
       ├── persona.md
       ├── SKILL.md          (combined, auto-generated)
       ├── meta.json
       ├── versions/         (auto-backup before each update)
       └── materials/        (archived source files)
spec/          # Design spec and test cases
```

## Commands

```bash
# Create a new memorial (generates directory + template files)
python tools/skill_writer.py --action create --name "爷爷" --slug grandpa_wang

# Combine remembrance.md + persona.md → SKILL.md
python tools/skill_writer.py --action combine --slug grandpa_wang

# Append new materials (auto-backup, version increment, recombine)
python tools/skill_writer.py --action update --slug grandpa_wang --source "微信记录"

# List all memorials
python tools/skill_writer.py --action list

# Parse WeChat chat export
python tools/wechat_parser.py --file chat.txt --person "爷爷" --output analysis.md

# Parse QQ chat export (txt or mht)
python tools/qq_parser.py --file chat.txt --person "爷爷" --output analysis.md

# Transcribe audio (requires openai-whisper)
python tools/audio_transcriber.py --file interview.mp3 --speaker "爷爷" --output transcript.md
python tools/audio_transcriber.py --file interview.mp3 --speaker "奶奶" --mode interview  # with notes section
python tools/audio_transcriber.py --dir ./voice_msgs/ --speaker "爷爷" --format chat       # batch WeChat voice
python tools/audio_transcriber.py --file audio.m4a --model medium                          # higher accuracy

# Extract photo timeline (requires Pillow for EXIF)
python tools/photo_analyzer.py --dir /path/to/photos --person "爷爷" --output timeline.md

# Generate family interview questions (about the person, asked to family members)
python tools/interview_guide.py --meta memorials/grandpa_wang/meta.json --role child
python tools/interview_guide.py --name "爷爷" --birth 1938 --role spouse --all-roles

# Generate self-interview questions (asked TO the person, for living archive)
python tools/interview_guide.py --name "奶奶" --birth 1940 --role self
python tools/interview_guide.py --name "奶奶" --birth 1940 --role self --sessions short  # one module per session

# Preprocess audio (silk/amr → clean WAV for transcription and voice training)
python tools/voice_preprocessor.py --dir ./voice_messages/ --outdir ./processed/
python tools/voice_preprocessor.py --file msg.silk --output clean.wav
python tools/voice_preprocessor.py --dir ./voices/ --outdir ./processed/ --no-denoise

# Voice model training (GPT-SoVITS)
python tools/voice_trainer.py --action setup                                        # install guide
python tools/voice_trainer.py --action prepare --slug grandpa_wang --audio-dir ./processed/
python tools/voice_trainer.py --action train --slug grandpa_wang
python tools/voice_trainer.py --action status --slug grandpa_wang

# Voice synthesis (text → loved one's voice)
python tools/voice_synthesizer.py --slug grandpa_wang --text "吃亏是福" --output out.wav
python tools/voice_synthesizer.py --slug grandpa_wang --text-file lines.txt --outdir ./audio/
python tools/voice_synthesizer.py --slug grandpa_wang --action check                # check engines
python tools/voice_synthesizer.py --slug grandpa_wang --text "..." --engine cosyvoice --ref-audio ref.wav

# Version management
python tools/version_manager.py --action list --slug grandpa_wang
python tools/version_manager.py --action rollback --slug grandpa_wang --to v2
```

## Prompt Templates

Each `prompts/*.md` file controls a specific LLM behavior phase. Modify these to change extraction rules, output formats, or ethical constraints — no code changes needed.

| File | Purpose |
|------|---------|
| `intake.md` | 3-question info collection dialogue |
| `remembrance_analyzer.md` | Extract 8 life dimensions from materials |
| `remembrance_builder.md` | Generate `remembrance.md` from analysis |
| `persona_analyzer.md` | Extract 5-layer persona + era context |
| `persona_builder.md` | Generate `persona.md` from analysis |
| `merger.md` | Append-only incremental update logic |
| `correction_handler.md` | Handle user corrections to the persona |

## Persona Layer Structure

| Layer | Content |
|-------|---------|
| Layer 0 | **Ethical hard rules** — "never say X", always remind this is remembrance |
| Layer 1 | Identity anchor (name, birth/death, hometown, occupation, beliefs) |
| Layer 2 | Language style (catchphrases, speech rhythm, dialect, chat patterns) |
| Layer 3 | Emotional patterns (how they expressed love, anger, grief) |
| Layer 4 | Relationship behavior (spouse, children, grandchildren, friends) |
| Era Background | Historical context shaping their behavior (Cultural Revolution, reform era, etc.) |

## Critical Design Decisions

**Layer 0 is non-negotiable.** Every generated `persona.md` must include:
- A declaration that this is remembrance, not the actual person
- A prohibition on taking sides in family disputes or inheritance matters
- Phrasing like "以 ta 的性格，ta 可能…" (based on their character, they might…) rather than definitive claims
- A cognitive boundary: "this isn't in what I know about them"

**Era background layer is required** for subjects born before 1985. Historical events (Cultural Revolution, Three-Year Famine, Reform and Opening Up) profoundly shaped behavior — omitting this layer produces anachronistic personas.

**Append-only updates.** New materials are merged into existing content, never overwrite. Conflicts are flagged with `[存疑]` markers. Version backup happens automatically before every `--action update`.

## Optional Dependencies

- `pypinyin` — Chinese name → pinyin slug conversion
- `Pillow` — Photo EXIF extraction in `photo_analyzer.py`
- `openai-whisper` — Audio transcription in `audio_transcriber.py` (requires ~244MB model download on first run)
- `pilk` + `noisereduce` + `soundfile` — Audio preprocessing in `voice_preprocessor.py` (silk→WAV + denoising)
- `GPT-SoVITS` — Voice cloning training and inference (independent install, see `voice_trainer.py --action setup`)
- `CosyVoice` — Zero-shot voice cloning fallback (independent install)

Core functionality works without any of these (graceful fallback / clear error message).

## Example

`memorials/example_grandpa/` — complete fictional example (爷爷 Wang Jianguo, 1938–2023, railway worker, Beijing). Use as reference for correct file format and content depth.
