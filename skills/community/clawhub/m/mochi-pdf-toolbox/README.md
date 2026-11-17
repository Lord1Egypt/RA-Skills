# PDF Toolbox

[Simplified Chinese guide](README.zh-CN.md)

Merge, split, select, reorder, rotate and compress PDFs; convert images, render previews and inspect blank pages.

## Features

Merge, split, select, reorder, rotate and compress PDFs; convert images, render previews and inspect blank pages.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Merge my two uploaded PDFs in upload order and produce a new PDF with page previews.
```

```text
Extract pages 2 through 5 of this PDF, rotate original page 3 clockwise by 90 degrees, and save a new file.
```

```text
Convert these images into a PDF in filename order, check for blank pages, and report the results.
```

Outputs PDFs or page images, a processing manifest and previews. Multiple results include a ZIP; source files are retained.

## Requirements

OpenClaw, a connected model, active-workspace access; Python 3.10+, pypdf 6.10+, pypdfium2 5.14+, Pillow 12.3+

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-pdf-toolbox
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-pdf-toolbox), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-pdf-toolbox
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-pdf-toolbox). Download the repository ZIP and copy `skills/mochi-pdf-toolbox` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
