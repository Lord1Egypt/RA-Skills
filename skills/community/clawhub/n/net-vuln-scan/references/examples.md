# 使用示例

## 示例 1: 本地主机安全检查

### 场景
用户想检查本地主机的安全状况

### 交互过程

```
用户: 检查本机安全
助手: 开始本地安全检测...
```

### 检测命令

```bash
# 1. 端口扫描
python scripts/port_scan.py localhost --fast

# 2. SSL 检测（如果有 Web 服务）
python scripts/ssl_check.py localhost

# 3. 生成报告
python scripts/report_gen.py
```

### 预期结果

```
=== 本机安全检测报告 ===

🔍 端口扫描:
- 135/tcp  Windows RPC
- 139/tcp  NetBIOS
- 445/tcp  SMB (风险: 建议关闭)
- 3389/tcp RDP (风险: 仅内网访问)

🔒 SSL 检测:
- 未检测到 HTTPS 服务

🛡️ 建议:
1. 禁用 SMB 1.0
2. 防火墙仅开放必要端口
3. 关闭 RDP（如果不常用）
```

---

## 示例 2: Web 服务器检测

### 场景
用户有一个 Web 服务器，想检查安全性

### 交互过程

```
用户: 检测 web.example.com 的安全
助手: 开始 SSL 和安全头检测...
```

### 检测命令

```bash
# SSL 证书和配置检测
python scripts/ssl_check.py web.example.com --verbose
```

### 预期结果

```
=== web.example.com 安全检测 ===

✅ 证书有效（剩余 89 天）
✅ 支持 TLS 1.3
✅ 已启用 HSTS
❌ 缺少 X-Content-Type-Options
❌ 缺少 X-Frame-Options

风险: 🟡 中危
建议: 配置缺失的安全响应头
```

---

## 示例 3: 内网主机批量检测

### 场景
用户想检查整个内网段的安全性

### 交互过程

```
用户: 扫描 192.168.1.0/24 网段
助手: 发现 15 台在线主机，开始检测...
```

### 检测命令

```bash
# 1. 发现在线主机
python scripts/network_discovery.py 192.168.1.0/24

# 2. 对在线主机进行端口扫描
python scripts/port_scan.py 192.168.1.1 --fast
python scripts/port_scan.py 192.168.1.2 --fast
# ... 以此类推

# 3. 生成汇总报告
python scripts/report_gen.py --format html
```

### 预期结果

```
=== 内网安全扫描报告 ===

发现主机: 15 台
在线主机: 12 台

高危问题:
- 192.168.1.5: 开放 Redis 6379 端口
- 192.168.1.8: MySQL 允许远程访问
- 192.168.1.10: 发现 Telnet 服务

中危问题:
- 3 台主机开放 RDP
- 2 台主机 SSH 使用弱密码

总体风险: 🔴 高危
```

---

## 示例 4: 修复建议生成

### 场景
用户收到检测报告，想知道如何修复

### 交互过程

```
用户: 如何修复发现的问题？
助手: 根据检测结果，生成修复方案...
```

### 修复步骤

1. **关闭不必要的端口**
   ```bash
   # Windows
   netsh advfirewall firewall add rule name="Block SMB" dir=in action=block localport=445
   
   # Linux
   sudo ufw deny 445/tcp
   ```

2. **加强 SSH 认证**
   ```bash
   # 生成密钥
   ssh-keygen -t ed25519
   
   # 禁用密码认证
   sudo nano /etc/ssh/sshd_config
   # PasswordAuthentication no
   # PubkeyAuthentication yes
   sudo systemctl restart sshd
   ```

3. **配置防火墙**
   ```bash
   # 仅允许特定 IP 访问
   sudo ufw allow from 192.168.1.0/24 to any port 3306
   ```
