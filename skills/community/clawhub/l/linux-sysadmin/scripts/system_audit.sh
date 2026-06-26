#!/usr/bin/env bash
# system_audit.sh — 系统管理状态全面审计
# 覆盖：系统信息、用户、存储、网络、服务、安全 6 大维度
# 用法: bash scripts/system_audit.sh [--output FILE]

# 不使用 set -e，因为部分命令在特定环境下可能失败（如容器中无 lvm）
# 所有诊断输出到 stdout，进度信息输出到 stderr

OUTPUT=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --output=*)
            OUTPUT="${1#*=}"
            shift
            ;;
        --help|-h)
            echo "用法: bash $0 [--output FILE]"
            echo ""
            echo "选项:"
            echo "  --output FILE   将审计报告保存到指定文件"
            echo "  --help, -h      显示此帮助信息"
            echo "  --version       显示版本信息"
            exit 0
            ;;
        --version)
            echo "system_audit.sh v3.0.2"
            exit 0
            ;;
        *)
            echo "未知参数: $1" >&2
            echo "使用 --help 查看帮助" >&2
            shift
            ;;
    esac
done

# 如果指定了输出文件，重定向 stdout
if [ -n "$OUTPUT" ]; then
    exec > "$OUTPUT"
    echo "输出将保存到: $OUTPUT" >&2
fi

divider() {
    echo ""
    echo "================================================================"
    echo "  $1"
    echo "================================================================"
}

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          Linux 系统管理状态审计报告                         ║"
echo "║          生成时间: $(date '+%Y-%m-%d %H:%M:%S')                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# ==================== 1. 系统信息 ====================
divider "1. 系统基本信息"

echo "--- 操作系统 ---"
cat /etc/os-release 2>/dev/null | head -5 || echo "无法读取 /etc/os-release"

echo ""
echo "--- 内核版本 ---"
uname -r

echo ""
echo "--- 主机名 ---"
hostname

echo ""
echo "--- 运行时间 ---"
uptime

echo ""
echo "--- 时区 ---"
timedatectl 2>/dev/null | grep -E "Time zone|Local time" || date

# ==================== 2. 用户信息 ====================
divider "2. 用户与权限"

echo "--- 当前登录用户 ---"
who 2>/dev/null || echo "无法获取"

echo ""
echo "--- 可登录用户 ---"
grep -v -E "nologin|/bin/false|/usr/sbin/nologin" /etc/passwd 2>/dev/null | awk -F: '{printf "  %-15s UID=%-6s HOME=%s\n", $1, $3, $6}'

echo ""
echo "--- sudo 用户/组 ---"
grep -v "^#" /etc/sudoers 2>/dev/null | grep -v "^$" | head -20
for f in /etc/sudoers.d/*; do
    [ -f "$f" ] && echo "  [$(basename $f)]:" && grep -v "^#" "$f" | grep -v "^$"
done 2>/dev/null

echo ""
echo "--- 空密码账户 ---"
awk -F: '($2 == "" || $2 == "!") && $1 != "root" {print "  ⚠️  " $1}' /etc/shadow 2>/dev/null || echo "  无法读取 /etc/shadow（需要 root）"

echo ""
echo "--- 最近登录失败 ---"
lastb 2>/dev/null | head -10 || echo "  无法读取（需要 root）"

# ==================== 3. 存储信息 ====================
divider "3. 存储与文件系统"

echo "--- 磁盘使用 ---"
df -hT 2>/dev/null | grep -v tmpfs | grep -v devtmpfs

echo ""
echo "--- 块设备 ---"
lsblk -f 2>/dev/null || lsblk 2>/dev/null

echo ""
echo "--- LVM 状态 ---"
if command -v pvs &>/dev/null; then
    echo "  PV:" && pvs 2>/dev/null
    echo "  VG:" && vgs 2>/dev/null
    echo "  LV:" && lvs 2>/dev/null
else
    echo "  LVM 工具未安装"
fi

echo ""
echo "--- RAID 状态 ---"
if [ -f /proc/mdstat ]; then
    cat /proc/mdstat
else
    echo "  无软件 RAID"
fi

echo ""
echo "--- Swap 状态 ---"
swapon --show 2>/dev/null || echo "  无 Swap"
echo "  swappiness: $(cat /proc/sys/vm/swappiness 2>/dev/null)"

echo ""
echo "--- 磁盘使用率告警（>80%） ---"
df -h 2>/dev/null | awk 'NR>1 && +$5 > 80 {printf "  ⚠️  %s 使用率 %s（挂载点: %s）\n", $1, $5, $6}'

# ==================== 4. 网络信息 ====================
divider "4. 网络配置"

echo "--- 网络接口 ---"
ip -br addr 2>/dev/null || ifconfig -a 2>/dev/null

echo ""
echo "--- 路由表 ---"
ip route 2>/dev/null | head -20

echo ""
echo "--- DNS 配置 ---"
cat /etc/resolv.conf 2>/dev/null | grep -v "^#"

echo ""
echo "--- 监听端口 ---"
ss -tlnp 2>/dev/null | head -30

echo ""
echo "--- 网络连接统计 ---"
ss -s 2>/dev/null

# ==================== 5. 服务信息 ====================
divider "5. 服务管理"

echo "--- 运行中的服务 ---"
systemctl list-units --type=service --state=running --no-pager 2>/dev/null | head -30

echo ""
echo "--- 失败的服务 ---"
failed=$(systemctl list-units --type=service --state=failed --no-pager 2>/dev/null | grep -c "failed")
if [ "$failed" -gt 0 ]; then
    systemctl list-units --type=service --state=failed --no-pager 2>/dev/null
else
    echo "  无失败服务 ✅"
fi

echo ""
echo "--- 定时任务 ---"
echo "  systemd timers:"
systemctl list-timers --no-pager 2>/dev/null | head -15
echo ""
echo "  crontab (root):"
crontab -l 2>/dev/null || echo "  无 root crontab"

# ==================== 6. 安全信息 ====================
divider "6. 安全状态"

echo "--- SSH 配置 ---"
if [ -f /etc/ssh/sshd_config ]; then
    echo "  PermitRootLogin: $(grep -i "^PermitRootLogin" /etc/ssh/sshd_config 2>/dev/null || echo '默认(prohibit-password)')"
    echo "  PasswordAuth: $(grep -i "^PasswordAuthentication" /etc/ssh/sshd_config 2>/dev/null || echo '默认(yes)')"
    echo "  PubkeyAuth: $(grep -i "^PubkeyAuthentication" /etc/ssh/sshd_config 2>/dev/null || echo '默认(yes)')"
    echo "  Port: $(grep -i "^Port" /etc/ssh/sshd_config 2>/dev/null || echo '默认(22)')"
fi

echo ""
echo "--- 防火墙状态 ---"
if command -v firewall-cmd &>/dev/null; then
    echo "  firewalld: $(firewall-cmd --state 2>/dev/null)"
    firewall-cmd --list-all 2>/dev/null | head -15
elif command -v ufw &>/dev/null; then
    echo "  UFW:"
    ufw status 2>/dev/null
else
    echo "  iptables 规则数: $(iptables -L -n 2>/dev/null | wc -l)"
fi

echo ""
echo "--- SELinux/AppArmor ---"
if command -v getenforce &>/dev/null; then
    echo "  SELinux: $(getenforce 2>/dev/null)"
elif command -v aa-status &>/dev/null; then
    echo "  AppArmor: $(aa-status 2>/dev/null | head -3)"
else
    echo "  无强制访问控制系统"
fi

echo ""
echo "--- SUID 文件（非标准） ---"
find /usr/local /opt /home -perm /4000 -type f 2>/dev/null | head -10
echo "  （仅检查 /usr/local /opt /home）"

echo ""
echo "--- 最近 OOM 事件 ---"
dmesg 2>/dev/null | grep -i "oom\|killed process" | tail -5 || echo "  无法读取 dmesg"

echo ""
divider "审计完成"
echo "报告生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
if [ -n "$OUTPUT" ]; then
    echo "报告已保存到: $OUTPUT" >&2
fi
