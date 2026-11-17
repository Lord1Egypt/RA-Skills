# Skill Package Inspector

[Simplified Chinese guide](README.zh-CN.md)

Inspect a Skill ZIP without executing it: archive boundaries, executable/network indicators and per-file hashes.

## What it does

Inspect a Skill ZIP without executing it: archive boundaries, executable/network indicators and per-file hashes.

## Examples

After installation, send an example with its required files or parameters.

```text
Inspect this Skill ZIP before installation; do not execute its code.
```

```text
List the package files and SHA256 hashes.
```

```text
Summarize the indicators that need manual review.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

Do not install or execute an inspected package as part of inspection. Indicators can be false positives and static checks can miss harmful behaviour. A clean report is not approval or certification.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-skill-inspector
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
