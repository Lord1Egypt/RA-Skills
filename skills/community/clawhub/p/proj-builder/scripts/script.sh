#!/usr/bin/env bash
# builder skill - Project scaffold generator
# Usage: bash script.sh <list|init|generate> [template] [project-name]
set -euo pipefail

COMMAND="${1:-}"
ARG1="${2:-}"
ARG2="${3:-}"

BOLD='\033[1m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

sep() { printf '──────────────────────────────────────\n'; }

usage() {
  cat <<EOF
${BOLD}builder skill${RESET} — Project scaffold generator

Commands:
  list                         List available templates
  init <template> <name>       Scaffold a new project
  generate <template> <file>   Print a specific template file

Templates: node  node-cli  python  python-flask  go  go-cli
EOF
  exit 0
}

# ── Template definitions (written via Python heredocs) ──────────────────────

scaffold_node() {
  local name="$1"
  python3 -u - "$name" <<'PYEOF'
import sys, os

name = sys.argv[1]
base = name

files = {
    "package.json": f'''{{\n  "name": "{name}",\n  "version": "1.0.0",\n  "description": "",\n  "main": "src/index.js",\n  "scripts": {{\n    "start": "node src/index.js",\n    "dev": "nodemon src/index.js",\n    "test": "jest"\n  }},\n  "dependencies": {{\n    "express": "^4.18.2"\n  }},\n  "devDependencies": {{\n    "nodemon": "^3.0.1",\n    "jest": "^29.7.0"\n  }}\n}}\n''',
    "src/index.js": f'''const express = require('express');\nconst router = require('./routes');\n\nconst app = express();\nconst PORT = process.env.PORT || 3000;\n\napp.use(express.json());\napp.use('/api', router);\n\napp.get('/health', (req, res) => res.json({{ status: 'ok' }}));\n\napp.listen(PORT, () => {{\n  console.log(`{name} running on port ${{PORT}}`);\n}});\n\nmodule.exports = app;\n''',
    "src/routes.js": '''const express = require('express');\nconst router = express.Router();\n\nrouter.get('/items', (req, res) => {\n  res.json({ items: [] });\n});\n\nrouter.post('/items', (req, res) => {\n  const item = req.body;\n  res.status(201).json({ created: item });\n});\n\nmodule.exports = router;\n''',
    "tests/index.test.js": '''const request = require('supertest');\nconst app = require('../src/index');\n\ntest('GET /health returns ok', async () => {\n  const res = await request(app).get('/health');\n  expect(res.statusCode).toBe(200);\n  expect(res.body.status).toBe('ok');\n});\n''',
    ".gitignore": "node_modules/\n.env\n*.log\ndist/\n",
    "README.md": f"# {name}\n\nA Node.js Express REST API.\n\n## Getting Started\n\n```bash\nnpm install\nnpm run dev\n```\n",
}

created = []
for path, content in files.items():
    full = os.path.join(base, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    created.append(full)
    print(f"  \033[0;32m✅\033[0m {full}")

print(f"\n\033[1m✨ Done! Next steps:\033[0m")
print(f"  cd {name}")
print(f"  npm install")
print(f"  npm run dev")
PYEOF
}

scaffold_node_cli() {
  local name="$1"
  python3 -u - "$name" <<'PYEOF'
import sys, os
name = sys.argv[1]
base = name
files = {
    "package.json": f'{{\n  "name": "{name}",\n  "version": "1.0.0",\n  "bin": {{\n    "{name}": "./src/cli.js"\n  }},\n  "scripts": {{\n    "start": "node src/cli.js",\n    "test": "jest"\n  }},\n  "dependencies": {{\n    "commander": "^11.1.0"\n  }},\n  "devDependencies": {{\n    "jest": "^29.7.0"\n  }}\n}}\n',
    "src/cli.js": f'''#!/usr/bin/env node\nconst {{ Command }} = require('commander');\nconst pkg = require('../package.json');\n\nconst program = new Command();\n\nprogram\n  .name('{name}')\n  .description('CLI tool')\n  .version(pkg.version);\n\nprogram\n  .command('run <input>')\n  .description('Run with input')\n  .option('-v, --verbose', 'verbose output')\n  .action((input, opts) => {{\n    if (opts.verbose) console.log('Input:', input);\n    console.log('Done:', input);\n  }});\n\nprogram.parse();\n''',
    ".gitignore": "node_modules/\n.env\n*.log\n",
    "README.md": f"# {name}\n\nA Node.js CLI tool.\n\n```bash\nnpm install\nnode src/cli.js --help\n```\n",
}
for path, content in files.items():
    full = os.path.join(base, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    print(f"  \033[0;32m✅\033[0m {full}")
print(f"\n\033[1m✨ Done!\033[0m  cd {name} && npm install && node src/cli.js --help")
PYEOF
}

scaffold_python() {
  local name="$1"
  local pkg
  pkg="${name//-/_}"
  python3 -u - "$name" "$pkg" <<'PYEOF'
import sys, os
name, pkg = sys.argv[1], sys.argv[2]
base = name
files = {
    f"src/{pkg}/__init__.py": f'"""{ name } package."""\n__version__ = "0.1.0"\n',
    f"src/{pkg}/main.py": f'"""Main module for {name}."""\n\ndef main():\n    print("Hello from {name}!")\n\nif __name__ == "__main__":\n    main()\n',
    "tests/__init__.py": "",
    f"tests/test_main.py": f'"""Tests for {name}."""\nfrom {pkg}.main import main\n\ndef test_main(capsys):\n    main()\n    captured = capsys.readouterr()\n    assert "Hello" in captured.out\n',
    "pyproject.toml": f'[build-system]\nrequires = ["setuptools>=68"]\nbuild-backend = "setuptools.backends.legacy:build"\n\n[project]\nname = "{name}"\nversion = "0.1.0"\nrequires-python = ">=3.8"\n\n[project.scripts]\n{name} = "{pkg}.main:main"\n',
    ".gitignore": "__pycache__/\n*.pyc\n.venv/\nvenv/\ndist/\n*.egg-info/\n.pytest_cache/\n",
    "README.md": f"# {name}\n\nA Python package.\n\n```bash\npython3 -m venv venv && source venv/bin/activate\npip install -e .\n{name}\n```\n",
}
for path, content in files.items():
    full = os.path.join(base, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    print(f"  \033[0;32m✅\033[0m {full}")
print(f"\n\033[1m✨ Done! Next steps:\033[0m")
print(f"  cd {name}")
print(f"  python3 -m venv venv && source venv/bin/activate")
print(f"  pip install -e .")
PYEOF
}

scaffold_python_flask() {
  local name="$1"
  python3 -u - "$name" <<'PYEOF'
import sys, os
name = sys.argv[1]
base = name
files = {
    "app/__init__.py": 'from flask import Flask\n\ndef create_app():\n    app = Flask(__name__)\n    from .routes import bp\n    app.register_blueprint(bp, url_prefix="/api")\n    return app\n',
    "app/routes.py": 'from flask import Blueprint, jsonify, request\n\nbp = Blueprint("main", __name__)\n\n@bp.get("/health")\ndef health():\n    return jsonify({"status": "ok"})\n\n@bp.get("/items")\ndef list_items():\n    return jsonify({"items": []})\n\n@bp.post("/items")\ndef create_item():\n    data = request.get_json()\n    return jsonify({"created": data}), 201\n',
    "run.py": 'from app import create_app\n\napp = create_app()\n\nif __name__ == "__main__":\n    app.run(debug=True, port=5000)\n',
    "requirements.txt": "flask>=3.0\ngunicorn>=21.2\n",
    ".gitignore": "__pycache__/\n*.pyc\nvenv/\n.env\n",
    "README.md": f"# {name}\n\nFlask REST API.\n\n```bash\npython3 -m venv venv && source venv/bin/activate\npip install -r requirements.txt\npython run.py\n```\n",
}
for path, content in files.items():
    full = os.path.join(base, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    print(f"  \033[0;32m✅\033[0m {full}")
print(f"\n\033[1m✨ Done!\033[0m  cd {name} && pip install -r requirements.txt && python run.py")
PYEOF
}

scaffold_go() {
  local name="$1"
  python3 -u - "$name" <<'PYEOF'
import sys, os
name = sys.argv[1]
base = name
files = {
    "go.mod": f'module github.com/you/{name}\n\ngo 1.21\n',
    "cmd/main.go": f'package main\n\nimport (\n\t"fmt"\n\t"log"\n\t"net/http"\n\n\t"github.com/you/{name}/internal/server"\n)\n\nfunc main() {{\n\ts := server.New()\n\taddr := ":8080"\n\tfmt.Printf("{name} listening on %s\\n", addr)\n\tlog.Fatal(http.ListenAndServe(addr, s))\n}}\n',
    "internal/server/server.go": 'package server\n\nimport (\n\t"encoding/json"\n\t"net/http"\n)\n\nfunc New() http.Handler {\n\tmux := http.NewServeMux()\n\tmux.HandleFunc("/health", healthHandler)\n\tmux.HandleFunc("/api/items", itemsHandler)\n\treturn mux\n}\n\nfunc healthHandler(w http.ResponseWriter, r *http.Request) {\n\twriteJSON(w, 200, map[string]string{"status": "ok"})\n}\n\nfunc itemsHandler(w http.ResponseWriter, r *http.Request) {\n\twriteJSON(w, 200, map[string]any{"items": []string{}})\n}\n\nfunc writeJSON(w http.ResponseWriter, status int, v any) {\n\tw.Header().Set("Content-Type", "application/json")\n\tw.WriteHeader(status)\n\tjson.NewEncoder(w).Encode(v)\n}\n',
    ".gitignore": "# Go\nbuild/\n*.exe\n*.test\n",
    "README.md": f"# {name}\n\nGo HTTP server.\n\n```bash\ngo run ./cmd/main.go\n```\n",
}
for path, content in files.items():
    full = os.path.join(base, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    print(f"  \033[0;32m✅\033[0m {full}")
print(f"\n\033[1m✨ Done!\033[0m  cd {name} && go run ./cmd/main.go")
PYEOF
}

scaffold_go_cli() {
  local name="$1"
  python3 -u - "$name" <<'PYEOF'
import sys, os
name = sys.argv[1]
base = name
files = {
    "go.mod": f'module github.com/you/{name}\n\ngo 1.21\n\nrequire github.com/spf13/cobra v1.8.0\n',
    "main.go": f'package main\n\nimport "{{\n\t"github.com/you/{name}/cmd"\n}}\n\nfunc main() {{\n\tcmd.Execute()\n}}\n'.replace("{{", "{").replace("}}", "}"),
    "cmd/root.go": f'package cmd\n\nimport (\n\t"fmt"\n\t"os"\n\n\t"github.com/spf13/cobra"\n)\n\nvar rootCmd = &cobra.Command{{\n\tUse:   "{name}",\n\tShort: "A CLI tool",\n\tLong:  `{name} - a CLI tool built with cobra.`,\n}}\n\nfunc Execute() {{\n\tif err := rootCmd.Execute(); err != nil {{\n\t\tfmt.Fprintln(os.Stderr, err)\n\t\tos.Exit(1)\n\t}}\n}}\n\nfunc init() {{\n\trootCmd.AddCommand(runCmd)\n}}\n\nvar runCmd = &cobra.Command{{\n\tUse:   "run [input]",\n\tShort: "Run with input",\n\tArgs:  cobra.ExactArgs(1),\n\tRun: func(cmd *cobra.Command, args []string) {{\n\t\tfmt.Println("Done:", args[0])\n\t}},\n}}\n',
    ".gitignore": "build/\n*.exe\n",
    "README.md": f"# {name}\n\nGo CLI tool.\n\n```bash\ngo run main.go --help\n```\n",
}
for path, content in files.items():
    full = os.path.join(base, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    print(f"  \033[0;32m✅\033[0m {full}")
print(f"\n\033[1m✨ Done!\033[0m  cd {name} && go mod tidy && go run main.go --help")
PYEOF
}

do_list() {
  printf "\n${BOLD}📦 Available Project Templates${RESET}\n"
  sep
  printf "  %-14s %s\n" "node"         "Node.js Express REST API"
  printf "  %-14s %s\n" "node-cli"     "Node.js CLI tool (commander)"
  printf "  %-14s %s\n" "python"       "Python package (src layout)"
  printf "  %-14s %s\n" "python-flask" "Python Flask REST API"
  printf "  %-14s %s\n" "go"           "Go module (cmd/internal layout)"
  printf "  %-14s %s\n" "go-cli"       "Go CLI tool (cobra)"
  printf "\nUsage: bash script.sh init <template> <project-name>\n\n"
}

do_init() {
  local template="$1"
  local name="$2"
  printf "\n${BOLD}🏗  Scaffolding: ${CYAN}%s${RESET}${BOLD} → %s/${RESET}\n" "$template" "$name"
  sep

  case "$template" in
    node)         scaffold_node "$name" ;;
    node-cli)     scaffold_node_cli "$name" ;;
    python)       scaffold_python "$name" ;;
    python-flask) scaffold_python_flask "$name" ;;
    go)           scaffold_go "$name" ;;
    go-cli)       scaffold_go_cli "$name" ;;
    *)
      echo -e "${RED}Unknown template: $template${RESET}"
      echo "Run: bash script.sh list"
      exit 1
      ;;
  esac
}

do_generate() {
  local template="$1"
  local filename="$2"
  # Print a representative file for the template
  case "$template" in
    node)
      case "$filename" in
        "src/index.js"|"index.js") cat <<'EOF'
const express = require('express');
const router = require('./routes');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use('/api', router);

app.get('/health', (req, res) => res.json({ status: 'ok' }));

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;
EOF
        ;;
        *) echo "Available files for 'node': src/index.js, src/routes.js, package.json" ;;
      esac
      ;;
    python)
      cat <<'EOF'
"""Main module."""


def main():
    print("Hello!")


if __name__ == "__main__":
    main()
EOF
      ;;
    go)
      cat <<'EOF'
package main

import (
    "fmt"
    "log"
    "net/http"
)

func main() {
    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintln(w, `{"status":"ok"}`)
    })
    log.Println("Listening on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
EOF
      ;;
    *)
      echo "Run: bash script.sh init $template my-project  to scaffold the full template"
      ;;
  esac
}

case "$COMMAND" in
  list)     do_list ;;
  init)
    [[ -z "$ARG1" ]] && { echo "Usage: bash script.sh init <template> <name>"; exit 1; }
    [[ -z "$ARG2" ]] && { echo "Usage: bash script.sh init <template> <name>"; exit 1; }
    do_init "$ARG1" "$ARG2"
    ;;
  generate)
    [[ -z "$ARG1" ]] && { echo "Usage: bash script.sh generate <template> <filename>"; exit 1; }
    do_generate "$ARG1" "${ARG2:-}"
    ;;
  help|--help|-h|"")
    usage
    ;;
  *)
    echo -e "${RED}Unknown command: $COMMAND${RESET}"
    exit 1
    ;;
esac
