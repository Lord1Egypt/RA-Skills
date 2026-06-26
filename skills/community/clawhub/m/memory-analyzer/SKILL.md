---
name: memory-analyzer
version: 1.0.0
description: Analyzes conversation history, extracts user preferences and feedback, updates memory files automatically.
homepage: https://clawhub.com/skills/memory-analyzer
metadata: {"openclaw":{"emoji":"🧠","category":"system","keywords":["memory","analysis","learning","automation"],"model":"google/gemini-3-flash-preview"}}
---

# Memory Analyzer Skill

Analyzes conversation history and updates memory files automatically.

## Usage

**Default: Google Gemini 3 Flash Preview**

```
Run memory-analyzer skill with Google model
```

Or manually:

```
Run /home/ubuntu/.openclaw/workspace/skills/memory-analyzer/analyzer.py with google/gemini-3-flash-preview model
```

## What It Does

1. **Reads** conversation history from sessions/
2. **Extracts** user preferences, feedback patterns
3. **Updates** memory files:
   - MEMORY.md (long-term memory)
   - AGENTS.md (agent rules)
   - USER.md (user preferences)
   - IDENTITY.md (identity notes)
   - SOUL.md (personality updates)

## Trigger

When Tevfik says things like:
- "Sen bu konuda böyle yap"
- "Ben şöyle çalışmayı tercih ediyorum"
- "Bu formatı beğendim/beğenmedim"
- Any direct feedback or preference

## Output

Automatically updates relevant memory files with new insights.

## Default Model

**google/gemini-3-flash-preview** (Configured by Tevfik)
