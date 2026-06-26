---
name: key-tracker
description: "智能关键信息记录技能：从对话和报告中自动捕获时间节点、遗留问题、决策点、承诺事项等16类关键信息。外置大脑，不遗漏重要信息。"
homepage: https://github.com/vincentlau2046-sudo/key-tracker
metadata: {"clawdbot":{"emoji":"🧠"}}
---

# Key Tracker - 智能关键信息记录

**外置大脑，自动捕获工作交流中的关键信息。**

GitHub: https://github.com/vincentlau2046-sudo/key-tracker

---

## 🎯 核心定位

**不是**：私人秘书、日程管理工具  
**而是**：外置大脑、关键信息捕获系统

### 核心价值

1. **不遗漏重要信息** — 自动检测并记录关键内容
2. **可追溯决策过程** — 记录决策及其原因
3. **提醒待处理事项** — 遗留问题、阻塞项跟踪
4. **沉淀知识经验** — 学习要点、想法灵感保存
5. **跟踪进展状态** — 进度、依赖、资源需求

---

## 📋 16 类记录类型

### ⏰ 时间类

| 类型 | 说明 | 触发词示例 |
|------|------|-----------|
| `deadline` | 截止日期 | "3月20日前完成"、"项目截止日期" |
| `milestone` | 里程碑 | "第一阶段里程碑"、"关键节点" |

### ❓ 问题类

| 类型 | 说明 | 触发词示例 |
|------|------|-----------|
| `issue` | 遗留问题 | "性能优化尚未完成"、"有个bug待解决" |
| `blocker` | 阻塞项 | "卡在等API文档"、"被依赖阻塞" |
| `risk` | 风险提示 | "可能延期"、"担心性能问题" |

### 🎯 决策类

| 类型 | 说明 | 触发词示例 |
|------|------|-----------|
| `decision` | 决策记录 | "决定用方案A"、"确定选PostgreSQL" |
| `rationale` | 决策原因 | "因为团队熟悉"、"考虑到成本问题" |
| `assumption` | 假设前提 | "假设用户量不超100万"、"前提是API稳定" |
| `change` | 变更记录 | "从方案A改成B"、"调整为新架构" |

### 🤝 承诺类

| 类型 | 说明 | 触发词示例 |
|------|------|-----------|
| `commitment` | 我的承诺 | "我明天发给你"、"我来负责这块" |
| `expectation` | 他人承诺 | "麻烦你帮忙"、"请你来处理" |

### 📊 过程类

| 类型 | 说明 | 触发词示例 |
|------|------|-----------|
| `progress` | 进展状态 | "已完成80%"、"正在开发中" |
| `dependency` | 依赖关系 | "依赖后端API"、"需要等测试环境" |
| `resource` | 资源需求 | "需要一台服务器"、"缺少人手" |

### 💡 知识类

| 类型 | 说明 | 触发词示例 |
|------|------|-----------|
| `learning` | 学习要点 | "以后要注意先检查依赖"、"经验教训" |
| `insight` | 想法灵感 | "也许可以用缓存优化"、"突然想到" |
| `context` | 背景上下文 | "项目背景是"、"目的是解决延迟" |

### 👤 人物类

| 类型 | 说明 | 触发词示例 |
|------|------|-----------|
| `stakeholder` | 关键人物 | "张三负责这块"、"涉及运维团队" |

---

## 🚀 快速开始

### 安装

**方式 1：ClawHub 安装（推荐）**
```bash
clawdhub install key-tracker
```

**方式 2：手动安装**
```bash
git clone https://github.com/vincentlau2046-sudo/key-tracker.git ~/.openclaw/workspace/skills/key-tracker
```

### 创建记录目录

```bash
mkdir -p ~/.openclaw/workspace/.keyrecords/{时间类,问题类,决策类,承诺类,过程类,知识类,人物类}
```

---

## 💬 使用示例

### 自动触发记录

在对话中自动检测关键词：

```
用户: "项目要在3月20日前完成"
→ 自动记录: deadline | 项目完成 | 2026-03-20

用户: "决定用 PostgreSQL，因为团队熟悉度高"
→ 自动记录: decision | 选择 PostgreSQL | rationale: 团队熟悉度高

用户: "我会明天把文档发给你"
→ 自动记录: commitment | 发送文档 | 2026-03-13

用户: "性能优化还没做，卡在缺少测试环境"
→ 自动记录: issue | 性能优化未完成 | blocker: 缺少测试环境
```

### 查询记录

```
用户: 有什么时间节点？     → 显示 deadlines + milestones
用户: 有哪些遗留问题？     → 显示 issues + blockers
用户: 做过什么决策？       → 显示 decisions + rationales
用户: 我承诺过什么？       → 显示 commitments
用户: 有什么风险？         → 显示 risks
用户: 卡在什么地方？       → 显示 blockers
用户: 依赖什么？           → 显示 dependencies
用户: 最近有什么想法？     → 显示 insights
用户: 显示所有记录         → 显示全部记录
```

---

## 📁 数据存储

### 目录结构

```
~/.openclaw/workspace/.keyrecords/
├── records.json           # 主记录库
├── 时间类/
│   └── deadlines.json
├── 问题类/
│   ├── issues.json
│   ├── blockers.json
│   └── risks.json
├── 决策类/
│   ├── decisions.json
│   ├── rationales.json
│   ├── assumptions.json
│   └── changes.json
├── 承诺类/
│   ├── commitments.json
│   └── expectations.json
├── 过程类/
│   ├── progress.json
│   ├── dependencies.json
│   └── resources.json
├── 知识类/
│   ├── learnings.json
│   ├── insights.json
│   └── contexts.json
└── 人物类/
    └── stakeholders.json
```

### 记录格式

```json
{
  "id": "KR-20260312-001",
  "type": "deadline",
  "title": "项目交付",
  "context": "讨论项目进度时确定",
  "source": "conversation",
  "source_text": "项目要在3月20日前完成",
  "datetime": "2026-03-20T18:00:00+08:00",
  "status": "pending",
  "priority": "high",
  "logged_at": "2026-03-12T14:00:00+08:00"
}
```

---

## 🔍 检测规则

### 时间检测

```regex
# 日期 + 截止词
\d{1,2}月\d{1,2}[日号].*(截止|之前|前完成)
# 相对时间
(下周|下月|月底).*(完成|交付)
```

### 决策检测

```regex
决定|确定|就.*了|选定
因为|考虑到|出于|由于
```

### 承诺检测

```regex
我会|我保证|我来负责
麻烦你|请你|你来负责
```

### 问题检测

```regex
问题|bug|issue|尚未|待.*完成
卡住|阻塞|等.*才能
风险|可能.*问题
```

---

## ⚙️ 定期回顾

建议配置定期回顾任务：

| 任务 | 时间 | 内容 |
|------|------|------|
| 晨间提醒 | 08:00 | 今日 deadline + pending commitments |
| 晚间回顾 | 21:00 | 今日记录汇总 + 明日关注点 |
| 周度盘点 | 周五 18:00 | 本周决策 + 遗留问题 + 风险项 |

---

## 🔗 相关链接

- **GitHub**: https://github.com/vincentlau2046-sudo/key-tracker
- **问题反馈**: https://github.com/vincentlau2046-sudo/key-tracker/issues
- **ClawHub**: https://clawhub.com

---

## 📄 许可证

MIT License

---

**外置大脑，让每一次思考都有痕迹。**