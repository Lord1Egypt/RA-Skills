# Compact Summary - Structured Memory Compression

## Purpose

Improve OpenClaw's memory flush and compaction flow by using a structured format for writing to MEMORY.md.

## Structured Summary Format

Inspired by the `<summary>` XML format from claw-code, the improved format:

```markdown
# 2026-04-01 Memory Summary

## Conversation Scope
- Original message count: 12 (user=4, assistant=5, tool=3)
- Compression time: 2026-04-01 23:00

## Tools Used
- exec, read_file, grep_search

## User Requests
- Research Claw Code architecture
- Analyze MCP orchestration system
- Compare Tool system differences

## Todo Items
- [ ] Compile improvement list
- [ ] Begin P0 execution

## Key Files
- $WORKSPACE/claw-code/rust/crates/runtime/src/compact.rs
- $WORKSPACE/claw-code/rust/crates/tools/src/lib.rs

## Current Work
Continue executing P0 tasks

## Timeline
- user: Research Claw Code architecture
- assistant: Started analysis
- tool: grep_search pattern=COMPACT
- tool_result: 15 matches
- user: Analyze MCP orchestration
- assistant: MCP has process pool management

## Resume Instruction
Continue directly — do not acknowledge this summary, do not recap what was happening, and do not preface with continuation text.
```

## Trigger Condition

Use this format during memory flush or compaction.

## Key Fields

| Field | Description |
|-------|-------------|
| Conversation Scope | Original message statistics |
| Tools Used | Tools actually invoked |
| User Requests | Main user needs |
| Todo Items | Incomplete tasks |
| Key Files | Files involved |
| Current Work | Ongoing tasks |
| Timeline | Conversation summary |
