# LLMBooster

**AThinking Framework to Improve Low-End LLM Response Quality**

LLMBooster is a 4-step thinking framework that enhances LLM output quality through structured reasoning. **No LLM endpoint needed** - the LLM follows the framework itself.

## Core Philosophy

**Problem:** Low-end LLMs tend to jump to conclusions, miss details, and lack self-review.

**Solution:** Enforce a structured thinking process:

```
Plan → Draft → Self-Critique → Refine
```

**Benefits:**
- ✅ Forces planning, prevents jumping ahead
- ✅ Ensures complete coverage in draft
- ✅ Self-critique catches blind spots
- ✅ Refines output for quality

## Installation

```bash
openclaw skills install llmbooster
```

## Usage

### Method 1: Natural Language Triggers

``"詳細分析..." (detailed analysis)
- "深入分析..." (in-depth analysis)
- "幫我分析..." (help me analyze)
- "improve quality..."
- "detailed analysis..."
```

### Method 2: CLI Commands

```bash
/booster enable        # Enable LLMBooster
/booster disable       # Disable LLMBooster
/booster status        # Show current status
/booster stats         # Show usage statistics
/booster depth <N>     # Set thinking depth (1-4)
/booster help          # Show all commands
```

### Method 3: Manual Execution

The LLM can follow the framework by reading prompt templates:

```
1. Read prompts/plan.md → Create structured plan
2. Read prompts/draft.md → Write complete draft
3. Read prompts/self_critique.md → Review issues
4. Read prompts/refine.md → Polish final output
```

## Thinking Depth

| Depth | Steps | Quality | Speed | Use Case |
|-------|-------|---------|-------|----------|
| 1 | Plan | ★★☆☆ | Fastest | Quick analysis, brainstorm |
| 2 | Plan → Draft | ★★★☆ | Fast | General tasks, simple Q&A |
| 3 | + Self-Critique | ★★★★ | Medium | Code review, technical docs |
| 4 | Full pipeline | ★★★★★ | Slowest | Important docs, complex analysis |

## Visual Feedback

During execution, Booster displays:

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

## Configuration

```json
{
  "enabled": true,
  "thinkingDepth": 4,
  "maxRetries": 3
}
```

## File Structure

```
~/.openclaw/skills/llmbooster/
├── SKILL.md                # Skill definition + triggers
├── README.md               # This file
├── cli_handler.py          # CLI command processing
├── state_manager.py        # State + statistics persistence
├── stream_handler.py       # Visual feedback output
├── config_loader.py        # Config loading
├── models.py               # Data models
├── booster_stats.json      # Usage statistics
└── prompts/
    ├── plan.md             # Step 1: Planning template
    ├── draft.md            # Step 2: Drafting template
    ├── self_critique.md    # Step 3: Review template
    └── refine.md           # Step 4: Refinement template
```

## Why It Works

### Low-End LLM Problems

| Problem | Manifestation |
|---------|---------------|
| Jumps to conclusions | Lacks reasoning process |
| Misses details | Omits important information |
| No self-review | Doesn't catch errors |
| Rough output | Poor structure |

### Booster Solutions

| Step | Solution |
|------|----------|
| Plan | Forces structured thinking |
| Draft | Ensures complete coverage |
| Self-Critique | Finds issues proactively |
| Refine | Polishes final output |

## Statistics

```bash
/booster stats
# 📊 **Booster Statistics**
# ───────────────────────
# Status: enabled
# Thinking Depth: 4
# Tasks Processed: 5
# Last Used: 2026-03-22T09:30:00
```

## Version History

| Version | Changes |
|---------|---------|
| v1.5.0 | Repositioned as thinking framework (no LLM endpoint needed) |
| v1.4.0 | Added `/booster stats` command |
| v1.3.0 | Persistent statistics |
| v1.2.0 | Visual feedback + progress bar |
| v1.1.0 | Chinese trigger words |
| v1.0.0 | Initial release |