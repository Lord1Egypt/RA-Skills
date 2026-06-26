---
name: nix-run
description: 'Execute **ANY** command via Nix, regardless of whether it is installed or the local version is outdated. Access 100,000+ packages from nixpkgs-unstable with zero installation. Supports multi-package environments via --shell for tasks requiring multiple tools simultaneously. Use proactively before running CLI tools, or reactively when commands fail with "command not found" or produce wrong results due to version issues.'
---

# nix-run — Universal CLI Tool Runner via Nix

Automatically find and run **any** CLI tool through Nix with zero configuration. If the tool is installed locally, it runs directly with no overhead. If not, it auto-fetches from nixpkgs (100,000+ packages) on the fly.

## CRITICAL RULES

1. **ALWAYS run CLI tools through `scripts/nix-run.sh`** — even if you think the tool might already be installed. The script checks locally first (zero overhead) and auto-fetches via nix only if missing.
2. **NEVER install packages** via `apt`, `brew`, `pip install`, `npm install -g`, `cargo install`, or any other package manager. This system uses nix exclusively.
3. **NEVER suggest the user install anything.** Just run it through nix-run.
4. **NEVER use `nix shell` or `nix run` directly.** Always go through `scripts/nix-run.sh` which handles package detection automatically. For multi-package environments, use `--shell`.
5. **On "command not found"**: Do NOT advise installation. Immediately retry through `scripts/nix-run.sh`.
6. **When unsure which tool to use**: Use `--search` to discover the right package, then run it.

## Quick Start

```bash
# Run ANY command — auto-detects package, zero config
scripts/nix-run.sh <command> [args...]

# Multi-package environment — run command with multiple tools available
scripts/nix-run.sh --shell <pkg1,pkg2,...> -- <command> [args...]

# Don't know the command name? Search by keyword
scripts/nix-run.sh --search "<keyword>"

# Update nix-locate database to get latest package info
scripts/nix-run.sh --update
```

## Workflows

### Workflow 1: Automatic Recovery from "command not found"

When a bash command fails with "command not found", **immediately** retry through nix-run — do NOT suggest installing:

```bash
# WRONG: "You need to install jq first: apt install jq"
# WRONG: brew install jq
# WRONG: nix shell nixpkgs#jq -c jq ...
# RIGHT:
scripts/nix-run.sh jq '.name' data.json
```

### Workflow 2: Proactive Use — Always Prefer nix-run

For **any** CLI tool, always go through nix-run first:

```bash
scripts/nix-run.sh pandoc README.md -o README.pdf
scripts/nix-run.sh fd '\.rs$' src/
scripts/nix-run.sh rg 'TODO' .
scripts/nix-run.sh ffmpeg -i input.mp4 output.gif
scripts/nix-run.sh htop
scripts/nix-run.sh tree -L 2
scripts/nix-run.sh imagemagick convert input.png output.jpg
scripts/nix-run.sh shellcheck script.sh
```

### Workflow 3: Discover Tools by Keyword

When you need a CLI tool but don't know its name, search nixpkgs:

```bash
scripts/nix-run.sh --search "json processor"
#   jq (1.8.1) - Lightweight and flexible command-line JSON processor
#   njq (...) - Command-line JSON processor using nix as query language

# Then run the discovered tool:
scripts/nix-run.sh jq '.name' data.json
```

### Workflow 4: Handling Multiple Candidates

When multiple packages provide the same command, nix-run lists candidates and exits. Re-run with `--pkg`:

```bash
scripts/nix-run.sh --pkg ffmpeg-headless ffmpeg -version
```

### Workflow 5: Multi-Package Environment with --shell

When a task requires multiple tools available simultaneously (e.g., a Python script that calls node, or a build step needing several compilers):

```bash
# Run a Python script that also needs node available
scripts/nix-run.sh --shell python3,nodejs -- python3 script.py

# Run multiple commands in a combined environment
scripts/nix-run.sh --shell python3,nodejs -- bash -c 'python3 --version && node --version'

# Data pipeline with jq and curl
scripts/nix-run.sh --shell jq,curl -- bash -c 'curl -s https://api.example.com | jq .data'
```

## Options

| Flag                   | Description                                                    |
| ---------------------- | -------------------------------------------------------------- |
| `--pkg <name>`         | Skip auto-detection, use specified nix package                 |
| `--shell <pkg1,...>`   | Multi-package environment (comma-separated), use `--` before command |
| `--search <keyword>`   | Search nixpkgs by keyword (returns package name + description) |
| `--limit <N>`          | Max search results (default: 20)                               |
| `--update`             | Update nix-locate database (nix-index) to latest nixpkgs       |

## How It Works

1. Command exists locally → execute directly (zero overhead)
2. `--pkg` specified → `nix shell github:NixOS/nixpkgs/nixpkgs-unstable#<pkg> -c <cmd> <args>`
3. `--shell` specified → `nix shell nixpkgs#pkg1 nixpkgs#pkg2 ... -c <cmd> <args>`
4. Otherwise → `nix-locate` to find the package providing `/bin/<cmd>`
5. Single candidate or exact match → run automatically
6. Multiple candidates → list them and exit (re-run with `--pkg`)

**Note:** All commands use `nixpkgs-unstable` flake reference to ensure latest package versions.

## Edge Cases

- **Command not in nixpkgs**: Exits with error. Use `--search` to find alternatives.
- **nix-locate not installed**: Exits with instructions to install nix-index.
- **nix-locate database outdated**: Run `scripts/nix-run.sh --update` to refresh.
- **Software versions too old**: The script uses `nixpkgs-unstable` by default, ensuring latest versions. If versions still seem stale, run `--update` to refresh the nix-locate index.
- **First run may be slow**: `nix shell` downloads on first use; subsequent runs use cache.
