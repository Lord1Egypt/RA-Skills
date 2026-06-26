#!/bin/bash
# setup-client-mode.sh — 一键授权配置（v5.4 优雅授权流）
#
# 流程：
#   1. 启动本地随机端口的 HTTP 服务
#   2. 自动打开浏览器到 www.liuxue.online/ielts/authorize.html
#   3. 用户在网页点击"授权" → 浏览器把 token POST/GET 到本机
#   4. 本地服务收到 token → 校验 → 写入 ~/.zshrc
#
# 兼容：保留 --manual 模式（沿用 F12 复制 token 流程）

set -e

API_BASE="https://www.liuxue.online/api/ielts"
AUTH_PAGE="https://www.liuxue.online/ielts/authorize.html"

echo "═══════════════════════════════════════════════════════════"
echo "  IELTS Reading Review · 客户端授权"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 检查现有配置
if [[ -n "$IELTS_USER_TOKEN" ]]; then
  echo "ℹ️  当前 shell 已有 IELTS_USER_TOKEN（前20位：${IELTS_USER_TOKEN:0:20}...）"
  read -p "继续覆盖配置？[y/N] " ans
  if [[ "$ans" != "y" && "$ans" != "Y" ]]; then
    echo "已取消。"
    exit 0
  fi
  echo ""
fi

MODE="${1:-auto}"

# ───────────────────────────────── 手动模式（兜底） ─────────────────────────────
if [[ "$MODE" == "--manual" || "$MODE" == "manual" ]]; then
  echo "📝 手动模式：从浏览器复制 token"
  echo "─────────────────────────────────────────────────"
  echo "1. 打开 https://www.liuxue.online/ielts/login.html 登录"
  echo "2. F12 → Console → 输入：localStorage.ielts_user_token"
  echo "3. 复制结果（去掉两端引号）"
  echo ""
  read -p "粘贴 token： " TOKEN
  TOKEN=$(echo "$TOKEN" | tr -d ' "'"'"'')
else
  # ───────────────────── 自动模式：启本地服务 + 唤起浏览器授权 ─────────────────────
  echo "🌐 浏览器授权模式"
  echo "─────────────────────────────────────────────────"

  # 选一个空闲端口
  PORT=$(python3 -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1]);s.close()')
  STATE=$(python3 -c 'import secrets;print(secrets.token_urlsafe(16))')

  TMP_RESULT=$(mktemp)
  trap 'rm -f "$TMP_RESULT"' EXIT

  # 后台跑 Python HTTP 服务（写入 token 后立刻退出）
  python3 - "$PORT" "$STATE" "$TMP_RESULT" <<'PY' &
import sys, http.server, urllib.parse, threading, time

PORT = int(sys.argv[1])
EXPECT_STATE = sys.argv[2]
RESULT_PATH = sys.argv[3]

# 1x1 透明 GIF
GIF = bytes.fromhex('47494638396101000100800000ffffff00000021f90401000000002c00000000010001000002024401003b')

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass  # 静音

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', 'https://www.liuxue.online')
        self.send_header('Access-Control-Allow-Private-Network', 'true')

    def do_OPTIONS(self):
        self.send_response(204); self._cors()
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        q = urllib.parse.urlparse(self.path).query
        params = dict(urllib.parse.parse_qsl(q))

        # 校验 state
        if params.get('state') != EXPECT_STATE:
            self.send_response(400); self._cors(); self.end_headers(); return

        # 写入结果
        if 'token' in params:
            with open(RESULT_PATH, 'w') as f:
                f.write('OK\n' + params['token'] + '\n' + params.get('user', ''))
        elif 'error' in params:
            with open(RESULT_PATH, 'w') as f:
                f.write('ERR\n' + params['error'])

        # 返回 1x1 gif
        self.send_response(200); self._cors()
        self.send_header('Content-Type', 'image/gif')
        self.end_headers()
        self.wfile.write(GIF)

        # 异步停服务
        threading.Thread(target=lambda: (time.sleep(0.3), httpd.shutdown())).start()

httpd = http.server.HTTPServer(('127.0.0.1', PORT), H)
httpd.serve_forever()
PY
  SERVER_PID=$!

  # 拼授权 URL
  CALLBACK="http://127.0.0.1:$PORT/cb"
  CB_ENC=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$CALLBACK")
  HOSTNAME_LABEL=$(scutil --get ComputerName 2>/dev/null || hostname)
  CLIENT_ENC=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "WorkBuddy@$HOSTNAME_LABEL")
  AUTH_URL="$AUTH_PAGE?callback=$CB_ENC&state=$STATE&client=$CLIENT_ENC"

  echo ""
  echo "👉 即将打开浏览器，请在页面上点击「授权」"
  echo "   如果浏览器没自动弹出，请手动打开下面链接："
  echo ""
  echo "   $AUTH_URL"
  echo ""

  # 唤起浏览器（macOS / Linux 兼容）
  if command -v open >/dev/null 2>&1; then
    open "$AUTH_URL"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$AUTH_URL"
  fi

  # 等待结果（最多 180 秒）
  echo "⏳ 等待授权（180 秒超时）..."
  for i in $(seq 1 180); do
    if [[ -s "$TMP_RESULT" ]]; then break; fi
    sleep 1
  done

  # 关掉服务
  kill "$SERVER_PID" 2>/dev/null || true
  wait "$SERVER_PID" 2>/dev/null || true

  if [[ ! -s "$TMP_RESULT" ]]; then
    echo "❌ 等待超时，未收到授权回调。可重试或使用：bash $0 --manual"
    exit 1
  fi

  STATUS=$(sed -n '1p' "$TMP_RESULT")
  if [[ "$STATUS" != "OK" ]]; then
    REASON=$(sed -n '2p' "$TMP_RESULT")
    echo "❌ 授权失败：$REASON"
    exit 1
  fi
  TOKEN=$(sed -n '2p' "$TMP_RESULT")
  WEB_USER=$(sed -n '3p' "$TMP_RESULT")
  echo "✅ 已收到授权（账号：${WEB_USER:-?}）"
fi

if [[ -z "$TOKEN" ]]; then
  echo "❌ token 为空，已取消"
  exit 1
fi

# ──────────────────────────── 服务端二次校验 ────────────────────────────
echo ""
echo "🔍 校验 token 有效性..."
RESP=$(curl -s -X POST "$API_BASE" \
  -H 'Content-Type: application/json' \
  -d "{\"action\":\"getUserInfo\",\"token\":\"$TOKEN\"}")

CODE=$(echo "$RESP" | python3 -c "import json,sys;print(json.load(sys.stdin).get('code','?'))" 2>/dev/null || echo "?")
if [[ "$CODE" != "0" ]]; then
  echo "❌ token 无效或已过期"
  echo "   响应: $RESP"
  exit 1
fi
USERNAME=$(echo "$RESP" | python3 -c "import json,sys;print(json.load(sys.stdin).get('data',{}).get('username','?'))" 2>/dev/null || echo "?")
echo "✅ token 有效，账号：$USERNAME"

# ──────────────────────────── 写入 shell rc ────────────────────────────
echo ""
echo "💾 写入环境变量..."
SHELL_NAME=$(basename "$SHELL")
case "$SHELL_NAME" in
  zsh)  RC="$HOME/.zshrc" ;;
  bash) RC="$HOME/.bashrc" ;;
  *)    RC="$HOME/.profile" ;;
esac

if [[ -f "$RC" ]] && grep -q "IELTS_USER_TOKEN" "$RC"; then
  echo "  → 移除 $RC 中已有的 IELTS_USER_TOKEN"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' '/IELTS_USER_TOKEN/d' "$RC"
  else
    sed -i '/IELTS_USER_TOKEN/d' "$RC"
  fi
fi

cat >> "$RC" << EOF

# IELTS Reading Review — 客户端 token (added by setup-client-mode.sh)
export IELTS_USER_TOKEN='$TOKEN'
EOF

echo "✅ 已写入 $RC"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✅ 授权完成！账号：$USERNAME"
echo ""
echo "  下一步："
echo "  1. 重开终端 或 运行：source $RC"
echo "  2. 验证：echo \"\${IELTS_USER_TOKEN:0:20}...\""
echo "  3. 现在可以直接说「复盘剑X-TestX-PassageX」"
echo "═══════════════════════════════════════════════════════════"
