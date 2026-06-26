---
name: self-improving-skill
version: 1.1.0
description: |
  让任何 writing style skill 自动从人类修改中学习。
  只需要两个数据点：AI 原稿 (original) 和人类最终版 (final)。
  自动 diff → 提取规则 → 更新目标 SKILL.md。
  兼容 Claude Code (~/.claude/skills/) 和 OpenClaw (ClawHub)。
dependencies: []
allowed-tools:
  - Read
  - Write
  - Edit
  - exec
---

# Self-Improving Skill Framework v1.0

**让你的 writing style skill 越用越准。**

---

## 🎯 核心概念

```
AI 写初稿 → 人类改到满意 → 对比两版 → 提取规则 → 更新 skill
     ↑                                              ↓
     └──────── 下次写作自动应用新规则 ←──────────────┘
```

**只有两个数据点：**
- **original**: AI 生成的第一版（不管用了什么 prompt/skill）
- **final**: 人类最终确认的版本（不管中间改了几轮、怎么改的）

中间过程不记录。Google Doc 来回改了 10 轮？无所谓，只比较首尾。

---

## 📋 使用流程

### 第一步：配置目标 skill

在你的 writing style skill 目录下创建 `self-improving.yaml`：

```yaml
# ~/your-skill/self-improving.yaml
target_skill: ~/path/to/your-writing-style/SKILL.md
log_dir: ~/clawd/memory/skill-runs/your-skill-name/
proposal_dir: ~/clawd/memory/skill-proposals/your-skill-name/
backup_dir: ~/clawd/memory/skill-backups/your-skill-name/
```

或者用环境变量 / 命令行参数覆盖（见下文）。

### 第二步：Agent 写完内容后，记录原稿

```bash
python3 ~/clawd/skills/self-improving-skill/scripts/observe.py record-original <file> \
  --skill ~/path/to/your-writing-style/
```

或直接传文本：
```bash
python3 observe.py record-original --text "AI 生成的内容..."
```

**输出：**
```
✅ 记录原稿: a3f8c2e1
📝 字数: 1234
```

记住这个 hash（`a3f8c2e1`），后面配对用。

### 第三步：人类确认最终版后，记录 final

```bash
python3 observe.py record-final <file> --match a3f8c2e1
```

**如果人类没改直接用了？** 也 record-final，脚本自动检测内容一致 → 标记为无修改（正反馈）。

### 第四步：提取改进规则

```bash
# 手动提取
python3 ~/clawd/skills/self-improving-skill/scripts/improve.py extract --days 7

# 或自动模式（适合 cron）：提取 + 自动应用 P0 规则
python3 improve.py auto
```

### 第五步：查看 / 应用 / 回滚

```bash
python3 improve.py show        # 查看所有提案
python3 improve.py apply <id>  # 应用某个提案
python3 improve.py rollback    # 回滚上次应用
```

---

## ⚙️ 自动化（推荐）

### 集成到你的内容创作流程

在你的 contentgen / writing skill 中加入：

```markdown
## 写完内容后必须做的事

1. 写完初稿 → `observe.py record-original <file>`
2. 人类确认最终版 → `observe.py record-final <file> --match <hash>`
```

### Cron Job

```bash
# 每晚自动提取 + 应用 P0 规则
# schedule: 0 23 * * * (每晚 11pm)
python3 ~/clawd/skills/self-improving-skill/scripts/improve.py auto \
  --skill ~/path/to/your-writing-style/
```

OpenClaw 用户可以用内置 cron：
```
cron add --name "skill-daily-extract" --schedule "0 23 * * *" --tz "America/New_York" \
  --payload "运行 improve.py auto 自动提取写作风格改进"
```

---

## 📂 数据结构

```
~/clawd/memory/
├── skill-runs/your-skill/
│   └── YYYY-MM-DD.jsonl        # 每日观察日志
│       ├── {type: "original", content_hash, content, context}
│       └── {type: "final", content_hash, original_content, final_content, no_change}
│
├── skill-proposals/your-skill/
│   └── YYYYMMDD-HHMMSS.md     # 改进提案（P0/P1/P2 分级）
│
└── skill-backups/your-skill/
    └── SKILL-YYYYMMDD-HHMMSS.md  # apply 前自动备份
```

---

## 🔄 循环原理

### 为什么只看 original vs final？

1. **中间过程有噪音** — 人类可能改了又改回来，中间状态不代表最终偏好
2. **指令不等于规则** — "把开头改一下"是一次性指令，不是通用规则。但如果 final 里开头确实更直接，diff 能自动捕捉
3. **简单就是可靠** — 两个数据点不会出错，复杂流程容易断

### 什么算好的学习数据？

| 数据 | 价值 |
|------|------|
| AI 原稿 2000 字 → final 1800 字（删了废话）| ⭐⭐⭐ 高 |
| AI 原稿 → final 完全不变（直接用）| ⭐⭐ 正反馈 |
| AI 原稿 500 字 → final 2000 字（大幅扩写）| ⭐ 低（扩写靠 prompt 不靠 style） |
| AI 原稿 → final 只改了一个错别字 | ⭐ 低（不是风格问题）|

### P0 / P1 / P2 规则分级

- **P0**: 高置信度（多次出现同一模式），cron 自动应用
- **P1**: 中置信度，需要人工确认后应用
- **P2**: 低置信度（只出现 1 次），存档观察

---

## 🛡 安全机制

1. **每次 apply 前自动备份** SKILL.md → `skill-backups/`
2. **一键回滚**: `improve.py rollback`
3. **auto 模式只应用 P0** — P1/P2 需要人工确认
4. **提案可审核** — 所有提案以 markdown 保存，可读可编辑

---

## 📊 CLI 参考

### observe.py

| 命令 | 功能 |
|------|------|
| `record-original <file>` | 记录 AI 原稿 |
| `record-original --text "..."` | 直接传文本 |
| `record-final <file> --match <hash>` | 记录最终版 |
| `pending` | 查看待配对原稿 |
| `stats` | 总体统计 |

### improve.py

| 命令 | 功能 |
|------|------|
| `extract` | 提取改进建议（默认今天）|
| `extract --days 7` | 最近 7 天 |
| `auto` | 自动提取 + 应用 P0（cron 用）|
| `show` | 查看所有提案 |
| `apply <id>` | 应用指定提案 |
| `rollback` | 回滚上次应用 |

---

## 💡 适用场景

这个 framework 不限于写作风格，任何 "AI 生成 → 人类修改" 的循环都适用：

- Writing style skill（推文、文章、小红书）
- Code review rules（AI 写代码 → 人类 review）
- Email drafting（AI 写邮件 → 人类调整语气）
- Translation style（AI 翻译 → 人类润色）

核心不变：**记录 original + final，自动 diff 提取规则。**

---

## 🔧 安装

### Claude Code 用户

```bash
# 方式 1: 直接复制到 skills 目录
cp -r self-improving-skill ~/.claude/skills/

# 方式 2: 项目级 skill
cp -r self-improving-skill ./your-project/.claude/skills/
```

数据自动存储在 `~/.claude/memory/skill-runs/` 下。

### OpenClaw / ClawHub 用户

```bash
# 方式 1: ClawHub 安装
npx clawhub@latest install self-improving-skill

# 方式 2: 手动复制
cp -r self-improving-skill ~/clawd/skills/
```

数据自动存储在 `~/clawd/memory/skill-runs/` 下。

### LLM 依赖

`improve.py extract/auto` 需要一个 LLM CLI 来分析 diff。自动检测：

| CLI | 安装 | 说明 |
|-----|------|------|
| `claude` | Claude Code 自带 | 优先使用 |
| `llm` | `pip install llm` | Simon Willison 的通用 CLI |
| 自定义 | `IMPROVE_LLM_CMD=...` | 任意接受 stdin 的命令 |

`observe.py` 不依赖任何 LLM，纯 Python，零依赖。

### 自定义存储路径

```bash
# 环境变量
export SKILL_BASE_DIR=~/my-custom-path/memory

# 或命令行参数
python3 observe.py stats --log-dir ~/my-path/skill-runs/my-skill/
```
