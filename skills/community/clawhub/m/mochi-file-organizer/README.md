# File Organization Plan and Duplicate Report

[Simplified Chinese guide](README.zh-CN.md)

Scan a chosen folder for a category plan and SHA256 duplicate-file report.

## Features

Read a chosen folder, identify identical files by size and SHA256, and suggest extension-based categories with collision-aware destination paths. Review the plan in `plan.json` and `report.md`; source files stay in place.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Scan my specified Downloads directory and propose classification by extension, showing target paths first.
```

```text
Find duplicate files across these two directories, verify with SHA256, and generate a duplicate report.
```

```text
Propose non-conflicting target names for these same-name files and save plan.json and report.md for review.
```

## Advanced usage: run in a terminal

These commands are for manual execution in the terminal on the computer or server running OpenClaw. For everyday use, send one of the chat examples above.

Replace these placeholders with actual paths before running:

- `SKILL_DIRECTORY`: the installed Skill folder.
- `INPUT_DIRECTORY`: the directory to scan.
- `NEW_REPORT_DIRECTORY`: a new report directory.

Or run:

```text
node "SKILL_DIRECTORY/scripts/organize.mjs" --root "INPUT_DIRECTORY" --out "NEW_REPORT_DIRECTORY"
```

Replace the paths with your actual folders. Put the new report folder outside the scanned tree. Start with `samples/sample-input` for a small example.

## Requirements

OpenClaw with a connected model, Node.js 24.16+ or 26.1+, local command access and workspace read/write permission.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-file-organizer
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-file-organizer), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-file-organizer
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-file-organizer). Download the repository ZIP and copy `skills/mochi-file-organizer` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
