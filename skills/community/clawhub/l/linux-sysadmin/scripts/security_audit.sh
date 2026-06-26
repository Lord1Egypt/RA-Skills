#!/usr/bin/env bash
# security_audit.sh — 安全基线检查脚本
# 基于 CIS Benchmark 关键项，检查系统安全配置
# 用法: bash scripts/security_audit.sh

# 不使用 set -e，因为部分检查在特定环境下可能失败

# 参数解析
case "${1:-}" in
    --help|-h)
        echo "用法: bash $0"
        echo ""
        echo "基于 CIS Benchmark 关键项检查系统安全配置。"
        echo ""
        echo "选项:"
        echo "  --help, -h      显示此帮助信息"
        echo "  --version       显示版本信息"
        exit 0
        ;;
    --version)
        echo "security_audit.sh v3.0.2"
        exit 0
        ;;
esac

PASS=0
WARN=0
FAIL=0

check() {
    local status="$1"
    local desc="$2"
    local detail="$3"

    case "$status" in
        PASS)
            echo "  ✅ PASS: $desc"
            PASS=$((PASS + 1))
            ;;
        WARN)
            echo "  ⚠️  WARN: $desc"
            [ -n "$detail" ] && echo "         → $detail"
            WARN=$((WARN + 1))
            ;;
        FAIL)
            echo "  ❌ FAIL: $desc"
            [ -n "$detail" ] && echo "         → $detail"
            FAIL=$((FAIL + 1))
            ;;
    esac
}

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          安全基线检查报告                                   ║"
echo "║          检查时间: $(date '+%Y-%m-%d %H:%M:%S')                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# ==================== 1. SSH 安全 ====================
echo "=== 1. SSH 安全 ==="

if [ -f /etc/ssh/sshd_config ]; then
    # 检查 root 登录
    root_login=$(grep -i "^PermitRootLogin" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null | grep -v "^#" | tail -1 | awk '{print $2}')
    if [ "$root_login" = "no" ]; then
        check PASS "SSH 禁止 root 登录"
    elif [ "$root_login" = "prohibit-password" ]; then
        check WARN "SSH root 登录限制为密钥认证" "建议设置为 no"
    else
        check FAIL "SSH 允许 root 登录" "设置 PermitRootLogin no"
    fi

    # 检查密码认证
    pw_auth=$(grep -i "^PasswordAuthentication" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null | grep -v "^#" | tail -1 | awk '{print $2}')
    if [ "$pw_auth" = "no" ]; then
        check PASS "SSH 禁止密码认证（仅密钥）"
    else
        check WARN "SSH 允许密码认证" "建议设置 PasswordAuthentication no"
    fi

    # 检查 MaxAuthTries
    max_auth=$(grep -i "^MaxAuthTries" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null | grep -v "^#" | tail -1 | awk '{print $2}')
    if [ -n "$max_auth" ] && [[ "$max_auth" =~ ^[0-9]+$ ]] && [ "$max_auth" -le 3 ]; then
        check PASS "SSH MaxAuthTries <= 3（当前: $max_auth）"
    else
        check WARN "SSH MaxAuthTries 未限制或过大" "建议设置 MaxAuthTries 3"
    fi

    # 检查 SSH 端口
    ssh_port=$(grep -i "^Port" /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}')
    if [ -n "$ssh_port" ] && [ "$ssh_port" != "22" ]; then
        check PASS "SSH 使用非标准端口（$ssh_port）"
    else
        check WARN "SSH 使用默认端口 22" "可考虑更换为非标准端口"
    fi
else
    check WARN "未找到 sshd_config"
fi

echo ""

# ==================== 2. 用户安全 ====================
echo "=== 2. 用户安全 ==="

# 检查空密码账户
empty_pw=$(awk -F: '($2 == "" || $2 == "!!") && $3 >= 1000' /etc/shadow 2>/dev/null | wc -l)
if [ "$empty_pw" -eq 0 ]; then
    check PASS "无空密码的普通用户账户"
else
    check FAIL "发现 $empty_pw 个空密码账户" "使用 passwd 设置密码"
fi

# 检查 UID 0 账户
uid0=$(awk -F: '$3 == 0 && $1 != "root"' /etc/passwd | wc -l)
if [ "$uid0" -eq 0 ]; then
    check PASS "仅 root 拥有 UID 0"
else
    check FAIL "发现非 root 的 UID 0 账户" "$(awk -F: '$3 == 0 && $1 != "root" {print $1}' /etc/passwd)"
fi

# 检查 sudo 配置
if [ -f /etc/sudoers ]; then
    nopasswd_count=$(grep -r "NOPASSWD" /etc/sudoers /etc/sudoers.d/ 2>/dev/null | grep -v "^#" | wc -l)
    if [ "$nopasswd_count" -eq 0 ]; then
        check PASS "无 NOPASSWD sudo 配置"
    else
        check WARN "发现 $nopasswd_count 条 NOPASSWD sudo 规则" "审查是否必要"
    fi
fi

# 检查密码过期策略
max_days=$(grep "^PASS_MAX_DAYS" /etc/login.defs 2>/dev/null | awk '{print $2}')
if [ -n "$max_days" ] && [[ "$max_days" =~ ^[0-9]+$ ]] && [ "$max_days" -le 90 ]; then
    check PASS "密码最长有效期 <= 90 天（当前: $max_days）"
else
    check WARN "密码最长有效期过长或未设置" "建议 PASS_MAX_DAYS 90"
fi

echo ""

# ==================== 3. 文件权限 ====================
echo "=== 3. 文件权限 ==="

# 检查关键文件权限
check_perm() {
    local file="$1"
    local expected="$2"
    local desc="$3"
    if [ -f "$file" ]; then
        actual=$(stat -c %a "$file" 2>/dev/null)
        if [ -n "$actual" ] && [[ "$actual" =~ ^[0-9]+$ ]] && { [ "$actual" = "$expected" ] || [ "$actual" -le "$expected" ]; }; then
            check PASS "$desc（$actual）"
        else
            check FAIL "$desc（当前: $actual，应为: $expected）"
        fi
    fi
}

check_perm /etc/passwd "644" "/etc/passwd 权限"
check_perm /etc/shadow "000" "/etc/shadow 权限"
check_perm /etc/group "644" "/etc/group 权限"
check_perm /etc/ssh/sshd_config "600" "/etc/ssh/sshd_config 权限"

# 检查非标准 SUID 文件
suid_count=$(find /usr/local /opt /home -perm /4000 -type f 2>/dev/null | wc -l)
if [ "$suid_count" -eq 0 ]; then
    check PASS "无非标准路径的 SUID 文件"
else
    check WARN "发现 $suid_count 个非标准 SUID 文件" "检查 /usr/local /opt /home"
fi

# 检查 world-writable 目录（排除 /tmp 等）
ww_dirs=$(find / -maxdepth 3 -type d -perm -0002 ! -path "/tmp*" ! -path "/var/tmp*" ! -path "/dev*" ! -path "/proc*" ! -path "/sys*" ! -path "/run*" 2>/dev/null | wc -l)
if [ "$ww_dirs" -eq 0 ]; then
    check PASS "无异常的 world-writable 目录"
else
    check WARN "发现 $ww_dirs 个 world-writable 目录" "检查是否必要"
fi

echo ""

# ==================== 4. 网络安全 ====================
echo "=== 4. 网络安全 ==="

# 检查防火墙
if command -v firewall-cmd &>/dev/null && firewall-cmd --state &>/dev/null 2>&1; then
    check PASS "firewalld 已启用"
elif command -v ufw &>/dev/null && ufw status 2>/dev/null | grep -q "active"; then
    check PASS "UFW 已启用"
elif iptables -L -n 2>/dev/null | grep -qv "^Chain.*policy ACCEPT"; then
    check PASS "iptables 有活跃规则"
else
    check FAIL "防火墙未启用或无规则" "启用 firewalld/ufw 或配置 iptables"
fi

# 检查 IP 转发
ip_forward=$(cat /proc/sys/net/ipv4/ip_forward 2>/dev/null)
if [ "$ip_forward" = "0" ]; then
    check PASS "IP 转发已禁用"
else
    check WARN "IP 转发已启用" "如非路由器/网关，建议禁用"
fi

# 检查监听端口
high_risk_ports=$(ss -tlnp 2>/dev/null | grep -E ":23\b|:21\b|:513\b|:514\b" | wc -l)
if [ "$high_risk_ports" -eq 0 ]; then
    check PASS "无高风险端口监听（telnet/ftp/rlogin/rsh）"
else
    check FAIL "发现高风险端口监听" "关闭 telnet/ftp/rlogin/rsh 服务"
fi

echo ""

# ==================== 5. 系统安全 ====================
echo "=== 5. 系统安全 ==="

# 检查 SELinux/AppArmor
if command -v getenforce &>/dev/null; then
    selinux_status=$(getenforce 2>/dev/null)
    if [ "$selinux_status" = "Enforcing" ]; then
        check PASS "SELinux 处于 Enforcing 模式"
    elif [ "$selinux_status" = "Permissive" ]; then
        check WARN "SELinux 处于 Permissive 模式" "建议切换到 Enforcing"
    else
        check FAIL "SELinux 已禁用" "建议启用"
    fi
elif command -v aa-status &>/dev/null; then
    profiles=$(aa-status 2>/dev/null | grep "profiles are loaded" | awk '{print $1}')
    if [ -n "$profiles" ] && [[ "$profiles" =~ ^[0-9]+$ ]] && [ "$profiles" -gt 0 ]; then
        check PASS "AppArmor 已启用（$profiles 个配置文件）"
    else
        check WARN "AppArmor 无活跃配置文件"
    fi
else
    check WARN "无强制访问控制系统（SELinux/AppArmor）"
fi

# 检查自动更新
if command -v unattended-upgrades &>/dev/null || systemctl is-active dnf-automatic &>/dev/null 2>&1; then
    check PASS "自动安全更新已配置"
else
    check WARN "未配置自动安全更新" "建议启用 unattended-upgrades 或 dnf-automatic"
fi

# 检查 core dump
core_limit=$(ulimit -c 2>/dev/null)
if [ "$core_limit" = "0" ]; then
    check PASS "Core dump 已禁用"
else
    check WARN "Core dump 未禁用" "echo '* hard core 0' >> /etc/security/limits.conf"
fi

echo ""

# ==================== 汇总 ====================
echo "================================================================"
echo "  检查汇总"
echo "================================================================"
total=$((PASS + WARN + FAIL))
echo "  总计: $total 项检查"
echo "  ✅ 通过: $PASS"
echo "  ⚠️  警告: $WARN"
echo "  ❌ 失败: $FAIL"
echo ""

if [ "$FAIL" -eq 0 ] && [ "$WARN" -eq 0 ]; then
    echo "  🎉 安全基线检查全部通过！"
elif [ "$FAIL" -eq 0 ]; then
    echo "  👍 无严重问题，建议处理警告项"
else
    echo "  ⚠️  发现 $FAIL 个安全问题，请尽快修复"
fi

echo ""
echo "报告生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
