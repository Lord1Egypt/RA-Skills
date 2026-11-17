#!/usr/bin/env bash
# run-all-doctors.sh 回归：doctor 崩溃、JSON 损坏和 env-doctor 非零都必须失败。
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)
SUITE="$ROOT/scripts/run-all-doctors.sh"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

mkdir -p \
  "$TMP/project/.agents/skills/example" \
  "$TMP/doctors/hekouwang-claude-md-doctor-skill" \
  "$TMP/doctors/hekouwang-claude-skill-doctor-skill" \
  "$TMP/doctors/hekouwang-env-doctor-skill/scripts"
printf '%s\n' '# fake skill' > "$TMP/project/.agents/skills/example/SKILL.md"
printf '%s\n' \
  'import json' \
  'import sys' \
  'print(json.dumps({"score": 100}) if "--json" in sys.argv else "")' \
  'sys.exit(0)' > "$TMP/doctors/hekouwang-claude-md-doctor-skill/check.py"
printf '%s\n' \
  'import json' \
  'import sys' \
  'print(json.dumps({"score": 100}) if "--json" in sys.argv else "")' \
  'sys.exit(0)' > "$TMP/doctors/hekouwang-claude-skill-doctor-skill/check.py"
printf '%s\n' \
  '#!/usr/bin/env bash' \
  'if [ "${FAKE_ENV_FAIL:-0}" = "1" ]; then exit 7; fi' \
  'exit 0' > "$TMP/doctors/hekouwang-env-doctor-skill/scripts/scan.sh"

run_suite() {
  local output="$1"
  shift
  if HEKOUWANG_SKILLS_DIR="$TMP/doctors" "$@" bash "$SUITE" "$TMP/project" > "$output" 2>&1; then
    return 0
  else
    return $?
  fi
}

printf '%s\n' 'import sys' 'sys.exit(2)' > "$TMP/doctors/hekouwang-claude-skill-doctor-skill/check.py"
if run_suite "$TMP/crash.txt"; then
  echo '❌ skill-doctor 崩溃未让套件失败'
  exit 1
fi
grep -q 'skill-doctor 运行失败' "$TMP/crash.txt"
echo '✅ skill-doctor 崩溃被 fail-closed'

printf '%s\n' \
  'import sys' \
  'print("not-json" if "--json" in sys.argv else "")' \
  'sys.exit(0)' > "$TMP/doctors/hekouwang-claude-skill-doctor-skill/check.py"
if run_suite "$TMP/json.txt"; then
  echo '❌ 损坏 JSON 未让套件失败'
  exit 1
fi
grep -q 'JSON 无法解析' "$TMP/json.txt"
echo '✅ 损坏 JSON 被 fail-closed'

printf '%s\n' \
  'import json' \
  'import sys' \
  'print(json.dumps({"score": 100}) if "--json" in sys.argv else "")' \
  'sys.exit(0)' > "$TMP/doctors/hekouwang-claude-skill-doctor-skill/check.py"
if run_suite "$TMP/env.txt" env FAKE_ENV_FAIL=1; then
  echo '❌ env-doctor 非零未让套件失败'
  exit 1
fi
echo '✅ env-doctor 非零被 fail-closed'
