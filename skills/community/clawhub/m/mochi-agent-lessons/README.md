# Agent Lessons Journal

[Simplified Chinese guide](README.zh-CN.md)

Record corrections with evidence, verify the fix and retrieve relevant lessons before another task.

## What it does

Record corrections with evidence, verify the fix and retrieve relevant lessons before another task.

## Examples

After installation, send an example with its required files or parameters.

```text
Record this command failure, its correction and supporting evidence.
```

```text
Find earlier lessons about CSV encoding.
```

```text
Append the successful retest evidence to this lesson.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

Only save corrections the user has asked to retain. Do not sweep chats or credentials, install hooks, rewrite system guidance, or claim one successful example proves a universal rule.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-agent-lessons
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
