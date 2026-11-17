# Document Templates and Batch Output

[Simplified Chinese guide](README.zh-CN.md)

Generate notices, certificates and business documents from DOCX, text or HTML templates, validate fields and retain Word run formatting.

## Features

Generate notices, certificates and business documents from DOCX, text or HTML templates, validate fields and retain Word run formatting.

Runs in the active agent workspace with local state. Supply your own account settings for mail, cloud storage or calendars. Scheduled notifications use OpenClaw scheduling.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Read the uploaded notice.docx template, list all {{fields}}, and tell me which values are missing.
```

```text
Fill certificate.docx from each row of this people CSV, creating one document per person while preserving formatting.
```

```text
Fill the HTML notice template with my title, date and body, and save a new file.
```

## Requirements

Python 3.10+; python-docx>=1.2,<2

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-document-templates
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-document-templates), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-document-templates
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-document-templates). Download the repository ZIP and copy `skills/mochi-document-templates` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
