# Daily and Weekly Work Reports

[Simplified Chinese guide](README.zh-CN.md)

Import work records, update status with revision history, and export dated reports and evidence.

## What it does

Import work records, update status with revision history, and export dated reports and evidence.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Turn my weekly work notes into completed work, work in progress and next week's plans, and save a weekly report.
```

```text
Combine these daily work records and flag items missing an owner or deadline.
```

```text
Compare last week's and this week's records, list new, completed and delayed items, and export a report.
```

## Exported files

work-report.md / work-records.csv

Files stay in the active agent workspace, with paths and SHA256 receipts. Existing records and earlier exports are retained.

## Requirements

OpenClaw, a connected model, Node.js 24.16+, and read/write access to the current agent workspace.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-work-reports
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-work-reports), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-work-reports
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-work-reports). Download the repository ZIP and copy `skills/mochi-work-reports` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
