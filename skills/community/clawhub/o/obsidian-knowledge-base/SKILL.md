# SKILL.md — Obsidian Dual-Layer Knowledge Base System

> Version: 0.2 | Updated: 2026-05-22
> Skill Name: obsidian-knowledge-base
> Tags: knowledge-management, obsidian, rag, agent-memory, daily-pipeline
> Install: `npx clawhub@latest install obsidian-knowledge-base`

---

## 1. Skill Overview

Turn Obsidian into a **Dual-Layer Knowledge Base** for AI Agents, supporting the full pipeline: daily incremental writes → structured indexing → context injection.

- **INBOX Layer**: Raw material entry (articles/conversations/logs), unstructured
- **WIKI Layer**: Structured knowledge (concept cards + Q&A cards), directly callable by AI

**Core Value**: Solve the "knowledge base paralysis" problem — knowledge gets written in, but the AI starts from scratch every time because it doesn't know what's in the base.

---

## 2. Directory Structure

```
Obsidian Vault/
├── INBOX/                          # Input layer (raw materials)
│   ├── articles/                   # Articles (daily scheduled writes)
│   ├── conversations/            # Conversation records
│   └── 日志/                    # Work logs (date-indexed)
└── wiki/
    ├── qa/                        # Q&A knowledge cards
    │   ├── index.md              # Q&A index (by category)
    │   └── Q-分类-摘要.md
    └── concepts/                  # Concept cards (deep structure)
        ├── index.md              # Concept card index
        ├── 概念-主题名.md
        └── ...
```

---

## 3. Knowledge Base Scale & Context Strategy

| Layer | File Count | Raw Size | How It Enters Context |
|-------|-----------|---------|----------------------|
| INBOX/articles | Daily incremental | Raw material | Not injected; searched on demand |
| wiki/qa | ~200-500 cards | ~500KB-1MB | **Daily 6KB summary injected** |
| wiki/concepts | ~20-100 cards | ~50-100KB | Searched on demand |

**Context Strategy (Progressive Disclosure)**:
- **At startup**: Run `wiki_daily_brief.py` → generate 6KB category summary → inject into context
- **During tasks**: Specific question → `tdai_memory_search` / `wiki_search` → read raw snippet (~700 chars)
- **Forbidden**: Do not pour full wiki content into context (session limit: 200KB)

---

## 4. Naming Conventions

### 4.1 INBOX/articles/

```
【Category】YYYY-MM-DD-Title.md
Example: 【Industry Research】2026-05-22-Some Industry Deep Dive Summary.md
```

**Category Tags**: 城市更新 / 物业管理 / 土地市场 / 楼市分析 / 城投转型 / 政策速递 / 行业研究 / 他山之石

### 4.2 wiki/qa/

```
Q-Category-ContentSummary.md
Example: Q-IndustryResearch-WhatAreKeyPointsOfCommercialPropertyLeaseManagement.md
```

### 4.3 wiki/concepts/

```
Concept-TopicName.md
Example: Concept-CityRenewal.md
```

---

## 5. Card Templates

### 5.1 Q&A Card Template (frontmatter)

```yaml
---
type: qa
date: 2026-05-22
title: Q-Category-ContentSummary
tags: [Category]
scenarios: [Report Writing/Article Writing/Policy Research]
keywords: [keyword1, keyword2]
operation: knowledge-query
---

## Question
(Specific question)

## Answer
(Complete answer, cite the source text, do not generalize)
```

### 5.2 Concept Card Template (frontmatter)

```yaml
---
type: concept
date: 2026-05-22
title: Topic Name
tags: [Category, Subcategory]
source: Source
summary: One-sentence core conclusion
---

# Concept: Topic Name

## When to Use
When encountering the following keywords/scenarios, prioritize this card:
- Keyword 1
- Keyword 2

## Core Conclusion (One Sentence)

## Detailed Content

## Source/Evidence
```

---

## 6. Filter Rules (Mandatory)

**Content PROHIBITED from writing to wiki/qa/ and wiki/concepts/**:

| Category | Examples | Correct Destination |
|----------|---------|-------------------|
| Work logs / daily matters | "Today's completed work", "Core completion items" | INBOX/日志/ |
| OpenClaw operations config | "How to batch process documents", "cron config" | skills/SKILL.md |
| Memory/session mechanisms | "OpenClaw memory scheme", "session structure" | memory/ (non-wiki) |
| Scheduled tasks/Cron | "How to write cron tasks" | skills/SKILL.md |
| Technical troubleshooting | "API Key invalid troubleshooting" | skills/SKILL.md |

**Content ALLOWED in wiki**:

Any **structured knowledge** refined through analysis and processing, including but not limited to:
- Industry/domain knowledge (concepts, models, cases, data)
- Policy interpretation and applicable scenarios
- Core conclusions and methods from research reports
- Standards and operational guidelines
- Cross-domain comparative analysis

**Rule of Thumb**: If a user can directly use it to write a report or make a decision, it's knowledge.

---

## 7. Daily Pipeline

```
05:00 ── INPUT END ──────────────────────────────
│
│  cron: Daily news scraping
│  → Scrape news → write to INBOX/articles/
│  → Push Word summary to relevant people
│
│  Note: Do NOT write to wiki/ directly; 8:30 handles it
│
08:30 ── OUTPUT END (Knowledge Base Injection) ──
│
│  cron: Daily knowledge base injection
│  → Scan INBOX/articles/ for today's new files
│  → Write to wiki/qa/ (extract Q&A pairs)
│  → Write to wiki/concepts/ (extract concept cards)
│  → Filter out operational content (see Section 6)
│  → Run wiki_daily_brief.py to update daily summary
│  → Push summary to owner (X new cards today, Z total in base)
│
│  At Session Startup (automatic):
│  → Run wiki_daily_brief.py
│  → Inject 6KB category summary into context
│  → AI knows what's available in the knowledge base today
```

---

## 8. Retrieval Flow (Per Task)

```
Receiving an analysis/writing task
  → wiki_daily_brief already injected at startup (6KB summary)
  → wiki_search(topic keywords) → match Q&A cards
  → High match → use the answer directly
  → Low match → wiki_search(subtopic) → read concept card
  → Still insufficient → search INBOX/articles/ raw materials
  → Last resort → web_search
```

---

## 9. wiki_daily_brief.py Script

```python
#!/usr/bin/env python3
"""
wiki_daily_brief.py
Run at first session startup each day. Generates a wiki knowledge base
daily summary so the model knows what's available in the knowledge base.

Output: ~/.openclaw/workspace/memory/wiki_daily_brief.md
"""
WIKI_QA_DIR = "/path/to/Obsidian/wiki/qa"
OUT = "~/.openclaw/workspace/memory/wiki_daily_brief.md"

# Script logic:
# 1. Scan all .md files in wiki/qa/ (excluding index.md)
# 2. Extract frontmatter tags, count by category
# 3. Take top 3 per category as examples, generate ~6KB summary
# 4. Write to OUT, ready for session startup injection
```

---

## 10. Daily Summary Format

```markdown
# Wiki Knowledge Base Daily Summary
> Generated: 2026-05-22 | Total: 230 Q&A Cards

---

## Available Knowledge Cards (By Category)

### Industry Research (83 cards)
- **What is the core content of「Some Report」?** (Source: `Q-IndustryResearch-SomeReport.md`)
- ...
  - ...and 80 more

### City Renewal (66 cards)
- ...

## Usage Guide
To query specific card content, call `tdai_memory_search` or `wiki_search`.
```

---

## 11. Installation

```bash
# Method 1: ClawHub
npx clawhub@latest install obsidian-knowledge-base

# Method 2: Manual
cp -r obsidian-knowledge-base ~/.openclaw/skills/
```

---

## 12. Use Cases

- Knowledge workers who need AI to write reports, analysis, or official documents
- Teams that want AI to have "memory" instead of starting from scratch every time
- Scenarios with daily incremental material inputs (news, reports, data)
- Teams that want knowledge base and AI context to work together, not in silos
