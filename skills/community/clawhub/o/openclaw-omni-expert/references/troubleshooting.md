# OpenClaw 故障排查手册

## 目录
- [安装故障](#安装故障)
- [配置故障](#配置故障)
- [运行故障](#运行故障)
- [性能故障](#性能故障)
- [网络故障](#网络故障)
- [安全故障](#安全故障)

---

## 安装故障

### 故障 1: Node.js 版本不兼容

**症状:**
- 安装失败
- 报错 'Unsupported platform'
- 启动报错 'ENGINE_ERROR'

**诊断:**
```bash
node --version
npm --version
```

**解决方案:**

1. 卸载旧版本:
```bash
sudo apt remove nodejs
```

2. 安装 Node.js 22:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22
```

3. 验证:
```bash
node --version  # 应显示 v22.x.x
```

---

### 故障 2: 权限不足

**症状:**
- npm install 报错 'EACCES'
- 无法创建配置文件

**解决方案:**

1. 配置 npm 全局目录:
```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

2. 或使用 Yarn:
```bash
npm install -g yarn
yarn global add openclaw
```

---

### 故障 3: 网络超时

**症状:**
- npm install 超时
- 无法下载依赖

**解决方案:**

1. 切换国内镜像:
```bash
npm config set registry https://registry.npmmirror.com
npm install openclaw
```

2. 配置代理:
```bash
npm config set proxy http://proxy.example.com:8080
npm config set https-proxy http://proxy.example.com:8080
```

---

## 配置故障

### 故障 4: API Key 无效

**症状:**
- API 返回 401
- 错误 'Invalid API key'

**诊断:**
```bash
cat ~/.openclaw/config.json | grep api_key
```

**解决方案:**

1. 重新获取 API Key:
   - 登录 OpenAI/Anthropic 控制台
   - 创建新 API Key
   - 更新配置

2. 验证配置:
```bash
openclaw config test-ai
```

---

### 故障 5: 配置文件格式错误

**症状:**
- 启动失败
- 报错 'Invalid JSON'

**诊断:**
```bash
cat ~/.openclaw/config.json | python3 -m json.tool
```

**解决方案:**

1. 备份并重置:
```bash
cp ~/.openclaw/config.json ~/.openclaw/config.json.bak
rm ~/.openclaw/config.json
openclaw config init
```

2. 手动修复 JSON 格式

---

### 故障 6: 端口被占用

**症状:**
- 报错 'Address already in use'
- 无法启动 Gateway

**诊断:**
```bash
lsof -i :18789
netstat -tlnp | grep 18789
```

**解决方案:**

1. 停止占用进程:
```bash
kill $(lsof -ti :18789)
```

2. 或更换端口:
```json
{
  "gateway": {"port": 18790}
}
```

---

## 运行故障

### 故障 7: Gateway 无法启动

**症状:**
- 服务启动后退出
- 健康检查失败

**诊断:**
```bash
tail -100 ~/.openclaw/logs/openclaw.log
free -h
openclaw health --verbose
```

**解决方案:**

1. 完整重启:
```bash
openclaw stop
rm -rf ~/.openclaw/tmp/*
openclaw config validate
openclaw start
openclaw status
```

---

### 故障 8: Agent 执行超时

**症状:**
- 任务长时间无响应
- 报错 'Task timeout'

**解决方案:**

1. 优化超时配置:
```json
{
  "agent": {
    "timeout": 120,
    "tool_timeout": 30
  }
}
```

2. 添加循环保护:
```json
{
  "agent": {
    "max_iterations": 10
  }
}
```

---

### 故障 9: 记忆数据丢失

**症状:**
- 历史对话丢失
- 上下文不连贯

**诊断:**
```bash
ls -la ~/.openclaw/chroma/
df -h ~/.openclaw
```

**解决方案:**

1. 从备份恢复:
```bash
openclaw stop
cp -r ~/.openclaw/backups/chroma/* ~/.openclaw/chroma/
openclaw start
```

2. 清理并重建:
```bash
openclaw memory cleanup --rebuild
```

---

### 故障 10: 工具调用失败

**症状:**
- 报错 'Tool not found'
- 工具返回错误

**诊断:**
```bash
openclaw tools list
openclaw tools test <tool_name>
```

**解决方案:**

1. 重新注册工具:
```bash
openclaw config edit
# 添加工具配置
openclaw restart
```

---

## 性能故障

### 故障 11: 响应延迟过高

**症状:**
- API 响应 > 5 秒
- 超时错误增加

**诊断:**
```bash
openclaw metrics latency
top -bn1 | head -20
```

**解决方案:**

1. 启用缓存:
```json
{
  "cache": {
    "enabled": true,
    "ttl": 3600
  }
}
```

2. 优化向量检索:
```json
{
  "memory": {
    "vector": {
      "ef_search": 100
    }
  }
}
```

3. 使用更快的模型:
```json
{
  "model": {"model": "gpt-4o-mini"}
}
```

---

### 故障 12: 内存使用过高

**症状:**
- 系统内存接近耗尽
- 出现 OOM

**诊断:**
```bash
free -h
du -sh ~/.openclaw/chroma/
```

**解决方案:**

1. 清理向量数据:
```bash
openclaw memory cleanup --older-than 30d
openclaw memory optimize
```

2. 限制上下文:
```json
{
  "agent": {
    "max_context_tokens": 32000
  }
}
```

---

### 故障 13: CPU 使用率过高

**症状:**
- CPU 持续 100%
- 系统响应慢

**解决方案:**

1. 限制并发:
```json
{
  "gateway": {
    "rate_limit": {
      "enabled": true,
      "requests_per_minute": 60
    }
  }
}
```

---

## 网络故障

### 故障 14: 无法连接外部 API

**症状:**
- API 调用超时
- SSL 错误

**诊断:**
```bash
curl -v https://api.openai.com
nslookup api.openai.com
```

**解决方案:**

1. 配置代理:
```json
{
  "proxy": {
    "http": "http://proxy:8080",
    "https": "http://proxy:8080"
  }
}
```

2. 禁用 SSL 验证 (仅测试):
```bash
export NODE_TLS_REJECT_UNAUTHORIZED=0
```

---

### 故障 15: Webhook 无法接收

**症状:**
- Webhook 无响应
- 消息接收失败

**解决方案:**

1. 配置公网访问:
```bash
# 获取公网 IP
curl ifconfig.me

# 配置防火墙
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 配置 SSL
sudo certbot --nginx -d your-domain.com
```

2. 更新 Webhook URL

---

## 安全故障

### 故障 16: API Key 泄露

**症状:**
- 额度异常消耗
- 未经授权的请求

**紧急处理:**

1. 撤销泄露的 Key:
   - 登录 OpenAI/Anthropic 控制台
   - 撤销当前 Key
   - 生成新 Key

2. 更新配置:
```bash
openclaw config edit
# 更新 API Key
openclaw restart
```

3. 检查使用记录

**安全加固:**

1. 限制文件权限:
```bash
chmod 600 ~/.openclaw/config.json
```

2. 使用环境变量:
```bash
export OPENCLAW_API_KEY="sk-xxx"
```

3. 启用审计日志

---

### 故障 17: 未授权访问

**症状:**
- 配置被篡改
- 异常操作

**解决方案:**

1. 启用认证:
```json
{
  "authentication": {
    "enabled": true,
    "jwt_secret": "生成随机密钥",
    "token_expiry": "1h"
  }
}
```

2. 配置 IP 白名单:
```json
{
  "security": {
    "allowed_ips": ["192.168.1.0/24"]
  }
}
```

---

## 快速诊断命令

```bash
# 系统状态
openclaw status

# 健康检查
openclaw health --verbose

# 查看日志
openclaw logs --tail 100

# 配置验证
openclaw config validate

# 工具测试
openclaw tools test <tool>

# 内存状态
openclaw memory stats

# 性能指标
openclaw metrics

# 网络诊断
openclaw diagnose network
```

---

## 常见问题速查

| 问题 | 快速解决方案 |
|------|-------------|
| 启动失败 | `openclaw logs` 查看日志 |
| 响应慢 | 检查 CPU/内存，启用缓存 |
| API 错误 | 验证 API Key 配置 |
| 连接超时 | 检查网络和代理设置 |
| 数据丢失 | 从备份恢复 |
| 权限错误 | 检查文件权限 |
