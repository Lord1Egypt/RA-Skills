#!/usr/bin/env bash
# test-cli-commands.sh — functional smoke test for huawei-cloud-ecs-export-excel
# NOTE: TC-02+ require live KooCLI credentials and network; they are the live
# acceptance path. The CI-safe offline suite lives in tests/ (unit tests).
set -uo pipefail

export PYTHONDONTWRITEBYTECODE=1

SKILL_PATH="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
REGION="${HUAWEI_CLOUD_REGION:-cn-north-4}"
OUT_DIR="${TEST_OUTPUT_DIR:-$(mktemp -d)}"

pass=0
fail=0

SCRIPT="$SKILL_PATH/scripts/list_ecs_export_excel.py"

run_test() {
    local id="$1" name="$2" cmd="$3"
    echo -n "  [$id] $name ... "
    if output=$(bash -c "$cmd" 2>&1); then
        echo "PASS"
        pass=$((pass + 1))
    else
        echo "FAIL"
        echo "    Error: $output"
        fail=$((fail + 1))
    fi
}

echo "=== ECS Instance-List Excel Skill Tests (region: $REGION) ==="
echo

if ! command -v python3 &>/dev/null; then
    echo "SKIP: python3 not available"
    exit 0
fi

run_test "TC-01" "Help output (syntax)" "python3 $SCRIPT --help"
run_test "TC-02" "List instances via CLI (table)" "python3 $SCRIPT --region $REGION --format table"
run_test "TC-03" "List instances via SDK fallback (json)" "python3 $SCRIPT --region $REGION --format json"
run_test "TC-04" "Export xlsx report" "python3 $SCRIPT --region $REGION --output $OUT_DIR/ecs_instances_$REGION.xlsx --summary"

echo
echo "=== Results: $pass passed, $fail failed ==="
echo "Output dir: $OUT_DIR"
if [ "$fail" -gt 0 ]; then
    exit 1
fi
exit 0