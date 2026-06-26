#!/bin/bash
# sync-review.sh — 上传雅思阅读复盘 JSON 到 liuxue.online
#
# 双通道：
#   Token 模式（推荐，进个人首页进度图）：
#     - 触发：环境变量 IELTS_USER_TOKEN 已设置
#     - 通道：POST /api/ielts {action:'batchImport', token, reviews:[...]}
#     - 写入：主库 ielts_reviews（受 username 隔离），首页/进度图/词汇本全部自动同步
#     - 适合：登录用户（dengjiawei / lishuzhuo / 其他注册用户）
#
#   匿名模式（老路径，仅自留 dashboard）：
#     - 触发：未设置 IELTS_USER_TOKEN，自动 fallback
#     - 通道：POST /ielts-api/skill-review (x-api-key 鉴权)
#     - 写入：匿名 dashboard 表（不进个人主页进度图）
#     - 适合：访客试用、本地脚本测试
#
# Usage:
#   bash sync-review.sh <json-file>
#   IELTS_USER_TOKEN=xxx bash sync-review.sh <json-file>
#
# JSON 文件支持两种格式：
#   - 扁平：{book, test, passage, score, total, date, ...}
#   - v4.0 富格式：{version:'4.0.0', source:{book,test,passage}, score:{correct,total}, timing:{minutes}, ...}
#   服务端 schemaUpgrader 会自动识别富格式。
#
# Environment variables:
#   IELTS_USER_TOKEN  — 登录 token（推荐）。从浏览器 localStorage.token 取，或
#                       用 ielts-reading-review/scripts/get-token.sh 生成
#   IELTS_API_BASE    — 主 API（默认 https://www.liuxue.online/api/ielts）
#   IELTS_LEGACY_BASE — 匿名 API（默认 https://www.liuxue.online/ielts-api）
#   IELTS_API_KEY     — 匿名模式 API key（默认内置）
#   IELTS_USER_ID     — 匿名模式覆盖 user id

set -e

# ─── Config ───
API_BASE="${IELTS_API_BASE:-https://www.liuxue.online/api/ielts}"
LEGACY_BASE="${IELTS_LEGACY_BASE:-https://www.liuxue.online/ielts-api}"
LEGACY_API_KEY="${IELTS_API_KEY:-ielts_8b0832b3cfd38884e44ab26ee68acaeed294623ef8da9b201871a7768b072606}"

# ─── Parse args ───
JSON_FILE=""
FORCE_MODE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --token-mode)  FORCE_MODE="token"; shift ;;
    --anon-mode)   FORCE_MODE="anon"; shift ;;
    --html|--bilingual) shift 2 ;;  # 兼容老参数，已无用
    -*)            echo "Unknown option: $1"; exit 1 ;;
    *)             JSON_FILE="$1"; shift ;;
  esac
done

if [[ -z "$JSON_FILE" ]]; then
  echo "Usage: bash sync-review.sh <data.json> [--token-mode|--anon-mode]"
  echo ""
  echo "推荐先配置 token：export IELTS_USER_TOKEN='你的token'"
  exit 1
fi

if [[ ! -f "$JSON_FILE" ]]; then
  echo "❌ 文件不存在: $JSON_FILE"
  exit 1
fi

# ─── 决定走哪条通道 ───
MODE="$FORCE_MODE"
if [[ -z "$MODE" ]]; then
  if [[ -n "$IELTS_USER_TOKEN" ]]; then
    MODE="token"
  else
    # 没 token，先尝试唤起浏览器授权（如果 setup 脚本可达）
    SETUP_SCRIPT=""
    for cand in \
      "$HOME/.workbuddy/skills/ielts-reading-review/scripts/setup-client-mode.sh" \
      "$(dirname "$0")/../../ielts-reading-review/scripts/setup-client-mode.sh"; do
      if [[ -f "$cand" ]]; then SETUP_SCRIPT="$cand"; break; fi
    done

    if [[ -n "$SETUP_SCRIPT" && -t 0 ]]; then
      echo "ℹ️  未检测到 IELTS_USER_TOKEN。"
      read -p "现在打开浏览器授权？[Y/n] " ans
      if [[ "$ans" != "n" && "$ans" != "N" ]]; then
        bash "$SETUP_SCRIPT" || true
        # setup 写到 ~/.zshrc，当前 shell 还没重载，从 rc 里抓出来
        if [[ -z "$IELTS_USER_TOKEN" ]]; then
          for rc in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.profile"; do
            if [[ -f "$rc" ]]; then
              T=$(grep '^export IELTS_USER_TOKEN=' "$rc" | tail -1 | sed "s/^export IELTS_USER_TOKEN='//;s/'$//")
              if [[ -n "$T" ]]; then export IELTS_USER_TOKEN="$T"; break; fi
            fi
          done
        fi
      fi
    fi

    if [[ -n "$IELTS_USER_TOKEN" ]]; then
      MODE="token"
    else
      MODE="anon"
    fi
  fi
fi

echo "═══════════════════════════════════════════════════════════"
echo "  IELTS Review Upload"
echo "  JSON: $JSON_FILE"
echo "  Mode: $MODE"
echo "═══════════════════════════════════════════════════════════"

if [[ "$MODE" == "token" ]]; then
  if [[ -z "$IELTS_USER_TOKEN" ]]; then
    echo "❌ --token-mode 需要 IELTS_USER_TOKEN 环境变量"
    exit 1
  fi

  # 包装成 batchImport payload
  PAYLOAD=$(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    review = json.load(f)
payload = {
    'action': 'batchImport',
    'token': sys.argv[2],
    'reviews': [review]
}
print(json.dumps(payload, ensure_ascii=False))
" "$JSON_FILE" "$IELTS_USER_TOKEN")

  echo "→ POST $API_BASE  (action=batchImport)"
  RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X POST "$API_BASE" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
    CODE=$(echo "$BODY" | python3 -c "import json,sys;print(json.load(sys.stdin).get('code','?'))" 2>/dev/null || echo "?")
    if [[ "$CODE" == "0" ]]; then
      echo "✅ 上传成功"
      echo "   响应: $BODY"
      echo ""
      echo "📊 你的复盘已进入个人主页："
      echo "   https://www.liuxue.online/ielts/reading.html"
      echo "   （登录后查看进度图、词汇本、错题本）"
    else
      echo "❌ 业务错误 ($CODE): $BODY"
      echo ""
      echo "💡 常见原因：token 过期 / 字段缺失"
      echo "   重新登录获取 token，或用 --anon-mode fallback"
      exit 1
    fi
  else
    echo "❌ HTTP $HTTP_CODE: $BODY"
    exit 1
  fi
  exit 0
fi

# ─── 匿名模式（老路径） ───
echo "⚠️  使用匿名模式（数据不进个人主页进度图，仅写匿名 dashboard 表）"
echo "   建议设置 IELTS_USER_TOKEN 切换 token 模式"
echo ""

# 生成稳定匿名 user id
if [[ -n "$IELTS_USER_ID" ]]; then
  USER_ID="$IELTS_USER_ID"
else
  RAW_ID="$(hostname)-$(whoami)"
  if command -v shasum &>/dev/null; then
    USER_ID=$(echo -n "$RAW_ID" | shasum -a 256 | cut -c1-16)
  elif command -v sha256sum &>/dev/null; then
    USER_ID=$(echo -n "$RAW_ID" | sha256sum | cut -c1-16)
  else
    USER_ID=$(echo -n "$RAW_ID" | md5sum 2>/dev/null | cut -c1-16 || echo "$RAW_ID")
  fi
fi
USER_NAME="${IELTS_USER_NAME:-$(whoami)}"

echo "  User: $USER_NAME ($USER_ID)"
PAYLOAD=$(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
data['source'] = 'skill'
print(json.dumps(data, ensure_ascii=False))
" "$JSON_FILE")

echo "→ POST $LEGACY_BASE/skill-review"
RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "$LEGACY_BASE/skill-review" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $LEGACY_API_KEY" \
  -H "x-user-id: $USER_ID" \
  -H "x-user-name: $USER_NAME" \
  -d "$PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  echo "✅ 上传成功 ($HTTP_CODE): $BODY"
  echo ""
  echo "════════════════════════════════════════════"
  echo "  📊 你的匿名复盘看板："
  echo "  $LEGACY_BASE/web/?user=$USER_ID&key=$LEGACY_API_KEY"
  echo "  🔑 User ID: $USER_ID"
  echo "════════════════════════════════════════════"
else
  echo "❌ 上传失败 ($HTTP_CODE): $BODY"
  exit 1
fi
