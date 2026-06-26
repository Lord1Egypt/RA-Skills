# System Memory vs Agent Memory Fragments

Two separate storage systems — do NOT confuse them.

| | System Memory (memory tool) | Agent Memory Fragments |
|:---|:---|:---|
| **Tool** | `memory()` | `write_file()` to Obsidian vault |
| **Location** | Hermes internal | `D:\App\Obsidian\RealGhost\agent memory\` |
| **Capacity** | ~2,200 chars total | No practical limit (filesystem) |
| **Format** | Compact text entries | Full `.md` files with frontmatter |
| **Survives reboot** | Yes | Yes |
| **User visible** | No (injected as context) | Yes (editable notes in Obsidian) |
| **What it stores** | Preferences, environment, user profile | Session decisions, root causes, lesson learned |

## When to Use Which

- **System memory**: durable facts about the user/environment that should always be in context. Preferences, tool quirks, project conventions. Keep under 2,200 chars.
- **Agent memory fragments**: session-specific findings, root cause analyses, design decisions, rule updates. Not restricted by char limit.

## Pitfall

This session's bug: saw `memory tool at 2,093/2,200` → thought "storage is full" → skipped writing agent memory fragments. But they occupy different storage. One being full has zero impact on the other.

**Always treat them independently.** Full system memory → remove stale entries or replace. Full agent memory → doesn't apply (filesystem). The two never share a capacity constraint.

## Verification

After writing an agent memory fragment, verify it exists:
```
search_files path=D:\App\Obsidian\RealGhost\agent memory pattern="<keyword>" target=files
```
