#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "$0")/.." && pwd)"
version="$(node -e 'const fs=require("node:fs"); const pkg=JSON.parse(fs.readFileSync(process.argv[1],"utf8")); console.log(pkg.version);' "$skill_dir/clawhub.json")"

default_changelog="$(node - "$skill_dir/CHANGELOG.md" <<'EOF'
const fs = require("node:fs");
const changelogPath = process.argv[2];
const text = fs.readFileSync(changelogPath, "utf8");
const match = text.match(/^##\s+[^\n]+\n\n- ([^\n]+)/m);
if (!match) {
  process.exit(1);
}
process.stdout.write(match[1]);
EOF
)"

changelog="${SKILL_PUBLISH_CHANGELOG:-$default_changelog}"

clawhub publish "$skill_dir" \
  --slug llm-knowledge-bases \
  --name "LLM Knowledge Bases" \
  --version "$version" \
  --changelog "$changelog" \
  --tags "knowledge-base,research,markdown,wiki,obsidian,multimodal,pdf,image,data,local-first"
