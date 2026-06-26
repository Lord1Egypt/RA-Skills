---
name: padel-tui-playtomic-booking
description: This skill should be used when the user asks to "book a padel court", "find available padel courts", "search padel courts near me", "reserve a Playtomic court", "book a court tonight", "list my active matches", "cancel a padel booking", "install padel-tui", "use padel-tui CLI", or "book through terminal instead of the app".
---

# Book Padel Courts With `padel-tui`

Use this skill to complete Playtomic booking tasks from a terminal with minimal assumptions about prior setup.

## Trigger Examples

- "Find me a padel court in Berlin tonight."
- "Book a Playtomic court for tomorrow at 19:00."
- "Show my active matches and cancel one."
- "Install padel-tui and use it to reserve a court."
- "Use CLI instead of TUI for booking."

## When To Use

- Use when the task is to search courts, book a slot, list active matches, or cancel a match.
- Use when the user requests Playtomic actions through CLI commands.
- Do not use for non-Playtomic tasks.

## Required Safety Rules

- Ask about installation only if needed (binary missing) or explicitly requested.
- Confirm installation intent before running any install command.
- Ask: "Do you want me to install `padel-tui` now, or skip installation and use your current setup?"
- If installation is declined, continue with the existing binary/path.
- Do not ask the user for email or password.
- Ask the user to authenticate interactively with `<prefix> auth login`.
- Treat `book` and `match-cancel` as user-impacting operations and run only after explicit user intent.

## Setup Check

1. Select a command prefix.
   - Global install: `padel-tui`
   - Source checkout: `./bin/padel-tui`
2. Verify access with `<prefix> --version`.
3. If command is missing and installation is approved, follow `references/INSTALLATION.md`.

## Terms (Minimal Context)

- `tenant_id`: venue or club id from `search` output.
- `resource_id`: specific court id from `search` output.
- `start`: slot datetime in `YYYY-MM-DDTHH:mm:ss` format.

## Minimal Booking Workflow

1. Ask the user to authenticate interactively.
   - Instruct the user to run: `<prefix> auth login`
   - Wait for user confirmation that login is complete.
2. Search availability (one mode required).
   - `<prefix> search --near "<city>" --date YYYY-MM-DD`
   - `<prefix> search --name "<venue>" --date YYYY-MM-DD`
3. Capture booking inputs from search output.
   - Record `tenant_id`, `resource_id`, and slot start time.
4. Create booking.
   - `<prefix> book --tenant-id <tenant-id> --resource-id <resource-id> --start YYYY-MM-DDTHH:mm:ss --duration 60 --players 4`
5. Verify result.
   - `<prefix> matches --size 30`
6. Cancel only when requested.
   - `<prefix> match-cancel --match-id <match-id>`

## Command Rules

- Require one of `--near` or `--name` for `search`.
- Require `--tenant-id`, `--resource-id`, and `--start` for `book`.
- Keep authentication interactive; use `<prefix> auth login` without credential flags.
- Use `search` and `book`; avoid legacy `availability` and `payment` groups.

## Reference Files

- `references/INSTALLATION.md` - install paths, verification, and first login.
