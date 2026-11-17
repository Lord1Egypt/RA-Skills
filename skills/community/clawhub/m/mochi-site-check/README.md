# Website Availability and Basic SEO Check

[Simplified Chinese guide](README.zh-CN.md)

Check selected pages once for status, redirects, timing and basic SEO fields.

## Features

Visit 1–5 public HTTPS URLs you supply. Record HTTP status, final URL, redirects, elapsed time and TLS validation. Read static HTML title, description, robots and canonical fields, then save JSON and Markdown reports.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Check https://mochilab.bz/ for HTTP status, redirects and response time, and save an inspection report.
```

```text
Run one check of my three public HTTPS URLs and compare titles, descriptions and canonical URLs.
```

```text
Check this page's TLS validation and robots metadata, and save issues and source URLs as Markdown.
```

## Advanced usage: run in a terminal

These commands are for manual execution in the terminal on the computer or server running OpenClaw. For everyday use, send one of the chat examples above.

Replace these placeholders with actual paths before running:

- `SKILL_DIRECTORY`: the installed Skill folder.
- `WORKSPACE`: the agent workspace path.

Create `urls.json` in the workspace, for example:

```json
["https://mochilab.bz/"]
```

Then run in the terminal:

```text
node "SKILL_DIRECTORY/scripts/site-check.mjs" check --workspace "WORKSPACE" --urls "WORKSPACE/urls.json" --language en
```

Replace the paths with actual values. Reports go into the workspace's `site-checks/` folder.

## Requirements

OpenClaw with a connected model, Node.js 24.16+ or 26.1+, local command access and workspace read/write permission. Network access to the selected public HTTPS sources.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-site-check
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-site-check), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-site-check
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-site-check). Download the repository ZIP and copy `skills/mochi-site-check` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
