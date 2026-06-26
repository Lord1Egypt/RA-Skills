---
name: headless-terminal
description: Drive hostile or full-screen terminal UIs through the `ht` CLI from montanaflynn/headless-terminal. Use when an agent needs reliable PTY-backed interaction, screen snapshots, or wait/synchronization for tools like `vim`, `top`, `htop`, `git add -p`, SSH-driven TUIs, installers, auth prompts, or REPLs. Prefer this over plain shell I/O when redraw behavior, alternate screen handling, cursor state, or deterministic waits matter; fall back to exec/process or tmux for ordinary shell commands and human-operated sessions.
---

# Headless Terminal

## Overview

Use `ht` from <https://github.com/montanaflynn/headless-terminal> as the special-purpose tool for terminal programs that behave badly under plain stdin/stdout control. It gives a real PTY, terminal-state snapshots, and explicit wait conditions so the agent can drive a TUI without guessing when the screen settled.

Do not let the hammer make everything look like a nail. `ht` is powerful but heavyweight; if a normal command, pipe, `exec` with `pty=true`, or tmux session fits better, use that instead.

## Workflow

1. Confirm `ht` exists before committing to this path.
2. Decide whether the task actually needs `ht`; explicitly reject hammer/nail overuse and try simpler shell or host-agent primitives first when they fit.
3. Create a uniquely named session with `ht run`.
4. Send the smallest meaningful keystrokes.
5. Wait for a deterministic condition.
6. Snapshot with `ht view`.
7. Stop and remove the session when done, unless the user explicitly wants a persistent session.

## Choose `ht` vs other tools

Use `ht` when:
- a program needs a real tty and redraws the whole screen
- alternate-screen behavior matters
- cursor position or screen state matters
- the task needs reliable waits after keys are sent
- you want a text or PNG snapshot of the terminal state

Prefer `exec` / `process` when:
- the command is ordinary shell I/O
- output is line-oriented and does not depend on screen state
- no full-screen TUI is involved
- `exec` with `pty=true` is enough to satisfy a TTY check without needing screen snapshots

Prefer tmux when:
- a human will monitor or resume the session directly
- persistence and shared human visibility matter more than terminal snapshots

## Preflight

Check availability first:

```bash
command -v ht
```

If `ht` is missing, say so plainly and switch to another tool or ask whether to install it. The expected install source is Montana Flynn's headless-terminal:

```bash
brew install montanaflynn/tap/ht
```

Without Homebrew, use a release tarball from <https://github.com/montanaflynn/headless-terminal/releases> that matches the host OS/architecture, then put the `ht` binary on `PATH`.

Security/trust posture for publishing:
- Tap installs and release tarballs are still trust decisions; name the repo/owner explicitly.
- Prefer the tap or release artifacts over random packages or copy-pasted scripts.
- If a user is security-sensitive, suggest reviewing the GitHub repo and release page before installation.
Important disambiguation: not every package named `ht` or `headless-terminal` is this CLI. On macOS/Homebrew, the core formula `ht` refers to HTE, a viewer/editor/analyzer for executables, not this terminal automation tool. The public npm package `headless-terminal` is an old library and may not provide the expected `ht run` / `ht send` CLI. Do not install either as a guess; verify that the candidate explicitly supports the commands this skill uses.

## Core commands

```bash
ht run --name demo-$(date +%s) <cmd...>
ht send demo "keys..." --wait-idle 200ms --view
ht view demo
ht view demo --format png > screenshot.png
ht wait demo --wait-text "READY"
ht stop demo
ht remove demo
```

Treat command names and flags as version-sensitive. If `ht --help` is available, check it before relying on less-common flags such as PNG output or cursor waits.

## Waiting strategy

This is the main reason to use `ht`.

Prefer, in order:
1. `--wait-text` when a known string should appear
2. `--wait-cursor` when the cursor position is predictable
3. `--wait-idle` when the app redraws and then settles
4. `--wait-duration` only when nothing better exists

Do not rely on blind sleeps when a real wait condition is available.

## Practical patterns

### Drive vim safely

```bash
ht run --name notes vim /tmp/notes.md
ht send notes "ihello<Esc>" --wait-idle 200ms --view
ht send notes ":wq<CR>" --wait-exit
ht remove notes
```

### Drive a remote TUI over SSH

```bash
ht run --name remote ssh user@host.example
ht send remote "top<CR>" --wait-idle 500ms --view
ht send remote "q" --wait-idle 200ms
ht send remote "exit<CR>" --wait-exit
ht remove remote
```

### Inspect `git add -p`

```bash
ht run --name addp git add -p
ht view addp
```

Then send one choice at a time and wait after each response.

## Operating guidance

- Use unique named sessions so follow-up commands stay readable and do not collide with older runs.
- Send the minimum keystrokes needed; avoid giant pasted blobs.
- After any state-changing input, capture a fresh view before assuming success.
- If the screen looks wrong, inspect with `ht view` before sending more keys.
- Clean up exited sessions with `ht remove`.
- Ask before using `ht` for privacy-sensitive auth flows, remote systems, or destructive TUI operations. A real PTY can make it easy to do real damage quickly.

## Failure modes

- If the program exits immediately, check the command, working directory, and whether the program refuses non-interactive/unknown terminals.
- If waits time out, use a different wait condition instead of stacking longer sleeps.
- If the captured screen is stale or blank, check whether the app uses an alternate screen, requires a larger terminal size, or has already exited.
- If a task is simple enough for plain shell control, stop using `ht` and simplify.
- If the session is for a human to keep around, tmux is usually the better container.

## References

- `references/examples.md`: quick fit checks, sample command patterns, and wait-strategy examples
- `references/keys.md`: vim-style key notation such as `<CR>`, `<Esc>`, arrows, control/meta keys, and raw bytes
- `references/waits.md`: wait strategy decision tree and timeout guidance
- `references/recipes.md`: recipes for vim, REPLs, installers, watch, terminal sizing, screenshots, and recording
- `references/troubleshooting.md`: exit codes, stale views, wait timeouts, zombies, daemon issues, and `ht debug`
