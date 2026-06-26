#!/bin/bash

# 二号重启迁移 Skill 安装脚本
# 版本: 1.0
# 创建时间: 2026-03-08

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查OpenClaw环境
check_openclaw() {
    log_info "检查OpenClaw环境..."
    
    if command -v openclaw &> /dev/null; then
        log_success "OpenClaw已安装"
        OPENCLAW_VERSION=$(openclaw --version 2>/dev/null || echo "未知版本")
        log_info "OpenClaw版本: $OPENCLAW_VERSION"
    else
        log_error "未找到OpenClaw，请先安装OpenClaw"
        exit 1
    fi
    
    # 检查workspace目录
    WORKSPACE_DIR="$HOME/.openclaw/workspace"
    if [ -d "$WORKSPACE_DIR" ]; then
        log_success "Workspace目录存在: $WORKSPACE_DIR"
    else
        log_warning "Workspace目录不存在，尝试创建..."
        mkdir -p "$WORKSPACE_DIR"
        log_success "已创建workspace目录"
    fi
}

# 备份现有文件
backup_existing() {
    log_info "备份现有文件..."
    
    BACKUP_DIR="$HOME/.openclaw/backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # 备份核心文件
    for file in IDENTITY.md USER.md SOUL.md AGENTS.md HEARTBEAT.md TOOLS.md MEMORY.md SESSION-STATE.md; do
        if [ -f "$WORKSPACE_DIR/$file" ]; then
            cp "$WORKSPACE_DIR/$file" "$BACKUP_DIR/"
            log_info "已备份: $file"
        fi
    done
    
    # 备份记忆目录
    if [ -d "$WORKSPACE_DIR/memory" ]; then
        cp -r "$WORKSPACE_DIR/memory" "$BACKUP_DIR/"
        log_info "已备份: memory/ 目录"
    fi
    
    # 备份技能配置
    if [ -f "$WORKSPACE_DIR/skills-integration.json" ]; then
        cp "$WORKSPACE_DIR/skills-integration.json" "$BACKUP_DIR/"
        log_info "已备份: skills-integration.json"
    fi
    
    log_success "备份完成，位置: $BACKUP_DIR"
    echo "如需恢复备份，请运行: cp -r $BACKUP_DIR/* $WORKSPACE_DIR/"
}

# 恢复核心文件
restore_core_files() {
    log_info "恢复核心文件..."
    
    # 恢复身份文件
    cp config/identity/*.md "$WORKSPACE_DIR/"
    log_success "已恢复身份文件"
    
    # 恢复操作系统文件
    cp config/system/*.md "$WORKSPACE_DIR/"
    log_success "已恢复操作系统文件"
    
    # 恢复技能配置
    cp config/skills/*.json "$WORKSPACE_DIR/"
    cp config/skills/*.md "$WORKSPACE_DIR/"
    log_success "已恢复技能配置"
}

# 恢复记忆文件
restore_memory() {
    log_info "恢复记忆文件..."
    
    # 创建记忆目录
    mkdir -p "$WORKSPACE_DIR/memory"
    
    # 恢复记忆文件
    cp -r config/memory/* "$WORKSPACE_DIR/memory/"
    log_success "已恢复记忆文件"
    
    # 设置正确的权限
    chmod -R 644 "$WORKSPACE_DIR/memory"/*.md
    log_info "已设置文件权限"
}

# 设置API密钥
setup_api_keys() {
    log_info "设置API密钥..."
    
    echo "=== API密钥配置 ==="
    echo "以下API密钥将被设置到环境变量中："
    echo ""
    echo "1. Moltbook API: moltbook_sk_4fM49PqzeqgI8jB5-qpV4x_CjiXAHHWW"
    echo "2. Manus网站API: 2552833787adbb6f3c5dae8c0c7dbba6d819fa344d7818a4d3537ffa535df5a4"
    echo "3. JWT密钥: 875b2e36d87bb4a67f706f34fb1f377a5a9d7a62487fe98fc753e0ccdd2f9d73"
    echo ""
    
    read -p "是否设置这些API密钥？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 创建环境变量文件
        ENV_FILE="$WORKSPACE_DIR/.二号环境变量"
        cat > "$ENV_FILE" << EOF
# 二号环境变量配置
# 创建时间: $(date)

# Moltbook API配置
export MOLTBOOK_API_KEY="moltbook_sk_4fM49PqzeqgI8jB5-qpV4x_CjiXAHHWW"
export MOLTBOOK_USERNAME="siliconone"

# Manus网站配置
export MANUS_API_KEY="2552833787adbb6f3c5dae8c0c7dbba6d819fa344d7818a4d3537ffa535df5a4"
export MANUS_JWT_SECRET="875b2e36d87bb4a67f706f34fb1f377a5a9d7a62487fe98fc753e0ccdd2f9d73"
export MANUS_WEBSITE_URL="https://earthguide-mcqwuxxb.manus.space"

# 其他配置
export OPENCLAW_ADMIN_KEY="2552833787adbb6f3c5dae8c0c7dbba6d819fa344d7818a4d3537ffa535df5a4"
export TZ="Asia/Shanghai"
EOF
        
        log_success "环境变量文件已创建: $ENV_FILE"
        echo "请将以下行添加到你的shell配置文件中（~/.bashrc, ~/.zshrc等）:"
        echo "source \"$ENV_FILE\""
    else
        log_warning "跳过API密钥设置"
    fi
}

# 验证安装
verify_installation() {
    log_info "验证安装..."
    
    # 检查核心文件
    REQUIRED_FILES=("IDENTITY.md" "USER.md" "SOUL.md" "AGENTS.md" "HEARTBEAT.md" "TOOLS.md" "MEMORY.md" "SESSION-STATE.md")
    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$WORKSPACE_DIR/$file" ]; then
            log_success "✓ $file 存在"
        else
            log_error "✗ $file 缺失"
        fi
    done
    
    # 检查记忆目录
    if [ -d "$WORKSPACE_DIR/memory" ]; then
        MEMORY_FILES=$(find "$WORKSPACE_DIR/memory" -name "*.md" | wc -l)
        log_success "✓ memory/ 目录存在，包含 $MEMORY_FILES 个记忆文件"
    else
        log_error "✗ memory/ 目录缺失"
    fi
    
    # 检查技能配置
    if [ -f "$WORKSPACE_DIR/skills-integration.json" ]; then
        log_success "✓ skills-integration.json 存在"
    else
        log_error "✗ skills-integration.json 缺失"
    fi
    
    log_info "安装验证完成"
}

# 显示完成信息
show_completion() {
    echo ""
    echo "========================================="
    echo "       二号重启迁移安装完成！"
    echo "========================================="
    echo ""
    echo "已成功恢复二号的所有状态："
    echo ""
    echo "✅ 身份文件：IDENTITY.md, USER.md, SOUL.md"
    echo "✅ 操作系统：AGENTS.md, HEARTBEAT.md, TOOLS.md"
    echo "✅ 记忆系统：MEMORY.md + memory/ 目录"
    echo "✅ 技能集成：11个技能的完整生态系统"
    echo "✅ 当前状态：SESSION-STATE.md"
    echo "✅ API配置：环境变量文件"
    echo ""
    echo "下一步操作："
    echo "1. 重启OpenClaw服务：openclaw gateway restart"
    echo "2. 启动二号会话"
    echo "3. 运行验证脚本：./verify.sh"
    echo "4. 测试所有功能"
    echo ""
    echo "重要提醒："
    echo "• 备份文件位于: $BACKUP_DIR"
    echo "• 环境变量文件: $ENV_FILE"
    echo "• 详细指南: 二号完整状态迁移指南.md"
    echo ""
    echo "如有问题，请参考故障排除指南或联系支持。"
    echo ""
}

# 主安装流程
main() {
    echo ""
    echo "========================================="
    echo "   二号重启迁移 Skill 安装程序"
    echo "========================================="
    echo ""
    
    # 检查环境
    check_openclaw
    
    # 确认安装
    echo "此操作将："
    echo "1. 备份现有的workspace文件"
    echo "2. 恢复二号的所有状态文件"
    echo "3. 设置必要的API密钥"
    echo "4. 配置技能集成"
    echo ""
    read -p "是否继续安装？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "安装已取消"
        exit 0
    fi
    
    # 执行安装步骤
    backup_existing
    restore_core_files
    restore_memory
    setup_api_keys
    verify_installation
    show_completion
}

# 运行主函数
main "$@"