#!/usr/bin/env bash
# lis-skill-bus 安装脚本（纯文本、可回滚、幂等）
# 用法: bash install_skillbus.sh [--dry-run|--apply|--uninstall]
# 环境变量: CODEX_HOME 默认 $HOME/.codex; SKIP_MCP_REG=1 只复制不注册 MCP
set -euo pipefail

MODE="${1:---help}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
BUS_DIR="$CODEX_HOME/mcp_servers/lis-skill-bus"
CONFIG="$CODEX_HOME/config.toml"
SECTION_LINE="[mcp_servers.lis-skill-bus]"
SKIP_MCP_REG="${SKIP_MCP_REG:-0}"

die() { echo "❌ $*" >&2; exit 1; }
info() { echo "→ $*"; }
ok()   { echo "✔ $*"; }

copy_runtime() {
  mkdir -p "$BUS_DIR/schemas" "$BUS_DIR/integration" "$BUS_DIR/example_pilot"
  cp "$SCRIPT_DIR/skillbus.py" "$SCRIPT_DIR/skillbus_client.py" "$BUS_DIR/"
  cp "$SCRIPT_DIR/README.md" "$SCRIPT_DIR/SKILL.md" "$SCRIPT_DIR/BENEFITS.md" "$SCRIPT_DIR/mcp-config.example.json" "$BUS_DIR/" 2>/dev/null || true
  cp "$SCRIPT_DIR/schemas/"*.json "$BUS_DIR/schemas/" 2>/dev/null || true
  cp "$SCRIPT_DIR/integration/"*.sh "$SCRIPT_DIR/integration/"*.cmd "$BUS_DIR/integration/" 2>/dev/null || true
  cp "$SCRIPT_DIR/example_pilot/"* "$BUS_DIR/example_pilot/" 2>/dev/null || true
  chmod +x "$BUS_DIR/skillbus.py" "$BUS_DIR/skillbus_client.py" 2>/dev/null || true
  chmod +x "$BUS_DIR/integration/"*.sh "$BUS_DIR/example_pilot/"*.sh 2>/dev/null || true
}

registered() {
  [[ -f "$CONFIG" ]] && grep -Fq "$SECTION_LINE" "$CONFIG"
}

if [[ "$MODE" == "--help" || "$MODE" == "-h" ]]; then
  echo "用法: bash install_skillbus.sh [--dry-run|--apply|--uninstall]"
  echo "  --dry-run   只预览将写入的路径与 config 变更，不写盘"
  echo "  --apply     复制 runtime 到 \$CODEX_HOME/mcp_servers/lis-skill-bus；默认注册 MCP（SKIP_MCP_REG=1 跳过注册）"
  echo "  --uninstall 只摘除 config 中的 MCP 注册段，保留已装 bus 文件"
  echo "环境: CODEX_HOME(默认 \$HOME/.codex), SKIP_MCP_REG(0/1)"
  exit 0
fi

case "$MODE" in
  --dry-run)
    info "BUS_DIR=$BUS_DIR"
    info "CONFIG=$CONFIG"
    info "将复制: skillbus.py / skillbus_client.py / README / SKILL / BENEFITS / mcp-config / schemas / integration / example_pilot"
    if registered; then
      info "检测到 config 已注册 $SECTION_LINE → 保持幂等，不会重复写入。"
    else
      info "将注册: $SECTION_LINE （SKIP_MCP_REG=1 时跳过）"
    fi
    exit 0
    ;;
  --uninstall)
    if registered; then
      cp "$CONFIG" "$CONFIG.skillbus.$(date +%Y%m%d%H%M%S).bak"
      awk -v pat="$SECTION_LINE" '$0==pat {skip=1; next} skip && /^\[/ {skip=0} !skip' "$CONFIG" > "$CONFIG.tmp"
      mv "$CONFIG.tmp" "$CONFIG"
      ok "已移除 $SECTION_LINE （config 已备份；bus 文件保留在 $BUS_DIR）"
    else
      ok "未注册 MCP，无需卸载。"
    fi
    exit 0
    ;;
  --apply)
    ;;
  *) die "未知模式: $MODE（--dry-run / --apply / --uninstall / --help）";;
esac

[[ -d "$CODEX_HOME" ]] || die "未找到 \$CODEX_HOME=$CODEX_HOME"

copy_runtime
ok "bus runtime 已复制到 $BUS_DIR"
info "验证: python3 \"$BUS_DIR/skillbus.py\" list-skills"

if [[ "$SKIP_MCP_REG" == "1" ]]; then
  info "SKIP_MCP_REG=1，跳过 MCP 注册（后续需要可再次 --apply）。"
  exit 0
fi

if registered; then
  ok "config 已注册 $SECTION_LINE → 跳过写入（幂等）"
else
  mkdir -p "$(dirname "$CONFIG")"
  if [[ -f "$CONFIG" ]]; then
    cp "$CONFIG" "$CONFIG.skillbus.$(date +%Y%m%d%H%M%S).bak"
  fi
  cat >> "$CONFIG" <<EOF

$SECTION_LINE
type = "stdio"
command = "$BUS_DIR/skillbus.py"
args = ["serve"]
EOF
  ok "已写入 $CONFIG（原文件已备份，可用 --uninstall 回滚）"
fi

echo
info "重启 Codex / 新开对话后，将出现 mcp__lis_skill_bus__* 工具。"
