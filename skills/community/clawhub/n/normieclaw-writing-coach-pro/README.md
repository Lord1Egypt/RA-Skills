# Writing Coach Pro

An agent-native writing coach for OpenClaw. Checks grammar, enforces your style, scores readability, and gets smarter every time you use it.

## What It Does

- **Grammar & Mechanics**: Catches errors, suggests fixes
- **Style Enforcement**: AP, Chicago, APA, or your own custom rules
- **Readability Scoring**: Flesch-Kincaid grade level, reading ease, passive voice %, adverb density
- **Document Consistency**: Flags terminology shifts, capitalization drift, tense changes across long documents
- **Smart Rewrites**: Produces improved versions that sound like you, not a robot
- **Persistent Style Memory**: Learns your preferences over time — the only writing tool that does this
- **Coach Mode**: Teaches you *why* something should change, not just *what*

## Why This Over Grammarly/ProWritingAid

| | Writing Coach Pro | Grammarly Pro | ProWritingAid |
|---|---|---|---|
| **Price** | $9.99 one-time | $144/year | $120/year |
| **Learns your style** | Yes, automatically | No | No |
| **Agent-native** | Yes, works in chat | No, browser extension | No, browser extension |
| **Document consistency** | Full cross-document | Basic | Basic |
| **Teaching mode** | Yes (Coach Mode) | No | No |

## Install

1. Drop `writing-coach-pro/` into `~/.openclaw/skills/`
2. Run `bash ~/.openclaw/skills/writing-coach-pro/scripts/setup.sh`
3. Say "review this" to your agent with any text

Full setup instructions: [SETUP-PROMPT.md](SETUP-PROMPT.md)

## Compatibility

- **OpenClaw**: v1.0+
- **Models**: Works with any LLM backend (Claude, GPT-4, Gemini, local models)
- **Platforms**: macOS, Linux, Windows (WSL)
- **Channels**: Telegram, Discord, Slack, CLI — anywhere your agent runs

## What's Included

```
writing-coach-pro/
├── SKILL.md              # The agent skill (core logic)
├── SETUP-PROMPT.md       # Setup guide
├── README.md             # This file
├── SECURITY.md           # Security information
├── config/settings.json  # Default style profile
├── scripts/              # Setup, export, and style-check scripts
├── examples/             # Before/after examples
└── dashboard-kit/        # Dashboard integration (optional)
```

## License

Included with NormieClaw Pro ($9.99) or The Full Stack (free). See [normieclaw.ai](https://normieclaw.ai) for terms.
