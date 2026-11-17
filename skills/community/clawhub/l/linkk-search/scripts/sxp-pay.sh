#!/usr/bin/env bash
# SearXNG 完整包 Pay Skill · pay：把 402 账单交给支付宝官方买家 CLI（alipay-bot），
# 展示金额与支付入口，等待用户本人扫码/确认。脚本只编排，不碰密钥、绝不代用户确认。
# 用法: bash scripts/sxp-pay.sh
# 依据（2026-10-15 简历审计官联调校准）：买家 CLI 真身是 alipay-bot；@alipay/agent-payment 仅为
#   安装/守护 helper，本脚本绝不代跑未知来源安装器。
set -euo pipefail
BASE="${SXP_BASE:-https://linkkhub.top}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="${SXP_STATE_DIR:-$HERE}/.sxp-state"
[[ -f "$STATE/payment-needed" ]] || { echo "先运行 sxp-probe.sh 获取账单"; exit 1; }

if [[ "${SXP_MOCK:-0}" == "1" ]]; then
  echo "[MOCK 模式·仅本机联调] 订单 $(cat "$STATE/out-trade-no") —— 生成凭证后跑 sxp-complete.sh"
  exit 0
fi

BOT="${ALIPAY_BOT_BIN:-$(command -v alipay-bot || true)}"
if [[ -z "$BOT" ]]; then
  cat <<'EOF'
未找到官方买家 CLI alipay-bot。请按官方渠道安装其一后再重试：
  1) SkillHub/WorkBuddy 安装官方「alipay-payment-skill」（推荐）
  2) 或官方 helper：npx -y @alipay/agent-payment@latest
安装后二进制通常位于 ~/.local/share/alipay-bot-cli 并加入 PATH；也可用 ALIPAY_BOT_BIN 显式指定。
EOF
  exit 127
fi

SESSION_ID="${SXP_SESSION_ID:-sxp-pack-$(date +%s)}"
# 教程口径：资源请求为 POST 时需把原始请求体交给 CLI 复放；具体 flag 以联调实测为准，
# 未设 SXP_BOT_BODY_ARGS 则按教程最小参数执行。
EXTRA=()
[[ -n "${SXP_BOT_BODY_ARGS:-}" ]] && read -r -a EXTRA <<< "$SXP_BOT_BODY_ARGS"

exec "$BOT" 402-buyer-pay \
  --session-id "$SESSION_ID" \
  --file "$STATE/payment-needed" \
  --resource-url "$BASE/api/pack/full" \
  --method POST \
  --intent-summary "SearXNG中国特供完整包-0.99元" \
  "${EXTRA[@]}"

# 2026-11-01 069R4：SXP_BASE 旧裸 IP → https://linkkhub.top（ICP 出号后切域名；旧值仅保留于 PROJECT.md L17 历史记录）
