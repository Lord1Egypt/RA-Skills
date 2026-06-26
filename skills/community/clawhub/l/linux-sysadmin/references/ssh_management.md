# SSH 管理

## 目录

- [1. 密钥管理](#1-密钥管理)
- [2. sshd 配置与加固](#2-sshd-配置与加固)
- [3. 端口转发](#3-端口转发)
- [4. 跳板机配置](#4-跳板机配置)
- [5. SSH Agent](#5-ssh-agent)
- [6. 多因素认证](#6-多因素认证)
- [7. 常见故障排查](#7-常见故障排查)

---

## 1. 密钥管理

### 1.1 生成密钥对

```bash
# 推荐：Ed25519（安全性高、密钥短、速度快）
ssh-keygen -t ed25519 -C "user@hostname" -f ~/.ssh/id_ed25519

# RSA 4096（兼容性好，老系统用）
ssh-keygen -t rsa -b 4096 -C "user@hostname" -f ~/.ssh/id_rsa

# 不设置密码短语（自动化场景）
ssh-keygen -t ed25519 -f ~/.ssh/id_deploy -N ""
```

### 1.2 部署公钥

```bash
# 方式一：ssh-copy-id（推荐）
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@remote-host

# 方式二：手动复制
cat ~/.ssh/id_ed25519.pub | ssh user@remote-host \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# 方式三：直接在远程机器上操作
# 将公钥内容追加到 ~/.ssh/authorized_keys
echo "ssh-ed25519 AAAA... user@hostname" >> ~/.ssh/authorized_keys
```

### 1.3 密钥权限要求

```bash
# 权限必须严格，否则 SSH 会拒绝使用
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519          # 私钥
chmod 644 ~/.ssh/id_ed25519.pub      # 公钥
chmod 600 ~/.ssh/authorized_keys     # 授权密钥
chmod 600 ~/.ssh/config              # 客户端配置
```

### 1.4 密钥轮换

```bash
# 1. 生成新密钥
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new

# 2. 部署新公钥到所有目标机器
ssh-copy-id -i ~/.ssh/id_ed25519_new.pub user@remote-host

# 3. 验证新密钥可用
ssh -i ~/.ssh/id_ed25519_new user@remote-host "echo OK"

# 4. 从目标机器移除旧公钥
ssh user@remote-host "sed -i '/OLD_KEY_FINGERPRINT/d' ~/.ssh/authorized_keys"

# 5. 替换本地密钥
mv ~/.ssh/id_ed25519 ~/.ssh/id_ed25519_old
mv ~/.ssh/id_ed25519_new ~/.ssh/id_ed25519
mv ~/.ssh/id_ed25519_new.pub ~/.ssh/id_ed25519.pub
```

---

## 2. sshd 配置与加固

### 2.1 关键配置项

```bash
# /etc/ssh/sshd_config 或 /etc/ssh/sshd_config.d/hardening.conf

# === 认证 ===
PermitRootLogin no                # 禁止 root 直接登录
PasswordAuthentication no         # 禁止密码登录（仅密钥）
PubkeyAuthentication yes          # 启用公钥认证
AuthenticationMethods publickey   # 只允许公钥认证
MaxAuthTries 3                    # 最大认证尝试次数
LoginGraceTime 30                 # 登录超时（秒）

# === 访问控制 ===
AllowUsers johndoe deployer       # 只允许指定用户登录
# 或
AllowGroups sshusers              # 只允许指定组登录
DenyUsers root                    # 明确拒绝用户

# === 网络 ===
Port 22                           # 可改为非标准端口（如 2222）
ListenAddress 0.0.0.0             # 监听地址
AddressFamily inet                # 仅 IPv4（inet6 仅 IPv6，any 都允许）

# === 会话 ===
ClientAliveInterval 300           # 每 5 分钟发送心跳
ClientAliveCountMax 2             # 2 次无响应断开
MaxSessions 5                     # 每个连接最大会话数

# === 安全 ===
X11Forwarding no                  # 禁止 X11 转发
AllowTcpForwarding no             # 禁止 TCP 转发（按需开启）
PermitTunnel no                   # 禁止隧道
Banner /etc/ssh/banner.txt        # 登录前显示警告横幅

# === 加密算法（禁用弱算法） ===
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
HostKeyAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256
```

### 2.2 配置变更流程

```bash
# 1. 备份
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%Y%m%d)

# 2. 修改配置（推荐使用 sshd_config.d 目录）
cat > /etc/ssh/sshd_config.d/hardening.conf << 'EOF'
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
EOF

# 3. 语法检查（重要！）
sshd -t
# 如果报错，修正后再继续

# 4. 重载配置（不断开现有连接）
systemctl reload sshd

# 5. 在另一个终端测试新连接
ssh user@this-host

# 6. 确认新连接正常后，关闭旧终端
```

---

## 3. 端口转发

### 3.1 本地端口转发（Local）

```bash
# 将本地 8080 端口转发到远程的 localhost:3306
# 场景：通过 SSH 访问远程数据库
ssh -L 8080:localhost:3306 user@remote-host

# 后台运行
ssh -fNL 8080:localhost:3306 user@remote-host

# 转发到远程内网的其他机器
ssh -L 8080:10.0.0.5:80 user@bastion-host
```

### 3.2 远程端口转发（Remote）

```bash
# 将远程 8080 端口转发到本地的 localhost:3000
# 场景：将内网服务暴露到外网
ssh -R 8080:localhost:3000 user@public-server

# 后台运行
ssh -fNR 8080:localhost:3000 user@public-server
```

### 3.3 动态端口转发（SOCKS 代理）

```bash
# 在本地 1080 端口创建 SOCKS5 代理
ssh -D 1080 user@remote-host

# 后台运行
ssh -fND 1080 user@remote-host

# 使用代理
curl --socks5 localhost:1080 http://internal-site.example.com
```

---

## 4. 跳板机配置

### 4.1 SSH Config 配置

```bash
# ~/.ssh/config

# 跳板机
Host bastion
    HostName bastion.example.com
    User admin
    Port 22
    IdentityFile ~/.ssh/id_ed25519

# 通过跳板机访问内网机器
Host internal-web
    HostName 10.0.0.5
    User deployer
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519

Host internal-db
    HostName 10.0.0.10
    User dba
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519

# 使用通配符批量配置
Host 10.0.0.*
    User admin
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519
```

### 4.2 直接命令行使用

```bash
# ProxyJump（OpenSSH 7.3+，推荐）
ssh -J bastion-user@bastion:22 target-user@10.0.0.5

# 多级跳转
ssh -J bastion1,bastion2 target-user@10.0.0.5

# 旧版本用 ProxyCommand
ssh -o ProxyCommand="ssh -W %h:%p bastion-user@bastion" target-user@10.0.0.5
```

---

## 5. SSH Agent

```bash
# 启动 agent
eval "$(ssh-agent -s)"

# 添加密钥（会提示输入密码短语）
ssh-add ~/.ssh/id_ed25519

# 查看已加载的密钥
ssh-add -l

# 转发 agent（通过跳板机时使用本地密钥）
ssh -A user@bastion-host
# 注意：Agent 转发有安全风险，跳板机管理员可能利用你的密钥

# 更安全的替代方案：ProxyJump（不需要 Agent 转发）
ssh -J bastion target-host
```

---

## 6. 多因素认证

### 6.1 Google Authenticator（TOTP）

```bash
# 安装
apt install libpam-google-authenticator   # Ubuntu/Debian
yum install google-authenticator          # RHEL/CentOS

# 用户初始化
google-authenticator
# 按提示扫描二维码，保存恢复码

# 配置 PAM（/etc/pam.d/sshd）
# 在文件顶部添加：
auth required pam_google_authenticator.so

# 配置 sshd（/etc/ssh/sshd_config）
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive

# 重载
systemctl reload sshd
```

---

## 7. 常见故障排查

### SSH 连接被拒绝

```bash
# 1. 检查 sshd 是否运行
systemctl status sshd

# 2. 检查端口是否监听
ss -tlnp | grep ssh

# 3. 检查防火墙
firewall-cmd --list-ports 2>/dev/null
iptables -L -n | grep 22

# 4. 检查 SELinux（非标准端口）
semanage port -l | grep ssh
# 如果改了端口，需要：
semanage port -a -t ssh_port_t -p tcp 2222
```

### 密钥认证失败

```bash
# 1. 客户端详细日志
ssh -vvv user@host

# 2. 检查权限
ls -la ~/.ssh/
# 目录 700，私钥 600，authorized_keys 600

# 3. 检查服务端日志
journalctl -u sshd -n 50 --no-pager
tail -50 /var/log/auth.log    # Ubuntu
tail -50 /var/log/secure      # RHEL

# 4. 检查 authorized_keys 格式
# 每行一个公钥，不能有多余换行或空格
cat ~/.ssh/authorized_keys | head -1 | wc -c
```

### 连接超时

```bash
# 1. 检查网络连通性
ping -c 3 remote-host
traceroute remote-host

# 2. 检查 SSH 端口连通性
nc -zv remote-host 22 -w 5
# 或
ssh -o ConnectTimeout=5 user@remote-host

# 3. 客户端保活配置（~/.ssh/config）
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes
```
