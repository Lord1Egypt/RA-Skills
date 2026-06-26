---
name: hermes-dashboard-extension-builder
description: Generate and validate Hermes-style dashboard extension scaffolds: themes, plugins, custom tabs, slots, and backend API route manifests for OpenClaw/Hermes agent teams.
---

# Hermes Dashboard Extension Builder

Use this skill when a team wants a packaged dashboard extension scaffold instead of hand-rolling UI folders and manifests.

## Workflow

1. Prepare a JSON spec or provide command-line arguments for a tab/plugin.
2. Run `scripts/hermes_dashboard_extension_builder.py` into a staging directory.
3. Review the generated `extension.json`, frontend stub, API route stub, and validation report.
4. Hand the scaffold to a UI developer or Hermes/OpenClaw dashboard integrator.

## Parameters

- `--name NAME`: Extension name, hyphen-case recommended.
- `--tab TITLE`: Dashboard tab label.
- `--slot SLOT`: UI slot, default `main-panel`.
- `--api-route PATH`: Backend route path, default `/api/<name>`.
- `--spec PATH`: Optional JSON spec overriding CLI values.
- `--output-dir DIR`: Destination directory.
- `--validate-only`: Validate spec without writing scaffold.

## Outputs

- `extension.json`: Manifest for tab/plugin/route metadata.
- `frontend/<name>.html`: Minimal dashboard tab stub.
- `backend/<name>_route.py`: Safe stdlib route handler stub.
- `VALIDATION.json`: Findings and readiness verdict.

The script writes only to the selected output directory.
