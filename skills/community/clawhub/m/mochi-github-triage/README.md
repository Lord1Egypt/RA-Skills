# GitHub Issue Triage Desk

[Simplified Chinese guide](README.zh-CN.md)

Triage a single repository’s exported issues or PRs for unassigned, stale and similar-title items without remote changes.

## What it does

Triage a single repository’s exported issues or PRs for unassigned, stale and similar-title items without remote changes.

## Examples

After installation, send an example with its required files or parameters.

```text
Triage these exported issues for stale, unassigned work.
```

```text
List open issues with no assignee and their last update.
```

```text
Find similar-title candidates without closing or labeling anything.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

If gh is already authenticated, export read-only data using gh issue list --repo OWNER/REPO --state all --limit 500 --json number,title,url,updatedAt,state,labels,assignees. Save its JSON in the workspace. Do not log tokens or create comments, labels, closes or PR merges. gh login and private repository access follow the user’s authorization.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-github-triage
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
