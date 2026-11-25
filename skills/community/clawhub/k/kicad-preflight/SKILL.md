---
name: kicad-preflight
description: Check a KiCad project before exporting Gerbers or ordering a board — schematic versus PCB mismatches, parts with no footprint, footprint disagreements, BOM quantity and reference errors, missing part numbers, obsolete or low-stock parts. Use when asked to check, review or preflight a KiCad project (.kicad_sch, .kicad_pcb, .kicad_pro), when checking a BOM CSV from any EDA tool (KiCad, Altium, Eagle, EasyEDA, JLCPCB) before ordering parts, or before a PCB order. Not for general electronics or circuit design review, for checking AI-agent skills (use skillscan), or for live distributor stock and price lookups.
license: MIT
compatibility: Requires Python 3.10+ and pip. KiCad itself is not required. Installing needs network access to GitHub; the checks run fully offline by default.
---

# KiCad Preflight

## What this tool does

KiCad Preflight reads a KiCad project (or a standalone BOM CSV from any
EDA tool) and gives one plain-English report — PASS, CAUTION, or BLOCK —
from deterministic checks: schematic ↔ PCB agreement, BOM sanity, and
offline part-risk flags. Every finding names the exact part and the
values that disagree. The same project always gets the same answer, and
project files are only parsed, never executed or modified.

## Install

```bash
pip install git+https://github.com/RakTikoo/kicad-preflight
```

This provides the `kicad-preflight` command (standard library only).

## Run

Check a KiCad project folder:

```bash
kicad-preflight path/to/project-folder
```

Check a lone BOM CSV (BOM checks only, any EDA tool):

```bash
kicad-preflight path/to/bom.csv
```

Machine-readable report: add `--format json`. Other formats:
`--format md` and `--format sarif`. The target may also be a single
`.kicad_pro`, `.kicad_sch` or `.kicad_pcb` file inside a project.

## Reading the results

The exit code is the verdict:

- `0` — PASS: no findings in what was checked.
- `1` — CAUTION: warnings worth a human look before ordering.
- `2` — BLOCK: at least one serious disagreement (a schematic part with
  no PCB footprint, a footprint mismatch, a BOM quantity or reference
  error, an obsolete part).
- `3` — usage error: bad path, bad flags, or a bad `--dataset` file.
  The CLI prints a message, never a traceback; no verdict was produced.

Findings print as severity, rule name, file and part reference, with the
values that disagree. Every report ends with a Coverage section: files
parsed, parts counted, BOM rows, parse errors, and whether KiCad's own
`kicad-cli` checks ran. A PASS only covers what was checked — if
something that exists could not be checked, the report carries a
`SCAN_INCOMPLETE` or `BOM_MISSING` finding instead of passing silently.
The JSON report carries `verdict`, `findings`, `coverage`, `project`
and `folder`.

## Limits

- The bundled part dataset is a small sample snapshot (2026-11-09):
  statuses and stock numbers are illustrative, not live distributor
  data. A part absent from the dataset is reported as "could not
  check", never guessed at. Live data needs `--online` with API keys.
- Without `kicad-cli` on PATH there is no official DRC/ERC; the report's
  Coverage section says which mode ran.
- Built-in geometry checks are a labelled subset (clearances,
  copper-to-edge, outline closure) — not full spatial DRC.
- One project per folder; KiCad 5 and older `.sch` files are reported
  as unsupported, not misread.
- Gerber package checks are file-level only; Gerber and drill contents
  are never parsed.
