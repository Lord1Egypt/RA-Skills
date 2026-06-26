# Image to Editable PPT Slide

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](#changelog) [![Skill](https://img.shields.io/badge/OpenClaw-skill-6f42c1.svg)](./SKILL.md)

Rebuild one or more reference images as visually matching editable PowerPoint slides using native shapes, text, fills, and layout instead of a flat screenshot.

## What it does

- recreates a source image as an **editable** PowerPoint slide
- supports **single-slide** and **multi-slide** decks
- includes reusable local helper scripts
- prefers editable shapes and text over embedding a flat screenshot

## Included files

- `SKILL.md`
- `CHANGELOG.md`
- `EXAMPLES.md`
- `PUBLISH.md`
- `scripts/pptx_rebuilder.py`
- `scripts/generate_spec_template.py`

## Installation

Copy this skill folder into your OpenClaw skills directory or publish it to ClawHub.

## Usage

Generate a starter JSON spec:

```bash
python scripts/generate_spec_template.py --title "Sample Deck" --slides 2 --output sample_spec.json
```

Build a PPTX from the spec:

```bash
python scripts/pptx_rebuilder.py sample_spec.json output.pptx
```

## Security & Privacy

- built-in helper scripts operate locally
- no external endpoints are called by default
- no environment variables are required in the current version
- local files are read and local output files are written

## Trust Statement

This skill is intended for local PowerPoint reconstruction workflows. It does not send data to third-party services in its built-in form. Only install it if you trust the skill contents and your local environment.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).
