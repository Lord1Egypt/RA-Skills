# MochiLab Skills assistant

[Simplified Chinese guide](README.zh-CN.md)

Find, install and maintain MochiLab Skills in chat, check dependencies, run packaged tests, preserve configuration and roll back versions.

## Features

Find and install MochiLab Skills, verify package files, and check runtimes and dependencies. Select runtime executables, run packaged tests, check updates and restore earlier versions. Configuration stays outside package folders and survives updates. Modified local files are flagged for review.

## Usage examples

After connecting the assistant, send any example below to your AI.

```text
Install MochiLab Translation QA, check its dependencies and run its packaged tests. Show the version, installation path and test results.
```

```text
Check my installed MochiLab Skills for updates and list the version changes first. After I choose, update them and run tests.
```

```text
This MochiLab Skill failed to run. Check its configuration and dependencies while preserving my files. If rollback is needed, list available earlier versions first.
```

## Getting started

Connect your account using the [setup guide](https://mochilab.bz/Skills/Connect.aspx?lang=en), then describe the task in your current agent conversation. Start a new conversation after adding a Skill.

Reports distinguish passed packaged tests, syntax-only checks, missing dependencies and failures. Email, cloud services and reminders also require their account configuration and a test of the intended real task.

## Requirements

OpenClaw, a connected model, Node.js 24.16+ or 26.1+, HTTPS access and workspace write permission.

## Installation and first use

### MochiLab Skills assistant

[Install and connect your account](https://mochilab.bz/Skills/Connect.aspx?lang=en).

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochilab-skills), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochilab-skills
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochilab-skills). Download the repository ZIP and copy `skills/mochilab-skills` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.
ClawHub and GitHub installs also need a [MochiLab account connection](https://mochilab.bz/Skills/Connect.aspx?lang=en).

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
