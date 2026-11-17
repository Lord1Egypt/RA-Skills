# Task Checkpoint and Handoff

[Simplified Chinese guide](README.zh-CN.md)

Save task checkpoints and file hashes, then resume with a clear next-step list and stale-file warnings.

## What it does

Save task checkpoints and file hashes, then resume with a clear next-step list and stale-file warnings.

## Examples

After installation, send an example with its required files or parameters.

```text
Save a checkpoint with completed work and the next steps.
```

```text
Resume the checkpoint and check whether its source files changed.
```

```text
Export a task handoff note with goals and blockers.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

A checkpoint is context, not proof that unfinished work is complete. Recheck stale inputs. No autonomous scheduling, cross-agent access, prompt-file replacement or external messaging is performed.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-task-handoff
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
