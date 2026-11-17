# Word Document Composer

[Simplified Chinese guide](README.zh-CN.md)

Create real DOCX documents with headings, paragraphs, bullets and tables, and inspect document text structure.

## What it does

Create real DOCX documents with headings, paragraphs, bullets and tables, and inspect document text structure.

## Examples

After installation, send an example with its required files or parameters.

```text
Turn this material into a Word document with headings and tables.
```

```text
Create a bilingual project brief with clear sections.
```

```text
Inspect this DOCX’s paragraphs and table structure.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

Verify the generated file in Word/LibreOffice or an available renderer before claiming visual layout is approved. Does not edit tracked changes, preserve an existing template, embed images, or export PDF. Inspection is structural, not visual verification.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-docx-composer
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
