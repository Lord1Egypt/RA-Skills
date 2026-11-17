---
name: herder-telegram
description: "Drive Herdr terminal multiplexer panes from Telegram: spawn a dedicated tab, send prompts to any CLI agent, wait for done/blocked, and relay transcripts back."
---

# Herder Telegram

Use the [Herdr](https://github.com/mentholmike/herdr) terminal multiplexer to spawn CLI agents (Kimi, Claude Code, aider, etc.) in dedicated panes from Telegram, then relay prompts, progress, and results back to the chat.

This agent runs outside Herdr (launched by the OpenClaw gateway, not inside a pane), so `HERDR_ENV` is unset and `HERDR_*` IDs are unavailable. Never use `--current`; it does not apply to this caller. Always resolve explicit pane and tab IDs from JSON responses.

Use when:

- user asks to run, prompt, or steer a CLI agent from Telegram
- user asks for the output, status, or a screenshot of a Herdr pane
- user asks to be notified when a pane agent finishes or needs input
- user sends `shot`, `tail`, or `status` for a running Herdr-driven task

## Prerequisites

Install Herdr and make sure `herdr` is on a PATH that the OpenClaw gateway process can resolve. If the gateway has a minimal PATH, use the absolute path to the binary in your commands.

```bash
which herdr          # interactive shell
ls -l $(which herdr) # absolute path if needed
```

## Contract

- Drive only panes and tabs this skill spawned, unless the user explicitly names a pane ID. The user's interactive panes are off limits by default; injecting text into them disrupts their work and is a prompt-injection vector.
- Always pass `--no-focus` on creates and splits. Never steal the user's terminal focus.
- Parse every ID from the JSON response of the call that created or listed it. Never construct an ID from a workspace number, tab number, or sidebar position. Treat IDs like `w5:t8` and `w5:pF` as opaque strings; suffixes vary in length.
- Inspect before waiting: `herdr pane read` current output first, then `herdr wait` for the next expected state. A wait timeout exits 1; on timeout, re-read the pane before deciding anything.
- Treat `idle` and `done` both as "finished." The difference is only whether the result was seen on screen.
- Treat `blocked` as "needs the user": relay what the agent is asking and forward the user's reply with `pane run`.
- Never run `herdr server stop`, and never close workspaces, tabs, or panes this skill did not create. Clean up your own tab when the user says the task is done.
- `pane run` sends text plus Enter together. Use it for prompts and replies; do not coordinate `send-text` and `send-keys` separately except for control keys like Escape.

## Environment

| Tool | Notes |
|------|-------|
| `herdr` | v0.7.x or later; control commands print JSON |
| agent binary | e.g. `kimi`, `claude`, `aider` — whatever the user has installed |

If `herdr` is not on the gateway's PATH, retry with the absolute path to the binary. Same for the chosen agent binary.

## Discover State

```bash
herdr workspace list
herdr tab list --workspace <workspace_id>
herdr pane list --workspace <workspace_id>
herdr pane get <pane_id>
```

`pane get` reports `agent` (e.g. `kimi`) and `agent_status` (`idle`, `working`, `blocked`, `done`, `unknown`). `unknown` means no agent has been detected in the pane yet — normal right after spawn.

## Spawn a Dedicated Tab

Default to one labeled tab in the active workspace, holding one agent pane. Do not create a new workspace unless the user asks.

```bash
herdr tab create --workspace <active_workspace_id> --label telegram --no-focus
```

Read `result.tab.tab_id` (or the pane ID embedded in the response) from the JSON. If the response carries no pane ID, list panes for that tab:

```bash
herdr pane list --workspace <workspace_id>
```

Label the pane, then launch the agent's interactive TUI by running only its normal executable:

```bash
herdr pane rename <pane_id> "tg-agent"
herdr pane run <pane_id> "<agent-binary>"
herdr wait agent-status <pane_id> --status idle --timeout 60000
```

For a second agent in the same tab, split instead of creating another tab:

```bash
herdr pane split <pane_id> --direction right --no-focus
```

Do not pass the task as argv to the agent, and do not add unattended auto-approval flags unless the user explicitly asks for them; the default is interactive approval, which surfaces as `blocked` and gets relayed (see below). If the user does ask for an unattended run, say plainly that auto-approval is on for that pane.

## Submit the Task and Relay

Send the user's prompt once the agent is idle:

```bash
herdr pane run <pane_id> "<user's prompt>"
herdr wait agent-status <pane_id> --status working --timeout 30000
```

Then wait for an outcome. Keep each wait under the gateway turn budget (agents.defaults.timeoutSeconds is 600, so use ~480000 ms max) and loop if the task runs longer:

```bash
herdr wait agent-status <pane_id> --status done --timeout 480000
```

On completion, read the transcript tail and relay it:

```bash
herdr pane read <pane_id> --source recent-unwrapped --lines 120
```

On `blocked`, read the visible viewport to see what the agent is asking, send it to the user verbatim with a short prefix like `<agent> is waiting for input:`, and forward their reply:

```bash
herdr pane read <pane_id> --source visible --lines 40
herdr pane run <pane_id> "<user's reply>"
```

On wait timeout, check `pane get`: still `working` means keep waiting; `unknown` means the agent was not detected — read the pane to see what actually happened before reporting failure.

## Read Sources and Visibility Commands

Pick the read source to match the job:

| Source | Returns | Use for |
|--------|---------|---------|
| `visible` | current rendered viewport | "screenshot" of the pane; seeing prompts/menus |
| `recent` | recent scrollback as rendered, soft-wrapped | short recent context |
| `recent-unwrapped` | recent scrollback, wraps joined | transcripts, logs, final answers — default |
| `detection` | bottom-buffer snapshot | debugging agent detection only |

User commands to honor while a task runs:

- `shot` — `pane read --source visible --lines 40`, send as a code block. This is the closest thing to seeing the pane live.
- `tail [N]` — `pane read --source recent-unwrapped --lines N` (default 60), send as a code block.
- `status` — report `agent_status`, pane label, and one line on what it is doing.
- `stop` — `herdr pane send-keys <pane_id> Escape` to interrupt the agent, then confirm with a `shot`.
- any other text — forward to the pane with `pane run` as a follow-up prompt.

## Telegram Formatting

- Wrap pane output in fenced code blocks; it is terminal text, not Markdown.
- Telegram messages cap at 4096 characters. Chunk long transcripts on line boundaries; for very long output, send the tail plus a one-line summary and offer more.
- Strip ANSI if it leaks through (default `--format text` already does); never relay `--format ansi` raw.
- For long tasks, prefer milestone messages over spam: tell the agent in the prompt to announce phase completions, then `herdr wait output <pane_id> --match "<marker>" --timeout 480000` and relay each marker. If the channel supports message edits, a single edited progress message (polled every 60-90s from `visible`) is the low-noise alternative.

## Headless Alternative

For one-shot questions with no need to watch or steer, skip Herdr and run the agent non-interactively, relaying stdout directly:

```bash
<agent-binary> -p "<question>"
```

Prefer the pane flow when the user wants a persistent session, follow-ups, live visibility in the terminal, or several agents coordinated at once. Prefer headless when the request is a single self-contained question and speed matters.

## Cleanup

When the user confirms the task is finished, close what this skill created:

```bash
herdr tab close <tab_id>
```

If the user wants the session kept (to scroll it in the terminal later), rename the tab to note it is done and leave it.

## Final Report

Include:

- pane/tab IDs used and their labels
- the prompt submitted and the final status (`done` / `blocked` / interrupted)
- the result: transcript tail for short answers, summary plus offer of `tail` for long ones
- anything forwarded to the pane on the user's behalf, and whether the tab was closed or kept
