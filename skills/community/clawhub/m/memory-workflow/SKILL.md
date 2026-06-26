---
name: memory-workflow
description: 记忆管理工作流 - 会话读档、每日摘要、实时写入，解决 AI 助手"失忆"问题
homepage: https://github.com/openclaw/openclaw
metadata: {
  "clawdbot": {
    "emoji": "📒",
    "requires": {
      "bins": ["bash", "cron"]
    },
    "install": [
      {
        "id": "setup",
        "kind": "script",
        "label": "配置记忆管理工作流"
      }
    ]
  }
}
---

# Memory Workflow - 记忆管理工作流

> 解决 AI 助手"失忆"问题的完整工作流方案，包含会话读档、每日摘要、实时写入三大核心机制。
> 
> **版本：** 1.0.0
> 
> **作者：** 小吴 (ENFP 快乐小狗)
> 
> **参考来源：** 小让 (Xiao Rang) 的"外挂硬盘"系统经验

---

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| **会话读档** | 新会话启动时自动读取记忆文件，确保记忆连续性 |
| **每日摘要** | 每天定时自动创建/更新当日笔记，5 分钟超时机制 |
| **实时写入** | 重要信息获取后即时询问并写入记忆文件 |
| **记忆维护** | 每周回顾清理过期信息，保持记忆精简 |

---

## 🚀 快速开始

### 1. 安装后自动配置

安装完成后，运行配置脚本：

```bash
/root/.openclaw/workspace/skills/memory-workflow/scripts/install.sh
```

### 2. 配置项（可选）

编辑配置文件 `~/.openclaw/workspace/.memory-workflow-config`：

```bash
# 每日摘要时间（默认 23:00）
DAILY_SUMMARY_HOUR=23

# 超时等待时间（默认 5 分钟）
SUMMARY_TIMEOUT_MINUTES=5

# 读档频率（默认：new_session_only）
# 选项：new_session_only | every_message
ARCHIVE_FREQUENCY=new_session_only

# 保留每日笔记天数（默认 7 天）
KEEP_DAYS=7
```

---

## 📖 工作机制

### 一、会话读档机制

**触发时机：**
- 新会话启动（每天第一次对话、系统重启、会话超时后重新连接）
- 同一会话内的多轮对话不重复读取（依靠上下文窗口）

**读取内容：**
| 文件 | 优先级 | 内容 |
|------|-------|------|
| `MEMORY.md` | ⭐⭐⭐ | 核心身份、重要渠道、偏好、待办事项 |
| `memory/YYYY-MM-DD.md`（今日） | ⭐⭐ | 当天已记录的对话摘要 |
| `memory/YYYY-MM-DD.md`（最近 3 天） | ⭐⭐ | 最近几天的重要事件 |

**读档后动作：**
1. 确认记忆恢复：主动告诉用户"已读档，记忆恢复"
2. 检查待办事项：查看 MEMORY.md 中的待办列表
3. 准备上下文：准备好继续之前的话题

---

### 二、每日摘要机制

**自动化流程：**

| 时间 | 动作 | 说明 |
|------|------|------|
| **配置时间** | cron 创建标记文件 | `.daily-summary-pending` + 时间戳 |
| **配置时间 + 5 分钟** | 等待用户补充 | 如果用户手动创建笔记，删除标记 |
| **超时后** | 自动执行 | 如果标记还在，自动创建基础模板 |

**脚本位置：**
- **脚本：** `/root/.openclaw/workspace/skills/memory-workflow/scripts/daily-summary.sh`
- **日志：** `/root/.openclaw/workspace/logs/daily-summary.log`
- **输出：** `memory/YYYY-MM-DD.md`

**每日笔记模板：**
```markdown
# YYYY-MM-DD - 每日摘要

## 📋 今日重点
_待填充..._

## 💬 重要对话
_待填充..._

## 🎯 关键决策
_待填充..._

## 📝 待办更新
_待填充..._

---
*自动生成时间：YYYY-MM-DD HH:MM:SS*
*记录者：[助手名称]*
```

---

### 三、实时写入机制

**触发场景：**
| 场景 | 动作 |
|------|------|
| 用户告诉我新偏好/设定 | 立即询问："要写入 MEMORY.md 吗？" |
| 重要决策完成 | 立即记录到 MEMORY.md 待办事项 |
| 新渠道/技能发现 | 立即更新 MEMORY.md 相关章节 |
| 投资调整 | 立即更新 MEMORY.md 持仓表格 |

**写入规则：**
1. **先询问**：重要信息先问用户是否写入
2. **即时写**：确认后立刻写入，不拖延
3. **双备份**：核心信息写 MEMORY.md，详细信息写每日笔记

---

### 四、记忆维护机制

**每周回顾（每周日 22:00）：**
- 回顾 MEMORY.md
- 清理过时的待办事项
- 更新重要信息
- 删除失效的链接/渠道

**精简原则：**
- MEMORY.md 保持精简（核心信息）
- 详细信息归档到 memory/每日笔记
- 定期（每周）回顾，删除过时信息

---

## 📁 文件结构

```
/root/.openclaw/workspace/
├── MEMORY.md                          # 长期记忆（核心信息）
├── .memory-workflow-config            # 工作流配置（可选）
├── .daily-summary-pending             # 每日摘要待处理标记（自动）
├── .daily-summary-timestamp           # 每日摘要时间戳（自动）
├── skills/memory-workflow/
│   ├── SKILL.md                       # 本技能文档
│   ├── scripts/
│   │   ├── install.sh                 # 安装配置脚本
│   │   ├── daily-summary.sh           # 每日摘要脚本
│   │   └── weekly-review.sh           # 每周回顾脚本（可选）
│   └── templates/
│       └── daily-note-template.md     # 每日笔记模板
├── memory/
│   ├── YYYY-MM-DD.md                  # 每日笔记
│   └── portfolio.md                   # 持仓清单（可选）
└── logs/
    └── daily-summary.log              # 每日摘要执行日志
```

---

## ⚙️ 配置选项

### 环境变量

| 变量 | 默认值 | 说明 |
|------|-------|------|
| `DAILY_SUMMARY_HOUR` | 23 | 每日摘要执行时间（小时） |
| `SUMMARY_TIMEOUT_MINUTES` | 5 | 等待用户补充的超时时间（分钟） |
| `ARCHIVE_FREQUENCY` | new_session_only | 读档频率（new_session_only / every_message） |
| `KEEP_DAYS` | 7 | 保留每日笔记的天数 |

### cron 配置

安装时自动添加 cron 任务：

```bash
# 每分钟检查一次（用于超时机制）
*/1 * * * * /root/.openclaw/workspace/skills/memory-workflow/scripts/daily-summary.sh >> /root/.openclaw/workspace/logs/daily-summary.log 2>&1
```

---

## 🎯 关键指标

| 指标 | 目标值 | 检查方式 |
|------|-------|---------|
| 会话启动读档率 | 100% | 每次新会话检查 |
| 每日摘要创建率 | 100% | cron 自动执行 |
| 重要信息写入延迟 | < 5 分钟 | 用户确认后即时写入 |
| 每周回顾执行率 | 100% | 每周日检查 |

---

## 🔧 故障排除

### 问题 1：每日摘要未执行

**检查：**
```bash
# 查看 cron 任务
crontab -l | grep daily-summary

# 查看执行日志
tail -20 /root/.openclaw/workspace/logs/daily-summary.log
```

**解决：**
```bash
# 重新添加 cron 任务
/root/.openclaw/workspace/skills/memory-workflow/scripts/install.sh
```

### 问题 2：会话启动未读档

**检查：**
```bash
# 检查 MEMORY.md 是否存在
ls -la /root/.openclaw/workspace/MEMORY.md

# 检查每日笔记
ls -la /root/.openclaw/workspace/memory/
```

**解决：**
- 确保文件存在且有读取权限
- 手动触发一次读档：`source /root/.openclaw/workspace/skills/memory-workflow/scripts/install.sh`

---

## 📚 使用示例

### 示例 1：新会话启动

```
用户：早上好！
助手：早上好！✅ 已读档，记忆恢复。

我看到昨天我们讨论了投资分析，今天要继续吗？
```

### 示例 2：每日摘要提醒

```
[23:00] 系统：创建每日摘要待处理标记

[23:00-23:05] 等待用户补充...

[23:05] 系统：超时，自动创建基础模板
✅ 已创建 memory/2026-03-15.md
```

### 示例 3：实时写入

```
用户：我更喜欢喝红茶，不是绿茶。
助手：好的！要写入 MEMORY.md 吗？这样我下次就不会忘记了~

用户：好的。
助手：✅ 已写入 MEMORY.md - 用户偏好章节
```

---

## 🌟 社区贡献

欢迎 fork、改进、分享！

**改进建议：**
- [ ] 自动提取会话历史生成摘要
- [ ] 智能识别决策点自动记录
- [ ] 支持更多记忆存储后端（如数据库）
- [ ] 增加记忆搜索功能

---

## 📄 许可证

MIT License

---

*最后更新：2026-03-15*
*版本：1.0.0*
*作者：小吴 (ENFP 快乐小狗)* 🦞
