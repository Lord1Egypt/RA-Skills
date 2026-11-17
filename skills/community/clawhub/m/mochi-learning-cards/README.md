# Study Cards with Source References

[Simplified Chinese guide](README.zh-CN.md)

Turn notes into source-backed Q&A cards, exported as Markdown and Anki TSV.

## Features

Split supplied notes into passages and use your connected model to write Q&A cards. The script checks source quotes, duplicate questions and card counts, then exports Markdown, Anki TSV and a local review checklist.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Turn my notes into eight Chinese question-and-answer cards, each with supporting source text.
```

```text
Check these cards for duplicate questions or unsupported answers and list cards needing revision.
```

```text
Export the approved cards as Markdown and Anki TSV, and create a revision list.
```

## Advanced usage: run in a terminal

These commands are for manual execution in the terminal on the computer or server running OpenClaw. For everyday use, send one of the chat examples above.

Replace these placeholders with actual paths before running:

- `SKILL_DIRECTORY`: the installed Skill folder.
- `WORKSPACE`: the agent workspace path.
- `EVIDENCE_FILE`: the evidence-file path returned by the previous step.

Prepare the source:

```text
node "SKILL_DIRECTORY/scripts/learning-cards.mjs" prepare --workspace "WORKSPACE" --source "WORKSPACE/source.md" --language en --max-cards 8
```

After OpenClaw fills the returned card JSON, export:

```text
node "SKILL_DIRECTORY/scripts/learning-cards.mjs" export --workspace "WORKSPACE" --evidence "EVIDENCE_FILE"
```

Use an existing workspace. Try `samples/source.en.md` first. For Anki import, select a Basic note type and preview the Front/Back mapping.

## Requirements

OpenClaw with a connected model, Node.js 24.16+ or 26.1+, local command access and workspace read/write permission.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-learning-cards
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-learning-cards), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-learning-cards
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-learning-cards). Download the repository ZIP and copy `skills/mochi-learning-cards` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
