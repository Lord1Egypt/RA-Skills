---
name: gomail
description: Send emails via the gomail sender CLI with attachments, templates, and recipient management. Use when sending or testing email delivery from OpenClaw.
---

# gomail Skill (OpenClaw)

Use the **gomail** `sender` CLI to send emails (with optional attachments and templates) from OpenClaw. This skill wraps the prebuilt Linux `sender` binary from the gomail project and exposes its flags as structured parameters.

## Installation

Download the latest prebuilt Linux AMD64 release that contains the `sender` binary:

```bash
# From a directory on your PATH or the skill directory
LATEST_URL=$(curl -sL -o /dev/null -w '%{url_effective}' https://github.com/craftslab/gomail/releases/latest)
VERSION=${LATEST_URL##*/}          # e.g. v2.7.2
VERSION_NO_V=${VERSION#v}         # e.g. 2.7.2

# Note: the release tag includes a leading "v", but the tarball filename does not.
wget "https://github.com/craftslab/gomail/releases/download/${VERSION}/gomail_${VERSION_NO_V}_linux_amd64.tar.gz"
tar -xf "gomail_${VERSION_NO_V}_linux_amd64.tar.gz"

# Ensure the binaries are executable
chmod +x sender parser
```

- **Recommended**: Place `sender` on your `PATH` (e.g. `/usr/local/bin/sender`) or keep it in the gomail skill directory and invoke it with `./sender`.
- This skill assumes a Linux environment compatible with the gomail Linux AMD64 builds.

## Configuration

The `sender` tool reads mail server and sender configuration from a JSON file passed via `--config`. This skill includes a starter config template at `sender.json` (in the gomail skill directory). It includes:

- SMTP server settings (host, port, TLS, auth)
- Authentication credentials
- A `sender` email address (the actual From address)

For OpenClaw, you can:

- Use the bundled config template in the gomail skill directory, `sender.json` (recommended).
- Or point `--config` to any other JSON file you manage.

> **Important**: `skill/sender.json` is a template. Replace the placeholder values with real SMTP credentials and keep secrets out of source control.

> **Important**: The `--header` flag only controls the human‑readable display name. The actual From email address is read from the `sender` field in the config file, as described in the gomail README.

## Parameters (CLI)

This skill uses the `sender` command exactly as documented in the gomail README:

```bash
usage: sender --recipients=RECIPIENTS [<flags>]
```

| Argument / Flag        | Required | Description |
|------------------------|----------|-------------|
| `--config` / `-c`      | ✅       | Path to config JSON file, e.g. `sender.json`. Defines SMTP/server settings and the actual sender address. |
| `--recipients` / `-p`  | ✅       | Recipients list, format: `alen@example.com,cc:bob@example.com`. Supports `cc:` prefix for CC recipients. |
| `--attachment` / `-a`  | ❌       | Comma‑separated attachment files, e.g. `attach1.txt,attach2.txt`. Paths are resolved relative to the working directory. |
| `--body` / `-b`        | ❌       | Body text or path to a body file, e.g. `body.txt`. |
| `--content_type` / `-e`| ❌       | Content type: `HTML` or `PLAIN_TEXT` (default). |
| `--header` / `-r`      | ❌       | Sender display name, combined with `sender` from config to form the From header (e.g. `"Your Name" <noreply@example.com>`). |
| `--title` / `-t`       | ❌       | Subject/title text for the email. |
| `--dry-run` / `-n`     | ❌       | If set, only outputs recipient validation JSON and exits; **does not send** the email. |
| `--help`               | ❌       | Show help. |
| `--version`            | ❌       | Show application version. |

## Basic usage

From inside the gomail skill directory (with a bundled config and body file):

```bash
./sender \
  --config="sender.json" \
  --attachment="attach1.txt,attach2.txt" \
  --body="body.txt" \
  --content_type="PLAIN_TEXT" \
  --header="Your Name" \
  --recipients="alen@example.com,bob@example.com,cc:catherine@example.com" \
  --title="TITLE"
```

When integrated in OpenClaw, construct the command with the appropriate flags based on user input. Use `--dry-run` during testing or when you only need to validate recipients without sending mail:

```bash
sender \
  --config="sender.json" \
  --recipients="test@example.com" \
  --dry-run
```

## When to use

- **Send email**: When the user asks to send an email, notification, or message (optionally with attachments) via SMTP.
- **Validate recipients**: When the user wants to validate or preview recipients without sending (use `--dry-run`).
- **gomail specific**: When the user mentions gomail, gomail sender, or wants to use the gomail CLI for mail delivery from OpenClaw.
