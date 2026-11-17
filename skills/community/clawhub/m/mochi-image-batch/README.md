# Batch Image Processing

[Simplified Chinese guide](README.zh-CN.md)

Batch resize, crop, pad, compress, convert and watermark images, with contact sheets and downloadable results.

## Features

Batch resize, crop, pad, compress, convert and watermark images, with contact sheets and downloadable results.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Resize images in my specified directory to a maximum edge of 1200 pixels, preserve proportions, and save to a new directory.
```

```text
Convert these images to WebP, preserve transparency, and generate a processing manifest.
```

```text
Add my text watermark to these product images, show two previews first, and batch-process after confirmation.
```

Outputs processed images, a contact sheet, manifest and ZIP. Original files are retained.

## Requirements

OpenClaw, a connected model, active-workspace access; Python 3.10+, Pillow 12.3+

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-image-batch
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-image-batch), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-image-batch
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-image-batch). Download the repository ZIP and copy `skills/mochi-image-batch` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
