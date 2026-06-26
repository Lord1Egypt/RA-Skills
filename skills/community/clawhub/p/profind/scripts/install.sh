#!/bin/bash
#===============================================================================
# install.sh — ProFind Skill 安装脚本
#
# 功能：安装 ProFind（若未安装）+ 复制技能文件 + 配置权限
# 用法：./install.sh
#===============================================================================

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()    { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }
confirm() { echo -e "${YELLOW}[CONFIRM]${NC} $*"; }

echo ""
echo "========================================"
echo "  ProFind Skill 安装程序"
echo "========================================"
echo ""

#-----------------------------------------------------------------------------
# 1. 检查 ProFind 是否已安装
#-----------------------------------------------------------------------------
info "检查 ProFind 安装状态..."

if [ -d "/Applications/ProFind.app" ]; then
    VERSION=$(defaults read /Applications/ProFind.app/Contents/Info.plist CFBundleShortVersionString 2>/dev/null)
    info "✓ ProFind 已安装: v${VERSION}"
else
    warn "ProFind 未安装，正在打开下载页面..."
    open "https://apps.apple.com/app/id1559203395"
    confirm "请先安装 ProFind 后，按回车继续..."
    read -r
fi

#-----------------------------------------------------------------------------
# 2. 复制技能文件到 OpenClaw
#-----------------------------------------------------------------------------
SKILL_DIR="$HOME/Library/Application Support/QClaw/openclaw/config/skills/profind-skill"
info "复制技能文件到: $SKILL_DIR"
mkdir -p "$SKILL_DIR"
cp "$(dirname "$0")/../SKILL.md" "$SKILL_DIR/SKILL.md"
info "✓ 技能文件已安装"

#-----------------------------------------------------------------------------
# 3. 创建用户脚本目录
#-----------------------------------------------------------------------------
USER_SCRIPT_DIR="$HOME/Library/Scripts/ProFind"
info "创建用户脚本目录: $USER_SCRIPT_DIR"
mkdir -p "$USER_SCRIPT_DIR"
info "✓ 用户脚本目录创建完成"
info "  → 将 .scpt / .sh 脚本放到此目录，ProFind 即可识别"

#-----------------------------------------------------------------------------
# 4. 权限检查
#-----------------------------------------------------------------------------
info "检查完全磁盘访问权限..."
FULL_DISK_ACCESS=$(sqlite3 ~/Library/Application\ Support/com.apple.TCC/TCC.db \
    "SELECT service FROM access WHERE service='kTCCServiceSystemPolicyAllFiles' AND allowed=1;" 2>/dev/null)

if [ -n "$FULL_DISK_ACCESS" ]; then
    info "✓ 完全磁盘访问权限已授予"
else
    warn "⚠ 完全磁盘访问权限未检测到"
    info "  请手动配置："
    info "  系统偏好设置 → 隐私与安全性 → 完全磁盘访问 → 勾选 ProFind"
fi

#-----------------------------------------------------------------------------
# 5. 验证安装
#-----------------------------------------------------------------------------
info "验证安装..."
if osascript -e 'tell application "ProFind" to open location "profind:search?name=test"' 2>/dev/null; then
    info "✓ ProFind URL Scheme 验证通过"
else
    warn "⚠ URL Scheme 验证失败，ProFind 可能需要重启"
fi

echo ""
info "========================================"
info "  安装完成！"
info "========================================"
info ""
info "使用方式："
info "  1. 在 OpenClaw 中直接描述搜索需求即可"
info "  2. 示例：'帮我找 Documents 里的 PDF 文件'"
info "  3. ProFind 会自动打开并展示搜索结果"
info ""
info "自定义脚本："
info "  → 放置到: $USER_SCRIPT_DIR"
info ""
