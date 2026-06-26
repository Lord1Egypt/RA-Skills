# session-recall

[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![python](https://img.shields.io/badge/python-3.10%2B-blue)](#requirements)
[![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)](#requirements)
[![openclaw](https://img.shields.io/badge/openclaw-skill-purple)](https://github.com/openclaw/openclaw)

**Give your AI agents memory across sessions.**

When an OpenClaw session rotates, agents lose all prior conversation context. A user says "continue where we left off" and the agent draws a blank. session-recall fixes this — it's a lightweight search tool that lets agents find and recover past conversations on their own.

No embeddings. No vector database. No LLM calls. Just fast text search over session transcript files, returning file paths and line numbers so the agent can read exactly what it needs.

## The Problem

```
User: So based on what we discussed, how should we proceed?
Agent: I don't have context for what we discussed — could you remind me?
```

This happens every time a session resets. The conversation history is right there on disk as JSONL files, but the agent has no way to search it.

## The Solution

session-recall gives agents two commands:

- **`list`** — Browse recent sessions with previews (time range, turn count, first message)
- **`search`** — Find specific keywords across all past transcripts

The agent gets back file paths and line numbers, reads the relevant lines, and continues the conversation as if the session never broke.

```
User: So based on what we discussed, how should we proceed?
Agent: [searches transcripts → finds the previous session → reads context]
Agent: Right, we were evaluating Option B. Based on the risk analysis...
```

## How It Works

```
session-recall list --start 48h
```
```
/path/to/abc123.jsonl  [03-08 02:15 ~ 03:35]  32 turns  "Can you look into the impact of..."
/path/to/def456.jsonl  [03-07 20:08 ~ 22:50]  67 turns  "What do you think about the proposal..."
```

```
session-recall search "risk analysis" --start 7d
```
```
/path/to/abc123.jsonl:142  [03-08 02:15] user: ...the risk analysis shows three main concerns...
/path/to/abc123.jsonl:158  [03-08 02:17] assistant: ...based on the risk analysis, Option B has...
```

The agent then uses `read --offset 142 --limit 30` to load the surrounding context.

## Features

- **Flexible time filtering** — relative (`6h`, `2d`, `1w`, `3mo`), absolute (`2026-03-01`, `03-01`), keywords (`today`, `yesterday`), or date ranges (`--start 2026-02-01 --end 2026-02-28`)
- **Pagination** — `--limit` and `--offset` for browsing through large result sets
- **Multi-agent support** — search your own sessions or other agents' sessions with `--agent`
- **Agent discovery** — `session-recall agents` lists all available agent IDs
- **Zero dependencies** — pure Python 3, no pip install needed
- **Zero LLM cost** — plain text search, runs in milliseconds

## Installation

### For humans

1. Copy the `session-recall` folder into your OpenClaw skills directory:

```bash
# Clone the repo
git clone https://github.com/hchen13/session-recall.git

# Copy to your skills directory
cp -r session-recall ~/.openclaw/skills/session-recall
```

2. That's it. OpenClaw auto-discovers skills from `~/.openclaw/skills/`. Your agents will pick it up on their next session.

### For AI agents

> **If you're an AI agent reading this because your user asked you to install this skill:**
>
> 1. Clone or download this repository
> 2. Copy the entire `session-recall` directory (containing `SKILL.md` and `scripts/`) to `~/.openclaw/skills/session-recall`
> 3. Verify the structure looks like this:
>    ```
>    ~/.openclaw/skills/session-recall/
>    ├── SKILL.md          ← OpenClaw reads this to know when to activate the skill
>    └── scripts/
>        └── session-recall.py   ← The search tool you'll call via exec
>    ```
> 4. Test it works: `python3 ~/.openclaw/skills/session-recall/scripts/session-recall.py agents`
> 5. The skill will be available in your next session (or after a session reset). You don't need to restart the gateway.
>
> **How to find your agent ID:** Look at your session key in the system prompt — it follows the pattern `agent:<YOUR_ID>:...`. Or run the `agents` subcommand to list all available IDs.
>
> **When to use this skill:** If a user's message assumes context you don't have (they reference past conversations, topics, or decisions that aren't in your current session), search your transcripts before asking them to repeat themselves. Read the `SKILL.md` for full usage details.

## Usage

### Commands

```bash
# List all available agents
python3 scripts/session-recall.py agents

# List recent sessions for an agent
python3 scripts/session-recall.py list --agent myagent --start 48h

# Search for a keyword
python3 scripts/session-recall.py search "deployment plan" --agent myagent --start 7d

# Search within a specific date range
python3 scripts/session-recall.py search "budget" --start 2026-02-01 --end 2026-02-28

# Paginate through results
python3 scripts/session-recall.py list --start 30d --limit 10 --offset 10
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `--agent` | Agent ID to search. Omit to search all agents. |
| `--start` | Start of time window. Durations (`6h`, `2d`), dates (`2026-03-01`), or keywords (`today`). |
| `--end` | End of time window. Same formats. Omit for "up to now". |
| `--limit` | Max results per page (default: 20 for list, 30 for search). |
| `--offset` | Skip N results for pagination (default: 0). |

## Requirements

- Python 3.10+
- [OpenClaw](https://github.com/openclaw/openclaw) (session transcripts stored as JSONL in `~/.openclaw/agents/`)

## How Agents Use It

The `SKILL.md` file tells OpenClaw when to activate this skill. When an agent detects that the user is referencing a previous conversation, the typical workflow is:

1. Run `list` to browse recent sessions and find candidates
2. Run `search` with keywords to narrow down specific mentions
3. Use `read` (the agent's built-in file reading tool) to load context from the returned line numbers
4. Continue the conversation with the recovered context

The skill triggers automatically — agents don't need to be told to use it. The `SKILL.md` description includes trigger conditions that OpenClaw matches against the conversation.

## License

MIT
