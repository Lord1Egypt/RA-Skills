#!/bin/bash

# 男装电商系统技能验证脚本
# 验证技能文件的完整性和正确性

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

# 检查文件是否存在
check_file_exists() {
    local file="$1"
    local description="$2"
    
    if [ -f "$file" ]; then
        print_success "$description: $file"
        return 0
    else
        print_error "$description: $file (文件不存在)"
        return 1
    fi
}

# 检查文件内容
check_file_content() {
    local file="$1"
    local pattern="$2"
    local description="$3"
    
    if [ -f "$file" ] && grep -q "$pattern" "$file"; then
        print_success "$description: 包含 '$pattern'"
        return 0
    else
        print_error "$description: 未找到 '$pattern'"
        return 1
    fi
}

# 检查文件大小
check_file_size() {
    local file="$1"
    local min_size="$2"
    local description="$3"
    
    if [ -f "$file" ]; then
        local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
        if [ "$size" -ge "$min_size" ]; then
            print_success "$description: ${size} bytes"
            return 0
        else
            print_error "$description: 文件过小 (${size} bytes < ${min_size} bytes)"
            return 1
        fi
    else
        print_error "$description: 文件不存在"
        return 1
    fi
}

# 验证技能主文件
validate_skill_md() {
    print_info "验证 SKILL.md 文件..."
    
    local errors=0
    
    # 检查文件存在
    check_file_exists "SKILL.md" "技能主文件" || ((errors++))
    
    # 检查YAML frontmatter
    check_file_content "SKILL.md" "name: $SKILL_NAME" "技能名称" || ((errors++))
    check_file_content "SKILL.md" "description:" "技能描述" || ((errors++))
    
    # 检查文件大小
    check_file_size "SKILL.md" 1000 "技能主文件大小" || ((errors++))
    
    # 检查技能内容
    check_file_content "SKILL.md" "技能执行流程" "技能执行流程" || ((errors++))
    check_file_content "SKILL.md" "技术栈详情" "技术栈详情" || ((errors++))
    check_file_content "SKILL.md" "参考文件" "参考文件" || ((errors++))
    
    if [ $errors -eq 0 ]; then
        print_success "SKILL.md 验证通过"
    else
        print_error "SKILL.md 验证失败，发现 $errors 个问题"
    fi
    
    return $errors
}

# 验证参考文件
validate_references() {
    print_info "验证参考文件..."
    
    local errors=0
    local reference_files=(
        "references/backend-architecture.md"
        "references/frontend-architecture.md"
        "references/database-schema.md"
        "references/api-specification.md"
    )
    
    for file in "${reference_files[@]}"; do
        if [ -f "$file" ]; then
            local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
            if [ "$size" -ge 500 ]; then
                print_success "$file: ${size} bytes"
            else
                print_error "$file: 文件过小 (${size} bytes)"
                ((errors++))
            fi
        else
            print_error "$file: 文件不存在"
            ((errors++))
        fi
    done
    
    # 检查续篇文件
    local continued_files=(
        "references/frontend-architecture-continued.md"
        "references/database-schema-continued.md"
        "references/api-specification-continued.md"
    )
    
    for file in "${continued_files[@]}"; do
        if [ -f "$file" ]; then
            local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
            print_info "$file: ${size} bytes (续篇文件)"
        fi
    done
    
    if [ $errors -eq 0 ]; then
        print_success "参考文件验证通过"
    else
        print_error "参考文件验证失败，发现 $errors 个问题"
    fi
    
    return $errors
}

# 验证脚本文件
validate_scripts() {
    print_info "验证脚本文件..."
    
    local errors=0
    local script_files=(
        "scripts/generate-project.sh"
        "scripts/generate-project-continued.sh"
        "scripts/init.sh"
        "scripts/package-skill.sh"
        "scripts/validate-skill.sh"
    )
    
    for file in "${script_files[@]}"; do
        if [ -f "$file" ]; then
            # 检查文件可执行权限
            if [ -x "$file" ] || [[ "$file" == *.sh && -f "$file" ]]; then
                local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
                print_success "$file: ${size} bytes"
                
                # 检查脚本头部
                if head -n 1 "$file" | grep -q "^#!/bin/bash"; then
                    print_success "  ✓ 正确的shebang"
                else
                    print_warning "  ⚠ 缺少或错误的shebang"
                fi
            else
                print_error "$file: 缺少可执行权限"
                ((errors++))
            fi
        else
            print_error "$file: 文件不存在"
            ((errors++))
        fi
    done
    
    if [ $errors -eq 0 ]; then
        print_success "脚本文件验证通过"
    else
        print_error "脚本文件验证失败，发现 $errors 个问题"
    fi
    
    return $errors
}

# 验证示例文件
validate_examples() {
    print_info "验证示例文件..."
    
    local errors=0
    
    if [ -f "examples/usage-example.md" ]; then
        local size=$(stat -f%z "examples/usage-example.md" 2>/dev/null || stat -c%s "examples/usage-example.md")
        if [ "$size" -ge 1000 ]; then
            print_success "examples/usage-example.md: ${size} bytes"
            
            # 检查示例内容
            if grep -q "技能触发" "examples/usage-example.md" && \
               grep -q "技能执行流程" "examples/usage-example.md"; then
                print_success "  ✓ 包含完整的示例内容"
            else
                print_warning "  ⚠ 示例内容不完整"
            fi
        else
            print_error "examples/usage-example.md: 文件过小 (${size} bytes)"
            ((errors++))
        fi
    else
        print_warning "examples/usage-example.md: 文件不存在 (可选文件)"
    fi
    
    if [ $errors -eq 0 ]; then
        print_success "示例文件验证通过"
    else
        print_error "示例文件验证失败，发现 $errors 个问题"
    fi
    
    return $errors
}

# 验证README文件
validate_readme() {
    print_info "验证README文件..."
    
    local errors=0
    
    if [ -f "README.md" ]; then
        local size=$(stat -f%z "README.md" 2>/dev/null || stat -c%s "README.md")
        if [ "$size" -ge 500 ]; then
            print_success "README.md: ${size} bytes"
            
            # 检查README内容
            check_file_content "README.md" "技能概述" "README概述" || ((errors++))
            check_file_content "README.md" "项目结构" "项目结构" || ((errors++))
            check_file_content "README.md" "核心功能模块" "核心功能" || ((errors++))
        else
            print_error "README.md: 文件过小 (${size} bytes)"
            ((errors++))
        fi
    else
        print_error "README.md: 文件不存在"
        ((errors++))
    fi
    
    if [ $errors -eq 0 ]; then
        print_success "README文件验证通过"
    else
        print_error "README文件验证失败，发现 $errors 个问题"
    fi
    
    return $errors
}

# 验证目录结构
validate_directory_structure() {
    print_info "验证目录结构..."
    
    local errors=0
    local required_dirs=(
        "references"
        "scripts"
        "examples"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [ -d "$dir" ]; then
            print_success "目录存在: $dir/"
        else
            print_error "目录不存在: $dir/"
            ((errors++))
        fi
    done
    
    # 检查文件总数
    local total_files=$(find . -type f -name "*.md" -o -name "*.sh" | wc -l)
    print_info "总文件数: $total_files"
    
    if [ $errors -eq 0 ]; then
        print_success "目录结构验证通过"
    else
        print_error "目录结构验证失败，发现 $errors 个问题"
    fi
    
    return $errors
}

# 生成验证报告
generate_validation_report() {
    local total_errors=$1
    
    echo ""
    echo "=" * 60
    echo "技能验证报告"
    echo "=" * 60
    echo "技能名称: $SKILL_NAME"
    echo "验证时间: $(date)"
    echo "总问题数: $total_errors"
    echo ""
    
    if [ $total_errors -eq 0 ]; then
        print_success "✅ 技能验证通过！技能文件完整且正确。"
        echo ""
        echo "技能可以正常使用，建议："
        echo "1. 运行 ./scripts/package-skill.sh 打包技能"
        echo "2. 将技能包部署到OpenClaw"
        echo "3. 测试技能功能"
    else
        print_error "❌ 技能验证失败！发现 $total_errors 个问题需要修复。"
        echo ""
        echo "需要修复的问题："
        echo "1. 检查缺失的文件"
        echo "2. 修复文件内容问题"
        echo "3. 确保文件大小符合要求"
        echo "4. 重新运行验证脚本"
    fi
    
    echo "=" * 60
}

# 主函数
main() {
    print_info "开始验证男装电商系统技能..."
    echo ""
    
    local total_errors=0
    
    # 执行各项验证
    validate_skill_md
    total_errors=$((total_errors + $?))
    
    echo ""
    validate_references
    total_errors=$((total_errors + $?))
    
    echo ""
    validate_scripts
    total_errors=$((total_errors + $?))
    
    echo ""
    validate_examples
    total_errors=$((total_errors + $?))
    
    echo ""
    validate_readme
    total_errors=$((total_errors + $?))
    
    echo ""
    validate_directory_structure
    total_errors=$((total_errors + $?))
    
    # 生成验证报告
    generate_validation_report $total_errors
    
    return $total_errors
}

# 运行主函数
main "$@"