---
name: minimax-vision-skill
description: Analyze images using MiniMax CLI (mmx-cli) for vision tasks. Use when user wants image understanding via MiniMax instead of OpenRouter. Triggers on requests like "analyze this image with minimax", "use minimax vision", "minimax image understanding", "mmx vision", or when user explicitly requests MiniMax-native vision analysis via CLI.
---

# Minimax Vision Skill

Analyzes images using MiniMax's CLI tool (`mmx`) with vision understanding.

## Prerequisites

- `mmx-cli` installed: `npm install -g mmx-cli`
  - If permission error: `npm install -g mmx-cli --prefix ~/.local`
- Authenticated: `mmx auth login --api-key <key>`

## Image Analysis

### With local file

```bash
mmx vision --prompt "What is in this image?" ./photo.jpg
```

### With URL

```bash
mmx vision --prompt "Describe this image in detail" https://example.com/image.jpg
```

## API Key

If not authenticated, get your key from [platform.minimax.io](https://platform.minimax.io/user-center/basic-information/interface-key), then:

```bash
mmx auth login --api-key <your-key>
```

Check quota:

```bash
mmx quota show
```