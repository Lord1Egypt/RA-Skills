---
name: memory-four-types
description: 四类型记忆管理 Skill。为 OpenClaw agent 提供标准化的记忆分类、存储和索引规范。将记忆分为 user / feedback / project / reference 四类，每类独立文件，MEMORY.md 做索引。触发词：记忆管理、memory classification、记忆分类、四类型记忆。
metadata:
  openclaw:
    requires:
      bins: []
    emoji: "🧠"

# ── Tool Registration (Stage 1: Metadata Only) ──────────────────

tools: []

---

# 🧠 Memory Four Types — 四类型记忆管理

> 参考 Claude Code 的记忆分类系统（`src/memdir/memoryTypes.ts`），
> 结合 OpenClaw 实践经验设计。

## 什么是四类型记忆？

Claude Code 将记忆严格分为 4 种类型，每种有明确的保存/使用规范：

| 类型 | 用途 | 何时保存 | 示例 |
|------|------|---------|------|
| **user** | 用户角色、偏好、知识水平 | 学到用户任何身份信息时 | "数据科学家，偏好 Python" |
| **feedback** | 用户纠正/确认的方法论 | 用户纠正或确认非直觉操作时 | "不要 mock 数据库，上次出过事故" |
| **project** | 项目进展、目标、deadline | 了解到"谁在做什么、为什么、什么时候" | "周四后冻结非关键合并" |
| **reference** | 外部系统指针 | 了解到外部资源位置时 | "pipeline bug 跟踪在 Linear" |

### 关键原则

- ❌ **不保存**可从代码/git 推导的内容（代码模式、架构、git 历史）
- ✅ **保存**人类直觉、隐性知识、"为什么这样做"
- ✅ 每个记忆独立文件，按语义主题组织（不按时间）
- ✅ MEMORY.md 只做索引，每行 ≤ 150 字符，超过 200 行时清理
- ✅ 文件命名格式：`{type}-{subject}.md`（如 `user-role.md`、`feedback-testing.md`）
- ✅ 写入前检查敏感信息（见下方安全规则）

---

## 命名规范

记忆文件使用 `{type}-{subject}.md` 格式：

| 类型 | 示例文件名 | 说明 |
|------|-----------|------|
| user | `user-da-lao-profile.md` | 用户画像 |
| feedback | `feedback-operating-rules.md` | 方法论、教训 |
| project | `project-calendar-add-v2.md` | 项目进展 |
| reference | `reference-deployed-skills.md` | 外部资源 |

**命名规则：**
- `type` 固定为 `user` / `feedback` / `project` / `reference`
- `subject` 用小写英文 + 连字符，简短描述主题
- 避免中文文件名（跨 agent 共享兼容性更好）
- 同一 subject 有更新时，直接更新原文件，不新建

---

## 目录结构

```
workspace/
├── MEMORY.md                      # 索引文件（手动维护）
└── memory/                        # 记忆目录
    ├── user/                      # 用户画像、偏好
    │   └── user-{subject}.md
    ├── feedback/                  # 方法论、教训
    │   └── feedback-{subject}.md
    ├── project/                   # 项目进展
    │   └── project-{subject}.md
    ├── reference/                 # 外部资源指针
    │   └── reference-{subject}.md
    └── YYYY-MM-DD.md              # 可选：每日原始日志
```

---

## 快速开始

### 1. 初始化目录结构

手动创建（或用模板）：

```powershell
# 在 workspace 根目录执行
New-Item -ItemType Directory -Path "memory\user","memory\feedback","memory\project","memory\reference" -Force
```

### 2. 配置 MEMORY.md

将现有的 `MEMORY.md` 改为索引格式。参考模板：`templates/MEMORY-index.md`

```markdown
# MEMORY.md - 长期记忆索引

> 每行一条记忆，按类型分组。详细内容见 `memory/` 子目录。
> 单条 ≤150 字符。超过 200 行时清理旧条目。

## User（用户画像）
- [用户名称](memory/user/xxx-profile.md) — 基本信息、偏好

## Feedback（方法论 & 教训）
- [教训名称](memory/feedback/xxx-lesson.md) — 核心要点，日期

## Project（项目进展）
- [项目名称](memory/project/xxx-progress.md) — 当前状态

## Reference（外部资源）
- [资源名称](memory/reference/xxx-resource.md) — 位置、用途
```

### 3. 创建记忆文件

每个记忆文件使用 frontmatter + 正文格式：

```markdown
---
name: 记忆名称
description: 一句话描述
type: user | feedback | project | reference
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# 标题

## 内容...

## Why（为什么重要）
...

## How to apply（怎么用）
...
```

参考各类型模板：
- `templates/user-example.md`
- `templates/feedback-example.md`
- `templates/project-example.md`
- `templates/reference-example.md`

---

## Agent 使用指南

### 什么时候写记忆？

| 场景 | 类型 | 操作 |
|------|------|------|
| 用户说了自己的偏好/背景 | `user` | 更新或创建 user 文件 + 索引 |
| 用户纠正了你的操作 | `feedback` | 创建 feedback 文件，记录"为什么"和"怎么避免" |
| 项目有进展/决策/变更 | `project` | 更新 project 文件 + 索引 |
| 发现外部工具/文档/资源 | `reference` | 创建 reference 文件 |
| 日常对话中有趣的事 | — | 写入 `memory/YYYY-MM-DD.md` 日志 |

### 怎么写好记忆？

**写 Why，不写 What：**
- ❌ "修改了 config.json 的 security 字段"
- ✅ "Windows 上 exec allowlist 不兼容，因为走 shell text 路径而非直接 binary 调用"

**写 How to apply：**
- 每条 feedback/project 记忆必须有"下次怎么做"
- 这是未来 agent 看到就能直接用的指引

**控制长度：**
- 索引行 ≤ 150 字符
- 单个文件正文 ≤ 200 行
- 超过时拆分或合并旧条目

### MEMORY.md 维护规则

1. **新增记忆** → 创建独立文件 → 更新 MEMORY.md 索引行
2. **定期清理**（heartbeat / cron 时做）→ 读最近 daily log → 提取重要事件 → 更新 MEMORY.md
3. **超 200 行时** → 合并过时条目、删除已失效内容
4. **安全** → 不在 MEMORY.md 中存密码/API Key，敏感内容只在独立文件中标记

### 记忆衰减规则

记忆有"新鲜度"，不同类型的衰减速度不同：

| 类型 | 衰减周期 | 处理方式 |
|------|---------|---------|
| **user** | 6 个月 | 超期后检查是否仍然准确，更新 `updated` 或标记过时 |
| **feedback** | 不衰减 | 长期有效，除非明确被推翻 |
| **project** | 1 个月 | 项目状态变化快，超期未更新的标记为 `[stale]` 候选清理 |
| **reference** | 3 个月 | 检查资源是否仍然可用 |

**清理流程（MEMORY.md 超 150 行时触发）：**
1. 检查每条索引对应的独立文件的 `updated` 日期
2. project 类型 > 1 个月未更新 → 索引行前加 `[stale]` 标记
3. 连续 2 次检查仍 stale → 合并到同类条目或删除
4. feedback 类型不衰减，除非明确标注"已推翻"
5. 清理后 MEMORY.md 应 ≤ 150 行

### 敏感信息扫描规则

**写入记忆文件前必须检查以下模式：**

| 模式 | 示例 | 处理 |
|------|------|------|
| API Key | `sk-xxx`, `BSAxxx`, `ghp_xxx` | ❌ 不写入，改为"已配置 [服务名] API Key" |
| 密码/token | 长随机字符串（>20 字符的 hex/base64） | ❌ 不写入，改为"已配置凭证" |
| OAuth Token | `ya29.xxx`, `gho_xxx` | ❌ 不写入 |
| 内部 URL 含 token | `https://xxx?token=yyy` | 只写域名，去掉 query string |
| 邮箱（可选脱敏） | `user@example.com` | 视场景，user 类型可记录 |

**正则参考（用于自动扫描）：**
```
sk-[a-zA-Z0-9]{20,}          # OpenAI/OpenRouter API Key
BSA[a-zA-Z0-9]{20,}          # Brave Search API Key
ghp_[a-zA-Z0-9]{36,}         # GitHub PAT
ya29\.[a-zA-Z0-9_-]+         # Google OAuth
[a-f0-9]{32,}                # 通用长 hex（可能是 token）
```

**原则：** 宁可多拦不漏。记忆文件中出现敏感信息时，记录"已配置 [服务] 凭证"即可，不需要记录具体内容。

### Session 启动时加载

```markdown
## Session Startup
1. 读 SOUL.md
2. 读 USER.md
3. 读 memory/YYYY-MM-DD.md（今天 + 昨天）
4. 如果是主 session：也读 MEMORY.md
```

---

## 与 AGENTS.md 集成

在 `AGENTS.md` 的 Session Startup 部分加入：

```markdown
## 记忆四类型
保存记忆时分类为 user/feedback/project/reference，写独立文件 + 更新 MEMORY.md 索引。
不保存可从代码推导的内容。MEMORY.md 每行 ≤150 字符，200 行截断。
```

---

## 与 Heartbeat 集成

在 HEARTBEAT.md 中加入定期记忆维护任务：

```markdown
- [ ] 每 3 天：读最近 daily log，提取重要事件更新 MEMORY.md
```

---

## 常见问题

**Q: 和 daily log 是什么关系？**
A: daily log 是原始流水账（什么都记），memory/ 下的四类型文件是提炼后的结构化记忆。
   好比：daily log = 日记本，memory/ = 笔记卡片。

**Q: 一个事件同时涉及 user 和 project 怎么办？**
A: 分别记录。user 文件记"用户偏好"，project 文件记"项目进展"。不要混在一起。

**Q: 可以跨 session 使用吗？**
A: 可以。所有 session 共享同一套 memory/ 目录和 MEMORY.md。
   但 MEMORY.md 只在主 session（直接对话）中加载，共享/群聊场景不加载以防泄露。

**Q: 需要脚本自动化吗？**
A: 可选。基本用法靠 agent 手动维护就够了。
   高级场景可以用 cron + 子代理做自动提取（类似 Claude Code 的 SessionMemory）。
