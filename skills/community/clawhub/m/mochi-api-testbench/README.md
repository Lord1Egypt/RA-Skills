# API Testbench

[Simplified Chinese guide](README.zh-CN.md)

Run request suites with status, JSON, header and latency assertions and compare regression reports.

## Features

Run request suites with status, JSON, header and latency assertions and compare regression reports.

Runs in the active agent workspace and saves results and reports while preserving source files.

## Usage examples

After installation, send an example to your AI with the relevant files or URLs.

```text
Test these public endpoints for HTTP200 and the JSON success field.
```

```text
Use my environment-based token and keep credentials and response bodies out of the report.
```

```text
Compare today’s API results with the previous report for regressions and latency changes.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-api-testbench
```

Alternatively, get the ZIP on this page and place its Skill folder in the active workspace's `skills/` directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
