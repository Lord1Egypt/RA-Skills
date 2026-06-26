# Grok Imagine Prompts Search Skill

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.com/skill/grok-imagine-prompts)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange)](https://github.com/YouMind-OpenLab/grok-imagine-prompts-search-skill)
[![Daily Updates](https://img.shields.io/badge/Updates-Daily-purple)]()

> Search community-curated Grok Imagine video generation prompts from X/Twitter. Continuously updated as creators share their work.
>
> 🎬 [Browse the Gallery →](https://youmind.com/grok-imagine-prompts)

## What Is This?

An **AI agent skill** that lets Claude, OpenClaw, Cursor, and other AI assistants search a live library of **Grok Imagine video generation prompts** curated from real X/Twitter creators.

**Grok Imagine** is xAI's AI video generation model. These prompts are specifically designed for Grok Imagine — not repurposed from other models.

## Why Use This Skill?

- ✅ **Real community prompts** — sourced from X/Twitter creators who actually used Grok Imagine
- ✅ **Always up to date** — live API, continuously growing as the community shares more
- ✅ **Includes source links** — trace every prompt back to its original creator on X
- ✅ **No setup required** — live search, no local cache or file downloads needed

## Installation

### OpenClaw (Recommended)

```bash
clawhub install grok-imagine-prompts
```

Or search inside OpenClaw chat:

> "Install the grok imagine prompts skill from clawhub"

### Claude Code / Cursor / Codex / Gemini CLI

```bash
npx skills i YouMind-OpenLab/grok-imagine-prompts-search-skill
```

### Manual

```bash
npx openskills install YouMind-OpenLab/grok-imagine-prompts-search-skill
```

## Usage

```bash
# Search prompts by keyword
node scripts/search.mjs --q "cinematic portrait" --limit 5

# Browse recent/featured prompts
node scripts/search.mjs --limit 10
```

Or just tell your AI assistant:

> "Find me Grok Imagine prompts for a slow-motion ocean wave"

## Related

- 🎬 [YouMind Grok Imagine Gallery](https://youmind.com/grok-imagine-prompts)
- 🍌 [nano-banana-pro-prompts](https://clawhub.com/skill/nano-banana-pro-prompts) — 10,000+ image generation prompts
- 🎬 [seedance-2-prompts](https://clawhub.com/skill/seedance-2-prompts) — Seedance 2.0 video prompts

## License

MIT © [YouMind](https://youmind.com)
