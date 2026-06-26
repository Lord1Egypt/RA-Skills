# Prompt Compressor for OpenClaw

**Saves 20-40% of LLM tokens** by teaching the agent to write compressed output from the start.

## The Problem

Every OpenClaw turn sends the full conversation history to the LLM. Verbose responses → verbose history → expensive turns. This compounds fast — a 20-message session with uncompressed responses can hit 60K+ tokens.

## The Solution

Add instructions to your SOUL.md that make the agent write compressed from the start:

- Compressed responses → compressed history → compressed compaction summaries
- Savings compound on every subsequent turn
- No hooks, no proxy, no extra process, no dependencies

## Install

```bash
# Append to your SOUL.md (don't overwrite!)
cat soul-snippet.md >> ~/.openclaw/SOUL.md

# Start a new session so it loads
# In your chat: /new
```

That's it. Two commands.

## What changes

### Before (default agent)
```
User: hey can you help me figure out how to deploy my app?

Agent: Of course! I'd be happy to help you with deploying your application.
There are several approaches we could take here, and I think it would be a
good idea to consider a few factors first. Let me walk you through the
main options that are available to you...
```

### After (with prompt-compressor SOUL.md)
```
User: hey can you help me figure out how to deploy my app?

Agent: Main deployment options:
- Docker + cloud (AWS ECS, GCP Cloud Run, Azure Container Apps)
- PaaS (Railway, Render, Fly.io) — simplest
- VPS (manual setup, most control)

What's your stack and budget?
```

Same information. ~60% fewer tokens. Multiplied across every turn in the session.

## What gets compressed

| Area | Before | After |
|------|--------|-------|
| Responses | "I'd be happy to help! Let me explain..." | Direct answer, no preamble |
| MEMORY.md | "The user mentioned they prefer FastAPI..." | "User prefers FastAPI+JWT for auth" |
| Daily logs | "We had a discussion about deployment..." | "- deploy: Docker+ECS, staging first" |
| Compaction | Full narrative paragraphs | Compressed fact lists |

## What is NEVER compressed

- Code (exact syntax matters)
- URLs, file paths, config values
- Error messages
- Names, versions, specific numbers

## Files

```
prompt-compressor-openclaw/
├── SKILL.md          # OpenClaw skill metadata + agent instructions
├── soul-snippet.md   # ← Append this to your SOUL.md
├── handler.js        # Future: message:received hook (for newer OpenClaw versions)
└── README.md
```

## Future: Hook-based compression

`handler.js` contains a `message:received` hook that compresses user messages *before* the LLM sees them (saving tokens on turn 1 too). This requires OpenClaw versions with custom hook support. When your version supports it:

```bash
mkdir -p ~/.openclaw/hooks/prompt-compressor
cp handler.js SKILL.md ~/.openclaw/hooks/prompt-compressor/
openclaw hooks enable prompt-compressor
```

## How it was built

1. 154 compression rules optimized through 300+ evolutionary variants
2. Scored 96.3% on a 24-test benchmark
3. Architecture research (217 variants) evaluated hooks, proxies, plugins, and SOUL.md approaches
4. SOUL.md won for Clawdbot v2026.1.x: zero deps, zero config, two-command install

## License

MIT
