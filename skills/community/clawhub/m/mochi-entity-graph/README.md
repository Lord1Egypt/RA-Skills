# Entity Relationship Memory

[Simplified Chinese guide](README.zh-CN.md)

Store source-linked entities and relationships, traverse their connections and export a local graph.

## What it does

Store source-linked entities and relationships, traverse their connections and export a local graph.

## Examples

After installation, send an example with its required files or parameters.

```text
Store this project, its owner and customer with their stated source.
```

```text
Show the people and resources connected to this project.
```

```text
Export this agent’s relationship data for review.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

Use only user-authorized information in the active agent workspace. Ask before storing sensitive personal details. Relations are supplied facts, not inferred employment, trust or eligibility decisions.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-entity-graph
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
