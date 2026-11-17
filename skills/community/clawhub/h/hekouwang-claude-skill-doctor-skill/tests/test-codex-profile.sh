#!/usr/bin/env bash
# Codex Profile 回归：迁入 skill-creator 的严格白名单和 TODO 契约，但默认 Agent Profile 不受影响。
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CHECK="$ROOT/check.py"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/good" "$TMP/bad" "$TMP/agent-extension"
printf '%s\n' \
  '---' \
  'name: codex-valid-skill' \
  'description: Validate a Codex skill package when its basic frontmatter contract is required.' \
  'metadata:' \
  '  short-description: Validate Codex skill' \
  'allowed-tools:' \
  '  - Read' \
  '---' \
  '# Valid' > "$TMP/good/SKILL.md"
if ! python3 "$CHECK" "$TMP/good" --profile codex --json > "$TMP/good.json"; then
  echo '❌ 合法 Codex Profile Skill 被阻断'
  exit 1
fi
python3 - "$TMP/good.json" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
assert data["profile"] == "codex", data
assert data["gate"] == "PASS", data
assert any(item["key"] == "codex" and item["status"] == "PASS"
           for item in data["results"]), data["results"]
PY
echo '✅ Codex Profile 合法 Skill 通过'

printf '%s\n' \
  '---' \
  'name: bad--codex-skill' \
  'description: [TODO: describe this skill]' \
  'slug: unsupported' \
  '---' \
  '[TODO: fill instructions]' \
  '```text' \
  '[TODO: example inside code is allowed]' \
  '```' > "$TMP/bad/SKILL.md"
if python3 "$CHECK" "$TMP/bad" --profile codex --json > "$TMP/bad.json"; then
  echo '❌ Codex Profile 未阻断非白名单字段、双连字符或 TODO'
  exit 1
fi
python3 - "$TMP/bad.json" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
result = next(item for item in data["results"] if item["key"] == "codex")
assert result["status"] == "FAIL", result
assert "slug" in result["detail"], result
assert "TODO" in result["detail"], result
PY
echo '✅ Codex Profile 严格阻断扩展字段与未完成 TODO'

printf '%s\n' \
  '---' \
  'name: cross-host-skill' \
  'description: 跨宿主扩展字段兼容性测试。当需要验证默认 Agent Profile 时使用。' \
  'slug: cross-host-skill' \
  'version: 1.0.0' \
  '---' \
  '# Agent extension' > "$TMP/agent-extension/SKILL.md"
if ! python3 "$CHECK" "$TMP/agent-extension" --json > "$TMP/agent.json"; then
  echo '❌ 默认 Agent Profile 错误阻断跨宿主扩展字段'
  exit 1
fi
if python3 "$CHECK" "$TMP/agent-extension" --profile codex --json > "$TMP/agent-codex.json"; then
  echo '❌ Codex Profile 未阻断跨宿主扩展字段'
  exit 1
fi
echo '✅ 默认 Agent 与严格 Codex Profile 正确分流'
