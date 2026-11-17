# Calendar and Agenda Desk

[Simplified Chinese guide](README.zh-CN.md)

Import ICS calendars, expand recurring events, inspect conflicts, create meeting files and transfer CalDAV resources with version checks.

## Features

Import ICS calendars, expand recurring events, inspect conflicts, create meeting files and transfer CalDAV resources with version checks.

Runs in the active agent workspace with local state. Supply your own account settings for mail, cloud storage or calendars. Scheduled notifications use OpenClaw scheduling.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Read the uploaded calendar.ics and list next week's events in Asia/Shanghai time.
```

```text
Check this calendar for overlapping events during the next two weeks.
```

```text
Create an ICS file for four weekly 30-minute meetings at 10 AM on Mondays starting next week.
```

## Requirements

Python 3.10+; icalendar>=6.3,<7, recurring-ical-events>=3.8,<4, tzdata>=2025.1

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-calendar-desk
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-calendar-desk), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-calendar-desk
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-calendar-desk). Download the repository ZIP and copy `skills/mochi-calendar-desk` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
