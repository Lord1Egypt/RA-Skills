---
name: imsgctl
description: "Read Apple Messages data with imsgctl: check access, list chats, inspect message history, filter by time, include attachment metadata, and watch new activity from the local data available to imsgctl."
metadata:
  openclaw:
    homepage: https://github.com/jpreagan/imsgkit
    os:
      - darwin
      - linux
    requires:
      bins:
        - imsgctl
    install:
      - kind: brew
        formula: jpreagan/tap/imsgctl
        bins:
          - imsgctl
---

# imsgctl

Use `imsgctl` to read Apple Messages data available on the current machine.

## Use This Skill When

- The user wants to inspect iMessage or SMS data from Apple Messages.
- The user wants to list recent chats.
- The user wants message history for a specific chat.
- The user wants to filter message history by time.
- The user wants attachment metadata.
- The user wants to watch for new messages or reactions.

## Do Not Use This Skill When

- The user wants to send or reply to a message.
- The user wants to delete, edit, react to, or otherwise modify Messages data.
- The request is about Slack, Discord, Telegram, Signal, WhatsApp, or another messaging system.

## Operating Rules

- Prefer `--json` when results may be parsed or reused.
- `imsgctl health --json` emits one JSON object.
- `imsgctl chats --json`, `history --json`, and `watch --json` emit JSONL.
- Use `--db PATH` when the user gives a specific database path or when the backend must be explicit.
- Use `watch` only for live monitoring. It streams until interrupted.

## Defaults And Access

- On macOS, running without `--db` prefers `~/Library/Application Support/imsgkit/replica.db` when a valid replica exists. Otherwise it falls back to `~/Library/Messages/chat.db`.
- On Linux, running without `--db` reads `~/.local/share/imsgkit/replica.db`, or `$XDG_DATA_HOME/imsgkit/replica.db` when `XDG_DATA_HOME` is set to an absolute path.
- Direct access to `~/Library/Messages/chat.db` requires macOS and Full Disk Access for the process doing the reading.
- If contact resolution is unavailable, chat and sender labels may fall back to raw identifiers.

## Common Commands

### Check Access

```bash
imsgctl health --json
```

### List Recent Chats

```bash
imsgctl chats --limit 20 --json
```

### Read Recent History For A Chat

```bash
imsgctl history --chat-id 42 --limit 50 --json
```

### Read History With Attachment Metadata

```bash
imsgctl history --chat-id 42 --limit 50 --attachments --json
```

### Read History In A Time Window

```bash
imsgctl history \
  --chat-id 42 \
  --limit 50 \
  --start 2026-03-01T00:00:00Z \
  --end 2026-03-02T00:00:00Z \
  --json
```

### Watch New Activity

```bash
imsgctl watch --chat-id 42 --json
```

### Watch New Messages, Attachments, and Reactions

```bash
imsgctl watch --chat-id 42 --attachments --reactions --json
```

### Use An Explicit Database Path

```bash
imsgctl chats --db ~/Library/Application\ Support/imsgkit/replica.db --limit 20 --json
imsgctl history --db ~/.local/share/imsgkit/replica.db --chat-id 42 --limit 50 --json
```

## Recommended Workflow

1. Run `imsgctl health --json` to confirm access.
2. Run `imsgctl chats --limit 20 --json` to identify the target chat.
3. Use the returned chat ID with `imsgctl history --chat-id ... --json`.
4. Add `--start`, `--end`, `--limit`, or `--attachments` only as needed.
5. Use `imsgctl watch` only if the user asked for live monitoring.

## Viewing Image Attachments

When `--attachments` reveals an image, the file is often too large to read directly. Convert it to a smaller JPEG preview, then read the result:

- **macOS:** `sips -s format jpeg -Z 800 "/path/to/image.heic" --out /tmp/preview.jpg`
- **Linux:** `magick "/path/to/image.heic" -resize 800x800 /tmp/preview.jpg`

## Failure Modes

- If direct macOS reads fail, check Full Disk Access first.
- If the expected local database path is missing, access will fail until the correct database is available on the current machine.
- If chat labels are ambiguous or missing, rely on chat IDs and raw identifiers.
