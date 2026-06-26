---
name: memory-index-manager
description: 记忆索引系统。用于管理长期项目记忆、自动维护索引、快速定位历史项目。仅在用户明确说"回忆一下""remember""recall"时触发读取，写入与OpenClaw原生机制保持一致，索引维护在后台自动进行。
---

# Memory Index Manager

A skill for project continuity and memory reconstruction. Maintains a curated index of topics with multi-generation consolidation to help recover context across long-running conversations.

## Core Design

### Trigger Rules

| Operation | Trigger | Behavior |
|-----------|---------|----------|
| **Read** | User explicitly says "回忆一下" / "remember" / "recall" / "记不记得" | Check INDEX.md → read consolidation → respond |
| **Write** | OpenClaw native flush (pre-compaction) | Write to `memory/YYYY-MM-DD.md` as usual |
| **Index Update** | End of conversation + heartbeat | Propose new entries, update dates, consolidate if needed |
| **Daily Flush** | Every day at 11:00 AM | Archive yesterday's memory, update INDEX, check consolidation |

### Philosophy

- **Passive by default**: Doesn't interrupt normal workflow
- **Active on request**: Full context recovery when explicitly asked
- **Automatic maintenance**: Index upkeep happens in background

---

## File Structure

```
memory/
├── INDEX.md                    # Master index of tracked topics
├── MEMORY.md                   # Native long-term memory (OpenClaw)
├── YYYY-MM-DD.md               # Daily memories (OpenClaw native writes)
└── consolidated/               # Multi-generation consolidations
    ├── {topic}-gen1-YYYY-MM-DD.md
    ├── {topic}-gen2-YYYY-MM-DD.md
    └── ...
```

---

## INDEX.md Format

```markdown
# Memory Index

## Projects
- **project-slug**
  - Dates: [2025-03-20, 2025-03-22, 2025-03-25, 2025-04-01]
  - Consolidations:
    - gen1 (2025-03-25): consolidated/project-slug-gen1-2025-03-25.md
  - Current: consolidated/project-slug-gen1-2025-03-25.md
  - Status: active | completed | paused | abandoned

## Major Events
- **event-slug**: [2025-03-15]
  - Description: Brief description

## Decisions
- **decision-slug**: [2025-03-10, 2025-03-12]
  - Consolidations:
    - gen1 (2025-03-12): consolidated/decision-slug-gen1-2025-03-12.md
  - Current: consolidated/decision-slug-gen1-2025-03-12.md
```

---

## Workflows

### 1. Explicit Recall ("回忆一下")

**User trigger**: "回忆一下那个网站项目" / "Remember the website project?"

**Agent workflow**:
```
1. Read INDEX.md
2. Find matching topic (fuzzy match on name)
3. If found:
   a. Read Current consolidation file
   b. Read today's memory/YYYY-MM-DD.md for fresh updates
   c. Synthesize and respond
4. If not found in INDEX:
   a. Fall back to memory_search("website project")
   b. Respond with search results
   c. (Optional) Propose adding to index if significant
```

### 2. Native Write (Automatic)

**Trigger**: OpenClaw pre-compaction flush or user says "remember this"

**Behavior**: Write to `memory/YYYY-MM-DD.md` per OpenClaw native rules

**No skill involvement** - this is pure OpenClaw behavior.

### 3. Index Maintenance (Background)

**Trigger**: End of conversation OR heartbeat

**Agent workflow**:
```
1. Review today's memory file
2. Identify topics worth indexing:
   - New projects started
   - Major events occurred
   - Important decisions made
   - Existing indexed topics mentioned
3. For existing topics: add today's date to Dates list
4. Propose new index entries to user (if autoPropose enabled)
5. Check consolidation threshold:
   - Count dates since last consolidation
   - If > 3: propose consolidation to user
   - On approval: create gen{N+1} consolidation
```

### 4. Daily Flush (11:00 AM)

**Trigger**: System cron job at 11:00 AM daily

**Agent workflow**:
```
1. Identify yesterday's date (YYYY-MM-DD)
2. Check if yesterday's memory file exists
   - If not: create empty file with <!-- DAILY_FLUSH --> marker
3. Execute OpenClaw native memory storage:
   - Append <!-- NATIVE_FLUSH --> to yesterday's file
   - Archive any in-memory context from yesterday
4. Execute Skill index update:
   - Scan yesterday's file for index-worthy topics
   - Update INDEX.md with yesterday's date
   - Check if any topic needs consolidation (>3 days)
5. Initialize today's memory file (if not exists)
6. Log flush completion
```

**Daily Flush Script**: `~/.openclaw/scripts/daily-flush.sh`
**Launchd Config**: `~/Library/LaunchAgents/com.openclaw.daily-flush.plist`

**Purpose**: Ensure yesterday's memory is properly archived even if:
- User didn't explicitly say "remember"
- Session didn't reach memoryFlush threshold
- System was restarted

---

## Consolidation Rules

### When to Consolidate

A topic needs new consolidation when:
- It has **>3 dates** (excluding today) **since last consolidation**

### Consolidation Process

1. **Create new file**: `consolidated/{topic}-gen{N}-{today}.md`
2. **Sources**:
   - Previous generation consolidation (if N>1)
   - Daily memories from dates since last consolidation
3. **Content structure**:
   ```markdown
   # {Topic} - Generation {N} Consolidation

   **Created**: 2025-04-15
   **Covers**: 2025-04-01 to 2025-04-15
   **Previous**: consolidated/{topic}-gen{N-1}-{date}.md

   ## Summary
   [Compiled narrative of all covered periods]

   ## Key Points
   - Point 1
   - Point 2

   ## Decisions Made
   - Decision 1

   ## Current Status
   [Where things stand now]

   ## Source References
   - gen{N-1}: [key info from previous consolidation]
   - 2025-04-01: [what happened]
   - 2025-04-05: [what happened]
   - ...
   ```
4. **Mark sources archived**: Add `<!-- ARCHIVED: consolidated into {file} -->` to daily files
5. **Update INDEX.md**: Add consolidation entry, update Current pointer

---

## Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Projects** | Multi-day efforts with deliverables | website redesign, app development |
| **Major Events** | Significant life/career changes | job change, relocation |
| **Decisions** | Choices with lasting impact | tech stack, vendor selection |
| **Preferences** | Personal settings that persist | communication style, tools |

---

## Configuration

`memory-index-manager/config.json`:

```json
{
  "consolidationThreshold": 3,
  "autoProposeIndex": true,
  "categories": ["Projects", "Major Events", "Decisions", "Preferences"],
  "indexFile": "memory/INDEX.md",
  "consolidatedDir": "memory/consolidated",
  "recallTriggers": ["回忆一下", "remember", "recall", "记不记得"]
}
```

---

## Integration with OpenClaw Native Memory

| Aspect | Native OpenClaw | This Skill |
|--------|-----------------|------------|
| **Storage** | `memory/*.md` | `INDEX.md` + `consolidated/*.md` |
| **Write timing** | Auto (flush) + Manual | Same (no change) |
| **Read timing** | Any search | Only on explicit recall trigger |
| **Search method** | Semantic (`memory_search`) | Index lookup + targeted read |
| **Granularity** | Chunk-level (~400 tokens) | Topic-level consolidation |

**Key point**: This skill's files are stored in `memory/` and indexed by OpenClaw's semantic search, but the skill only activates on explicit recall requests.

---

## Example Session

```
[Day 1 - 2025-03-20]
User: "Let's start a new project: building a personal blog"
Agent: [writes to memory/2025-03-20.md]
Agent: "I'll track this as 'personal-blog' project. Adding to index?"
User: "Yes"
→ Creates INDEX.md entry: personal-blog, Dates: [2025-03-20]

[Day 2 - 2025-03-22]
User: "For the blog, let's use Next.js"
Agent: [writes to memory/2025-03-22.md]
→ Updates INDEX.md: personal-blog Dates: [2025-03-20, 2025-03-22]

[Day 3 - 2025-03-25]
User: "Blog hosting should be Vercel"
Agent: [writes to memory/2025-03-25.md]
→ Updates INDEX.md: personal-blog Dates: [2025-03-20, 2025-03-22, 2025-03-25]
→ TRIGGER: 3 dates, proposes consolidation
User: "Go ahead"
→ Creates consolidated/personal-blog-gen1-2025-03-25.md
→ Archives daily files

[Day 7 - 2025-04-05]
User: "回忆一下博客项目"
Agent: [reads INDEX.md → finds personal-blog]
Agent: [reads consolidated/personal-blog-gen1-2025-03-25.md]
Agent: "We started the personal blog project on March 20th. We decided to use Next.js 
        (March 22nd) and host on Vercel (March 25th). The project is currently active."
```

---

## Migration from v1.0.0

**Breaking Changes:**
- 旧版本触发条件（每天9:00 AM、创建项目时等）已移除
- 改为纯按需触发（"回忆一下"），减少干扰
- 索引格式兼容，可无缝迁移

**升级步骤：**
1. 备份现有的 `memory/INDEX.md`
2. 更新 skill 到 2.0.0
3. 继续使用，索引文件自动兼容

---

## Usage Examples

| User Says | Agent Action |
|-----------|--------------|
| "回忆一下那个网站项目" | 查 INDEX.md → 读 consolidation → 回答 |
| "remember the blog project" | 同上，支持英文触发 |
| "把这个加入索引" | 询问分类 → 创建 INDEX.md 条目 |
| "显示索引" | 展示 INDEX.md 内容 |
| "Consolidate blog project" | 检查阈值 → 执行整合 |

---

## Notes

- Index entries are append-only; mark deprecated rather than delete
- Consolidated files are immutable; new generations for updates
- Daily memories marked archived are preserved but skipped by default
- User can force deep read: "check the original March 20th file"
