---
name: obsidian-wiki
description: Build and maintain a personal knowledge Wiki using the LLM Wiki pattern with OpenClaw-optimized step-by-step execution. Use sub-agents for parallel processing of file operations, content extraction, and wiki maintenance. This skill is designed for OpenClaw environments where file reading may be partial - it uses chunked reading and task delegation to ensure completeness. For PDF/Word conversion, it automatically checks and installs Python and required packages (pypdf, python-docx) if not present.
---

# Obsidian Wiki Builder for OpenClaw

A skill for building and maintaining personal knowledge bases using the **LLM Wiki pattern**, optimized for OpenClaw with **step-by-step execution** and **sub-agent delegation**.

How to use:
Send the following command:
Set cron to run "obsidian-wiki" from skills.

Initial Setup:
The skill will automatically initialize and create a vault named "Obsidian Wiki" in your root directory. Simply open this vault with Obsidian to view your knowledge base.

Workflow:
When sending files to OpenClaw, instruct it to save them in the ~/Obsidian Wiki/raw/ directory.

> **Note:** This skill utilizes parallel task descriptions ("spawn X agent for each file"), which OpenClaw automatically executes as sub-agents. It automatically manages Python environment setup and library installations to handle diverse file formats. This skill is specifically optimized for autonomous execution to align with OpenClaw's native workflow. 

## The Core Idea

Unlike traditional RAG, the LLM Wiki is a **persistent, compounding artifact**. When you add a source, the LLM doesn't just index it — it reads, extracts, and integrates knowledge into the existing wiki.

**Key principle:** The human curates sources and asks questions; the LLM does all the bookkeeping through delegated sub-agents.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (Main Claude)                                 │
│  - Plans and coordinates all operations                     │
│  - Spawns sub-agents for parallel work                      │
│  - Aggregates results and maintains TaskList                │
├─────────────────────────────────────────────────────────────┤
│  SUB-AGENTS                                                 │
│  ├─ FileReader      → Reads files in chunks                 │
│  ├─ CategoryDetector → Detects file categories              │
│  ├─ EntityExtractor → Extracts entities from content        │
│  ├─ ConceptExtractor → Extracts concepts from content       │
│  ├─ PageCreator     → Creates wiki pages                    │
│  ├─ IndexUpdater    → Updates index.md and log.md           │
│  └─ CrossReferencer → Creates wiki links                    │
├─────────────────────────────────────────────────────────────┤
│  THREE-LAYER ARCHITECTURE                                   │
│  ~/Obsidian Wiki/                                           │
│  ├── CLAUDE.md     (Schema)                                 │
│  ├── raw/          (Immutable sources)                      │
│  └── wiki/         (LLM-generated knowledge)                │
└─────────────────────────────────────────────────────────────┘
```

---

## TaskList-Driven Workflow

Every operation uses a TaskList to track progress. Tasks are executed by sub-agents in parallel where possible.

### Task States
- `pending` → `in_progress` → `completed`/`failed`
- Tasks can have dependencies (`blockedBy`)
- Tasks can spawn child tasks

---

## Core Operations

### 1. Initialize Wiki

Create the complete directory structure with TaskList tracking.

**Workflow:**

```
TaskList: Initialize Wiki
├── [1] Create base directory (~/Obsidian Wiki/)
├── [2] Create raw/ folder
├── [3] Create wiki/ folder
├── [4] Create wiki subdirectories
│   ├── [4a] wiki/00_Index/
│   ├── [4b] wiki/10_Sources/
│   ├── [4c] wiki/20_Entities/
│   ├── [4d] wiki/30_Concepts/
│   ├── [4e] wiki/40_Syntheses/
│   └── [4f] wiki/99_Attachments/
├── [5] Create CLAUDE.md (depends on [1])
├── [6] Create index.md (depends on [4a])
└── [7] Create log.md (depends on [4a])
```

**Execution:**
1. Create TaskList with all tasks
2. Execute independent tasks in parallel (1-3)
3. Execute dependent tasks sequentially (4-7)
4. Report completion status

---

### 2. Auto-Organize Raw Files

Scan, categorize, rename, and move files using parallel sub-agents.

**Workflow:**

```
Phase 1: Discovery
└── Spawn FileScanner agent
    └── Scan raw/ for unorganized files
    └── Return: list of files with paths

Phase 2: Categorization (Parallel)
└── For each file, spawn CategoryDetector agent
    └── Analyze filename (priority 1)
    └── If unclear, read first 500 chars (priority 2)
    └── Return: detected category + confidence

Phase 3: Organization (Parallel)
└── For each categorized file, spawn FileOrganizer agent
    └── Generate timestamp: YYYYMMDD-HHMMSS
    └── Create category folder if needed
    └── Rename: timestamp-original_name.ext
    └── Move to category folder
    └── Return: new path + metadata

Phase 4: Ingest (Parallel)
└── For each organized file, spawn Ingestor agent
    └── Read full content (chunked if large)
    └── Create source summary page
    └── Extract entities → create/update entity pages
    └── Extract concepts → create/update concept pages
    └── Return: pages created/updated

Phase 5: Aggregation
└── Spawn IndexUpdater agent
    └── Update index.md with all new/updated pages
    └── Append entries to log.md
    └── Return: final summary
```

**TaskList Structure:**

```
TaskList: Auto-Organize Raw Files
├── Phase 1: Discovery
│   └── [1] Scan raw directory
├── Phase 2: Categorization
│   ├── [2] Detect category: file1.md (depends on [1])
│   ├── [3] Detect category: file2.pdf (depends on [1])
│   └── [4] Detect category: file3.txt (depends on [1])
├── Phase 3: Organization
│   ├── [5] Organize file1.md (depends on [2])
│   ├── [6] Organize file2.pdf (depends on [3])
│   └── [7] Organize file3.txt (depends on [4])
├── Phase 4: Ingest
│   ├── [8] Ingest file1.md (depends on [5])
│   ├── [9] Ingest file2.pdf (depends on [6])
│   └── [10] Ingest file3.txt (depends on [7])
└── Phase 5: Aggregation
    └── [11] Update index and log (depends on [8,9,10])
```

---

### 3. Ingest Single Source

Deep ingestion of one source file with parallel extraction.

**Workflow:**

```
Phase 1: Read Content
└── Spawn FileReader agent with chunked reading
    └── If file > 50KB, read in 50KB chunks
    └── Aggregate all chunks
    └── Return: full content

Phase 2: Parallel Analysis
├── Spawn SummaryGenerator agent (depends on Phase 1)
│   └── Generate source summary
│   └── Return: summary content
├── Spawn EntityExtractor agent (depends on Phase 1)
│   └── Extract people, orgs, products
│   └── Return: entity list with context
└── Spawn ConceptExtractor agent (depends on Phase 1)
    └── Extract key concepts, frameworks
    └── Return: concept list with definitions

Phase 3: Page Creation (Parallel)
├── Spawn SourcePageCreator agent
│   └── Create wiki/10_Sources/<filename>.md
├── For each entity, spawn EntityPageCreator agent
│   └── Create/update wiki/20_Entities/<entity>.md
└── For each concept, spawn ConceptPageCreator agent
    └── Create/update wiki/30_Concepts/<concept>.md

Phase 4: Cross-Reference
└── Spawn CrossReferencer agent
    └── Add wiki links between related pages
    └── Update entity pages with mentions

Phase 5: Index Update
└── Spawn IndexUpdater agent
    └── Update wiki/00_Index/index.md
    └── Append to wiki/00_Index/log.md
```

---

### 4. Query Knowledge Base

Answer questions using parallel page reading.

**Workflow:**

```
Phase 1: Index Analysis
└── Read wiki/00_Index/index.md
    └── Identify relevant pages

Phase 2: Parallel Page Reading
└── For each relevant page, spawn PageReader agent
    └── Read page content
    └── Return: page content + relevance score

Phase 3: Synthesis
└── Spawn AnswerSynthesizer agent
    └── Combine all page contents
    └── Generate answer with citations
    └── Return: synthesized answer

Phase 4: Optional Filing
└── If answer is valuable:
    └── Spawn SynthesisPageCreator agent
        └── Create wiki/40_Syntheses/<question>.md
```

---

### 5. Lint (Health Check)

Parallel health check of the wiki.

**Workflow:**

```
TaskList: Lint Wiki
├── Phase 1: Data Collection (Parallel)
│   ├── [1] Check for contradictions
│   ├── [2] Find orphan pages
│   ├── [3] Find missing concept pages
│   ├── [4] Check for stale claims
│   ├── [5] Verify cross-references
│   └── [6] Identify data gaps
├── Phase 2: Report Generation
│   └── [7] Aggregate findings (depends on [1-6])
└── Phase 3: Optional Fixes
    └── [8] Create missing pages (depends on [7])
    └── [9] Fix broken references (depends on [7])
```

**Auto-Maintenance Mode Behavior:**

In auto-maintenance mode, Lint will **automatically fix** simple issues and **flag** complex issues:

| Check Item | Auto-Fix Behavior | Flag Behavior |
|------------|-------------------|---------------|
| **Orphan pages** | Add reference in index.md Inbox | None |
| **Missing concept pages** | Auto-create basic page (draft) | Log to log.md for later refinement |
| **Broken cross-references** | None | Mark as `[[Broken Link]]` |
| **Contradictory claims** | None | Add `## Contradictions` section |
| **Stale claims** | None | Add `[stale?]` tag |
| **Data gaps** | None | Log to log.md Suggested Research |

**Auto-Fix Rules:**
1. **Orphan pages**: Read page content, add reference line in index.md under appropriate category
2. **Missing concept pages**:
   - Extract context from existing mentions
   - Create basic template page
   - Add `tags: [concept, draft]`
   - Add `> [!warning] Auto-created, needs refinement` at page top
3. **Broken links**: Preserve original text, add comment `<!-- broken link: PageName -->`

---

## Sub-Agent Specifications

### FileReader Agent

**Purpose:** Read files completely, handling large files via chunking.

**Input:**
```json
{
  "file_path": "/path/to/file",
  "chunk_size": 50000,  // bytes
  "start_offset": 0
}
```

**Behavior:**
- If file size <= 50KB: read entire file
- If file size > 50KB: read in chunks, aggregate
- Return complete content with metadata

**Output:**
```json
{
  "content": "full file content",
  "file_size": 123456,
  "chunks_read": 3,
  "complete": true
}
```

---

### FileConverter Agent

**Purpose:** Convert PDF, Word, and other non-Markdown files to Markdown format.

**Supported Formats:**
- `.pdf` → `.md` (requires `pypdf` or `pdfplumber`)
- `.docx`, `.doc` → `.md` (requires `python-docx`)
- `.txt` → `.md` (native, just copy)

**Prerequisites Check:**

```bash
# Step 1: Check if Python is installed
python --version || python3 --version

# If not installed, install Python:
# macOS: brew install python
# Linux: sudo apt-get install python3 python3-pip
# Windows: Download from python.org

# Step 2: Check if required packages are installed
python -c "import pypdf" 2>/dev/null || echo "pypdf not installed"
python -c "import docx" 2>/dev/null || echo "python-docx not installed"

# Step 3: Auto-install missing packages
pip install pypdf python-docx
```

**Conversion Process:**
1. Detect file type from extension
2. Check/install required Python packages
3. Extract text content
4. Create Markdown version alongside original file
5. Return path to Markdown file

**Behavior:**
- Original file is preserved (immutable sources)
- Markdown copy is created in same directory
- Markdown includes YAML frontmatter with source reference
- If conversion fails, log error and skip file

**Output:**
```json
{
  "success": true,
  "original_file": "document.pdf",
  "markdown_file": "document.md",
  "conversion_method": "pypdf",
  "pages_extracted": 5,
  "error": null
}
```

---

### CategoryDetector Agent

**Purpose:** Detect file category based on filename and content.

**Categories:**
- `articles/` - Articles, blog posts, news
- `research/` - Research papers, technical documents, analysis reports
- `books/` - Book chapters, reading notes
- `meetings/` - Meeting notes, transcripts
- `projects/` - Project documents, PRDs, plans, milestones
- `inbox/` - Todo items, temporary files, unprocessed
- `journal/` - Diaries, daily logs, weekly reviews
- `reference/` - Reference materials, cheatsheets, handbooks
- `notes/` - General notes
- `others/` - Uncategorized

**Priority Rules:**
1. Filename keywords (strongest)
2. File extension
3. First 500 chars of content (if needed)

**Auto-Maintenance Mode Behavior:**
- **Deterministic judgment**: Based on explicit filename keywords (e.g., meeting, sync, paper, research, etc.)
- **No ambiguous questions**: If category is unclear, use `inbox/` or `others/` directly
- **Keyword mapping**:
  - `meeting`, `sync`, `discuss`, `会议`, `讨论` → `meetings/`
  - `paper`, `research`, `study`, `analysis`, `调研`, `研究`, `分析` → `research/`
  - `article`, `blog`, `post`, `文章`, `博客` → `articles/`
  - `book`, `chapter`, `reading`, `书籍`, `章节`, `阅读` → `books/`
  - `project`, `prd`, `spec`, `plan`, `milestone`, `项目`, `需求`, `规划`, `复盘` → `projects/`
  - `todo`, `inbox`, `temp`, `待办`, `收件箱`, `临时` → `inbox/`
  - `journal`, `diary`, `daily`, `日志`, `日记`, `周记` → `journal/`
  - `ref`, `cheatsheet`, `handbook`, `guide`, `manual`, `参考`, `手册`, `速查` → `reference/`
  - `note`, `memo`, `draft`, `笔记`, `备忘录`, `草稿` → `notes/`
  - Others or ambiguous → `others/`
- **Quick return**: Only read first 500 chars as auxiliary, no deep content analysis

**Output Format:**
```json
{
  "file": "filename.md",
  "category": "articles|research|books|meetings|projects|inbox|journal|reference|notes|others",
  "confidence": "high|medium|low",
  "reason": "brief explanation"
}
```

---

### EntityExtractor Agent

**Purpose:** Extract entities from source content.

**Entity Types:**
- `person` - People
- `organization` - Companies, institutions
- `product` - Products, services
- `place` - Locations

**Output:** List of entities with context quotes.

**Auto-Maintenance Mode Behavior:**
- **Extract all possible entities**, include even if uncertain
- **Entity disambiguation**: Merge when same noun appears multiple times, preserve all contexts
- **Auto-categorize**: Determine entity type based on context
- **No questions asked**: Directly output extraction results

---

### ConceptExtractor Agent

**Purpose:** Extract key concepts and frameworks.

**Output:** List of concepts with:
- Definition
- Context from source
- Related concepts

**Auto-Maintenance Mode Behavior:**
- **Extract all explicitly defined concepts** (e.g., "X refers to...")
- **Extract recurring terms** (may imply importance)
- **Keep definitions brief**: No more than 2-3 sentences
- **Annotate source context**: Each concept must include quote from source
- **No questions asked**: Directly output all identified concepts

---

### PageCreator Agent

**Purpose:** Create or update wiki pages.

**Input:**
```json
{
  "page_type": "source|entity|concept|synthesis",
  "title": "Page Title",
  "content": {...},
  "template": "standard"
}
```

**Output:** Path to created/updated page.

**Auto-Maintenance Mode Behavior:**
- **Source pages**: Always create new page (each source is unique)
- **Entity/Concept pages**:
  - Read existing page (if present)
  - **Auto-merge**: Append new content to existing content
  - **Handle conflicts**: Add `## Contradictions` section to document differences
  - **Update metadata**: Append source reference, update `updated` timestamp
- **No confirmation**: Directly write to file
- **Atomic write**: Complete content written at once, avoid partial writes

**Merge Strategy Example:**
```
Existing Concept page definition: "X is A"
New source definition: "X is B"

After auto-merge:
## Definition
X has multiple definitional perspectives:
- [[Source A]]: X is A
- [[Source B]]: X is B

## Contradictions
- Source A and Source B have different definitions for X
```

---

## Page Templates

### Source Page (wiki/10_Sources/)

```markdown
---
title: "Source Title"
source: "raw/category/filename.md"
ingested: "2026-04-11"
tags: [source, domain/topic]
entities: [Entity A, Entity B]
concepts: [Concept X, Concept Y]
---

# Source Title

## Summary
Brief summary (2-3 paragraphs).

## Key Points
- Point 1
- Point 2

## Entities Mentioned
- [[Entity A]] — context

## Concepts Discussed
- [[Concept X]] — how used here

## Questions Raised
- Questions from source

## Related Sources
- [[Related Source]]
```

### Entity Page (wiki/20_Entities/)

```markdown
---
title: "Entity Name"
type: person|organization|product|place
created: "2026-04-11"
updated: "2026-04-11"
sources: [Source A, Source B]
tags: [entity, category]
---

# Entity Name

## Overview
Brief description.

## Key Information
| Attribute | Value |
|-----------|-------|
| Type | Category |
| First mentioned | [[Source A]] |

## Mentions in Sources
- From [[Source A]]: "quote or summary"

## Related
- [[Related Concept]]
```

### Concept Page (wiki/30_Concepts/)

```markdown
---
title: "Concept Name"
created: "2026-04-11"
updated: "2026-04-11"
sources: [Source A, Source B]
tags: [concept, domain]
---

# Concept Name

## Definition
Clear definition.

## Key Aspects
- Aspect 1
- Aspect 2

## Sources
- [[Source A]] — context

## Related Concepts
- [[Related Concept]]
```

---

## Error Handling

Each sub-agent should:
1. Report success/failure status
2. On failure: provide error message + partial results
3. Allow parent to retry or skip

**Retry Strategy:**
- Network errors: retry 3 times with backoff
- File not found: fail immediately
- Parse errors: try alternative parser

---

## Best Practices

### For the Orchestrator
1. **Always use TaskList** - Track every operation
2. **Parallelize where possible** - Independent tasks run together
3. **Chunk large files** - Prevent partial reads
4. **Aggregate before updating** - Batch index updates

### For Sub-Agents
1. **Complete the task fully** - Don't return partial results
2. **Report errors clearly** - Include context for debugging
3. **Respect dependencies** - Wait for prerequisite tasks
4. **Write atomically** - Complete page writes in one operation

### For the User
1. **Check TaskList** - Monitor progress of long operations
2. **Review sub-agent outputs** - Verify correctness
3. **Report failures** - Help improve error handling

---

## Directory Structure

```
~/Obsidian Wiki/
├── CLAUDE.md              # This schema file
├── raw/                   # Original sources (immutable)
│   └── (auto-organized into subfolders)
│       ├── articles/      # Articles, blog posts
│       ├── research/      # Research papers, technical docs
│       ├── books/         # Book chapters, reading notes
│       ├── meetings/      # Meeting notes, transcripts
│       ├── projects/      # Project documents, PRDs, plans
│       ├── inbox/         # Todo items, temporary files
│       ├── journal/       # Diaries, daily logs
│       ├── reference/     # Reference materials, cheatsheets
│       ├── notes/         # General notes
│       └── others/        # Uncategorized
└── wiki/                  # LLM-generated knowledge base
    ├── 00_Index/
    │   ├── index.md       # Master catalog
    │   └── log.md         # Operation history
    ├── 10_Sources/        # Source summaries
    ├── 20_Entities/       # People, orgs, products
    ├── 30_Concepts/       # Ideas, frameworks
    ├── 40_Syntheses/      # Analyses, comparisons
    └── 99_Attachments/    # Images and files
```

---

## Auto-Maintenance Mode

When the skill is triggered by OpenClaw scheduled tasks, it enters **unattended auto-maintenance mode**, automatically completing the full wiki maintenance workflow.

### Trigger Conditions
- OpenClaw scheduled task triggers (e.g., every 4 hours, daily)
- No user input or confirmation required
- All decisions made automatically

### Auto-Execution Workflow

```
Auto-Maintenance Cycle
├── Phase 1: Auto-Organize
│   └── Scan raw/ root directory for uncategorized files
│   └── Auto-detect category (based on filename/content)
│   └── Rename and move to corresponding category folder
│   └── Log to log.md
│
├── Phase 2: Ingest New Sources
│   └── Discover all uningested new files
│   └── Ingest each new file in parallel
│       ├── Create Source page
│       ├── Extract and update Entity pages
│       ├── Extract and update Concept pages
│       └── Create cross-references
│   └── Update index.md
│   └── Log to log.md
│
├── Phase 3: Health Check (Lint)
│   ├── Check for orphan pages
│   ├── Check for missing concept pages
│   ├── Verify cross-reference validity
│   ├── Identify data gaps
│   └── Auto-fix simple issues
│       ├── Create backlinks for orphan pages
│       ├── Create missing concept pages (basic template)
│       └── Flag complex issues for manual handling
│
└── Phase 4: Report Generation
    └── Generate execution summary
    └── Update log.md
    └── Output statistics
```

### Auto-Decision Rules

| Scenario | Auto Behavior |
|----------|---------------|
| Uncertain file category | Use `others/` category, no pause to ask |
| Entity exists but content conflicts | Add contradiction note on Entity page, preserve all versions |
| Concept definition conflicts | Add multi-source definition comparison on Concept page |
| Orphan page | Auto-add reference in index.md, mark as pending organization |
| Missing concept page | Auto-create basic page, mark as draft |
| Broken cross-reference | Mark as pending fix, do not auto-delete |

### Execution Report Format

After auto-maintenance completes, append to `log.md`:

```markdown
## [2026-04-12 02:00] auto-maintenance | Scheduled maintenance complete
- Duration: 45s
- Organized: 3 files → articles/, notes/
- Ingested: 2 new sources
  - [[New Article A]] — extracted 5 entities, 3 concepts
  - [[New Article B]] — extracted 2 entities, 4 concepts
- Lint fixes:
  - Fixed orphan pages: 1
  - Created missing concept pages: 2 (draft)
  - Flagged pending issues: 0
- Status: ✅ Healthy
```

### Comparison with Manual Mode

| Aspect | Manual Mode | Auto-Maintenance Mode |
|--------|-------------|----------------------|
| User confirmation | Confirm/cancel at each step | Fully automated, no confirmation |
| Uncertain category | Ask user | Use `others/` |
| Content conflicts | Discuss solutions | Log conflicts, preserve all |
| Report format | Display in conversation | Write only to log.md |
| Suitable scenarios | First ingestion, important sources | Daily maintenance, scheduled sync |

### Best Practices

1. **First-time use**: Run manually a few times first to ensure category rules are correct
2. **Schedule frequency**: Recommend every 4-6 hours or once daily
3. **Regular review**: Manually check maintenance logs in log.md weekly
4. **Process drafts**: Auto-created draft pages need manual refinement

---

## Why This Works for OpenClaw

**The Problem:**
- OpenClaw may read only part of large files
- Complex operations can be interrupted
- Context limits may truncate outputs

**The Solution:**
1. **Chunked Reading** - FileReader agent reads large files in pieces
2. **Task Persistence** - TaskList maintains state across interruptions
3. **Parallel Processing** - Sub-agents work independently
4. **Aggregation** - Results combined only when all sub-tasks complete
5. **Error Recovery** - Failed sub-tasks can be retried without restarting all

---

**Note:** This is a pattern optimized for OpenClaw. The core insight is **divide and conquer through sub-agents** — each agent has a focused task, and the orchestrator coordinates them via TaskList.