<div align="center">

# Memorial.skill

> *"You're gone, but I still remember the way you held your teacup."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

**Turn WeChat messages and voice notes into a digital life you can talk to.**

<br>

Just give the AI your WeChat chat history with them (text and voice),<br>
it learns how they spoke, their personality, their stories —<br>
then you can keep talking to them,<br>
in text, or **in their own voice**.

[Demo](#demo) · [How to Use](#how-to-use) · [Installation](#installation) · [中文](README.md)

</div>

---

## Demo

### Text Conversation

```
You          ❯ Grandpa, I got promoted today

Grandpa      ❯ Mm, good. Does your mom know?
               Don't just celebrate — more responsibility now. Stay grounded.
               "Taking a loss is a blessing." Remember that.

               — This response is inferred from his personality, not his actual words.
```

### Voice

```
You          ❯ Say "taking a loss is a blessing" in grandpa's voice

Grandpa      ❯ 🔊 [10-second audio clip — in grandpa's actual voice timbre]
```

> The voice is trained from WeChat voice messages. The timbre is theirs.

---

## How to Use

**Simplest way: give AI your WeChat chat history. That's it.**

```
You          ❯ /create-memorial

AI           ❯ Who would you like to create a memorial for?

You          ❯ My grandfather. There are chat logs and voice messages in our family WeChat group.

AI           ❯ Got it. Extracting his data from WeChat...
               Found 350 voice messages and 3 text messages.
               Analyzing his speech patterns and personality...
               Training his voice model...

               ✓ Done. You can talk to him now.
```

---

## What It Does

```
WeChat chats + voice messages
        ↓
  AI analyzes their speech style, personality, stories, values
        ↓
  Generates persona (how they'd talk and react)
        ↓
  Trains voice model (their timbre)
        ↓
  You can talk to them (text + voice)
```

### Input

| Material | Value | Notes |
|----------|:---:|-------|
| **WeChat/QQ voice messages** | ★★★ | Most precious — personality analysis + voice training |
| **WeChat/QQ text chats** | ★★★ | Catchphrases, habits, how they show care |
| **Photos** | ★★ | Timeline, places they frequented |
| **Family interviews** | ★★ | Others' perspective of them |
| **Letters/diaries** | ★★ | Values, inner world |
| **Oral stories** | ★ | Anything you remember |

> Minimum: **just WeChat text chats** — paste them in and you get a memorial.
> Best results: voice messages + text → both text and voice conversation unlocked.

### Output

| Capability | Basic | Voice Enhanced |
|------------|:---:|:---:|
| Text conversation with them | ✓ | ✓ |
| Ask their opinion on things | ✓ | ✓ |
| Tell their stories | ✓ | ✓ |
| Generate eulogies | ✓ | ✓ |
| Family interview questions | ✓ | ✓ |
| **Hear their voice** | | ✓ |

> ⚠️ This is remembrance based on memory, not the actual person. Responses are AI-inferred "what they might say."

---

## If They're Still Here

Starting the archive now is even better.

A person telling their own story is ten times richer than reconstructing it afterward. The system includes guided interview questions to help them share stories they've never told.

Archives built while alive automatically become memorial archives after they pass — no rebuilding needed.

---

## Installation

Two tiers, pick what you need:

| | Basic (Text + Photos) | Voice Enhanced (+Voice Cloning) |
|---|---|---|
| Features | Memorial archive, chat analysis, photo timeline | Everything + hear their voice |
| Hardware | Any computer | NVIDIA GPU required |
| Setup time | 5 minutes | 30 minutes |

**Basic install (5 min):**

```bash
# Install to Claude Code skills directory
mkdir -p .claude/skills
git clone https://github.com/Terry-cyx/memorial-skill .claude/skills/create-memorial

# Install dependencies (optional deps failing won't break basic features)
pip install -r .claude/skills/create-memorial/requirements.txt
```

**Voice Enhanced** requires PyTorch CUDA, GPT-SoVITS, WeChat 3.9.x, etc. See **[INSTALL.md](INSTALL.md)** for details.

---

## Usage

In Claude Code, type:

```
/create-memorial
```

Answer three questions — name and relationship, basic background, personality impression — then choose your data sources.
All fields can be skipped. Even a brief oral description generates a working archive; you can always add more later.

Once created, use `/{slug}` to open the memorial and begin remembering.

### Commands

| Command | Description |
|---------|-------------|
| `/list-memorials` | List all memorial archives |
| `/{slug}` | Full archive (remembrance + persona) |
| `/{slug}-remembrance` | Remembrance mode (life story, timeline) |
| `/{slug}-persona` | Persona mode (how they would speak and act) |
| `/{slug}-interview` | Generate family interview questions |
| `/memorial-rollback {slug} {version}` | Roll back to a previous version |
| `/delete-memorial {slug}` | Delete |

---

## Examples

> Input: `Grandpa, born 1938, from Hunan, railway worker in Beijing, grew vegetables after retirement, quiet, always said "taking a loss is a blessing"`

**Scenario 1: Recalling a Story**

```
You          ❯ Tell me about grandpa when he was young

Memorial     ❯ He rarely talked about that period on his own.
               But grandma once told me — during the Cultural Revolution,
               he wrapped his books in oilpaper and buried them in the garden.
               When reform came, he dug them up one by one, still readable.
               He said one thing: "Books can't be burned. Knowledge can't be severed."
```

**Scenario 2: Asking What He'd Say**

```
You          ❯ If I told him I got into university, what would he say?

Memorial     ❯ He probably wouldn't say anything.
               He'd put two extra pieces of food on your plate, then go to the garden alone.
               Come back with red eyes. You'd ask what's wrong.
               He'd say: "Nothing. Wind got in my eyes."
               — This is a reflection based on his character, not a statement from him.
```

**Scenario 3: Writing an Eulogy**

```
You          ❯ Help me put together a eulogy for him

Memorial     ❯ Wang Jianguo. Born 1938 in Hunan. Passed 2023, age 85.
               He worked in Beijing for 65 years, tended his garden for 25.
               He never said "I love you," but he poured water for grandma every morning —
               not once in their 58 years together did he skip it.
               His phrase was "taking a loss is a blessing"...
```

**Scenario 4: Preparing a Family Interview**

```
You          ❯ I want to ask grandma about him. Give me some questions

Memorial     ❯ Interview questions for his spouse:
               1. How did you two meet?
               2. How did he show love — through words, or through actions?
               3. Did you have any shared rituals or routines?
               4. What's one thing he did that moved you most?...
```

---

## Features

### Generated Archive Structure

Each memorial has two parts working together:

| Part | Content |
|------|---------|
| **Part A — Remembrance Archive** | Life timeline, life roles, values and beliefs, daily habits, signature stories, relationship network, regrets and last words, legacy and impact |
| **Part B — Persona Archive** | 5+1 layer structure: Ethical rules → Identity anchor → Language style → Emotional patterns → Relationship behavior → **Era background layer** |

How it works: `Question received → Remembrance provides the material → Persona shapes how they'd respond → Output delivered in reflective voice`

### Era Background Layer (unique to memorial-skill)

For people born before 1985, historical events profoundly shaped how they thought and behaved. This layer maps birth decade to specific behavioral tendencies:

| Birth Era | Historical Context | Behavioral Influence |
|-----------|-------------------|---------------------|
| 1930–1945 | WWII, Civil War | Strong survival instinct, extreme frugality, political caution |
| 1945–1965 | Three-Year Famine, Cultural Revolution | Never wastes food, avoids political speech, collectivist values |
| 1965–1985 | Reform and Opening Up | Pragmatic, hardworking, values stability |

### Supported Tags

**Speech style**: Quiet · Talkative · Tough exterior, soft heart · Reserved · Likes to lecture · Dialect accent

**Expressing love**: Through actions · Through words · Silent care · Pride hidden behind strictness · Doting on grandchildren

**Values**: Principled · Self-sacrificing · Frugal · Warm-hearted · Expects nothing in return · Face-conscious · Stubborn

**Relationship style**: Head-of-household · Quiet supporter · Strict parent · Lenient grandparent

### Evolution

- **Append materials** → New chat logs, photos, or oral accounts → Auto-analyzed and merged into existing content, never overwritten
- **Conversation corrections** → "They wouldn't say that" → Written into Correction log, takes effect immediately
- **Version management** → Auto-backup before every update → Rollback to any of the last 10 versions

---

## Voice Cloning — Hear Their Voice Again

The memorial archive isn't just text. If you have WeChat/QQ voice messages from your loved one, the system can train a voice model — **type any text, and hear it spoken in their voice**.

### How Much Audio Do You Need

| Amount | Quality |
|--------|---------|
| < 30 seconds | Recognizable timbre (zero-shot mode) |
| 1-3 minutes | Good timbre match |
| 5-10 minutes | Highly similar, natural prosody |
| 10+ minutes | Excellent — almost indistinguishable for short phrases |

> A few dozen voice messages from a family WeChat group is usually enough.

### Dialect Support

**Supported.** Even if your loved one spoke a regional dialect, the voice model can still be trained.

The system trains on dialect audio to capture their unique voice characteristics (SoVITS learns acoustic features, not language). During synthesis, the output uses their voice timbre to speak Mandarin. The result: **sounds like them, but speaks Mandarin**.

> Future versions will support dialect output (synthesized speech in the original dialect). Stay tuned.

### Technical Approach

Built on [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS). Training and inference run **entirely on your local machine** — no data leaves your device.

```
WeChat/QQ voice messages → Preprocessing (format + denoising) → Train voice model → Type text → Their voice
```

Requires an NVIDIA GPU (RTX 3060 12GB+ recommended). Training takes ~20-30 minutes.

---

## Project Structure

This project follows the [AgentSkills](https://agentskills.io) open standard:

```
create-memorial/
├── SKILL.md                      # Skill entry point (standard frontmatter)
├── prompts/                      # Prompt templates
│   ├── intake.md                 #   3-question intake dialogue
│   ├── remembrance_analyzer.md   #   Life story extraction (8 dimensions)
│   ├── remembrance_builder.md    #   remembrance.md generation template
│   ├── persona_analyzer.md       #   Persona extraction (era layer, tag translation table)
│   ├── persona_builder.md        #   persona.md 5+1 layer template
│   ├── merger.md                 #   Append-only incremental merge logic
│   └── correction_handler.md    #   Correction handling
├── tools/                        # Python utilities
│   ├── wechat_parser.py          #   WeChat chat log parser
│   ├── qq_parser.py              #   QQ chat log parser (txt/mht)
│   ├── audio_transcriber.py      #   Audio transcription (Whisper)
│   ├── photo_analyzer.py         #   Photo EXIF timeline extractor
│   ├── interview_guide.py        #   Interview question generator (self + family modes)
│   ├── voice_preprocessor.py      #   Voice preprocessing (silk→WAV + denoising)
│   ├── voice_trainer.py           #   One-click voice model training (GPT-SoVITS)
│   ├── voice_synthesizer.py       #   Voice synthesis (text → loved one's voice)
│   ├── skill_writer.py           #   Archive file management
│   └── version_manager.py        #   Version backup and rollback
├── memorials/                    # Generated memorial archives (gitignored)
│   └── example_grandpa/          #   Complete example (fictional grandpa Wang Jianguo)
├── spec/                         # Design spec and test cases
├── docs/PRD.md
├── requirements.txt
└── LICENSE
```

---

## Two Ways to Build

| | Build while they're alive | Build after they've passed |
|---|---|---|
| **Data quality** | Highest — firsthand, in their own words | Depends on memory and preserved materials |
| **Accuracy** | Real-time corrections, self-verified | Can't be corrected; needs family cross-checking |
| **Emotional context** | Warm, proactive, feels like leaving a legacy | Tinged with longing, like assembling a puzzle |
| **Best time to start** | When parents or grandparents are getting older | Anytime, as long as materials and memories exist |
| **Subject involvement** | Core data source | N/A |

> If they're still here, now is the best time.

---

## Full Pipeline (CLI)

If you prefer command-line over conversation:

```bash
# ① Extract WeChat voice messages (WeChat 3.9.x must be running)
python tools/wechat_voice_extractor.py --group "family" --person "target name" --outdir ./voices_raw/

# ② Preprocess: silk → WAV + denoising
python tools/voice_preprocessor.py --dir ./voices_raw/ --outdir ./voices_processed/

# ③ Transcribe audio to text (for memorial text content)
python tools/audio_transcriber.py --dir ./voices_processed/ --speaker "name" --format chat --output transcripts.md

# ④ Create memorial directory
python tools/skill_writer.py --action create --name "display name" --slug my_memorial

# ⑤ One-click voice model training (auto-detects dialect)
python tools/voice_trainer.py --action full --slug my_memorial --audio-dir ./voices_processed/

# ⑥ Test voice synthesis
python tools/voice_synthesizer.py --slug my_memorial --text "words to speak in their voice"

# ⑦ Check status
python tools/voice_synthesizer.py --slug my_memorial --action check
```

---

## Running Tests

```bash
python tests/test_tools.py
```

Covers: file management, version rollback, WeChat/QQ parsing, audio preprocessing, interview generation, voice synthesis.

---

## Notes

- **Source quality determines archive depth**: chat logs + family interviews > personal description alone
- Priority materials: **everyday conversations** (best for language patterns) > **pivotal exchanges** > **one-sided descriptions**
- Family interviews are a unique and important source for memorial-skill — use `/{slug}-interview` to generate tailored questions
- Archives can be built up over time. Memories surface gradually; add them as they come
- This Skill is not a substitute for grief. If you find yourself struggling to move forward, please consider professional support

---

## Acknowledgements

The architecture of this project was deeply inspired by two excellent open-source projects:

- [**Colleague.skill**](https://github.com/titanwings/colleague-skill) — Distill a colleague into an AI Skill. Originated the dual-track architecture (Work Skill + Persona) and the 5-layer personality model.
- [**Ex-Partner.skill**](https://github.com/therealXiaomanChu/ex-skill) — Reconstruct an ex-partner as an AI Skill. Pioneered relationship memory extraction and emotional healing scenarios.

memorial-skill inherits their dual-track analysis framework, prompt-driven architecture, and incremental evolution mechanism, while adding the era-background layer, living-archive mode, and voice cloning capabilities. Thanks to both authors for their open-source spirit.

---

<div align="center">

*What they left behind isn't just photos and chat logs.*<br>
*It's a way of speaking. A habit. A phrase that always appeared at the right moment.*<br>
*This archive just gives those things somewhere that won't disappear.*

</div>
