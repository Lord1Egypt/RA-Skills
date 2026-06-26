#!/bin/bash
# create-rescue-instance.sh - 创建 OpenClaw 救援 Gateway 实例
# 用法：./create-rescue-instance.sh [实例编号] [端口]

set -e

INSTANCE_NUM=${1:-1}
PORT=${2:-$((19000 + INSTANCE_NUM * 1000))}
RESCUE_NAME="rescue${INSTANCE_NUM}"

echo "=== 创建救援实例 $RESCUE_NAME (端口 $PORT) ==="

# 1. 创建目录结构
RESCUE_DIR="$HOME/.openclaw-$RESCUE_NAME"
mkdir -p "$RESCUE_DIR"/{sessions,credentials,agents,workspace,logs}
echo "✓ 创建目录：$RESCUE_DIR"

# 2. 复制并修改配置文件
cp "$HOME/.openclaw/openclaw.json" "$RESCUE_DIR/openclaw.json"

# 修改端口
sed -i '' "s/\"port\": [0-9]*/\"port\": $PORT/" "$RESCUE_DIR/openclaw.json"

# 修改工作目录
sed -i '' "s|\"workspace\": \"~/.openclaw/workspace\"|\"workspace\": \"~/.openclaw-$RESCUE_NAME/workspace\"|" "$RESCUE_DIR/openclaw.json"

# 禁用企业微信（避免冲突）
sed -i '' 's/"wecom": {/"wecom": {\n      "enabled": false,/' "$RESCUE_DIR/openclaw.json" 2>/dev/null || true

# 清空插件配置（避免冲突）
perl -i -0pe 's/"plugins":\s*\{[^}]*"allow":[^}]*\}/"plugins": {\n    "allow": [],\n    "entries": {},\n    "installs": {}\n  }/s' "$RESCUE_DIR/openclaw.json" 2>/dev/null || true

echo "✓ 配置文件：$RESCUE_DIR/openclaw.json"

# 3. 创建 LaunchAgent plist
PLIST_FILE="$HOME/Library/LaunchAgents/ai.openclaw.gateway-$RESCUE_NAME.plist"
cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>ai.openclaw.gateway-$RESCUE_NAME</string>
    <key>Comment</key>
    <string>OpenClaw Gateway $RESCUE_NAME (v2026.3.24)</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ThrottleInterval</key>
    <integer>1</integer>
    <key>Umask</key>
    <integer>63</integer>
    <key>ProgramArguments</key>
    <array>
      <string>/opt/homebrew/opt/node@22/bin/node</string>
      <string>/opt/homebrew/Cellar/node/25.8.0/lib/node_modules/openclaw/dist/index.js</string>
      <string>gateway</string>
      <string>--port</string>
      <string>$PORT</string>
    </array>
    <key>StandardOutPath</key>
    <string>$RESCUE_DIR/logs/gateway.log</string>
    <key>StandardErrorPath</key>
    <string>$RESCUE_DIR/logs/gateway.err.log</string>
    <key>EnvironmentVariables</key>
    <dict>
    <key>PATH</key>
    <string>/opt/homebrew/opt/node@22/bin:/Users/zhuobao/.local/bin:/Users/zhuobao/.npm-global/bin:/Users/zhuobao/bin:/Users/zhuobao/.volta/bin:/Users/zhuobao/.asdf/shims:/Users/zhuobao/.bun/bin:/Users/zhuobao/Library/Application Support/fnm/aliases/default/bin:/Users/zhuobao/.fnm/aliases/default/bin:/Users/zhuobao/Library/pnpm:/Users/zhuobao/.local/share/pnpm:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    <key>HOME</key>
    <string>/Users/zhuobao</string>
    <key>TMPDIR</key>
    <string>/var/folders/hq/dyyz3j2s51l80tfvfm6kpb5r0000gn/T/</string>
    <key>NODE_EXTRA_CA_CERTS</key>
    <string>/etc/ssl/cert.pem</string>
    <key>NODE_USE_SYSTEM_CA</key>
    <string>1</string>
    <key>OPENCLAW_CONFIG_PATH</key>
    <string>$RESCUE_DIR/openclaw.json</string>
    <key>OPENCLAW_STATE_DIR</key>
    <string>$RESCUE_DIR</string>
    <key>OPENCLAW_GATEWAY_PORT</key>
    <string>$PORT</string>
    <key>OPENCLAW_LAUNCHD_LABEL</key>
    <string>ai.openclaw.gateway-$RESCUE_NAME</string>
    <key>OPENCLAW_SERVICE_MARKER</key>
    <string>openclaw-$RESCUE_NAME</string>
    <key>OPENCLAW_SERVICE_KIND</key>
    <string>gateway</string>
    <key>OPENCLAW_SERVICE_VERSION</key>
    <string>2026.3.24</string>
    </dict>
  </dict>
</plist>
EOF
echo "✓ 服务文件：$PLIST_FILE"

# 4. 加载并启动服务
launchctl load "$PLIST_FILE"
echo "✓ 服务已加载"

# 5. 等待启动并检查
sleep 3
if curl -sk "https://localhost:$PORT/health" | grep -q '"status":"live"'; then
  echo "✓ 实例 $RESCUE_NAME 已启动 (端口 $PORT)"
  echo ""
  echo "访问地址：https://localhost:$PORT"
else
  echo "⚠ 实例可能未正常启动，请检查日志：$RESCUE_DIR/logs/gateway.err.log"
  exit 1
fi
