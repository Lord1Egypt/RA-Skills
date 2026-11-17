# Subscription and Renewal Desk

[Simplified Chinese guide](README.zh-CN.md)

Track software, memberships and service renewals, calculate cancellation deadlines, forecast costs by currency and queue due notices.

## Features

Track software, memberships and service renewals, calculate cancellation deadlines, forecast costs by currency and queue due notices.

Runs in the active agent workspace with local state. Supply your own account settings for mail, cloud storage or calendars. Scheduled notifications use OpenClaw scheduling.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Record a cloud-storage subscription: CNY 15 monthly, renewal on the 20th, cancellation required three days ahead.
```

```text
List services renewing within 30 days and total CNY and USD separately.
```

```text
Mark this subscription as cancelled and regenerate this month's renewal list and reminder records.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-subscription-desk
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-subscription-desk), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-subscription-desk
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-subscription-desk). Download the repository ZIP and copy `skills/mochi-subscription-desk` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
