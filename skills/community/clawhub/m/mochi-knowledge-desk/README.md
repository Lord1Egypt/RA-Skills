# Local Knowledge Desk

[Simplified Chinese guide](README.zh-CN.md)

Incrementally index local documents, search Chinese and English text, and return source snippets with file hashes.

## Features

Incrementally index local documents, search Chinese and English text, and return source snippets with file hashes.

Runs in the active agent workspace and saves results and reports while preserving source files.

## Usage examples

After installation, send an example to your AI with the relevant files or URLs.

```text
Index my docs folder and update only changed files on later runs.
```

```text
Search the library for refund conditions and return snippets with source citations.
```

```text
Check whether the sources behind these results changed and export the index.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-knowledge-desk
```

Alternatively, get the ZIP on this page and place its Skill folder in the active workspace's `skills/` directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
