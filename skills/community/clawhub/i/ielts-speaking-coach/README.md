# IELTS Speaking Coach

An OpenClaw skill that acts as a professional IELTS Speaking Examiner and Tutor. Get instant, evidence-based assessment of your spoken English with actionable feedback — including real pronunciation scoring from audio input.

## Features

- **Four-criterion scoring** (Band 1-9, 0.5 increments): Fluency & Coherence, Lexical Resource, Grammar, Pronunciation — each with specific transcript evidence
- **Audio pronunciation scoring**: Send voice messages for real PR band scores via ffmpeg + ASR (text-only mode estimates PR from other criteria)
- **CHAI-calibrated scores**: Human-prior calibration adjusts for Part difficulty and criterion bias
- **Mock exam simulation** (Menu 7): Full Part 1→2→3 timed test with no in-test feedback and comprehensive final report
- **ZPD learning paths** (Menu 6): Personalized vocabulary and grammar progression based on your current band level
- **Adaptive difficulty**: Questions automatically adjust to your band level
- **Grammar corrections**: Identifies genuine spoken grammar errors with minimal corrections and rule explanations
- **Context-aware vocabulary upgrades**: Topic-specific collocational improvements, not generic thesaurus swaps
- **Pronunciation guidance**: Targeted tips for Chinese speakers covering th/v/r/l, stress, rhythm, intonation, and connected speech
- **Spoken-register model answers**: Rewrites at your target band using natural discourse markers, contractions, and idiomatic language
- **All three Parts**: Part 1 (Interview), Part 2 (Long Turn), Part 3 (Discussion) with Part-specific expectations
- **Menu-driven practice mode**: Fixed entry phrases, numbered menu options, and standardized output templates
- **42 difficulty-tagged cue cards**: Part 2 practice with [Easy]/[Medium]/[Hard] cards across 7 topic categories

## Installation

```bash
openclaw skills install ielts-speaking-coach
```

## Quick Start

### Assess a response (text)

> Score my IELTS Part 1 answer: "I'm studying computer science at university. It's quite challenging but I find it rewarding because I enjoy problem-solving."

The skill returns a full assessment: scores, grammar corrections, vocabulary upgrades, model answer, and ZPD learning recommendations.

### Assess with audio

Send a voice message and the skill will:
1. Convert audio via ffmpeg
2. Transcribe using ASR
3. Score pronunciation based on ASR confidence
4. Provide full four-criterion feedback with real PR scores

### Practice session

> Let's do IELTS speaking practice, Part 2

The skill gives you a difficulty-appropriate cue card, listens to your response, and provides detailed feedback.

### Mock exam

> 模拟考试

Full 11-14 minute IELTS simulation: Part 1 (4-5 min) → Part 2 (3-4 min) → Part 3 (4-5 min), followed by a comprehensive score report.

### Learning path

> 学习路线

Get a personalized ZPD-based vocabulary and grammar study plan based on your current band level.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `target_band` | number | 7.0 | Your target IELTS band (model answers aim at this level) |
| `default_part` | number | 1 | Default IELTS Speaking part (1, 2, or 3) |
| `user_id` | string | "default" | Learner ID for trajectory tracking |

```bash
openclaw skills config ielts-speaking-coach target_band 7.5
openclaw skills config ielts-speaking-coach default_part 2
```

## Fixed Entry Mode

Use one of these phrases to enter the guided practice flow:

- `进入雅思口语模式`
- `启动雅思口语教练`
- `Use IELTS speaking coach`

The skill then shows a fixed menu:

1. `Part 1 练习`
2. `Part 2 练习`
3. `Part 3 练习`
4. `口语评分`
5. `语法纠错`
6. `学习路线`
7. `模拟考试`

You can reply with a number or paste a transcript directly.

## How Scoring Works

The skill evaluates four criteria independently using official IELTS Band Descriptors:

1. **Fluency & Coherence**: Speech rate (WPM), filler density, discourse markers, coherence
2. **Lexical Resource**: Vocabulary sophistication, semantic variety, idiomatic usage, collocations
3. **Grammatical Range & Accuracy**: Complex structures per 18 words, error density
4. **Pronunciation**: ASR confidence-based scoring for audio input; median estimation for text-only

Scores are calibrated using the CHAI framework (hybrid human-prior calibration) with Part-specific adjustments, then averaged and rounded to the nearest 0.5 band.

## Permissions

| Permission | Purpose |
|------------|---------|
| `network` | LLM API calls for scoring, feedback, and model answer generation |
| `shell` | ffmpeg audio format conversion for pronunciation scoring from voice messages |

## Bundled Resources

- `scoring-rubric.md` — Official IELTS Band descriptors
- `cue-cards-2025-may-aug.md` — 15 official cue cards (2025 May–August bank)
- `cue-cards.md` — 42 difficulty-tagged cue cards across 7 categories
- `learning-path.md` — ZPD vocabulary/grammar progression reference
- `pronunciation-guide.md` — Chinese speaker pronunciation diagnostics and exercises
- `vocab-map.json` — Topic-aware vocabulary upgrade hints
- `examples.md` — Sample interactions

## Self-hosted Backend (Optional)

The GitHub repository includes an optional `backend/` directory with a FastAPI server that provides enhanced features:

- DL model-based precise scoring
- Persistent learning state tracking across sessions
- Vocabulary ontology-driven trajectory planning

The backend is **not required** for the skill to work. All core features (scoring, practice, mock exam, learning paths) run entirely via the built-in LLM and bundled reference files. See the [GitHub repository](https://github.com/kevin0818-lxd/ielts-speaking-coach) for backend setup instructions.

## License

MIT
