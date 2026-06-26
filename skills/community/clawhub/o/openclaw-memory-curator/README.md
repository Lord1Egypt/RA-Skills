# Memory Curator / 记忆整理器

[English](#english) | [中文](#中文)

---

## 中文

一个用于 OpenClaw/Clawd 的记忆整理技能，帮助你组织、去重、压缩记忆文件。

### 功能

- **备份** - 在修改前快照 `memory/` 和 `MEMORY.md`
- **报告** - 显示记忆文件数量、行数、最大文件
- **验证** - 检查工作区结构，汇总记忆占用
- **整理** - 将冗长的对话记录转化为简洁的持久记忆

### 安装

#### 方法 1：克隆到技能目录

```bash
cd /root/clawd/skills
git clone https://github.com/1217047020/memory-curator.git
```

#### 方法 2：手动安装

```bash
mkdir -p /root/clawd/skills/memory-curator/scripts
cp SKILL.md /root/clawd/skills/memory-curator/
cp scripts/curate_memory.py /root/clawd/skills/memory-curator/scripts/
chmod +x /root/clawd/skills/memory-curator/scripts/curate_memory.py
```

### 使用方法

#### 命令行

```bash
# 查看记忆状态
python3 scripts/curate_memory.py report --workspace /root/clawd

# 修改前备份
python3 scripts/curate_memory.py backup --workspace /root/clawd

# 验证工作区结构
python3 scripts/curate_memory.py validate --workspace /root/clawd
```

#### 作为 OpenClaw 技能

当你对 AI 说以下内容时，技能会自动激活：

- "整理记忆"
- "压缩每日笔记"
- "更新 MEMORY.md"
- "记忆去重"

### 工作区结构

期望的工作区布局：

```
<workspace>/
├── AGENTS.md          # 工作区指南
├── MEMORY.md          # 整理后的长期记忆
└── memory/
    ├── 2026-03-30.md  # 每日笔记
    └── topic-note.md  # 主题笔记
```

### 整理流程

1. **检查** - 读取 `AGENTS.md`、`MEMORY.md`，运行 `report`
2. **提取** - 保留持久信息，丢弃噪音和重复内容
3. **更新** - 用分类章节刷新 `MEMORY.md`
4. **压缩** - 将每日笔记重写为 3-6 条要点
5. **验证** - 对比前后变化，汇报结果

### 保留什么

- 用户偏好和操作规则
- 环境事实和访问方式
- 稳定的集成和配置
- 反复出现的失败模式和已知限制
- 进行中的长期目标

### 丢弃什么

- 原始对话记录
- 重复的确认消息
- 重复的日志
- 过期的 token 和一次性输出
- 敏感数据（除非明确需要）

---

## English

A skill for OpenClaw/Clawd to organize, deduplicate, and compress memory files.

### Features

- **Backup** - Snapshot `memory/` and `MEMORY.md` before changes
- **Report** - Show memory file counts, line counts, and largest files
- **Validate** - Check workspace structure and summarize memory footprint
- **Curate** - Turn bloated transcripts into concise, durable memory

### Installation

```bash
cd /root/clawd/skills
git clone https://github.com/1217047020/memory-curator.git
```

### Usage

```bash
# Show memory status
python3 scripts/curate_memory.py report --workspace /root/clawd

# Backup before changes
python3 scripts/curate_memory.py backup --workspace /root/clawd

# Validate workspace structure
python3 scripts/curate_memory.py validate --workspace /root/clawd
```

### Workspace Pattern

```
<workspace>/
├── AGENTS.md          # Workspace guidance
├── MEMORY.md          # Curated long-term memory
└── memory/
    ├── 2026-03-30.md  # Daily notes
    └── topic-note.md  # Topic-specific notes
```

### What to Keep

- User preferences and operating rules
- Environment facts and access patterns
- Stable integrations and working setups
- Recurring failure modes and known constraints
- Active long-running goals

### What to Drop

- Raw transcripts
- Repeated confirmations
- Duplicated logs
- Expired tokens and one-off outputs
- Sensitive data (unless explicitly needed)

---

## License

MIT
