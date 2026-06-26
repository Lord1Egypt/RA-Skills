---
name: longterm-memory
description: "Long-term memory management system for maintaining MEMORY.md, consolidating daily memories, and extracting key insights. Use when: (1) Consolidating daily memories into MEMORY.md, (2) Archiving old daily memories, (3) Extracting key facts from conversations, (4) Searching through memory history, (5) Setting up memory maintenance automation. Triggers on '长期记忆', 'memory consolidate', '记忆管理', '归档', 'MEMORY.md', '记忆压缩'."
---

# Long-Term Memory Management

Systematic management of MEMORY.md and daily memory files for persistent knowledge retention.

## Memory Architecture

```
~/.openclaw/workspace/
├── MEMORY.md              # Long-term curated memory (main)
├── memory/                # Daily memory files
│   ├── 2025-01-20.md
│   ├── 2025-01-21.md
│   └── ...
└── .memory-archive/       # Archived memories
    └── 2025-01/
        ├── consolidated.md
        └── raw/
```

## Quick Commands

```bash
# Consolidate recent daily memories
python3 {baseDir}/scripts/memory_manager.py --consolidate --days 7

# Archive old memories
python3 {baseDir}/scripts/memory_manager.py --archive --older-than 30

# Extract key facts from MEMORY.md
python3 {baseDir}/scripts/memory_manager.py --extract-facts

# Search memory history
python3 {baseDir}/scripts/memory_manager.py --search "关键词"

# Generate memory summary
python3 {baseDir}/scripts/memory_manager.py --summary --output memory-summary.md

# Health check
python3 {baseDir}/scripts/memory_manager.py --health
```

## MEMORY.md Management

### Structure

MEMORY.md should contain distilled, long-term knowledge:

```markdown
# MEMORY.md - Long-Term Memory

## User Profile
- Name: ...
- Preferences: ...
- Work patterns: ...

## Key Decisions
- [Date] Decision: Reasoning...

## Important Facts
- Account: location...
- Credentials: stored in...
- Recurring tasks: ...

## Lessons Learned
- Pattern: Insight...

## Active Projects
- Project A: Status, next steps...

## Recurring Context
- Weekly meetings: ...
- Regular reports: ...
```

### Consolidation Workflow

1. **Review daily memories** (last 7 days)
2. **Extract significant items**:
   - User preferences mentioned
   - Important decisions made
   - New facts discovered
   - Lessons learned
   - Active project updates
3. **Update MEMORY.md** with distilled content
4. **Archive processed daily files**

```bash
# Full consolidation workflow
python3 {baseDir}/scripts/memory_manager.py --consolidate --auto-archive
```

### What to Keep in MEMORY.md

| Keep | Don't Keep |
|------|------------|
| User preferences | Temporary states |
| Key decisions | Daily trivia |
| Important facts | Transient data |
| Lessons learned | Detailed logs |
| Active projects | Heartbeat checks |
| Recurring patterns | One-time events |
| Credentials locations | OAuth URLs |

## Daily Memory Files

### Purpose

`memory/YYYY-MM-DD.md` files capture:
- What happened today
- Important conversations
- Decisions made
- Tasks completed
- Context for future reference

### Best Practices

**DO:**
```markdown
# 2025-01-20

## Key Events
- User asked about X, decided Y
- Set up new integration Z
- Discovered preference for concise responses

## Decisions
- Use tool X instead of Y for Z task (user preference)

## Pending
- Follow up on ...
```

**DON'T:**
```markdown
# 2025-01-20

Got message. Replied HEARTBEAT_OK.
User said hi. Said hi back.
Time is 3pm.
```

### Automatic Extraction

The system can extract valuable content:

```bash
# Extract what matters from daily files
python3 {baseDir}/scripts/memory_manager.py --extract --from "2025-01-20.md"

# Output: List of extractable facts
```

## Archival System

### Archive Threshold

Default: Archive daily memories older than 30 days

```bash
# Archive old memories
python3 {baseDir}/scripts/memory_manager.py --archive --older-than 30

# Archive with consolidation
python3 {baseDir}/scripts/memory_manager.py --archive --older-than 30 --consolidate-first
```

### Archive Structure

```
.memory-archive/
├── 2025-01/
│   ├── consolidated.md    # Summary of the month
│   └── raw/               # Original daily files
│       ├── 2025-01-01.md
│       └── ...
└── 2025-02/
    └── ...
```

### Retrieval from Archive

```bash
# Search archived memories
python3 {baseDir}/scripts/memory_manager.py --search "keyword" --include-archive

# Retrieve specific archived content
python3 {baseDir}/scripts/memory_manager.py --retrieve "2025-01-15"
```

## Memory Compression

### What Gets Compressed

Daily memories contain repetition and noise. Compression extracts:

1. **Unique events** - Things that happened once
2. **Recurring patterns** - Things that repeat
3. **Key decisions** - Choices made
4. **Important facts** - Persistent information

### Compression Rules

```bash
# Compress with custom rules
python3 {baseDir}/scripts/memory_manager.py --compress \
  --rules keep-decisions,keep-preferences,keep-facts \
  --remove heartbeets,trivial,transient
```

### Example Compression

**Before (daily files, 5000 words):**
```markdown
# 2025-01-20
User asked about API. Looked up docs. Found answer.
User preferred concise response. Noted preference.
...

# 2025-01-21
User asked about API again. Provided concise answer.
User appreciated brevity.
...
```

**After (MEMORY.md, 100 words):**
```markdown
## User Preferences
- Prefers concise responses over detailed explanations

## Knowledge
- API documentation location: ...

## Lessons
- Concise answers are preferred for API questions
```

## Memory Search

### Search Commands

```bash
# Search all memories
python3 {baseDir}/scripts/memory_manager.py --search "关键词"

# Search specific range
python3 {baseDir}/scripts/memory_manager.py --search "..." --from 2025-01-01 --to 2025-01-31

# Search with context
python3 {baseDir}/scripts/memory_manager.py --search "..." --context 3

# Search archives too
python3 {baseDir}/scripts/memory_manager.py --search "..." --include-archive
```

### Search Output

```json
{
  "query": "关键词",
  "results": [
    {
      "date": "2025-01-20",
      "file": "memory/2025-01-20.md",
      "line": 15,
      "context": "...",
      "relevance": "high"
    }
  ],
  "total": 3
}
```

## Integration with Vector Memory

This skill works alongside vector memory (LanceDB):

| System | Purpose | Retention |
|--------|---------|-----------|
| MEMORY.md | Curated long-term memory | Permanent |
| memory/YYYY-MM-DD.md | Daily logs | 30 days → archive |
| Vector memory (LanceDB) | Semantic search | Variable |

### Coordination

```bash
# Consolidate both systems
python3 {baseDir}/scripts/memory_manager.py --consolidate --sync-vector

# The script will:
# 1. Update MEMORY.md
# 2. Archive old daily files
# 3. Sync key facts to vector memory
```

## Automation

### Periodic Consolidation

Add to heartbeat or cron:

```yaml
# HEARTBEAT.md
- Run memory consolidation weekly
- Archive memories older than 30 days
- Sync to vector memory
```

Or via cron:

```bash
# Weekly consolidation (Sunday 4am)
cron action=add job='{
  "name": "memory-consolidation",
  "schedule": "0 4 * * 0",
  "text": "Consolidate weekly memories: 1) Review memory/ files 2) Update MEMORY.md 3) Archive old files 4) Sync to vector memory"
}'
```

### Automated Extraction

During heartbeats, automatically extract:

```bash
python3 {baseDir}/scripts/memory_manager.py --auto-extract --days 1
```

## Memory Health

### Health Metrics

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Daily files count | <30 | 30-60 | >60 |
| MEMORY.md size | <50KB | 50-100KB | >100KB |
| Archive coverage | >90% | 50-90% | <50% |
| Last consolidation | <7 days | 7-14 days | >14 days |

### Health Check

```bash
python3 {baseDir}/scripts/memory_manager.py --health

# Output
```

```json
{
  "status": "healthy",
  "metrics": {
    "daily_files": 15,
    "memory_md_size": "12KB",
    "last_consolidation": "2025-01-18",
    "archive_coverage": "95%"
  },
  "recommendations": []
}
```

### Cleanup

```bash
# Clean up stale content
python3 {baseDir}/scripts/memory_manager.py --cleanup

# Remove duplicates
python3 {baseDir}/scripts/memory_manager.py --dedupe

# Reorganize structure
python3 {baseDir}/scripts/memory_manager.py --reorganize
```

## Best Practices

### Writing to MEMORY.md

1. **Be concise** - Distill, don't copy
2. **Use structure** - Consistent sections
3. **Date important items** - When did this become true?
4. **Review periodically** - Remove outdated info
5. **One concept per line** - Easy to search

### Managing Daily Files

1. **Write daily** - Capture what matters
2. **Skip trivial** - No heartbeat logs
3. **Link related** - Reference other files
4. **Mark important** - Use clear headings
5. **Archive promptly** - Don't accumulate

### Integration with Other Skills

```bash
# Use with self-evolution
python3 {baseDir}/scripts/memory_manager.py --consolidate
python3 ../self-evolution/scripts/evolution.py --analyze --with-memory

# Use with self-improvement
# Log a learning, then consolidate
python3 {baseDir}/scripts/memory_manager.py --extract-from .learnings/LEARNINGS.md
```

## Workflow Examples

### Weekly Maintenance

```bash
# 1. Check health
python3 {baseDir}/scripts/memory_manager.py --health

# 2. Consolidate recent memories
python3 {baseDir}/scripts/memory_manager.py --consolidate --days 7

# 3. Archive old files
python3 {baseDir}/scripts/memory_manager.py --archive --older-than 30

# 4. Sync to vector memory
python3 {baseDir}/scripts/memory_manager.py --sync-vector

# 5. Generate report
python3 {baseDir}/scripts/memory_manager.py --summary
```

### After Important Session

```bash
# Extract key facts immediately
python3 {baseDir}/scripts/memory_manager.py --extract --today

# Update MEMORY.md
python3 {baseDir}/scripts/memory_manager.py --update --section "Key Decisions" --add "..."
```

### Research Task

```bash
# Search all memories for context
python3 {baseDir}/scripts/memory_manager.py --search "项目名" --include-archive --context 5

# Export relevant memories
python3 {baseDir}/scripts/memory_manager.py --export "项目名" --output project-context.md
```

## Notes

- MEMORY.md is for main sessions only (not group chats)
- Daily files should be raw logs, not polished documents
- Archiving preserves data, just moves it out of active view
- Consolidation is distillation, not summarization
- The goal: quick recall of important information
