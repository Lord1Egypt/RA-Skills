# 防火墙与安全加固

## 目录

- [1. iptables](#1-iptables)
- [2. nftables](#2-nftables)
- [3. firewalld](#3-firewalld)
- [4. UFW](#4-ufw)
- [5. NAT 与端口转发](#5-nat-与端口转发)
- [6. 系统安全加固](#6-系统安全加固)
- [7. 常见故障排查](#7-常见故障排查)

---

## 1. iptables

### 1.1 基本概念

```text
表（Table）→ 链（Chain）→ 规则（Rule）

表：filter（默认，过滤）、nat（地址转换）、mangle（修改包）、raw（跟踪）
链：INPUT（入站）、OUTPUT（出站）、FORWARD（转发）、PREROUTING、POSTROUTING
动作：ACCEPT（允许）、DROP（丢弃）、REJECT（拒绝并通知）、LOG（记录）
```

### 1.2 查看规则

```bash
# 查看所有规则
iptables -L -n -v                    # filter 表
iptables -L -n -v --line-numbers     # 带行号
iptables -t nat -L -n -v             # nat 表

# 查看规则（命令格式，可直接复制执行）
iptables-save
```

### 1.3 常用规则

```bash
# === 基本策略 ===
# 默认策略（先设置 ACCEPT 再添加规则，最后改 DROP）
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 允许回环接口
iptables -A INPUT -i lo -j ACCEPT

# 允许已建立的连接
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# === 端口管理 ===
# 允许 SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 允许 HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 允许特定 IP 访问
iptables -A INPUT -s 252.227.81.0/24 -p tcp --dport 3306 -j ACCEPT

# 封禁 IP
iptables -A INPUT -s 1.2.3.4 -j DROP

# 限速（防 DDoS）
iptables -A INPUT -p tcp --dport 80 -m limit --limit 100/min --limit-burst 200 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j DROP

# 允许 ICMP（ping）
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

# === 规则管理 ===
# 插入规则到指定位置
iptables -I INPUT 1 -s 10.0.0.100 -j ACCEPT

# 删除规则（按行号）
iptables -D INPUT 3

# 删除规则（按内容）
iptables -D INPUT -s 1.2.3.4 -j DROP

# 清空所有规则
iptables -F
iptables -X          # 删除自定义链
iptables -Z          # 清零计数器
```

### 1.4 保存与恢复

```bash
# 保存规则
iptables-save > /etc/iptables/rules.v4
ip6tables-save > /etc/iptables/rules.v6

# 恢复规则
iptables-restore < /etc/iptables/rules.v4

# 持久化（Ubuntu）
apt install iptables-persistent
netfilter-persistent save

# 持久化（RHEL）
service iptables save
# 或
iptables-save > /etc/sysconfig/iptables
```

---

## 2. nftables

### 2.1 基本操作

```bash
# nftables 是 iptables 的替代品（内核 3.13+）

# 查看规则
nft list ruleset

# 清空规则
nft flush ruleset
```

### 2.2 基本配置

```bash
# /etc/nftables.conf
nft -f - << 'EOF'
flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # 允许回环
        iif lo accept

        # 允许已建立连接
        ct state established,related accept

        # 允许 ICMP
        ip protocol icmp accept
        ip6 nexthdr icmpv6 accept

        # 允许 SSH
        tcp dport 22 accept

        # 允许 HTTP/HTTPS
        tcp dport { 80, 443 } accept

        # 允许特定网段访问数据库
        ip saddr 252.227.81.0/24 tcp dport 3306 accept

        # 日志并丢弃其他
        log prefix "nftables-drop: " drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}
EOF

# 加载配置
nft -f /etc/nftables.conf

# 启用服务
systemctl enable --now nftables
```

---

## 3. firewalld

### 3.1 基本操作

```bash
# 查看状态
firewall-cmd --state
firewall-cmd --list-all
firewall-cmd --list-all-zones

# 查看当前区域
firewall-cmd --get-default-zone
firewall-cmd --get-active-zones
```

### 3.2 端口管理

```bash
# 开放端口
firewall-cmd --add-port=80/tcp --permanent
firewall-cmd --add-port=8080-8090/tcp --permanent

# 关闭端口
firewall-cmd --remove-port=80/tcp --permanent

# 开放服务
firewall-cmd --add-service=http --permanent
firewall-cmd --add-service=https --permanent

# 重载（使 --permanent 生效）
firewall-cmd --reload

# 查看开放的端口和服务
firewall-cmd --list-ports
firewall-cmd --list-services
```

### 3.3 Zone 管理

```bash
# 常用 Zone
# drop     — 丢弃所有入站
# block    — 拒绝所有入站（返回 ICMP）
# public   — 默认，只允许选定服务
# external — 外部网络（启用 NAT）
# internal — 内部网络
# trusted  — 允许所有

# 设置默认区域
firewall-cmd --set-default-zone=public

# 将接口分配到区域
firewall-cmd --zone=internal --change-interface=eth1 --permanent

# 添加源地址到区域
firewall-cmd --zone=trusted --add-source=252.227.81.0/24 --permanent
```

### 3.4 Rich Rules

```bash
# 允许特定 IP 访问特定端口
firewall-cmd --add-rich-rule='rule family="ipv4" source address="10.0.0.100" port port="3306" protocol="tcp" accept' --permanent

# 封禁 IP
firewall-cmd --add-rich-rule='rule family="ipv4" source address="1.2.3.4" reject' --permanent

# 限速
firewall-cmd --add-rich-rule='rule family="ipv4" service name="http" limit value="100/m" accept' --permanent

# 端口转发
firewall-cmd --add-rich-rule='rule family="ipv4" forward-port port="8080" protocol="tcp" to-port="80"' --permanent

# 查看 rich rules
firewall-cmd --list-rich-rules

# 重载
firewall-cmd --reload
```

---

## 4. UFW

```bash
# UFW（Uncomplicated Firewall）— Ubuntu 默认防火墙前端

# 启用/禁用
ufw enable
ufw disable
ufw status verbose

# 默认策略
ufw default deny incoming
ufw default allow outgoing

# 允许端口
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# 允许服务
ufw allow ssh
ufw allow http

# 允许特定 IP
ufw allow from 252.227.81.0/24 to any port 3306

# 封禁 IP
ufw deny from 1.2.3.4

# 删除规则
ufw delete allow 80/tcp
# 或按编号删除
ufw status numbered
ufw delete 3

# 日志
ufw logging on
ufw logging medium   # low/medium/high/full
```

---

## 5. NAT 与端口转发

### 5.1 SNAT（源地址转换）

```bash
# 场景：内网机器通过网关访问外网

# 启用 IP 转发
echo 1 > /proc/sys/net/ipv4/ip_forward
# 持久化
echo "net.ipv4.ip_forward=1" > /etc/sysctl.d/99-forward.conf
sysctl -p /etc/sysctl.d/99-forward.conf

# iptables MASQUERADE（动态 SNAT）
iptables -t nat -A POSTROUTING -s 252.227.81.0/24 -o eth0 -j MASQUERADE

# iptables SNAT（静态）
iptables -t nat -A POSTROUTING -s 252.227.81.0/24 -o eth0 -j SNAT --to-source 203.0.113.1
```

### 5.2 DNAT（目标地址转换 / 端口转发）

```bash
# 场景：将外部 8080 端口转发到内网 10.0.0.100:80

# iptables
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 10.0.0.100:80
iptables -A FORWARD -p tcp -d 10.0.0.100 --dport 80 -j ACCEPT

# firewalld
firewall-cmd --add-forward-port=port=8080:proto=tcp:toport=80:toaddr=10.0.0.100 --permanent
firewall-cmd --add-masquerade --permanent
firewall-cmd --reload
```

---

## 6. 系统安全加固

### 6.1 CIS Benchmark 关键项

```bash
# 1. 禁用不必要的服务
systemctl disable --now avahi-daemon
systemctl disable --now cups
systemctl disable --now rpcbind

# 2. 文件权限加固
chmod 600 /etc/crontab
chmod 600 /etc/ssh/sshd_config
chmod 644 /etc/passwd
chmod 000 /etc/shadow
chmod 000 /etc/gshadow
chmod 644 /etc/group

# 3. 禁用 USB 存储
echo "blacklist usb-storage" > /etc/modprobe.d/usb-storage.conf

# 4. 配置 /tmp 挂载选项（noexec,nosuid）
# /etc/fstab
# tmpfs /tmp tmpfs defaults,noexec,nosuid,nodev 0 0

# 5. 设置 GRUB 密码
grub2-setpassword   # RHEL
# 或
grub-mkpasswd-pbkdf2   # Ubuntu

# 6. 禁用 core dump
echo "* hard core 0" >> /etc/security/limits.conf
echo "fs.suid_dumpable=0" >> /etc/sysctl.d/99-security.conf
```

### 6.2 登录安全

```bash
# 设置登录超时
echo "TMOUT=900" >> /etc/profile.d/timeout.sh
echo "readonly TMOUT" >> /etc/profile.d/timeout.sh
echo "export TMOUT" >> /etc/profile.d/timeout.sh

# 限制 su 命令
# /etc/pam.d/su
auth required pam_wheel.so use_uid
# 只有 wheel 组成员才能 su

# 登录横幅（法律警告）
cat > /etc/issue.net << 'EOF'
*******************************************************************
*  WARNING: Unauthorized access to this system is prohibited.     *
*  All activities are monitored and logged.                       *
*******************************************************************
EOF
```

### 6.3 审计日志

```bash
# 安装 auditd
apt install auditd   # Ubuntu
yum install audit     # RHEL

# 常用审计规则（/etc/audit/rules.d/audit.rules）
# 监控 sudoers 文件修改
-w /etc/sudoers -p wa -k sudoers_changes
-w /etc/sudoers.d/ -p wa -k sudoers_changes

# 监控用户/组文件修改
-w /etc/passwd -p wa -k user_changes
-w /etc/shadow -p wa -k user_changes
-w /etc/group -p wa -k group_changes

# 监控 SSH 配置修改
-w /etc/ssh/sshd_config -p wa -k sshd_changes

# 监控登录事件
-w /var/log/lastlog -p wa -k logins
-w /var/log/faillog -p wa -k logins

# 搜索审计日志
ausearch -k sudoers_changes
ausearch -k user_changes --start today
aureport --auth          # 认证报告
aureport --login         # 登录报告
```

### 6.4 fail2ban

```bash
# 安装
apt install fail2ban   # Ubuntu
yum install fail2ban   # RHEL

# 配置（/etc/fail2ban/jail.local）
[DEFAULT]
bantime = 3600         # 封禁 1 小时
findtime = 600         # 10 分钟内
maxretry = 5           # 5 次失败
banaction = iptables-multiport

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

# 启动
systemctl enable --now fail2ban

# 查看状态
fail2ban-client status
fail2ban-client status sshd

# 手动封禁/解封
fail2ban-client set sshd banip 1.2.3.4
fail2ban-client set sshd unbanip 1.2.3.4
```

---

## 7. 常见故障排查

### 防火墙规则不生效

```bash
# 1. 检查规则是否存在
iptables -L -n -v --line-numbers | grep 80

# 2. 检查规则顺序（前面的规则优先匹配）
iptables -L INPUT -n --line-numbers

# 3. 检查默认策略
iptables -L | head -3

# 4. 检查 firewalld 是否覆盖了 iptables
systemctl status firewalld

# 5. 检查云平台安全组（阿里云/腾讯云/AWS）
# 云安全组优先于 OS 防火墙
```

### 被锁在外面

```bash
# 预防措施：
# 1. 修改防火墙前，设置定时恢复
echo "iptables-restore < /etc/iptables/rules.v4.bak" | at now + 5 minutes

# 2. 保持一个 SSH 会话不关闭

# 3. 使用控制台/IPMI/VNC 访问

# 4. firewalld 使用 --timeout 选项（临时规则）
firewall-cmd --add-port=22/tcp --timeout=300   # 5 分钟后自动移除
```

### 端口转发不工作

```bash
# 1. 检查 IP 转发是否启用
sysctl net.ipv4.ip_forward

# 2. 检查 NAT 规则
iptables -t nat -L -n -v

# 3. 检查 FORWARD 链
iptables -L FORWARD -n -v

# 4. 检查目标机器是否可达
ping target-ip
```
