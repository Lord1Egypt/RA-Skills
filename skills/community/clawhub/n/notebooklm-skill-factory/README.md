# NotebookLM Skill Factory

> Turn domain knowledge into Claude Code skills — NotebookLM research → structured SKILL.md generation → automated validation pipeline.

[中文文档](README.zh-CN.md)

## What It Does

Manually writing SKILL.md files is slow: research takes hours, hallucinations creep in, and iteration is painful. This skill orchestrates a 4-phase pipeline that combines NotebookLM's source-grounded research with Claude Code's execution:

```
User Intent → NotebookLM Source Ingestion → SKILL.md Extraction → Validation → Test & Iterate
```

## Why This Works

- **No hallucinations** — NotebookLM answers only from sources you provide, never invents
- **Minutes, not hours** — What used to take a full afternoon now takes a few minutes
- **Structured output** — Extracts production-ready SKILL.md with proper YAML frontmatter
- **Built-in iteration** — Test failures feed back into NotebookLM for automatic fixes

## Quick Start

### Prerequisites

```bash
# One-time setup
notebooklm login        # Google OAuth (opens browser once)
```

### Usage

```
/create a skill for high-conversion landing page copywriting
```

The skill will:
1. Ask you for source materials (PDFs, URLs, YouTube)
2. Create a dedicated NotebookLM notebook and index them
3. Extract a complete, validated SKILL.md
4. Test it and iterate if needed

## Manual Installation

```bash
# Copy to skills directory
cp -r notebooklm-skill-factory ~/.claude/skills/
```

Or install via ClawHub:

```bash
clawhub install notebooklm-skill-factory
```

## File Structure

```
├── SKILL.md                              # Main skill definition
├── scripts/
│   └── parse-skill-output.py             # Parse NotebookLM JSON → SKILL.md
└── references/
    └── skill-extraction-prompt.md         # Prompt templates for extraction
```

## Dependencies

- [NotebookLM CLI](https://github.com/UseClawPro/notebooklm) — `notebooklm` command
- Python 3.10+ (stdlib only, no pip packages)
- Claude Code with `skill-creator` and `skill-vetter` skills

## License

MIT — see [LICENSE](LICENSE)
