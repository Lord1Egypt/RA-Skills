---
name: privacy-protector
description: >-
  Runs PII anonymization, local de-anonymization, and deterministic local
  detector checks for text and supported files. Use for redact/restore flows,
  file-first anonymization, or offline detector tuning with allowlist,
  blocklist, and threshold controls.
version: 0.1.0
metadata:
  clawdbot:
    homepage: https://github.com/mode-io/mode-io-skills/tree/main/privacy-protector
    requires:
      bins:
        - python3
---

# Run anonymization and restore flows

Use this skill when you need to anonymize text/files, restore placeholders with a saved map, or tune the local detector.

Maintainer-only validation assets are excluded from ClawHub uploads.

## Scope

- Included:
  - anonymize (`scripts/anonymize.py`)
  - deanonymize (`scripts/deanonymize.py`)
  - local detector diagnostics (`scripts/detect_local.py`)
  - file/map workflow helpers behind those entrypoints
- Not included:
  - request/response gateway routing (`modeio-middleware`)
  - command safety analysis (`security`)
  - staged-diff or git pre-commit scanning

## Working directory

Run these commands from inside the `privacy-protector` folder.

## Requirements

- Hard requirement: `python3`
- Optional package: `requests` for API-backed `dynamic`, `strict`, and `crossborder`
- Optional package: `python-docx` for `.docx`
- Optional package: `PyMuPDF` for `.pdf`
- Optional override: `ANONYMIZE_API_URL` for non-`lite` levels
- Optional override: `MODEIO_REDACT_MAP_DIR` for local map storage

## Core commands

### Anonymize text

```bash
python3 scripts/anonymize.py \
  --input "Email: alice@example.com, Phone: 415-555-1234" \
  --level lite \
  --json
```

### Anonymize a file

```bash
python3 scripts/anonymize.py \
  --input ./incident.docx \
  --level lite \
  --json
```

### Restore from a saved map

```bash
python3 scripts/deanonymize.py \
  --input "Email: [EMAIL_1]" \
  --map ~/.modeio/redact/maps/<map-id>.json \
  --json
```

### Tune the local detector

```bash
python3 scripts/detect_local.py \
  --input "Project codename Phoenix is approved. Reach support@example.com." \
  --allowlist-file examples/detect-local/allowlist.json \
  --blocklist-file examples/detect-local/blocklist.json \
  --thresholds-file examples/detect-local/thresholds.json \
  --json
```

## Runtime notes

- `lite` runs fully local. `dynamic`, `strict`, and `crossborder` call the backend API
- For `crossborder`, pass both `--sender-code` and `--recipient-code`
- Supported file inputs: `.txt`, `.md`, `.markdown`, `.csv`, `.tsv`, `.json`, `.jsonl`, `.yaml`, `.yml`, `.xml`, `.html`, `.htm`, `.rst`, `.log`, `.docx`, `.pdf`
- Saved maps default to `~/.modeio/redact/maps`; use `MODEIO_REDACT_MAP_DIR` to override that location
- Text-like outputs get embedded map markers or sidecar `.map.json` references when needed
- `.pdf` supports anonymization only; de-anonymization is not supported
- Rich-file outputs keep assurance metadata in the JSON response so callers can decide how strict they want to be
- Use `--json` when you want the stable machine-readable envelope and file workflow metadata

## Resources

- `ARCHITECTURE.md` for package boundaries
- `references/cli-contracts.md` for flags and output contracts
- `references/file-workflows.md` for map linkage and assurance behavior
- `references/local-detector.md` for profiles and shipped config examples
- `examples/detect-local/` for ready-to-edit tuning files

## When not to use

- Middleware interception or policy routing
- Safety approval/block decisions
