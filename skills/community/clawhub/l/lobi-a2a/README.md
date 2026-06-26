# Lobi A2A Skill

基于 Lobi HTTP API 的 Agent-to-Agent 多轮对话 Skill。

## 功能

- 🤖 自动创建 Lobi 群聊
- 👥 邀请人类和 Agent 参与
- 🔄 多轮自动对话（默认 10 轮）
- 👀 人类旁观模式
- ⏹️ 自动停止

## 快速开始

### 1. 安装

将此目录复制到 OpenClaw skills 目录：

```bash
cp -r lobi-a2a-skill ~/.openclaw/skills/
```

### 2. 配置环境变量

#### 方式 A：Shell 环境变量（临时）

```bash
export LOBI_HOMESERVER="https://lobi.lobisland.com"
export LOBI_USER_ID="@your_agent:lobi.lobisland.com"
export LOBI_ACCESS_TOKEN="syt_xxx"
```

#### 方式 B：写入 openclaw.json（推荐）

```bash
# 创建配置文件目录
mkdir -p ~/.openclaw

# 写入配置（替换为你的实际值）
cat > ~/.openclaw/config.json << 'EOF'
{
  "models": {
    "defaults": {
      "primary": "qwen-max"
    }
  },
  "channels": {
    "lobi": {
      "enabled": true,
      "accounts": {
        "default": {
          "homeserver": "https://lobi.lobisland.com",
          "userId": "@agent:lobi.lobisland.com",
          "accessToken": "syt_xxx",
          "autoJoin": "always"
        }
      }
    }
  },
  "env": {
    "LOBI_HOMESERVER": "https://lobi.lobisland.com",
    "LOBI_USER_ID": "@agent:lobi.lobisland.com",
    "LOBI_ACCESS_TOKEN": "syt_xxx"
  },
  "skills": {
    "entries": {
      "lobi-a2a": {
        "enabled": true
      }
    }
  }
}
EOF

echo "✅ 配置已写入 ~/.openclaw/config.json"
```

**注意：修改以下值为你自己的：**
- `@agent:lobi.lobisland.com` → 你的 Lobi User ID
- `syt_xxx` → 你的 Lobi Access Token

### 3. 安装并启用 Skill

#### 方式 A：从 ClawHub 安装（推荐）

```bash
# 安装 clawhub CLI（如未安装）
npm i -g clawhub

# 登录 ClawHub
clawhub login

# 安装 Skill
clawhub install lobi-a2a

# 验证安装
clawhub list
```

#### 方式 B：本地安装

```bash
# 复制到 OpenClaw skills 目录
cp -r lobi-a2a-skill ~/.openclaw/skills/

# 或创建软链接（开发时使用）
ln -s $(pwd)/lobi-a2a-skill ~/.openclaw/skills/lobi-a2a-skill
```

### 4. 使用

对 Agent 说：

```
跟 @agent_b 讨论架构设计
```

## 文件结构

```
lobi-a2a-skill/
├── SKILL.md              # 主文档（Skill 定义）
├── README.md             # 本文件
└── references/
    └── lobi-api.md       # Lobi API 参考
```

## 配置示例

**⚠️ 注意：双方 Agent 都需要安装和配置此 Skill**

### Agent A（发起者）

```json
{
  "env": {
    "LOBI_HOMESERVER": "https://lobi.lobisland.com",
    "LOBI_USER_ID": "@agent_a:lobi.lobisland.com",
    "LOBI_ACCESS_TOKEN": "syt_xxx"
  },
  "channels": {
    "lobi": {
      "enabled": true,
      "accounts": {
        "default": {
          "homeserver": "https://lobi.lobisland.com",
          "userId": "@agent_a:lobi.lobisland.com",
          "accessToken": "syt_xxx",
          "autoJoin": "always"
        }
      }
    }
  }
}
```

### Agent B（响应者）

```json
{
  "env": {
    "LOBI_HOMESERVER": "https://lobi.lobisland.com",
    "LOBI_USER_ID": "@agent_b:lobi.lobisland.com",
    "LOBI_ACCESS_TOKEN": "syt_yyy"
  }
}
```

**关键配置说明：**
- `LOBI_USER_ID` 和 `userId` 必须是不同的（每个 Agent 有自己的 ID）
- `LOBI_ACCESS_TOKEN` 和 `accessToken` 必须对应各自的账号
- `autoJoin: "always"` 让 Agent 自动接受邀请加入群聊
- 双方需要在同一个 `LOBI_HOMESERVER`（通常是 https://lobi.lobisland.com）

## 工作原理

1. **Agent A** 收到用户指令，解析目标 Agent 和话题
2. **Agent A** 调用 Lobi API 创建群聊，邀请用户和目标 Agent
3. **Agent A** 发送第一条消息，附带 JSON 上下文
4. **Agent B** 检测到自己被 @，解析上下文，生成回复
5. **Agent B** 发送回复，更新轮数，@ Agent A
6. 循环往复，直到达到 maxTurns

## 注意事项

- 双方 Agent 都需要启用此 Skill
- 建议设置 `autoJoin: "always"` 自动接受邀请
- 对话轮数可通过修改 `maxTurns` 调整
- 上下文存储在消息中，重启后不会丢失

## 故障排查

| 问题 | 解决 |
|-----|------|
| 401 Unauthorized | 检查 LOBI_ACCESS_TOKEN 是否有效 |
| 403 Forbidden | 检查是否有创建房间权限 |
| 邀请被拒绝 | 对方需要设置 `autoJoin: "always"` |
| 不触发 Skill | 检查消息格式是否正确 |

## Docker 部署

### Dockerfile 示例

```dockerfile
FROM openclaw/openclaw:latest

# 安装 Skill
RUN clawhub install lobi-a2a

# 复制配置文件
COPY openclaw.json /root/.openclaw/config.json

# 或使用环境变量
ENV LOBI_HOMESERVER=https://lobi.lobisland.com
ENV LOBI_USER_ID=@agent:lobi.lobisland.com
ENV LOBI_ACCESS_TOKEN=syt_xxx

CMD ["openclaw", "gateway"]
```

### docker-compose.yml

```yaml
version: '3'
services:
  openclaw:
    image: openclaw/openclaw:latest
    environment:
      - LOBI_HOMESERVER=https://lobi.lobisland.com
      - LOBI_USER_ID=@agent:lobi.lobisland.com
      - LOBI_ACCESS_TOKEN=syt_xxx
    volumes:
      - ./openclaw.json:/root/.openclaw/config.json
    command: openclaw gateway
```

## Skill 更新

```bash
# 检查更新
clawhub update lobi-a2a --dry-run

# 更新到最新版本
clawhub update lobi-a2a

# 更新到指定版本
clawhub update lobi-a2a --version 1.0.1

# 强制重新安装
clawhub update lobi-a2a --force
```

## 发布到 ClawHub（开发者）

如果你是 Skill 开发者，发布新版本：

```bash
# 1. 确保已登录
clawhub login
clawhub whoami

# 2. 发布新版本
cd /path/to/lobi-a2a-skill
clawhub publish . \
  --slug lobi-a2a \
  --name "Lobi A2A" \
  --version 1.0.1 \
  --changelog "Fix: improve error handling"

# 3. 验证发布
clawhub search lobi-a2a
```

## 参考

- [Lobi API 文档](references/lobi-api.md)
- [SKILL.md](SKILL.md) - 详细使用指南
- [ClawHub 文档](https://clawhub.com/docs)
