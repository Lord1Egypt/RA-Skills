#!/bin/bash
# Loudy.ai 自动任务 Skill 安装脚本
# 使用方法: curl -fsSL https://raw.githubusercontent.com/sfsf332/claw-loudyai-skill/main/install.sh | bash

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的信息
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# 检查依赖
check_dependencies() {
    info "检查依赖..."
    
    if ! command -v git &> /dev/null; then
        error "Git 未安装，请先安装 Git"
    fi
    
    if ! command -v python3 &> /dev/null; then
        error "Python3 未安装，请先安装 Python3"
    fi
    
    success "依赖检查通过"
}

# 获取安装路径
get_install_path() {
    # 优先使用 OPENCLAW_SKILLS_DIR 环境变量
    if [ -n "$OPENCLAW_SKILLS_DIR" ]; then
        INSTALL_DIR="$OPENCLAW_SKILLS_DIR"
    else
        # 默认路径
        INSTALL_DIR="/usr/lib/node_modules/openclaw/skills"
    fi
    
    info "安装路径: $INSTALL_DIR"
}

# 创建目录
create_directories() {
    info "创建目录..."
    
    if [ ! -d "$INSTALL_DIR" ]; then
        warning "目录 $INSTALL_DIR 不存在，尝试创建..."
        mkdir -p "$INSTALL_DIR" || error "无法创建目录 $INSTALL_DIR，请检查权限"
    fi
    
    # 检查写入权限
    if [ ! -w "$INSTALL_DIR" ]; then
        error "没有写入权限: $INSTALL_DIR，请以 root 用户运行或使用 sudo"
    fi
    
    success "目录创建完成"
}

# 克隆仓库
clone_repository() {
    info "克隆仓库..."
    
    cd "$INSTALL_DIR"
    
    # 如果目录已存在，先删除
    if [ -d "loudy-ai-auto-task" ]; then
        warning "目录已存在，正在删除..."
        rm -rf loudy-ai-auto-task
    fi
    
    # 克隆仓库
    git clone https://github.com/sfsf332/claw-loudyai-skill.git loudy-ai-auto-task || error "克隆仓库失败"
    
    success "仓库克隆完成"
}

# 设置权限
set_permissions() {
    info "设置权限..."
    
    cd "$INSTALL_DIR/loudy-ai-auto-task"
    
    # 设置脚本可执行权限
    if [ -d "scripts" ]; then
        chmod +x scripts/*.py scripts/*.sh 2>/dev/null || true
    fi
    
    success "权限设置完成"
}

# 验证安装
verify_installation() {
    info "验证安装..."
    
    cd "$INSTALL_DIR/loudy-ai-auto-task"
    
    # 检查必要文件
    if [ ! -f "SKILL.md" ]; then
        error "SKILL.md 文件缺失"
    fi
    
    # 检查 Python 语法
    if [ -d "scripts" ]; then
        for file in scripts/*.py; do
            if [ -f "$file" ]; then
                python3 -m py_compile "$file" || error "Python 语法错误: $file"
            fi
        done
    fi
    
    success "安装验证通过"
}

# 打印使用说明
print_usage() {
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}  安装成功！${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo -e "${BLUE}使用说明:${NC}"
    echo ""
    echo "1. 配置 API Key (推荐环境变量方式):"
    echo -e "   ${YELLOW}export LOUDY_API_KEY=你的API密钥${NC}"
    echo ""
    echo "2. 在 OpenClaw 中对 AI 说:"
    echo -e "   ${YELLOW}\"查看 loudy 可用奖池\"${NC}"
    echo ""
    echo "3. 根据提示发推文，然后将推文链接发给 AI:"
    echo -e "   ${YELLOW}\"提交推文链接 https://x.com/... 到奖池 3\"${NC}"
    echo ""
    echo -e "${BLUE}注意事项:${NC}"
    echo "- 请妥善保管 API Key，不要分享给他人"
    echo "- 建议将 API Key 设置为环境变量，不要写入文件"
    echo "- 默认安装路径: $INSTALL_DIR"
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo ""
}

# 主函数
main() {
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}  Loudy.ai 自动任务 Skill 安装脚本${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    
    check_dependencies
    get_install_path
    create_directories
    clone_repository
    set_permissions
    verify_installation
    print_usage
    
    exit 0
}

# 运行主函数
main "$@"
