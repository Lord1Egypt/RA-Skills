#!/usr/bin/env bash
# frontmatter 回归：BOM、嵌套 metadata、宿主 openai.yaml、保护文件和 malformed YAML。
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)
CHECK="$ROOT/check.py"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/nested/agents"
printf '\357\273\277---\nname: nested-skill\ndescription: >\n  检查嵌套元数据。当需要验证 Skill 宿主策略时使用。\nmetadata:\n  openclaw: true\nallowed-tools:\n  - Read\n---\n\n# Nested\n' > "$TMP/nested/SKILL.md"
printf '%s\n' \
  'interface:' \
  '  display_name: "Nested Skill"' \
  'policy:' \
  '  allow_implicit_invocation: true' > "$TMP/nested/agents/openai.yaml"

# 这些文件必须存在，但 Doctor 不能打开它们。
fake_prefix='sk-'
fake_suffix='ant-should-not-be-read-123456789012345'
printf 'api_key="%s%s"\n' "$fake_prefix" "$fake_suffix" > "$TMP/nested/.env"
printf 'api_key="%s%s"\n' "$fake_prefix" "$fake_suffix" > "$TMP/nested/private.secret.txt"

if ! python3 "$CHECK" "$TMP/nested" --json > "$TMP/nested.json"; then
  echo '❌ BOM + 嵌套 metadata 的合法 Skill 被阻断'
  exit 1
fi
python3 - "$TMP/nested.json" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
assert data["gate"] == "PASS", data
assert data["fm_errors"] == [], data
assert data["read_errors"] == [], data
assert any(
    item["key"] == "openclaw" and item["status"] == "PASS"
    for item in data["results"]
), data["results"]
assert any(
    item["key"] == "invocation" and item["status"] == "PASS"
    for item in data["results"]
), data["results"]
PY
echo '✅ BOM、嵌套 metadata、openai.yaml 和保护文件通过'

mkdir -p "$TMP/flow"
printf '%s\n' \
  '---' \
  'name: flow-metadata-skill' \
  'description: 验证跨行 flow metadata。当需要兼容现有宿主 Skill 时使用。' \
  'metadata:' \
  '  {' \
  '    "openclaw":' \
  '      {' \
  '        "emoji": "📊",' \
  '        "homepage": "https://echarts.apache.org/"' \
  '      }' \
  '  }' \
  '---' \
  '# flow metadata' > "$TMP/flow/SKILL.md"
if ! python3 "$CHECK" "$TMP/flow" --json > "$TMP/flow.json"; then
  echo '❌ 跨行 flow metadata 的合法 Skill 被阻断'
  exit 1
fi
python3 - "$TMP/flow.json" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
assert data["gate"] == "PASS", data
assert data["fm_errors"] == [], data
assert any(item["key"] == "openclaw" and item["status"] == "PASS"
           for item in data["results"]), data["results"]
PY
echo '✅ 跨行 flow metadata 被正确解析'

mkdir -p "$TMP/conflict/agents"
printf '%s\n' \
  '---' \
  'name: conflict-skill' \
  'description: 验证宿主调用策略冲突。当需要检查调用门禁时使用。' \
  'disable-model-invocation: true' \
  '---' \
  '# conflict' > "$TMP/conflict/SKILL.md"
printf '%s\n' 'policy:' '  allow_implicit_invocation: true' > "$TMP/conflict/agents/openai.yaml"
if python3 "$CHECK" "$TMP/conflict" --json > "$TMP/conflict.json"; then
  echo '❌ frontmatter 与 openai.yaml 冲突未被阻断'
  exit 1
fi
python3 - "$TMP/conflict.json" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
assert data["gate"] == "FAIL", data
assert any(item["key"] == "invocation" and item["status"] == "FAIL"
           for item in data["results"]), data["results"]
PY
echo '✅ 宿主调用策略冲突被阻断'

mkdir -p "$TMP/malformed"
printf '%s\n' '---' $'\tname: malformed-skill' 'description: [unclosed' '---' '# malformed' > "$TMP/malformed/SKILL.md"
if python3 "$CHECK" "$TMP/malformed" --json > "$TMP/malformed.json"; then
  echo '❌ malformed frontmatter 未被阻断'
  exit 1
fi
python3 - "$TMP/malformed.json" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
assert data["gate"] == "FAIL", data
assert data["fm_errors"], data
assert any(item["key"] == "frontmatter" and item["status"] == "FAIL"
           for item in data["results"]), data["results"]
PY
echo '✅ malformed frontmatter 被阻断且 JSON 可解析'
