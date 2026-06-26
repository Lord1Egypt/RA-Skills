# Knowledge Distillation

Distill OpenClaw daily memory, session transcripts, and newly generated report files into new knowledge points and deeper knowledge leads.

## Overview

This skill scans agent-native working materials, identifies what is newly learned, and separates that from what should be investigated, connected, or strengthened next.

## Installation

Place this skill directory in your skills folder.

## Usage

See SKILL.md for detailed usage instructions.

Quick start:

```bash
bash scripts/distill.sh ./memory ./dist
KNOWLEDGE_DISTILLATION_MEMORY_DIR=./memory KNOWLEDGE_DISTILLATION_OUTPUT_DIR=./dist bash scripts/distill.sh
```

The script creates a dated Markdown draft. The agent still needs to review the
source material and replace TODO entries with evidence-backed knowledge points.

## Scripts

- `scripts/distill.sh` - Run knowledge distillation on memory files
- `scripts/test.sh` - Run tests for this skill

Run before publishing:

```bash
bash scripts/test.sh
```

## References

- `references/output-templates.md` - Output templates for different distillation scenarios
