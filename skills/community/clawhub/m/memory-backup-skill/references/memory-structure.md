# 记忆分层结构参考

## 整体架构

```
memory/
├── MEMORY.md              ← 长期核心记忆（仅主会话读取）
├── SOUL.md                ← AI 人格设定
├── USER.md                ← 用户基本信息
├── TOOLS.md               ← 本地工具配置与凭据
├── IDENTITY.md            ← AI 身份设定
├── HEARTBEAT.md           ← 心跳检查任务模板
│
├── YYYY-MM-DD.md          ← 每日日记（所有渠道共享的核心上下文）
│
├── core/                  ← 跨渠道共享的核心能力与经验
│   ├── capabilities.md     ← AI 已掌握的能力清单
│   ├── environments.md     ← 已对接的环境配置
│   └── validated-workflows.md  ← 已验证的工作流
│
├── channels/               ← 按渠道隔离的上下文
│   ├── feishu/            ← 飞书专用
│   ├── wechat/            ← 微信专用
│   ├── telegram/          ← Telegram 专用
│   └── ...                ← 其他渠道按需创建
│
├── projects/              ← 项目级记忆（跨渠道共享）
│   └── _TEMPLATE.md       ← 项目记忆模板
│
└── scripts/               ← （注意：脚本放 workspace 根目录 scripts/）
```

## 核心原则

1. **跨渠道共享** → 写 `memory/core/` 或 `memory/projects/`
2. **渠道私有** → 写 `memory/channels/<渠道名>/`
3. **每日上下文** → 写 `memory/YYYY-MM-DD.md`
4. **敏感凭据** → 只写状态/位置，不写实际密钥，存 `TOOLS.md`

## 记忆文件说明

### MEMORY.md
- 仅主会话（direct chat）读取，**不在群聊/共享上下文加载**
- 存放下述内容：
  - 用户的长期偏好、习惯
  - 重要决策结论
  - 项目关键上下文
  - 已验证的配置和经验

### memory/YYYY-MM-DD.md
- 每日日记，包含当天所有重要讨论、项目进展、决策结论
- 所有渠道共享读取
- 每日结束时自动沉淀（由 AI 主动写入）

### memory/channels/<渠道>/
- 该渠道私有的上下文
- 例如微信渠道的独特偏好、只在微信讨论的项目
- 与其他渠道的记忆互补，不重复记录已存信息

## 备份策略

- 核心记忆文件（见 `memory-backup.sh` 的 `TRACKED_PATHS`）每日自动备份到 Git 远程仓库
- `TOOLS.md` 不含实际密钥，仅记录配置位置和状态
- 备份脚本：`bash scripts/memory-backup.sh`
