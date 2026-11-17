# Meeting Minutes and Action Items

[Simplified Chinese guide](README.zh-CN.md)

Turn meeting text into cited minutes, decisions and action items.

## Features

Use your connected model to extract summaries, decisions, actions and open questions from meeting text. The script checks source quotes, owners and dates, then exports `meeting.md`, `meeting.json` and `tasks.csv`. Unstated owners or dates remain marked unknown.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Turn this meeting text into a summary, decisions and actions, each with source quotations.
```

```text
Extract owners and deadlines from the meeting notes, marking unspecified values for confirmation.
```

```text
Export this meeting's actions as tasks.csv and save Markdown minutes.
```

## Advanced usage: run in a terminal

These commands are for manual execution in the terminal on the computer or server running OpenClaw. For everyday use, send one of the chat examples above.

Replace these placeholders with actual paths before running:

- `SKILL_DIRECTORY`: the installed Skill folder.
- `NEW_REPORT_DIRECTORY`: a new report directory.
- `TRANSCRIPT.txt`: the meeting transcript file.
- `NEW_EVIDENCE_DIRECTORY`: a new source-evidence directory.
- `EVIDENCE_FILE`: the evidence-file path returned by the previous step.
- `EXTRACTION_JSON`: the extraction JSON completed from the template.

Prepare numbered evidence:

```text
node "SKILL_DIRECTORY/scripts/meeting.mjs" prepare --input "TRANSCRIPT.txt" --out "NEW_EVIDENCE_DIRECTORY"
```

Have OpenClaw fill the returned extraction template, then export:

```text
node "SKILL_DIRECTORY/scripts/meeting.mjs" render --evidence "EVIDENCE_FILE" --draft "EXTRACTION_JSON" --out "NEW_REPORT_DIRECTORY"
```

Use actual input paths and new output folders. Try `samples/sample-input.txt` first.

## Requirements

OpenClaw with a connected model, Node.js 24.16+ or 26.1+, local command access and workspace read/write permission.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-meeting-actions
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-meeting-actions), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-meeting-actions
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-meeting-actions). Download the repository ZIP and copy `skills/mochi-meeting-actions` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
