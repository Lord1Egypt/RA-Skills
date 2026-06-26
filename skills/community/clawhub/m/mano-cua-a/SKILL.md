---
name: mano-cua
description: Computer use for GUI automation tasks via VLA models. Use when the user describes a task in natural language that requires visual screen interaction and no API or CLI exists for the target app.
homepage: https://github.com/Mininglamp-AI/mano-skill
metadata: {"openclaw": {"emoji": "🖥️", "install": [{"id": "brew", "kind": "brew", "formula":"Mininglamp-AI/tap/mano-cua", "bins":["mano-cua"],"label": "Install mano-cua (brew)"}]}}
---

# mano-cua

Desktop GUI automation for tasks via VLA models. Use when the user describes a task in natural language that requires visual screen interaction and no API or CLI exists for the target app. Supports fully on-device local mode and cloud mode.

## Requirements

- A system with a **graphical desktop** (macOS / Windows / Linux)
- `mano-cua` binary installed

### Installation

**macOS / Linux (Homebrew):**

```bash
brew install Mininglamp-AI/tap/mano-cua
```

**Windows:**

Download the latest `mano-cua-windows.zip` from [GitHub Releases](https://github.com/Mininglamp-AI/mano-skill/releases), extract it, and add the folder to your `PATH`.

## Usage

```bash
# Run a task
mano-cua run "your task description"

# Run with options(minimize UI panel and set max steps)
mano-cua run "task" --minimize --max-steps 10

# Open a URL in the browser before starting the task
mano-cua run "task" --url "https://example.com"

# Open an app before starting the task (use the macOS app name, e.g. 'Notes', 'Safari', 'Google Chrome')
mano-cua run "task" --app "Notes"

# Run in local mode (on-device inference, macOS Apple Silicon only)
mano-cua run "task" --local

# Stop the current running task
mano-cua stop
```

Run `mano-cua --help` or `mano-cua <command> --help` for full flags and options.

> **Note:** Only one task can run at a time per device. If you need to start a new task, first stop the current one with `mano-cua stop`.

> **--app vs --url:** Use one or the other, not both. `--app` launches a desktop application by its macOS name (as shown in Spotlight search). `--url` opens a URL in the default browser. Both bring the target to the foreground before the agent starts.

> **Tip for local mode:** Write task descriptions with explicit step-by-step instructions for best results. For example, instead of "search for iphone on Xiaohongshu", write "click the search box at the top, type iphone, click the search button, then click the first result". Explicit steps significantly improve local model accuracy.

## Local Mode

Runs [Mano-P](https://huggingface.co/Mininglamp-2718/Mano-P) entirely on-device via MLX. No data leaves the machine. Requires macOS with Apple Silicon (M1+). Highly recommended to add `--url` or `--app` arg when using local mode to improve efficiency and accuracy. Without `--local`, the tool uses cloud inference.

**Setup:**

```bash
mano-cua check
mano-cua install-sdk
mano-cua install-model
```

**Run:**

```bash
mano-cua run "click the search box, type openai, click search, click the first result to open OpenAI homepage" --local --url "https://www.google.com"
mano-cua run "click the search box, type iphone, click the search button, open the first post" --local --url "https://www.xiaohongshu.com" --minimize --max-steps 15
mano-cua run "create a new note and type hello world" --local --app "Notes"
```

## Examples

```bash
# Local mode (recommended for privacy — all inference on-device, no data leaves the machine)
mano-cua run "click the search box, type openai, click search, click the first result" --local --url "https://www.google.com" --minimize
mano-cua run "create a new note and type hello world" --local --app "Notes"

# Cloud mode
mano-cua run "Open Notes and create a new note titled Meeting Summary"
mano-cua run "Search for AI news in the browser and show the first result" --minimize --max-steps 20

# Cloud mode with --app or --url
mano-cua run "Create a calendar event for Friday 20:00 named Team Meeting" --app "Microsoft Outlook"
mano-cua run "Compare available plans for the AeroAPI" --url "https://www.flightaware.com/"

# Stop the current task (use before starting a new one)
mano-cua stop
```

## How It Works

At each step, the current screen state is analyzed by a hybrid vision model to decide the next action. The agent performs bounded GUI actions (click, type, scroll, drag) only within the user-specified task scope, visible foreground target, and configured step/session limits. For sensitive or irreversible actions, the agent pauses and prompts the user for explicit confirmation before proceeding.

Hybrid vision model:
- **Mano-P model** — handles straightforward, lightweight tasks with rapid output.
- **Claude (vision analysis)** — handles complex tasks requiring deeper reasoning. In cloud mode, only the primary-display screenshot is sent transiently via HTTPS for the current inference step; no background monitoring occurs.

The system automatically selects the appropriate model based on task complexity.

In **local mode (`--local`)**, a local Mano-P model runs on-device via MLX. No network calls for inference.

**Structural capability boundaries (what the tool cannot do):**

- Cannot run in the background or persist between sessions — each invocation is a single, short-lived task.
- Cannot access the filesystem, clipboard, network, or any data beyond what is visible on the primary display.
- Cannot interact with secondary monitors — only the primary display is used.
- Cannot bypass OS-level permission dialogs or security prompts.
- Cannot execute shell commands, install software, or modify system settings.
- Cannot access stored passwords, tokens, cookies, or credential managers — it can only see and interact with what is visually rendered on screen.

## Status Panel

A small UI panel is displayed on the top-right corner of the screen to track and manage the current session status.

## Data, Privacy & Safety

- The user must explicitly describe the task before any action is taken. There is no background operation, no scheduled scanning, and no persistent connection.
- Sensitive or irreversible actions (making purchases, entering credentials, deleting data) trigger a confirmation prompt — the agent pauses and waits for explicit user approval before proceeding.
- Step count is capped via `--max-steps`, preventing runaway execution.
- The on-screen status panel displays every action in real-time; the user can stop immediately via the panel or `mano-cua stop`.
- The agent stops the moment the user intervenes with mouse/keyboard input or the session ends.
- Most actions performed are inherently reversible (clicking, scrolling, typing can be undone). For non-reversible actions, the confirmation mechanism described above applies.
- In cloud mode, primary-display screenshots are sent transiently for inference only during an active user-initiated session; no continuous recording, background monitoring, or credential-store access occurs.
- For privacy-sensitive tasks, **local mode (`--local`)** runs inference entirely on-device with zero network calls — no data ever leaves the machine.
- The agent has no programmatic access to application data, APIs, or internal state — it can only see what is visually rendered on screen and interact via standard mouse/keyboard input.
- It does not access stored passwords, tokens, cookies, session stores, keychains, or credential managers. No API keys or secrets are required or embedded.
- The scope is limited to what the user explicitly describes in the task — the agent does not navigate to unrelated apps or accounts on its own.
- When `--app` or `--url` is specified, the agent's interaction is focused on that specific application or webpage.
- The full source code is [open source on GitHub](https://github.com/Mininglamp-AI/mano-skill) under MIT-0 license. The Homebrew formula builds directly from tagged GitHub releases with verifiable checksums.
- All network calls are isolated in a single module ([`task_model.py`](https://github.com/Mininglamp-AI/mano-skill/blob/main/visual/model/task_model.py)) for easy auditing.
- The client identifies itself only with a locally generated device ID (`~/.myapp_device_id`) — no secrets are transmitted or stored remotely.

## Important Notes

- **Do not use the mouse or keyboard during the task.** Manual input while mano-cua is running may cause unexpected behavior.
- **Multiple displays:** only the primary display is used. All mouse movements, clicks, and screenshots are restricted to that display.

## Platform Support

macOS is the preferred and most tested platform. Adaptations for Windows and Linux are not yet fully completed — minor issues are expected.
