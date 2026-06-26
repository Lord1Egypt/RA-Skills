#!/bin/bash

# GitHub 安全克隆脚本
# 版本: 1.0.0
# 作者: 安全改进版
# 描述: 安全地从 GitHub 克隆项目，包含输入验证和安全检查

set -euo pipefail

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

# 显示使用说明
show_usage() {
    echo "GitHub 安全克隆脚本"
    echo "用法: $0 [选项] <GitHub_URL> [目标目录]"
    echo ""
    echo "选项:"
    echo "  -h, --help         显示此帮助信息"
    echo "  -s, --safe         启用安全检查（默认）"
    echo "  -d, --depth NUM    设置克隆深度（默认: 1）"
    echo "  -t, --temp         使用临时目录"
    echo "  --no-check         禁用安全检查"
    echo ""
    echo "示例:"
    echo "  $0 https://github.com/psf/requests"
    echo "  $0 -t https://github.com/psf/requests /tmp/requests_analysis"
    echo "  $0 --depth 5 https://github.com/psf/requests requests_deep"
}

# 验证 GitHub URL
validate_github_url() {
    local url="$1"
    
    # 基本格式验证
    if [[ ! "$url" =~ ^https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(/.*)?$ ]]; then
        log_error "URL 格式无效：必须来自 github.com"
        return 1
    fi
    
    # 移除 .git 后缀和尾部斜杠
    local clean_url="${url%.git}"
    clean_url="${clean_url%/}"
    
    # 提取仓库信息
    local repo_path="${clean_url#https://github.com/}"
    local owner_repo="${repo_path%%/*}/${repo_path#*/}"
    owner_repo="${owner_repo%%/*}/${owner_repo#*/}"
    
    echo "$owner_repo"
    return 0
}

# 检查仓库信息
check_repo_info() {
    local owner_repo="$1"
    
    log_info "检查仓库信息: $owner_repo"
    
    # 使用 GitHub API 获取仓库信息
    local api_url="https://api.github.com/repos/$owner_repo"
    local response
    
    if command -v curl &> /dev/null; then
        response=$(curl -s -H "Accept: application/vnd.github.v3+json" "$api_url")
    elif command -v wget &> /dev/null; then
        response=$(wget -qO- --header="Accept: application/vnd.github.v3+json" "$api_url")
    else
        log_warning "无法检查仓库信息：需要 curl 或 wget"
        return 0
    fi
    
    # 检查响应
    if [[ -z "$response" ]] || [[ "$response" == *"Not Found"* ]]; then
        log_error "仓库不存在或无法访问: $owner_repo"
        return 1
    fi
    
    # 提取信息
    local size=$(echo "$response" | grep -o '"size":[0-9]*' | cut -d: -f2)
    local stars=$(echo "$response" | grep -o '"stargazers_count":[0-9]*' | cut -d: -f2)
    local updated=$(echo "$response" | grep -o '"updated_at":"[^"]*"' | cut -d'"' -f4)
    
    log_info "仓库大小: $((size / 1024)) MB"
    log_info "星标数: $stars"
    log_info "最后更新: $updated"
    
    # 检查仓库大小（警告超过 100MB）
    if [[ $size -gt 102400 ]]; then
        log_warning "仓库较大 ($((size / 1024)) MB)，克隆可能需要较长时间"
    fi
    
    return 0
}

# 安全克隆仓库
safe_clone() {
    local url="$1"
    local target_dir="$2"
    local depth="${3:-1}"
    
    log_info "开始安全克隆..."
    log_info "URL: $url"
    log_info "目标目录: $target_dir"
    log_info "克隆深度: $depth"
    
    # 检查目标目录是否存在
    if [[ -d "$target_dir" ]]; then
        log_warning "目标目录已存在: $target_dir"
        read -p "是否覆盖？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_error "操作取消"
            return 1
        fi
        rm -rf "$target_dir"
    fi
    
    # 执行克隆
    if git clone --depth "$depth" "$url" "$target_dir" 2>/dev/null; then
        log_success "克隆成功"
        return 0
    else
        log_error "克隆失败"
        return 1
    fi
}

# 分析项目结构
analyze_project() {
    local target_dir="$1"
    
    log_info "分析项目结构..."
    
    # 检查目录是否存在
    if [[ ! -d "$target_dir" ]]; then
        log_error "目标目录不存在: $target_dir"
        return 1
    fi
    
    # 基本文件统计
    local total_files=$(find "$target_dir" -type f | wc -l)
    local total_dirs=$(find "$target_dir" -type d | wc -l)
    
    log_info "文件总数: $total_files"
    log_info "目录总数: $total_dirs"
    
    # 检查常见文件类型
    echo ""
    log_info "文件类型分布:"
    find "$target_dir" -type f -name "*.py" | wc -l | xargs echo "  Python 文件:"
    find "$target_dir" -type f -name "*.js" | wc -l | xargs echo "  JavaScript 文件:"
    find "$target_dir" -type f -name "*.json" | wc -l | xargs echo "  JSON 文件:"
    find "$target_dir" -type f -name "*.md" | wc -l | xargs echo "  Markdown 文件:"
    find "$target_dir" -type f -name "*.txt" | wc -l | xargs echo "  文本文件:"
    find "$target_dir" -type f -name "*.sh" | wc -l | xargs echo "  Shell 脚本:"
    
    # 检查依赖文件
    echo ""
    log_info "依赖文件检查:"
    
    if [[ -f "$target_dir/requirements.txt" ]]; then
        log_success "找到 requirements.txt"
        echo "  前10行内容:"
        head -10 "$target_dir/requirements.txt" | sed 's/^/    /'
    fi
    
    if [[ -f "$target_dir/package.json" ]]; then
        log_success "找到 package.json"
    fi
    
    if [[ -f "$target_dir/setup.py" ]]; then
        log_success "找到 setup.py"
    fi
    
    if [[ -f "$target_dir/pyproject.toml" ]]; then
        log_success "找到 pyproject.toml"
    fi
    
    # 检查 README
    echo ""
    log_info "文档检查:"
    for readme in "$target_dir/README.md" "$target_dir/README.rst" "$target_dir/README.txt" "$target_dir/README"; do
        if [[ -f "$readme" ]]; then
            log_success "找到 README: $(basename "$readme")"
            echo "  前5行内容:"
            head -5 "$readme" | sed 's/^/    /'
            break
        fi
    done
    
    # 检查可疑文件
    echo ""
    log_info "安全检查:"
    local suspicious_files=0
    
    # 检查潜在的危险文件
    for pattern in "*.sh" "*.bat" "*.cmd" "*.ps1" "*.exe" "*.bin"; do
        local count=$(find "$target_dir" -type f -name "$pattern" 2>/dev/null | wc -l)
        if [[ $count -gt 0 ]]; then
            log_warning "找到 $count 个 $pattern 文件"
            suspicious_files=$((suspicious_files + count))
        fi
    done
    
    if [[ $suspicious_files -eq 0 ]]; then
        log_success "未发现可疑文件"
    fi
    
    return 0
}

# 生成安全建议
generate_recommendations() {
    local target_dir="$1"
    
    echo ""
    log_info "安全建议:"
    echo "═══════════════════════════════════════"
    
    # Python 项目建议
    if [[ -f "$target_dir/requirements.txt" ]] || [[ -f "$target_dir/setup.py" ]] || [[ -f "$target_dir/pyproject.toml" ]]; then
        echo "🐍 Python 项目建议:"
        echo "  1. 创建虚拟环境:"
        echo "     python -m venv venv"
        echo "     source venv/bin/activate  # Linux/Mac"
        echo "     venv\\Scripts\\activate     # Windows"
        echo ""
        echo "  2. 安全安装依赖:"
        echo "     pip install --user -r requirements.txt"
        echo "     或使用国内镜像:"
        echo "     pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt"
        echo ""
        echo "  3. 检查依赖安全性:"
        echo "     pip list --outdated"
        echo "     pip-audit"
    fi
    
    # Node.js 项目建议
    if [[ -f "$target_dir/package.json" ]]; then
        echo "📦 Node.js 项目建议:"
        echo "  1. 检查 package.json:"
        echo "     npm audit"
        echo ""
        echo "  2. 安全安装:"
        echo "     npm ci  # 推荐，使用 package-lock.json"
        echo "     或"
        echo "     npm install --ignore-scripts  # 忽略安装脚本"
    fi
    
    # 通用建议
    echo "🔒 通用安全建议:"
    echo "  1. 在沙盒环境中测试:"
    echo "     - 使用 Docker 容器"
    echo "     - 使用虚拟机"
    echo "     - 使用临时系统"
    echo ""
    echo "  2. 代码审查:"
    echo "     - 检查所有脚本文件"
    echo "     - 验证外部依赖"
    echo "     - 查看提交历史"
    echo ""
    echo "  3. 权限控制:"
    echo "     - 不要使用 root 权限运行"
    echo "     - 限制文件系统访问"
    echo "     - 监控网络访问"
    
    echo "═══════════════════════════════════════"
}

# 主函数
main() {
    # 默认参数
    local safe_mode=true
    local use_temp=false
    local depth=1
    local url=""
    local target_dir=""
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                return 0
                ;;
            -s|--safe)
                safe_mode=true
                shift
                ;;
            --no-check)
                safe_mode=false
                shift
                ;;
            -d|--depth)
                depth="$2"
                shift 2
                ;;
            -t|--temp)
                use_temp=true
                shift
                ;;
            -*)
                log_error "未知选项: $1"
                show_usage
                return 1
                ;;
            *)
                if [[ -z "$url" ]]; then
                    url="$1"
                elif [[ -z "$target_dir" ]]; then
                    target_dir="$1"
                else
                    log_error "参数过多"
                    show_usage
                    return 1
                fi
                shift
                ;;
        esac
    done
    
    # 检查必要参数
    if [[ -z "$url" ]]; then
        log_error "必须提供 GitHub URL"
        show_usage
        return 1
    fi
    
    # 设置目标目录
    if [[ -z "$target_dir" ]]; then
        if [[ "$use_temp" == true ]]; then
            target_dir="/tmp/github_clone_$(date +%s)"
        else
            # 从 URL 提取仓库名作为目录名
            local repo_name=$(basename "$url" .git)
            target_dir="./$repo_name"
        fi
    fi
    
    # 创建目标目录
    mkdir -p "$(dirname "$target_dir")"
    
    echo ""
    log_info "🔒 GitHub 安全克隆工具"
    echo "═══════════════════════════════════════"
    
    # 验证 URL
    local owner_repo
    if ! owner_repo=$(validate_github_url "$url"); then
        return 1
    fi
    
    # 安全检查
    if [[ "$safe_mode" == true ]]; then
        if ! check_repo_info "$owner_repo"; then
            log_error "安全检查失败"
            return 1
        fi
    fi
    
    # 执行克隆
    if ! safe_clone "$url" "$target_dir" "$depth"; then
        return 1
    fi
    
    # 分析项目
    if ! analyze_project "$target_dir"; then
        return 1
    fi
    
    # 生成建议
    generate_recommendations "$target_dir"
    
    echo ""
    log_success "✅ 完成！项目已克隆到: $target_dir"
    log_info "💡 下一步: 在安全环境中测试项目"
    
    return 0
}

# 运行主函数
main "$@"