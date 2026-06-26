# Publishing to ClawHub

Skill slug: `paper-deep-reading-teaching-explainer`
Version: `10.1.8`
License: `MIT-0`
Primary metadata source: `SKILL.md` YAML frontmatter

## Package contents

The package is a skill folder containing:

- `SKILL.md`
- `README.md`
- `_meta.json`
- `workflow/`
- `schemas/`
- `scripts/`
- publish-page and security notes

The upload zip intentionally excludes `.clawhubignore` and `LICENSE` because ClawHub may reject extensionless or dotfiles during non-text-file validation. MIT-0 remains declared in metadata and documentation.

## Recommended publish command

```bash
clawhub skill publish ./paper-deep-reading-teaching-explainer --version 10.1.8
```

## Pre-publish checklist

- `SKILL.md` starts with YAML frontmatter containing `name`, `description`, and `version`.
- Folder name is lowercase and URL-safe: `paper-deep-reading-teaching-explainer`.
- License is declared as MIT-0 in metadata and documentation.
- No generated images, PDFs, large binaries, or paper PDFs are included in the package.
- Optional helper scripts are transparent and local-only.
- Visual generation instructions clearly separate report generation, image generation, and final PDF assembly.
