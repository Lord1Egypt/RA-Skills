# My Daily Brief

[Simplified Chinese guide](README.zh-CN.md)

Organize public updates by topic into a local brief with source links and dates.

## Features

Collect public RSS/Atom updates from OpenAI News, Google AI, GitHub Changelog or your chosen feeds. Filter by topic, date and timezone, deduplicate entries, and use your connected OpenClaw model to write a Chinese or English brief.

Markdown reports go into `daily-briefs/` with original links, publication dates and source information. Choose 1–30 calendar days and up to 20 items. Custom feeds are configured in `references/options.md`.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Collect AI news from supported RSS sources for the last 24 hours, filter in Asia/Shanghai time, deduplicate, and include source links.
```

```text
Summarize GitHub Changelog updates from the last seven days by date and save Markdown.
```

```text
Create today's Chinese brief from my RSS feeds, stating the time window and each item's publication time.
```

## Requirements

OpenClaw with a connected model, Node.js 24.16+ or 26.1+, local command access and workspace read/write permission. Network access to the selected public HTTPS sources.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-daily-brief
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-daily-brief), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-daily-brief
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-daily-brief). Download the repository ZIP and copy `skills/mochi-daily-brief` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
