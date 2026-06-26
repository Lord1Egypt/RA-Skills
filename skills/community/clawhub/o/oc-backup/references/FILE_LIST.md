# OpenClaw 备份文件清单说明

本文档详细说明 OpenClaw 备份技能所包含的文件和目录。

## 目录结构概览

```
~/.openclaw/                          # OpenClaw 根目录
├── openclaw.json                     # 主配置文件
├── .env                              # 环境变量（敏感）
├── exec-approvals.json               # 执行审批配置
├── gateway.cmd                       # Gateway 启动脚本
├── workspace/                        # 工作空间
│   ├── AGENTS.md                     # 工作空间指南
│   ├── SOUL.md                       # AI 人格定义
│   ├── USER.md                       # 用户信息
│   ├── IDENTITY.md                   # 身份定义
│   ├── TOOLS.md                      # 工具配置
│   ├── HEARTBEAT.md                  # 心跳配置
│   ├── MEMORY.md                     # 长期记忆
│   └── skills/                       # 技能目录
│       └── {skill-name}/             # 单个技能
├── cron/                             # 定时任务配置
├── devices/                          # 设备配置
└── memory/                           # 记忆数据
```

---

## 1. 系统配置文件

### 1.1 openclaw.json

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/openclaw.json` |
| 必需性 | ✅ 必需 |
| 敏感性 | ❌ 非敏感 |
| 说明 | OpenClaw 主配置文件，包含模型设置、认证信息、网关配置等核心设置 |

**典型内容**:
```json
{
  "model": "dashscope-coding-plan/glm-5",
  "gateway": {
    "port": 3000,
    "remote": {
      "url": "https://gateway.example.com"
    }
  },
  "auth": {
    "provider": "openclaw"
  }
}
```

### 1.2 .env

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/.env` |
| 必需性 | ✅ 必需 |
| 敏感性 | ⚠️ **敏感** - 包含 API 密钥 |
| 说明 | 环境变量文件，存储 API 密钥、令牌等敏感信息 |

**典型内容**:
```env
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
# 其他 API 密钥...
```

⚠️ **注意**: 此文件包含敏感信息，备份时会在清单中标记，请妥善保管备份文件。

### 1.3 exec-approvals.json

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/exec-approvals.json` |
| 必需性 | 🟡 可选 |
| 敏感性 | ❌ 非敏感 |
| 说明 | 执行审批配置，记录哪些命令需要审批 |

**典型内容**:
```json
{
  "approved": ["npm install", "git status"],
  "denied": ["rm -rf /"]
}
```

### 1.4 gateway.cmd

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/gateway.cmd` |
| 必需性 | 🟡 可选 |
| 敏感性 | ❌ 非敏感 |
| 说明 | Gateway 启动脚本，定义如何启动 OpenClaw Gateway 服务 |

---

## 2. Workspace 核心文件

### 2.1 AGENTS.md

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/workspace/AGENTS.md` |
| 必需性 | ✅ 必需 |
| 说明 | 工作空间指南，定义 AI 的行为准则、记忆规则、安全边界等 |

**核心内容**:
- 首次运行指南
- 每日会话流程
- 记忆管理规则
- 安全约束
- 群聊行为规范
- 心跳处理逻辑

### 2.2 SOUL.md

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/workspace/SOUL.md` |
| 必需性 | ✅ 必需 |
| 说明 | AI 人格定义，定义 AI 的核心特质、边界和风格 |

**核心内容**:
- 核心原则
- 边界设定
- 沟通风格
- 持续性规则

### 2.3 USER.md

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/workspace/USER.md` |
| 必需性 | ✅ 必需 |
| 说明 | 用户信息，定义 AI 的主人、时区等基本信息 |

**典型内容**:
```markdown
# USER.md - About Your Human

- **Name:** 用户名
- **Timezone:** Asia/Shanghai (GMT+8)
```

### 2.4 IDENTITY.md

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/workspace/IDENTITY.md` |
| 必需性 | ✅ 必需 |
| 说明 | 身份定义，定义 AI 的名称、形象和性格特点 |

**典型内容**:
- AI 名称和形象
- 性格特点
- 能力亮点
- 核心原则

### 2.5 TOOLS.md

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/workspace/TOOLS.md` |
| 必需性 | 🟡 可选 |
| 说明 | 工具配置，记录特定环境的配置信息 |

**典型内容**:
- 摄像头名称和位置
- SSH 主机和别名
- TTS 语音偏好
- 其他环境特定配置

### 2.6 HEARTBEAT.md

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/workspace/HEARTBEAT.md` |
| 必需性 | 🟡 可选 |
| 说明 | 心跳配置，定义定期检查的任务 |

**典型内容**:
- 待检查事项清单
- 定期任务定义

### 2.7 MEMORY.md

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/workspace/MEMORY.md` |
| 必需性 | 🟡 可选 |
| 说明 | 长期记忆，存储 AI 的持久化记忆 |

**典型内容**:
- 重要事件记录
- 用户偏好
- 学到的经验教训

---

## 3. Skills 目录

### 3.1 目录结构

```
~/.openclaw/workspace/skills/
├── {skill-name-1}/
│   ├── SKILL.md              # 技能定义（必需）
│   ├── scripts/              # 脚本目录（可选）
│   │   ├── main.js
│   │   └── helper.js
│   ├── references/           # 参考文档（可选）
│   │   └── guide.md
│   ├── config/               # 配置文件（可选）
│   │   └── config.json
│   └── data/                 # 数据目录（可选）
│       └── .gitkeep
└── {skill-name-2}/
    └── ...
```

### 3.2 SKILL.md 规范

每个技能目录必须包含 `SKILL.md` 文件，包含：

- 技能名称和描述
- 触发条件
- 使用说明
- 依赖说明

---

## 4. 其他重要数据

### 4.1 cron/ 目录

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/cron/` |
| 必需性 | 🟡 可选 |
| 说明 | 定时任务配置目录 |

**典型内容**:
- 定时任务定义文件
- 定时任务状态文件

### 4.2 devices/ 目录

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/devices/` |
| 必需性 | 🟡 可选 |
| 说明 | 设备配置目录，存储已配对设备的信息 |

**典型内容**:
- 设备配置文件
- 设备认证信息

### 4.3 memory/ 目录

| 属性 | 值 |
|------|-----|
| 路径 | `~/.openclaw/memory/` |
| 必需性 | 🟡 可选 |
| 说明 | 记忆数据目录，存储每日记忆日志 |

**典型内容**:
- `YYYY-MM-DD.md` 每日记忆文件
- `heartbeat-state.json` 心跳状态

---

## 5. 备份输出结构

### 5.1 备份包内部结构

```
openclaw-backup-{type}-{timestamp}.tar.gz
└── openclaw-backup/
    ├── manifest.json           # 备份元数据
    ├── system/                 # 系统配置
    │   ├── openclaw.json
    │   ├── .env
    │   ├── exec-approvals.json
    │   └── gateway.cmd
    ├── workspace/              # 核心文件
    │   ├── AGENTS.md
    │   ├── SOUL.md
    │   ├── USER.md
    │   ├── IDENTITY.md
    │   ├── TOOLS.md
    │   ├── HEARTBEAT.md
    │   └── MEMORY.md
    ├── skills/                 # 技能目录
    │   └── {skill-name}/
    ├── cron/                   # 定时任务
    ├── devices/                # 设备配置
    └── memory/                 # 记忆数据
```

### 5.2 备份清单格式

备份时生成的 JSON 清单包含：

```json
{
  "version": "1.0.0",
  "backupType": "full",
  "timestamp": "2026-03-27T08:45:00+08:00",
  "hostname": "user-machine",
  "platform": "win32",
  "backupFile": "openclaw-backup-full-20260327-084500.tar.gz",
  "backupSize": 1048576,
  "backupSizeHuman": "1.00 MB",
  "duration": 1.5,
  "summary": {
    "totalFiles": 25,
    "successCount": 23,
    "skippedCount": 2,
    "totalSize": 2097152
  },
  "categories": {
    "system": { ... },
    "workspace": { ... },
    "skills": { ... }
  }
}
```

---

## 6. 不备份的文件

以下文件/目录不会被备份：

| 文件/目录 | 原因 |
|-----------|------|
| `logs/` | 日志文件体积大且可重新生成 |
| `tmp/` | 临时文件无长期保存价值 |
| `cache/` | 缓存可重新生成 |
| `node_modules/` | 可通过 npm install 重新安装 |
| `.git/` | 版本控制数据，通常不需要备份 |

---

## 7. 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.0.0 | 2026-03-27 | 初始版本 |

---

*本文档由 OpenClaw Backup Skill 自动维护*