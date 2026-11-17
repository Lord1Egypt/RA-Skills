# Important Dates and Holidays

[Simplified Chinese guide](README.zh-CN.md)

Track Gregorian and lunar birthdays, anniversaries and sourced annual holidays, with advance alerts, time zones, leap-day policies and calendar export.

## Features

Track Gregorian and lunar birthdays, anniversaries and sourced annual holidays, with advance alerts, time zones, leap-day policies and calendar export.

Runs in the active agent workspace with local state. Supply your own account settings for mail, cloud storage or calendars. Scheduled notifications use OpenClaw scheduling.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Record Mum's birthday on lunar month 8 day 15, with reminders seven days ahead and on the day in Asia/Shanghai; confirm scheduling and delivery.
```

```text
Record our wedding anniversary on June 18 each year and list important dates within the next 90 days.
```

```text
Import the annual official holiday schedule I provide, distinguish holidays from make-up workdays, and export an ICS calendar.
```

## Requirements

Python 3.10+; lunar-python==1.4.8, icalendar>=6.3,<7, tzdata>=2025.1

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-important-dates
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-important-dates), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-important-dates
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-important-dates). Download the repository ZIP and copy `skills/mochi-important-dates` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
