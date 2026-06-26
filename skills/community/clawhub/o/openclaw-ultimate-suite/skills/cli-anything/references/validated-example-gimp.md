# Validated example: gimp harness

This is the first locally validated example for the OpenClaw `cli-anything` skill.

## What was verified

### Environment

- Python present: `Python 3.12.3`
- Local repo present: `/root/.openclaw/workspace/CLI-Anything`

### Python dependencies installed for the harness

Installed into the current machine Python environment:

- `Pillow`
- `numpy`
- `prompt_toolkit`

### Harness installation

Installed from:

- `/root/.openclaw/workspace/CLI-Anything/gimp/agent-harness`

Command used conceptually:

```bash
python3 -m pip install --break-system-packages -e /root/.openclaw/workspace/CLI-Anything/gimp/agent-harness
```

### Entry point verification

Verified command:

```bash
cli-anything-gimp --help
```

The CLI loaded successfully and exposed command groups including:

- `canvas`
- `draw`
- `export`
- `filter`
- `layer`
- `media`
- `project`
- `repl`
- `session`

### Minimal functional verification

Verified JSON project creation:

```bash
cli-anything-gimp --json project new --width 320 --height 240 -o /root/.openclaw/workspace/tmp-gimp-project.json
```

Observed result:

- JSON printed to stdout
- project file created successfully
- output file path:
  - `/root/.openclaw/workspace/tmp-gimp-project.json`

## Important note

The `gimp` harness is a good first demonstration target because it is runnable in the current environment after Python dependency installation.

However, its packaging/docs are not perfectly aligned:

- `setup.py` describes it as a GIMP batch-mode harness
- the README describes a Pillow-based image editing CLI

Treat this harness as:

- **validated enough for local demonstration**
- **not yet proof that every CLI-Anything harness exactly matches its stated backend model**

## Recommended use in the skill

When using the `cli-anything` method skill:

1. Prefer `gimp` as the first runnable example
2. Use it to demonstrate harness inspection, installation, and entry-point checks
3. Avoid over-claiming that all bundled harnesses are equally verified until they are tested one by one
