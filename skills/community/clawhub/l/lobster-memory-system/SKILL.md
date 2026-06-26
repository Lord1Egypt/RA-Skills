---
name: lobster-memory-system
description: 龙虾记忆体系统 - 模块化、版本化、自动备份的 AI 记忆管理方案
version: "1.0.0"
author: Alan & 麻小
type: skill
tags: [memory, backup, persistence, lobster, openclaw]
homepage: https://github.com/openclaw/lobster-memory-system
license: MIT
---

# 🦞 Lobster Memory System (龙虾记忆体)

**模块化、版本化、自动备份的 AI 记忆管理方案**

专为 OpenClaw/Clawdbot 设计的记忆系统，让 AI 助手拥有持续的记忆能力和自我改进机制。

---

## ✨ 特性

- 📦 **模块化设计** - CORE/MEMORY/CONFIG/SKILLS 分离
- 🔄 **自动备份** - 每日 18:00 自动备份，支持 Windows 任务计划
- 📊 **分层记忆** - 长期记忆 + 短期记忆 + 核心身份
- 🧠 **智能加载** - 首次会话全量加载，后续按需加载
- 📈 **自我改进** - 心跳检查 + 周报生成
- 🔒 **安全架构** - 权限控制 + 敏感数据保护

---

## 📦 安装

### 方式 1：ClawHub 安装（推荐）
```bash
clawdhub install lobster-memory-system
```

### 方式 2：手动安装
```bash
# 1. 下载技能包
# 2. 解压到 ~/.openclaw/skills/lobster-memory-system
# 3. 运行初始化脚本
powershell -ExecutionPolicy Bypass -File ~/.openclaw/skills/lobster-memory-system/scripts/init.ps1
```

---

## 🚀 快速开始

### 1. 初始化记忆系统
```powershell
cd ~/.openclaw/skills/lobster-memory-system
powershell -ExecutionPolicy Bypass -File scripts/init.ps1
```

### 2. 配置自动备份
```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup-auto-backup.ps1
```

### 3. 配置心跳检查
编辑工作区的 `HEARTBEAT.md`：
```markdown
## 🔄 自我改进检查
- 分析最近任务的用户反馈
- 记录需要改进的点
- 每周日生成周报
```

---

## 📁 目录结构

```
memory-system/
├── CORE/                    # 核心身份（每次必加载）
│   ├── identity.json        # AI 身份信息
│   ├── soul.md             # 人格设定
│   └── constraints.md      # 行为约束
├── MEMORY/                  # 记忆数据
│   ├── long-term/          # 长期记忆
│   │   ├── preferences.json
│   │   ├── knowledge.json
│   │   ├── people.json
│   │   └── projects.json
│   └── short-term/         # 短期记忆（每日）
│       └── YYYY-MM-DD.json
├── CONFIG/                  # 配置数据
│   ├── channels.json       # 频道配置
│   ├── tools.json          # 工具配置
│   └── permissions.json    # 权限控制
├── SKILLS/                  # 技能注册表
│   └── registry.json
├── SNAPSHOTS/              # 自动备份
│   └── auto-backup-YYYYMMDD.zip
├── scripts/                 # 工具脚本
│   ├── init.ps1            # 初始化
│   ├── check-first-session.ps1
│   ├── auto-backup.ps1
│   └── setup-auto-backup.ps1
└── README.md               # 本文档
```

---

## 🔄 工作流程

### 首次会话（每天）
```
1. 运行 check-first-session.ps1
2. 如果是首次 → 加载全部记忆
3. 更新追踪器 (session-tracker.json)
4. 设置 fullMemoryLoaded = true
```

### 其他会话
```
1. 只加载 CORE/identity.json
2. 加载 preferences.json
3. 加载当日短期记忆
```

### 自动备份（每日 18:00）
```
1. 压缩 CORE + MEMORY + CONFIG + SKILLS
2. 保存到 SNAPSHOTS/auto-backup-YYYYMMDD.zip
3. 记录备份日志
```

---

## 📊 记忆加载策略

| 会话类型 | 加载内容 | 用途 |
|---------|---------|------|
| **首次会话** | 全部记忆文件 | 完整上下文 |
| **其他会话** | CORE + 偏好 + 今日 | 快速启动 |
| **按需加载** | memory_search 工具 | 历史查询 |

---

## 🛠️ 工具脚本

### check-first-session.ps1
检查是否是今日首次会话，返回 true/false。

### auto-backup.ps1
执行完整备份，可手动运行或通过任务计划自动执行。

### setup-auto-backup.ps1
配置 Windows 任务计划，设置每日 18:00 自动备份。

### init.ps1
初始化记忆系统，创建目录结构和示例文件。

---

## 🔧 配置示例

### identity.json
```json
{
  "name": "麻小",
  "creature": "AI 助手",
  "vibe": "正式且带点幽默",
  "emoji": "🦞",
  "version": "1.0.0"
}
```

### preferences.json
```json
{
  "replyStyle": "简洁，不要包含错误输出",
  "imageSending": "直接发送图片文件",
  "timezone": "Asia/Shanghai"
}
```

---

## 📈 自我改进系统

集成 self-improving-agent 技能，实现：

- **心跳检查** - 每 30-60 分钟分析最近任务
- **改进日志** - 记录到 `memory/improvement_log.md`
- **周报生成** - 每周日汇总改进点
- **SOUL 建议** - 根据学习成果建议更新人格

---

## 🔒 安全特性

- **权限控制** - CONFIG/permissions.json 定义访问权限
- **敏感数据保护** - 不输出 API Key、私钥等
- **备份加密** - 可选加密备份文件
- **审计日志** - 记录所有记忆访问

---

##  与 Markdown 记忆对比

| 特性 | Lobster 记忆体 | Markdown 记忆 |
|------|--------------|-------------|
| 结构化 | ✅ JSON + 目录 | ⚪ 纯文本 |
| 自动备份 | ✅ 每日自动 | ⚪ 手动 |
| 版本控制 | ✅ 快照管理 | ⚪ Git |
| 按需加载 | ✅ 智能策略 | ⚪ 全文加载 |
| 自我改进 | ✅ 集成系统 | ⚪ 手动记录 |

---

## 🐛 故障排除

### 备份失败
```powershell
# 检查任务计划
Get-ScheduledTask -TaskName "LobsterMemoryBackup"

# 手动运行备份
powershell -File scripts/auto-backup.ps1
```

### 记忆加载异常
```powershell
# 修复记忆系统
powershell -File scripts/repair-memory.ps1
```

### 首次会话检测失败
```powershell
# 重置会话追踪器
Remove-Item session-tracker.json
```

---

## 📝 更新日志

### v1.0.0 (2026-04-21)
- ✅ 初始版本发布
- ✅ 模块化记忆结构
- ✅ 自动备份系统
- ✅ 心跳检查集成
- ✅ 自我改进系统

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

## 📄 许可证

MIT License - 让所有龙虾都拥有优秀的记忆力！🦞
