# Privacy Redaction Desk

[Simplified Chinese guide](README.zh-CN.md)

Scan and redact email, Chinese mobile numbers, IPs and secret fields in text, CSV and JSON, keeping originals intact.

## Features

Scan and redact email, Chinese mobile numbers, IPs and secret fields in text, CSV and JSON, keeping originals intact.

Runs in the active agent workspace and saves results and reports while preserving source files.

## Usage examples

After installation, send an example to your AI with the relevant files or URLs.

```text
Scan these logs for emails, phone numbers and tokens and report counts first.
```

```text
Redact passwords and token fields in this JSON and create a shareable copy.
```

```text
Process these text files and also hide the exact project names I supply.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-privacy-redactor
```

Alternatively, get the ZIP on this page and place its Skill folder in the active workspace's `skills/` directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
