# Web Research Notes

[Simplified Chinese guide](README.zh-CN.md)

Read selected pages and save local research notes with source links and dates.

## Features

Read 1–3 public HTTPS pages you supply, extract static text, source dates and excerpts, then use your connected model to write cited Markdown notes. Useful for comparing articles or collecting material on a topic.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Read the two public pages I provide, compare their main points, and include source links and dates.
```

```text
Collect installation requirements from these three pages into research notes with quotations.
```

```text
Summarize my supplied web sources in Chinese and save Markdown notes and source records.
```

## Advanced usage: run in a terminal

These commands are for manual execution in the terminal on the computer or server running OpenClaw. For everyday use, send one of the chat examples above.

Replace these placeholders with actual paths before running:

- `SKILL_DIRECTORY`: the installed Skill folder.
- `WORKSPACE`: the agent workspace path.
- `EVIDENCE_FILE`: the evidence-file path returned by the previous step.

Create `urls.json` in the workspace with an array of page URLs, then collect:

```text
node "SKILL_DIRECTORY/scripts/web-notes.mjs" collect --workspace "WORKSPACE" --urls "WORKSPACE/urls.json" --language en
```

Have OpenClaw write a draft from the returned evidence, then save:

```text
node "SKILL_DIRECTORY/scripts/web-notes.mjs" save --workspace "WORKSPACE" --evidence "EVIDENCE_FILE"
```

Replace placeholders with actual paths. Finished notes go into the workspace's `web-notes/` folder.

## Requirements

OpenClaw with a connected model, Node.js 24.16+ or 26.1+, local command access and workspace read/write permission. Network access to the selected public HTTPS sources.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-web-notes
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-web-notes), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-web-notes
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-web-notes). Download the repository ZIP and copy `skills/mochi-web-notes` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
