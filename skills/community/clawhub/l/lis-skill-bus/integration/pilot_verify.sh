#!/usr/bin/env bash
# 试点验收：cad-file-reader 发布契约 → 土建算量拉取，验证免重复解图的数据链路。
# 用法: SKILLBUS_STATE_DIR=<临时目录> bash integration/pilot_verify.sh
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLE="$(dirname "$HERE")/example_pilot/demo_state.json"
if [[ -n "${SKILLBUS_TEST_OUT:-}" ]]; then
  TMPOUT="$SKILLBUS_TEST_OUT/pilot"
else
  TMPOUT="$(mktemp -d)/pilot"
fi
mkdir -p "$TMPOUT"

echo "★ 端1: cad-file-reader 解析完成后发布契约"
bash "$HERE/cad_publish_contract.sh" --project 示例项目 --building B栋 --floor F2 \
  --entry-file "$EXAMPLE" --skill cad-file-reader

echo
echo "★ 端2: 土建算量开工前拉取（命中 → 不再重复解图）"
PULL="$(bash "$HERE/qty_pull_contract.sh" --project 示例项目 --building B栋 --floor F2 --out "$TMPOUT/candidates.json")"
echo "$PULL"
echo
echo "★ 落盘供 run_qty 消费: $TMPOUT/candidates.json"
python3 - <<PY
import json, pathlib
p = pathlib.Path("$TMPOUT/candidates.json")
d = json.loads(p.read_text(encoding="utf-8"))
assert d["schema"] == "cad-contract/v1", "契约 schema 不符"
assert d["contract"]["sections"]["wall_segments"][0]["id"] == "walls/012", "候选未命中"
print("✔ 契约 schema/候选均已命中，链路可用")
PY
