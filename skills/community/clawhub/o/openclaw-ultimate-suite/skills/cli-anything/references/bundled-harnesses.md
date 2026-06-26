# Bundled harnesses in CLI-Anything

Use this as a quick map before reading a specific harness deeply.

## Included examples observed in the local repo

- `gimp/agent-harness`
- `blender/agent-harness`
- `inkscape/agent-harness`
- `audacity/agent-harness`
- `libreoffice/agent-harness`
- `obs-studio/agent-harness`
- `kdenlive/agent-harness`
- `shotcut/agent-harness`
- `zoom/agent-harness`
- `drawio/agent-harness`
- `anygen/agent-harness`

## Common structure to expect

Most examples contain:

- `setup.py`
- a PEP 420 namespace package under `cli_anything/<software>/`
- a software-specific SOP like `GIMP.md` or `LIBREOFFICE.md`
- `tests/test_core.py`
- `tests/test_full_e2e.py`
- `tests/TEST.md`

## What to verify before claiming one is usable

1. The target software/backend is installed
2. The Python package can be installed or imported
3. The console entry point resolves
4. A minimal command works
5. Any E2E claim uses the real software backend, not only synthetic tests

## Recommended first targets

If you need a smaller proof-of-concept, start with examples that look structurally complete and have straightforward file-based workflows, such as:

- `gimp`
- `inkscape`
- `libreoffice`

More environment-sensitive examples may need extra services, APIs, or media tools.
