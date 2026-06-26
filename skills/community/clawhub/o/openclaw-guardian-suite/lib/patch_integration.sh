#!/usr/bin/env bash
# patch_integration.sh — 跨技能联动补丁
# 用法: bash patch_integration.sh <SKILLS_TARGET> <LIB_TARGET> <IDENTIFIER>
set -euo pipefail

SKILLS_TARGET="${1:?SKILLS_TARGET required}"
LIB_TARGET="${2:?LIB_TARGET required}"
IDENTIFIER="${3:-unknown}"

GREEN='\033[0;32m'; BLUE='\033[0;34m'; RESET='\033[0m'
info()    { echo -e "${BLUE}  [patch]${RESET} $*"; }
success() { echo -e "${GREEN}  [ok]${RESET}    $*"; }

# ── 1. config-preflight-validator → .lib/ 软链接 ──────────────────────────────
CPV_SRC="$SKILLS_TARGET/config-preflight-validator/scripts/config-preflight-validator.py"
CPV_DST="$LIB_TARGET/config-preflight-validator.py"
if [ -f "$CPV_SRC" ]; then
  ln -sf "$CPV_SRC" "$CPV_DST"
  success "config-preflight-validator.py → .lib/ 软链接完成"
else
  info "警告：config-preflight-validator.py 未找到，跳过软链接"
fi

# ── 2. 统一备份目录（gateway-auto-rollback + config-modification 共享）─────────
BACKUP_DIR="${HOME}/.openclaw/backup"
mkdir -p "$BACKUP_DIR"
success "备份目录确保存在: $BACKUP_DIR"

# config-modification auto_rollback.py 引用的备份目录
# （auto_rollback.py 读取 ~/.openclaw/backup，已是默认值，无需 patch）

# gateway-auto-rollback 的备份目录同为 ~/.openclaw/backup/，已对齐

# ── 3. openclaw-health-audit config.json 初始化 ──────────────────────────────
HA_DIR="$SKILLS_TARGET/openclaw-health-audit"
CONF_TMPL="$HA_DIR/config/config.template.json"
CONF_FILE="$HA_DIR/config/config.json"
if [ -f "$CONF_TMPL" ] && [ ! -f "$CONF_FILE" ]; then
  cp "$CONF_TMPL" "$CONF_FILE"
  success "openclaw-health-audit config.json 已从模板初始化"
elif [ -f "$CONF_FILE" ]; then
  info "openclaw-health-audit config.json 已存在，跳过"
fi

# ── 4. model-failover-doctor 备份目录 ────────────────────────────────────────
MFD_BACKUP="${HOME}/.openclaw/workspace/.lib/.mfd_backups"
mkdir -p "$MFD_BACKUP"
success "model-failover-doctor 备份目录确保存在: $MFD_BACKUP"

# ── 5. compaction-proxy routes.json 存在性检查（不覆盖已有配置）────────────────
ROUTES_FILE="${HOME}/.openclaw/compaction-proxy/routes.json"
if [ ! -f "$ROUTES_FILE" ]; then
  mkdir -p "$(dirname "$ROUTES_FILE")"
  cat > "$ROUTES_FILE" << 'ROUTES_EOF'
{
  "custom-llmapi-lovbrowser-com": {
    "baseUrl": "https://llmapi.lovbrowser.com",
    "apiKey": "<LOVBROWSER_API_KEY>"
  }
}
ROUTES_EOF
  chmod 600 "$ROUTES_FILE"
  success "compaction-proxy routes.json 模板已创建（请填入真实 API Key）"
else
  info "compaction-proxy routes.json 已存在，保留现有配置"
fi

# ── 6. logs 目录 ──────────────────────────────────────────────────────────────
mkdir -p "${HOME}/.openclaw/logs"
success "日志目录确保存在: ~/.openclaw/logs"

echo ""
echo "  跨技能联动补丁全部完成。"
echo "  授权副本标识: $IDENTIFIER"
