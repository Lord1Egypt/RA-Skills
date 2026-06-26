# Multi-Agent Deploy 🦞

快速部署新的 assistant agent，编号递增，自动配置。

## 功能

- ✅ 自动检测下一个可用编号（assistant1, assistant2, assistant3...）
- ✅ 复制模板工作空间（SOUL.md, AGENTS.md, USER.md）
- ✅ 创建 agent 目录结构
- ✅ 自动更新 openclaw.json 配置
- ✅ 一键部署，无需手动编辑

## 安装

```bash
clawhub install multi-agent-deploy
```

## 使用

### 命令行直接运行

```bash
python3 /home/admin/.openclaw/workspace/skills/multi-agent-deploy/scripts/deploy-agent.py
```

### 通过 AI 助手

直接说：
- 「新增一个 agent」
- 「创建 assistant3」
- 「加一个日常助手」

## 输出示例

```
🦞 创建新的 Assistant Agent #3
----------------------------------------
✓ 创建：SOUL.md
✓ 创建：AGENTS.md
✓ 创建：USER.md
✓ 创建 agent 目录：/home/admin/.openclaw/agents/assistant3/agent
✓ 更新配置：/home/admin/.openclaw/openclaw.json
  - Agent ID: assistant3
  - Name: 日常助手 3
  - Workspace: /home/admin/.openclaw/workspace-assistant3
----------------------------------------
✅ 完成！新 Agent 已就绪
   重启 Gateway 生效：openclaw gateway restart
```

## 依赖

- Python 3.6+
- OpenClaw
- 模板工作空间：`workspace-assistant`

## 迁移到其他服务器

```bash
# 1. 安装技能
clawhub install multi-agent-deploy

# 2. 确认模板工作空间存在
ls /home/admin/.openclaw/workspace-assistant/

# 3. 运行部署
python3 skills/multi-agent-deploy/scripts/deploy-agent.py
```

## License

MIT
