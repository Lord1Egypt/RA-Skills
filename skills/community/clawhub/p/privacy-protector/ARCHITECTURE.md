# privacy-protector Architecture

## Goal

Keep `privacy-protector` focused on anonymize/deanonymize, deterministic local detection, and safe file projection workflows.

## Layout

```text
privacy-protector/
  SKILL.md
  ARCHITECTURE.md
  references/
    cli-contracts.md
    file-workflows.md
    local-detector.md
  examples/
    detect-local/
      allowlist.json
      blocklist.json
      thresholds.json
  scripts/
    anonymize.py
    deanonymize.py
    detect_local.py
    smoke_redact.sh
  modeio_redact/
    __init__.py
    adapters/
    assurance/
    cli/
      anonymize.py
      anonymize_output.py
      deanonymize.py
    core/
      models.py
      pipeline.py
      policy.py
      replacement.py
    detection/
      __init__.py
      data.py
      detect_local.py
    planning/
    providers/
    workflow/
  tests/
```

## Boundary Rules

- `modeio_redact/` is the reusable Python surface.
- `scripts/` are stable repo-local entrypoints and smoke helpers.
- `references/` keeps deep behavior/docs out of `SKILL.md`.
- `examples/` contains working config artifacts, not placeholder prose.
- `tests/` are maintainer regression coverage and stay out of the ClawHub upload surface.
- Middleware- and guardrail-specific behavior does not live in redact.

## Core Pipelines

- `core/pipeline.py` owns provider selection and file projection orchestration.
- `core/models.py` owns typed redact contracts used across pipeline stages.
- `detection/detect_local.py` owns detector execution logic.
- `detection/data.py` owns static detector rules/config tables.
- `workflow/*` owns file typing, map linkage, and persistence helpers.
- `adapters/*` isolates format-specific projection behavior for text, DOCX, and PDF.

## Public Surface

The package-level surface in `modeio_redact/__init__.py` intentionally exposes:

- `detect_sensitive_local`
- `RedactionProviderPipeline`
- `RedactionFilePipeline`
- `AssurancePolicy`
- shared redact contract models

That keeps downstream code from reaching through arbitrary internal modules when a stable surface is enough.

## Maintainer Validation Checklist

```bash
python3 -m unittest discover privacy-protector/tests -p "test_*.py"
python3 -m unittest discover privacy-protector/tests -p "test_smoke_matrix_extensive.py"
bash scripts/smoke_redact.sh
```
