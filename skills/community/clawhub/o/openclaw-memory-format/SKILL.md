# Memory Format - Memory Format Guide

## Overview

OpenClaw's memory system uses multi-layered storage combining semantic and keyword search.

## Memory Layers

### 1. MEMORY.md (Long-term Memory)
- Manually maintained core memory
- Loaded into system prompt on startup
- Human-readable and editable
- Path: `$WORKSPACE/MEMORY.md`

### 2. memory/YYYY-MM-DD.md (Daily Memory)
- Auto-written by memory flush
- Triggered when context is full
- Appended to the day's date file
- Path: `memory/YYYY-MM-DD.md`

### 3. Session Memory
- Only visible in current session
- Auto-cleared after session ends

## Improved Daily Memory Format

Use structured format for easy later retrieval:

```markdown
# 2026-04-01 Daily Memory

## Completed Today
- Researched Claw Code architecture
- Completed MCP orchestration analysis
- Started P0 improvement tasks

## Conversation Summary
- User request: Full analysis of OpenClaw vs Claw-Code
- Systems involved: Tool/Session/MCP/API/Hook/Plugin/Prompt/Skill/Memory/Sandbox/Error
- Output: Complete improvement list (22 items)

## Key Decisions
- MCP process pool needs core modification, P3
- Tool Schema supplements added to TOOLS.md
- Hook examples library created

## Follow-up Items
- [ ] Execute P0 tasks 1-6
- [ ] Verify improvement effects
- [ ] Continue P1 tasks

## Important Files
- $WORKSPACE/MEMORY.md
- $WORKSPACE/claw-code/ (cloned claw-code repository)

## Technical Notes
- Hybrid search: vector 70% + text 30%
- Compaction threshold: 4k tokens reserved space
- Sandbox: Docker network=none, capDrop=ALL
```

## Memory Search

### memory_search tool
```
Use semantic search to find relevant memories:
- Returns 6 results by default
- minScore: 0.35
- Supports hybrid search mode
```

### memory_get tool
```
Read specific memory files:
- path: file path (MEMORY.md or memory/YYYY-MM-DD.md)
- from: start line
- lines: line limit
```

## Flush Triggers

| Condition | Threshold |
|-----------|-----------|
| softThresholdTokens | 4000 tokens reserved space |
| forceFlushTranscriptBytes | 2MB force flush |
| reserveTokensFloor | 20000 tokens floor |

## Best Practices

1. **Daily summary**: Write end-of-day summary
2. **Structured**: Use headings, sections, lists
3. **Searchable**: Include keywords for search
4. **Not excessive**: Only write important, long-term memories
5. **Periodic cleanup**: Distill daily → MEMORY.md

## Difference from Compact

| | Memory Flush | Compaction |
|--|-------------|-----------|
| Trigger | Context full | Context full |
| Write | memory/YYYY-MM-DD.md | No file write |
| Content | Important memories | Conversation summary |
| Format | Structured markdown | Internal summary |
