---
name: writing-style-skill
version: 1.0.0
description: |
  可复用的写作风格 Skill 模板。内置自动学习：
  从你的修改中自动提取规则，SKILL.md 越用越准。
  Fork 后改成你自己的风格。
dependencies: []
allowed-tools:
  - Read
  - Write
  - Edit
  - exec
---

# Writing Style Skill（模板）

**Fork 这个 skill，改成你的写作风格。内置自动学习，越用越准。**

---

## 🎯 怎么用

1. Fork / clone 这个 skill
2. 把下面的风格规则改成你自己的
3. 让 AI 用这个 skill 写内容
4. 你改到满意 → 脚本自动学习你改了什么
5. 下次 AI 写出来的就更像你

---

## 【0】Voice Dimensions（量化你的风格）

**用 1-10 分定义你的风格维度。AI 比"写得自然一点"这种话更容易理解数字。**

| Dimension | Score | 你的说明 |
|-----------|-------|---------|
| **formal_casual** | **?/10** | 偏正式还是偏随意？ |
| **technical_accessible** | **?/10** | 技术深度？ |
| **serious_playful** | **?/10** | 严肃还是活泼？ |
| **concise_elaborate** | **?/10** | 简洁还是详细？ |
| **reserved_expressive** | **?/10** | 保守还是直接？ |

> 💡 **不知道填什么？** 先跑几次 AI 写作 → 你改 → 自动学习会帮你填。

---

## 【1】角色与读者

**我是谁：**
- （填你的身份，比如：独立开发者，新晋 AI 爱好者）

**读者是谁：**
- （填你的读者，比如：对 AI 感兴趣的技术人）

**和读者的关系：**
- （比如：同行交流，不是教学）

---

## 【2】写作规则

### 基础规则

- （填你的规则，比如：不用"深入探讨"、段落要短、要有具体数字）
- 
- 

### 禁止词

- （AI 爱用但你不喜欢的词，比如：值得注意的是、综上所述、本文将介绍）
- 
- 

### 句式偏好

- （你喜欢的句式，比如：结论前置、不要学术导语）
- 
- 

> 💡 **不需要一开始就写完。** 这些规则会通过你的修改自动积累。
> 跑完 10 次写作→修改循环后，这里会长出几十条精准规则。

---

## 【3】格式规范

### 平台适配

| 平台 | 格式要求 |
|------|---------|
| X/Twitter | 不渲染 markdown，用纯文本 |
| 小红书 | emoji 多、分段短 |
| 博客 | 标准 markdown |
| （你的平台） | （你的要求）|

---

## 🔄 自动学习（内置）

**这个 skill 会从你的修改中自动学习。不需要手动写规则。**

### 工作原理

```
AI 用这个 skill 写初稿
    ↓
你改到满意
    ↓
脚本 diff 两版 → 提取你改了什么
    ↓
新规则自动写入这个 SKILL.md
    ↓
下次 AI 写出来就更像你
```

### 只需要两个数据点

- **original**: AI 生成的第一版
- **final**: 你最终确认的版本

中间改了几轮不管。在 Google Doc 里来回改了 10 次？无所谓，只比较首尾。

### Agent 操作指南

**写完内容后：**
```bash
python3 scripts/observe.py record-original <file> --account <账号> --content-type <类型>
```

**人类确认最终版后：**
```bash
python3 scripts/observe.py record-final <file> --match <hash>
```

**提取规则（手动或 cron 自动）：**
```bash
python3 scripts/improve.py auto --skill .
```

### 规则分级

| 级别 | 含义 | 处理方式 |
|------|------|---------|
| P0 | 高置信度（多次出现） | 自动应用 |
| P1 | 中置信度 | 人工确认 |
| P2 | 低置信度（仅 1 次） | 存档观察 |

### 安全

- 每次更新前自动备份 SKILL.md
- `improve.py rollback` 一键回滚
- auto 模式只应用 P0

---

## 📊 CLI 参考

### observe.py（零依赖纯 Python）

| 命令 | 功能 |
|------|------|
| `record-original <file>` | 记录 AI 原稿 |
| `record-final <file> --match <hash>` | 记录最终版 |
| `pending` | 查看待配对 |
| `stats` | 统计 |

### improve.py（需要 LLM CLI）

| 命令 | 功能 |
|------|------|
| `extract [--days 7]` | 提取改进建议 |
| `auto` | 提取 + 自动应用 P0 |
| `show` | 查看提案 |
| `apply <id>` | 应用提案 |
| `rollback` | 回滚 |

支持的 LLM CLI: `claude`（Claude Code）/ `llm`（pip install llm）/ `IMPROVE_LLM_CMD` 环境变量

---

## 📂 数据存储

```
~/clawd/memory/                    # OpenClaw
~/.claude/memory/                  # Claude Code
├── skill-runs/<skill-name>/
│   └── YYYY-MM-DD.jsonl          # 每日观察日志
├── skill-proposals/<skill-name>/
│   └── YYYYMMDD-HHMMSS.md       # 改进提案
└── skill-backups/<skill-name>/
    └── SKILL-YYYYMMDD-HHMMSS.md  # 自动备份
```

自动检测环境，不需要手动配置路径。

---

## 🚀 30 天预期

| 时间 | 预期效果 |
|------|---------|
| 第 1 周 | 积累 3-5 次修改，生成第一批规则 |
| 第 2 周 | 10+ 条规则，AI 输出明显更像你 |
| 第 1 月 | 30+ 条规则，风格维度自动校准 |
| 持续 | 规则库稳定增长，新 pattern 自动捕捉 |
