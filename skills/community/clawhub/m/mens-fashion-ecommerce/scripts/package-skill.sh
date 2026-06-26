#!/bin/bash

# 男装电商系统技能打包脚本
# 将技能打包为 .skill 文件

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 技能目录
SKILL_DIR="."
SKILL_NAME="mens-fashion-ecommerce"
OUTPUT_DIR="../dist"
PACKAGE_FILE="${OUTPUT_DIR}/${SKILL_NAME}.skill"

# 打印带颜色的消息
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

# 检查技能目录结构
validate_skill_structure() {
    print_info "验证技能目录结构..."
    
    # 检查必需文件
    required_files=(
        "SKILL.md"
        "README.md"
        "references/backend-architecture.md"
        "references/frontend-architecture.md"
        "references/database-schema.md"
        "references/api-specification.md"
        "scripts/generate-project.sh"
    )
    
    for file in "${required_files[@]}"; do
        if [ ! -f "${SKILL_DIR}/${file}" ]; then
            print_error "必需文件缺失: ${file}"
            return 1
        fi
    done
    
    # 检查SKILL.md格式
    if ! head -n 20 "${SKILL_DIR}/SKILL.md" | grep -q "name: ${SKILL_NAME}"; then
        print_error "SKILL.md中未找到正确的技能名称"
        return 1
    fi
    
    print_success "技能目录结构验证通过"
    return 0
}

# 创建输出目录
create_output_dir() {
    print_info "创建输出目录..."
    mkdir -p "${OUTPUT_DIR}"
    print_success "输出目录创建完成: ${OUTPUT_DIR}"
}

# 打包技能文件
package_skill() {
    print_info "打包技能文件..."
    
    # 创建临时目录
    TEMP_DIR=$(mktemp -d)
    
    # 复制技能文件到临时目录
    cp -r "${SKILL_DIR}"/* "${TEMP_DIR}/"
    
    # 移除不需要的文件
    cd "${TEMP_DIR}"
    find . -name "*.swp" -delete
    find . -name "*.swo" -delete
    find . -name ".DS_Store" -delete
    
    # 创建技能包
    zip -r "${PACKAGE_FILE}" . > /dev/null
    
    # 清理临时目录
    cd - > /dev/null
    rm -rf "${TEMP_DIR}"
    
    print_success "技能打包完成: ${PACKAGE_FILE}"
}

# 验证技能包
validate_package() {
    print_info "验证技能包..."
    
    if [ ! -f "${PACKAGE_FILE}" ]; then
        print_error "技能包文件未创建: ${PACKAGE_FILE}"
        return 1
    fi
    
    # 检查文件大小
    file_size=$(stat -f%z "${PACKAGE_FILE}" 2>/dev/null || stat -c%s "${PACKAGE_FILE}")
    if [ "${file_size}" -lt 1024 ]; then
        print_error "技能包文件过小: ${file_size} bytes"
        return 1
    fi
    
    # 检查文件内容
    if ! unzip -l "${PACKAGE_FILE}" | grep -q "SKILL.md"; then
        print_error "技能包中未包含SKILL.md文件"
        return 1
    fi
    
    print_success "技能包验证通过"
    print_info "文件大小: $((${file_size}/1024)) KB"
    return 0
}

# 生成技能清单
generate_manifest() {
    print_info "生成技能清单..."
    
    MANIFEST_FILE="${OUTPUT_DIR}/${SKILL_NAME}-manifest.txt"
    
    cat > "${MANIFEST_FILE}" << EOF
# 男装电商系统技能清单
技能名称: ${SKILL_NAME}
打包时间: $(date)
文件大小: $(stat -f%z "${PACKAGE_FILE}" 2>/dev/null || stat -c%s "${PACKAGE_FILE}") bytes

## 包含文件
EOF
    
    # 列出所有文件
    unzip -l "${PACKAGE_FILE}" | tail -n +4 | head -n -2 >> "${MANIFEST_FILE}"
    
    # 添加文件统计
    file_count=$(unzip -l "${PACKAGE_FILE}" | tail -n +4 | head -n -2 | wc -l)
    echo "" >> "${MANIFEST_FILE}"
    echo "## 统计信息" >> "${MANIFEST_FILE}"
    echo "文件总数: ${file_count}" >> "${MANIFEST_FILE}"
    
    print_success "技能清单生成完成: ${MANIFEST_FILE}"
}

# 主函数
main() {
    print_info "开始打包男装电商系统技能..."
    
    # 检查当前目录
    if [ ! -f "SKILL.md" ]; then
        print_error "请在技能目录中运行此脚本"
        exit 1
    fi
    
    # 执行打包步骤
    validate_skill_structure || exit 1
    create_output_dir
    package_skill
    validate_package || exit 1
    generate_manifest
    
    print_success "技能打包完成！"
    echo ""
    print_info "生成的技能包: ${PACKAGE_FILE}"
    print_info "技能清单: ${OUTPUT_DIR}/${SKILL_NAME}-manifest.txt"
    echo ""
    print_info "使用说明:"
    print_info "1. 将 ${SKILL_NAME}.skill 文件复制到OpenClaw的skills目录"
    print_info "2. 重启OpenClaw服务"
    print_info "3. 技能将自动加载并可用"
}

# 运行主函数
main "$@"