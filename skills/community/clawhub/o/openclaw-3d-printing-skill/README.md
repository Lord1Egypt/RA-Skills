# OpenClaw 3D Printing Skill

An OpenClaw-native skill for designing **parametric 3D-printable parts** with **CadQuery**.

It helps an agent gather requirements, model physical parts parametrically, export STL or 3MF files, render previews, and iterate on fit, tolerances, and printability.

## Quick start

1. Install the skill from ClawHub or clone the repo into your OpenClaw skills directory.
2. Use **Python 3.10 to 3.12** only.
3. Install CadQuery using the platform guidance below.
4. Verify `import cadquery as cq` works before trying previews or exports.

## Install from ClawHub

```bash
openclaw skills install openclaw-3d-printing-skill
```

Or with the ClawHub CLI:

```bash
clawhub install openclaw-3d-printing-skill
```

## 5-minute setup

### macOS

```bash
git clone https://github.com/antoniosilveira/openclaw-3d-printing-skill.git ~/.openclaw/workspace/skills/openclaw-3d-printing-skill
cd ~/.openclaw/workspace/skills/openclaw-3d-printing-skill
brew install python@3.12
/opt/homebrew/bin/python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r references/requirements.txt
```

### Linux x86_64

```bash
git clone https://github.com/antoniosilveira/openclaw-3d-printing-skill.git ~/.openclaw/workspace/skills/openclaw-3d-printing-skill
cd ~/.openclaw/workspace/skills/openclaw-3d-printing-skill
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r references/requirements.txt
```

### Linux arm64 / Raspberry Pi

```bash
git clone https://github.com/antoniosilveira/openclaw-3d-printing-skill.git ~/.openclaw/workspace/skills/openclaw-3d-printing-skill
cd /tmp
curl -L micro.mamba.pm/install.sh | bash
source ~/.bashrc
micromamba create -n cadquery312 -c conda-forge python=3.12 cadquery -y
micromamba activate cadquery312
python -m pip install -r ~/.openclaw/workspace/skills/openclaw-3d-printing-skill/references/requirements.txt
```

## Install matrix

| Platform | Recommended Python | Recommended CadQuery install path |
|---|---|---|
| macOS | 3.12 | Homebrew Python + `venv` + `pip install -r references/requirements.txt` |
| Linux x86_64 | 3.12 | `venv` + `pip install -r references/requirements.txt` |
| Linux arm64 / Raspberry Pi | 3.12 | `micromamba` + `conda-forge` for CadQuery, then `pip install -r references/requirements.txt` |

## What it includes

- `SKILL.md` with trigger and workflow guidance
- `scripts/run_cadquery_model.py` for structured model execution and validation
- `scripts/preview.py` for preview rendering
- `scripts/mesh_io.py` for safe mesh loading
- `scripts/stl_to_3mf.py` for STL to 3MF conversion
- `references/design-review.md` for final review guidance
- `references/requirements.txt` for Python dependency expectations
- `examples/` for small prompt briefs

## Install in OpenClaw

Clone or copy this repository into your OpenClaw skills directory so the repo root itself is the skill folder.

Example:

```bash
git clone https://github.com/antoniosilveira/openclaw-3d-printing-skill.git ~/.openclaw/workspace/skills/openclaw-3d-printing-skill
```

OpenClaw should then discover the root `SKILL.md` automatically.

## Python and CadQuery requirements

Use **Python 3.10 to 3.12**. Python 3.13+ is not recommended for this skill yet because CadQuery wheel support is less reliable there.

This repo expects:
- a working CadQuery install
- the preview/export helper dependencies from `references/requirements.txt`
- an isolated environment instead of system Python

Before doing anything else, verify CadQuery imports cleanly in the environment you plan to use.

### Recommended install paths

- **macOS**: use Python 3.12 and a local `venv`
- **Linux x86_64**: try Python 3.12 and a local `venv` first
- **Linux arm64 / Raspberry Pi**: prefer **micromamba + conda-forge** for CadQuery

### macOS setup

Install Python 3.12 with Homebrew:

```bash
brew install python@3.12
```

Create a project-local environment and install dependencies:

```bash
cd ~/.openclaw/workspace/skills/openclaw-3d-printing-skill
/opt/homebrew/bin/python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r references/requirements.txt
```

Verify:

```bash
python - <<'PY'
import cadquery as cq
print("CadQuery OK", cq.__version__)
PY
```

### Linux setup (x86_64)

Install Python 3.12 using your distro package manager if available, then:

```bash
cd ~/.openclaw/workspace/skills/openclaw-3d-printing-skill
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r references/requirements.txt
```

Verify:

```bash
python - <<'PY'
import cadquery as cq
print("CadQuery OK", cq.__version__)
PY
```

### Linux setup (arm64 / Raspberry Pi)

CadQuery installation is usually more reliable through conda-forge than plain `pip` on arm64.

Install micromamba:

```bash
cd /tmp
curl -L micro.mamba.pm/install.sh | bash
source ~/.bashrc
```

Create the environment:

```bash
micromamba create -n cadquery312 -c conda-forge python=3.12 cadquery -y
micromamba activate cadquery312
python -m pip install -r ~/.openclaw/workspace/skills/openclaw-3d-printing-skill/references/requirements.txt
```

Verify:

```bash
python - <<'PY'
import cadquery as cq
print("CadQuery OK", cq.__version__)
PY
```

## First successful test

Run this after setup in the same environment you plan to use for the skill:

```bash
python - <<'PY'
import cadquery as cq
box = cq.Workplane("XY").box(10, 20, 5)
cq.exporters.export(box, "test_box.stl")
print("CadQuery OK", cq.__version__)
print("STL export OK")
PY
```

If that works, your CadQuery environment is ready for the skill.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'cadquery'` | CadQuery is not installed in the active environment | Activate the right `venv` or `micromamba` env and reinstall |
| `freecad_impl` or `No module named 'FreeCAD'` | You installed the legacy CadQuery 1.x package | Do not use plain `pip install cadquery`; use the recommended setup above |
| `ModuleNotFoundError: trimesh` | Preview/export helper dependencies are missing | Run `python -m pip install -r references/requirements.txt` |
| `python3.12: command not found` | Python 3.12 is not installed or not on PATH | Install Python 3.12 first, then recreate the environment |
| `micromamba: command not found` | Micromamba is not installed or shell is not initialized | Install micromamba, then `source ~/.bashrc` or initialize the shell hook |
| `micromamba activate ...` does not work | Shell hook is not loaded | Run `eval "$($HOME/.local/bin/micromamba shell hook --shell bash)"` |
| CadQuery installs on Linux arm64 but import still fails | Wheel/solver mismatch or wrong environment | Recreate the env with `micromamba create -n cadquery312 -c conda-forge python=3.12 cadquery -y` |

## Packaging the skill

You can validate and package the skill directly from the repo root:

```bash
python3 /path/to/openclaw/skills/skill-creator/scripts/package_skill.py . ./dist
```

That should produce a `.skill` artifact in `dist/`.

## Publish on ClawHub

Recommended publish metadata for this repo:

- **slug**: `openclaw-3d-printing-skill`
- **name**: `OpenClaw 3D Printing Skill`
- **version**: use semver like `1.0.0`, `1.0.1`, `1.1.0`
- **tags**: keep `latest`

Login first:

```bash
clawhub login
clawhub whoami
```

Then publish from the repo root:

```bash
clawhub skill publish . \
  --slug openclaw-3d-printing-skill \
  --name "OpenClaw 3D Printing Skill" \
  --version 1.0.0 \
  --tags latest \
  --changelog "Initial public release"
```

For later updates, bump the version and changelog:

```bash
clawhub skill publish . \
  --slug openclaw-3d-printing-skill \
  --name "OpenClaw 3D Printing Skill" \
  --version 1.0.1 \
  --tags latest \
  --changelog "Docs and install improvements"
```

## Example usage

See `examples/` for short briefs you can adapt:

- `examples/simple-bracket.md`
- `examples/enclosure-brief.md`

## Attribution

**Inspired by** the original Claude-oriented CAD skill from Flowful:

- [flowful-ai/cad-skill](https://github.com/flowful-ai/cad-skill)

This repository is an **OpenClaw-native adaptation** with its own packaging, layout, and workflow. It is **not an official fork** and is not affiliated with the original project.

## License

MIT. See `LICENSE`.
