#!/bin/bash

# ============================================================================
# Nexus Agent Framework - 安全審計腳本
# Nexus Agent Framework - Security Audit Script
# 版本 Version: 1.0.0
# ============================================================================

set -e

# 顏色定義 | Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Emoji 定義 | Emoji definitions
CHECK_MARK="✅"
CROSS_MARK="❌"
WARNING="⚠️"
INFO="ℹ️"

# ============================================================================
# 幫助信息 | Help Information
# ============================================================================

show_help() {
    cat << EOF
Nexus Agent Framework - 安全審計腳本 | Security Audit Script

用法 | Usage: $0 [選項]

選項 | Options:
    -h, --help          顯示幫助信息 | Show this help message
    -v, --verbose       詳細輸出 | Verbose output
    -s, --skip-network  跳過網絡檢查 | Skip network checks
    -q, --quick         快速模式（只檢查關鍵項目）| Quick mode

示例 | Examples:
    $0                  # 完整審計 | Full audit
    $0 -v               # 詳細審計 | Verbose audit
    $0 -q               # 快速檢查 | Quick check

EOF
}

# ============================================================================
# 日誌函數 | Logging Functions
# ============================================================================

log_info() {
    echo -e "${BLUE}${INFO}${NC} $1"
}

log_success() {
    echo -e "${GREEN}${CHECK_MARK}${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}${WARNING}${NC} $1"
}

log_error() {
    echo -e "${RED}${CROSS_MARK}${NC} $1"
}

# ============================================================================
# 審計檢查 | Audit Checks
# ============================================================================

# 檢查 1: 文件權限 | Check 1: File Permissions
check_file_permissions() {
    log_info "檢查文件權限... | Checking file permissions..."

    local issues=0

    # 檢查敏感文件權限 | Check sensitive file permissions
    if [ -f "TOOLS.md" ]; then
        local perms=$(stat -f "%Lp" TOOLS.md 2>/dev/null || stat -c "%a" TOOLS.md 2>/dev/null)
        if [ "$perms" -gt 644 ]; then
            log_warning "TOOLS.md 權限過高: $perms | TOOLS.md permissions too high: $perms"
            ((issues++))
        else
            log_success "TOOLS.md 權限正常 | TOOLS.md permissions OK"
        fi
    fi

    if [ $issues -eq 0 ]; then
        log_success "文件權限檢查通過 | File permissions check passed"
        return 0
    else
        log_error "發現 $issues 個權限問題 | Found $issues permission issues"
        return 1
    fi
}

# 檢查 2: 敏感關鍵詞 | Check 2: Sensitive Keywords
check_sensitive_keywords() {
    log_info "檢查敏感關鍵詞... | Checking sensitive keywords..."

    local issues=0

    # 需要確認的關鍵詞 | Keywords requiring confirmation
    local keywords=(
        "password"
        "api_key"
        "secret"
        "token"
        "credential"
    )

    for keyword in "${keywords[@]}"; do
        if grep -rq "$keyword" . --include="*.md" 2>/dev/null; then
            # 排除註釋和示例 | Exclude comments and examples
            local found=$(grep -r "$keyword" . --include="*.md" 2>/dev/null | grep -v "^#\|example\|Example\|EXAMPLE" | wc -l)
            if [ $found -gt 0 ]; then
                log_warning "發現敏感關鍵詞 '$keyword' ($found 次) | Found sensitive keyword '$keyword' ($found times)"
                ((issues++))
            fi
        fi
    done

    if [ $issues -eq 0 ]; then
        log_success "敏感關鍵詞檢查通過 | Sensitive keywords check passed"
        return 0
    else
        log_error "發現 $issues 個敏感關鍵詞問題 | Found $issues sensitive keyword issues"
        return 1
    fi
}

# 檢查 3: 指令矛盾 | Check 3: Directive Contradictions
check_directive_contradictions() {
    log_info "檢查指令矛盾... | Checking directive contradictions..."

    local issues=0

    # 檢查常見矛盾模式 | Check common contradiction patterns
    local patterns=(
        "不要問許可.*直接"
        "無需確認.*執行"
        "no.*confirm.*execute"
    )

    for pattern in "${patterns[@]}"; do
        if grep -riE "$pattern" . --include="*.md" 2>/dev/null | grep -v "^#"; then
            log_warning "發現潛在指令矛盾: $pattern | Found potential directive contradiction: $pattern"
            ((issues++))
        fi
    done

    if [ $issues -eq 0 ]; then
        log_success "指令矛盾檢查通過 | Directive contradiction check passed"
        return 0
    else
        log_warning "發現 $issues 個潛在矛盾 | Found $issues potential contradictions"
        return 0  # 這是警告，不是錯誤
    fi
}

# 檢查 4: 安全協議存在性 | Check 4: Security Protocol Presence
check_security_protocols() {
    log_info "檢查安全協議... | Checking security protocols..."

    local required_files=(
        "AGENTS.md"
        "SOUL.md"
        "TOOLS.md"
        "WAL.md"
    )

    local missing=0

    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            log_error "缺少必需文件: $file | Missing required file: $file"
            ((missing++))
        else
            log_success "找到: $file | Found: $file"
        fi
    done

    if [ $missing -eq 0 ]; then
        log_success "安全協議檢查通過 | Security protocol check passed"
        return 0
    else
        log_error "缺少 $missing 個必需文件 | Missing $missing required files"
        return 1
    fi
}

# 檢查 5: 網絡安全 | Check 5: Network Security
check_network_security() {
    log_info "檢查網絡安全... | Checking network security..."

    # 檢查是否有多餘的網絡請求配置 | Check for unnecessary network request configs
    local issues=0

    if grep -rq "curl.*http\|wget.*http\|fetch.*url" . --include="*.md" 2>/dev/null | grep -v "^#\|#\|example"; then
        log_warning "發現潛在網絡請求 | Found potential network requests"
        ((issues++))
    fi

    if [ $issues -eq 0 ]; then
        log_success "網絡安全檢查通過 | Network security check passed"
        return 0
    else
        log_warning "發現 $issues 個潛在網絡問題 | Found $issues potential network issues"
        return 0  # 這是警告
    fi
}

# 檢查 6: 記憶文件結構 | Check 6: Memory File Structure
check_memory_structure() {
    log_info "檢查記憶文件結構... | Checking memory file structure..."

    local required_dirs=(
        "memory/daily"
        "memory/lessons"
    )

    for dir in "${required_dirs[@]}"; do
        if [ -d "$dir" ]; then
            log_success "找到目錄: $dir | Found directory: $dir"
        else
            log_warning "缺少目錄: $dir (將自動創建) | Missing directory: $dir (will be auto-created)"
            mkdir -p "$dir"
        fi
    done

    log_success "記憶結構檢查完成 | Memory structure check completed"
    return 0
}

# ============================================================================
# 主程序 | Main Program
# ============================================================================

main() {
    local verbose=false
    local skip_network=false
    local quick_mode=false

    # 解析參數 | Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            -s|--skip-network)
                skip_network=true
                shift
                ;;
            -q|--quick)
                quick_mode=true
                shift
                ;;
            *)
                log_error "未知參數: $1 | Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done

    echo "========================================"
    echo "  Nexus Agent Framework 安全審計"
    echo "  Nexus Agent Framework Security Audit"
    echo "========================================"
    echo ""

    local total_checks=0
    local passed_checks=0
    local failed_checks=0

    # 執行檢查 | Execute checks
    log_info "開始安全審計... | Starting security audit..."
    echo ""

    # 總是執行的檢查 | Checks to always run
    check_security_protocols && ((passed_checks++)) || ((failed_checks++))
    ((total_checks++))

    if [ "$quick_mode" = false ]; then
        check_file_permissions && ((passed_checks++)) || ((failed_checks++))
        ((total_checks++))

        check_sensitive_keywords && ((passed_checks++)) || ((failed_checks++))
        ((total_checks++))

        check_directive_contradictions && ((passed_checks++)) || ((failed_checks++))
        ((total_checks++))
    fi

    if [ "$skip_network" = false ] && [ "$quick_mode" = false ]; then
        check_network_security && ((passed_checks++)) || ((failed_checks++))
        ((total_checks++))
    fi

    check_memory_structure && ((passed_checks++)) || ((failed_checks++))
    ((total_checks++))

    # 總結 | Summary
    echo ""
    echo "========================================"
    echo "  審計總結 | Audit Summary"
    echo "========================================"
    echo "總檢查數: $total_checks"
    echo "通過: ${GREEN}$passed_checks${NC}"
    echo "失敗: ${RED}$failed_checks${NC}"
    echo ""

    if [ $failed_checks -eq 0 ]; then
        log_success "所有檢查通過！框架可以安全使用。"
        log_success "All checks passed! Framework is safe to use."
        exit 0
    else
        log_error "部分檢查失敗，請修復後再使用。"
        log_error "Some checks failed, please fix before using."
        exit 1
    fi
}

# 運行主程序 | Run main program
main "$@"
