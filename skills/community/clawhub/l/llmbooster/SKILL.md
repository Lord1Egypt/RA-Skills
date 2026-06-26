---
name: llmbooster
description: 'A 4-step thinking framework to boost LLM output quality. Enforces structured reasoning (Plan → Draft → Self-Critique → Refine) to improve low-end LLM responses. No LLM endpoint needed - LLM follows the framework itself. Triggered by "detailed analysis", "in-depth analysis", "use booster", or /booster command.'
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      bins: []
---

# LLMBooster Skill

**A Thinking Framework, Not an Automation Tool**

LLMBooster is a 4-step thinking framework that improves LLM output quality through structured reasoning. **No LLM endpoint needed** - the LLM follows the framework itself.

## Core Philosophy

**Problem with low-end LLMs:** Jump to conclusions, miss details, lack self-review.

**Booster solution:** Enforce structured thinking process.

```
Plan → Draft → Self-Critique → Refine
```

## Trigger Conditions

- User says "use booster", "booster", or "/booster"
- User requests: "detailed analysis", "in-depth analysis", "help me analyze"
- User requests: "improve quality", "detailed analysis"
- User asks for evaluation, comparison, or decision support
- User requests code review or technical documentation
- User asks complex questions (lengthy tasks, multi-step problems)

## How It Works

**LLM executes the framework itself, no Python calls needed:**

1. LLM reads `prompts/plan.md` → Create structured plan
2. LLM reads `prompts/draft.md` → Write complete draft
3. LLM reads `prompts/self_critique.md` → Review issues
4. LLM reads `prompts/refine.md` → Polish final output

## Command Handling

When user enters `/booster` command, execute:

```bash
cd ~/.openclaw/workspace/skills/llmbooster && python3 -c "
from config_loader import ConfigLoader
from state_manager import SkillStateManager
from cli_handler import CLICommandHandler

loader = ConfigLoader()
config = loader.load('config.schema.json')
state_mgr = SkillStateManager(config)
cli = CLICommandHandler(state_mgr)
result = cli.handle('/booster status')
print(result.message)
"
```

### CLI Commands

| Command | Description |
|---------|-------------|
| `/booster enable` | Enable LLMBooster |
| `/booster disable` | Disable LLMBooster |
| `/booster status` | Show current status |
| `/booster stats` | Show usage statistics |
| `/booster depth <1-4>` | Set thinking depth |
| `/booster help` | Show help |

## Thinking Depth

| Depth | Steps | Quality | Speed | Use Case |
|-------|-------|---------|-------|----------|
| 1 | Plan | ★★☆☆ | Fastest | Quick analysis, brainstorm |
| 2 | Plan → Draft | ★★★☆ | Fast | General tasks, simple Q&A |
| 3 | + Self-Critique | ★★★★ | Medium | Code review, technical docs |
| 4 | Full pipeline | ★★★★★ | Slowest | Important docs, complex analysis |

## Visual Feedback

When executing, Booster displays:

```
🚀 **Booster Pipeline Started**: Analyzing task...
────────────────────────────────────────
🚀 Booster [█░░░░] Step 1/4: **Plan**
✅ Plan completed (2.3s)

🚀 Booster [██░░░] Step 2/4: **Draft**
✅ Draft completed (5.1s)

🚀 Booster [███░░] Step 3/4: **Self-Critique**
✅ Self-Critique completed (1.8s)

🚀 Booster [████] Step 4/4: **Refine**
✅ Refine completed (3.2s)
────────────────────────────────────────
✅ **Booster Complete** - 4 steps, 12.4s total
```

## Prompt Templates

All templates are in `prompts/` directory:

- `plan.md` - Step 1: Create structured plan
- `draft.md` - Step 2: Write complete draft
- `self_critique.md` - Step 3: Review and list improvements
- `refine.md` - Step 4: Apply improvements

## Why It Works

| Low-End LLM Problem | Booster Solution |
|---------------------|-------------------|
| Jumps to conclusions | Plan step forces structured thinking |
| Misses details | Draft step requires complete coverage |
| No self-review | Self-Critique step finds issues |
| Rough output | Refine step polishes final result |

## Usage Statistics

```bash
/booster stats
# 📊 **Booster Statistics**
# ───────────────────────
# Status: enabled
# Thinking Depth: 4
# Tasks Processed: 5
# Last Used: 2026-03-22T09:30:00
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill definition + trigger conditions |
| `README.md` | Documentation |
| `booster.py` | Core module + helpers |
| `cli_handler.py` | CLI command processing |
| `state_manager.py` | State + statistics |
| `stream_handler.py` | Visual feedback |
| `config_loader.py` | Config loading |
| `prompts/*.md` | Step prompt templates |