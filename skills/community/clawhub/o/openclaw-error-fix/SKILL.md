---
name: openclaw-error-fix
version: 1.0.0
description: OpenClaw 常见错误修复 - 解决安装/配置/运行问题。适合：遇到错误的用户。
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins: []
---

# OpenClaw 常见错误修复指南

遇到错误不用慌，这里有你需要的解决方案。

## 安装错误

### 1. Node.js 版本不对

**错误**：
```
error: node >= 20 required
```

**解决**：
```bash
# macOS
brew install node@20

# Ubuntu
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证
node --version  # 应该显示 v20.x.x
```

### 2. 权限错误

**错误**：
```
EACCES: permission denied
```

**解决**：
```bash
# 不要用 sudo！修复 npm 权限
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
source ~/.zshrc

# 重新安装
npm install -g openclaw
```

### 3. 网络错误

**错误**：
```
network timeout
```

**解决**：
```bash
# 切换国内镜像
npm config set registry https://registry.npmmirror.com

# 或使用代理
npm config set proxy http://127.0.0.1:7890
```

## 配置错误

### 1. API Key 无效

**错误**：
```
Invalid API key
```

**解决**：
1. 检查 API Key 是否正确（无空格）
2. 检查是否过期
3. 检查余额是否充足

```bash
# 验证 DeepSeek API Key
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer $API_KEY"
```

### 2. 模型不存在

**错误**：
```
Model not found
```

**解决**：
```bash
# 查看支持的模型
openclaw models list

# 使用正确的模型名
openclaw config set model deepseek-chat
```

### 3. 配置文件损坏

**错误**：
```
Cannot read config file
```

**解决**：
```bash
# 重置配置
rm ~/.openclaw/config.yaml
openclaw config init
```

## 运行错误

### 1. 端口被占用

**错误**：
```
Port 3000 already in use
```

**解决**：
```bash
# 查找占用进程
lsof -i :3000

# 杀掉进程
kill -9 <PID>

# 或换端口
openclaw config set port 3001
```

### 2. 内存不足

**错误**：
```
JavaScript heap out of memory
```

**解决**：
```bash
# 增加内存限制
export NODE_OPTIONS="--max-old-space-size=4096"
openclaw start
```

### 3. 连接超时

**错误**：
```
Connection timeout
```

**解决**：
```bash
# 检查网络
ping api.deepseek.com

# 增加超时时间
openclaw config set timeout 60000
```

## 平台连接错误

### 1. Telegram 连接失败

**错误**：
```
Telegram bot token invalid
```

**解决**：
1. 重新创建 Bot：https://t.me/BotFather
2. 复制新的 Token
3. 更新配置

### 2. Discord 连接失败

**错误**：
```
Discord token invalid
```

**解决**：
1. 重新生成 Token：https://discord.com/developers
2. 检查 Bot 权限
3. 邀请 Bot 到服务器

### 3. 钉钉连接失败

**错误**：
```
DingTalk webhook invalid
```

**解决**：
1. 检查 Webhook URL
2. 确认机器人未被禁用
3. 检查关键词配置

## 快速诊断

```bash
# 运行诊断
openclaw doctor

# 查看日志
openclaw logs --tail 100

# 检查配置
openclaw config check
```

## 需要帮助？

如果以上方法都无法解决：

- 技术支持：¥99
- 远程调试：¥299
- 企业支持：¥999

联系：微信 yang1002378395 或 Telegram @yangster151

---
创建：2026-03-14
