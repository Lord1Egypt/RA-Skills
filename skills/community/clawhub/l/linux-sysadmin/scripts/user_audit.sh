#!/usr/bin/env bash
# user_audit.sh — 用户权限审计脚本
# 检查：sudo 权限、SSH 密钥、空密码、过期账户、可登录用户
# 用法: bash scripts/user_audit.sh

# 参数解析
case "${1:-}" in
    --help|-h)
        echo "用法: bash $0"
        echo ""
        echo "用户权限审计：检查 sudo 权限、SSH 密钥、空密码、过期账户、可登录用户。"
        echo ""
        echo "选项:"
        echo "  --help, -h      显示此帮助信息"
        echo "  --version       显示版本信息"
        exit 0
        ;;
    --version)
        echo "user_audit.sh v3.0.2"
        exit 0
        ;;
esac

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          用户权限审计报告                                   ║"
echo "║          审计时间: $(date '+%Y-%m-%d %H:%M:%S')                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# ==================== 1. 可登录用户 ====================
echo "=== 1. 可登录用户 ==="
echo ""
printf "  %-15s %-8s %-8s %-25s %s\n" "用户名" "UID" "GID" "HOME" "Shell"
printf "  %-15s %-8s %-8s %-25s %s\n" "------" "---" "---" "----" "-----"
while IFS=: read -r user _ uid gid _ home shell; do
    case "$shell" in
        */nologin|*/false|"") continue ;;
    esac
    printf "  %-15s %-8s %-8s %-25s %s\n" "$user" "$uid" "$gid" "$home" "$shell"
done < /etc/passwd
echo ""

# ==================== 2. UID 0 账户 ====================
echo "=== 2. UID 0 账户（应仅有 root） ==="
echo ""
uid0_users=$(awk -F: '$3 == 0 {print $1}' /etc/passwd)
for u in $uid0_users; do
    if [ "$u" = "root" ]; then
        echo "  ✅ $u (UID=0) — 正常"
    else
        echo "  ❌ $u (UID=0) — 异常！非 root 账户拥有 UID 0"
    fi
done
echo ""

# ==================== 3. 密码状态 ====================
echo "=== 3. 密码状态 ==="
echo ""
if [ -r /etc/shadow ]; then
    printf "  %-15s %-12s %-15s %-15s %s\n" "用户名" "状态" "最后修改" "过期日期" "备注"
    printf "  %-15s %-12s %-15s %-15s %s\n" "------" "----" "--------" "--------" "----"
    while IFS=: read -r user pw last_change min max warn inactive expire _; do
        # 跳过系统用户
        uid=$(id -u "$user" 2>/dev/null)
        [ -z "$uid" ] && continue
        [ "$uid" -lt 1000 ] && [ "$user" != "root" ] && continue

        # 密码状态
        case "$pw" in
            "!"|"!!"|"!*") status="锁定" ;;
            "*") status="禁用" ;;
            "") status="⚠️ 空密码" ;;
            *) status="已设置" ;;
        esac

        # 最后修改日期
        if [ -n "$last_change" ] && [ "$last_change" != "0" ]; then
            last_date=$(date -d "1970-01-01 + $last_change days" '+%Y-%m-%d' 2>/dev/null || echo "N/A")
        else
            last_date="从未/需修改"
        fi

        # 过期日期
        if [ -n "$expire" ] && [ "$expire" != "" ] && [ "$expire" != "-1" ]; then
            exp_date=$(date -d "1970-01-01 + $expire days" '+%Y-%m-%d' 2>/dev/null || echo "N/A")
        else
            exp_date="永不过期"
        fi

        # 备注
        note=""
        [ "$status" = "⚠️ 空密码" ] && note="需立即设置密码"
        [ "$last_date" = "从未/需修改" ] && note="首次登录需改密"

        printf "  %-15s %-12s %-15s %-15s %s\n" "$user" "$status" "$last_date" "$exp_date" "$note"
    done < /etc/shadow
else
    echo "  ⚠️ 无法读取 /etc/shadow（需要 root 权限）"
    echo "  使用 passwd -S 逐用户检查："
    for user in $(awk -F: '$3 >= 1000 || $1 == "root" {print $1}' /etc/passwd); do
        echo "  $(passwd -S "$user" 2>/dev/null)"
    done
fi
echo ""

# ==================== 4. sudo 权限 ====================
echo "=== 4. sudo 权限配置 ==="
echo ""

echo "  --- /etc/sudoers ---"
grep -v "^#" /etc/sudoers 2>/dev/null | grep -v "^$" | grep -v "^Defaults" | while read -r line; do
    echo "  $line"
done

echo ""
echo "  --- /etc/sudoers.d/ ---"
for f in /etc/sudoers.d/*; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    echo "  [$fname]:"
    grep -v "^#" "$f" | grep -v "^$" | while read -r line; do
        echo "    $line"
    done
done 2>/dev/null

echo ""
echo "  --- NOPASSWD 规则 ---"
nopasswd=$(grep -r "NOPASSWD" /etc/sudoers /etc/sudoers.d/ 2>/dev/null | grep -v "^#")
if [ -n "$nopasswd" ]; then
    echo "$nopasswd" | while read -r line; do
        echo "  ⚠️ $line"
    done
else
    echo "  ✅ 无 NOPASSWD 规则"
fi
echo ""

# ==================== 5. SSH 密钥 ====================
echo "=== 5. SSH 密钥审计 ==="
echo ""

for home_dir in /root /home/*; do
    [ -d "$home_dir" ] || continue
    user=$(basename "$home_dir")
    [ "$home_dir" = "/root" ] && user="root"

    auth_keys="$home_dir/.ssh/authorized_keys"
    if [ -f "$auth_keys" ]; then
        key_count=$(grep -c "^ssh-" "$auth_keys" 2>/dev/null || echo 0)
        perm=$(stat -c %a "$auth_keys" 2>/dev/null)
        dir_perm=$(stat -c %a "$home_dir/.ssh" 2>/dev/null)

        echo "  用户: $user"
        echo "    密钥数: $key_count"
        echo "    authorized_keys 权限: $perm $([ "$perm" = "600" ] && echo '✅' || echo '⚠️ 应为 600')"
        echo "    .ssh 目录权限: $dir_perm $([ "$dir_perm" = "700" ] && echo '✅' || echo '⚠️ 应为 700')"

        # 显示密钥指纹
        while IFS= read -r key; do
            [[ "$key" =~ ^ssh- ]] || continue
            fingerprint=$(echo "$key" | ssh-keygen -l -f - 2>/dev/null | awk '{print $2}')
            comment=$(echo "$key" | awk '{print $NF}')
            echo "    🔑 $fingerprint ($comment)"
        done < "$auth_keys"
        echo ""
    fi
done

# ==================== 6. 组成员 ====================
echo "=== 6. 特权组成员 ==="
echo ""

for group in root sudo wheel docker adm; do
    members=$(getent group "$group" 2>/dev/null | cut -d: -f4)
    if [ -n "$members" ]; then
        echo "  $group 组: $members"
    fi
done
echo ""

# ==================== 7. 最近登录 ====================
echo "=== 7. 最近登录记录 ==="
echo ""
echo "  --- 最近 10 次成功登录 ---"
last -10 2>/dev/null | head -10
echo ""
echo "  --- 最近 10 次失败登录 ---"
lastb 2>/dev/null | head -10 || echo "  无法读取（需要 root 权限）"
echo ""

# ==================== 汇总 ====================
echo "================================================================"
echo "  审计完成"
echo "================================================================"
login_users=$(grep -v -E "nologin|/bin/false" /etc/passwd | awk -F: '$3 >= 1000 || $1 == "root"' | wc -l)
sudo_rules=$(grep -r -v "^#" /etc/sudoers /etc/sudoers.d/ 2>/dev/null | grep -v "^$" | grep -v "Defaults" | wc -l)
nopasswd_rules=$(grep -r "NOPASSWD" /etc/sudoers /etc/sudoers.d/ 2>/dev/null | grep -v "^#" | wc -l)

echo "  可登录用户: $login_users"
echo "  sudo 规则数: $sudo_rules"
echo "  NOPASSWD 规则: $nopasswd_rules"
echo ""
echo "报告生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
