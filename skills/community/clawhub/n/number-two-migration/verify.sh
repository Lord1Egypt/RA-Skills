#!/bin/bash

# 二号重启迁移 Skill 验证脚本
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

# 工作空间目录
WORKSPACE_DIR="$HOME/.openclaw/workspace"

# 检查文件存在性
check_file_exists() {
    local file="$1"
    local description="$2"
    
    if [ -f "$WORKSPACE_DIR/$file" ]; then
        log_success "✓ $description ($file) 存在"
        return 0
    else
        log_error "✗ $description ($file) 缺失"
        return 1
    fi
}

# 检查目录存在性
check_dir_exists() {
    local dir="$1"
    local description="$2"
    
    if [ -d "$WORKSPACE_DIR/$dir" ]; then
        local file_count=$(find "$WORKSPACE_DIR/$dir" -type f | wc -l)
        log_success "✓ $description ($dir) 存在，包含 $file_count 个文件"
        return 0
    else
        log_error "✗ $description ($dir) 缺失"
        return 1
    fi
}

# 检查文件内容
check_file_content() {
    local file="$1"
    local keyword="$2"
    local description="$3"
    
    if [ -f "$WORKSPACE_DIR/$file" ]; then
        if grep -q "$keyword" "$WORKSPACE_DIR/$file"; then
            log_success "✓ $description 内容正确"
            return 0
        else
            log_warning "⚠ $description 内容可能不完整"
            return 1
        fi
    else
        log_error "✗ 文件不存在: $file"
        return 1
    fi
}

# 验证核心身份文件
verify_identity() {
    log_info "验证核心身份文件..."
    
    check_file_exists "IDENTITY.md" "身份文件"
    check_file_exists "USER.md" "用户信息文件"
    check_file_exists "SOUL.md" "灵魂定义文件"
    
    # 检查关键内容
    check_file_content "IDENTITY.md" "二号" "身份定义"
    check_file_content "USER.md" "创造者" "用户信息"
    check_file_content "SOUL.md" "技能集成" "灵魂定义"
}

# 验证操作系统文件
verify_os() {
    log_info "验证操作系统文件..."
    
    check_file_exists "AGENTS.md" "操作系统规则"
    check_file_exists "HEARTBEAT.md" "心跳检查清单"
    check_file_exists "TOOLS.md" "工具配置"
    check_file_exists "SESSION-STATE.md" "当前状态"
    
    # 检查关键内容
    check_file_content "AGENTS.md" "WAL协议" "操作系统功能"
    check_file_content "HEARTBEAT.md" "安全检查" "心跳系统"
    check_file_content "SESSION-STATE.md" "当前任务" "工作状态"
}

# 验证记忆系统
verify_memory() {
    log_info "验证记忆系统..."
    
    check_dir_exists "memory" "记忆目录"
    check_file_exists "MEMORY.md" "长期记忆"
    
    # 检查记忆文件
    if [ -d "$WORKSPACE_DIR/memory" ]; then
        # 检查最近的记忆文件
        recent_files=$(find "$WORKSPACE_DIR/memory" -name "2026-03-*.md" | head -5)
        for file in $recent_files; do
            local filename=$(basename "$file")
            log_success "✓ 记忆文件: $filename"
        done
        
        # 检查心跳状态
        if [ -f "$WORKSPACE_DIR/memory/heartbeat-state.json" ]; then
            log_success "✓ 心跳状态文件存在"
        else
            log_warning "⚠ 心跳状态文件缺失"
        fi
    fi
    
    # 检查长期记忆内容
    check_file_content "MEMORY.md" "重要教训" "长期记忆"
}

# 验证技能集成
verify_skills() {
    log_info "验证技能集成..."
    
    check_file_exists "skills-integration.json" "技能集成配置"
    check_file_exists "skills-auto-trigger.md" "技能自动触发规则"
    
    # 检查技能集成状态
    if [ -f "$WORKSPACE_DIR/skills-integration.json" ]; then
        local skill_count=$(grep -c '"name"' "$WORKSPACE_DIR/skills-integration.json" 2>/dev/null || echo "0")
        if [ "$skill_count" -ge 10 ]; then
            log_success "✓ 技能集成配置完整 ($skill_count 个技能)"
        else
            log_warning "⚠ 技能集成可能不完整 ($skill_count 个技能)"
        fi
    fi
}

# 验证API配置
verify_api() {
    log_info "验证API配置..."
    
    # 检查环境变量文件
    local env_file="$WORKSPACE_DIR/.二号环境变量"
    if [ -f "$env_file" ]; then
        log_success "✓ 环境变量文件存在: $env_file"
        
        # 检查关键环境变量
        if grep -q "MOLTBOOK_API_KEY" "$env_file"; then
            log_success "✓ Moltbook API配置存在"
        else
            log_warning "⚠ Moltbook API配置缺失"
        fi
        
        if grep -q "MANUS_API_KEY" "$env_file"; then
            log_success "✓ Manus API配置存在"
        else
            log_warning "⚠ Manus API配置缺失"
        fi
    else
        log_warning "⚠ 环境变量文件不存在"
        echo "建议运行: source scripts/setup-api-keys.sh"
    fi
}

# 验证OpenClaw服务
verify_openclaw() {
    log_info "验证OpenClaw服务..."
    
    if command -v openclaw &> /dev/null; then
        log_success "✓ OpenClaw已安装"
        
        # 检查服务状态
        if openclaw gateway status &> /dev/null; then
            log_success "✓ OpenClaw网关服务运行中"
        else
            log_warning "⚠ OpenClaw网关服务未运行"
            echo "建议运行: openclaw gateway start"
        fi
    else
        log_error "✗ OpenClaw未安装"
    fi
}

# 运行功能测试
run_functional_tests() {
    log_info "运行功能测试..."
    
    # 测试1: 检查文件可读性
    log_info "测试1: 文件可读性测试"
    for file in "IDENTITY.md" "AGENTS.md" "MEMORY.md"; do
        if [ -r "$WORKSPACE_DIR/$file" ]; then
            log_success "✓ $file 可读"
        else
            log_error "✗ $file 不可读"
        fi
    done
    
    # 测试2: 检查记忆系统完整性
    log_info "测试2: 记忆系统完整性"
    if [ -f "$WORKSPACE_DIR/MEMORY.md" ] && [ -d "$WORKSPACE_DIR/memory" ]; then
        local memory_lines=$(wc -l < "$WORKSPACE_DIR/MEMORY.md")
        local daily_files=$(find "$WORKSPACE_DIR/memory" -name "*.md" | wc -l)
        
        if [ "$memory_lines" -gt 50 ] && [ "$daily_files" -ge 3 ]; then
            log_success "✓ 记忆系统完整 (长期记忆: $memory_lines 行, 每日记忆: $daily_files 个文件)"
        else
            log_warning "⚠ 记忆系统可能不完整"
        fi
    fi
    
    # 测试3: 检查技能集成
    log_info "测试3: 技能集成检查"
    if [ -f "$WORKSPACE_DIR/skills-integration.json" ]; then
        local integration_status=$(grep -o '"integrationStatus": *"[^"]*"' "$WORKSPACE_DIR/skills-integration.json" | cut -d'"' -f4)
        if [ "$integration_status" = "complete" ]; then
            log_success "✓ 技能集成状态: $integration_status"
        else
            log_warning "⚠ 技能集成状态: $integration_status"
        fi
    fi
}

# 生成验证报告
generate_report() {
    log_info "生成验证报告..."
    
    local report_file="$WORKSPACE_DIR/迁移验证报告_$(date +%Y%m%d-%H%M%S).md"
    
    cat > "$report_file" << EOF
# 二号重启迁移验证报告

## 验证信息
- **验证时间:** $(date)
- **工作空间目录:** $WORKSPACE_DIR
- **OpenClaw版本:** $(openclaw --version 2>/dev/null || echo "未知")

## 验证结果

### 1. 核心身份文件
$(if [ -f "$WORKSPACE_DIR/IDENTITY.md" ]; then echo "✅ IDENTITY.md 存在"; else echo "❌ IDENTITY.md 缺失"; fi)
$(if [ -f "$WORKSPACE_DIR/USER.md" ]; then echo "✅ USER.md 存在"; else echo "❌ USER.md 缺失"; fi)
$(if [ -f "$WORKSPACE_DIR/SOUL.md" ]; then echo "✅ SOUL.md 存在"; else echo "❌ SOUL.md 缺失"; fi)

### 2. 操作系统文件
$(if [ -f "$WORKSPACE_DIR/AGENTS.md" ]; then echo "✅ AGENTS.md 存在"; else echo "❌ AGENTS.md 缺失"; fi)
$(if [ -f "$WORKSPACE_DIR/HEARTBEAT.md" ]; then echo "✅ HEARTBEAT.md 存在"; else echo "❌ HEARTBEAT.md 缺失"; fi)
$(if [ -f "$WORKSPACE_DIR/TOOLS.md" ]; then echo "✅ TOOLS.md 存在"; else echo "❌ TOOLS.md 缺失"; fi)
$(if [ -f "$WORKSPACE_DIR/SESSION-STATE.md" ]; then echo "✅ SESSION-STATE.md 存在"; else echo "❌ SESSION-STATE.md 缺失"; fi)

### 3. 记忆系统
$(if [ -d "$WORKSPACE_DIR/memory" ]; then echo "✅ memory/ 目录存在"; else echo "❌ memory/ 目录缺失"; fi)
$(if [ -f "$WORKSPACE_DIR/MEMORY.md" ]; then echo "✅ MEMORY.md 存在"; else echo "❌ MEMORY.md 缺失"; fi)

### 4. 技能集成
$(if [ -f "$WORKSPACE_DIR/skills-integration.json" ]; then echo "✅ skills-integration.json 存在"; else echo "❌ skills-integration.json 缺失"; fi)
$(if [ -f "$WORKSPACE_DIR/skills-auto-trigger.md" ]; then echo "✅ skills-auto-trigger.md 存在"; else echo "❌ skills-auto-trigger.md 缺失"; fi)

### 5. API配置
$(if [ -f "$WORKSPACE_DIR/.二号环境变量" ]; then echo "✅ 环境变量文件存在"; else echo "❌ 环境变量文件缺失"; fi)

## 建议
1. 确保所有✅标记的文件都存在
2. 如有❌标记，请重新运行安装脚本
3. 启动OpenClaw服务: openclaw gateway start
4. 测试二号功能

## 状态总结
$(if [ -f "$WORKSPACE_DIR/IDENTITY.md" ] && [ -f "$WORKSPACE_DIR/AGENTS.md" ] && [ -f "$WORKSPACE_DIR/MEMORY.md" ] && [ -d "$WORKSPACE_DIR/memory" ]; then
    echo "**✅ 迁移成功** - 二号状态已完整恢复"
else
    echo "**⚠ 迁移不完整** - 请检查缺失的文件"
fi)

---
*验证报告生成时间: $(date)*
EOF
    
    log_success "验证报告已生成: $report_file"
    echo "查看完整报告: cat $report_file"
}

# 主验证流程
main() {
    echo ""
    echo "========================================="
    echo "   二号重启迁移 Skill 验证程序"
    echo "========================================="
    echo ""
    
    # 检查工作空间目录
    if [ ! -d "$WORKSPACE_DIR" ]; then
        log_error "工作空间目录不存在: $WORKSPACE_DIR"
        echo "请先运行安装脚本: ./install.sh"
        exit 1
    fi
    
    # 执行验证步骤
    verify_identity
    verify_os
    verify_memory
    verify_skills
    verify_api
    verify_openclaw
    run_functional_tests
    generate_report
    
    echo ""
    echo "========================================="
    echo "          验证完成"
    echo "========================================="
    echo ""
    echo "所有验证步骤已完成。"
    echo "请查看上面的结果，确保所有检查都通过。"
    echo ""
    echo "如有问题，请参考:"
    echo "1. 验证报告文件"
    echo "2. 故障排除指南"
    echo "3. 重新运行安装脚本"
    echo ""
}

# 运行主函数
main "$@"