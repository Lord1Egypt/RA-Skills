# Manuscript Math, DOCX, and Visual QC Agent Skill

An agent-agnostic manuscript QC skill/playbook for OpenClaw, Hermes, Claude, Codex, and other coding or research agents working with Markdown, LaTeX-style math, figures, tables, DOCX export, PDF conversion, or submission-package synchronization.

This is designed for practical manuscript production work: inspect the source, rebuild the DOCX/PDF, render pages, catch formula/table/figure issues, and verify that the final upload package is not stale.

## What It Helps Catch

- Mathematical variables accidentally written as code spans instead of math.
- Multi-letter variables that render as spaced letters in Word/PDF conversion.
- Figures that look fixed in source folders but remain stale inside the DOCX.
- Wide tables that overflow or become unreadable after DOCX export.
- Upload packages that still contain old manuscript or figure assets.

## Repository Contents

- `SKILL.md` - the portable skill/playbook file. Codex can load it as a skill; other agents can read it directly as task instructions.
- `AGENTS.md` - a generic agent entrypoint for OpenClaw, Hermes, Claude, Codex-style agents, and repository-aware assistants.
- `examples/minimal/manuscript.md` - a small manuscript source with good and risky formula patterns.
- `examples/minimal/qc_commands.sh` - example commands for DOCX/PDF conversion and visual checks.
- `LICENSE` - MIT-0 license, matching ClawHub's published-skill licensing.

## Agent Usage

Use the file that fits your agent runtime:

- OpenClaw / repository-aware agents: keep this repository in the workspace and let the agent read `AGENTS.md`.
- Hermes / Claude / chat agents: paste or attach `SKILL.md`, or point the agent to this repository and ask it to follow `SKILL.md`.
- Codex-style skill loaders: copy the directory into the skill folder expected by that runtime.

Example for Codex-compatible local skill folders:

```bash
mkdir -p ~/.codex/skills
cp -R manuscript-math-docx-qc ~/.codex/skills/
```

Example prompt for any agent:

```text
Use the manuscript-math-docx-qc skill/playbook to check this manuscript before DOCX/PDF submission.
```

## Typical Workflow

1. Locate the authoritative source file and figure/table scripts.
2. Search for formula-risk patterns before editing exported files.
3. Rebuild the DOCX from source.
4. Validate the DOCX archive with `unzip -t`.
5. Convert DOCX to PDF with LibreOffice.
6. Render PDF pages to images for visual inspection.
7. Fix formulas, figures, or tables at source level.
8. Sync the final files into the upload package and test the zip.

## Dependencies

The skill can be adapted to different environments. The example commands assume:

- `pandoc`
- LibreOffice `soffice`
- Poppler tools such as `pdfinfo` and `pdftoppm`
- `rg`
- `zip` and `unzip`

## Privacy

This repository intentionally avoids project-specific manuscript titles, local paths, author details, unpublished findings, or submission package names. Keep future examples generic and synthetic.
