# Pi Compaction & Session Format

## Auto Compaction

Trigger: `contextTokens > contextWindow - reserveTokens`
Defaults: `reserveTokens = 16384`, `keepRecentTokens = 20000`

Process:
1. Walk backwards from newest message, accumulating tokens until reaching keepRecentTokens
2. Collect messages between the cut point and the last kept boundary
3. LLM generates a structured summary (with iterative context)
4. Save CompactionEntry; on reload, rebuild context from summary + kept messages

### Structured Summary Format

```
## Goal
[User goal]

## Constraints & Preferences
- [User requirements]

## Progress
### Done
- [x] [Completed]

### In Progress
- [ ] [In progress]

### Blocked
- [Issue]

## Key Decisions
- **[Decision]**: [Rationale]

## Next Steps
1. [Next step]

## Critical Context
- [Key data]

<read-files>
path/to/file.ts
</read-files>

<modified-files>
path/to/changed.ts
</modified-files>
```

Tool results truncated to 2000 characters.

### Split Turn

When a single turn exceeds keepRecentTokens, split at an assistant message boundary, generating two summaries (history summary + turn prefix summary).

### Branch Summary

When navigating via /tree, abandoned branches are auto-summarized and attached to the new position.

## Custom Compaction (Extension)

```ts
import { convertToLlm, serializeConversation } from "@earendil-works/pi-coding-agent";

pi.on("session_before_compact", async (event, ctx) => {
  const { preparation } = event;
  // preparation.messagesToSummarize, .turnPrefixMessages, .previousSummary, .fileOps

  const text = serializeConversation(convertToLlm(preparation.messagesToSummarize));
  const summary = await myModel.summarize(text);

  return { compaction: { summary, firstKeptEntryId: preparation.firstKeptEntryId, tokensBefore: preparation.tokensBefore } };
});

pi.on("session_before_tree", async (event, ctx) => {
  // preparation.targetId, .oldLeafId, .commonAncestorId, .entriesToSummarize
  return { cancel: true }; // or { summary: { summary, details } }
});
```

## Session JSONL Format

```
~/.pi/agent/sessions/--<path>--/<timestamp>_<uuid>.jsonl
```

Version: v3 (id/parentId tree structure)

### Entry Types

| type | Description | Special Fields |
|------|-------------|----------------|
| `session` | File header | version, id, cwd, parentSession? |
| `message` | Message | message (AgentMessage) |
| `model_change` | Model switch | provider, modelId |
| `thinking_level_change` | Thinking switch | thinkingLevel |
| `compaction` | Compaction | summary, firstKeptEntryId, tokensBefore |
| `branch_summary` | Branch summary | summary, fromId |
| `custom` | Extension state | customType, data (not fed to LLM) |
| `custom_message` | Extension message | customType, content, display (fed to LLM) |
| `label` | Bookmark | targetId, label |
| `session_info` | Session metadata | name |

### AgentMessage Union

```
UserMessage | AssistantMessage | ToolResultMessage | BashExecutionMessage | CustomMessage | BranchSummaryMessage | CompactionSummaryMessage
```

- `BashExecutionMessage`: command, output, exitCode, cancelled, truncated
- `CustomMessage`: customType, content, display, details

### SessionManager API Quick Reference

- Create: `SessionManager.create(cwd)`, `.open(path)`, `.continueRecent(cwd)`, `.inMemory()`, `.forkFrom()`
- List: `.list(cwd)`, `.listAll()`
- Append: `.appendMessage()`, `.appendCompaction()`, `.appendCustomEntry()`, `.appendLabelChange()`
- Navigate: `.getLeafId()`, `.getTree()`, `.branch(id)`, `.branchWithSummary()`
- Context: `.buildSessionContext()` → messages, thinkingLevel, model