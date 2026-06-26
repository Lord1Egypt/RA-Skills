---
name: nchat
description: Install, configure, inspect, troubleshoot, and operate the terminal-based nchat messenger client for Telegram, WhatsApp, and Signal. Use when Codex needs to set up nchat profiles, adjust ~/.config/nchat app/ui/key/color configuration, diagnose nchat startup/sync/media/keyboard issues, export or inspect nchat message cache with explicit privacy approval, or guide safe terminal workflows around sending, replying, editing, forwarding, attachments, reactions, proxies, QR/pairing login, and auto-compose.
---

# Nchat

Created by OpenClaw.

Use this skill for local nchat work. Treat nchat as privacy-sensitive because it stores chat accounts, logs, media/cache, and exportable message history under its config directory.

## Safety Boundaries

- Do not run `nchat`, `nchat --setup`, `nchat --remove`, `nchat --export`, or interactive key automation that can send, delete, archive, forward, or react unless the user explicitly authorized the exact action and account/scope.
- Do not print full phone numbers, profile local keys, proxy passwords, message cache, exported messages, logs, QR codes, pairing codes, auth codes, or private media paths into chat.
- For read-only diagnostics, prefer `scripts/nchat_doctor.py`; it avoids cache/history/log files and masks phone-like profile names.
- Scrub logs, core dumps, and exported histories before sharing with maintainers or third parties.
- Prefer separate config directories per protocol/phone number when configuring multiple accounts, for example `~/.config/nchat-telegram` and `~/.config/nchat-whatsapp`.

## Quick Start

Check the local install:

```bash
nchat --version
nchat --help
man nchat
```

Install on macOS:

```bash
brew tap d99kris/nchat
brew install nchat
```

Set up an account only after the user approves login/linking:

```bash
nchat --setup
USE_PAIRING_CODE=1 nchat --setup
USE_QR_TERMINAL=1 nchat --setup
```

Use a separate config directory:

```bash
nchat -d ~/.config/nchat-telegram --setup
nchat -d ~/.config/nchat-telegram
```

Remove an account or export message cache only with explicit approval:

```bash
nchat --remove
nchat --export <private-output-dir>
```

## Workflow

1. Classify the request: install/setup, config edit, UI/key/theme tuning, troubleshooting, message export, or interactive operation.
2. Check side effects. Ask before login/linking, send/delete/archive/forward/react, account removal, message export, log sharing, or anything that can reveal private messages.
3. Gather read-only context:

```bash
python3 scripts/nchat_doctor.py --confdir ~/.config/nchat
python3 scripts/nchat_doctor.py --confdir ~/.config/nchat --include-config
```

4. Read `references/nchat-reference.md` before editing config or giving detailed troubleshooting instructions.
5. Edit config files only while nchat is not running. Keep backups for user-specific config changes.
6. Verify with the smallest safe check: `nchat --version`, `nchat --help`, the doctor script, or an approved interactive launch.

## Configuration Map

- `app.conf`: cache, attachment behavior, downloads dir, SOCKS5 proxy, QR/pairing preferences, ISO timestamps, clipboard commands.
- `ui.conf`: UI layout, notifications, read receipts, typing/online status sharing, file/link/message open commands, spell check, auto-compose, terminal bell.
- `key.conf`: ncurses key bindings; use `nchat --keydump` to discover key codes.
- `color.conf` and `usercolor.conf`: theme colors and per-user group colors.
- `profiles/<Protocol_phone>/telegram.conf`: Telegram markdown and display-name settings.
- `profiles/<Protocol_phone>/whatsappmd.conf` and `signal.conf`: protocol display-name settings.

## Common Tasks

- **Send on Enter**: set `send_msg=KEY_RETURN` in `key.conf`. To keep multiline compose on Alt/Opt-Enter, set `linefeed_on_enter=0` in `ui.conf` and `linebreak=\\33\\15` in `key.conf`.
- **Alt/Opt shortcuts on macOS**: enable the terminal profile option that sends Option as Meta. If a shortcut still fails, use `nchat --keydump` and update `key.conf`.
- **Themes**: copy a theme's `color.conf` and `usercolor.conf` into the config directory while nchat is stopped.
- **Invisible sent messages**: remove `gray` values from `color.conf` if a terminal maps gray poorly.
- **Proxy setup before first login**: launch `nchat` once to create the config dir, edit `app.conf` proxy fields, then run `nchat --setup`.
- **Auto-compose**: treat as external AI usage. It may require `OPENAI_API_KEY` or `GEMINI_API_KEY` and can incur costs; keep disabled unless the user explicitly asks.
- **Debugging**: start with `nchat --verbose`. Review `log.txt` privately and redact it before any external sharing.

## Reference

Use `references/nchat-reference.md` for grounded details on commands, key bindings, config keys, setup modes, build flags, debugging, and limitations. The reference was distilled from nchat 5.15.26 README/manpage and the official d99kris/nchat docs.
