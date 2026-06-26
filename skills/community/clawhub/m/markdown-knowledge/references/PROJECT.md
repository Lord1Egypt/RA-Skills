# Markdown Knowledge Base for OpenClaw

> **Version 1.1.0** | Turn your local Markdown files into a queryable intelligent knowledge base

---

## Table of Contents

1. [Project Introduction](#1-project-introduction)
2. [Features](#2-features)
3. [Quick Start](#3-quick-start)
4. [User Guide](#4-user-guide)
   - 4.4 Knowledge Organization
   - 4.5 Usage Scenarios
5. [Configuration](#5-configuration)
6. [Precautions](#6-precautions)
7. [Migration Guide](#7-migration-guide)
8. [File Structure](#8-file-structure)
9. [FAQ](#9-faq)
10. [Changelog](#10-changelog)
11. [Roadmap](#11-roadmap)

---

## 1. Project Introduction

### 1.1 Skill Name and Description

| Item | Description |
|------|-------------|
| **Skill Name** | `markdown-knowledge` |
| **Version** | v1.1.0 |
| **Description** | Integrates local Markdown knowledge base with OpenClaw, supporting semantic search and context injection |
| **Author** | aaronjager92 |
| **License** | MIT |

### 1.2 Core Features

```
+----------------------------------------------------------+
|                    Core Workflow                         |
+----------------------------------------------------------+
|  User Question                                           |
|       |                                                   |
|  AI matches trigger pattern                              |
|       |                                                   |
|  Knowledge base search                                    |
|       |                                                   |
|  Inject relevant snippets into context                    |
|       |                                                   |
|  AI answers based on knowledge                           |
+----------------------------------------------------------+
```

**Core Capabilities:**

- 🔍 **Semantic Search** — Understands query intent, not just keyword matching
- 💉 **Context Injection** — Automatically injects relevant knowledge into AI conversation context
- 📦 **Out-of-the-box** — Works immediately with default settings
- 🔄 **Real-time Sync** — Automatically tracks file changes without manual refresh

### 1.2.1 Why This Skill Exists — Our Philosophy

> **"In the AI era, we're all just frantically asking questions and getting answers that feed into training data. We wanted to leave something behind."**

This skill was born from a simple realization:

| Before | After |
|--------|-------|
| Ask → Get answer → Forgotten | Learn → Save → Grow |
| Knowledge scattered in AI providers' servers | Knowledge lives in YOUR files |
| Answers used to train next model | Your insights, YOUR knowledge base |
| One-time queries | Living knowledge that evolves |
| Expensive cloud RAG services | Lightweight local RAG anyone can run |

**What we built:**

- 🌱 **A Personal Knowledge Garden** — Not just Q&A, but a curated collection that grows with you
- 📚 **Micro RAG** — Minimal overhead, runs on Raspberry Pi, migrates easily between machines
- 🏠 **Your Data, Your Control** — No cloud dependency, no subscription, no vendor lock-in
- 🔄 **Living Documentation** — Your notes, your docs, your knowledge — always accessible to AI

**The Goal:**

> In the age of AI that consumes everything to train itself, this skill is a small act of rebellion. Your knowledge should belong to YOU, grow with YOU, and stay with YOU.

```
+------------------+     +------------------+     +------------------+
|     LEARN        | --> |     SAVE         | --> |     GROW         |
+------------------+     +------------------+     +------------------+
     |                      |                      |
     v                      v                      v
 Acquire new          Store in YOUR          AI answers using
 insights             knowledge base          YOUR context
```

### 1.3 Supported Scale

| Metric | Limit | Description |
|--------|-------|-------------|
| **Max Files** | ≤ 2000 MD files | Performance may degrade beyond this |
| **Recommended** | ≤ 500 MD files | Optimal for best experience |
| **Single File** | ≤ 1 MB | Suggest splitting if larger |
| **Supported Formats** | `.md` | Markdown only |

### 1.4 Design Goals

```
+----------------------------------------------------------+
|                    Design Principles                     |
+----------------------------------------------------------+
|                                                          |
|  ✅ Out-of-the-box                                       |
|     Works immediately after install, no complex setup    |
|                                                          |
|  ✅ Lightweight & Efficient                              |
|     Optimized for resource-constrained devices (Pi etc.) |
|                                                          |
|  ✅ Cross-platform                                       |
|     Supports Linux, macOS, Windows, Raspberry Pi          |
|                                                          |
|  ✅ Privacy-first                                        |
|     All data stored locally, nothing uploaded            |
|                                                          |
+----------------------------------------------------------+
```

---

## 2. Features

### 2.1 Automatic Features

These features are handled automatically by the system:

| Feature | Automatic Behavior | When |
|---------|-------------------|------|
| **Config Loading** | Automatically reads `config.json` | Every call |
| **Index Loading** | Automatically loads existing index file | On search |
| **Path Resolution** | Automatically expands `~` to home directory | On config parse |
| **Document Parsing** | Automatically parses Markdown metadata and content blocks | On index build |
| **Result Formatting** | Automatically generates readable search results | After search |
| **Incremental Update** | Automatically detects file changes and updates only changed parts | When enabled (optional) |

### 2.2 Manual Commands

Users can trigger manual operations in the following ways:

#### Method 1: Conversation Triggers (Recommended)

Simply say the following to AI:

| What You Say | Action | Description |
|--------------|--------|-------------|
| "Refresh knowledge index" | `rebuild` | Rebuild entire index |
| "Update knowledge base" | `rebuild` | Rebuild entire index |
| "Rebuild knowledge index" | `rebuild` | Rebuild entire index |
| "Knowledge base stats" | `stats` | View index statistics |
| "View knowledge base" | `stats` | View index statistics |
| "Knowledge base status" | `stats` | View index statistics |
| "Search knowledge base" | `search` | Search knowledge base content |
| "Search in knowledge" | `search` | Search knowledge base content |
| "In the knowledge" | `search` | Search knowledge base content |
| "Find in knowledge" | `search` | Search knowledge base content |
| "Knowledge search" | `search` | Search knowledge base content |
| "Knowledge query" | `search` | Search knowledge base content |

#### Method 2: Command Line Triggers

```bash
# Navigate to skill directory
cd ~/.openclaw/skills/markdown-knowledge

# Build index
python3 knowledge_base.py build

# Search knowledge base
python3 knowledge_base.py search "your question"

# View statistics
python3 knowledge_base.py stats

# Initialize config (first-time use)
python3 knowledge_base.py init
python3 knowledge_base.py init ~/your-knowledge-path
```

### 2.3 Core Feature List

| Feature | Status | Description |
|---------|--------|-------------|
| ✅ Markdown File Parsing | Done | Supports frontmatter, titles, keywords, tags extraction |
| ✅ Multi-level Directory Scan | Done | Supports recursive subdirectory scanning |
| ✅ Content Block Splitting | Done | Split by H2 headings for precise retrieval |
| ✅ Semantic Scoring & Ranking | Done | Multi-level scoring: title > keywords > tags > content |
| ✅ Context Injection | Done | Automatically injects relevant snippets into AI conversation |
| ✅ Incremental Update | Done | Only updates changed documents |
| ✅ Exclusion Patterns | Done | Supports excluding `.trash`, `@Recycle` and other directories |
| 🔜 Semantic Vector Search | Planned | Use embeddings to improve retrieval accuracy |
| 🔜 Multi-language Support | Planned | Support English, Japanese and other language documents |

---

## 3. Quick Start

### 3.1 Installation Steps

#### Method 1: Via ClawHub (Recommended)

```bash
clawhub install markdown-knowledge
```

#### Method 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/your-repo/markdown-knowledge.git

# Navigate to directory
cd markdown-knowledge

# Install to OpenClaw skills directory
cp -r . ~/.openclaw/skills/markdown-knowledge
```

### 3.2 First-Time Setup

```
+----------------------------------------------------------+
|                   First-Time Flow                        |
+----------------------------------------------------------+
|                                                          |
|  Step 1:  Create your knowledge base folder               |
|                                                          |
|          mkdir -p ~/Knowledge                            |
|          # or use your own folder                        |
|                                                          |
|  Step 2:  Put your Markdown files in                     |
|                                                          |
|          ~/Knowledge/                                    |
|          ├── my-notes.md                                |
|          └── project-docs/                              |
|              └── design.md                              |
|                                                          |
|  Step 3:  Initialize and build index                      |
|                                                          |
|          python3 knowledge_base.py init                  |
|          # or specify path: python3 knowledge_base.py init ~/my-docs |
|                                                          |
|  Step 4:  Start using!                                   |
|                                                          |
|          "Search knowledge: How to set up cron jobs?"   |
|                                                          |
+----------------------------------------------------------+
```

### 3.3 Verify Installation

Run the following commands to verify:

```bash
# 1. Check if skill is installed
ls -la ~/.openclaw/skills/markdown-knowledge/

# 2. View knowledge base statistics
python3 ~/.openclaw/skills/markdown-knowledge/scripts/knowledge_base.py stats

# 3. Expected output example
# 📊 Knowledge Base Statistics
# --------------------------------
# Total Documents: 12
# Total Content Blocks: 48
# Index Path: /home/user/.openclaw/skills/markdown-knowledge/index.json
# Last Updated: 2024-03-26T10:30:00.000000
```

---

## 4. User Guide

### 4.1 What Users Need to Do

```
+----------------------------------------------------------+
|                  User Responsibilities                   |
+----------------------------------------------------------+
|                                                          |
|  📁 Put Files                                            |
|     -> Just drop Markdown files into the knowledge folder |
|                                                          |
|  🔍 Ask Questions                                        |
|     -> Include trigger words like "search knowledge"    |
|                                                          |
|  🔄 Update Periodically                                  |
|     -> Say "refresh knowledge index" after changes       |
|                                                          |
+----------------------------------------------------------+
```

### 4.2 Command Trigger Reference

#### 4.2.1 Search Commands

| Chinese Phrase | Action | English Equivalent |
|----------------|--------|-------------------|
| 搜索知识库 + 问题 | search | search knowledge base |
| 查一下知识库 + 问题 | search | search in knowledge |
| 知识库里关于 XXX | search | knowledge about XXX |
| 查知识库 XXX | search | find XXX in knowledge |

**Example:**
```
User: Search knowledge, how to set up cron jobs on Linux?
AI: Searching knowledge base...
(Shows relevant document snippets)
Based on knowledge base "Linux Operations Notes"...
```

#### 4.2.2 Rebuild Commands

| Chinese Phrase | Action | Description |
|----------------|--------|-------------|
| 刷新知识库索引 | rebuild | Rebuild entire index |
| 更新知识库 | rebuild | Rebuild entire index |
| 重建知识库索引 | rebuild | Rebuild entire index |

**Example:**
```
User: Rebuild knowledge index
AI: Rebuilding index...
✅ Index build successful!
   Document count: 15
   Content block count: 62
```

#### 4.2.3 Stats Commands

| Chinese Phrase | Action | Description |
|----------------|--------|-------------|
| 知识库统计 | stats | View statistics |
| 查看知识库 | stats | View statistics |
| 知识库状态 | stats | View statistics |

**Example:**
```
User: Knowledge base stats
AI: 📊 Knowledge Base Statistics
   --------------------------------
   Total Documents: 12
   Total Content Blocks: 48
   Last Updated: 2024-03-26
```

### 4.3 Auto-Trigger Mechanism

```
Trigger Detection Flow:

+----------------------------------------------------------+
|  User Message                                             |
|       |                                                   |
|  OpenClaw matches trigger                                 |
|       |                                                   |
|  +----------------------------------------------------+  |
|  | Matched search trigger?                            |  |
|  |     | Yes            | No                         |  |
|  | Call search     Check other triggers              |  |
|  +----------------------------------------------------+  |
+----------------------------------------------------------+
```

**Auto-Trigger Conditions:**

| Trigger Type | Condition | Auto Execute |
|--------------|-----------|-------------|
| `auto_refresh` | Config enabled + file change detected | Incrementally update index |
| Search request | Message contains trigger word | Execute search and inject context |
| Context injection | Relevant results found | Automatically add snippets to context |

### 4.4 Knowledge Organization Best Practices

> **⚠️ Important: Knowledge Quality Determines Output Quality**
> 
> The knowledge base is only as good as the documents you put in it. Follow these practices to maximize effectiveness.

#### Recommended Directory Structure

```
~/Knowledge/
│
├── 📁 技术文档/                  # Technical documentation
│   ├── 编程语言/
│   │   ├── Python/
│   │   └── JavaScript/
│   └── 工具使用/
│       ├── Git使用指南.md
│       └── Docker入门.md
│
├── 📁 业务知识/                  # Business knowledge
│   ├── 产品设计/
│   └── 项目管理/
│
├── 📁 个人成长/                  # Personal development
│   ├── 学习笔记/
│   └── 读书笔记/
│
└── 📁 医学健康/                  # Health/Medical
    ├── 常见疾病/
    └── 用药指南/
```

#### Key Principles for Effective Knowledge Storage

| Principle | Do | Don't |
|-----------|-----|-------|
| **Atomicity** | One concept per file | Multiple unrelated topics in one file |
| **Naming** | Use clear, descriptive titles | Generic names like "笔记.md" |
| **Frontmatter** | Always add title/keywords/tags | Skip metadata |
| **Structure** | Use ## headings to divide content | Long paragraphs without structure |
| **Updates** | Regularly update outdated content | Let knowledge become stale |

#### Frontmatter Template (Recommended)

```markdown
---
title: Python 基础教程
keywords: [Python, 编程, 入门, 学习]
tags: [编程, Python, 教程]
created: 2024-03-01
updated: 2024-06-15
category: 技术文档
---

# Python 基础教程

## 安装 Python

...
```

---

### 4.5 Real-World Usage Scenarios

These are the scenarios this skill was designed for:

#### Scenario 1: Weather Expert Mode

**When**: You want AI to analyze current weather using your knowledge base

**Workflow**:
1. Maintain weather knowledge in `~/Knowledge/气象知识/`
2. When asking about weather, AI searches knowledge base + combines with live data
3. Results are richer than generic answers

**Example**:
```
User: 北京今天天气怎么样？结合我的气象知识分析一下
AI: 📚 Searching knowledge base for relevant meteorology concepts...
✅ Found "气象预警解读", "降水形成原理" in your knowledge base

Based on your weather knowledge + live data:
- Current conditions: Temperature, humidity, wind
- Your knowledge: "强对流天气的形成需要三个条件..."
- AI provides analysis tailored to YOUR understanding level
```

#### Scenario 2: Professional Investment Configuration

**When**: You want investment advice based on YOUR financial knowledge

**Workflow**:
1. Build financial knowledge base: `~/Knowledge/金融/`
   - Investment principles (value investing, risk management)
   - Asset allocation strategies
   - Personal portfolio notes
2. When asking about stocks/funds/ETFs, AI references YOUR knowledge + current market data

**Example**:
```
User: 帮我分析一下现在的黄金走势，结合我的投资配置
AI: 📚 Found your investment notes: "黄金ETF配置策略", "风险偏好: 保守型"

Based on your knowledge + live data:
- Your current allocation: X% in bonds, Y% in equities, Z% in gold
- Your principle: "黄金用于对冲极端风险"
- Live data: Current gold price, market sentiment
- AI gives advice aligned with YOUR strategy
```

#### Scenario 3: Building a Second Brain

**When**: You want AI to remember your learning, not just answer questions

**Workflow**:
1. Save insights during conversations
2. Ask AI to organize and connect concepts
3. Search across your accumulated knowledge

**Example**:
```
User: AI, I just learned about MOPD (Multi-Teacher On-Policy Distillation) from this paper.
AI: Should I save this to your knowledge base?
User: Yes, save under "AI学习/模型训练" with tags: [AI, 蒸馏, MOPD]
AI: ✅ Saved! Want me to connect it with existing knowledge about model training?

User: Sure, link it to what I have about model compression
AI: 📚 Found "模型压缩技术" in your knowledge base. 
Connected: MOPD relates to knowledge distillation — I've linked them.
```

#### Scenario 4: Daily Knowledge Accumulation

**When**: You want to passively build knowledge over time

**Daily workflow**:
- Morning: "搜索知识库：今天要知道的XXX"
- During work: "把这个记录到知识库XXX分类"
- After learning: "刷新知识库索引"
- Weekly review: Ask AI to summarize what you've learned

**Example**:
```
User: 搜索知识库，总结一下这周我新增了哪些知识点
AI: 📚 This week you added 8 new documents covering:
- Weather forecasting principles
- Stock valuation methods  
- Python async programming
- ...

Shall I provide a structured summary of these new additions?
```

> **⚠️ Note**: Even with `auto_refresh: true` enabled, we recommend explicitly saying "刷新知识库索引" after adding or updating knowledge to ensure the index is immediately current.

**Daily habit (recommended)**:
- Morning: "搜索知识库：今天要知道的XXX"
- After learning: "把这个知识点存到知识库XXX分类"
- Weekly: "刷新知识库索引" to rebuild index

---

## 5. Configuration

### 5.1 Config File Path

```
Unified Config Path (Recommended):
~/.openclaw/skills/markdown-knowledge/config.json

Legacy Path (v1.0.0):
~/.openclaw/knowledge-base/config.json
```

### 5.2 Key Configuration Parameters

```json
{
    // ===== Required =====
    
    "knowledge_path": "~/Knowledge",
    // Type: string
    // Description: Directory where Markdown documents are stored (supports ~ expansion)
    // Example: "~/Documents/my-notes" or "/home/user/knowledge"
    
    "index_path": "~/.openclaw/skills/markdown-knowledge/index.json",
    // Type: string
    // Description: Index file storage path
    // Recommended: Keep default, not recommended to change
    
    
    // ===== Optional =====
    
    "search_top_k": 3,
    // Type: number
    // Default: 3
    // Description: Number of most relevant documents returned per search
    // Recommended: 3-5 for daily use, 5-10 for professional research
    
    "auto_refresh": true,
    // Type: boolean
    // Default: true
    // Description: Whether to enable automatic index refresh
    // When enabled, new/modified files will automatically update index
    
    "refresh_interval": 3600,
    // Type: number
    // Default: 3600 (seconds)
    // Description: Auto refresh interval (only effective when auto_refresh=true)
    
    "exclude_patterns": [
        ".markdown",
        ".trash",
        "@Recycle",
        "node_modules"
    ]
    // Type: array[string]
    // Default: [".markdown", ".trash", "@Recycle", "node_modules"]
    // Description: Directory or filename patterns to exclude during scanning
}
```

### 5.3 Configuration Examples

#### Example 1: Basic (Recommended for Beginners)

```json
{
    "knowledge_path": "~/Knowledge",
    "index_path": "~/.openclaw/skills/markdown-knowledge/index.json",
    "search_top_k": 3,
    "auto_refresh": true
}
```

#### Example 2: Multi-Folder Knowledge Base

```json
{
    "knowledge_path": "~/Documents/my-knowledge",
    "index_path": "~/.openclaw/skills/markdown-knowledge/index.json",
    "search_top_k": 5,
    "auto_refresh": true,
    "refresh_interval": 1800
}
```

#### Example 3: High Performance (For 500+ Files)

```json
{
    "knowledge_path": "~/Knowledge",
    "index_path": "~/.openclaw/skills/markdown-knowledge/index.json",
    "search_top_k": 3,
    "auto_refresh": false,
    "exclude_patterns": [
        ".markdown",
        ".trash",
        "@Recycle",
        "node_modules",
        ".git"
    ]
}
```

### 5.4 How to Customize

**Step 1: Create or edit config file**
```bash
nano ~/.openclaw/skills/markdown-knowledge/config.json
```

**Step 2: Modify config and save**
```json
{
    "knowledge_path": "~/your-knowledge-path",
    "search_top_k": 5
}
```

**Step 3: Rebuild index (important!)**
```bash
python3 ~/.openclaw/skills/markdown-knowledge/scripts/knowledge_base.py build
```

---

## 6. Precautions

### 6.1 File Count Limit

```
+----------------------------------------------------------+
|  ⚠️  Important Limitations                               |
+----------------------------------------------------------+
|                                                          |
|  Maximum: 2000 MD files                                  |
|                                                          |
|  What happens if exceeded?                              |
|  • Index building slows down                            |
|  • Search response delays                               |
|  • Memory usage increases                              |
|                                                          |
|  Recommended: ≤ 500 files for best experience           |
|                                                          |
+----------------------------------------------------------+
```

**Optimization Tips:**

| Scenario | Solution |
|----------|----------|
| 500-2000 files | Disable `auto_refresh`, manually update periodically |
| Over 2000 files | Split into multiple knowledge bases |
| Single file over 1MB | Split into multiple smaller files |
| Large image attachments | Use external links, do not embed base64 |

### 6.2 When to Build Index

| Situation | Need Rebuild? | Recommended Action |
|----------|---------------|-------------------|
| First install | ✅ Yes | `knowledge_base.py init` |
| New files added | ⚙️ Depends | Auto when `auto_refresh=true`, otherwise manual |
| Files modified | ⚙️ Depends | Auto when `auto_refresh=true`, otherwise manual |
| Files deleted | ❌ No | Automatically excluded on next build |
| Config changed | ✅ Yes | Rebuild after modification |

### 6.3 No Sensitive Info in Knowledge Base

```
+----------------------------------------------------------+
|  🔒 Security Warning                                      |
+----------------------------------------------------------+
|                                                          |
|  ❌ DO NOT include:                                     |
|                                                          |
|  • Passwords, API Keys, Tokens                          |
|  • ID numbers, bank card numbers, personal info          |
|  • Trade secrets, internal documents                     |
|  • Anything you don't want AI to know                  |
|                                                          |
|  ✅ SAFE to include:                                    |
|                                                          |
|  • Technical documentation, tutorials                    |
|  • Meeting notes (with sensitive info removed)          |
|  • Personal knowledge, study notes                       |
|  • Product documentation, manuals                        |
|                                                          |
|  💡 Note: Knowledge base content is loaded into AI context |
|                                                          |
+----------------------------------------------------------+
```

### 6.4 Other Precautions

| Precaution | Description |
|-----------|-------------|
| **Use `~` for paths** | Use `~` to represent home directory, avoid hardcoded paths |
| **Encoding** | All files use UTF-8 encoding to avoid garbled Chinese |
| **File naming** | Avoid special characters (`/`, `\`, `*`, etc.), use Chinese or English naming |
| **Directory structure** | Don't nest too deeply (recommended: no more than 5 levels) |
| **Regular backup** | Regularly backup important index file `index.json` |
| **Disk space** | Ensure at least 100MB available for index storage |

---

## 7. Migration Guide

### Upgrading from Old Version
v1.0.0 → v1.1.0 upgraded config path:
- Old path: `~/.openclaw/knowledge-base/config.json`
- New path: `~/.openclaw/skills/markdown-knowledge/config.json`

### Automatic Compatibility
System will automatically detect old path config and continue using it, no manual migration needed.

### Manual Migration (Optional)
To migrate config, run:
```bash
mv ~/.openclaw/knowledge-base/config.json ~/.openclaw/skills/markdown-knowledge/config.json
mv ~/.openclaw/knowledge-base/index.json ~/.openclaw/skills/markdown-knowledge/index.json
```

---

## 8. File Structure

### 8.1 Directory Structure

```
~/.openclaw/skills/markdown-knowledge/
|
|-- SKILL.md                      # Skill definition file (read by OpenClaw)
|-- PROJECT.md                    # Project documentation (this file)
|-- README.md                     # Quick reference documentation
|-- config.json                   # Configuration file
|-- knowledge_base.py            # Main entry script (CLI)
|
|-- actions/                      # OpenClaw actions module
|   |-- __init__.py              # Module initialization
|   |-- actions.py               # Actions interface definition
|
|-- lib/                          # Core library
|   |-- __init__.py               # Module initialization
|   |-- knowledge_core.py         # Core engine (parse/index/search)
|   |-- global_memory.py          # Global injection module (disabled by default)
|
|-- index.json                    # Generated index file (auto-created)
    This file is auto-generated by the system, do not edit manually
```

### 8.2 File Descriptions

| File | Purpose | Editable? |
|------|---------|-----------|
| `SKILL.md` | OpenClaw skill definition, describes trigger words and action mappings | ⚠️ Advanced users only |
| `PROJECT.md` | Detailed project documentation | ✅ Yes |
| `README.md` | Quick introduction and getting started | ✅ Yes |
| `config.json` | User configuration, stores knowledge base path and other settings | ✅ Recommended |
| `knowledge_base.py` | CLI tool, provides init/build/search/stats commands | ❌ Not recommended |
| `actions/actions.py` | OpenClaw actions interface, defines search/build/stats/check | ❌ Not recommended |
| `lib/knowledge_core.py` | Core engine, contains parser, indexer, retriever | ❌ Not recommended |
| `lib/global_memory.py` | Global injection module (optional, disabled by default) | ⚠️ Advanced users only |
| `index.json` | Index data file (auto-generated) | ❌ Auto-generated |

---

## 9. FAQ

### Q1: What if nothing happens after installation?

**A:** Manually run the initialization command:

```bash
cd ~/.openclaw/skills/markdown-knowledge
python3 knowledge_base.py init
```

---

### Q2: How to fix index build failure?

**A:** Troubleshoot with these steps:

```
Step 1: Check if knowledge base path is correct
        ls -la ~/Knowledge  # Confirm directory exists and contains .md files

Step 2: Check config file
        cat ~/.openclaw/skills/markdown-knowledge/config.json
        # Confirm knowledge_path points to correct directory

Step 3: Check file permissions
        chmod 755 ~/.openclaw/skills/markdown-knowledge/
        
Step 4: Rebuild
        python3 knowledge_base.py build
```

---

### Q3: What to do if running out of memory on Raspberry Pi?

**A:** Optimize configuration:

```json
{
    "search_top_k": 2,
    "auto_refresh": false,
    "exclude_patterns": [
        ".markdown",
        ".trash",
        "@Recycle",
        "node_modules",
        ".git",
        "__pycache__"
    ]
}
```

Or reduce the number of knowledge base files.

---

### Q4: What if search results are inaccurate?

**A:** Optimize document format:

```markdown
---
title: Python Basic Tutorial
keywords: Python, programming, beginner
tags: [programming, Python, tutorial]
created: 2024-01-15
---

# Python Basic Tutorial

## Install Python

Content...
```

- Add clear titles (`#` headings)
- Use frontmatter to add keywords and tags
- Use H2 headings (`##`) to split content blocks

---

### Q5: How to exclude certain files from index?

**A:** Configure `exclude_patterns` in `config.json`:

```json
{
    "exclude_patterns": [
        ".markdown",
        ".trash",
        "@Recycle",
        "node_modules",
        "private-notes"
    ]
}
```

---

### Q6: What to do after knowledge base content is updated?

**A:**

| Situation | Action |
|----------|--------|
| `auto_refresh: true` | No action needed, auto update |
| `auto_refresh: false` | Say "refresh knowledge index" |

---

### Q7: Can I use multiple knowledge base directories simultaneously?

**A:** Direct configuration of multiple directories is not currently supported. Recommended:
- Use symlinks: `ln -s /path/to/other ~/Knowledge/other`
- Or merge into a parent directory

---

### Q8: What if index file is too large?

**A:**

| Cause | Solution |
|-------|----------|
| Too many files | Split knowledge base, reduce files |
| Single file too large | Split into multiple smaller files (<1MB) |
| Cache not excluded | Add `.cache`, `__pycache__` to exclusion list |

---

## 10. Changelog

### v1.1.0 (2024-03-26)

**Bug Fixes:**
- 🐛 Fixed path inconsistency, unified to `~/.openclaw/skills/markdown-knowledge/config.json`
- 🐛 Fixed config file loading priority issue

**Improvements:**
- ⚡ Optimized trigger mechanism for better matching accuracy
- ⚡ Optimized index build speed
- ⚡ Improved search result ranking algorithm
- 📝 Updated documentation with bilingual explanations

**New Features:**
- ✨ Support incremental update (`incremental_update`)
- ✨ Added health check command (`check` action)

---

### v1.0.0 (2024-03-25)

**Initial Release:**
- 🎉 Initial version released
- 🔍 Basic semantic search functionality
- 📦 Markdown file parsing support
- 💉 Context injection functionality
- 🔄 Automatic index refresh

---

## 11. Roadmap

### 11.1 Continuous Improvement Plan

```
+----------------------------------------------------------+
|                    Version Roadmap                       |
+----------------------------------------------------------+
|                                                          |
|  🔜 v1.2.0 (Planned)                                    |
|     • Embeddings-based semantic search                   |
|     • Multi-language document support                    |
|                                                          |
|  🔜 v1.3.0 (Planned)                                    |
|     • Web UI management interface                        |
|     • Batch import/export                                |
|                                                          |
|  💭 v2.0.0 (Future)                                     |
|     • Multi-knowledge base management                    |
|     • Knowledge graph visualization                      |
|                                                          |
+----------------------------------------------------------+
```

### 11.2 Planned Features

| Feature | Priority | ETA | Description |
|---------|----------|-----|-------------|
| Semantic vector search | 🔴 High | v1.2.0 | Use embeddings to improve retrieval accuracy |
| Multi-language support | 🔴 High | v1.2.0 | Support English, Japanese documents |
| Web management interface | 🟡 Medium | v1.3.0 | GUI for managing knowledge base |
| Batch operations | 🟡 Medium | v1.3.0 | Batch import/export |
| Multiple knowledge bases | 🟢 Low | v2.0.0 | Manage multiple knowledge bases simultaneously |
| Knowledge graph | 🟢 Low | v2.0.0 | Visualize knowledge relationships |

### 11.3 How to Report Issues

| Method | Channel |
|--------|---------|
| **GitHub Issues** | [https://github.com/your-repo/markdown-knowledge/issues](https://github.com/your-repo/markdown-knowledge/issues) |
| **Submit PR** | Pull Requests welcome |
| **Feature requests** | Via OpenClaw feedback channel |

**When reporting, please include:**
- OS and version (e.g., macOS 14.2 / Raspberry Pi OS 64-bit)
- OpenClaw version
- Config file content (hide sensitive info)
- Reproduction steps and error messages

---

## Appendix: Recommended Knowledge Base Directory Structure

### Recommended Structure

```
~/Knowledge/
|
|-- technical-docs/
|   |-- programming-languages/
|   |   |-- Python/
|   |   |   |-- basic-syntax.md
|   |   |   |-- advanced-features.md
|   |   |-- JavaScript/
|   |       |-- TypeScript.md
|   |-- tools/
|       |-- git-guide.md
|       |-- docker-getting-started.md
|
|-- business-knowledge/
|   |-- product-design/
|   |   |-- user-research-methods.md
|   |-- project-management/
|       |-- agile-practices.md
|
|-- personal-growth/
|   |-- study-notes/
|   |   |-- 2024-learning-plan.md
|   |-- book-notes/
|       |-- atomic-habits.md
|       |-- deep-work.md
|
|-- templates/
    |-- meeting-notes-template.md
    |-- weekly-report-template.md
```

---

**Last Updated:** 2024-03-26

**Contact:** See GitHub repository

---

*If you find this skill useful, please Star ⭐ to show support!*

---

# Markdown 知识库 for OpenClaw

> **版本 1.1.0** | 将您的本地 Markdown 文件变成可对话的智能知识库

---

## 目录

1. [项目简介](#一项目简介)
2. [功能说明](#二功能说明)
3. [快速开始](#三快速开始)
4. [使用指南](#四使用指南)
   - 4.4 知识整理规范
   - 4.5 使用场景
5. [配置说明](#五配置说明)
6. [注意事项](#六注意事项)
7. [配置迁移说明](#七配置迁移说明)
8. [文件结构](#八文件结构)
9. [常见问题](#九常见问题)
10. [版本历史](#十版本历史)
11. [后续计划](#十一后续计划)

---

## 一、项目简介

### 1.1 技能名称与描述

| 项目 | 说明 |
|------|------|
| **技能名称** | `markdown-knowledge` |
| **版本** | v1.1.0 |
| **描述** | 将本地 Markdown 知识库与 OpenClaw 集成，支持语义检索和上下文注入 |
| **作者** | aaronjager92 |
| **许可证** | MIT |

### 1.2 核心功能

```
+----------------------------------------------------------+
|                      核心工作流                           |
+----------------------------------------------------------+
|  用户提问                                                 |
|       |                                                   |
|  AI 匹配触发词                                            |
|       |                                                   |
|  知识库检索                                               |
|       |                                                   |
|  相关文档片段注入上下文                                    |
|       |                                                   |
|  AI 基于知识回答                                          |
+----------------------------------------------------------+
```

**核心能力：**

- 🔍 **语义检索** — 理解用户问题的含义，而非简单的关键词匹配
- 💉 **上下文注入** — 自动将相关知识注入 AI 对话上下文
- 📦 **开箱即用** — 零配置即可使用默认设置
- 🔄 **实时同步** — 自动追踪文件变化，无需手动刷新

### 1.3 支持规模

| 指标 | 限制 | 说明 |
|------|------|------|
| **最大文件数** | ≤ 2000 个 MD 文件 | 超过此数量可能影响性能 |
| **推荐文件数** | ≤ 500 个 MD 文件 | 最佳体验的推荐数量 |
| **单文件大小** | ≤ 1 MB | 超过此大小建议拆分成多个文件 |
| **支持格式** | `.md` | 仅支持 Markdown 格式 |

### 1.4 设计目标

```
+----------------------------------------------------------+
|                       设计原则                            |
+----------------------------------------------------------+
|                                                          |
|  ✅ 开箱即用                                              |
|     安装后立即可用，无需复杂配置                          |
|                                                          |
|  ✅ 轻量高效                                              |
|     专为树莓派等资源受限环境优化                          |
|                                                          |
|  ✅ 跨平台                                                |
|     支持 Linux、macOS、Windows、树莓派                    |
|                                                          |
|  ✅ 隐私优先                                              |
|     所有数据存储在本地，不上传任何内容                    |
|                                                          |
+----------------------------------------------------------+
```

### 1.5 做这个的初衷 —— 我们的理念

> **"AI 时代，大家都在匆匆忙忙地提问、得到答案，然后这些答案又被拿去训练下一代 AI。我们想留下点什么。"**

我们从一个小小的念头开始：

| 以前 | 现在 |
|------|------|
| 问完 → 得到答案 → 忘掉 | 学到 → 存下来 → 成长 |
| 知识散落在各个 AI 服务商的服务器上 | 知识存在你自己的文件里 |
| 你的答案被用来训练别人的模型 | 你的洞察，属于你的知识库 |
| 一次性的问答 | 会生长的活知识 |
| 昂贵的云端 RAG 服务 | 任何人都能跑的轻量 RAG |

**我们做的是：**

- 🌱 **个人知识花园** — 不是简单的 Q&A，而是与你一起成长的知识收藏
- 📚 **微型 RAG** — 开销极小，能跑在树莓派上，轻松搬运和迁移
- 🏠 **你的数据，你做主** — 不依赖云端，不用订阅，不被服务商锁定
- 🔄 **活的文档** — 你的笔记，你的文档，你的知识 — AI 随时可用

**目标：**

> 在这个 AI 吞噬一切来训练自己的时代，这个技能是一个小小的反叛。你的知识应该属于你、随你生长、留在你身边。

```
+------------------+     +------------------+     +------------------+
|      学习         | --> |      保存         | --> |      成长         |
+------------------+     +------------------+     +------------------+
     |                      |                      |
     v                      v                      v
 获得新洞察            存入你的知识库           AI 用你的上下文回答

---

## 二、功能说明

### 2.1 自动功能（无需用户操作）

以下功能由系统自动完成，无需用户干预：

| 功能 | 自动行为 | 何时触发 |
|------|---------|----------|
| **配置加载** | 自动读取 `config.json` 配置 | 每次调用时 |
| **索引加载** | 自动加载已有索引文件 | 搜索操作时 |
| **路径解析** | 自动转换 `~` 为用户主目录 | 配置解析时 |
| **文档解析** | 自动解析 Markdown 元数据和内容块 | 构建索引时 |
| **结果格式化** | 自动生成易读的搜索结果 | 搜索完成后 |
| **增量更新** | 自动检测文件变化，只更新有变动的部分 | 启用时（可选） |

### 2.2 手动命令（用户触发）

用户可以通过以下方式触发手动操作：

#### 方式一：对话触发（推荐）

直接对 AI 说出以下命令：

| 用户说法 | 触发动作 | 说明 |
|----------|----------|------|
| "**刷新知识库索引**" | `rebuild` | 立即重建整个索引 |
| "**更新知识库**" | `rebuild` | 立即重建整个索引 |
| "**重建知识库索引**" | `rebuild` | 立即重建整个索引 |
| "**知识库统计**" | `stats` | 查看索引统计信息 |
| "**查看知识库**" | `stats` | 查看索引统计信息 |
| "**知识库状态**" | `stats` | 查看索引统计信息 |
| "**搜索知识库**" | `search` | 搜索知识库内容 |
| "**查一下知识库**" | `search` | 搜索知识库内容 |
| "**知识库里**" | `search` | 搜索知识库内容 |
| "**查知识库**" | `search` | 搜索知识库内容 |
| "**知识库搜索**" | `search` | 搜索知识库内容 |
| "**知识库查询**" | `search` | 搜索知识库内容 |

#### 方式二：命令行触发

```bash
# 进入技能目录
cd ~/.openclaw/skills/markdown-knowledge

# 构建索引
python3 knowledge_base.py build

# 搜索知识库
python3 knowledge_base.py search "你的问题"

# 查看统计
python3 knowledge_base.py stats

# 初始化配置（首次使用）
python3 knowledge_base.py init
python3 knowledge_base.py init ~/你的知识库路径
```

### 2.3 核心功能列表

| 功能 | 状态 | 说明 |
|------|------|------|
| ✅ Markdown 文件解析 | 已完成 | 支持 frontmatter、标题、关键词、标签提取 |
| ✅ 多级目录扫描 | 已完成 | 支持递归扫描子目录 |
| ✅ 内容块分割 | 已完成 | 按二级标题分割，便于精确检索 |
| ✅ 语义评分排序 | 已完成 | 标题>关键词>标签>内容的多级评分 |
| ✅ 上下文注入 | 已完成 | 自动将相关片段注入 AI 对话 |
| ✅ 增量更新 | 已完成 | 只更新有变化的文档 |
| ✅ 排除模式 | 已完成 | 支持排除 `.trash`、`@Recycle` 等目录 |
| 🔜 语义向量检索 | 计划中 | 使用 embeddings 提升检索精度 |
| 🔜 多语言支持 | 计划中 | 支持英文、日文等多语言文档 |

---

## 三、快速开始

### 3.1 安装步骤

#### 方式一：使用 ClawHub 安装（推荐）

```bash
clawhub install markdown-knowledge
```

#### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/your-repo/markdown-knowledge.git

# 进入目录
cd markdown-knowledge

# 安装到 OpenClaw 技能目录
cp -r . ~/.openclaw/skills/markdown-knowledge
```

### 3.2 首次使用

```
+----------------------------------------------------------+
|                      首次使用流程                          |
+----------------------------------------------------------+
|                                                          |
|  Step 1:  创建知识库目录                                   |
|                                                          |
|          mkdir -p ~/Knowledge                            |
|          # 或使用你自己的目录                             |
|                                                          |
|  Step 2:  放入 Markdown 文件                              |
|                                                          |
|          ~/Knowledge/                                    |
|          ├── 我的笔记.md                                  |
|          └── 项目文档/                                   |
|              └── 设计方案.md                              |
|                                                          |
|  Step 3:  初始化并构建索引                                |
|                                                          |
|          python3 knowledge_base.py init                  |
|          # 或指定路径：python3 knowledge_base.py init ~/我的文档 |
|                                                          |
|  Step 4:  开始使用！                                      |
|                                                          |
|          "搜索知识库：如何设置定时任务？"                   |
|                                                          |
+----------------------------------------------------------+
```

### 3.3 验证安装成功

执行以下命令验证：

```bash
# 1. 检查技能是否安装
ls -la ~/.openclaw/skills/markdown-knowledge/

# 2. 查看知识库统计
python3 ~/.openclaw/skills/markdown-knowledge/scripts/knowledge_base.py stats

# 3. 预期输出示例
# 📊 知识库统计信息
# --------------------------------
# 总文档数：12
# 总内容块：48
# 索引路径：/home/user/.openclaw/skills/markdown-knowledge/index.json
# 最后更新：2024-03-26T10:30:00.000000
```

---

## 四、使用指南

### 4.1 使用者需要干什么

```
+----------------------------------------------------------+
|                      用户职责                             |
+----------------------------------------------------------+
|                                                          |
|  📁 放置文件                                              |
|     -> 只需把 Markdown 文件放入知识库目录即可              |
|                                                          |
|  🔍 提出问题                                              |
|     -> 在问题中提到"搜索知识库"、"查一下"等触发词          |
|                                                          |
|  🔄 定期更新                                              |
|     -> 新增或修改文件后，说"刷新知识库索引"                 |
|                                                          |
+----------------------------------------------------------+
```

### 4.2 手动命令触发词对照表

#### 4.2.1 搜索命令

| 中文说法 | 触发动作 | 说明 |
|----------|----------|------|
| 搜索知识库 + 问题 | search | 搜索知识库内容 |
| 查一下知识库 + 问题 | search | 搜索知识库内容 |
| 知识库里关于 XXX | search | 搜索知识库内容 |
| 查知识库 XXX | search | 搜索知识库内容 |

**使用示例：**
```
用户：搜索知识库，如何在 Linux 上设置定时任务？
AI：正在检索知识库...
（显示相关文档片段）
根据知识库《Linux 运维笔记》...
```

#### 4.2.2 重建索引命令

| 中文说法 | 触发动作 | 说明 |
|----------|----------|------|
| 刷新知识库索引 | rebuild | 重建整个索引 |
| 更新知识库 | rebuild | 重建整个索引 |
| 重建知识库索引 | rebuild | 重建整个索引 |

**使用示例：**
```
用户：重建知识库索引
AI：正在重建索引...
✅ 索引构建成功！
   文档数量：15
   内容块数：62
```

#### 4.2.3 统计命令

| 中文说法 | 触发动作 | 说明 |
|----------|----------|------|
| 知识库统计 | stats | 查看统计信息 |
| 查看知识库 | stats | 查看统计信息 |
| 知识库状态 | stats | 查看统计信息 |

**使用示例：**
```
用户：知识库统计
AI：📊 知识库统计信息
   --------------------------------
   总文档数：12
   总内容块：48
   最后更新：2024-03-26
```

### 4.3 自动触发机制说明

```
触发检测流程：

+----------------------------------------------------------+
|  用户消息                                                 |
|       |                                                   |
|  OpenClaw 匹配触发词                                      |
|       |                                                   |
|  +----------------------------------------------------+  |
|  | 命中"搜索/查/查询"类触发词？                        |  |
|  |     | 是              | 否                        |  |
|  | 调用 search       检查其他触发词                    |  |
|  +----------------------------------------------------+  |
+----------------------------------------------------------+
```

**自动触发条件：**

| 触发类型 | 条件 | 自动执行 |
|----------|------|----------|
| `auto_refresh` | 配置启用 + 文件变更检测 | 增量更新索引 |
| 搜索搜索请求 | 消息包含触发词 | 执行搜索并注入上下文 |
| 上下文注入 | 搜索到相关结果 | 自动将片段加入上下文 |

---

### 4.5 实际使用场景

这些是我们设计这个技能时针对的实际场景：

#### 场景一：气象专家模式

**场景**：你想让 AI 结合气象知识分析天气

**工作流**：
1. 在 `~/Knowledge/气象知识/` 维护气象知识
2. 询问天气时，AI 搜索知识库 + 结合实时数据
3. 结果比通用回答更丰富、更专业

**示例**：
```
用户：北京今天天气怎么样？结合我的气象知识分析一下
AI：📚 在知识库中搜索相关气象概念...
✅ 找到了"气象预警解读"、"降水形成原理"

结合你的气象知识 + 实时数据进行分析：
- 当前状况：温度、湿度、风力
- 你的知识："强对流天气的形成需要三个条件..."
- AI 提供符合你认知水平的专业分析
```

#### 场景二：专业投资配置

**场景**：你想基于自己的金融知识获得投资建议

**工作流**：
1. 建立金融知识库：`~/Knowledge/金融/`
   - 投资原则（价值投资、风险管理）
   - 资产配置策略
   - 个人投资笔记
2. 询问股票/基金/黄金时，AI 参考你的知识 + 当前市场数据

**示例**：
```
用户：帮我分析一下现在的黄金走势，结合我的投资配置
AI：📚 找到了你的投资笔记："黄金ETF配置策略"、"风险偏好: 保守型"

基于你的知识 + 实时数据：
- 你的当前配置：债券 X%、股票 Y%、黄金 Z%
- 你的原则："黄金用于对冲极端风险"
- 实时数据：当前金价、市场情绪
- AI 给出符合你策略的投资建议
```

#### 场景三：构建第二大脑

**场景**：你想让 AI 记住你学到的东西，而不只是回答问题

**工作流**：
1. 在对话中保存洞察
2. 让 AI帮你整理和串联概念
3. 跨时间搜索你积累的知识

**示例**：
```
用户：AI，我刚从这篇论文学到了 MOPD（Multi-Teacher On-Policy Distillation）
AI：要不要帮你存到知识库里？
用户：好，存到"AI学习/模型训练"，标签：[AI, 蒸馏, MOPD]
AI：✅ 已保存！要不要帮你关联到已有的模型训练知识？

用户：好，关联到我关于模型压缩的内容
AI：📚 在知识库中找到了"模型压缩技术"
已关联：MOPD 与知识蒸馏相关 —— 我已建立连接。
```

#### 场景四：日常知识积累

**场景**：你想随时间被动地建立知识体系

**每日工作流**：
- 早上：搜索知识库：今天要了解的 XXX
- 工作中：把这个记录到知识库 XXX 分类
- 学完后：刷新知识库索引
- 每周回顾：让 AI 总结你新增了哪些知识点

**示例**：
```
用户：搜索知识库，总结一下这周我新增了哪些知识点
AI：📚 这周你新增了 8 个文档，覆盖：
- 气象预报原理
- 股票估值方法
- Python 异步编程
- ...

需要我提供这些新知识的结构化总结吗？
```

> **⚠️ 注意**：即使 `auto_refresh: true` 已启用，也建议在新增或更新知识后明确说"刷新知识库索引"，确保索引立即更新。

---

## 五、配置说明

### 5.1 配置文件路径

```
统一配置路径（推荐）:
~/.openclaw/skills/markdown-knowledge/config.json

兼容旧路径（v1.0.0）:
~/.openclaw/knowledge-base/config.json
```

### 5.2 关键配置参数

```json
{
    // ===== 必需配置 =====
    
    "knowledge_path": "~/Knowledge",
    // 类型：string
    // 说明：Markdown 文档所在目录（支持 ~ 路径展开）
    // 示例："~/Documents/我的笔记" 或 "/home/user/knowledge"
    
    "index_path": "~/.openclaw/skills/markdown-knowledge/index.json",
    // 类型：string
    // 说明：索引文件存储路径
    // 建议保持默认，不要修改
    
    
    // ===== 可选配置 =====
    
    "search_top_k": 3,
    // 类型：number
    // 默认值：3
    // 说明：每次搜索返回的最相关文档数量
    // 推荐：日常使用 3-5，专业研究 5-10
    
    "auto_refresh": true,
    // 类型：boolean
    // 默认值：true
    // 说明：是否启用自动刷新索引功能
    // 启用后，新增/修改文件会自动更新索引
    
    "refresh_interval": 3600,
    // 类型：number
    // 默认值：3600（秒）
    // 说明：自动刷新间隔（仅 auto_refresh=true 时生效）
    
    "exclude_patterns": [
        ".markdown",
        ".trash",
        "@Recycle",
        "node_modules"
    ]
    // 类型：array[string]
    // 默认值：[".markdown", ".trash", "@Recycle", "node_modules"]
    // 说明：扫描时排除的目录或文件名模式
}
```

### 5.3 配置示例

#### 示例一：基本使用（推荐新手）

```json
{
    "knowledge_path": "~/Knowledge",
    "index_path": "~/.openclaw/skills/markdown-knowledge/index.json",
    "search_top_k": 3,
    "auto_refresh": true
}
```

#### 示例二：多目录知识库

```json
{
    "knowledge_path": "~/Documents/我的知识库",
    "index_path": "~/.openclaw/skills/markdown-knowledge/index.json",
    "search_top_k": 5,
    "auto_refresh": true,
    "refresh_interval": 1800
}
```

#### 示例三：高性能配置（适合 500+ 文件）

```json
{
    "knowledge_path": "~/Knowledge",
    "index_path": "~/.openclaw/skills/markdown-knowledge/index.json",
    "search_top_k": 3,
    "auto_refresh": false,
    "exclude_patterns": [
        ".markdown",
        ".trash",
        "@Recycle",
        "node_modules",
        ".git"
    ]
}
```

### 5.4 如何自定义

**步骤 1：创建或编辑配置文件**
```bash
nano ~/.openclaw/skills/markdown-knowledge/config.json
```

**步骤 2：修改配置并保存**
```json
{
    "knowledge_path": "~/你的知识库路径",
    "search_top_k": 5
}
```

**步骤 3：重新构建索引（重要！）**
```bash
python3 ~/.openclaw/skills/markdown-knowledge/scripts/knowledge_base.py build
```

---

## 六、注意事项

### 6.1 文件数量限制

```
+----------------------------------------------------------+
|  ⚠️  重要限制                                            |
+----------------------------------------------------------+
|                                                          |
|  最大文件数：2000 个 MD 文件                              |
|                                                          |
|  超过限制会发生什么？                                     |
|  • 索引构建变慢                                          |
|  • 搜索响应延迟                                          |
|  • 内存占用增加                                          |
|                                                          |
|  建议：≤ 500 个文件 for 最佳体验                         |
|                                                          |
+----------------------------------------------------------+
```

**优化建议：**

| 场景 | 建议 |
|------|------|
| 文件数量 500-2000 | 关闭 `auto_refresh`，手动定期更新 |
| 文件数量超过 2000 | 拆分成多个知识库 |
| 单文件超过 1MB | 拆分成多个小文件 |
| 大量图片附件 | 使用外部链接，不要嵌入 base64 |

### 6.2 索引构建时机

| 情况 | 是否需要重建 | 推荐方式 |
|------|-------------|----------|
| 首次安装 | ✅ 是 | `knowledge_base.py init` |
| 新增文件 | ⚙️ 取决于 | `auto_refresh=true` 时自动，否则手动 |
| 修改文件 | ⚙️ 取决于 | `auto_refresh=true` 时自动，否则手动 |
| 删除文件 | ❌ 不需要 | 下次构建时自动排除 |
| 修改配置 | ✅ 是 | 修改后重新 build |

### 6.3 敏感信息不要放入知识库

```
+----------------------------------------------------------+
|  🔒 安全警告                                              |
+----------------------------------------------------------+
|                                                          |
|  ❌ 不要包含：                                            |
|                                                          |
|  • 密码、API Keys、Tokens                                 |
|  • 身份证号、银行卡号等个人信息                           |
|  • 商业机密、内部文档                                     |
|  • 任何不想让 AI 知道的内容                              |
|                                                          |
|  ✅ 可以包含：                                            |
|                                                          |
|  • 技术文档、教程                                         |
|  • 会议笔记（去除敏感信息）                               |
|  • 个人知识、学习笔记                                     |
|  • 产品说明、操作手册                                     |
|                                                          |
|  💡 提示：知识库内容会被加载到 AI 上下文中                 |
|                                                          |
+----------------------------------------------------------+
```

### 6.4 其他注意事项

| 注意事项 | 说明 |
|----------|------|
| **路径使用 `~`** | 配置中推荐使用 `~` 表示主目录，避免硬编码路径 |
| **编码格式** | 所有文件使用 UTF-8 编码，避免中文乱码 |
| **文件命名** | 避免特殊字符（`/`、`\`、`*`等），推荐使用中文或英文命名 |
| **目录结构** | 不要嵌套过深（建议不超过 5 层），便于维护 |
| **定期备份** | 重要索引文件 `index.json` 定期备份 |
| **磁盘空间** | 确保至少 100MB 可用空间用于索引存储 |

---

## 七、配置迁移说明

### 从旧版本升级
v1.0.0 → v1.1.0 版本升级了配置路径：
- 旧路径：`~/.openclaw/knowledge-base/config.json`
- 新路径：`~/.openclaw/skills/markdown-knowledge/config.json`

### 自动兼容
系统会自动检测旧路径配置并继续使用，无需手动迁移。

### 手动迁移（可选）
如需迁移配置，执行：
```bash
mv ~/.openclaw/knowledge-base/config.json ~/.openclaw/skills/markdown-knowledge/config.json
mv ~/.openclaw/knowledge-base/index.json ~/.openclaw/skills/markdown-knowledge/index.json
```

---

## 八、文件结构

### 8.1 目录结构说明

```
~/.openclaw/skills/markdown-knowledge/
|
|-- SKILL.md                      # 技能定义文件（OpenClaw 读取）
|-- PROJECT.md                    # 项目说明文档（本文件）
|-- README.md                     # 简要说明文档
|-- config.json                   # 配置文件
|-- knowledge_base.py            # 主入口脚本（CLI）
|
|-- actions/                      # OpenClaw 动作模块
|   |-- __init__.py              # 模块初始化
|   |-- actions.py               # 动作接口定义
|
|-- lib/                          # 核心库
|   |-- __init__.py               # 模块初始化
|   |-- knowledge_core.py         # 核心引擎（解析/索引/检索）
|   |-- global_memory.py          # 全局注入模块（默认禁用）
|
|-- index.json                    # 生成的索引文件（自动创建）
    此文件由系统自动生成，无需手动编辑
```

### 8.2 各文件作用

| 文件 | 作用 | 是否可编辑 |
|------|------|-----------|
| `SKILL.md` | OpenClaw 技能定义，描述触发词和动作映射 | ⚠️ 仅高级用户 |
| `PROJECT.md` | 本项目详细说明文档 | ✅ 可以 |
| `README.md` | 简要介绍和快速开始 | ✅ 可以 |
| `config.json` | 用户配置文件，存储知识库路径等设置 | ✅ 建议编辑 |
| `knowledge_base.py` | 命令行工具，提供 init/build/search/stats 命令 | ❌ 不建议 |
| `actions/actions.py` | OpenClaw 动作接口，定义 search/build/stats/check | ❌ 不建议 |
| `lib/knowledge_core.py` | 核心引擎，包含解析器、索引器、检索器 | ❌ 不建议 |
| `lib/global_memory.py` | 全局注入模块（可选，默认禁用） | ⚠️ 仅高级用户 |
| `index.json` | 索引数据文件（自动生成） | ❌ 自动生成 |

---

## 九、常见问题

### Q1: 安装后没有自动初始化怎么办？

**A:** 手动执行初始化命令：

```bash
cd ~/.openclaw/skills/markdown-knowledge
python3 knowledge_base.py init
```

---

### Q2: 索引构建失败怎么解决？

**A:** 按以下步骤排查：

```
Step 1: 检查知识库路径是否正确
        ls -la ~/Knowledge  # 确认目录存在且包含 .md 文件

Step 2: 检查配置文件
        cat ~/.openclaw/skills/markdown-knowledge/config.json
        # 确认 knowledge_path 指向正确目录

Step 3: 检查文件权限
        chmod 755 ~/.openclaw/skills/markdown-knowledge/
        
Step 4: 重新构建
        python3 knowledge_base.py build
```

---

### Q3: 树莓派上运行内存不足怎么办？

**A:** 优化配置：

```json
{
    "search_top_k": 2,
    "auto_refresh": false,
    "exclude_patterns": [
        ".markdown",
        ".trash",
        "@Recycle",
        "node_modules",
        ".git",
        "__pycache__"
    ]
}
```

或减少知识库文件数量。

---

### Q4: 搜索结果不准确怎么办？

**A:** 优化文档格式：

```markdown
---
title: Python 基础教程
keywords: Python, 编程, 入门
tags: [编程, Python, 教程]
created: 2024-01-15
---

# Python 基础教程

## 安装 Python

正文内容...
```

- 添加清晰的标题（`#` 标题）
- 使用 frontmatter 添加 keywords 和 tags
- 使用二级标题（`##`）分割内容块

---

### Q5: 如何排除某些文件不加入索引？

**A:** 在 `config.json` 中配置 `exclude_patterns`：

```json
{
    "exclude_patterns": [
        ".markdown",
        ".trash",
        "@Recycle",
        "node_modules",
        "私人笔记"
    ]
}
```

---

### Q6: 知识库内容更新后需要做什么？

**A:**

| 情况 | 操作 |
|------|------|
| `auto_refresh: true` | 无需操作，自动更新 |
| `auto_refresh: false` | 说"刷新知识库索引" |

---

### Q7: 可以同时使用多个知识库目录吗？

**A:** 目前不支持直接配置多个目录。建议：
- 使用软链接：`ln -s /path/to/other ~/Knowledge/other`
- 或合并到一个父目录

---

### Q8: 索引文件太大怎么办？

**A:**

| 原因 | 解决方案 |
|------|----------|
| 文件数量太多 | 拆分知识库，减少文件 |
| 单文件太大 | 拆分成多个小文件（<1MB） |
| 未排除缓存 | 添加 `.cache`, `__pycache__` 等到排除列表 |

---

## 十、版本历史

### v1.1.0 (2024-03-26)

**修复内容：**
- 🐛 修复路径不一致问题，统一使用 `~/.openclaw/skills/markdown-knowledge/config.json`
- 🐛 修复配置文件加载优先级问题

**优化内容：**
- ⚡ 优化触发机制，提高匹配准确性
- ⚡ 优化索引构建速度
- ⚡ 改善搜索结果排序算法
- 📝 更新文档，增加双语说明

**新增功能：**
- ✨ 支持增量更新（`incremental_update`）
- ✨ 添加健康检查命令（`check` action）

---

### v1.0.0 (2024-03-25)

**首次发布：**
- 🎉 初始版本发布
- 🔍 基础语义检索功能
- 📦 支持 Markdown 文件解析
- 💉 上下文注入功能
- 🔄 自动索引刷新

---

## 十一、后续计划

### 11.1 持续更新计划

```
+----------------------------------------------------------+
|                      版本规划                              |
+----------------------------------------------------------+
|                                                          |
|  🔜 v1.2.0 (计划中)                                      |
|     • 支持语义向量检索（基于 embeddings）                 |
|     • 多语言文档支持                                      |
|                                                          |
|  🔜 v1.3.0 (计划中)                                      |
|     • Web UI 管理界面                                     |
|     • 批量导入/导出功能                                   |
|                                                          |
|  💭 v2.0.0 (远期计划)                                   |
|     • 支持多知识库管理                                    |
|     • 知识图谱可视化                                      |
|                                                          |
+----------------------------------------------------------+
```

### 11.2 计划中的功能

| 功能 | 优先级 | 预计版本 | 说明 |
|------|--------|---------|------|
| 语义向量检索 | 🔴 高 | v1.2.0 | 使用 embeddings 提升检索精度 |
| 多语言支持 | 🔴 高 | v1.2.0 | 支持英文、日文等文档 |
| Web 管理界面 | 🟡 中 | v1.3.0 | 图形化管理知识库 |
| 批量操作 | 🟡 中 | v1.3.0 | 批量导入导出 |
| 多知识库 | 🟢 低 | v2.0.0 | 同时管理多个知识库 |
| 知识图谱 | 🟢 低 | v2.0.0 | 可视化知识关联 |

### 11.3 如何反馈问题

如果您遇到问题或有功能建议，欢迎通过以下方式反馈：

| 反馈方式 | 渠道 |
|----------|------|
| **GitHub Issues** | [https://github.com/your-repo/markdown-knowledge/issues](https://github.com/your-repo/markdown-knowledge/issues) |
| **提交 PR** | 欢迎提交 Pull Request |
| **功能建议** | 通过 OpenClaw 反馈渠道 |

**反馈时建议包含：**
- 操作系统和版本（如：macOS 14.2 / 树莓派 OS 64-bit）
- OpenClaw 版本
- 配置文件内容（隐藏敏感信息）
- 复现步骤和错误信息

---

## 附录：推荐的知识库目录结构

### 推荐结构

```
~/Knowledge/
|
|-- 技术文档/
|   |-- 编程语言/
|   |   |-- Python/
|   |   |   |-- 基础语法.md
|   |   |   |-- 高级特性.md
|   |   |-- JavaScript/
|   |       |-- TypeScript.md
|   |-- 工具使用/
|       |-- Git 使用指南.md
|       |-- Docker 入门.md
|
|-- 业务知识/
|   |-- 产品设计/
|   |   |-- 用户研究方法.md
|   |-- 项目管理/
|       |-- 敏捷开发实践.md
|
|-- 个人成长/
|   |-- 学习笔记/
|   |   |-- 2024年学习计划.md
|   |-- 读书笔记/
|       |-- 原子习惯.md
|       |-- 深度工作.md
|
|-- 常用模板/
    |-- 会议纪要模板.md
    |-- 周报模板.md
```

---

**最后更新：** 2024-03-26

**联系作者：** 详见 GitHub 仓库

---

*如果您觉得这个技能有用，欢迎 Star ⭐ 支持！*
