# 小虾本地部署完整配置指南

> 从腾讯云迁移到本地的完整步骤

---

## 📋 目录

1. [环境准备](#1-环境准备)
2. [安装 OpenClaw](#2-安装-openclaw)
3. [恢复备份数据](#3-恢复备份数据)
4. [网络配置](#4-网络配置)
5. [飞书 Bot 配置](#5-飞书-bot-配置)
6. [启动与验证](#6-启动与验证)
7. [常见问题](#7-常见问题)

---

## 1. 环境准备

### 1.1 硬件要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| CPU | 2核 | 4核+ |
| 内存 | 4GB | 8GB+ |
| 存储 | 20GB 可用空间 | 50GB+ SSD |
| 网络 | 能访问互联网 | 公网 IP 或 Tailscale |
| 运行时间 | - | 24小时开机 |

**推荐设备**: Mac Mini / 树莓派4B / NAS / 旧笔记本

### 1.2 系统要求

- **macOS**: 12+ (Monterey 或更新)
- **Linux**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **Windows**: Windows 10/11 + WSL2

### 1.3 安装依赖

#### macOS

```bash
# 安装 Homebrew（如未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Node.js 22
brew install node@22

# 安装 ffmpeg（用于语音/视频功能）
brew install ffmpeg

# 验证安装
node --version  # v22.x.x
npm --version   # 10.x.x
```

#### Ubuntu/Debian

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# 安装 ffmpeg
sudo apt install -y ffmpeg

# 验证安装
node --version
npm --version
```

#### Windows (WSL2)

```bash
# 在 WSL2 Ubuntu 中执行
sudo apt update
sudo apt install -y curl

# 安装 Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs ffmpeg

# 验证
node --version
```

---

## 2. 安装 OpenClaw

```bash
# 全局安装 OpenClaw
npm install -g openclaw

# 验证安装
openclaw --version

# 查看帮助
openclaw --help
```

---

## 3. 恢复备份数据

### 3.1 下载备份包

```bash
# 创建下载目录
mkdir -p ~/Downloads/xiaoxia-backup
cd ~/Downloads/xiaoxia-backup

# 下载备份包（514MB，可能需要几分钟）
curl -L -o xiaoxia-full-backup.tar.gz \
  https://github.com/zhangzeyu99-web/xiaoxia-memory/releases/download/backup-20260318-full/xiaoxia-full-backup-20260318_112254.tar.gz

# 下载校验文件
curl -L -o xiaoxia-full-backup.tar.gz.sha256 \
  https://github.com/zhangzeyu99-web/xiaoxia-memory/releases/download/backup-20260318-full/xiaoxia-full-backup-20260318_112254.tar.gz.sha256

# 验证文件完整性
sha256sum -c xiaoxia-full-backup.tar.gz.sha256
# 应显示: xiaoxia-full-backup.tar.gz: OK
```

### 3.2 解压备份

```bash
# 解压
tar xzvf xiaoxia-full-backup.tar.gz

# 进入解压后的目录
cd xiaoxia-full-backup-20260318_112254

# 查看内容
ls -la
```

### 3.3 执行恢复脚本

```bash
# 确保 ~/.openclaw 目录存在
mkdir -p ~/.openclaw

# 运行恢复脚本
./restore.sh
```

**恢复脚本会自动复制**:
- `openclaw.json` → `~/.openclaw/`
- `workspace/` → `~/.openclaw/`
- `agents/` → `~/.openclaw/`
- `extensions/` → `~/.openclaw/`
- `autoskill/` → `~/.openclaw/`
- `sessions/` → `~/.openclaw/`
- `cron.json` → `~/.openclaw/`
- `nodes/` → `~/.openclaw/`

### 3.4 验证恢复

```bash
# 检查目录结构
ls -la ~/.openclaw/

# 应显示:
# agents/
# autoskill/
# cron.json
# extensions/
# nodes/
# openclaw.json
# sessions/
# workspace/
```

---

## 4. 网络配置

### 方案 A: Tailscale（推荐）

**优点**: 无需公网IP，自动组网，安全可靠

#### 4.1.1 安装 Tailscale

**macOS**:
```bash
# 从 App Store 安装 Tailscale
# 或命令行
brew install tailscale
sudo tailscale up
```

**Linux**:
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

#### 4.1.2 登录 Tailscale

```bash
# 启动 Tailscale
sudo tailscale up

# 按提示在浏览器中登录账号
# 确保和云端服务器登录同一个账号
```

#### 4.1.3 获取 Tailscale IP

```bash
# 查看本机 Tailscale IP
tailscale ip -4
# 示例输出: 100.x.x.x
```

#### 4.1.4 修改 OpenClaw 配置

```bash
# 编辑配置文件
nano ~/.openclaw/openclaw.json
```

**修改以下字段**:

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "0.0.0.0",
    "controlUi": {
      "allowedOrigins": [
        "http://100.x.x.x:18789"
      ],
      "allowInsecureAuth": false,
      "dangerouslyDisableDeviceAuth": false
    }
  }
}
```

将 `100.x.x.x` 替换为你实际的 Tailscale IP。

---

### 方案 B: 公网 IP + 端口转发

如果你有公网 IP:

#### 4.2.1 配置路由器端口转发

```
路由器后台 → 端口转发/虚拟服务器
外部端口: 18789
内部 IP: 你的本地机器IP
内部端口: 18789
协议: TCP
```

#### 4.2.2 修改 OpenClaw 配置

```bash
nano ~/.openclaw/openclaw.json
```

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local", 
    "bind": "0.0.0.0",
    "controlUi": {
      "allowedOrigins": [
        "http://你的公网IP:18789"
      ]
    }
  }
}
```

#### 4.2.3 DDNS（动态域名）

如果公网 IP 会变化，建议使用 DDNS:
- 花生壳
- No-IP
- 阿里云 DDNS

---

### 方案 C: FRP 内网穿透

如果你没有公网 IP，可用 FRP:

**frps.ini（云服务器）**:
```ini
[common]
bind_port = 7000
token = your_secure_token
```

**frpc.ini（本地机器）**:
```ini
[common]
server_addr = 你的云服务器IP
server_port = 7000
token = your_secure_token

[openclaw]
type = tcp
local_port = 18789
remote_port = 18789
```

---

## 5. 飞书 Bot 配置

### 5.1 登录飞书开发者平台

访问: https://open.feishu.cn/app/

### 5.2 修改事件订阅地址

对每个 Bot 应用执行:

#### bot-xiaoxia（小虾）

1. 找到应用: **bot-xiaoxia**
2. 进入: **事件与回调** → **事件订阅**
3. 修改 **请求地址 URL**:

```
旧: http://43.162.108.47:18789/webhook/feishu
新: http://你的IP:18789/webhook/feishu

# 使用 Tailscale 时:
http://100.x.x.x:18789/webhook/feishu
```

4. 点击 **保存**
5. 验证连接（飞书会发送验证请求）

#### bot-xiaopin（狃姐）

同上，修改 webhook URL

#### bot-xiaoyi（小伊）

同上，修改 webhook URL

### 5.3 验证 Webhook 可访问

```bash
# 从其他机器测试（或用手机流量）
curl http://你的IP:18789/status

# 应返回类似:
{"status":"ok","version":"2026.3.x"}
```

---

## 6. 启动与验证

### 6.1 启动 Gateway

```bash
# 启动服务
openclaw gateway start

# 或使用后台模式
nohup openclaw gateway start > ~/openclaw-gateway.log 2>&1 &
```

### 6.2 检查状态

```bash
# 查看 OpenClaw 状态
openclaw status

# 查看 Gateway 状态
openclaw gateway status

# 查看定时任务
openclaw cron list
```

### 6.3 测试消息收发

1. **飞书私聊测试**:
   - 给小虾发送: "你好"
   - 应收到回复

2. **子 Agent 测试**:
   - @狃姐 测试
   - @小伊 测试

3. **定时任务测试**:
   ```bash
   # 手动触发早报测试
   openclaw cron run 晚星早报
   ```

### 6.4 验证 Session 历史

```bash
# 查看会话列表
openclaw sessions list

# 查看特定会话历史
openclaw sessions history <session-key>
```

---

## 7. 常见问题

### Q1: 启动时报 "port already in use"

```bash
# 查找占用进程
lsof -i :18789

# 或
netstat -tlnp | grep 18789

# 结束占用进程
kill -9 <PID>

# 或修改端口
# 编辑 ~/.openclaw/openclaw.json
# 修改 gateway.port 为其他端口（如 18790）
```

### Q2: 飞书收不到消息

**排查步骤**:

1. **检查 Gateway 是否运行**:
   ```bash
   openclaw gateway status
   ```

2. **检查端口是否可访问**:
   ```bash
   # 本地测试
curl http://localhost:18789/status
   
   # 外部测试（从手机或其他网络）
   curl http://你的IP:18789/status
   ```

3. **检查防火墙**:
   ```bash
   # macOS
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
   
   # Linux
   sudo ufw status
   sudo iptables -L | grep 18789
   ```

4. **查看飞书开发者平台日志**:
   - 事件与回调 → 查看事件日志

### Q3: 插件加载失败

```bash
# 重新安装插件依赖
cd ~/.openclaw/extensions/openclaw-lark
npm install

cd ~/.openclaw/extensions/a2a-gateway
npm install
```

### Q4: Session 历史丢失

```bash
# 检查 sessions 目录
ls -la ~/.openclaw/sessions/

# 如果为空，从备份重新复制
cp -r ~/Downloads/xiaoxia-backup/xiaoxia-full-backup-*/sessions ~/.openclaw/
```

### Q5: 定时任务不执行

```bash
# 检查 cron 配置
openclaw cron list

# 重新添加任务
openclaw cron add --cron "0 9 * * *" --agent main --session isolated \
  --message "执行早报任务" --name "晚星早报"
```

### Q6: 启动时提示权限不足

```bash
# 修复权限
sudo chown -R $(whoami) ~/.openclaw

# 或使用 sudo 启动（不推荐）
sudo openclaw gateway start
```

### Q7: Tailscale 连接不上

```bash
# 检查 Tailscale 状态
tailscale status

# 重新登录
tailscale up --force-reauth

# 检查防火墙是否放行
tailscale netcheck
```

---

## 📞 需要帮助？

如果遇到其他问题:

1. **查看日志**:
   ```bash
   openclaw logs
   # 或
   cat ~/openclaw-gateway.log
   ```

2. **检查配置**:
   ```bash
   openclaw config validate
   ```

3. **重置 Gateway**:
   ```bash
   openclaw gateway stop
   openclaw gateway start
   ```

4. **联系小虾**:
   - 飞书私聊 @小虾
   - 或发送消息到关联的飞书 Bot

---

## ✅ 完成清单

迁移完成后检查:

- [ ] OpenClaw 安装完成
- [ ] 备份数据已恢复
- [ ] 网络配置完成（Tailscale/公网IP/FRP）
- [ ] 飞书 Webhook 已更新
- [ ] Gateway 正常启动
- [ ] 飞书消息能正常收发
- [ ] 子 Agent（狃姐、小伊）响应正常
- [ ] Session 历史可访问
- [ ] 定时任务列表显示正常
- [ ] 测试消息收发成功

---

**祝你迁移顺利！** 🦞

如有问题随时联系小虾。
