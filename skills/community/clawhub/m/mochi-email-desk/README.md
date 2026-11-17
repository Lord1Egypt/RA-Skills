# Multi-account Email Desk

[Simplified Chinese guide](README.zh-CN.md)

Connect IMAP/SMTP/POP3 accounts, sync and search mail, extract attachments, prepare and send messages, and track new-mail notifications.

## Features

Connect IMAP/SMTP/POP3 accounts, sync and search mail, extract attachments, prepare and send messages, and track new-mail notifications.

Runs in the active agent workspace with local state. Supply your own account settings for mail, cloud storage or calendars. Scheduled notifications use OpenClaw scheduling.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Use my configured work mailbox to read the latest ten emails and list sender, subject and time.
```

```text
Search this month's work-mail subjects for invoice and save the attachments I select into a new directory.
```

```text
Prepare a meeting-confirmation email to the recipient I specify with my attachment; show the draft and wait for my confirmation before sending.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-email-desk
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-email-desk), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-email-desk
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-email-desk). Download the repository ZIP and copy `skills/mochi-email-desk` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
