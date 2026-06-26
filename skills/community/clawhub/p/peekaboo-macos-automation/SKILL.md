---
name: peekaboo-macos-automation
description: Use Peekaboo for macOS desktop GUI automation, screen understanding, and MCP-backed local app control. Trigger when the user wants to inspect or control native macOS apps, Finder, Notes, Xcode, Terminal, system dialogs, menu bar items, Dock, Spaces, or other non-browser UI; when they ask to click, type, scroll, drag, switch apps, handle popups, or automate a desktop workflow on Mac; or when they explicitly mention Peekaboo. If Peekaboo is missing, detect that first and proactively install it for the user, then continue. Prefer this over browser automation for native macOS interfaces.
---

# Peekaboo macOS automation

Use this skill to drive native macOS UI with Peekaboo.

## Core rules

- Treat Peekaboo as an external local automation backend, not as a built-in tool.
- Prefer `peekaboo` CLI via `exec`.
- Detect installation before doing anything else.
- If Peekaboo is not installed, proactively install it for the user, then verify installation before continuing.
- Check permissions before first real automation step.
- Prefer semantic actions over coordinate clicks whenever possible.
- Use browser automation instead for web-page DOM tasks.

## Detection and installation

Run these checks in order:

```bash
command -v peekaboo
peekaboo --version
```

If `peekaboo` is missing, install it proactively:

```bash
brew install steipete/tap/peekaboo
```

After installation, verify again:

```bash
command -v peekaboo && peekaboo --version
```

If Homebrew is missing, check for it first:

```bash
command -v brew
```

If `brew` is also missing, ask one concise question before installing Homebrew or using another path.

## Permission check

Before GUI actions, check permissions:

```bash
peekaboo permissions status
```

If Screen Recording or Accessibility is missing, tell the user exactly what is missing and pause until granted. Do not pretend automation can succeed without them.

For a quick readiness check, you can run:

```bash
~/.openclaw/skills/peekaboo-macos-automation/scripts/doctor.sh
```

## Preferred workflow

1. Detect/install Peekaboo.
2. Check permissions.
3. If the task targets a specific native app window, bring that app to the foreground first.
4. Inspect the target UI.
5. Prefer semantic action APIs.
6. Fall back to synthetic input only when needed.
7. Re-inspect after state-changing actions when the next step depends on fresh UI state.

Before `see`, `click`, `set-value`, or other window-level actions on a named app, do this first:

```bash
peekaboo app switch --to "AppName"
```

If needed, unhide or launch it first:

```bash
peekaboo app unhide --app "AppName"
peekaboo app launch "AppName"
```

Do not assume a running app has a capturable front window. Bring it forward first, then inspect it.

## Inspection patterns

Use structured inspection first. Start broad, then narrow:

```bash
peekaboo list apps
peekaboo app switch --to "Safari"
peekaboo see --app "Safari" --json
peekaboo image --mode screen --retina --path ~/Desktop/peekaboo-screen.png
```

When a command returns a `snapshot_id`, reuse it for follow-up actions.

A good first-pass sequence is:

```bash
peekaboo list apps
peekaboo app switch --to "TargetApp"
peekaboo see --app "TargetApp" --json
```

## Action preference order

Prefer actions in this order:

1. `set-value`
2. `perform-action`
3. `click --on <id/query>`
4. `type`
5. coordinate-based actions only as a fallback

Examples:

```bash
peekaboo set-value --on T1 --value "hello" --snapshot "$SNAPSHOT"
peekaboo perform-action --on B1 --action AXPress --snapshot "$SNAPSHOT"
peekaboo click --on "Save" --snapshot "$SNAPSHOT"
peekaboo type --text "hello world"
```

## Common commands

- Focus + inspect UI: `peekaboo app switch --to "AppName" && peekaboo see --app "AppName" --json`
- List windows: prefer app-focused inspection over raw window listing
- Click element: `peekaboo click --on "Label" --snapshot "$SNAPSHOT"`
- Set text directly: `peekaboo set-value --on T1 --value "text" --snapshot "$SNAPSHOT"`
- Trigger AX action: `peekaboo perform-action --on B1 --action AXPress --snapshot "$SNAPSHOT"`
- Hotkey: `peekaboo hotkey cmd,shift,t`
- Switch apps: `peekaboo app switch --to "Notes"`
- Work with dialogs: `peekaboo dialog list`
- Menu bar: `peekaboo menubar list`
- Dock: `peekaboo dock list`
- Spaces: `peekaboo space list`
- Natural language agent: `peekaboo agent "..."`

## When to ask first

Ask before:

- destructive or irreversible actions
- sending messages, emails, or posts through another app
- entering secrets, passwords, or 2FA codes
- bulk actions that could affect user data
- installing Homebrew if it is not present

Do not ask before installing Peekaboo itself if Homebrew is already available and the user asked to use or set up Peekaboo.

## Troubleshooting

If `peekaboo see` fails:

- switch/focus the app first with `peekaboo app switch --to "AppName"`
- if the app may be hidden, run `peekaboo app unhide --app "AppName"`
- retry with `peekaboo see --app frontmost --json`
- retry with a simpler target or a full-screen capture

If a semantic action fails:

- refresh the snapshot
- try `perform-action`
- only then fall back to `click` or keyboard input

If permission output is unclear, report the raw missing permission names to the user.

## Reporting

Keep updates short and concrete:

- whether Peekaboo was already installed or was installed now
- whether permissions are ready
- what app/UI was inspected
- what action succeeded or what blocked progress

## Safety notes

- Native desktop automation is high-impact; avoid risky guesses.
- Do not claim success without command evidence.
- If Peekaboo errors, retry once with a simpler or more direct command before concluding.
- If the task is clearly a browser page task, use the browser tool instead of forcing Peekaboo.
