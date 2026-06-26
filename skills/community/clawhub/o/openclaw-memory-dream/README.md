# memory-dream

> Auto-consolidates agent memory files after sessions — like REM sleep for AI agents.

## What it does

As an AI agent accumulates sessions, its memory files can get cluttered: vague date references ("yesterday", "last week"), stale context that no longer applies, and contradictions where newer information superseded older entries but both remain.

**memory-dream** runs automatically in the background after enough sessions have passed and enough time has elapsed — like REM sleep. It uses the configured LLM to quietly clean up memory files, resolving contradictions, replacing vague date references with actual dates, removing stale entries, and preserving everything that still matters.

The consolidation is:
- **Non-blocking** — fires after session end, doesn't delay anything
- **Lock-safe** — won't run twice simultaneously, handles stale locks from crashed processes
- **Conservative** — the prompt instructs the LLM to keep everything important, not to summarize aggressively

## Install

```bash
openclaw plugins install openclaw-memory-dream
```

## Configuration

Add to your `openclaw.json` under `plugins.entries`:

```json
{
  "plugins": {
    "entries": {
      "memory-dream": {
        "enabled": true,
        "config": {
          "minSessions": 5,
          "minHours": 24,
          "memoryFiles": ["MEMORY.md"],
          "model": "claude-haiku-4-5"
        }
      }
    }
  }
}
```

| Option | Type | Default | Description |
|---|---|---|---|
| `minSessions` | `number` | `5` | Session boundaries since last consolidation before triggering |
| `minHours` | `number` | `24` | Hours since last consolidation before triggering |
| `memoryFiles` | `string[]` | `["MEMORY.md"]` | Memory files to consolidate (relative to workspace root) |
| `model` | `string` | *(agent default)* | Model override for consolidation LLM calls |
| `enabled` | `boolean` | `true` | Disable without uninstalling |

Both `minSessions` **and** `minHours` must be satisfied for consolidation to trigger.

> **Session detection in persistent channels:** In DM-style channels where there's no discrete session lifecycle (e.g. Slack DMs), the plugin detects session boundaries via inactivity gaps — a gap of 30+ minutes between messages counts as a new session. This matches the spirit of Claude Code's Auto Dream behavior.

## How it works

### Trigger conditions

After every session ends, the plugin increments a session counter stored in `{agentDir}/.memory-dream-state.json`. Consolidation fires when:

1. `sessionCount >= minSessions` — enough sessions have accumulated
2. `hoursSinceLastRun >= minHours` — enough time has passed (or this is the first run)
3. No lock file is held by a running process

### Consolidation process

1. Acquires a lock file at `{agentDir}/.memory-dream.lock` (PID + timestamp)
2. Reads each file in `memoryFiles` from the workspace root
3. Reads recent LCM (Lossless Context Management) summaries from `{agentDir}/lossless-claw/` for additional session context — **optional**, skipped gracefully if [lossless-claw](https://clawhub.ai) is not installed
4. Calls the LLM once per memory file with the consolidation prompt
5. Writes updated content back to each file
6. Resets session counter to 0, records timestamp and summary
7. Releases lock

### What the LLM is asked to do

- Replace vague date references ("yesterday", "last week") with actual dates based on context
- Remove entries that are clearly stale or superseded
- Resolve contradictions — keep the most recent/accurate version
- Preserve relationship history, decisions, and learned preferences
- Return only the updated file content — no commentary

### State file

The plugin maintains state at `~/.openclaw/memory-dream/<agentId>/.memory-dream-state.json` (one directory per agent, under the user's home directory — not in the workspace):

```json
{
  "sessionCount": 3,
  "lastRunAt": "2026-03-20T14:32:00.000Z",
  "lastRunStatus": "success",
  "lastRunSummary": "updated: MEMORY.md",
  "lastMessageAt": "2026-03-26T17:04:00.000Z"
}
```

The memory files themselves (e.g. `MEMORY.md`) are read from and written back to the **agent workspace root** (not the state directory).

### Lock file

`~/.openclaw/memory-dream/<agentId>/.memory-dream.lock` contains the PID of the consolidating process and a timestamp. On lock check, the PID is validated — stale locks from crashed processes are automatically cleared.

## Status tool

Use the built-in tool to check plugin state:

```
memory_dream_status
```

Returns session count, last run time, next trigger estimate, and whether consolidation is currently running.

## Contributing

Issues and PRs welcome at [github.com/mitchelldavis44/openclaw-memory-dream](https://github.com/mitchelldavis44/openclaw-memory-dream).

## License

MIT
