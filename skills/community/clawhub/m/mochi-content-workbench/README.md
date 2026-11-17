# Content Repurposing Workbench

[Simplified Chinese guide](README.zh-CN.md)

Adapt one source into channel-specific drafts, checking evidence and character budgets.

## Features

Build a fact ledger from release notes, product material or an article, then use your connected model to draft for different channels, languages and tones. Check your chosen character budgets, citations, language and similar copy. Save `drafts.md`, `facts.md` and JSON.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Using my product materials, write a Chinese social post under 150 characters and an English X draft, retaining factual sources.
```

```text
Adapt these release notes into a formal email and a short announcement, save both, and check numbers and links.
```

```text
Shorten this draft to 300 words while preserving prices, dates and core features, and show a before/after comparison.
```

## Advanced usage: run in a terminal

These commands are for manual execution in the terminal on the computer or server running OpenClaw. For everyday use, send one of the chat examples above.

Replace these placeholders with actual paths before running:

- `SKILL_DIRECTORY`: the installed Skill folder.
- `WORKSPACE`: the agent workspace path.
- `INPUT_JSON`: the prepared input JSON file.

Have OpenClaw prepare material, facts and drafts using `samples/campaign.json`, then run:

```text
node "SKILL_DIRECTORY/scripts/check.mjs" --input "INPUT_JSON" --output-dir "WORKSPACE"
```

Use actual file paths and an existing workspace. Character budgets count Unicode code points, including spaces and newlines.

## Requirements

OpenClaw with a connected model, Node.js 24.16+ or 26.1+, local command access and workspace read/write permission.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-content-workbench
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-content-workbench), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-content-workbench
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-content-workbench). Download the repository ZIP and copy `skills/mochi-content-workbench` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
