#!/usr/bin/env bash
# 土建算量接线：开工前从 lis-skill-bus 拉取上一次 cad-file-reader 的契约。
# 命中 → 直接复用，不再重新解图；未命中 → 返回 hit=false，skill 降级本机解析。
# 用法: bash qty_pull_contract.sh --project 项目 --building 楼栋 --floor 楼层 [--out out.json]
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CLIENT="$(dirname "$HERE")/skillbus_client.py"
PROJECT=""; BUILDING=""; FLOOR=""; OUT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2;;
    --building) BUILDING="$2"; shift 2;;
    --floor) FLOOR="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    *) echo "未知参数: $1" >&2; exit 2;;
  esac
done
[[ -n "$PROJECT" ]] || { echo "需要 --project" >&2; exit 2; }
ARGS=(--project "$PROJECT" --building "$BUILDING" --floor "$FLOOR")
[[ -n "$OUT" ]] && ARGS+=(--out "$OUT")
python3 "$CLIENT" pull "${ARGS[@]}"
