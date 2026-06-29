# Pi RPC Mode

`pi --mode rpc` — Embed the agent via stdin/stdout JSONL protocol.

## Frame Protocol

- Strict LF (`\n`) as the sole record delimiter
- Clients must split only on `\n`, no Unicode delimiters (e.g. Node readline is incompatible)
- Optional `id` field for request/response correlation
- Response: `{"type":"response", "command":"...", "success":true, "data":{...}}`
- Event: `{"type":"agent_start", ...}` (continuously pushed, no id field)

## Command List

| Command | Description |
|---------|-------------|
| `prompt` | Send prompt `{ message, images?, streamingBehavior? }` |
| `steer` | Steering message (insert while running) `{ message }` |
| `follow_up` | Follow-up message (insert after completion) `{ message }` |
| `abort` | Abort current operation |
| `new_session` | New session `{ parentSession? }` |
| `get_state` | Get session state |
| `get_messages` | Get all messages |
| `set_model` | Switch model `{ provider, modelId }` |
| `cycle_model` | Cycle to next model |
| `get_available_models` | List all available models |
| `set_thinking_level` | Set thinking level `{ level }` |
| `cycle_thinking_level` | Cycle thinking level |
| `set_steering_mode` | `"one-at-a-time"` or `"all"` |
| `set_follow_up_mode` | `"one-at-a-time"` or `"all"` |
| `compact` | Manual compaction `{ customInstructions? }` |
| `set_auto_compaction` | `{ enabled }` |
| `set_auto_retry` | `{ enabled }` |
| `abort_retry` | Abort retry |
| `bash` | Execute command `{ command }` |
| `abort_bash` | Abort bash |
| `get_session_stats` | Get token/cost/context stats |
| `export_html` | Export HTML `{ outputPath? }` |
| `switch_session` | Load another session `{ sessionPath }` |
| `fork` | Fork from message `{ entryId }` |
| `clone` | Copy current branch to new session |
| `get_fork_messages` | Get forkable messages |
| `get_last_assistant_text` | Get last assistant reply |
| `set_session_name` | Set session name `{ name }` |
| `get_commands` | Get all extension commands/prompts/skills |

## Event Stream

| Event | Description |
|-------|-------------|
| `agent_start` / `agent_end` | Agent cycle |
| `turn_start` / `turn_end` | Single LLM call cycle |
| `message_start` / `message_update` / `message_end` | Message stream |
| `tool_execution_start/update/end` | Tool execution |
| `queue_update` | Steering/follow-up queue changes |
| `compaction_start` / `compaction_end` | Compaction events |
| `auto_retry_start` / `auto_retry_end` | Auto retry |
| `extension_error` | Extension error |

assistantMessageEvent types in message_update:

- `start`, `text_start`, `text_delta`, `text_end` — text stream
- `thinking_start`, `thinking_delta`, `thinking_end` — reasoning
- `toolcall_start`, `toolcall_delta`, `toolcall_end` — tool calls
- `done` (reason: "stop"/"length"/"toolUse")
- `error` (reason: "aborted"/"error")

## Image Format

```json
{"type": "prompt", "message": "What's this?", "images": [
  {"type": "image", "data": "<base64>", "mimeType": "image/png"}
]}
```

## Bash Command Results

Bash output is stored as `BashExecutionMessage` in agent state and sent to the LLM as a UserMessage on the next prompt.