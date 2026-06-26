# MemoryHamster 🤖

**Agent 记忆进化系统 - 让 AI 每天变得更聪明**

[![ClawHub](https://img.shields.io/badge/ClawHub-skill-blue)](https://clawhub.com)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-green)](https://openclaw.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-orange)](https://clawhub.com/skills/memory-hamster)

---

## 📖 简介

MemoryHamster 是一个完整的 AI 记忆管理与自我进化系统。

**核心功能**：
- 🌡️ **温度模型**：热/温/冷数据分层管理
- 🗄️ **自动归档**：30 天冷数据自动归档
- 📝 **学习记录**：教训/错误/功能请求追踪
- 🔍 **语义搜索**：跨会话记忆检索
- 🏗️ **技能提炼**：从教训自动提取技能
- 📈 **Promotion 机制**：知识提升到配置文件

---

## ✨ 特性

| 特性 | 说明 |
|------|------|
| 温度模型 | 热数据 (<7 天) → 温数据 (7-30 天) → 冷数据 (>30 天) |
| 自动 GC | 每周日自动归档冷数据 |
| 夜间反思 | 每日 23:45 自动反思验证 |
| 学习系统 | 教训/错误/功能请求三类记录 |
| 语义搜索 | 基于关键词的语义匹配 |
| 技能提取 | 从教训自动提取独立技能 |
| Promotion | 知识提升到 SOUL/AGENTS/TOOLS |

---

## 📦 安装

```bash
# 从 ClawHub 安装
clawhub install memory-hamster

# 或手动安装
git clone https://github.com/your-repo/memory-hamster.git
cp -r memory-hamster ~/.openclaw/workspace/skills/
```

---

## 🚀 快速开始

### 1. 配置 Cron 任务

```bash
# 编辑 crontab
crontab -e

# 添加以下任务
0 0 * * 0 /path/to/skills/memory-hamster/scripts/memory-gc.sh >> /path/to/logs/memory-gc.log 2>&1
45 23 * * * /path/to/skills/memory-hamster/scripts/nightly-reflection.sh >> /path/to/logs/nightly-reflection.log 2>&1
```

### 2. 初始化目录

```bash
# 脚本会自动创建以下结构
memory/
├── INDEX.md
├── YYYY-MM-DD.md
├── lessons/
├── decisions/
└── .archive/

.learnings/
├── LEARNINGS.md
├── ERRORS.md
└── FEATURE_REQUESTS.md
```

### 3. 开始使用

**会话开始**：读取 `MEMORY.md` + 今日日志  
**会话中**：记录重要决策/教训/错误  
**会话结束**：更新每日日志

---

## 📚 文档

- [SKILL.md](SKILL.md) - 完整技能文档
- [templates/](templates/) - 模板文件
- [scripts/](scripts/) - 自动化脚本

---

## 🔧 脚本说明

| 脚本 | 功能 | 频率 |
|------|------|------|
| `memory-gc.sh` | GC 归档冷数据 | 每周 |
| `nightly-reflection.sh` | 夜间反思验证 | 每日 |
| `extract-skill.sh` | 技能提取 | 按需 |
| `search-memory.cjs` | 语义搜索 | 按需 |

---

## 📊 目录结构

```
skills/memory-hamster/
├── SKILL.md                 # 技能文档
├── README.md                # 本文件
├── scripts/
│   ├── memory-gc.sh         # GC 脚本
│   ├── nightly-reflection.sh # 反思脚本
│   ├── extract-skill.sh     # 提取脚本
│   └── search-memory.cjs    # 搜索脚本
└── templates/
    ├── feature-template.md
    ├── lesson-template.md
    ├── error-template.md
    └── daily-log-template.md
```

---

## 🎯 使用场景

### 场景 1：记录教训

```markdown
## [LRN-20260316-001] workflow

**Summary**: 长任务需要 spawning 子代理，避免主会话阻塞

**Priority**: medium
**Status**: promoted
**Area**: workflow

### Details
在处理复杂任务时，直接使用主会话会导致上下文膨胀...

### Suggested Action
长任务（>5 分钟）使用 sessions_spawn 创建子代理
```

### 场景 2：记录错误

```markdown
## [ERR-20260316-001] git-push

**Summary**: Git push 失败，未配置认证

**Error**:
```
fatal: Authentication failed
```

### Context
- 尝试：git push origin main
- 环境：新初始化的仓库

### Suggested Fix
先配置 Git 认证：git config --global credential.helper store
```

### 场景 3：语义搜索

```bash
# 搜索昨天的工作
node search-memory.cjs "work yesterday recent activity"

# 搜索编码偏好
node search-memory.cjs --user "coding preferences style"
```

---

## 📈 健康度指标

| 指标 | 正常范围 | 检查频率 |
|------|----------|----------|
| MEMORY.md 大小 | < 5KB | 每日 |
| 热数据数量 | 5-10 个 | 每周 |
| 教训数量 | 持续增长 | 每周 |
| 归档率 | < 20%/周 | 每周 |
| 上下文大小 | < 100k | 每会话 |

---

## 🤝 与其他技能配合

| 技能 | 配合方式 |
|------|---------|
| browser-search | 搜索信息后记录学习 |
| tavily-search | 搜索结果记录到记忆 |
| github | 项目相关学习记录 |
| skill-creator | 技能提取时使用 |

---

## 📝 更新日志

### v1.0.0 (2026-03-16)
- ✨ 初始版本发布
- 🌡️ 温度模型实现
- 🗄️ 自动 GC 归档
- 📝 学习记录系统
- 🔍 语义搜索
- 🏗️ 技能提取

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- OpenClaw 团队提供的平台支持
- ClawHub 技能分发平台

---

_🤖 MemoryHamster：高效管理记忆，让 AI 每天变得更聪明！_
