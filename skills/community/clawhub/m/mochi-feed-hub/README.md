# RSS Subscription and Reading Hub

[Simplified Chinese guide](README.zh-CN.md)

Subscribe to RSS/Atom, import and export OPML, retain read state, search saved entries and queue new-content notifications.

## Features

Subscribe to RSS/Atom, import and export OPML, retain read state, search saved entries and queue new-content notifications.

Runs in the active agent workspace with local state. Supply your own account settings for mail, cloud storage or calendars. Scheduled notifications use OpenClaw scheduling.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Add the RSS URL I provide and establish an initial baseline without treating historical articles as new.
```

```text
Import this OPML subscription list, fetch updates, and list unread articles with their sources.
```

```text
Search saved articles for OpenClaw and mark the items I have finished as read.
```

## Requirements

Python 3.10+; feedparser>=6.0.12,<7

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-feed-hub
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-feed-hub), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-feed-hub
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-feed-hub). Download the repository ZIP and copy `skills/mochi-feed-hub` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
