#!/usr/bin/env bash
# oc-pay-sdk/auth.sh  —  OpenClaw Skill 支付门控 SDK v1.0
#
# 用法：
#   source "$HOME/.openclaw/workspace/.lib/oc-pay-sdk/auth.sh"
#   oc_require_license "skill-id" "$IDENTIFIER" [dry_run]
#
# 完成后 $OC_LICENSE_TOKEN 被设置为 JWT token
#
# 环境变量：
#   OC_PAY_SERVER  - 支付网关地址（必须设置，或在此修改默认值）
#   OC_PAY_SDK     - SDK 路径（自动传递）

OC_PAY_SERVER="${OC_PAY_SERVER:-https://skill.socialmore.net}"
OC_LICENSE_TOKEN=""

# ── 内部工具函数 ─────────────────────────────────────────────
_oc_urlencode() {
  python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1" 2>/dev/null || \
  printf '%s' "$1" | python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.stdin.read()))"
}

_oc_json_get() {
  # $1=json_string, $2=key
  python3 -c "import sys,json; d=json.loads(sys.argv[1]); print(d.get(sys.argv[2],''))" "$1" "$2" 2>/dev/null || echo ""
}

_oc_check_deps() {
  if ! command -v python3 &>/dev/null; then
    echo "❌ 需要 python3，请先安装"
    return 1
  fi
  if ! command -v curl &>/dev/null; then
    echo "❌ 需要 curl，请先安装"
    return 1
  fi
  return 0
}

_oc_is_interactive() {
  # 返回 0（真）表示有真实终端，返回 1 表示非交互（Agent/CI/管道）
  [ -t 0 ] && [ -t 1 ]
}

_oc_get_pay_hint() {
  # 向服务器请求推荐支付方式（服务器根据 Accept-Language + IP 自动判断）
  local hint
  hint=$(curl -sf --max-time 5 \
    -H "Accept-Language: ${LANG:-en}" \
    "$OC_PAY_SERVER/api/install/pay-hint" 2>/dev/null \
    || echo '{"method":"alipay"}')
  _oc_json_get "$hint" "method"
}

# ── 主函数 ──────────────────────────────────────────────────
oc_require_license() {
  local skill_id="${1:?skill_id required}"
  local identifier="${2:?identifier required}"
  local dry_run="${3:-false}"
  local bundle_id="${OC_BUNDLE_ID:-}"    # 可选：指定套餐 ID

  _oc_check_deps || return 1

  # dry-run 模式（CI/测试用）
  if [ "$dry_run" = "true" ] || [ "$dry_run" = "--dry-run" ]; then
    echo "  [dry-run] 跳过支付验证"
    OC_LICENSE_TOKEN="dry-run-token-$(date +%s)"
    return 0
  fi

  echo ""

  # ── 1. 检查已有 license ─────────────────────────────────
  local enc_id
  enc_id=$(_oc_urlencode "$identifier")
  local verify_resp
  verify_resp=$(curl -sf --max-time 10 \
    "$OC_PAY_SERVER/api/install/verify?identifier=$enc_id&skill_id=$skill_id" 2>/dev/null || true)

  if [ -n "$verify_resp" ] && echo "$verify_resp" | grep -q '"status":"valid"'; then
    OC_LICENSE_TOKEN=$(_oc_json_get "$verify_resp" "token")
    local source
    source=$(_oc_json_get "$verify_resp" "source")
    local src_label="直购"
    echo "$source" | grep -q "bundle" && src_label="套餐"
    echo "  ✅ 已有授权（$src_label，终身有效）"
    return 0
  fi

  # ── 2. 获取 Skill/套餐信息（用于显示名称和定价）──────────
  local item_info item_name item_prices=""
  if [ -n "$bundle_id" ]; then
    item_info=$(curl -sf --max-time 5 "$OC_PAY_SERVER/api/bundle/$bundle_id" 2>/dev/null || echo "{}")
    item_name=$(_oc_json_get "$item_info" "name")
    [ -z "$item_name" ] && item_name="$bundle_id"
  else
    item_info=$(curl -sf --max-time 5 "$OC_PAY_SERVER/api/skill/$skill_id" 2>/dev/null || echo "{}")
    item_name=$(_oc_json_get "$item_info" "name")
    [ -z "$item_name" ] && item_name="$skill_id"
  fi

  echo "  ╔══════════════════════════════════════════════════╗"
  printf "  ║  🔑 需要授权：%-34s║\n" "$item_name"
  echo "  ║  首次安装需付费，授权终身有效（重装/更新免费）  ║"
  echo "  ╚══════════════════════════════════════════════════╝"
  echo ""

  # ── 3. 自动检测支付方式 ──────────────────────────────────
  local pay_method currency
  local _hint
  _hint=$(_oc_get_pay_hint)

  if [ "$_hint" = "alipay" ]; then
    echo "  检测到您的地区，默认使用 支付宝（人民币）支付"
    pay_method="alipay"
    currency="CNY"
  else
    echo "  Detected your region, defaulting to Crypto (USDT) payment"
    pay_method="crypto"
    currency="USDT"
  fi

  if _oc_is_interactive; then
    read -r -t 30 -p "  按 Enter 确认，或输入 s 手动切换支付方式: " _switch_choice || true
    if [ "${_switch_choice:-}" = "s" ]; then
      echo "  请选择支付方式："
      echo "    1) 支付宝（人民币）"
      echo "    2) 数字钱包 USDT（CryptoMus）"
      read -r -t 30 -p "  请输入 1 或 2 [默认 1]: " _manual_choice || true
      if [ "${_manual_choice:-1}" = "2" ]; then
        pay_method="crypto"
        currency="USDT"
      else
        pay_method="alipay"
        currency="CNY"
      fi
    fi
  else
    echo "  (非交互环境，使用默认支付方式：$pay_method)"
  fi

  # ── 4. 创建订单 ─────────────────────────────────────────
  local os_info oc_ver request_body
  os_info=$(uname -srm 2>/dev/null | tr '"' "'" || echo "unknown")
  oc_ver=$(openclaw --version 2>/dev/null | grep -oE '[0-9.]+' | head -1 || echo "unknown")

  if [ -n "$bundle_id" ]; then
    request_body="{\"identifier\":\"$identifier\",\"skill_id\":\"$skill_id\",
      \"bundle_id\":\"$bundle_id\",\"os_info\":\"$os_info\",\"oc_ver\":\"$oc_ver\",
      \"pay_method\":\"$pay_method\",\"currency\":\"$currency\"}"
  else
    request_body="{\"identifier\":\"$identifier\",\"skill_id\":\"$skill_id\",
      \"os_info\":\"$os_info\",\"oc_ver\":\"$oc_ver\",
      \"pay_method\":\"$pay_method\",\"currency\":\"$currency\"}"
  fi

  local req_resp
  req_resp=$(curl -sf --max-time 15 -X POST "$OC_PAY_SERVER/api/install/request" \
    -H "Content-Type: application/json" -d "$request_body" 2>/dev/null || true)

  if [ -z "$req_resp" ]; then
    echo "  ❌ 无法连接授权服务器，请检查网络或联系 Owner"
    echo "  服务器地址：$OC_PAY_SERVER"
    return 1
  fi

  # 服务端发现已有 license
  if echo "$req_resp" | grep -q '"status":"existing_license"'; then
    OC_LICENSE_TOKEN=$(_oc_json_get "$req_resp" "token")
    echo "  ✅ 已有授权，无需重复付费"
    return 0
  fi

  local order_id amount cur_disp
  order_id=$(_oc_json_get "$req_resp" "order_id")
  amount=$(_oc_json_get "$req_resp" "amount")
  cur_disp=$(_oc_json_get "$req_resp" "currency")

  if [ -z "$order_id" ]; then
    echo "  ❌ 创建订单失败：$req_resp"
    return 1
  fi

  # ── 5. 展示支付信息 ─────────────────────────────────────
  echo ""
  echo "  ╔══════════════════════════════════════════════════════════════╗"
  echo "  ║   ⚠️  AI AGENT / 自动化脚本 必读                            ║"
  echo "  ║                                                              ║"
  echo "  ║   此步骤需要【人类操作】—— AI 无法自行完成支付。            ║"
  echo "  ║   请将下方付款信息（金额 + 二维码/地址）完整发给您的        ║"
  echo "  ║   Owner，由人类扫码或转账后，脚本将自动继续，请勿重试。    ║"
  echo "  ║                                                              ║"
  echo "  ║   HUMAN ACTION REQUIRED. You CANNOT pay this yourself.      ║"
  echo "  ║   Send the payment info below to your human operator and    ║"
  echo "  ║   wait — the script will auto-proceed after confirmation.   ║"
  echo "  ╚══════════════════════════════════════════════════════════════╝"
  echo ""
  if [ "$pay_method" = "alipay" ]; then
    local qr_content pay_url
    qr_content=$(_oc_json_get "$req_resp" "qr_content")
    pay_url=$(_oc_json_get "$req_resp" "pay_url")

    echo "  ┌─────────────────────────────────────────────┐"
    printf "  │  支付宝扫码付款  ¥%s 元                        \n" "$amount"
    echo "  └─────────────────────────────────────────────┘"

    if command -v qrencode &>/dev/null && [ -n "$qr_content" ]; then
      qrencode -t UTF8 -m 1 "$qr_content" 2>/dev/null | sed 's/^/  /'
      echo "  ↑ 支付宝扫码"
    else
      echo "  付款链接（浏览器打开）："
      echo "  $pay_url"
      if command -v open &>/dev/null && [ -n "$pay_url" ]; then
        if _oc_is_interactive; then
          read -r -t 15 -p "  是否自动打开浏览器？[Y/n] " ob || true
          [ "${ob:-Y}" != "n" ] && [ "${ob:-Y}" != "N" ] && open "$pay_url" 2>/dev/null &
        fi
      fi
    fi

  else
    local address network pay_url
    address=$(_oc_json_get "$req_resp" "address")
    network=$(_oc_json_get "$req_resp" "network")
    pay_url=$(_oc_json_get "$req_resp" "pay_url")

    echo "  ┌─────────────────────────────────────────────┐"
    printf "  │  USDT 转账  %s %s (%s 网络)              \n" "$amount" "$cur_disp" "$network"
    echo "  └─────────────────────────────────────────────┘"
    echo "  收款地址：$address"
    echo ""
    if command -v qrencode &>/dev/null && [ -n "$address" ]; then
      qrencode -t UTF8 -m 1 "$address" 2>/dev/null | sed 's/^/  /'
    fi
    if [ -n "$pay_url" ]; then
      echo "  支付页面：$pay_url"
      command -v open &>/dev/null && open "$pay_url" 2>/dev/null &
    fi
  fi

  # ── 6. 轮询等待（3s 间隔，最长 10min / 200次）────────────
  echo ""
  echo "  ⏳ 等待支付确认（最长 10 分钟）... Ctrl+C 可取消"
  echo "  💡 AI Agent：请确认已将付款信息转发给您的 Owner，等待其完成支付即可，请勿中断。"
  local i=0
  while [ $i -lt 200 ]; do
    local st_resp status
    st_resp=$(curl -sf --max-time 8 "$OC_PAY_SERVER/api/install/status/$order_id" 2>/dev/null || true)
    status=$(_oc_json_get "$st_resp" "status")

    case "$status" in
      paid)
        OC_LICENSE_TOKEN=$(_oc_json_get "$st_resp" "token")
        echo ""
        echo "  ✅ 支付成功！授权已激活（终身有效，重装免费）"
        return 0
        ;;
      expired)
        echo ""
        echo "  ❌ 订单已过期（10分钟），请重新运行安装脚本"
        return 1
        ;;
    esac

    printf "."
    sleep 3
    i=$((i + 1))
  done

  echo ""
  echo "  ❌ 等待超时，请确认支付后重新运行安装脚本"
  return 1
}

# ── 加密 Skill 执行（内存管道，不落盘）──────────────────────
oc_execute_skill() {
  # 用法：oc_execute_skill <skill_id> [额外参数...]
  # 必须在 oc_require_license 成功后调用（需要 $OC_LICENSE_TOKEN）
  local skill_id="${1:?skill_id required}"
  shift  # 剩余参数将传给解密后的脚本

  if [ -z "$OC_LICENSE_TOKEN" ]; then
    echo "  ❌ 未找到授权 token，请先调用 oc_require_license"
    return 1
  fi

  if ! command -v openssl &>/dev/null; then
    echo "  ❌ 需要 openssl 才能运行加密 skill，请先安装"
    return 1
  fi

  local enc_sid
  enc_sid=$(_oc_urlencode "$skill_id")

  local fetch_resp
  fetch_resp=$(curl -sf --max-time 15 \
    "$OC_PAY_SERVER/api/install/fetch-skill?skill_id=$enc_sid&token=$OC_LICENSE_TOKEN" \
    2>/dev/null || true)

  if [ -z "$fetch_resp" ]; then
    echo "  ❌ 无法获取 Skill 内容，请检查网络或联系 Owner"
    return 1
  fi

  local encrypted session_key
  encrypted=$(_oc_json_get "$fetch_resp" "encrypted")
  session_key=$(_oc_json_get "$fetch_resp" "session_key")

  if [ -z "$encrypted" ] || [ -z "$session_key" ]; then
    local err
    err=$(_oc_json_get "$fetch_resp" "detail")
    echo "  ❌ 获取 Skill 内容失败：${err:-unknown error}"
    return 1
  fi

  # 内存管道解密并执行，解密内容不写入磁盘
  # 使用与服务端相同的加密参数（aes-256-cbc + pbkdf2 + 10000轮）
  # fold -w 64: 服务端返回的 base64 为单行，openssl -a 需要每64字符换行
  printf '%s' "$encrypted" | fold -w 64 | \
    openssl enc -d -aes-256-cbc -pass "pass:$session_key" -pbkdf2 -iter 10000 -a | \
    bash -s -- "$@"
}


# ── D1：Prompt 类 Skill 服务端执行（AI 在服务端运行，结果返回本地）────
oc_prompt_skill() {
  # 用法：oc_prompt_skill <skill_id> [key=value ...]
  # 额外参数作为 context 键值对传入服务端，例如：oc_prompt_skill "code-reviewer" file=main.go
  # 必须在 oc_require_license 成功后调用（需要 $OC_LICENSE_TOKEN）
  local skill_id="${1:?skill_id required}"
  shift

  if [ -z "$OC_LICENSE_TOKEN" ]; then
    echo "  ❌ 未找到授权 token，请先调用 oc_require_license"
    return 1
  fi

  # 将剩余参数构建为 JSON context（key=value 格式）
  local context_json="{}"
  if [ $# -gt 0 ]; then
    context_json=$(python3 -c "
import sys, json
pairs = sys.argv[1:]
ctx = {}
for p in pairs:
    if '=' in p:
        k, v = p.split('=', 1)
        ctx[k] = v
    else:
        ctx['arg'] = p
print(json.dumps(ctx))
" "$@" 2>/dev/null || echo '{}')
  fi

  local enc_sid
  enc_sid=$(_oc_urlencode "$skill_id")

  local resp
  resp=$(curl -sf --max-time 60 -X POST \
    "$OC_PAY_SERVER/api/skill/execute" \
    -H "Content-Type: application/json" \
    -d "{\"skill_id\":\"$skill_id\",\"token\":\"$OC_LICENSE_TOKEN\",\"context\":$context_json}" \
    2>/dev/null || true)

  if [ -z "$resp" ]; then
    echo "  ❌ 无法连接服务器，请检查网络"
    return 1
  fi

  local result err
  result=$(_oc_json_get "$resp" "result")
  if [ -n "$result" ]; then
    echo "$result"
    return 0
  fi

  err=$(_oc_json_get "$resp" "detail")
  echo "  ❌ 执行失败：${err:-unknown error}"
  return 1
}


# ── 辅助：验证 token 后解码显示（调试用）────────────────────
oc_show_license() {
  local token="$1"
  python3 -c "
import sys, base64, json
t = sys.argv[1].split('.')
if len(t) >= 2:
    pad = 4 - len(t[1])%4
    payload = json.loads(base64.b64decode(t[1] + '='*pad))
    print('  sub:', payload.get('sub',''))
    print('  skill:', payload.get('sid',''))
    print('  exp:', payload.get('exp',''))
" "$token" 2>/dev/null || echo "  (无法解码 token)"
}
