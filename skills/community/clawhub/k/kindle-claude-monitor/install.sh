#!/bin/bash
# Kindle Claude Monitor — install script
# 把 server.py / notify.sh 部署到 ~/.claude/kindle-monitor/，注册 launchd，
# 在 ~/.claude/settings.json append 7 个 hook（不动既有 hooks）。

set -e

SKILL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RUNTIME_DIR="$HOME/.claude/kindle-monitor"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
PLIST_DST="$LAUNCH_AGENTS/com.user.kindle-monitor.plist"
SETTINGS="$HOME/.claude/settings.json"

# ---- 1. 检查依赖 ----
echo "==> 检查 python3..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. 请先安装 Python 3.8+"
  exit 1
fi
PYTHON_PATH=$(command -v python3)
echo "    python: $PYTHON_PATH"

echo "==> 检查 jq..."
if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: jq not found. macOS: brew install jq"
  exit 1
fi

# ---- 2. 拷贝运行时文件 ----
echo "==> 部署运行时文件到 $RUNTIME_DIR"
mkdir -p "$RUNTIME_DIR"
cp "$SKILL_DIR/scripts/server.py" "$RUNTIME_DIR/server.py"
cp "$SKILL_DIR/scripts/notify.sh" "$RUNTIME_DIR/notify.sh"
chmod +x "$RUNTIME_DIR/server.py" "$RUNTIME_DIR/notify.sh"
echo "    server.py + notify.sh 已部署"

# ---- 3. 渲染并安装 launchd plist ----
echo "==> 安装 launchd plist"
mkdir -p "$LAUNCH_AGENTS"
sed -e "s|__PYTHON_PATH__|$PYTHON_PATH|g" \
    -e "s|__HOME__|$HOME|g" \
    "$SKILL_DIR/templates/com.user.kindle-monitor.plist" > "$PLIST_DST"
echo "    $PLIST_DST"

# ---- 4. 启动（如果已经启动过先卸载）----
echo "==> 启动 server"
launchctl unload "$PLIST_DST" 2>/dev/null || true
launchctl load "$PLIST_DST"
sleep 2

# ---- 5. 验证 ----
if curl -s -m 2 http://localhost:8787/healthz | grep -q ok; then
  echo "    ✓ server 已启动 (http://localhost:8787/)"
else
  echo "    ✗ server 启动失败，看 $RUNTIME_DIR/launchd.err.log"
  exit 1
fi

# ---- 6. 注册 hooks 到 settings.json ----
echo "==> 注册 7 个 hook 到 $SETTINGS"
if [ ! -f "$SETTINGS" ]; then
  echo '{"hooks": {}}' > "$SETTINGS"
fi

# 备份
cp "$SETTINGS" "$SETTINGS.bak.$(date +%Y%m%d-%H%M%S)"

python3 <<PY
import json, os
p = "$SETTINGS"
with open(p) as f:
    cfg = json.load(f)
hooks = cfg.setdefault("hooks", {})

def append_kindle(category, event_label):
    arr = hooks.setdefault(category, [])
    cmd = "~/.claude/kindle-monitor/notify.sh " + event_label
    for entry in arr:
        for h in entry.get("hooks", []):
            if h.get("command") == cmd:
                return False
    arr.append({
        "matcher": "*",
        "hooks": [{"type": "command", "command": cmd, "timeout": 1}]
    })
    return True

added = []
for evt in ["SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse",
            "Notification", "Stop", "SessionEnd"]:
    if append_kindle(evt, evt):
        added.append(evt)

with open(p, "w") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
print(f"    +{len(added)} hooks: {added}")
PY

# ---- 7. 防火墙提示 ----
STEALTH=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode 2>/dev/null | grep -i "stealth mode is on" || true)
if [ -n "$STEALTH" ]; then
  echo
  echo "⚠️  检测到 macOS 防火墙隐身模式开启——Kindle 可能连不上。"
  echo "    请手动跑（需要 sudo）："
  echo "    sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode off"
fi

# ---- 8. 显示 LAN IP ----
LAN_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "<unknown>")
cat <<EOF

==================================================
✅ Kindle Claude Monitor 安装完成

Mac 浏览器:    http://localhost:8787/
Kindle 浏览器:  http://${LAN_IP}:8787/   (同一 WiFi 下)
紧急重置:       http://localhost:8787/reset
日志:           $RUNTIME_DIR/events.jsonl

下次新开 Claude Code 会话时所有事件都会自动转发。
本会话之后开的 hook 也立即生效。
==================================================
EOF
