# Contacts and Follow-up Desk

[Simplified Chinese guide](README.zh-CN.md)

Import CSV/vCard contacts, review email and phone duplicates, merge records, track follow-ups and export an address book.

## Features

Import CSV/vCard contacts, review email and phone duplicates, merge records, track follow-ups and export an address book.

Runs in the active agent workspace with local state. Supply your own account settings for mail, cloud storage or calendars. Scheduled notifications use OpenClaw scheduling.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Preview field mappings and duplicate contacts in contacts.csv before importing.
```

```text
Find duplicate contacts by email and phone, list conflicting fields, and let me choose merge values.
```

```text
Record today's conversation with Alex and a follow-up next Wednesday; list this week's follow-ups and export CSV.
```

## Requirements

Python 3.10+; vobject==0.9.9

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-contact-desk
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-contact-desk), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-contact-desk
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-contact-desk). Download the repository ZIP and copy `skills/mochi-contact-desk` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
