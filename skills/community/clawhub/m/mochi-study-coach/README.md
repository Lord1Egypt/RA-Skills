# Study Coach and Mistake Review

[Simplified Chinese guide](README.zh-CN.md)

Import question decks, retain attempts and review dates, summarize practice and export answer-hidden queues.

## What it does

Import question decks, retain attempts and review dates, summarize practice and export answer-hidden queues.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Import my question bank, choose five exercises for today, ask them one at a time, and record my results.
```

```text
Find my previously incorrect answers, offer hints first, and explain after I answer.
```

```text
Generate a revision list from saved practice records and export a version without answers.
```

## Exported files

review-plan.md / review-queue.csv

Files stay in the active agent workspace, with paths and SHA256 receipts. Existing records and earlier exports are retained.

## Requirements

OpenClaw, a connected model, Node.js 24.16+, and read/write access to the current agent workspace.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-study-coach
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-study-coach), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-study-coach
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-study-coach). Download the repository ZIP and copy `skills/mochi-study-coach` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
