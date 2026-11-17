# Log Diagnostics Toolbox

[Simplified Chinese guide](README.zh-CN.md)

Analyze access, JSONL application and GZIP logs for errors, HTTP status, popular routes and time patterns.

## Features

Analyze access, JSONL application and GZIP logs for errors, HTTP status, popular routes and time patterns.

Runs in the active agent workspace and saves results and reports while preserving source files.

## Usage examples

After installation, send an example to your AI with the relevant files or URLs.

```text
Analyze this access log and report the most frequent 404 and 500 routes.
```

```text
Show errors by hour and the most common failure signatures.
```

```text
Inspect these compressed logs, exclude likely bots and count routes and unique IPs.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-log-diagnostics
```

Alternatively, get the ZIP on this page and place its Skill folder in the active workspace's `skills/` directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
