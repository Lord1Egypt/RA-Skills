---
name: personal-tutor
description: >
  🎓 Personal Tutor — Your private AI learning coach. 你的私人AI学习导师。
  Formerly knowledge-digest, now rebranded and upgraded to v1.0.1.
  原名 knowledge-digest，现已全面升级为 personal-tutor v1.0.1。
  Full-cycle learning management: start a subject → daily lessons → quizzes →
  three-layer post-lesson archiving (learning records + memory + knowledge base).
  全流程学习管理：开新课→每日上课→测验→三层课后归档（学习记录+记忆+知识库）。
  NEW in v1.0.1: Mandatory Post-Lesson Self-Verification Protocol — agent cannot
  declare "lesson complete" until all three archive layers are verified.
  v1.0.1 新增：强制课后自查协议——三层归档全部验证通过，agent 才能说"下课"。
  Trigger / 触发："start learning [subject]" / "开始学[科目]" /
  "continue [subject]" / "继续[科目]" / "update learning records" / "更新学习记录"。
  NOT for: casual Q&A, one-off lookups, non-learning conversations.
  不适用于：随手问答、一次性查询、非学习类对话。
version: 1.0.3
changelog: |
  v1.0.3 (2026-05-29):
  - Hardened Post-Lesson Self-Verification Protocol: added 🚨 red-line warning banner, self-check mantra (1️⃣2️⃣3️⃣), and explicit "user-caught-skipping" failure behavior.
  v1.0.2 (2026-05-29):
  - Updated description with bilingual rebranding announcement (knowledge-digest → personal-tutor).
  - Scenario 2: Added mandatory Post-Lesson Self-Verification Protocol; agent cannot declare "lesson complete" without checking all archive layers.
  - New section: Post-Lesson Self-Verification Protocol — a universal checklist for multi-agent scenarios.
  - Common Edge Cases: Added "Skipped Archiving" failure mode with recovery procedure.
  v1.0.0 (2026-05-28): Initial release.
metadata:
  tags: [learning, knowledge-management, obsidian, productivity, education, study, note-taking]
---

# Personal Tutor — Full-Cycle Learning Management / 全流程学习管理系统

## Overview / 概述

Personal Tutor turns every learning session into structured, searchable, long-term knowledge. It handles three scenarios / 三个场景：

1. **Start a new subject / 开启新学科** — create syllabus, learning log, config entries
2. **Daily lesson / 每日上课** — review → teach → quiz → prompt to archive
3. **Post-lesson archive / 课后归档** — update 6 layers: log, syllabus, memory, knowledge base, index, config

---

## First-Run Onboarding / 首次设置引导

Before executing any workflow, check for a config file at:

```
{workspace}/.personal-tutor-config.json
```

If it does **not** exist, run the onboarding flow / 如不存在则运行引导流程：

### Onboarding Flow / 引导问题

Ask the user these questions (one at a time, or all at once if they prefer)：

1. **Learning root directory / 学习资料根目录** — Where should subject folders be stored?
   - Example: `D:\Learning\` or `~/Documents/Learning/`
   - This is where syllabus files and learning logs live.

2. **Knowledge base tool / 知识库工具** — What do you use for long-term notes?
   - `obsidian` — wikilinks (`[[link]]`), vault-based
   - `plain` — standard Markdown, folder-based / 纯文件夹
   - `notion` — notes only (API integration not included)
   - `none` — skip concept archiving entirely / 跳过概念归档

3. **Knowledge base path / 知识库路径** (if tool ≠ `none`) — Where is your vault/notes root?
   - Example: `D:\Obsidian\MyVault\` or `~/Notes/`

4. **Archive depth / 归档深度** — How thorough should post-lesson archiving be?
   - `light` — update log + syllabus + memory only / 仅更新记录+大纲+记忆
   - `full` — light + extract concepts to knowledge base + refresh index / 完整归档含概念入库+索引刷新

5. **Preferred language / 内容语言** — `zh` (Chinese), `en` (English), `zh-en` (bilingual / 中英双语), or `auto` (follow user's language)

6. **Knowledge base schema / 知识库规则文件** (if tool = `obsidian` or `plain`) — Do you have a rules file that defines how concepts should be structured, named, and linked?
   - If yes, provide the path (e.g., `D:\Notes\WIKI-SCHEMA.md`). This file will be read before every concept extraction and its rules **take priority** over built-in defaults.
   - If no, the built-in Knowledge Base Rules (see section below) will be used.

### Config File Schema / 配置文件结构

After onboarding, create:

```json
{
  "version": "1.0",
  "learningRoot": "/path/to/learning/",
  "knowledgeBase": {
    "tool": "obsidian",
    "path": "/path/to/vault/",
    "schemaPath": "/path/to/WIKI-SCHEMA.md"
  },
  "archiveDepth": "full",
  "language": "auto",
  "subjects": {}
}
```

The `subjects` field will be populated as new subjects are added.

---

## Scenario 1: Starting a New Subject / 场景一：开启新学科

### Trigger / 触发条件

User says "start learning [subject name]" or "open a new subject: [name]"。
中文触发："开启[学科名]学习"、"新建学科[学科名]"。

### Workflow / 工作流

1. **Read config / 读取配置** — Load `.personal-tutor-config.json` to get `learningRoot` and preferences.

2. **Detect category structure / 检测分类结构** — Scan `{learningRoot}/` for existing subdirectories:
   - If subdirectories exist (e.g., `大学专业知识/`, `职业发展/`, `Academic/`, `Professional/`), they are treated as **categories / 分类**。Present them to the user and ask which one the new subject belongs to. If none fit, offer to create a new category.
   - If `{learningRoot}/` is flat (no subdirectories), the subject goes directly under `{learningRoot}/`.
   - Store the chosen category in the subject's config entry as `category`.

3. **Create subject directory / 创建学科目录** — Under `{learningRoot}/{category}/` (or `{learningRoot}/` if no category), create a folder named after the subject.

4. **Create syllabus file / 创建教学大纲** — `{learningRoot}/{category}/{subject}/syllabus.md`
   - Content: subject overview, learning objectives, phased plan (by day/week), key topics per phase, estimated completion, expected outcomes.
   - If the user provides specific goals or a textbook, incorporate them.
   - Leave the first phase/day marked as `⏳ Pending / 待学`.

5. **Create learning log file / 创建学习记录** — `{learningRoot}/{category}/{subject}/learning-log.md`
   - Content: an empty tracking table with columns: Date | Content | Mastery | Issues | Next
   - Initial entry: today's date, "Subject initialized", N/A, "None", "Day 1 — start learning"

6. **Update config / 更新配置** — Add to `subjects`:
   ```json
   "subject-name": {
     "currentDay": 1,
     "category": "大学专业知识",
     "syllabusPath": "{learningRoot}/{category}/{subject}/syllabus.md",
     "logPath": "{learningRoot}/{category}/{subject}/learning-log.md",
     "status": "active",
     "startedAt": "YYYY-MM-DD"
   }
   ```

7. **Update memory / 更新记忆** — If the agent has a memory system (MEMORY.md or equivalent), record the new subject there.

8. **Create knowledge base folder / 创建知识库文件夹** (if `archiveDepth` = `full` and `knowledgeBase.tool` ≠ `none`) — Create an empty subject folder under `{knowledgeBase.path}/` if it doesn't exist.

9. **Report / 汇报** (output in configured language，按配置语言输出):

```
✅ New subject "[Subject Name]" is ready. / 新学科"[学科名]"已开启。

Created / 已创建：
  📋 Syllabus: {category}/{subject}/syllabus.md
  📝 Learning log: {category}/{subject}/learning-log.md
  ⚙️  Config updated / 配置已更新

You're all set for Day 1. Say "start learning [subject]" when ready.
```

---

## Scenario 2: Daily Lesson / 场景二：每日上课

### Trigger / 触发条件

User says "start learning [subject]" or "continue [subject]"。
中文触发："开始[学科名]学习"、"继续[学科名]学习"。

### Workflow / 工作流

1. **Read config / 读取配置** — Load current progress from `.personal-tutor-config.json`.

2. **Read syllabus and log / 读取大纲与记录** — Load `syllabus.md` and `learning-log.md` to understand where we are.

3. **Review previous lesson / 回顾上节课** — Briefly summarize the last session's core content (read from the learning log). Keep it under 3 bullet points.

4. **Teach new content / 讲授新知** — Deliver the next topic(s) according to the syllabus. Follow these teaching principles:
   - Start with "why this matters" before "how it works" / 先讲"为什么重要"再讲"怎么运作"
   - Use concrete examples before abstract definitions / 用具体例子引导抽象定义
   - Break complex topics into digestible chunks / 把复杂话题拆成可消化的模块
   - Pause for questions between major sections / 大段落之间主动询问

5. **Interactive check / 互动测验** (if applicable to the subject) — Ask 2-5 questions to verify understanding. Wait for user's answers, then give feedback and corrections.

6. **Session notes / 课堂记录** — Mentally record: what was covered, what the user struggled with, what needs review.

7. **Post-Lesson Self-Verification / 课后自查（强制执行）** — Before telling the user the lesson is complete, run the **Post-Lesson Self-Verification Protocol** (see dedicated section below). If any layer is missing, fix it immediately. Do NOT say "lesson complete" / "学完了" / "done" until all layers pass.

8. **End prompt / 课堂结束语** (only after self-verification passes, output in configured language):

```
📚 Today's lesson on [Subject] (Day [N]) is complete. / 今日课程完成。

Covered / 内容: [brief summary]
Mastery / 掌握: [assessment]
Issues / 问题: [any problems noted]

✅ Archive verified / 归档自检:
  📁 Learning records: updated
  🧠 Knowledge base: [N concepts created/updated, or "no changes"]
  ⚙️  Config: updated

Ready for Day [N+1]! / 准备好下一课了！
```

---

## Scenario 3: Post-Lesson Archive / 场景三：课后归档

### Trigger / 触发条件

User says "update learning records" or "archive today's learning"。
中文触发："更新学习记录"、"归档今天的学习"。

### Workflow / 工作流

This is the most important scenario — it turns a conversation into permanent knowledge.
这是最关键的步骤——把对话变成永久知识。

### Step 1: Update Learning Log / 更新学习记录

Append to the learning log (path from config):

```markdown
## Day [N] — YYYY-MM-DD

**Content / 内容:** [summary of what was covered]
**Mastery / 掌握程度:** [good / okay / needs review]
**Quiz results / 测验成绩:** [scores & wrong answers if applicable]
**Issues / 遇到问题:** [concepts the user struggled with]
**Next / 下一步:** Day [N+1] — [next topic from syllabus]
```

### Step 2: Update Syllabus Progress / 更新大纲进度

In `syllabus.md`, mark the current phase/day as `✅ Complete / 完成`. If a milestone was reached, note it.

### Step 3: Update Config / 更新配置

In `.personal-tutor-config.json`, update:
```json
"subject-name": {
  "currentDay": N+1,
  ...
}
```

### Step 4: Update Memory / 更新记忆

If the agent has a memory system, update it with the subject's new progress.

### Step 5: Extract Concepts to Knowledge Base / 提取概念入库

**Only if `archiveDepth` = `full` and `knowledgeBase.tool` ≠ `none`.**

Follow the **Knowledge Base Rules** section below. If a custom `schemaPath` is configured, read that file first — its rules take priority over built-in defaults.

从当日课程提炼核心概念，严格按照下方「知识库规则」章节执行。如配置了自定义 schema 文件，先读取它——其规则覆盖内置默认。

**If no new concepts were introduced:** note this in the report / 如无新概念，在汇报中说明。

### Step 6: Report / 汇报 (output in configured language)

```
✅ Learning records updated. / 学习记录已更新。

  📚 Subject: [Subject Name]
  📍 Progress: Day [N] → Day [N+1]
  🆕 New concepts: [list, or "none"]
  📁 Archived to: {path}
  🧠 Knowledge base: [updated / no changes]
  ⚙️  Config updated / 配置已更新
```

---

## Post-Lesson Self-Verification Protocol / 课后自查协议（v1.0.1 新增）

> 🚨 **THIS IS A RED LINE. DO NOT CROSS IT.**
> 这是红线。不可越界。
>
> Every agent that teaches a lesson via this skill **MUST** self-verify all three layers below before telling the user "lesson complete" ("学完了"/"done"/etc). If any layer is missing, **you are NOT done.** There is no exception. There is no "I'll do it later." Fix the gap now.
>
> 每个使用此 skill 教课的 agent，在告诉用户"学完了"之前，**必须**自检以下三层。少一层就不是"学完了"。没有例外。没有"待会补"。现在修。

After every lesson (whether triggered via Scenario 2 or via the agent's own workflow), the agent MUST self-verify the following three layers before declaring the session complete:

### The Three-Layer Verification / 三层验证

| # | Layer / 层 | What to check / 检查内容 | How to verify / 验证方式 |
|:-:|-----------|------------------------|------------------------|
| 1 | 📁 **Learning Records** / 学习记录 | Learning log appended with new knowledge + quiz results; syllabus marked as complete | Read the last few lines of the log file; check syllabus for ✅ mark |
| 2 | 🧠 **Agent Memory** / 智能体记忆 | MEMORY.md or equivalent updated with current progress | Read the subject's progress line in memory |
| 3 | 📝 **Knowledge Base** / 知识库 | Each core concept has its own `.md` file with proper frontmatter, bilingual content, and wikilinks | List files in the subject's knowledge base folder; verify new files exist and are non-empty |

### Self-Check Mantra / 自查口诀

Before saying anything that means "done", mentally run this checklist:

```
1️⃣ D盘/Learning records → ✅ ?
2️⃣ Agent memory → ✅ ?
3️⃣ Knowledge base → ✅ ?
→ All three checked? NOW you can say "lesson complete."
```

### When to skip Layer 3 / 何时可跳过第三层

Only skip knowledge base archiving if:
- `archiveDepth` is set to `light` (not `full`), OR
- `knowledgeBase.tool` is set to `none`, OR
- The lesson was pure review with zero new concepts introduced

In all other cases, Layer 3 is mandatory.

### Failure Recovery / 故障恢复

If any verification fails:
1. **Do NOT tell the user the lesson is complete** — fix the gap first
2. If the gap cannot be fixed (e.g., missing path), report it to the user with a clear description
3. Record the failure in the learning log so the next session can catch up

**If the user catches you skipping a layer** (they will notice):
- Stop immediately. Do not argue. Do not defend.
- Fix the missing layer right there.
- Record this as a lesson learned — update your own rules (SOUL.md, TOOLS.md, etc.) to make it harder to skip next time.

### Multi-Agent Guarantee / 多智能体保障

This protocol is designed for environments where different agents may handle different sessions. Each agent is independently responsible for completing all three layers. Do not assume a previous agent already did it — verify.

---

## Knowledge Base Rules / 知识库规则（内置默认）

> ⚠️ If a custom `schemaPath` is configured, read that file before every concept extraction — its rules take priority over the defaults below.
> 如配置了自定义 schema 文件，每次提取概念前先读取它——其规则优先于以下默认。

When extracting concepts from a lesson, follow these rules strictly:
从课程提炼概念时，严格遵循以下规则：

### 1. One Concept = One File / 一个概念一个文件

- Each core concept gets its own `.md` file. Never bundle multiple concepts into one file.
- File name format: `{NN}-{ConceptName}.md` (e.g., `01-Derivative.md`, `01-导数.md`)
- Use a numbered prefix to maintain sort order within the folder.
- Place files in the appropriate subject folder under `{knowledgeBase.path}/`.

### 2. File Format / 文件格式

Every concept file must include:

```markdown
---
aliases:
  - ConceptName
  - 别名1
  - 别名2
---

# ConceptName / 概念名

> One-line summary. 一句话概述。

## Core Content / 核心内容
...

## Related / 关联
- [[path/to/related-concept|Related Concept]] — relationship description
```

- **YAML frontmatter with `aliases`** — list synonyms and translations for searchability
- Output language follows the user's configured `language` setting
- If `language` = `zh-en`, output bilingual (Chinese + English)

### 3. Naming & Linking / 命名与链接

**Obsidian (wikilink) mode:**
- Use `[[full/path/to/file|Display Name]]` format — full path from vault root, pipe (`|`) without spaces
- Always reference the numbered filename (e.g., `[[01-Derivative]]`, not `[[Derivative]]`)
- Cross-discipline links: `[[OtherFolder/SomeFile|Display]]`

**Plain Markdown mode:**
- Use standard relative links: `[Display Name](../folder/file.md)`

**Bidirectional linking / 双向链接:**
- If A links to B, also add a backlink from B to A (create or update B's file)
- Tag cross-discipline links with type hints: `💡 方法借鉴` (method reference), `💡 思维模型类比` (mental model analogy)

### 4. Duplicate Detection / 去重检查

Before creating any new file, check for existing content:

1. Search for files with the same or similar name (including `aliases` in frontmatter)
2. If an exact match exists → add a wikilink to it, do NOT create a duplicate / 已存在则不新建，直接引用
3. If partial overlap → enrich the existing file with new content, do NOT create a duplicate / 部分重叠则补充已有文件
4. If contradictory content found → mark `⚠️ 待确认` and flag to the user / 发现矛盾则标记待确认

### 5. Index & Outline Updates / 索引与总纲更新

If the knowledge base has an index file (e.g., `00_概念索引.md`) or subject outlines (e.g., `XX-XXX总纲.md`):

- Add new concepts to the index under the correct subject
- Update the subject outline to include new concept entries with correct wikilink paths
- Verify that outline links point to actual files on disk
- If the knowledge base has a link-checking script, run it after major updates

### 6. Post-Archive Verification / 归档后验证

After creating or modifying knowledge base files:

1. Verify all new wikilinks resolve to existing files
2. Check numbering consistency within the subject folder (no gaps or collisions)
3. Report any broken links or inconsistencies to the user

---

## Configuration Reference / 配置参考

### `.personal-tutor-config.json`

| Field | Type | Description |
|:------|:-----|:------------|
| `version` | string | Config schema version (`"1.0"`) |
| `learningRoot` | string | Absolute path to the learning directory / 学习资料根目录 |
| `knowledgeBase.tool` | string | `"obsidian"` / `"plain"` / `"notion"` / `"none"` |
| `knowledgeBase.path` | string | Absolute path to vault/notes root / 知识库路径 |
| `knowledgeBase.schemaPath` | string | (Optional) Path to custom knowledge base rules file / 自定义规则文件路径 |
| `archiveDepth` | string | `"light"` (log + syllabus + memory) or `"full"` (includes knowledge base + index) |
| `language` | string | `"zh"` / `"en"` / `"zh-en"` / `"auto"` |
| `subjects` | object | Keyed by subject name, each containing `currentDay`, `category`, `syllabusPath`, `logPath`, `status`, `startedAt` |

### Directory Structure / 目录结构 (after setup)

```
{learningRoot}/
├── {Category/分类}/
│   ├── {Subject Name/学科名}/
│   │   ├── syllabus.md
│   │   └── learning-log.md
│   └── {Another Subject}/
│       ├── syllabus.md
│       └── learning-log.md
├── {Another Category}/
│   └── ...
└── ...

{knowledgeBase.path}/
├── {Subject Name}/
│   ├── 01-concept.md
│   ├── 02-concept.md
│   └── ...
└── (existing vault structure preserved / 现有结构保留)
```

---

## Design Principles / 设计原则

1. **Progressive disclosure / 渐进展开** — Lightweight onboarding, fully optional deep features
2. **Tool-agnostic / 工具无关** — Works with Obsidian, plain folders, or no knowledge base at all
3. **Conversation-first / 对话优先** — The lesson happens in chat; the skill handles the paperwork behind the scenes
4. **Incremental / 增量式** — Each day builds on the last; the log and syllabus grow together
5. **Non-destructive / 非破坏性** — Never overwrite existing knowledge base content; always check for duplicates first
6. **Language-respecting / 语言自适应** — Follow the user's configured language for all generated content

---

## Common Edge Cases / 常见边缘情况

| Situation / 情况 | Handling / 处理方式 |
|:----------|:---------|
| User forgot which day they're on / 忘记学到哪了 | Read config → `currentDay`, confirm with user |
| User wants to skip ahead / 想跳过某天 | Update config to the new day, note in log |
| User restarted a subject from scratch / 重启学科 | Archive old log (rename with date suffix), create fresh files |
| Multiple subjects in one session / 同一会话多学科切换 | Process each archive command independently |
| Knowledge base tool is `none` / 未配置知识库 | Silently skip Steps 5-6 in Scenario 3 |
| Config file is corrupted/missing / 配置文件损坏或缺失 | Re-run onboarding; old learning files are preserved |
| Subject name has special characters / 学科名含特殊字符 | Sanitize for filesystem: replace `<>:"/\|?*` with `-` |
| **Agent skipped knowledge base update / Agent 漏了知识库归档** | **v1.0.1 新增**。This is the most common failure mode. Recovery: (1) Check if the subject folder exists at `{knowledgeBase.path}`; (2) Read the latest learning log to identify which concepts were taught; (3) Create/update `.md` files for each missing concept; (4) Run Post-Lesson Self-Verification Protocol; (5) This failure suggests the agent DID read the skill but skipped verification — after recovery, the agent should update its local rules (SOUL.md, TOOLS.md, etc.) to prevent recurrence. |
