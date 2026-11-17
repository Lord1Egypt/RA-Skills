#!/usr/bin/env bash
# SearXNG 完整包 Pay Skill · complete：付款后取货（校验 sha256 → 解压 → 存档凭证供日后免费重取最新）
# 用法: bash scripts/sxp-complete.sh
# 官方口径：主路径 alipay-bot 402-query-payment-status 携凭证续请求并自动买家回执；
#   若 CLI 复放对 JSON body 支持不足，用兜底：SXP_MANUAL=1 SXP_PROOF=<官方CLI给出的凭证> bash scripts/sxp-complete.sh
#   （服务端幂等：同一订单重复取货绝不二次扣费。）
set -euo pipefail
BASE="${SXP_BASE:-https://linkkhub.top}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="${SXP_STATE_DIR:-$HERE}/.sxp-state"
PACK_DIR="${SXP_PACK_DIR:-$HERE/searxng-full-pack}"
OTN=$(cat "$STATE/out-trade-no" 2>/dev/null || true)

if [[ "${SXP_MOCK:-0}" == "1" ]]; then
  [[ -n "$OTN" ]] || { echo "缺订单号（先 sxp-probe.sh）"; exit 1; }
  PROOF="${SXP_MOCK_PROOF:-$(python3 - "$OTN" <<'PY'
import sys,base64,json,time,secrets
proof={"protocol":{"payment_proof":"MOCKPROOF"+secrets.token_hex(8),
 "trade_no":f"MOCKTRADE{int(time.time()*1000)}","out_trade_no":sys.argv[1]},
 "method":{"client_session":"mock-session"}}
print(base64.urlsafe_b64encode(json.dumps(proof,ensure_ascii=False).encode()).decode().rstrip("="))
PY
)}"
elif [[ "${SXP_MANUAL:-0}" == "1" ]]; then
  PROOF="${SXP_PROOF:?SXP_MANUAL 模式需显式提供 SXP_PROOF（官方 CLI 输出的凭证）}"
else
  BOT="${ALIPAY_BOT_BIN:-$(command -v alipay-bot || true)}"
  [[ -n "$BOT" ]] || { echo "未找到 alipay-bot（见 sxp-pay.sh 安装指引；本机联调可用 SXP_MOCK=1）"; exit 127; }
  [[ -n "$OTN" ]] || { echo "缺订单号（先 sxp-probe.sh）"; exit 1; }
  EXTRA=()
  [[ -n "${SXP_BOT_BODY_ARGS:-}" ]] && read -r -a EXTRA <<< "$SXP_BOT_BODY_ARGS"
  echo "走官方 CLI 查单取货（输出原样转述）；完成后若未自动落盘内容，请补跑："
  echo "  SXP_MANUAL=1 SXP_PROOF=<凭证> bash scripts/sxp-complete.sh"
  exec "$BOT" 402-query-payment-status --out-shake-no "$OTN" \
    --resource-url "$BASE/api/pack/full" --method POST "${EXTRA[@]}"
fi

SEED=$(cat "$STATE/seed" 2>/dev/null || echo manual)
STATUS=$(curl -s -X POST "$BASE/api/pack/full" -H "Payment-Proof: $PROOF" \
  -H 'Content-Type: application/json' -d "{\"client_seed\":\"$SEED\"}" \
  -o "$STATE/result.json" -w '%{http_code}')

if [[ "$STATUS" != "200" ]]; then
  echo "HTTP $STATUS 取货失败（402=凭证与订单不匹配需重新支付；5xx=服务异常，持同一凭证重试不重复扣费）"; exit 2
fi

printf '%s' "$PROOF" > "$STATE/proof"; chmod 600 "$STATE/proof"
python3 - "$STATE/result.json" "$PACK_DIR" "$STATE" <<'PY'
import sys, json, base64, hashlib, io, zipfile, pathlib
res = json.loads(pathlib.Path(sys.argv[1]).read_text())
assert res.get("status") == "fulfilled", res.get("status")
raw = base64.urlsafe_b64decode(res["zip_b64"] + "=" * (-len(res["zip_b64"]) % 4))
digest = hashlib.sha256(raw).hexdigest()
if digest != res["sha256"]:
    sys.exit(f"sha256 校验失败！期望 {res['sha256']} 实得 {digest}——请重取或联系卖家")
outdir = pathlib.Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(io.BytesIO(raw)) as zf:
    names = zf.namelist()
    for n in names:  # 防路径穿越
        target = (outdir / n).resolve()
        if not str(target).startswith(str(outdir.resolve())):
            sys.exit(f"包内含非法路径条目: {n}")
    zf.extractall(outdir)
pathlib.Path(sys.argv[3], "last-sha256").write_text(digest)
print(f"✅ 完整包 v{res['version']} 已就绪: {outdir}（{res['file_count']} 个文件，sha256 {digest[:12]}…）")
print("   先读 README-FULL.md；以后对它说『检查搜索引擎更新』可凭存档凭证免费重取最新版")
for line in res.get("changelog", [])[:5]:
    print("   ·", line)
PY

# 2026-11-01 069R4：SXP_BASE 旧裸 IP → https://linkkhub.top（ICP 出号后切域名；旧值仅保留于 PROJECT.md L17 历史记录）
