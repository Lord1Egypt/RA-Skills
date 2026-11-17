# HTML Slide Storyboard

[Simplified Chinese guide](README.zh-CN.md)

Build self-contained HTML slides with bilingual text, navigation, speaker notes, print styles and a Markdown outline.

## What it does

Build self-contained HTML slides with bilingual text, navigation, speaker notes, print styles and a Markdown outline.

## Examples

After installation, send an example with its required files or parameters.

```text
Turn these talking points into HTML slides with speaker notes.
```

```text
Create a bilingual product outline and slide deck.
```

```text
Make five concise slides with a printable presentation file.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

Use when the user accepts an HTML presentation. If they explicitly need PPTX, use an available PPTX tool or explain the missing capability. Check browser and print layout; HTML generation alone is not visual approval.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-slide-storyboard
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
