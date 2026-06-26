---
name: multi-bot-deploy
description: OpenClaw 多 Bot 多 Agent 一键搭建技能。根据用户提供的 Bot 名称、职能、模型和飞书凭证，自动完成 Agent 创建、账号配置、路由绑定和验证测试全流程。
allowed-tools: Bash(openclaw:*), Bash(cp:*), Bash(date:*), Bash(mkdir:*)
---

# OpenClaw 多 Bot 多 Agent 一键搭建技能

## 功能特性

- 🚀 一键创建多 Bot 多 Agent 配置
- 📝 自动解析用户需求（Bot 名称、职能、模型）
- 🔐 自动填入飞书 appId 和 appSecret
- ✅ 自动验证配置并测试
- 📊 输出配置摘要和验证结果

## 指令格式

```
新建 Bot: <名称>
职能：<描述>
模型：<可选，默认 bailian/qwen3.5-plus>
appId: <飞书 App ID>
appSecret: <飞书 App Secret>
```

## 自动化流程

### 1️⃣ 解析输入

从用户输入中提取：
- **Bot 名称** → 生成 agentId（小写 + 连字符）+ 显示名称
- **职能描述** → 生成 workspace 路径
- **模型偏好** → model.primary（默认 `bailian/qwen3.5-plus`）
- **appId/appSecret** → 直接填入配置

### 2️⃣ 执行 5 步指令

#### 步骤 1：备份配置
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak_$(date +%Y%m%d_%H%M%S)
```

#### 步骤 2：创建 Agent
```bash
openclaw agents add <agent-id> \
  --workspace /root/.openclaw/workspace-<agent-id> \
  --model <model-id> \
  --non-interactive
```

#### 步骤 3：添加飞书账号 + 填入凭证
```bash
openclaw channels add \
  --channel feishu \
  --account <agent-id> \
  --name "<显示名称>"

openclaw config set "channels.feishu.accounts.<agent-id>.appId" "<appId>"
openclaw config set "channels.feishu.accounts.<agent-id>.appSecret" "<appSecret>"
```

#### 步骤 4：绑定路由
```bash
openclaw agents bind \
  --agent <agent-id> \
  --bind "feishu:<agent-id>"
```

#### 步骤 5：重启 + 验证
```bash
openclaw gateway restart
openclaw agents list
openclaw config get bindings
```

### 3️⃣ 输出验证结果

- ✅ `agents list` 确认新增成功
- ✅ `bindings` 确认路由正确
- 📧 发送测试消息确认 Bot 响应

---

## 📝 使用示例

### 示例 1：创建产品助理 Bot

**用户输入：**
```
新建 Bot: lukas-product
职能：产品助理
模型：bailian/qwen3.5-plus
appId: cli_xxx
appSecret: XXXXXXXXXXXXXXXXXXXX
```

**技能执行：**

```bash
# 1️⃣ 备份
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak_20260312_120000

# 2️⃣ 创建 Agent
openclaw agents add product-assistant \
  --workspace /root/.openclaw/workspace-product \
  --model bailian/qwen3.5-plus \
  --non-interactive

# 3️⃣ 添加飞书账号 + 凭证
openclaw channels add \
  --channel feishu \
  --account product-assistant \
  --name "Lukas-产品助理"

openclaw config set "channels.feishu.accounts.product-assistant.appId" "cli_xxxxx"
openclaw config set "channels.feishu.accounts.product-assistant.appSecret" "xxxxxxxx"

# 4️⃣ 绑定路由
openclaw agents bind \
  --agent product-assistant \
  --bind "feishu:product-assistant"

# 5️⃣ 重启 + 验证
openclaw gateway restart
openclaw agents list
openclaw config get bindings
```

**输出摘要：**
```markdown
## ✅ 多 Bot 多 Agent 搭建完成

### 配置摘要
| 项目 | 值 |
|------|-----|
| Agent ID | product-assistant |
| 显示名称 | Lukas-产品助理 |
| Workspace | /root/.openclaw/workspace-product |
| 模型 | bailian/qwen3.5-plus |
| 飞书账号 | product-assistant |

### 验证结果
- ✅ Agent 创建成功
- ✅ 飞书账号配置成功
- ✅ 路由绑定成功
- ✅ Gateway 重启成功

### 下一步
1. 在飞书添加 Bot「Lukas-产品助理」
2. 发送测试消息确认响应
```

---

### 示例 2：创建开发助手 Bot

**用户输入：**
```
新建 Bot: dev-helper
职能：代码审查和技术问答
模型：bailian/qwen3-coder-plus
appId: cli_aXXXXXXXXXXXXXX
appSecret: XXXXXXXXXXXXXXXXXXXX
```

**技能执行：**
```bash
# agentId 自动生成：dev-helper
openclaw agents add dev-helper \
  --workspace /root/.openclaw/workspace-dev-helper \
  --model bailian/qwen3-coder-plus \
  --non-interactive

openclaw channels add \
  --channel feishu \
  --account dev-helper \
  --name "Dev-Helper"

openclaw config set "channels.feishu.accounts.dev-helper.appId" "cli_aXXXXXXXXXXXXXX"
openclaw config set "channels.feishu.accounts.dev-helper.appSecret" "XXXXXXXXXXXXXXXXXXXX"

openclaw agents bind \
  --agent dev-helper \
  --bind "feishu:dev-helper"

openclaw gateway restart
```

---

## 🎯 命名规范

| 项目 | 规范 | 示例 |
|------|------|------|
| **agentId** | 小写 + 连字符 | `product-assistant` |
| **workspace** | `/root/.openclaw/workspace-<id>` | `workspace-product` |
| **accountId** | 与 agentId 一致 | `product-assistant` |
| **显示名称** | 可读性优先 | `Lukas-产品助理` |

---

## ⚠️ 注意事项

### 安全提示
1. **凭证安全**：appSecret 是敏感信息，不要明文分享
2. **备份配置**：操作前自动备份 `openclaw.json`
3. **权限最小化**：飞书应用只配置必要权限

### 技术提示
1. **agentId 唯一性**：不能与现有 Agent 重复
2. **workspace 路径**：确保有写入权限
3. **路由优先级**：精确规则在前，兜底规则在后
4. **重启生效**：配置修改后必须 `gateway restart`

---

## 🔧 故障排查

### 问题 1：Agent 创建失败
```bash
# 检查 agentId 是否重复
openclaw agents list

# 检查 workspace 路径权限
ls -la /root/.openclaw/
```

### 问题 2：飞书账号配置失败
```bash
# 检查 appId/appSecret 格式
openclaw config get channels.feishu.accounts

# 验证凭证是否正确
openclaw gateway logs
```

### 问题 3：路由绑定失败
```bash
# 检查现有绑定
openclaw config get bindings

# 手动添加绑定
openclaw agents bind --agent <id> --bind "feishu:<account>"
```

### 问题 4：Bot 无响应
```bash
# 检查 Gateway 状态
openclaw gateway status

# 查看日志
openclaw gateway logs

# 检查飞书应用权限
# 确保已配置：机器人、消息、群组读写
```

---

## 📚 相关文档

- [OpenClaw 官方文档 - Agents](https://docs.openclaw.ai/cli/agents)
- [OpenClaw 官方文档 - Channels](https://docs.openclaw.ai/cli/channels)
- [飞书开放平台](https://open.feishu.cn/document)

---

## 🚀 快速开始

直接发送指令：
```
新建 Bot: <名称>
职能：<描述>
模型：<可选>
appId: <xxx>
appSecret: <xxx>
```

技能自动完成全流程配置！
