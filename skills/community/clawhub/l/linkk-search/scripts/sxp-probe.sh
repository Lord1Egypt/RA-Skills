#!/usr/bin/env bash
# SearXNG 完整包 Pay Skill · probe：不带凭证请求付费端点，预期 HTTP 402 + Payment-Needed 账单。
# 用法: bash scripts/sxp-probe.sh
# 官方口径（probe→pay→complete）：保存账单(0600)与订单号，供 sxp-pay.sh / sxp-complete.sh 使用。
set -euo pipefail
BASE="${SXP_BASE:-https://linkkhub.top}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="${SXP_STATE_DIR:-$HERE}/.sxp-state"; mkdir -p "$STATE"

# client_seed：本机稳定指纹（一次生成长期复用），用于 Proof 未带单号时的服务端兜底定位
if [[ ! -f "$STATE/seed" ]]; then head -c 16 /dev/urandom | od -An -tx1 | tr -d ' \n' > "$STATE/seed"; chmod 600 "$STATE/seed"; fi
SEED=$(cat "$STATE/seed")

STATUS=$(curl -s -D "$STATE/headers" -o "$STATE/body" -w '%{http_code}' \
  -X POST "$BASE/api/pack/full" -H 'Content-Type: application/json' \
  -d "{\"client_seed\":\"$SEED\"}")

if [[ "$STATUS" != "402" ]]; then
  echo "预期 402，实际 HTTP $STATUS（200=本单已付过，直接 bash scripts/sxp-complete.sh 取货；其余状态检查服务）"
  exit 2
fi
PN=$(grep -i '^payment-needed:' "$STATE/headers" | sed 's/^[Pp]ayment-[Nn]eeded: *//' | tr -d '\r\n')
[[ -n "$PN" ]] || { echo "402 缺少 Payment-Needed 头"; exit 3; }
printf '%s' "$PN" > "$STATE/payment-needed"; chmod 600 "$STATE/payment-needed"

OTN=$(python3 - "$PN" <<'PY'
import sys, base64, json
raw = sys.argv[1]
d = json.loads(base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)))
print(d.get("protocol", d).get("out_trade_no", ""))
PY
)
[[ -n "$OTN" ]] || { echo "账单缺少 out_trade_no"; exit 4; }
printf '%s\n' "$OTN" > "$STATE/out-trade-no"
echo "HTTP 402 账单已保存: $STATE/payment-needed（订单 $OTN，¥0.99）"
echo "请核对账单金额后运行: bash scripts/sxp-pay.sh"

# 2026-11-01 069R4：SXP_BASE 旧裸 IP → https://linkkhub.top（ICP 出号后切域名；旧值仅保留于 PROJECT.md L17 历史记录）
