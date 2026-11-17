# Reply Drafts

[Simplified Chinese guide](README.zh-CN.md)

Draft replies from messages and verified notes, with evidence and a follow-up checklist.

## Features

Organize incoming messages, confirmed facts and supplied policies, then use your connected model to write an email or support reply. Check recipients, evidence, numbers, links and commitment wording. Save a local `draft.txt` and checklist for your review.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Draft a polite Chinese response to a customer's order-status inquiry using my processing records.
```

```text
Draft an English reply using this email and refund policy; check amounts, dates and links, and list unresolved facts.
```

```text
Make this reply shorter, retain confirmed facts, and save draft.txt for my review.
```

## Advanced usage: run in a terminal

These commands are for manual execution in the terminal on the computer or server running OpenClaw. For everyday use, send one of the chat examples above.

Replace these placeholders with actual paths before running:

- `SKILL_DIRECTORY`: the installed Skill folder.
- `WORKSPACE`: the agent workspace path.
- `INPUT_JSON`: the prepared input JSON file.

Have OpenClaw prepare the message, facts and draft using `samples/reply.json`, then run:

```text
node "SKILL_DIRECTORY/scripts/check.mjs" --input "INPUT_JSON" --output-dir "WORKSPACE"
```

Use actual file paths and an existing workspace. Results include the reply draft, `checklist.md` and a structured report.

## Requirements

OpenClaw with a connected model, Node.js 24.16+ or 26.1+, local command access and workspace read/write permission.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-reply-drafts
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-reply-drafts), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-reply-drafts
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-reply-drafts). Download the repository ZIP and copy `skills/mochi-reply-drafts` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
