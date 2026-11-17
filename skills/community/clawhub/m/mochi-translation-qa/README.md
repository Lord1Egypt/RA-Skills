# Translation and Proofreading

[Simplified Chinese guide](README.zh-CN.md)

Translate or review text, check terms, numbers and links, and export a bilingual comparison with issues.

## Features

Translate or polish supplied text with your connected model, then check segment alignment, required terminology, numbers and links. Save Markdown and CSV comparisons with specific issues for review.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Source: The Starter plan costs USD 9.90 per month and supports 3 projects. Chinese draft: Starter计划每年收费99美元，支持30个项目。 Find the three errors and give the correct translation.
```

```text
Translate my product description into English, keep OpenClaw unchanged, and check dates, numbers and links.
```

```text
Review this bilingual draft against my glossary and export a comparison CSV and issue list.
```

## Advanced usage: run in a terminal

These commands are for manual execution in the terminal on the computer or server running OpenClaw. For everyday use, send one of the chat examples above.

Replace these placeholders with actual paths before running:

- `SKILL_DIRECTORY`: the installed Skill folder.
- `WORKSPACE`: the agent workspace path.
- `INPUT_JSON`: the prepared input JSON file.

Have OpenClaw prepare source and target text using the format in `samples/review.json`, then run:

```text
node "SKILL_DIRECTORY/scripts/check.mjs" --input "INPUT_JSON" --output-dir "WORKSPACE"
```

Use actual file paths and an existing workspace. Each run creates its own folder containing `comparison.md`, `comparison.csv` and `report.json`.

## Requirements

OpenClaw with a connected model, Node.js 24.16+ or 26.1+, local command access and workspace read/write permission.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-translation-qa
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-translation-qa), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-translation-qa
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-translation-qa). Download the repository ZIP and copy `skills/mochi-translation-qa` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
