---
name: gitignore-gen
description: Generate .gitignore files for any project type using GitHub's 200+ official templates. Use when creating new projects, setting up repositories, needing to combine multiple gitignore templates (e.g., Python + Node + JetBrains), auto-detecting project types, or adding custom ignore rules. Supports listing, filtering, combining templates, auto-detection, appending to existing files, and custom patterns.
---

# Gitignore Generator

Generate .gitignore files from GitHub's official template collection. Combine multiple templates, auto-detect project type, add custom rules.

## Quick Start

```bash
# List all available templates
python3 scripts/gitignore_gen.py list

# Generate for a Python project
python3 scripts/gitignore_gen.py generate Python --force

# Combine multiple templates
python3 scripts/gitignore_gen.py generate Python Node JetBrains --force

# Auto-detect project type
python3 scripts/gitignore_gen.py detect /path/to/project
```

## Commands

### list
List all 200+ available templates. Filter with `--filter`:
```bash
python3 scripts/gitignore_gen.py list --filter java
```

### generate
Create a .gitignore from one or more templates:
```bash
python3 scripts/gitignore_gen.py generate Python Node --stdout     # print to stdout
python3 scripts/gitignore_gen.py generate Rust -o /tmp/.gitignore  # custom output path
python3 scripts/gitignore_gen.py generate Go --append              # append to existing
python3 scripts/gitignore_gen.py generate Swift --extra '*.local' --extra 'secrets/'
```

### detect
Auto-detect project type from files in a directory:
```bash
python3 scripts/gitignore_gen.py detect           # current directory
python3 scripts/gitignore_gen.py detect ~/myproj   # specific path
```

Detects: Node, Python, Ruby, Rust, Go, Java, PHP/Composer, Dart, Elixir, Swift, Terraform, Docker, JetBrains, VS Code, and more.

## Flags
- `--stdout` — Print to stdout instead of writing a file
- `--force` — Overwrite existing .gitignore
- `--append` / `-a` — Append to existing .gitignore
- `--output` / `-o` — Custom output file path
- `--extra` / `-e` — Add custom ignore patterns (repeatable)
- `--filter` / `-f` — Filter template list by name
