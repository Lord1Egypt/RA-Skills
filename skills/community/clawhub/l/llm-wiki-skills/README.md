# 🧠 LLM Wiki Skills

> **Supercharge your AI agent with persistent knowledge management**

[English](./README.md) | [中文](./README.zh.md) 

---

## Why This Skill Set?

| Feature | Traditional RAG | **LLM Wiki Skills** |
|---------|-----------------|---------------------|
| Knowledge Persistence | ❌ Retrieve each time | ✅ Accumulates over time |
| Cross-Reference | ❌ No connections | ✅ Auto-linked relationships |
| Contradiction Detection | ❌ None | ✅ Automatic flagging |
| Multi-Format Output | ❌ Text only | ✅ Markdown, Tables, Slides |
| Query Synthesis | ❌ Simple retrieval | ✅ Reasoning + citations |

> **These skills transform your AI from a stateless query tool into a persistent learning companion.**

---

## ✨ Core Features

### 1. **wiki-init** — One-command wiki setup
- Creates complete wiki architecture
- Generates CLAUDE.md schema for AI context
- Sets up index.md and log.md

### 2. **wiki-ingest** — Intelligent source processing
- Reads articles, papers, books
- Extracts key takeaways, entities, concepts
- Auto-updates cross-references
- Flags contradictions

### 3. **wiki-query** — Context-aware Q&A
- Searches index first, then deep-dives
- Synthesizes answers with wiki citations
- Supports multiple output formats
- Files valuable answers back to wiki

### 4. **wiki-lint** — Automatic quality control
- Detects contradictory claims
- Finds orphan pages
- Identifies missing links
- Suggests data gaps

### 5. **wiki-maintain** — Schema evolution
- Updates conventions
- Refines workflows
- Adds new page types

---

## 🔗 Combo: Obsidian + Web Clipper + CLI

### Workflow

```
🌐 Web → Obsidian Web Clipper → 📝 Obsidian/raw
                                        ↓
      🧠Claude code/Open code → 🔧 LLM Wiki Skills
                                        ↓
                                   🔧Obsidian CLI
                                        ↓
                                     📚 Knowledge Base
```

### 1. Install Obsidian, enable CLI, install Web Clipper, install this project's skills
- Obsidian cloud sync guide:
  https://www.bilibili.com/video/BV1fZCyBYEuT/?spm_id_from=333.788.top_right_bar_window_history.content.click&vd_source=2c231d5b43d9ccf0848317adb47c0383
  
### 2. Capture with Obsidian Web Clipper
- Save articles, research papers, web content directly to Obsidian
- Use templates for consistent structure

### 3. Use Claude Code or Open Code to call skills
```markdown
User: Process the new article I saved in Obsidian

AI: (uses wiki-ingest to extract and integrate)
```

### Integration Pattern

| Tool | Role |
|------|------|
| **Obsidian** | UI + Storage |
| **Web Clipper** | Content capture |
| **Obsidian CLI** | Programmatic access |
| **LLM Wiki Skills** | AI-powered processing |

## 📁 Project Structure

```
LLM-wiki-skills/
├── SKILL.md                    # Master skill file
├── README.md                   # English version
├── README.zh.md                # 中文版
├── wiki/                       # Example wiki content
│   ├── entities/               # Entity pages
│   ├── concepts/               # Concept pages
│   ├── sources/               # Source summaries
│   ├── index.md               # Content catalog
│   └── log.md                 # Operation log
└── skills/                     # Individual skills
    ├── wiki-init/
    ├── wiki-ingest/
    ├── wiki-query/
    ├── wiki-lint/
    └── wiki-maintain/
```

---

## 🎯 Use Cases

- 📚 **Research Assistant** — Process papers, extract insights
- 📖 **Reading Notes** — Capture and synthesize books
- 💼 **Team Knowledge** — Shared documentation
- 🧠 **Second Brain** — Personal knowledge management
- 🔬 **Technical Docs** — API and codebase knowledge
