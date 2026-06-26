#!/usr/bin/env bash
# ansible_check.sh — Ansible 环境检查与 Playbook 验证脚本
# 支持：环境检查、Inventory 验证、Playbook 语法检查、连通性测试
# 用法:
#   bash scripts/ansible_check.sh env         — 检查 Ansible 环境
#   bash scripts/ansible_check.sh inventory   — 验证 Inventory
#   bash scripts/ansible_check.sh syntax      — Playbook 语法检查
#   bash scripts/ansible_check.sh ping        — 主机连通性测试
#   bash scripts/ansible_check.sh all         — 全部检查

# 参数解析（优先处理 --help/--version）
case "${1:-}" in
    --help|-h)
        echo "用法: bash $0 {env|inventory|syntax|ping|all} [path]"
        echo ""
        echo "Ansible 环境检查与 Playbook 验证。"
        echo ""
        echo "命令:"
        echo "  env        — 检查 Ansible 环境（安装/Python/SSH/配置）"
        echo "  inventory  — 验证 Inventory 文件"
        echo "  syntax     — Playbook 语法检查"
        echo "  ping       — 主机连通性测试"
        echo "  all        — 执行所有检查"
        echo ""
        echo "选项:"
        echo "  --help, -h      显示此帮助信息"
        echo "  --version       显示版本信息"
        exit 0
        ;;
    --version)
        echo "ansible_check.sh v3.0.2"
        exit 0
        ;;
esac

ACTION="${1:-env}"

# 颜色输出（非终端环境自动禁用，避免转义码泄露）
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' CYAN='' NC=''
fi

pass()  { echo -e "  ${GREEN}✅ PASS${NC}: $1"; }
warn()  { echo -e "  ${YELLOW}⚠️  WARN${NC}: $1"; }
fail()  { echo -e "  ${RED}❌ FAIL${NC}: $1"; }
info()  { echo -e "  ℹ️  INFO: $1"; }

divider() {
    echo ""
    echo "================================================================"
    echo "  $1"
    echo "================================================================"
}

TOTAL=0
PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

check_pass()  { TOTAL=$((TOTAL+1)); PASS_COUNT=$((PASS_COUNT+1)); pass "$1"; }
check_warn()  { TOTAL=$((TOTAL+1)); WARN_COUNT=$((WARN_COUNT+1)); warn "$1"; }
check_fail()  { TOTAL=$((TOTAL+1)); FAIL_COUNT=$((FAIL_COUNT+1)); fail "$1"; }

# ==================== 环境检查 ====================
cmd_env() {
    divider "1. Ansible 安装"

    # 检查 ansible
    if command -v ansible &>/dev/null; then
        local ver
        ver=$(ansible --version 2>/dev/null | head -1)
        check_pass "Ansible 已安装: $ver"
    else
        check_fail "Ansible 未安装"
        info "安装方式: pip3 install ansible 或 apt install ansible"
        return
    fi

    # 检查 ansible-playbook
    if command -v ansible-playbook &>/dev/null; then
        check_pass "ansible-playbook 可用"
    else
        check_fail "ansible-playbook 不可用"
    fi

    # 检查 ansible-lint
    if command -v ansible-lint &>/dev/null; then
        local lint_ver
        lint_ver=$(ansible-lint --version 2>/dev/null | head -1)
        check_pass "ansible-lint 已安装: $lint_ver"
    else
        check_warn "ansible-lint 未安装（建议: pip3 install ansible-lint）"
    fi

    # 检查 ansible-galaxy
    if command -v ansible-galaxy &>/dev/null; then
        check_pass "ansible-galaxy 可用"
    else
        check_warn "ansible-galaxy 不可用"
    fi

    divider "2. Python 环境"

    # Python 版本
    if command -v python3 &>/dev/null; then
        local pyver
        pyver=$(python3 --version 2>/dev/null)
        check_pass "Python3: $pyver"
    else
        check_fail "Python3 未安装"
    fi

    # pip
    if command -v pip3 &>/dev/null; then
        check_pass "pip3 可用"
    else
        check_warn "pip3 不可用"
    fi

    # 检查关键 Python 模块
    for mod in jinja2 yaml paramiko; do
        if python3 -c "import $mod" 2>/dev/null; then
            check_pass "Python 模块 $mod 可用"
        else
            check_warn "Python 模块 $mod 缺失"
        fi
    done

    divider "3. SSH 配置"

    # SSH 客户端
    if command -v ssh &>/dev/null; then
        check_pass "SSH 客户端可用"
    else
        check_fail "SSH 客户端不可用"
    fi

    # SSH 密钥
    local key_found=0
    for key_file in ~/.ssh/id_ed25519 ~/.ssh/id_rsa ~/.ssh/id_ecdsa; do
        if [ -f "$key_file" ]; then
            local perms
            perms=$(stat -c '%a' "$key_file" 2>/dev/null)
            if [ "$perms" = "600" ] || [ "$perms" = "400" ]; then
                check_pass "SSH 密钥: $key_file（权限 $perms）"
            else
                check_warn "SSH 密钥 $key_file 权限不安全: $perms（应为 600）"
            fi
            key_found=1
        fi
    done
    [ "$key_found" -eq 0 ] && check_warn "未找到 SSH 密钥"

    # SSH Agent
    if ssh-add -l &>/dev/null; then
        local key_count
        key_count=$(ssh-add -l 2>/dev/null | wc -l)
        check_pass "SSH Agent 运行中（$key_count 个密钥）"
    else
        check_warn "SSH Agent 未运行或无密钥加载"
    fi

    divider "4. Ansible 配置"

    # ansible.cfg
    local cfg
    cfg=$(ansible --version 2>/dev/null | grep "config file" | awk -F= '{print $2}' | xargs)
    if [ -n "$cfg" ] && [ "$cfg" != "None" ]; then
        check_pass "配置文件: $cfg"
    else
        check_warn "未找到 ansible.cfg（使用默认配置）"
    fi

    # 默认 Inventory
    local inv
    inv=$(ansible-config dump 2>/dev/null | grep "DEFAULT_HOST_LIST" | awk -F= '{print $2}' | xargs)
    if [ -n "$inv" ]; then
        info "默认 Inventory: $inv"
    fi

    # forks
    local forks
    forks=$(ansible-config dump 2>/dev/null | grep "DEFAULT_FORKS" | awk -F= '{print $2}' | xargs)
    info "并行度 (forks): ${forks:-5}"

    # pipelining
    local pipe
    pipe=$(ansible-config dump 2>/dev/null | grep "ANSIBLE_PIPELINING" | awk -F= '{print $2}' | xargs)
    if [ "$pipe" = "True" ]; then
        check_pass "SSH Pipelining 已启用"
    else
        check_warn "SSH Pipelining 未启用（建议启用以提高性能）"
    fi

    divider "5. Galaxy Collections"
    if command -v ansible-galaxy &>/dev/null; then
        local col_count
        col_count=$(ansible-galaxy collection list 2>/dev/null | grep -c "^\w" || echo "0")
        info "已安装 Collections: $col_count 个"

        # 检查常用 collection
        for col in community.general ansible.posix community.docker community.crypto; do
            if ansible-galaxy collection list 2>/dev/null | grep -q "$col"; then
                check_pass "Collection: $col 已安装"
            else
                info "Collection: $col 未安装"
            fi
        done
    fi

    divider "6. 辅助工具"
    for tool in sshpass jq yq git rsync; do
        if command -v "$tool" &>/dev/null; then
            check_pass "$tool 可用"
        else
            info "$tool 未安装"
        fi
    done

    # Molecule
    if command -v molecule &>/dev/null; then
        check_pass "Molecule 可用（$(molecule --version 2>/dev/null | head -1)）"
    else
        info "Molecule 未安装（用于 Role 测试）"
    fi
}

# ==================== Inventory 验证 ====================
cmd_inventory() {
    divider "Inventory 验证"

    local inv_path="${2:-inventory}"
    if [ ! -e "$inv_path" ]; then
        # 尝试常见路径
        for try_path in inventory hosts hosts.ini hosts.yaml /etc/ansible/hosts; do
            if [ -e "$try_path" ]; then
                inv_path="$try_path"
                break
            fi
        done
    fi

    info "Inventory 路径: $inv_path"

    if [ ! -e "$inv_path" ]; then
        check_fail "Inventory 文件/目录不存在: $inv_path"
        return
    fi

    # 列出主机
    local host_count
    host_count=$(ansible -i "$inv_path" all --list-hosts 2>/dev/null | grep -c "^\s" || echo "0")
    if [ "$host_count" -gt 0 ]; then
        check_pass "Inventory 包含 $host_count 个主机"
    else
        check_warn "Inventory 中没有主机"
    fi

    # 列出组
    local groups
    groups=$(ansible -i "$inv_path" all --list-hosts 2>/dev/null | grep ":" | sed 's/://' | xargs)
    if [ -n "$groups" ]; then
        info "主机组: $groups"
    fi

    # 图形化展示
    echo ""
    echo -e "  ${CYAN}--- Inventory 结构 ---${NC}"
    ansible-inventory -i "$inv_path" --graph 2>/dev/null | head -30
}

# ==================== Playbook 语法检查 ====================
cmd_syntax() {
    divider "Playbook 语法检查"

    local playbook_dir="${2:-.}"
    local yaml_files

    # 查找 YAML 文件
    yaml_files=$(find "$playbook_dir" -maxdepth 3 -name "*.yaml" -o -name "*.yml" 2>/dev/null | \
                 grep -v "node_modules\|\.git\|venv\|__pycache__\|galaxy\|requirements" | sort)

    if [ -z "$yaml_files" ]; then
        check_warn "未找到 YAML 文件: $playbook_dir"
        return
    fi

    local checked=0
    local passed=0
    local failed=0

    while IFS= read -r f; do
        # 检查是否是 Playbook（包含 hosts: 或 tasks:）
        if grep -qE "^\s*-?\s*(hosts|tasks|roles):" "$f" 2>/dev/null; then
            checked=$((checked + 1))
            if ansible-playbook --syntax-check "$f" &>/dev/null; then
                check_pass "语法正确: $f"
                passed=$((passed + 1))
            else
                check_fail "语法错误: $f"
                ansible-playbook --syntax-check "$f" 2>&1 | head -5 | while IFS= read -r line; do
                    echo "    $line"
                done
                failed=$((failed + 1))
            fi
        fi
    done <<< "$yaml_files"

    echo ""
    info "检查了 $checked 个 Playbook: $passed 通过, $failed 失败"

    # ansible-lint（如果可用）
    if command -v ansible-lint &>/dev/null; then
        echo ""
        echo -e "  ${CYAN}--- ansible-lint 检查 ---${NC}"
        local lint_issues
        lint_issues=$(ansible-lint "$playbook_dir" 2>/dev/null | grep -c "WARNING\|ERROR" || echo "0")
        if [ "$lint_issues" -eq 0 ]; then
            check_pass "ansible-lint 无警告"
        else
            check_warn "ansible-lint 发现 $lint_issues 个问题"
            ansible-lint "$playbook_dir" 2>/dev/null | head -10
        fi
    fi
}

# ==================== 连通性测试 ====================
cmd_ping() {
    divider "主机连通性测试"

    local inv_path="${2:-inventory}"
    # 尝试找到 inventory
    if [ ! -e "$inv_path" ]; then
        for try_path in inventory hosts hosts.ini hosts.yaml /etc/ansible/hosts; do
            if [ -e "$try_path" ]; then
                inv_path="$try_path"
                break
            fi
        done
    fi

    if [ ! -e "$inv_path" ]; then
        check_fail "Inventory 不存在，无法测试连通性"
        return
    fi

    info "使用 Inventory: $inv_path"
    echo ""

    # 执行 ping
    local result
    result=$(ansible -i "$inv_path" all -m ping --one-line 2>&1)

    local success=0
    local failed=0
    local unreachable=0

    while IFS= read -r line; do
        if echo "$line" | grep -q "SUCCESS"; then
            host=$(echo "$line" | awk '{print $1}')
            check_pass "$host 连通"
            success=$((success + 1))
        elif echo "$line" | grep -q "UNREACHABLE"; then
            host=$(echo "$line" | awk '{print $1}')
            check_fail "$host 不可达"
            unreachable=$((unreachable + 1))
        elif echo "$line" | grep -q "FAILED"; then
            host=$(echo "$line" | awk '{print $1}')
            check_fail "$host 连接失败"
            failed=$((failed + 1))
        fi
    done <<< "$result"

    echo ""
    info "结果: $success 成功, $unreachable 不可达, $failed 失败"
}

# ==================== 汇总 ====================
print_summary() {
    echo ""
    echo "================================================================"
    echo "  检查汇总"
    echo "================================================================"
    echo "  总计: $TOTAL 项检查"
    echo -e "  ${GREEN}✅ 通过${NC}: $PASS_COUNT"
    echo -e "  ${YELLOW}⚠️  警告${NC}: $WARN_COUNT"
    echo -e "  ${RED}❌ 失败${NC}: $FAIL_COUNT"
    echo ""

    if [ "$FAIL_COUNT" -gt 0 ]; then
        echo -e "  ${RED}⚠️  发现 $FAIL_COUNT 个问题，请检查并修复${NC}"
    elif [ "$WARN_COUNT" -gt 0 ]; then
        echo -e "  ${YELLOW}👍 无严重问题，建议关注警告项${NC}"
    else
        echo -e "  ${GREEN}🎉 所有检查通过${NC}"
    fi
}

# ==================== 主入口 ====================
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          Ansible 环境检查报告                               ║"
echo "║          检查时间: $(date '+%Y-%m-%d %H:%M:%S')                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"

case "$ACTION" in
    env)       cmd_env; print_summary ;;
    inventory) cmd_inventory "$@"; print_summary ;;
    syntax)    cmd_syntax "$@"; print_summary ;;
    ping)      cmd_ping "$@"; print_summary ;;
    all)
        cmd_env
        cmd_inventory "$@"
        cmd_syntax "$@"
        cmd_ping "$@"
        print_summary
        ;;
    *)
        echo "用法: $0 {env|inventory|syntax|ping|all} [path]"
        echo ""
        echo "  env        — 检查 Ansible 环境（安装/Python/SSH/配置）"
        echo "  inventory  — 验证 Inventory 文件"
        echo "  syntax     — Playbook 语法检查"
        echo "  ping       — 主机连通性测试"
        echo "  all        — 执行所有检查"
        echo ""
        echo "示例:"
        echo "  $0 env"
        echo "  $0 inventory ./inventory/production"
        echo "  $0 syntax ./playbooks"
        echo "  $0 ping ./inventory/staging"
        exit 1
        ;;
esac
