# Gateway 配置指南片段

> 摘录自 `gateway/configuration.md` + `gateway/configuration-reference.md`

---

## 配置文件位置

- **主配置**：`~/.openclaw/openclaw.json`
- **环境变量**：`.env` 文件（加载顺序优先级最高）
- **Skills 配置**：`~/.openclaw/skills/<skill-name>/config.yaml`

---

## openclaw.json 核心结构

```json
{
  "gateway": {
    "host": "127.0.0.1",
    "port": 18789,
    "auth": {
      "type": "token",
      "token": "<48-hex-token>"
    }
  },
  "agents": {
    "defaults": {
      "models": ["anthropic/claude-sonnet-4-7"]
    }
  },
  "channels": {
    "discord": {
      "enabled": true,
      "token": "<bot-token>"
    }
  }
}
```

---

## 关键配置项

### Gateway Host/Port

```bash
# 查看当前配置
openclaw config get gateway.host
openclaw config get gateway.port

# 修改
openclaw config set gateway.host 0.0.0.0
openclaw config set gateway.port 18789
```

### 认证 Token

```bash
# 生成新 token
openclaw gateway token --length 48

# 查看当前 token
openclaw config get gateway.auth.token
```

### 模型配置

```bash
# 查看可用模型
openclaw models list

# 设置默认模型
openclaw config set agents.defaults.models '["anthropic/claude-sonnet-4-7"]'

# 设置回退模型
openclaw config set agents.defaults.fallback '["openai/gpt-4o"]'
```

### 通道启用

```bash
# 查看已配置通道
openclaw channels status

# 探活所有通道
openclaw channels status --probe
```

---

## 配置验证

```bash
# 启动前验证配置
openclaw doctor

# 启动 gateway
openclaw gateway start

# 查看运行状态
openclaw gateway status
```

---

## Skill 配置

```bash
# 查看 skills 配置
openclaw skills list

# 查看 skill 详情
openclaw skills get <skill-name>
```

---

## 环境变量配置（.env）

```bash
# 常用环境变量
OPENCLAW_HOST=127.0.0.1
OPENCLAW_PORT=18789
OPENCLAW_GATEWAY_TOKEN=<token>
ANTHROPIC_API_KEY=sk-...
OPENAI_API_KEY=sk-...
```

---

## 配置示例

完整配置示例见：`https://docs.openclaw.ai/gateway/configuration-examples`

常见场景：
- [单通道最小配置](https://docs.openclaw.ai/gateway/configuration-examples#minimal)
- [多通道配置](https://docs.openclaw.ai/gateway/configuration-examples#multi-channel)
- [远程访问配置](https://docs.openclaw.ai/gateway/configuration-examples#remote)
