# Multi-layered Memory System

To make the AI your true engineering partner without suffering from context pollution and token limits, this Skill introduces an advanced, multi-layered memory system inspired by advanced platforms (Index-Content Separation & Smart Retrieval).

## 1. The Architecture: Index-Content Separation
Instead of loading a massive JSON file containing all project history into the context window, this Skill uses a decentralized memory architecture:
- **The Index (`.claude/MEMORY.md`)**: A lightweight, always-read index file. It acts as a table of contents, mapping broad topics to specific memory files.
- **The Topics (`.claude/memory-topics/*.json` or `*.md`)**: Detailed, domain-specific memory files (e.g., `database-rules.json`, `ui-components.md`). These are only retrieved when the Index suggests they are relevant to the current task.

## 2. Memory Scopes
- **Session Memory**: Temporary context relevant only to the current task execution. Kept in the working memory.
- **Global/Agent Memory**: Transferable methodologies, project constraints, and "Lessons Learned" that are persisted across sessions in the topic files.

## 3. How the Execution Loop Uses Memory

### Clarify Phase (Retrieval)
1. Read `.claude/MEMORY.md` (if it exists).
2. Determine if any topics listed in the index are relevant to the current goal and scope.
3. Use the `Read` tool to fetch only the relevant topic files.
4. Incorporate these retrieved rules and lessons into the task map.

### Deliver Phase (Extraction & Compact)
1. At the end of the task, the AI asks: *"What did we learn from this task that I should remember for next time?"* or self-reflects on errors encountered.
2. The AI categorizes the new lesson into an existing topic or creates a new one in `.claude/memory-topics/`.
3. If a new topic is created, the AI updates the central index `.claude/MEMORY.md`.

## 4. Why This Matters
By keeping the index small (usually < 200 lines), the AI remains fast and focused. It only "remembers" the full details of the database schema when you ask it to modify the database, perfectly balancing deep context with token efficiency.
