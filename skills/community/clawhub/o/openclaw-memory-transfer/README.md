# openclaw-memory-transfer

> **Zero-friction memory migration for OpenClaw.** Bring your memories from ChatGPT, Claude, Gemini, Copilot, and more — in under 10 minutes.

[![Powered by MyClaw.ai](https://img.shields.io/badge/Powered%20by-MyClaw.ai-blue)](https://myclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[中文](README.zh-CN.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Italiano](README.it.md) | [Español](README.es.md)

---

You spent months (or years) with ChatGPT. It knows your writing style, your projects, your preferences, your quirks. When you switch to OpenClaw, none of that should start from zero.

**Memory Transfer** extracts everything your old AI knows about you, cleans it up, and imports it into OpenClaw's memory system. Just tell your agent where you came from.

## How It Works

Tell your OpenClaw agent:

```
I'm coming from ChatGPT
```

or:

```
Migrate my data from Gemini
```

Your agent handles the rest — step by step, in plain language.

## Supported Sources

| Source | Method | What You Do |
|--------|--------|-------------|
| **ChatGPT** | ZIP data export | Click export in Settings, upload the ZIP |
| **ChatGPT** (alt) | Prompt-guided | Copy one prompt, paste the result back |
| **Claude.ai** | Prompt-guided | Copy one prompt, paste the result back |
| **Gemini** | Prompt-guided | Copy one prompt, paste the result back |
| **Copilot** | Prompt-guided | Copy one prompt, paste the result back |
| **Perplexity** | Prompt-guided | Copy one prompt, paste the result back |
| **Claude Code** | Auto-scan | Nothing — automatic |
| **Cursor** | Auto-scan | Nothing — automatic |
| **Windsurf** | Auto-scan | Nothing — automatic |

### ChatGPT ZIP Export (Recommended)

The most complete migration path. ChatGPT's data export includes your full conversation history — the parser extracts:

- 📝 Writing style patterns from your messages
- 🔧 Tools and platforms you mention frequently
- 📊 What you ask for most (code, analysis, writing, etc.)
- 🚫 Corrections and "don't do this" patterns
- 💬 Frequently discussed topics

### Prompt-Guided Export

For cloud AIs without structured export, your agent gives you **one prompt** to send to your old AI. It outputs everything it knows about you in a structured format. Copy it back — done.

### Local Agent Auto-Scan

If you used Claude Code, Cursor, or Windsurf, the skill automatically scans local config files — zero effort.

## What Gets Migrated

| Category | Destination | Examples |
|----------|------------|---------|
| Identity & profile | `USER.md` | Name, profession, language, timezone |
| Communication style | `USER.md` | Writing tone, formatting preferences |
| Knowledge & experience | `MEMORY.md` | Projects, domain expertise, insights |
| Behavioral patterns | `MEMORY.md` | Workflows, habits, corrections |
| Tool preferences | `TOOLS.md` | Tech stack, platforms, environments |

## What NEVER Gets Migrated

- 🔒 API keys, tokens, or passwords
- 🔒 Authentication credentials
- 🔒 Sensitive personal data (unless explicitly requested)

All imported data is shown to you for review before writing. Nothing is imported silently.

## Install

### OpenClaw (via ClawHub)

```bash
clawhub install openclaw-memory-transfer
```

### Manual

```bash
cp -r . ~/.openclaw/skills/openclaw-memory-transfer/
```

## How Migration Feels

```
You: I used to use ChatGPT, want to bring my stuff over

Agent: The easiest way — export your ChatGPT data:
       1. Settings → Data Controls → Export Data
       2. Click "Export" — you'll get an email
       3. Download the ZIP and send it to me

You: [uploads zip]

Agent: Done! Found 847 conversations. Here's what I extracted:

       📋 Migration Preview
       USER.md: Leo, entrepreneur, bilingual EN/ZH...
       MEMORY.md: MyClaw project, growth strategy...
       TOOLS.md: Node.js, React, Netlify...

       Anything to change?

You: Looks good, write it

Agent: ✅ Migration complete! I know who you are now.
```

## Architecture

```
openclaw-memory-transfer/
├── SKILL.md                           # Agent skill definition
├── scripts/
│   └── parse-chatgpt-export.js        # ChatGPT ZIP parser (Node.js, zero deps)
├── package.json                       # Package metadata
├── README.md                          # This file (+ 7 language variants)
└── LICENSE                            # MIT
```

## Contributing

Issues and PRs welcome. If you want to add support for a new AI platform:

1. Add the export method to `SKILL.md` (prompt template or file scan paths)
2. If structured export exists, add a parser in `scripts/`
3. Update the supported sources table

## License

MIT — do whatever you want with it.

---

**Powered by [MyClaw.ai](https://myclaw.ai)** — the AI personal assistant platform that gives every user a full server with complete code control.
