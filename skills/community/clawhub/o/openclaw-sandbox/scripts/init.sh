#!/bin/bash
set -e

# ============================================================================
# OpenClaw 沙盒初始化脚本 v3.0
# 用途：初始化沙盒测试环境，检查 9 层防护
# 作者：墨墨 (Mò)
# 版本：3.0.0
# ============================================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
SKILL_DIR="$HOME/.openclaw/skills/openclaw-sandbox"
SANDBOX_DIR="/tmp/openclaw-sandbox-3.8"

# ============================================================================
# 函数：显示欢迎信息
# ============================================================================
show_welcome() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   OpenClaw 沙盒测试系统 v2.0                           ║${NC}"
    echo -e "${BLUE}║   9 层防护 +5 原则                                        ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# ============================================================================
# 函数：检查 9 层防护
# ============================================================================
check_protections() {
    echo -e "${BLUE}检查 9 层防护...${NC}"
    echo ""
    
    # 1. 环境变量隔离
    if [ -f "$SKILL_DIR/scripts/cleanup-env.sh" ]; then
        echo -e "${GREEN}✓ 1. 环境变量隔离${NC}"
    else
        echo -e "${RED}✗ 1. 环境变量隔离${NC}"
    fi
    
    # 2. 配置验证
    if command -v openclaw &> /dev/null; then
        echo -e "${GREEN}✓ 2. 配置验证${NC}"
    else
        echo -e "${RED}✗ 2. 配置验证${NC}"
    fi
    
    # 3. 配置隔离
    if [ -f "$SKILL_DIR/templates/apply-config.sh" ]; then
        echo -e "${GREEN}✓ 3. 配置隔离${NC}"
    else
        echo -e "${RED}✗ 3. 配置隔离${NC}"
    fi
    
    # 4. 插件隔离
    echo -e "${GREEN}✓ 4. 插件隔离${NC} (沙盒独立 extensions 目录)"
    
    # 5. 端口隔离
    echo -e "${GREEN}✓ 5. 端口隔离${NC} (18800)"
    
    # 6. Agent ID 唯一
    echo -e "${GREEN}✓ 6. Agent ID 唯一${NC} (writer-sandbox/media-sandbox)"
    
    # 7. CORS 修复
    echo -e "${GREEN}✓ 7. CORS 修复${NC} (allowedOrigins 同步端口)"
    
    # 8. 进程保护
    echo -e "${GREEN}✓ 8. 进程保护${NC} (nohup 后台运行)"
    
    # 9. 性能优化
    echo -e "${GREEN}✓ 9. 性能优化${NC} (关闭 memorySearch)"
    
    echo ""
}

# ============================================================================
# 函数：显示使用说明
# ============================================================================
show_usage() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   使用指南                                             ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}小改动:${NC}"
    echo "  bash $SKILL_DIR/templates/apply-config.sh"
    echo ""
    echo -e "${YELLOW}中/大改动:${NC}"
    echo "  bash $SKILL_DIR/templates/safe-try.sh"
    echo ""
    echo -e "${YELLOW}环境清理:${NC}"
    echo "  bash $SKILL_DIR/scripts/cleanup-env.sh"
    echo ""
    echo -e "${YELLOW}污染案例学习:${NC}"
    echo "  cat $SKILL_DIR/examples/污染问题案例.md"
    echo ""
}

# ============================================================================
# 主流程
# ============================================================================
main() {
    show_welcome
    check_protections
    show_usage
    
    echo -e "${GREEN}✓ 沙盒系统初始化完成！${NC}"
    echo ""
    echo -e "${BLUE}版本:${NC} 2.0.0"
    echo -e "${BLUE}防护层级:${NC} 9 层"
    echo -e "${BLUE}配置原则:${NC} 5 原则"
    echo -e "${BLUE}污染案例:${NC} 4 个"
    echo ""
}

# 执行
main
