# openclaw-sonar

Local OpenRouter Sonar CLI and OpenClaw skill.

This repo provides a lightweight local `sonar` command for OpenRouter Sonar web search, plus the accompanying OpenClaw skill docs.

## Features

- `sonar "query"` for default search using `sonar`
- `sonar "query" --model sonar-pro`
- `sonar models`
- `sonar pro "query"`
- `sonar pro-search "query"`
- `sonar deep "query"`
- `sonar reason "query"`
- `sonar reason-pro "query"`
- `sonar research "query"`
- `sonar extract "https://example.com"`

## Models

Short model names are normalized to OpenRouter model ids:

- `sonar` → `perplexity/sonar`
- `sonar-pro` → `perplexity/sonar-pro`
- `sonar-pro-search` → `perplexity/sonar-pro-search`
- `sonar-reasoning` → `perplexity/sonar-reasoning`
- `sonar-reasoning-pro` → `perplexity/sonar-reasoning-pro`
- `sonar-deep-research` → `perplexity/sonar-deep-research`

## Install

### Requirements

- [Bun](https://bun.sh)
- `OPENROUTER_API_KEY`

### Quick install

```bash
git clone https://github.com/iamjameskeane/openclaw-sonar.git
cd openclaw-sonar
chmod +x scripts/openrouter-sonar.ts
mkdir -p ~/.local/bin
ln -sf "$PWD/scripts/openrouter-sonar.ts" ~/.local/bin/sonar
```

Ensure `~/.local/bin` is on your `PATH`.

## Usage

```bash
sonar "latest OpenRouter Sonar features"
sonar "best cited search workflow for AI agents" --model sonar-pro
sonar models
sonar deep "compare Tavily, Exa, and Sonar for agent research"
sonar extract "https://openrouter.ai/docs/api/reference/overview"
```

## Environment variables

- `OPENROUTER_API_KEY` required
- `OPENROUTER_SONAR_MODEL` optional default, prefers short names like `sonar`
- `OPENROUTER_REFERER` optional
- `OPENROUTER_TITLE` optional

## Repo layout

- `scripts/openrouter-sonar.ts` - Bun CLI
- `SKILL.md` - OpenClaw skill definition
