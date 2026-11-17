#!/usr/bin/env bash
# test-cli-commands.sh — functional smoke test for huawei-cloud-ecs-export-sorted
# NOTE: TC-02+ require live KooCLI credentials and network; they are the live
# acceptance path. The CI-safe offline suite lives in tests/ (unit tests).
set -uo pipefail

export PYTHONDONTWRITEBYTECODE=1

SKILL_PATH="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
REGION="${HUAWEI_CLOUD_REGION:-cn-north-4}"
OUT_DIR="${TEST_OUTPUT_DIR:-$(mktemp -d)}"

pass=0
fail=0

SCRIPT="$SKILL_PATH/scripts/list_ecs_export_sorted.py"

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

echo "=== ECS Instance-List Sorted Export Skill Tests (region: $REGION) ==="
echo

if ! command -v python3 &>/dev/null; then
    echo "SKIP: python3 not available"
    exit 0
fi

run_test "TC-01" "Help output (syntax)" "python3 $SCRIPT --help"
run_test "TC-02" "List instances (table)" "python3 $SCRIPT --region $REGION --format table"
run_test "TC-03" "Sorted JSON by created desc" "python3 $SCRIPT --region $REGION --format json --sort-by created --order desc"
run_test "TC-04" "Export sorted xlsx report" "python3 $SCRIPT --region $REGION --sort-by name --order asc --output $OUT_DIR/ecs_sorted_$REGION.xlsx --summary"
run_test "TC-05" "Export sorted csv report" "python3 $SCRIPT --region $REGION --sort-by vcpus --order desc --output $OUT_DIR/ecs_sorted_$REGION.csv --summary"

echo
echo "=== Results: $pass passed, $fail failed ==="
echo "Output dir: $OUT_DIR"
if [ "$fail" -gt 0 ]; then
    exit 1
fi
exit 0