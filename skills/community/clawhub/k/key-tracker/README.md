# 🧠 Key Tracker - 智能关键信息记录技能

> 外置大脑，自动捕获工作交流中的关键信息

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()
[![ClawHub](https://img.shields.io/badge/ClawHub-Ready-orange.svg)]()

**GitHub**: https://github.com/vincentlau2046-sudo/key-tracker

---

## 🎯 这是什么？

Key Tracker 是一个**外置大脑**技能，帮助你在工作交流中不遗漏重要信息。

**核心理念**：
- 不是私人秘书，不需要你主动添加日程
- 而是第二记忆系统，自动捕获你大脑应该记住的一切
- 在对话、报告分析中自动检测关键词并记录

---

## ✨ 核心功能

### 自动捕获 16 类关键信息

| 类别 | 类型 | 示例 |
|------|------|------|
| **时间类** | deadline, milestone | "3月20日前完成" |
| **问题类** | issue, blocker, risk | "性能优化还没做" |
| **决策类** | decision, rationale, assumption, change | "决定用方案A" |
| **承诺类** | commitment, expectation | "我明天发给你" |
| **过程类** | progress, dependency, resource | "已完成80%" |
| **知识类** | learning, insight, context | "以后要注意..." |
| **人物类** | stakeholder | "张三负责这块" |

### 智能检测触发

```
用户说: "项目要在3月20日前完成"
→ 自动记录: deadline | 项目完成 | 2026-03-20

用户说: "决定用 PostgreSQL，因为团队熟悉"
→ 自动记录: decision + rationale

用户说: "我会明天把文档发给你"
→ 自动记录: commitment | 明天
```

### 快速查询

```
用户: 有什么时间节点？
用户: 有哪些遗留问题？
用户: 做过什么决策？
用户: 我承诺过什么？
```

---

## 🚀 安装

### ClawHub 安装（推荐）

```bash
clawdhub install key-tracker
```

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/vincentlau2046-sudo/key-tracker.git ~/.openclaw/workspace/skills/key-tracker

# 创建记录目录
mkdir -p ~/.openclaw/workspace/.keyrecords/{时间类,问题类,决策类,承诺类,过程类,知识类,人物类}
```

---

## 📋 16 类记录类型详解

### ⏰ 时间类

| 类型 | 说明 | 触发词 |
|------|------|--------|
| `deadline` | 截止日期 | 截止、之前完成、deadline |
| `milestone` | 里程碑 | 里程碑、节点、阶段性目标 |

### ❓ 问题类

| 类型 | 说明 | 触发词 |
|------|------|--------|
| `issue` | 遗留问题 | 问题、bug、issue、待解决 |
| `blocker` | 阻塞项 | 卡住、阻塞、等...才能 |
| `risk` | 风险提示 | 风险、可能出问题、担心 |

### 🎯 决策类

| 类型 | 说明 | 触发词 |
|------|------|--------|
| `decision` | 决策记录 | 决定、确定、选定、就...了 |
| `rationale` | 决策原因 | 因为、考虑到、出于、由于 |
| `assumption` | 假设前提 | 假设、前提、如果...的话 |
| `change` | 变更记录 | 改为、换成、调整、从...改 |

### 🤝 承诺类

| 类型 | 说明 | 触发词 |
|------|------|--------|
| `commitment` | 我的承诺 | 我会、我保证、我来负责 |
| `expectation` | 他人承诺 | 麻烦你、请你、你来负责 |

### 📊 过程类

| 类型 | 说明 | 触发词 |
|------|------|--------|
| `progress` | 进展状态 | 已完成、正在做、进度 |
| `dependency` | 依赖关系 | 依赖、需要等、取决于 |
| `resource` | 资源需求 | 需要、缺少、希望有 |

### 💡 知识类

| 类型 | 说明 | 触发词 |
|------|------|--------|
| `learning` | 学习要点 | 经验、教训、记住、以后注意 |
| `insight` | 想法灵感 | 突然想到、灵感、也许可以 |
| `context` | 背景上下文 | 背景、原因是、目的是、为了 |

### 👤 人物类

| 类型 | 说明 | 触发词 |
|------|------|--------|
| `stakeholder` | 关键人物 | 负责、找...、联系...、涉及 |

---

## 💬 使用示例

### 场景 1：时间节点检测

```
用户: "项目要在3月20日前完成"
→ 自动记录:
  type: deadline
  title: 项目完成
  datetime: 2026-03-20
  context: 项目交付时间
```

### 场景 2：决策记录

```
用户: "决定用 PostgreSQL，因为团队熟悉度高"
→ 自动记录:
  type: decision
  title: 选择 PostgreSQL
  rationale: 团队熟悉度高
```

### 场景 3：问题捕获

```
报告: "性能优化尚未完成，卡在缺少测试环境"
→ 自动记录:
  type: issue
  title: 性能优化未完成
  blocker: 缺少测试环境
```

### 场景 4：承诺记录

```
用户: "我会明天把文档发给你"
→ 自动记录:
  type: commitment
  title: 发送文档
  deadline: 2026-03-13
```

---

## 📁 数据存储

所有记录保存在 `~/.openclaw/workspace/.keyrecords/`

```
.keyrecords/
├── records.json           # 主记录库
├── 时间类/
├── 问题类/
├── 决策类/
├── 承诺类/
├── 过程类/
├── 知识类/
└── 人物类/
```

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/vincentlau2046-sudo/key-tracker
- **问题反馈**: https://github.com/vincentlau2046-sudo/key-tracker/issues
- **ClawHub 社区**: https://clawhub.com

---

## 📄 许可证

MIT License

---

**外置大脑，让每一次思考都有痕迹。**