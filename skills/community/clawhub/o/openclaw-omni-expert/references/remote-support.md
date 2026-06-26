# OpenClaw 远程支持指南

## 目录
- [概述](#概述)
- [SSH 配置](#ssh-配置)
- [密钥管理](#密钥管理)
- [远程安装](#远程安装)
- [远程诊断](#远程诊断)
- [远程修复](#远程修复)
- [批量操作](#批量操作)
- [安全最佳实践](#安全最佳实践)
- [常见场景](#常见场景)

## 概述

OpenClaw 远程支持功能允许您从本地电脑远程帮助朋友、同事或客户安装、诊断和修复 OpenClaw。

**核心能力**:
- 远程环境检测
- 远程自动化安装
- 远程故障诊断
- 远程自动修复
- 远程日志收集
- 批量多主机操作

**适用场景**:
- 帮助技术能力较弱的朋友安装 OpenClaw
- 管理多台服务器的 OpenClaw 部署
- 远程技术支持和故障排查
- 团队协作环境配置

## SSH 配置

### 方式一:密码认证 (简单但不推荐)

```bash
python3 scripts/remote-helper.py install \
  --host friend@example.com \
  --password yourpassword
```

**缺点**:
- 每次需要输入密码
- 安全性较低
- 不支持批量操作

### 方式二:密钥认证 (推荐)

**1. 生成 SSH 密钥对** (本地电脑)
```bash
# 生成新密钥 (如果还没有)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 默认保存到 ~/.ssh/id_rsa 和 ~/.ssh/id_rsa.pub
```

**2. 将公钥复制到远程主机**

**方法 A: 使用 ssh-copy-id (Linux/macOS)**
```bash
ssh-copy-id user@remote-host
```

**方法 B: 手动复制 (Windows/Linux/macOS)**
```bash
# 查看公钥内容
cat ~/.ssh/id_rsa.pub

# 在远程主机上添加到 authorized_keys
mkdir -p ~/.ssh
echo "ssh-rsa AAAAB3... your_email@example.com" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

**方法 C: 在远程主机上执行 (需要密码)**
```bash
# 在远程主机上
mkdir -p ~/.ssh
chmod 700 ~/.ssh
# 粘贴公钥内容到 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**3. 测试连接**
```bash
ssh user@remote-host
# 应该能直接登录,无需输入密码
```

### 方式三:指定密钥文件

```bash
python3 scripts/remote-helper.py install \
  --host user@remote-host \
  --key-file ~/.ssh/my_custom_key
```

## 密钥管理

### 安全最佳实践

1. **保护私钥**
```bash
# 设置私钥文件权限
chmod 600 ~/.ssh/id_rsa
chmod 600 ~/.ssh/my_custom_key

# 不要分享私钥
# 不要将私钥提交到代码仓库
```

2. **使用不同的密钥对**
```bash
# 为不同用途生成不同的密钥
ssh-keygen -t rsa -f ~/.ssh/openclaw_remote -C "openclaw-remote"
ssh-keygen -t rsa -f ~/.ssh/friend_computer -C "friend-computer"
```

3. **定期轮换密钥**
```bash
# 每 6-12 个月更换一次密钥
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# 将新公钥添加到远程主机
# 删除旧密钥的公钥
```

4. **使用 SSH 配置文件**
```bash
# 编辑 ~/.ssh/config
cat >> ~/.ssh/config << 'EOF'

# 朋友的电脑
Host friend-computer
    HostName friend.example.com
    User friend
    Port 22
    IdentityFile ~/.ssh/friend_computer

# 生产服务器
Host prod-server
    HostName prod.example.com
    User admin
    Port 2222
    IdentityFile ~/.ssh/prod_server

EOF
```

### 密钥分发清单

**分发公钥前确认**:
- [ ] 对方信任你
- [ ] 了解对方将给予的权限级别
- [ ] 明确密钥用途和有效期
- [ ] 约定安全删除密钥的方式

**撤销密钥访问**:
```bash
# 在远程主机上编辑 authorized_keys
vi ~/.ssh/authorized_keys
# 删除对应的公钥行
```

## 远程安装

### 基本用法

**单台主机安装**:
```bash
python3 scripts/remote-helper.py install \
  --host friend@example.com \
  --key-file ~/.ssh/id_rsa
```

**指定目标平台**:
```bash
# 如果自动检测失败,可以手动指定
python3 scripts/remote-helper.py install \
  --host friend@example.com \
  --key-file ~/.ssh/id_rsa \
  --platform linux    # 或 macos/windows
```

### 安装流程

1. **连接验证**: 建立 SSH 连接
2. **平台检测**: 自动识别目标操作系统
3. **脚本上传**: 将安装脚本上传到远程主机的 /tmp 目录
4. **执行安装**: 远程运行安装脚本
5. **验证安装**: 检查 openclaw 命令是否可用
6. **清理临时文件**: 删除上传的安装脚本

### 支持的平台

| 平台 | 自动检测 | 手动指定 | 脚本类型 |
|------|----------|----------|----------|
| Linux (Ubuntu/Debian/CentOS) | ✅ | `--platform linux` | Bash |
| macOS | ✅ | `--platform macos` | Bash |
| Windows (通过 Git Bash) | ✅ | `--platform windows` | PowerShell |

### Windows 特殊说明

如果目标主机是 Windows,需要先安装 Git Bash:

1. 在 Windows 主机上下载并安装 Git for Windows
2. 启动 Git Bash
3. 确保 OpenSSH 服务器已启用 (Windows 10 1809+)

**启用 Windows SSH 服务** (在目标主机上):
```powershell
# 以管理员身份运行 PowerShell
Install-WindowsFeature -Name OpenSSH-Server
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

## 远程诊断

### 基本用法

```bash
python3 scripts/remote-helper.py diagnose \
  --host friend@example.com \
  --key-file ~/.ssh/id_rsa
```

### 诊断内容

远程诊断会执行以下检查:

1. **服务状态**
   - OpenClaw 是否安装
   - Gateway 服务状态
   - 端口占用情况

2. **配置检查**
   - 配置文件是否存在
   - JSON 格式是否有效
   - 模型是否配置
   - 频道是否配置

3. **依赖检查**
   - Node.js 版本
   - npm 版本
   - Git 版本
   - Python 版本

4. **网络检查**
   - npm 源连接
   - GitHub 连接

5. **日志分析**
   - 错误模式识别
   - 常见问题定位

### 下载日志

默认情况下,诊断会下载远程日志文件到本地:

```bash
python3 scripts/remote-helper.py diagnose \
  --host friend@example.com \
  --key-file ~/.ssh/id_rsa
```

**日志保存位置**:
```
~/openclaw-remote-backup/
├── {hostname}_gateway.err.log
├── {hostname}_gateway.out.log
└── {hostname}_install.log
```

**不下载日志**:
```bash
python3 scripts/remote-helper.py diagnose \
  --host friend@example.com \
  --key-file ~/.ssh/id_rsa \
  --no-download-logs
```

### 诊断报告

诊断结果会自动保存为 JSON 文件:

```bash
~/openclaw-remote-backup/
└── diagnosis_{hostname}_20260306_194500.json
```

报告包含:
- 系统信息
- 服务状态
- 配置详情
- 检测到的问题列表
- 每个问题的严重程度和修复建议

## 远程修复

### 基本用法

**修复所有问题**:
```bash
python3 scripts/remote-helper.py fix \
  --host friend@example.com \
  --key-file ~/.ssh/id_rsa
```

**修复特定类别**:
```bash
python3 scripts/remote-helper.py fix \
  --host friend@example.com \
  --key-file ~/.ssh/id_rsa \
  --fix-category dependencies    # 或 permissions/network/config/service
```

### 修复类别

| 类别 | 说明 |
|------|------|
| `dependencies` | 修复依赖问题 (Node.js/Git/Python) |
| `permissions` | 修复权限问题 |
| `network` | 修复网络配置 (npm 镜像源) |
| `configuration` | 修复配置文件 |
| `service` | 修复服务状态 |
| `filesystem` | 修复文件系统问题 |

### 修复流程

1. 上传修复脚本到远程主机
2. 执行诊断获取问题列表
3. 逐个尝试自动修复
4. 输出修复结果
5. 清理临时文件

**注意**: 某些修复可能需要用户交互或手动操作,修复工具会给出明确提示。

## 批量操作

### 准备主机列表

创建文本文件,每行一个主机:

```bash
# hosts.txt
friend@example.com
colleague@example.com
prod1@server.example.com
prod2@server.example.com
```

### 批量安装

```bash
python3 scripts/remote-helper.py install \
  --batch hosts.txt \
  --key-file ~/.ssh/id_rsa
```

### 批量诊断

```bash
python3 scripts/remote-helper.py diagnose \
  --batch hosts.txt \
  --key-file ~/.ssh/id_rsa \
  --no-download-logs    # 批量时建议不下载日志
```

### 批量修复

```bash
python3 scripts/remote-helper.py fix \
  --batch hosts.txt \
  --key-file ~/.ssh/id_rsa \
  --fix-category dependencies
```

### 批量操作输出

批量操作会显示每台主机的处理进度和结果:

```
======================================================
批量操作: install
目标主机: 4 台
======================================================

[friend@example.com] 开始处理...

检测到操作系统: Linux 5.15.0-72-generic x86_64
✓ 检测到: ubuntu

上传安装脚本...
✓ 上传成功

开始远程安装 (这可能需要几分钟)...
--------------------------------------------------
...

[friend@example.com] 处理完成

[prod1@server.example.com] 开始处理...
...

======================================================
批量操作完成
======================================================

总计: 4 台
成功: 3 台
失败: 1 台

失败的主机:
  - prod2@server.example.com: Connection timed out

======================================================
```

## 安全最佳实践

### 1. 最小权限原则

```bash
# 不要使用 root 账户进行远程操作
# 使用普通用户,必要时使用 sudo

# 在远程主机上配置 sudoers
visudo
# 添加: friend ALL=(ALL) NOPASSWD: /usr/bin/npm, /usr/bin/openclaw
```

### 2. 网络安全

```bash
# 使用 VPN 或专用网络
# 避免在公共网络上传输敏感信息

# 限制 SSH 端口访问
# 配置防火墙规则,只允许特定 IP 访问
```

### 3. 审计日志

```bash
# 在远程主机上启用 SSH 日志
# /var/log/auth.log (Linux)
# /var/log/secure (CentOS/RHEL)

# 定期检查可疑登录
grep "Accepted" /var/log/auth.log
```

### 4. 定期审查密钥

```bash
# 在远程主机上查看所有授权密钥
cat ~/.ssh/authorized_keys

# 定期清理不再使用的密钥
```

### 5. 使用配置文件管理

```bash
# ~/.ssh/config 示例
Host friend-desktop
    HostName 192.168.1.100
    User friend
    IdentityFile ~/.ssh/friend_desktop_key
    Port 22

Host prod-db
    HostName db.example.com
    User dbadmin
    IdentityFile ~/.ssh/db_key
    Port 2222
```

## 常见场景

### 场景 1: 帮助朋友在家安装

**背景**: 朋友对技术不熟悉,需要你帮助安装 OpenClaw

**步骤**:

1. **准备密钥**
```bash
# 生成密钥对
ssh-keygen -t rsa -f ~/.ssh/friend_desktop -C "friend-desktop"

# 将公钥发给朋友 (通过微信/QQ/邮件)
cat ~/.ssh/friend_desktop.pub
```

2. **指导朋友配置密钥**
```
请按以下步骤操作:

1. 打开终端 (Linux/macOS) 或 Git Bash (Windows)
2. 复制以下公钥内容:
   ssh-rsa AAAAB3N... friend-desktop

3. 执行命令:
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   echo "粘贴公钥内容" >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys

4. 完成后告诉我
```

3. **测试连接**
```bash
ssh -i ~/.ssh/friend_desktop friend@friend-desktop-ip
```

4. **远程安装**
```bash
python3 scripts/remote-helper.py install \
  --host friend@friend-desktop-ip \
  --key-file ~/.ssh/friend_desktop
```

5. **指导朋友使用**
```
安装完成!现在你可以:

1. 打开终端,输入:
   openclaw onboard

2. 按照提示配置 AI 模型和通讯频道

3. 访问 Web UI:
   http://127.0.0.1:18789
```

### 场景 2: 管理多台开发服务器

**背景**: 你需要管理 5 台开发服务器的 OpenClaw 环境

**步骤**:

1. **配置批量密钥**
```bash
# 为所有服务器生成统一密钥
ssh-keygen -t rsa -f ~/.ssh/dev_servers -C "dev-servers"

# 将公钥部署到所有服务器
for server in dev1 dev2 dev3 dev4 dev5; do
    ssh-copy-id -i ~/.ssh/dev_servers.pub admin@$server.example.com
done
```

2. **创建主机列表**
```bash
cat > ~/dev_servers.txt << EOF
admin@dev1.example.com
admin@dev2.example.com
admin@dev3.example.com
admin@dev4.example.com
admin@dev5.example.com
EOF
```

3. **批量检查环境**
```bash
python3 scripts/remote-helper.py check \
  --batch ~/dev_servers.txt \
  --key-file ~/.ssh/dev_servers
```

4. **批量安装 (如需要)**
```bash
python3 scripts/remote-helper.py install \
  --batch ~/dev_servers.txt \
  --key-file ~/.ssh/dev_servers \
  --platform linux
```

5. **批量诊断**
```bash
python3 scripts/remote-helper.py diagnose \
  --batch ~/dev_servers.txt \
  --key-file ~/.ssh/dev_servers \
  --no-download-logs
```

### 场景 3: 远程故障排查

**背景**: 朋友的 OpenClaw 出现问题,需要你远程诊断

**步骤**:

1. **远程诊断**
```bash
python3 scripts/remote-helper.py diagnose \
  --host friend@example.com \
  --key-file ~/.ssh/friend_key \
  --download-logs
```

2. **分析诊断报告**
```bash
# 查看本地保存的报告
cat ~/openclaw-remote-backup/diagnosis_friend_*.json

# 或使用 jq 工具格式化查看
jq . ~/openclaw-remote-backup/diagnosis_friend_*.json
```

3. **查看下载的日志**
```bash
# 查看错误日志
cat ~/openclaw-remote-backup/friend_gateway.err.log

# 搜索错误
grep -i error ~/openclaw-remote-backup/friend_*.log
```

4. **远程修复**
```bash
# 根据诊断结果选择修复策略

# 修复依赖问题
python3 scripts/remote-helper.py fix \
  --host friend@example.com \
  --key-file ~/.ssh/friend_key \
  --fix-category dependencies

# 修复权限问题
python3 scripts/remote-helper.py fix \
  --host friend@example.com \
  --key-file ~/.ssh/friend_key \
  --fix-category permissions

# 修复所有问题
python3 scripts/remote-helper.py fix \
  --host friend@example.com \
  --key-file ~/.ssh/friend_key
```

### 场景 4: 团队协作环境配置

**背景**: 新员工加入团队,需要快速配置 OpenClaw 开发环境

**步骤**:

1. **创建配置脚本**
```bash
cat > setup_employee.sh << 'EOF'
#!/bin/bash
# 新员工环境配置脚本

# 1. 安装依赖
sudo apt-get update
sudo apt-get install -y nodejs npm git python3

# 2. 安装 OpenClaw
npm install -g openclaw@latest

# 3. 配置团队模型和频道
openclaw config edit
# 添加团队统一的配置

EOF
chmod +x setup_employee.sh
```

2. **使用远程助手部署**
```bash
python3 scripts/remote-helper.py install \
  --host newemployee@example.com \
  --key-file ~/.ssh/team_key

# 上传并执行配置脚本
python3 scripts/remote-helper.py diagnose \
  --host newemployee@example.com \
  --key-file ~/.ssh/team_key
```

3. **提供使用文档**
```
欢迎加入团队!OpenClaw 环境已配置完成。

快速开始:
1. 访问: http://127.0.0.1:18789
2. 输入你的 API Key
3. 开始使用

团队文档: https://docs.example.com/openclaw
遇到问题: 联系技术支持
```

## 故障排查

### 问题 1: SSH 连接超时

**症状**: `Connection timed out`

**原因**:
- 目标主机未开启 SSH 服务
- 防火墙阻止连接
- 网络不可达
- 端口号错误

**解决方案**:
```bash
# 1. 检查目标主机 SSH 服务
ssh user@remote-host "systemctl status sshd"  # Linux
ssh user@remote-host "launchctl list | grep ssh"  # macOS

# 2. 检查防火墙
# 在目标主机上开放 SSH 端口

# 3. 测试网络连通性
ping remote-host
telnet remote-host 22

# 4. 检查端口
nmap -p 22 remote-host
```

### 问题 2: 认证失败

**症状**: `Authentication failed`

**原因**:
- 密码错误
- 密钥文件路径错误
- 公钥未添加到 authorized_keys
- 权限配置错误

**解决方案**:
```bash
# 1. 验证密钥权限
ls -l ~/.ssh/id_rsa  # 应该是 600

# 2. 测试连接 (显示详细信息)
ssh -vvv user@remote-host

# 3. 检查 authorized_keys
ssh user@remote-host "cat ~/.ssh/authorized_keys"

# 4. 检查 SSH 日志
ssh user@remote-host "tail -20 /var/log/auth.log"
```

### 问题 3: 权限不足

**症状**: 远程安装失败,提示权限错误

**原因**:
- 目标用户无 sudo 权限
- 安装目录权限不足

**解决方案**:
```bash
# 1. 配置 sudo 免密码 (谨慎使用)
sudo visudo
# 添加: username ALL=(ALL) NOPASSWD: /usr/bin/npm, /usr/bin/openclaw

# 2. 使用用户级安装目录
npm config set prefix ~/.npm-global
```

### 问题 4: 网络问题

**症状**: 远程脚本执行超时或失败

**原因**:
- 目标主机网络受限
- npm 源无法访问
- 依赖下载失败

**解决方案**:
```bash
# 1. 配置国内镜像源 (在目标主机上)
python3 scripts/remote-helper.py fix \
  --host user@remote-host \
  --key-file ~/.ssh/id_rsa \
  --fix-category network

# 2. 使用代理
# 在目标主机上设置代理
export http_proxy=http://proxy-server:port
export https_proxy=http://proxy-server:port
```

## 总结

OpenClaw 远程支持功能提供了强大的远程协作能力:

**核心优势**:
- 安全可靠的 SSH 连接
- 全自动化的安装流程
- 智能诊断和修复
- 批量多主机管理
- 完整的日志收集

**使用建议**:
1. 优先使用密钥认证
2. 遵循最小权限原则
3. 定期审查密钥和访问权限
4. 做好日志审计和备份
5. 为不同场景创建配置模板

通过远程支持功能,您可以轻松帮助任何人、任何地点安装和使用 OpenClaw,真正实现"零距离"的技术支持!
