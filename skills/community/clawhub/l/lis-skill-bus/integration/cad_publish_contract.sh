#!/usr/bin/env bash
# cad-file-reader 接线：把一次解析产生的 cad-contract/v1 发布到 lis-skill-bus。
# 用法: bash cad_publish_contract.sh --project 项目 --building 楼栋 --floor 楼层 \
#          --entry-file <cad-contract.json> [--skill cad-file-reader]
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CLIENT="$(dirname "$HERE")/skillbus_client.py"
PROJECT=""; BUILDING=""; FLOOR=""; ENTRY=""; SKILL="${SKILL:-cad-file-reader}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2;;
    --building) BUILDING="$2"; shift 2;;
    --floor) FLOOR="$2"; shift 2;;
    --entry-file) ENTRY="$2"; shift 2;;
    --skill) SKILL="$2"; shift 2;;
    *) echo "未知参数: $1" >&2; return 2 2>/dev/null || exit 2;;
  esac
done
[[ -n "$PROJECT" && -n "$ENTRY" && -f "$ENTRY" ]] || { echo "需要 --project 与存在的 --entry-file" >&2; exit 2; }
python3 "$CLIENT" push --project "$PROJECT" --building "$BUILDING" --floor "$FLOOR" \
  --skill "$SKILL" --entry-file "$ENTRY"
