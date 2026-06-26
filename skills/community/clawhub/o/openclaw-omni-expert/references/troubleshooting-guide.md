# OpenClaw 故障排查指南

## 目录
- [安装阶段问题](#安装阶段问题)
- [配置阶段问题](#配置阶段问题)
- [运行阶段问题](#运行阶段问题)
- [性能问题](#性能问题)
- [安全与权限问题](#安全与权限问题)
- [日志分析](#日志分析)

## 概览
本指南提供 OpenClaw 在安装、配置和运行过程中常见问题的诊断方法和解决方案,帮助快速定位和解决问题。

## 安装阶段问题

### 问题 1: Node.js 版本过低
**错误信息**:
```
npm ERR! openclaw requires Node >= 22
npm ERR! You have Node v18.17.0
```

**原因**: OpenClaw 严格要求 Node.js v22+,旧版本不支持 ES 模块特性。

**解决方案**:

macOS:
```bash
# 使用 Homebrew 升级
brew install node@22
brew link node@22

# 验证
node --version  # 应显示 v22.x.x
```

Linux:
```bash
# 使用 nvm 安装
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc  # 或 source ~/.zshrc

# 安装 Node.js 22
nvm install 22
nvm use 22
nvm alias default 22

# 验证
node --version
```

Windows:
1. 访问 https://nodejs.org
2. 下载 Node.js v22 LTS 安装包
3. 运行安装程序,一路"下一步"
4. 重启终端验证

---

### 问题 2: npm 权限不足
**错误信息**:
```
npm ERR! Error: EACCES: permission denied
npm ERR! mkdir '/usr/local/lib/node_modules/openclaw'
```

**原因**: npm 缺乏全局安装目录的写入权限。

**解决方案**:

**方案 A: 修复目录权限 (Linux/macOS)**
```bash
# 获取 npm 全局目录
npm config get prefix  # 通常是 /usr/local 或 /usr

# 修复权限
sudo chown -R $(whoami) $(npm config get prefix)/lib/node_modules
sudo chown -R $(whoami) $(npm config get prefix)/bin
```

**方案 B: 配置用户级安装目录 (推荐)**
```bash
# 创建用户目录
mkdir ~/.npm-global

# 配置 npm 使用用户目录
npm config set prefix '~/.npm-global'

# 添加到 PATH
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc  # 或 ~/.zshrc
source ~/.bashrc

# 验证
npm config get prefix  # 应显示 /home/用户/.npm-global
```

**方案 C: 使用官方安装脚本**
```bash
# Linux/macOS
curl -fsSL https://openclaw.ai/install.sh | bash

# Windows PowerShell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

---

### 问题 3: 网络超时
**错误信息**:
```
npm ERR! ETIMEDOUT
npm ERR! network timeout at: https://registry.npmjs.org/openclaw
```

**原因**: npm 官方源在国内访问不稳定。

**解决方案**:

**配置国内镜像源**:
```bash
# 切换到淘宝镜像
npm config set registry https://registry.npmmirror.com

# 验证
npm config get registry
```

**清理缓存并重试**:
```bash
# 清理缓存
npm cache clean --force

# 重新安装
npm install -g openclaw@latest
```

**使用代理** (如有):
```bash
# 配置 npm 代理
npm config set proxy http://127.0.0.1:7890
npm config set https-proxy http://127.0.0.1:7890

# 配置 git 代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 安装完成后可取消代理
npm config delete proxy
npm config delete https-proxy
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

### 问题 4: 构建工具缺失 (Linux/macOS)
**错误信息**:
```
gyp ERR! stack Error: `make` failed with exit code: 2
gyp ERR! not ok
```

**原因**: 缺少 C++ 编译工具。

**解决方案**:

Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y build-essential python3
```

CentOS/RHEL:
```bash
sudo yum groupinstall -y "Development Tools"
sudo yum install -y python3
```

macOS:
```bash
# 安装 Xcode Command Line Tools
xcode-select --install
```

---

### 问题 5: OpenClaw 命令不可用
**现象**: `npm install -g openclaw` 成功,但 `openclaw` 命令报错"command not found"

**原因**: npm 全局安装路径未在 PATH 中。

**解决方案**:

**查找实际安装路径**:
```bash
# 查看 npm 全局路径
npm config get prefix

# 查找 openclaw 可执行文件
$(npm config get prefix)/bin/openclaw --version
```

**添加到 PATH**:
```bash
# 方式1: 临时添加 (仅当前会话)
export PATH=$(npm config get prefix)/bin:$PATH

# 方式2: 永久添加
echo 'export PATH=$(npm config get prefix)/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 验证
which openclaw  # 应显示完整路径
```

**创建软链接 (Linux/macOS)**:
```bash
# 查找 openclaw 路径
which openclaw

# 创建软链接到 /usr/bin
sudo ln -s $(which openclaw) /usr/bin/openclaw

# 验证
openclaw --version
```

---

## 配置阶段问题

### 问题 6: 配置文件不存在
**错误信息**:
```
Error: Configuration file not found: ~/.openclaw/openclaw.json
```

**原因**: 未运行初始化向导。

**解决方案**:
```bash
# 运行配置向导
openclaw onboard

# 或手动创建配置目录
mkdir -p ~/.openclaw
```

---

### 问题 7: 配置文件 JSON 格式错误
**错误信息**:
```
SyntaxError: Unexpected token < in JSON at position 0
```

**原因**: 配置文件被破坏或内容格式错误。

**解决方案**:

**备份并重建**:
```bash
# 备份现有配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 删除损坏的配置
rm ~/.openclaw/openclaw.json

# 重新运行向导
openclaw onboard
```

**验证 JSON 格式**:
```bash
# 使用 jq 验证 (如已安装)
jq . ~/.openclaw/openclaw.json

# 或使用 Python 验证
python3 -m json.tool ~/.openclaw/openclaw.json
```

---

### 问题 8: AI 模型未配置
**现象**: 发送消息后无响应或报错"No model configured"

**解决方案**:

**配置 OpenAI**:
```bash
# 设置 API Key
export OPENAI_API_KEY="your-api-key"

# 或在配置文件中添加
openclaw config edit
# 在 model 部分添加:
# {
#   "provider": "openai",
#   "name": "gpt-4o"
# }
```

**配置 DeepSeek**:
```bash
export DEEPSEEK_API_KEY="your-api-key"
```

**配置本地 Ollama**:
```bash
# 确保 Ollama 已启动
ollama serve

# 拉取模型
ollama pull qwen2.5

# 在配置文件中设置
openclaw config edit
# 添加:
# {
#   "provider": "ollama",
#   "base_url": "http://localhost:11434",
#   "name": "qwen2.5"
# }
```

---

## 运行阶段问题

### 问题 9: Gateway 服务未运行
**错误信息**:
```
❌ Gateway is not running
```

**原因**: 网关服务未启动或已崩溃。

**解决方案**:

**启动网关**:
```bash
# 启动服务
openclaw gateway start

# 检查状态
openclaw gateway status

# 查看日志
tail -f ~/.openclaw/logs/gateway.err.log
```

**查看错误日志**:
```bash
# 查看最新错误
tail -50 ~/.openclaw/logs/gateway.err.log

# 查看完整日志
cat ~/.openclaw/logs/gateway.err.log
```

**重启网关**:
```bash
# 停止服务
openclaw gateway stop

# 启动服务
openclaw gateway start

# 或直接重启
openclaw gateway restart
```

---

### 问题 10: 端口被占用
**错误信息**:
```
Error: Address already in use (port 18789)
```

**原因**: 端口 18789 被其他进程占用。

**解决方案**:

**查找占用进程**:

Linux/macOS:
```bash
# 查找占用进程
lsof -i :18789

# 输出示例:
# COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
# node    12345 user   20u  IPv4  0t0  TCP  *:18789 (LISTEN)
```

Windows:
```powershell
# 查找占用进程
netstat -ano | findstr :18789

# 输出示例:
# TCP    0.0.0.0:18789    0.0.0.0:0    LISTENING    12345
```

**终止进程**:
```bash
# Linux/macOS
kill 12345

# 或强制终止
kill -9 12345

# Windows
taskkill /PID 12345 /F
```

**修改端口配置** (如不能终止进程):
```bash
openclaw config edit
# 修改 gateway 部分的 port 配置
```

---

### 问题 11: 技能安装失败
**错误信息**:
```
❌ Installation failed
npm ERR! code ERESOLVE
```

**原因**: 依赖冲突或网络问题。

**解决方案**:

**清理缓存**:
```bash
# 清理 npm 缓存
npm cache clean --force

# 清理 OpenClaw 插件缓存
rm -rf ~/.openclaw/plugins/*
```

**强制重新安装**:
```bash
# 使用 --force 标志
openclaw plugin install skill-name --force
```

**查看详细错误**:
```bash
# 使用 --verbose 标志
openclaw plugin install skill-name --verbose
```

---

### 问题 12: 通讯频道连接失败
**错误信息**:
```
Channel: telegram ❌ Authentication failed
```

**原因**: API Token 错误或网络问题。

**解决方案**:

**重新配置频道**:
```bash
# 重新登录
openclaw channels login --provider telegram

# 按提示完成 OAuth 流程
```

**验证 API Token**:

Telegram:
1. 访问 @BotFather
2. 选择你的 Bot
3. 查看 Token 格式是否正确 (123456:ABC-DEF1234...)

Discord:
1. 访问 Discord Developer Portal
2. 检查 Token 和 Client ID 是否正确
3. 确保 Bot 有必要的权限

---

## 性能问题

### 问题 13: 响应速度慢
**现象**: 发送消息后需要很长时间才收到回复。

**诊断步骤**:

1. **检查模型类型**:
   - 云端 API: 网络延迟
   - 本地模型: 显存和计算能力不足

2. **检查网络**:
   ```bash
   # 测试 API 连接
   curl -o /dev/null -s -w "%{time_total}\n" https://api.openai.com/

   # 测试本地模型
   curl http://localhost:11434/api/generate -d '{"model":"qwen2.5","prompt":"test"}'
   ```

3. **检查硬件使用**:
   ```bash
   # CPU 使用率
   top

   # 内存使用
   free -h

   # GPU 使用 (Linux)
   nvidia-smi
   ```

**优化建议**:

- 使用更快的模型 (如 gpt-4o-mini)
- 增加系统内存
- 使用 GPU 加速 (本地模型)
- 优化网络连接 (使用代理)
- 减少上下文长度

---

### 问题 14: 内存占用过高
**现象**: OpenClaw 占用大量内存,系统变慢。

**原因**: 长时间运行积累的上下文和日志。

**解决方案**:

**清理日志**:
```bash
# 清理旧日志
find ~/.openclaw/logs -name "*.log" -mtime +7 -delete

# 压缩日志
gzip ~/.openclaw/logs/*.log
```

**限制上下文长度**:
```bash
openclaw config edit
# 设置 max_tokens 或上下文限制
```

**重启服务**:
```bash
openclaw gateway restart
```

---

## 安全与权限问题

### 问题 15: 沙箱权限错误
**错误信息**:
```
Error: Permission denied (sandbox)
```

**原因**: 沙箱环境配置不当。

**解决方案**:

**检查沙箱配置**:
```bash
openclaw config edit
# 检查 sandbox 配置部分
```

**禁用沙箱** (不推荐生产环境):
```bash
openclaw config edit
# 设置 "sandbox": false
```

**修复权限**:
```bash
# 确保用户有执行权限
chmod +x ~/.openclaw/scripts/*
```

---

### 问题 16: macOS 辅助功能权限
**错误信息**:
```
Error: Accessibility features not enabled
```

**原因**: macOS 需要授予辅助功能权限。

**解决方案**:

1. 打开"系统偏好设置"
2. 进入"安全性与隐私" > "隐私" > "辅助功能"
3. 点击左下角锁图标解锁
4. 添加终端或 OpenClaw 应用
5. 重启 OpenClaw

---

## Windows 特有问题

### 问题 17: PowerShell 执行策略限制
**错误信息**:
```
无法加载文件 install_openclaw.ps1,因为在此系统上禁止运行脚本
```

**原因**: PowerShell 默认执行策略限制脚本运行。

**解决方案**:

**临时允许脚本执行**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 或使用 Bypass 策略(仅当前会话)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**永久修改执行策略**:
```powershell
# 以管理员身份运行
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**绕过执行策略**:
```powershell
powershell -ExecutionPolicy Bypass -File install_openclaw.ps1
```

---

### 问题 18: Windows 防火墙阻止连接
**现象**: Gateway 启动但无法访问 Web UI

**原因**: Windows 防火墙阻止端口 18789

**解决方案**:

**添加防火墙规则**:
```powershell
# 以管理员身份运行
New-NetFirewallRule -DisplayName "OpenClaw Gateway" -Direction Inbound -LocalPort 18789 -Protocol TCP -Action Allow
```

**手动配置**:
1. 打开"Windows Defender 防火墙"
2. 点击"高级设置"
3. 选择"入站规则" > "新建规则"
4. 选择"端口" > TCP > 特定本地端口: 18789
5. 选择"允许连接"
6. 应用规则到域、专用、公用网络
7. 命名规则为"OpenClaw Gateway"

---

### 问题 19: 环境变量未刷新
**现象**: 安装成功后 `openclaw` 命令不可用

**原因**: 安装后环境变量未刷新

**解决方案**:

**刷新环境变量**:
```powershell
# 刷新当前会话环境变量
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 验证
openclaw --version
```

**重启终端**:
```powershell
# 关闭并重新打开 PowerShell
# 新终端会自动加载最新环境变量
```

**手动添加 PATH**:
```powershell
# 查找 openclaw 安装路径
where.exe openclaw

# 添加到用户 PATH
$path = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$path;C:\Users\你的用户名\.npm-global", "User")
```

---

### 问题 20: Windows Defender 误杀
**现象**: 安装文件或可执行文件被 Windows Defender 隔离

**原因**: Windows Defender 误判为恶意软件

**解决方案**:

**添加排除项**:
```powershell
# 排除 OpenClaw 目录
Add-MpPreference -ExclusionPath "$env:USERPROFILE\.openclaw"

# 排除 npm 全局目录
Add-MpPreference -ExclusionPath "$env:USERPROFILE\.npm-global"
```

**手动配置**:
1. 打开"Windows 安全中心"
2. 进入"病毒和威胁防护" > "管理设置"
3. 滚动到"排除项"
4. 点击"添加或删除排除项"
5. 添加文件夹: `%USERPROFILE%\.openclaw` 和 `%USERPROFILE%\.npm-global`

---

### 问题 21: spawn EINVAL 错误
**错误信息**:
```
Error: spawn EINVAL
    at ChildProcess.spawn (internal/child_process.js:xxx)
```

**原因**: Windows 原生环境兼容性问题

**解决方案**:

**方案 A: 使用 WSL2** (推荐)
```powershell
# 按照本指南"Windows WSL2 安装步骤"配置 WSL2
# 在 WSL2 Ubuntu 中运行:
bash scripts/install_openclaw.sh
```

**方案 B: 修复环境变量**
```powershell
# 确保 Path 环境变量中不包含空格或特殊字符
# 检查并清理 Path:
$env:Path -split ';'

# 移除无效路径
```

**方案 C: 使用 Git Bash**
```powershell
# 在 Git Bash 中运行安装脚本
bash scripts/install_openclaw.sh
```

---

### 问题 22: Windows Build Tools 缺失
**错误信息**:
```
MSBuild project tools build or are not available
```

**原因**: 缺少 Visual Studio Build Tools

**解决方案**:

**安装 Windows Build Tools**:
```powershell
# 使用 npm 全局安装
npm install --global --production windows-build-tools

# 或使用 Chocolatey
choco install visualstudio2019buildtools
```

**手动安装**:
1. 访问 https://visualstudio.microsoft.com/downloads/
2. 下载 "Build Tools for Visual Studio 2019"
3. 运行安装程序
4. 选择"使用 C++ 的桌面开发"
5. 完成安装

---

### 问题 23: 端口被占用 (Windows)
**错误信息**:
```
Error: bind EADDRINUSE: address already in use :::18789
```

**解决方案**:

**查找占用进程**:
```powershell
# 方法 1: 使用 netstat
netstat -ano | findstr :18789

# 输出示例:
# TCP    0.0.0.0:18789    0.0.0.0:0    LISTENING    12345

# 方法 2: 使用 PowerShell
Get-NetTCPConnection -LocalPort 18789 -ErrorAction SilentlyContinue
```

**终止进程**:
```powershell
# 使用 PID 终止进程
Stop-Process -Id 12345 -Force

# 或使用 taskkill
taskkill /PID 12345 /F
```

**重启 OpenClaw Gateway**:
```powershell
openclaw gateway stop
openclaw gateway start
```

---

## 日志分析

### 日志文件位置

OpenClaw 日志存储在 `~/.openclaw/logs/` 目录:

```
~/.openclaw/logs/
├── gateway.err.log     # Gateway 错误日志
├── gateway.out.log     # Gateway 输出日志
├── agent.log           # Agent 日志
└── install.log         # 安装日志
```

### 常见错误模式

#### EACCES
- **含义**: 权限不足
- **解决**: 修复文件或目录权限

#### ENOENT
- **含义**: 文件或目录不存在
- **解决**: 检查路径或重新安装

#### ETIMEDOUT
- **含义**: 网络超时
- **解决**: 配置镜像源或检查网络

#### ERR_UNSUPPORTED_DIR_IMPORT
- **含义**: Node.js 版本过低
- **解决**: 升级到 Node.js v22+

#### spawn EINVAL
- **含义**: Windows 兼容性问题
- **解决**: 使用 WSL2 或修复权限

### 日志分析技巧

**实时查看日志**:
```bash
tail -f ~/.openclaw/logs/gateway.err.log
```

**搜索错误**:
```bash
grep -i error ~/.openclaw/logs/*.log
grep -i failed ~/.openclaw/logs/*.log
```

**查看最新 100 行**:
```bash
tail -100 ~/.openclaw/logs/gateway.err.log
```

---

## 自动诊断工具

使用内置的诊断工具:

```bash
# 运行完整诊断
python3 scripts/diagnose.py

# 指定日志文件分析
python3 scripts/diagnose.py --log ~/.openclaw/logs/gateway.err.log

# 自动修复问题
python3 scripts/diagnose.py --fix
```

或使用 OpenClaw 内置工具:

```bash
# 健康检查
openclaw doctor

# 查看状态
openclaw status
```

---

## 获取帮助

如果以上方案都无法解决问题:

1. **查看文档**: https://docs.openclaw.ai/
2. **GitHub Issues**: https://github.com/openclaw/openclaw/issues
3. **Discord 社区**: https://discord.gg/openclaw
4. **生成诊断报告**:
   ```bash
   python3 scripts/diagnose.py > diagnosis-report.txt
   # 提供此报告给支持团队
   ```

---

## 预防措施

**定期维护**:
- 定期清理日志文件
- 定期备份配置文件
- 定期更新 OpenClaw 版本

**监控**:
- 设置日志监控
- 配置告警通知
- 定期检查服务状态

**备份**:
```bash
# 自动备份脚本
cat > backup-openclaw.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="~/openclaw-backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/openclaw_$TIMESTAMP.tar.gz ~/.openclaw

echo "Backup created: $BACKUP_DIR/openclaw_$TIMESTAMP.tar.gz"
EOF

chmod +x backup-openclaw.sh
```

**定时任务** (Linux):
```bash
# 添加到 crontab,每天凌晨备份
crontab -e
# 添加: 0 0 * * * ~/backup-openclaw.sh
```
