# builder

**Project Scaffold Generator** — Instantly generate well-structured project skeletons for Node.js, Python, and Go. Get a ready-to-code directory layout with sensible defaults in seconds.

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list` | List all available project templates | `list` |
| `init` | Initialize a project scaffold in a directory | `init node my-api` |
| `generate` | Print the file contents for a specific template file | `generate python main.py` |

## Usage

```bash
bash script.sh list
bash script.sh init <template> <project-name>
bash script.sh generate <template> <filename>
```

## Supported Templates

| Template | Language | Description |
|----------|----------|-------------|
| `node` | JavaScript / Node.js | Express REST API with basic routing |
| `node-cli` | JavaScript / Node.js | CLI tool with commander.js |
| `python` | Python 3 | Python package with src layout |
| `python-flask` | Python 3 | Flask REST API |
| `go` | Go | Go module with cmd/internal layout |
| `go-cli` | Go | CLI tool with cobra |

## Requirements

- `bash` >= 4.0
- `python3` >= 3.7 (for `init` command file writing)
- No external packages required

## Examples

```
$ bash script.sh list

📦 Available Project Templates
──────────────────────────────────────
  node          Node.js Express REST API
  node-cli      Node.js CLI tool
  python        Python package (src layout)
  python-flask  Python Flask REST API
  go            Go module (cmd/internal)
  go-cli        Go CLI tool with cobra

Usage: bash script.sh init <template> <project-name>
```

```
$ bash script.sh init python my-project

🏗  Scaffolding: python → my-project/
──────────────────────────────────────
  ✅ my-project/src/my_project/__init__.py
  ✅ my-project/src/my_project/main.py
  ✅ my-project/tests/__init__.py
  ✅ my-project/tests/test_main.py
  ✅ my-project/pyproject.toml
  ✅ my-project/README.md
  ✅ my-project/.gitignore

✨ Done! Next steps:
  cd my-project
  python3 -m venv venv && source venv/bin/activate
  pip install -e .
```

```
$ bash script.sh generate go main.go

package main

import (
    "fmt"
    "log"
    "net/http"
)
...
```
