#!/usr/bin/env bash
# SearXNG 完整包 Pay Skill · check-update：查服务端最新版本；已付订单凭存档凭证幂等免费重取。
# 用法: bash scripts/sxp-check-update.sh
set -euo pipefail
BASE="${SXP_BASE:-https://linkkhub.top}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="${SXP_STATE_DIR:-$HERE}/.sxp-state"
PACK_DIR="${SXP_PACK_DIR:-$HERE/searxng-full-pack}"

REMOTE=$(curl -s -m 15 "$BASE/api/pack/manifest" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("version",""))' 2>/dev/null || true)
[[ -n "$REMOTE" ]] || { echo "拿不到服务端版本（服务不可达？稍后再试）"; exit 1; }
LOCAL=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("version",""))' "$PACK_DIR/version.json" 2>/dev/null || echo "")

echo "服务端最新: v$REMOTE；本机: ${LOCAL:-未安装}"
if [[ -n "$LOCAL" && "$LOCAL" == "$REMOTE" ]]; then echo "✅ 已是最新版"; exit 0; fi

if [[ -f "$STATE/proof" && -f "$STATE/out-trade-no" ]]; then
  echo "发现存档付款凭证 → 免费重取最新版（幂等，不二次扣费）"
  SXP_MANUAL=1 SXP_PROOF=$(cat "$STATE/proof") bash "$HERE/scripts/sxp-complete.sh"
else
  echo "本机尚无付款记录 → 请先走三步：sxp-probe.sh → sxp-pay.sh（用户本人付款）→ sxp-complete.sh"
  exit 3
fi

# 2026-11-01 069R4：SXP_BASE 旧裸 IP → https://linkkhub.top（ICP 出号后切域名；旧值仅保留于 PROJECT.md L17 历史记录）
