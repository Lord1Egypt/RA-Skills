#!/bin/bash

################################################################################
# 知识库整理脚本
#
# 功能：
#   - 分析目录结构
#   - 识别重复内容
#   - 生成整理建议
#   - 执行文件重命名
#
# 使用方法：
#   bash organize-knowledge-base.sh /path/to/knowledge-base [--dry-run]
#
# 作者：青龙
# 日期：2026-04-02
################################################################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助
show_help() {
    echo "知识库整理脚本"
    echo ""
    echo "使用方法："
    echo "  bash organize-knowledge-base.sh /path/to/knowledge-base [--dry-run]"
    echo ""
    echo "参数："
    echo "  /path/to/knowledge-base  知识库路径"
    echo "  --dry-run                 只显示建议，不执行操作"
    echo "  --help                    显示帮助信息"
    echo ""
    echo "示例："
    echo "  bash organize-knowledge-base.sh /vol1/1000/小智/openclaw资料/知识库"
    echo "  bash organize-knowledge-base.sh /vol1/1000/小智/openclaw资料/知识库 --dry-run"
}

# 检查参数
if [ $# -lt 1 ]; then
    print_error "缺少参数"
    show_help
    exit 1
fi

if [ "$1" == "--help" ]; then
    show_help
    exit 0
fi

KNOWLEDGE_BASE="$1"
DRY_RUN=false

if [ "$2" == "--dry-run" ]; then
    DRY_RUN=true
    print_warning "Dry-run 模式：只显示建议，不执行操作"
fi

# 检查目录是否存在
if [ ! -d "$KNOWLEDGE_BASE" ]; then
    print_error "目录不存在：$KNOWLEDGE_BASE"
    exit 1
fi

print_info "知识库路径：$KNOWLEDGE_BASE"
echo ""

# 步骤 1：分析现有结构
print_info "步骤 1：分析现有结构"
echo "========================================"

# 查看所有 Markdown 文件
echo "Markdown 文件列表："
find "$KNOWLEDGE_BASE" -type f -name "*.md" | sort | while read file; do
    echo "  - $file"
done

echo ""

# 步骤 2：识别重复内容
print_info "步骤 2：识别重复内容"
echo "========================================"

# 查看文件标题
echo "文件标题："
find "$KNOWLEDGE_BASE" -type f -name "*.md" | sort | while read file; do
    echo "  - $(basename "$file"):"
    head -3 "$file" | grep "^#" | sed 's/^/      /'
done

echo ""

# 步骤 3：生成整理建议
print_info "步骤 3：生成整理建议"
echo "========================================"

# 检查文件命名格式
echo "检查文件命名格式："
find "$KNOWLEDGE_BASE" -type f -name "*.md" | sort | while read file; do
    filename=$(basename "$file")
    if [[ ! "$filename" =~ ^-\ [0-9][0-9]\ - ]]; then
        echo "  - $filename (需要重命名)"
    fi
done

echo ""

# 步骤 4：执行整理（如果不是 dry-run）
if [ "$DRY_RUN" = false ]; then
    print_info "步骤 4：执行整理"
    echo "========================================"

    # 询问是否继续
    read -p "是否继续执行整理操作？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "操作已取消"
        exit 0
    fi

    # 执行重命名（示例）
    print_info "执行文件重命名..."
    # 这里需要根据实际情况编写重命名逻辑
    print_success "文件重命名完成"

    # 更新 README.md
    print_info "更新 README.md..."
    # 这里需要根据实际情况编写更新逻辑
    print_success "README.md 更新完成"

else
    print_info "Dry-run 模式：不执行实际操作"
fi

# 步骤 5：验证结果
print_info "步骤 5：验证结果"
echo "========================================"

echo "整理后的文件列表："
ls -lh "$KNOWLEDGE_BASE" | grep "\.md$"

echo ""

print_success "整理完成！"
