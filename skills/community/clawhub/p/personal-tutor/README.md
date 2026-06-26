# Knowledge Digest 🧠

> Turn every learning session into structured, searchable, long-term knowledge.
> 把每一次学习对话变成结构化的永久知识。

---

## What Is This?

Knowledge Digest is a **full-cycle learning management system** for AI agents. You do the learning in chat — the agent handles everything else:

- 📋 Auto-creates syllabi and daily learning logs
- 📝 Runs quizzes and tracks mastery
- 🧠 Extracts concepts into your knowledge base (Obsidian / plain Markdown)
- 🔗 Builds bidirectional links between related ideas
- ✅ Keeps config, memory, and indexes in sync

Three simple commands drive the whole thing:

```
"Open a new subject: Philosophy"
"Start learning Philosophy"
"Update learning records"
```

---

## Features

| Feature | What It Does |
|:--------|:-------------|
| **One-command subject setup** | Creates syllabus + learning log + config in one go |
| **Smart category detection** | Auto-detects existing folder structure (e.g., `Academic/`, `Professional/`) |
| **Incremental daily lessons** | Reviews previous session → teaches new content → quizzes → prompts to archive |
| **Dual-depth archiving** | Light (log + syllabus + memory) or Full (+ concept extraction + index refresh) |
| **Multi-tool knowledge base** | Works with Obsidian (wikilinks), plain Markdown, or no KB at all |
| **De-duplication** | Checks for existing concepts before creating, prevents duplicate notes |
| **Bidirectional linking** | New concepts automatically link to related ones, with backlinks |
| **Custom schema support** | Point to your own rules file (e.g., `WIKI-SCHEMA.md`) for full control |
| **Bilingual output** | Configurable: English, Chinese, bilingual, or auto-detect |

---

## Quick Start

### 1. Install

Install from ClawHub:

```bash
clawhub install knowledge-digest
```

### 2. First Run

Just say **"start learning [any subject]"**. The agent will detect it's your first time and walk you through a 6-question setup:

1. Where to store learning files
2. What knowledge base tool you use (Obsidian / plain / none)
3. Where your knowledge base is located
4. Archive depth (light or full)
5. Output language
6. Custom schema file (optional)

That's it. Your config is saved and you never answer these again.

### 3. Start Learning

```
"Open a new subject: Machine Learning"
"Start learning Machine Learning"
"Update learning records"
```

---

## The Three Scenarios

### 🆕 Starting a New Subject

```
You: "Open a new subject: Cognitive Psychology"
Agent: [scans folder structure, asks which category]
You: "Academic"
Agent: ✅ Created syllabus, learning log, config. You're set for Day 1.
```

**What's created:**
- `{learning root}/{category}/{subject}/syllabus.md` — phased learning plan
- `{learning root}/{category}/{subject}/learning-log.md` — daily tracking table
- Config entry with progress, paths, and status

### 📚 Daily Lesson

```
You: "Continue Cognitive Psychology"
Agent: [reads config → reads syllabus → reviews last lesson → teaches Day 3]
```

**Every session includes:**
- Brief review of the previous lesson
- New content with concrete examples
- Interactive quiz (2-5 questions)
- End prompt reminding you to archive

### 📦 Post-Lesson Archive

```
You: "Update learning records"
Agent: [updates 6 layers]
```

| Layer | What Happens |
|:------|:-------------|
| Learning log | Appends today's content, mastery, quiz results, issues |
| Syllabus | Marks current day as ✅ complete |
| Config | Advances to Day N+1 |
| Memory | Updates agent memory with progress |
| Knowledge base | Extracts concepts as individual `.md` files (full mode) |
| Index | Refreshes concept index and subject outline (full mode) |

---

## Configuration

All settings live in `{workspace}/.knowledge-digest-config.json`:

```json
{
  "version": "1.0",
  "learningRoot": "/path/to/learning/",
  "knowledgeBase": {
    "tool": "obsidian",
    "path": "/path/to/vault/",
    "schemaPath": "/path/to/WIKI-SCHEMA.md"
  },
  "archiveDepth": "full",
  "language": "zh-en",
  "subjects": {}
}
```

| Field | Options | Description |
|:------|:--------|:------------|
| `learningRoot` | Any path | Where subject folders are stored |
| `knowledgeBase.tool` | `obsidian` / `plain` / `notion` / `none` | Your note-taking tool |
| `knowledgeBase.path` | Any path | Root of your vault or notes folder |
| `knowledgeBase.schemaPath` | Any path (optional) | Custom rules file for concept formatting |
| `archiveDepth` | `light` / `full` | `light` = log+syllabus+memory, `full` = +concept extraction+index |
| `language` | `zh` / `en` / `zh-en` / `auto` | Output language for all generated content |

### Directory Structure

```
{learningRoot}/
├── Academic/                    ← category (auto-detected)
│   ├── Philosophy/
│   │   ├── syllabus.md
│   │   └── learning-log.md
│   └── Machine Learning/
│       ├── syllabus.md
│       └── learning-log.md
├── Professional/
│   └── Public Speaking/
│       ├── syllabus.md
│       └── learning-log.md
```

---

## Knowledge Base Rules

When `archiveDepth` is `full`, the agent extracts concepts from each lesson and creates structured notes:

- **One concept = one file** with numbered prefix (`01-Derivative.md`)
- **YAML frontmatter** with aliases for searchability
- **Bidirectional wikilinks** (Obsidian) or relative links (plain Markdown)
- **De-duplication** before creation — checks filenames AND aliases
- **Index + outline updates** after every batch

If you have a custom schema (e.g., `WIKI-SCHEMA.md`), its rules take priority over built-in defaults.

---

## FAQ

**Q: I already have existing subjects. Can I migrate them?**
A: Yes. Just add them to the `subjects` object in the config with `currentDay`, paths, and `status`. The agent will pick up from wherever you are.

**Q: What if I study multiple subjects in one session?**
A: Each "update learning records" is processed independently. The agent reads the config to know which subject you're archiving.

**Q: Can I use this without a knowledge base?**
A: Absolutely. Set `knowledgeBase.tool` to `none` and concept extraction is skipped entirely.

**Q: Does it work with Notion?**
A: Concept files are written as standard Markdown, which Notion can import. Full API integration is not included in v1.0.

**Q: I forgot which day I'm on.**
A: Just say "continue [subject]" — the agent reads the config and tells you.

**Q: Can I skip days or reorder topics?**
A: Yes. Tell the agent to skip ahead, and it updates the config accordingly.

---

## Requirements

- An AI agent that supports ClawHub skills
- A workspace directory for the config file
- (Optional) Obsidian or any Markdown-based note system for knowledge base archiving

---

*Made for learners who want their chat sessions to outlive the chat window.*
