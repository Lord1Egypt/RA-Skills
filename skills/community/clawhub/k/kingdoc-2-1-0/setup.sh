#!/usr/bin/env bash
# KingDoc Linux/macOS 安装脚本
set -e

echo ""
echo "============================================"
echo "  KingDoc - Kingsoft Docs AI Assistant"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3.10+ required"
    exit 1
fi
echo "[OK] Python: $(which python3)"

# Create venv
VENV_DIR="$(dirname "$0")/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "[..] Creating venv..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# Install deps
echo "[..] Installing dependencies..."
pip install -q requests mcp python-docx python-pptx pyyaml 2>/dev/null
echo "[OK] Dependencies installed"

# Get App credentials
echo ""
echo "Get credentials from: https://developer.kdocs.cn"
echo ""
read -p "App ID: " APP_ID
read -sp "App Secret: " APP_SECRET
echo ""

# Save config
CONFIG_PATH="$(dirname "$0")/config.json"
cat > "$CONFIG_PATH" << EOF
{
  "appName": "kingdoc",
  "appId": "$APP_ID",
  "appSecret": "$APP_SECRET",
  "scope": "user:file:write user:file:read team:file:write team:file:read",
  "environment": "production"
}
EOF
echo "[OK] Config saved"

# Create MCP config
cat > "$(dirname "$0")/mcp-config.json" << MEOF
{
  "kingdoc": {
    "command": "python",
    "args": ["-m", "engine.api.mcp_server", "--config", "./config.json"],
    "env": {},
    "description": "KingDoc — Kingsoft Docs AI Assistant"
  }
}
MEOF
echo "[OK] MCP config created"

# Create templates
cat > "$(dirname "$0")/templates/meeting_notes.md" << 'TEOF'
# 会议纪要

**会议时间**：{{date}}
**参会人员**：{{participants}}
**主持人**：{{host}}

## 议题

{{topics}}

## 讨论要点

{{discussion_points}}

## 决策事项

{{decisions}}

## 待办事项

| 序号 | 事项 | 负责人 | 截止日期 |
|------|------|--------|---------|
| 1 | {{task1}} | {{owner1}} | {{deadline1}} |
| 2 | {{task2}} | {{owner2}} | {{deadline2}} |
TEOF
echo "[OK] meeting_notes template created"

cat > "$(dirname "$0")/templates/weekly_report.md" << 'TEOF'
# 周报 {{week_range}}

**姓名**：{{name}}
**部门**：{{department}}
**日期**：{{date}}

## 本周完成

{{this_week_done}}

## 本周收获

{{this_week_learnings}}

## 遇到的问题

{{issues}}

## 下周计划

{{next_week_plan}}

## 需要协助

{{needs_help}}
TEOF
echo "[OK] weekly_report template created"

# Create assets placeholder
mkdir -p "$(dirname "$0")/assets/screenshots"
cat > "$(dirname "$0")/assets/icon_placeholder.txt" << 'AEOF'
Replace this file with a 256x256 icon.png for KingDoc
AEOF
echo "[OK] assets placeholder created"

# Set script permissions
chmod +x "$(dirname "$0")/scripts/env_check.sh" 2>/dev/null || true
chmod +x "$(dirname "$0")/scripts/setup.sh" 2>/dev/null || true
echo "[OK] Script permissions set"

# Test
echo "[..] Testing connection..."
python3 "$(dirname "$0")/engine/auth.py" --config "$CONFIG_PATH" --test 2>&1 && {
    echo "[OK] Connection successful!"
} || {
    echo "[WARN] Connection failed. Check credentials."
}

echo ""
echo "============================================"
echo "  Done! Restart WorkBuddy to use KingDoc"
echo "============================================"
