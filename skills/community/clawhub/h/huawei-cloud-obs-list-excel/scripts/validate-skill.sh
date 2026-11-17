#!/usr/bin/env bash
# validate-skill.sh — Huawei Cloud Skill Specification validation
set -euo pipefail

SKILL_PATH="${1:?Usage: validate-skill.sh <skill-path>}"

echo "=== Huawei Cloud Skill Validation ==="
echo "Skill path: $SKILL_PATH"
echo ""

CRITICAL=0
HIGH=0
MEDIUM=0
LOW=0
PASS=0

check() {
  local level="$1"
  local name="$2"
  local result="$3"
  if [ "$result" = "PASS" ]; then
    echo "  [PASS] [$level] $name"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] [$level] $name"
    case "$level" in
      Critical) CRITICAL=$((CRITICAL + 1)) ;;
      High) HIGH=$((HIGH + 1)) ;;
      Medium) MEDIUM=$((MEDIUM + 1)) ;;
      Low) LOW=$((LOW + 1)) ;;
    esac
  fi
}

SKILL_MD="$SKILL_PATH/SKILL.md"

# Critical checks
check "Critical" "SKILL.md exists" "$([ -f "$SKILL_MD" ] && echo PASS || echo FAIL)"
check "Critical" "YAML frontmatter exists" "$(head -1 "$SKILL_MD" 2>/dev/null | grep -q '^---$' && echo PASS || echo FAIL)"
check "Critical" "name field exists" "$(grep -q '^name:' "$SKILL_MD" && echo PASS || echo FAIL)"
check "Critical" "description field exists" "$(grep -q '^description:' "$SKILL_MD" && echo PASS || echo FAIL)"
check "Critical" "Reference Documents section" "$(grep -qi 'Reference Documents\|References\|参考文档' "$SKILL_MD" && echo PASS || echo FAIL)"
check "Critical" "references/iam-policies.md exists" "$([ -f "$SKILL_PATH/references/iam-policies.md" ] && echo PASS || echo FAIL)"
check "Critical" "No credential hardcoding" "$(grep -qiE '(AK=|SK=|access.key=|secret.key=|password=)' "$SKILL_MD" && echo FAIL || echo PASS)"

# High checks
check "High" "Overview section" "$(grep -qi 'Overview\|概述' "$SKILL_MD" && echo PASS || echo FAIL)"
check "High" "Prerequisites section" "$(grep -qi 'Prerequisites\|前置条件' "$SKILL_MD" && echo PASS || echo FAIL)"
check "High" "Workflow section" "$(grep -qi 'Workflow\|工作流' "$SKILL_MD" && echo PASS || echo FAIL)"
check "High" "Core Commands section" "$(grep -qi 'Core Commands\|核心命令' "$SKILL_MD" && echo PASS || echo FAIL)"
check "High" "Parameter Confirmation section" "$(grep -qi 'Parameter Confirmation\|参数确认' "$SKILL_MD" && echo PASS || echo FAIL)"
check "High" "CLI installation guide" "$([ -f "$SKILL_PATH/references/cli-installation-guide.md" ] && echo PASS || echo FAIL)"

# Medium checks
check "Medium" "description includes trigger words" "$(grep -qi 'trigger\|use when' "$SKILL_MD" && echo PASS || echo FAIL)"
check "Medium" "No version field" "$(grep -q '^version:' "$SKILL_MD" && echo FAIL || echo PASS)"
check "Medium" "verification-method.md exists" "$([ -f "$SKILL_PATH/references/verification-method.md" ] && echo PASS || echo FAIL)"
check "Medium" "Service name OBS uppercase" "$(grep -q 'hcloud OBS' "$SKILL_MD" && echo PASS || echo FAIL)"
check "Medium" "Includes obsutil ls command" "$(grep -q 'hcloud OBS ls' "$SKILL_MD" && echo PASS || echo FAIL)"

# Low checks
check "Low" "acceptance-criteria.md exists" "$([ -f "$SKILL_PATH/references/acceptance-criteria.md" ] && echo PASS || echo FAIL)"
check "Low" "KooCLI format section" "$(grep -qi 'KooCLI Command Format Standard' "$SKILL_MD" && echo PASS || echo FAIL)"

# Size checks
FILE_COUNT=$(find "$SKILL_PATH" -type f | wc -l)
SKILL_LINES=$(wc -l < "$SKILL_MD")
check "Medium" "File count <= 30" "$([ "$FILE_COUNT" -le 30 ] && echo PASS || echo FAIL)"
check "Medium" "SKILL.md lines <= 500" "$([ "$SKILL_LINES" -le 500 ] && echo PASS || echo FAIL)"

echo ""
echo "=== Validation Summary ==="
echo "PASS: $PASS"
echo "CRITICAL failures: $CRITICAL"
echo "HIGH failures: $HIGH"
echo "MEDIUM failures: $MEDIUM"
echo "LOW failures: $LOW"

if [ "$CRITICAL" -gt 0 ]; then
  echo ""
  echo "VALIDATION FAILED: Critical issues found"
  exit 1
fi

echo ""
echo "VALIDATION PASSED"