#!/bin/bash
#
# QQBot 调试信息泄露修复脚本
# 功能：修复语音消息文件路径泄露给 LLM 的问题
# 作者：北京老李
# 版本：1.0
# 日期：2026-03-22
#

set -e

# 颜色定义
COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
COLOR_NC='\033[0m'

log_info() {
    echo -e "${COLOR_BLUE}[INFO]${COLOR_NC} $1"
}

log_success() {
    echo -e "${COLOR_GREEN}[PASS]${COLOR_NC} $1"
}

log_warning() {
    echo -e "${COLOR_YELLOW}[WARN]${COLOR_NC} $1"
}

log_error() {
    echo -e "${COLOR_RED}[FAIL]${COLOR_NC} $1"
}

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║   QQBot 调试信息泄露修复脚本                       ║"
echo "║   修复：语音消息文件路径泄露给 LLM 的问题          ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# 检查 QQBot 扩展目录
QQBOT_DIR="/root/.openclaw/extensions/qqbot"
if [ ! -d "$QQBOT_DIR" ]; then
    log_error "QQBot 扩展目录不存在：$QQBOT_DIR"
    exit 1
fi

log_info "QQBot 扩展目录：$QQBOT_DIR"

# 1. 修复 ref-index-store.ts
log_info "修复 ref-index-store.ts..."
REF_INDEX_FILE="$QQBOT_DIR/src/ref-index-store.ts"

if [ ! -f "$REF_INDEX_FILE" ]; then
    log_error "文件不存在：$REF_INDEX_FILE"
    exit 1
fi

# 检查是否已修复
if grep -q "// 移除 localPath 避免调试信息泄露给 LLM" "$REF_INDEX_FILE"; then
    log_success "ref-index-store.ts 已修复"
else
    # 备份原文件
    cp "$REF_INDEX_FILE" "$REF_INDEX_FILE.bak.$(date +%Y%m%d%H%M%S)"
    log_info "已备份原文件"
    
    # 修复文件
    sed -i 's/const sourceHint = att.localPath ? ` (${att.localPath})` : att.url ? ` (${att.url})` : "";/\/\/ 移除 localPath 避免调试信息泄露给 LLM\n      \/\/ const sourceHint = att.localPath ? ` (${att.localPath})` : att.url ? ` (${att.url})` : "";/' "$REF_INDEX_FILE"
    sed -i 's/parts.push(`\[语音消息（内容: "${att.transcript}"${sourceTag}）${sourceHint}\]`);/parts.push(`[语音消息（内容: "${att.transcript}"${sourceTag}）]`);/' "$REF_INDEX_FILE"
    sed -i 's/parts.push(`\[语音消息${sourceHint}\]`);/parts.push(`[语音消息]`);/' "$REF_INDEX_FILE"
    sed -i 's/parts.push(`\[图片${att.filename ? `: ${att.filename}` : ""}${sourceHint}\]`);/parts.push(`[图片${att.filename ? `: ${att.filename}` : ""}]`);/' "$REF_INDEX_FILE"
    sed -i 's/parts.push(`\[视频${att.filename ? `: ${att.filename}` : ""}${sourceHint}\]`);/parts.push(`[视频${att.filename ? `: ${att.filename}` : ""}]`);/' "$REF_INDEX_FILE"
    sed -i 's/parts.push(`\[文件${att.filename ? `: ${att.filename}` : ""}${sourceHint}\]`);/parts.push(`[文件${att.filename ? `: ${att.filename}` : ""}]`);/' "$REF_INDEX_FILE"
    sed -i 's/parts.push(`\[附件${att.filename ? `: ${att.filename}` : ""}${sourceHint}\]`);/parts.push(`[附件${att.filename ? `: ${att.filename}` : ""}]`);/' "$REF_INDEX_FILE"
    
    log_success "ref-index-store.ts 修复完成"
fi

# 2. 修复 gateway.ts
log_info "修复 gateway.ts..."
GATEWAY_FILE="$QQBOT_DIR/src/gateway.ts"

if [ ! -f "$GATEWAY_FILE" ]; then
    log_error "文件不存在：$GATEWAY_FILE"
    exit 1
fi

# 检查是否已修复
if grep -q "// 移除 localPath 避免调试信息泄露给 LLM" "$GATEWAY_FILE"; then
    log_success "gateway.ts 已修复"
else
    # 备份原文件
    cp "$GATEWAY_FILE" "$GATEWAY_FILE.bak.$(date +%Y%m%d%H%M%S)"
    log_info "已备份原文件"
    
    # 修复 onMessageSent 回调
    sed -i 's/const localPath = meta.mediaLocalPath;/\/\/ 移除 localPath 避免调试信息泄露给 LLM\n      \/\/ const localPath = meta.mediaLocalPath;/' "$GATEWAY_FILE"
    sed -i 's/\.\.\.(localPath ? { localPath } : {}),/\/\/ 移除 localPath: localPath ? { localPath } : {},/' "$GATEWAY_FILE"
    
    log_success "gateway.ts 修复完成"
fi

# 3. 清理旧缓存
log_info "清理旧引用索引缓存..."
CACHE_FILE="$HOME/.openclaw/qqbot/data/ref-index.jsonl"

if [ -f "$CACHE_FILE" ]; then
    rm -f "$CACHE_FILE"
    log_success "已清理旧缓存：$CACHE_FILE"
else
    log_info "缓存文件不存在，无需清理"
fi

# 4. 提示重启
echo ""
echo "═══════════════════════════════════════════════════════"
echo "  🎉 修复完成！"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "请执行以下命令重启 OpenClaw 使修复生效："
echo ""
echo "  ${COLOR_BLUE}openclaw gateway restart${COLOR_NC}"
echo ""
echo "重启后，调试信息（📎 文件路径）将不再出现。"
echo ""
echo "修复内容："
echo "  ✅ ref-index-store.ts - 引用消息格式化不再包含本地路径"
echo "  ✅ gateway.ts - 出站消息缓存不再保存本地路径"
echo "  ✅ 旧缓存已清理"
echo ""
