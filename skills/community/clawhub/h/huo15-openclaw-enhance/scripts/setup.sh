#!/usr/bin/env bash
#
# 龙虾增强包 — 一键安装脚本
#
# 用法:
#   方式1: npx @huo15/openclaw-enhance setup
#   方式2: bash <(curl -fsSL https://raw.githubusercontent.com/jobzhao15/openclaw-enhance/main/scripts/setup.sh)
#
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

OPENCLAW_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
PLUGIN_ID="enhance"
NPM_PACKAGE="@huo15/openclaw-enhance"

echo -e "${CYAN}🦞 龙虾增强包 (OpenClaw Enhancement Kit) 安装程序${NC}"
echo ""

# ── 1. 检测 OpenClaw ──
if [ ! -f "$OPENCLAW_DIR/openclaw.json" ]; then
  echo -e "${RED}✗ 未检测到 OpenClaw 安装（$OPENCLAW_DIR/openclaw.json 不存在）${NC}"
  echo "  请先安装 OpenClaw: https://openclaw.com"
  exit 1
fi
echo -e "${GREEN}✓${NC} 检测到 OpenClaw: $OPENCLAW_DIR"

# ── 2. 安装插件 ──
echo ""
echo -e "${CYAN}正在安装插件...${NC}"
if command -v openclaw &>/dev/null; then
  openclaw plugins install "$NPM_PACKAGE" || {
    echo -e "${YELLOW}⚠ openclaw plugins install 失败，尝试手动安装...${NC}"
    INSTALL_DIR="$OPENCLAW_DIR/extensions/openclaw-enhance"
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    npm init -y --silent 2>/dev/null || true
    npm install "$NPM_PACKAGE" --silent
    cd - >/dev/null
  }
else
  echo -e "${YELLOW}⚠ 未找到 openclaw CLI，使用手动安装模式${NC}"
  INSTALL_DIR="$OPENCLAW_DIR/extensions/openclaw-enhance"
  mkdir -p "$INSTALL_DIR"
  cd "$INSTALL_DIR"
  npm init -y --silent 2>/dev/null || true
  npm install "$NPM_PACKAGE" --silent
  cd - >/dev/null
fi
echo -e "${GREEN}✓${NC} 插件已安装"

# ── 3. 定位插件文件 ──
PLUGIN_DIR=""
for candidate in \
  "$OPENCLAW_DIR/extensions/openclaw-enhance/node_modules/$NPM_PACKAGE" \
  "$OPENCLAW_DIR/extensions/openclaw-enhance" \
  "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")/.."; do
  if [ -f "$candidate/openclaw.plugin.json" ]; then
    PLUGIN_DIR="$candidate"
    break
  fi
done

if [ -z "$PLUGIN_DIR" ]; then
  echo -e "${YELLOW}⚠ 无法定位插件文件目录，跳过技能和模板安装${NC}"
  echo "  你可以手动从 npm 包中复制 skills/ 和 templates/ 到工作区"
else
  # ── 4. 复制增强技能 ──
  echo ""
  echo -e "${CYAN}正在安装增强技能...${NC}"
  SKILLS_DIR="$OPENCLAW_DIR/workspace/skills"
  mkdir -p "$SKILLS_DIR"

  for skill in plan-mode explore-mode verify-mode memory-curator; do
    if [ -d "$PLUGIN_DIR/skills/$skill" ]; then
      if [ -d "$SKILLS_DIR/$skill" ]; then
        echo -e "  ${YELLOW}⚠ $skill 已存在，跳过${NC}"
      else
        cp -r "$PLUGIN_DIR/skills/$skill" "$SKILLS_DIR/"
        echo -e "  ${GREEN}✓${NC} $skill"
      fi
    fi
  done

  # ── 5. 应用工作区模板补丁 ──
  echo ""
  echo -e "${CYAN}正在应用工作区增强...${NC}"
  WS_DIR="$OPENCLAW_DIR/workspace"

  for file in AGENTS.md SOUL.md; do
    patch_file="$PLUGIN_DIR/templates/${file%.md}.enhance-patch.md"
    target_file="$WS_DIR/$file"

    if [ ! -f "$patch_file" ]; then
      continue
    fi

    if [ ! -f "$target_file" ]; then
      echo -e "  ${YELLOW}⚠ $target_file 不存在，跳过${NC}"
      continue
    fi

    # 检查是否已经打过补丁
    if grep -q "龙虾增强包补丁" "$target_file" 2>/dev/null; then
      echo -e "  ${YELLOW}⚠ $file 已包含增强补丁，跳过${NC}"
      continue
    fi

    # 备份并追加
    cp "$target_file" "${target_file}.bak.$(date +%Y%m%d%H%M%S)"
    cat "$patch_file" >> "$target_file"
    echo -e "  ${GREEN}✓${NC} $file 已增强（备份: ${file}.bak.*）"
  done
fi

# ── 6. 打印完成信息 ──
echo ""
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}  🦞 龙虾增强包安装完成！${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""
echo "  已安装模块:"
echo "    📦 结构化记忆 (enhance_memory_store/search/review)"
echo "    🛡️  工具安全守卫 (enhance_safety_log/rules)"
echo "    ✨ 提示词增强 (自动注入)"
echo "    🔄 工作流自动化 (enhance_workflow_define/list/delete)"
echo "    📊 仪表盘 (http://localhost:18789/plugins/enhance/)"
echo ""
echo "  已安装技能:"
echo "    📋 plan-mode — 结构化规划"
echo "    🔍 explore-mode — 深度探索"
echo "    ✅ verify-mode — 验证检查"
echo "    🧠 memory-curator — 记忆整理"
echo ""
echo -e "  ${CYAN}重启 OpenClaw 使插件生效:${NC}"
echo "    openclaw restart"
echo ""
echo -e "  ${CYAN}配置（可选）:${NC}"
echo "    编辑 $OPENCLAW_DIR/openclaw.json → plugins.entries.enhance.config"
echo ""
