# Language Tutor Pro

A persistent, conversation-driven language tutor for OpenClaw agents. No gamification. No flashcard drills. Just real conversation practice with a tutor that remembers everything you struggle with.

## What It Does

- **Immersive conversation practice** at your level with adaptive difficulty
- **Contextual grammar correction** — errors fixed in the flow of conversation, not disconnected lessons
- **Spaced repetition** woven into natural conversation — vocabulary reviews that don't feel like flashcards
- **Persistent memory** — your tutor remembers weaknesses, vocabulary, and progress across every session
- **CEFR-aligned progress tracking** from A1 (beginner) to C2 (mastery)
- **Situation role-plays** — practice ordering food, job interviews, doctor visits, and more

## Supported Languages

Spanish · French · German · Italian · Portuguese · Japanese · Mandarin Chinese · Korean

## Install

1. Copy the `language-tutor-pro/` folder into `~/.openclaw/workspace/.agents/skills/`
2. Run `bash scripts/setup.sh` to initialize data directories
3. Edit `config/settings.json` with your native language, target language, and level
4. Say "Let's practice Spanish" (or your target language) to start

Full setup instructions: [SETUP-PROMPT.md](SETUP-PROMPT.md)

## Session Types

| Type | Trigger | Description |
|------|---------|-------------|
| Free Conversation | "Practice [language]" | Open topic conversation at your level |
| Guided Lesson | "Teach me [topic]" | Focused grammar or vocabulary lesson |
| Vocab Review | "Vocab review" | Spaced repetition session |
| Situation Practice | "Situation: [scenario]" | Role-play real-world scenarios |

## Compatibility

- **Requires:** OpenClaw agent runtime
- **Models:** Works with any LLM backend supported by OpenClaw (Claude, GPT, Gemini, etc.)
- **Platform:** macOS, Linux (anywhere OpenClaw runs)
- **Dashboard:** Optional integration via `dashboard-kit/` — see [DASHBOARD-SPEC.md](dashboard-kit/DASHBOARD-SPEC.md)

## What's Included

```
language-tutor-pro/
├── SKILL.md              # Agent skill definition
├── SETUP-PROMPT.md       # Setup walkthrough
├── README.md             # This file
├── SECURITY.md           # Security stance
├── config/settings.json  # Learner configuration
├── scripts/              # Setup, export, and review scripts
├── examples/             # Real session transcripts
└── dashboard-kit/        # Dashboard integration
```

## Pricing

**$9.99** standalone (Pro tier) · Included in **The Full Stack (free)**

Replaces: Duolingo Max ($168/yr) + Babbel ($96/yr) + italki sessions ($480+/yr)

One payment. Unlimited practice. A tutor that actually remembers you.

## License

Proprietary — NormieClaw (normieclaw.ai). All rights reserved.
