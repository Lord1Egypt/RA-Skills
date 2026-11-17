# Document Reading and Questions

[Simplified Chinese guide](README.zh-CN.md)

Read DOCX and text, search across files and export extracted text and line-cited evidence.

## What it does

Read DOCX and text, search across files and export extracted text and line-cited evidence.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Read the uploaded notice.docx and list required actions and deadlines with source locations.
```

```text
Find refund conditions across these text files and quote the source with filenames and line numbers.
```

```text
Export this DOCX as text and generate a key-evidence list with line numbers.
```

## Exported files

document.txt / source.json / evidence.md / citations.json

Files stay in the active agent workspace, with paths and SHA256 receipts. Existing records and earlier exports are retained.

## Requirements

OpenClaw, a connected model, Node.js 24.16+ and active-workspace read/write access. DOCX is read locally; PDF and images use available host readers.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-document-reader
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-document-reader), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-document-reader
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-document-reader). Download the repository ZIP and copy `skills/mochi-document-reader` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
