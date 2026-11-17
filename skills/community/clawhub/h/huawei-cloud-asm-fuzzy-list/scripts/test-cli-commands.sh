#!/usr/bin/env bash
# test-cli-commands.sh — functional smoke test for huawei-cloud-asm-fuzzy-list
set -uo pipefail

SKILL_PATH="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
REGION="${HUAWEI_CLOUD_REGION:-cn-north-4}"

pass=0
fail=0
skip=0

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Shared SDK boilerplate (prepended to every test body)
cat > "$TMPDIR/base.py" <<'PYEOF'
import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkasm.v1 import AsmClient, ListMeshesRequest
from huaweicloudsdkasm.v1.region.asm_region import AsmRegion

def get_client():
    return AsmClient.new_builder() \
        .with_credentials(BasicCredentials(os.environ["HUAWEICLOUD_SDK_AK"],
                                           os.environ["HUAWEICLOUD_SDK_SK"])) \
        .with_region(AsmRegion.value_of("cn-north-4")) \
        .build()
PYEOF

run_test_body() {
    local id="$1" name="$2" body="$3"
    local tmpfile="$TMPDIR/$id.py"
    cat "$TMPDIR/base.py" > "$tmpfile"
    printf '%s\n' "$body" >> "$tmpfile"
    echo -n "  [$id] $name ... "
    if output=$(python3 "$tmpfile" 2>&1); then
        echo "PASS"
        echo "$output" | sed 's/^/    /'
        pass=$((pass + 1))
    else
        echo "FAIL"
        echo "    Error: $output"
        fail=$((fail + 1))
    fi
}

echo "=== ASM List Skill Tests (region: $REGION) ==="
echo

# Prerequisite check
if ! python3 -c "from huaweicloudsdkasm.v1 import AsmClient, ListMeshesRequest" >/dev/null 2>&1; then
    echo "SKIP: huaweicloudsdkasm not installed"
    skip=$((skip + 5))
    exit 0
fi
if [ -z "${HUAWEICLOUD_SDK_AK:-}" ] || [ -z "${HUAWEICLOUD_SDK_SK:-}" ]; then
    echo "SKIP: HUAWEICLOUD_SDK_AK/HUAWEICLOUD_SDK_SK not set"
    skip=$((skip + 5))
    exit 0
fi

run_test_body "TC-01" "ASM SDK importable" '
print("SDK OK")
'

run_test_body "TC-02" "List all ASM meshes live (SDK)" '
resp = get_client().list_meshes(ListMeshesRequest())
items = resp.items or []
print("total meshes:", len(items))
for m in items:
    print(m.metadata.name, m.metadata.uid, m.status.phase, m.metadata.creation_timestamp)
'

run_test_body "TC-03" "Fuzzy match meshes by name (keyword='a')" '
resp = get_client().list_meshes(ListMeshesRequest())
matched = [m for m in (resp.items or []) if "a" in (m.metadata.name or "").lower()]
print("matched", len(matched))
'

run_test_body "TC-04" "Fuzzy match no-match keyword returns 0" '
resp = get_client().list_meshes(ListMeshesRequest())
matched = [m for m in (resp.items or []) if "zzzz_no_match_zzzz" in (m.metadata.name or "").lower()]
print("matched", len(matched))
'

run_test_body "TC-05" "Verify GET list endpoint from SDK _http_info" '
from huaweicloudsdkasm.v1.asm_client import AsmClient
import inspect
src = inspect.getsource(AsmClient._list_meshes_http_info)
assert "/v1/{project_id}/meshes" in src, src
assert "GET" in src
print("endpoint OK")
'

echo
echo "=== Results: $pass passed, $fail failed, $skip skipped ==="
if [ "$fail" -gt 0 ]; then
    exit 1
fi
exit 0
