---
name: openclaw-never-forget
description: The ultimate bilingual (English/Chinese) memory management engine for Openclaw. Combines episodic daily logging, 30-minute short-term contextual snapshots, long-term semantic knowledge extraction, and intelligent on-demand retrieval to completely solve context amnesia and build a continuous second brain. 终极双语记忆管理引擎。结合每日情景日志、30分钟短期上下文快照、长期语义知识提取与智能按需检索，彻底解决上下文遗忘，持续构建第二大脑。
---

# Openclaw Never Forget Skill (全知记忆管理引擎)

## 🎯 核心愿景 (Core Vision)
This is a unified memory system designed to transform Openclaw from a stateless assistant into an evolving entity with continuous, reliable context. It merges **short-term anti-amnesia tactics** (periodic snapshots) with **long-term knowledge structuring** (semantic extraction and daily logs).
这是一个统一的记忆系统，旨在将 Openclaw 从无状态助手转变为具有连续、可靠上下文的不断进化的实体。它将**短期防遗忘战术**（定期快照）与**长期知识结构化**（语义提取和每日日志）结合在一起。

## 🧠 记忆层级架构 (Memory Architecture Tiers)

1. **Episodic Memory (情景记忆) - `memory/YYYY-MM-DD.md`**
   - **What**: The chronological journal of the day. (当天的按时间顺序记录的日志表。)
   - **Contents**: Task logs, errors encountered, successful actions, and 30-minute short-term context summaries. (任务执行日志、遇到的错误、成功的操作以及每30分钟的短期上下文总结。)

2. **Semantic Memory (语义记忆) - `memory/MEMORY.md` (or core knowledge files)**
   - **What**: The distilled, timeless facts and rules learned about the user and their projects. (关于用户及其项目的经过提炼的、永久的事实和规则。)
   - **Contents**: Preferences, recurring workflows, API keys context (not raw), important structural decisions. (偏好设置、重复出现的工作流、重要的结构性决策。)

## ⚙️ 触发与运行机制 (Triggers & Execution Logic)

### 阶段 1: 隐性后台运转 (Phase 1: Silent Background Operations)
**Trigger**: Continuous during active sessions. (活跃对话期间持续进行。)

- **00:00 Daily Boot (每日零点初始化)**: 
  - On the first prompt of a new day, verify the existence of `memory/YYYY-MM-DD.md`. Create it with a standard template if missing.
  - (在每天的第一次对话时，验证并初始化当天的记忆文档。)
- **30-Minute Checkpoint (30分钟强制快照)**: 
  - *Action*: Every 30 minutes of active interaction, briefly summarize the immediate context (What are we building? What bugs are we fixing?).
  - *Storage*: Append this snapshot seamlessly under the current time block in today's Episodic Memory file.
  - (每活跃30分钟，简要总结当前的即时上下文，并静默追加到当天的情景记忆文件中，以此防止长文本窗口溢出。)
- **Insight Extraction (洞察提取)**:
  - *Action*: If a significant decision is made, a rule is established by the user, or a major task completes, extract the "Core Knowledge" and append it to the long-term `memory/MEMORY.md`.
  - (如果做出了重大决定、用户确立了规则或重大任务完成，自动提取“核心知识”并追加到长期的 `memory/MEMORY.md` 中。)

### 阶段 2: 显性主动检索 (Phase 2: Explicit Active Retrieval)
**Trigger**: Explicit user commands like "let openclaw recall previous chats", "what did we do yesterday?", "review my preferences", "让openclaw回忆之前的聊天", "我们昨天做了什么". (明确的用户指令触发。)

- **Action**: Use tools like `memory_get` or `memory_search` (if available in your environment) to read the relevant `YYYY-MM-DD.md` files or the global `MEMORY.md`.
- **Synthesis**: Do not just paste raw logs. Analyze the retrieved data and provide a coherent, synthesized summary bridging the past memory with the current prompt's needs.
- (使用文件读取机制快速调取相关日期的记忆文件或全局知识库。分析提取的数据，提供一个连贯、综合的总结，将过去的记忆与当前提示的需求连接起来。)

## 📝 存储规范与模板 (Storage Standards & Templates)

### 1. Daily Episodic Template (`memory/YYYY-MM-DD.md`)
```markdown
# Openclaw Daily Log - [YYYY-MM-DD]

## 🕒 [HH:MM] - [HH:MM] | Session Snapshot (30-Min Interval)
- **Current Task (当前任务)**: [What is being worked on / 正在处理的内容]
- **Context/Decisions (关键上下文)**: [Why we are doing this, chosen approach / 为什么这么做，选择的方案]
- **Progress/Artifacts (进度与产出)**: [Files created/modified, blockers hit / 修改的文件，遇到的阻碍]
```

### 2. Global Semantic Template (`memory/MEMORY.md`)
```markdown
# Openclaw Core Knowledge Base

## 👤 User Preferences (用户偏好)
- [Example: Always use verbose logging in Python scripts / Python 脚本中始终使用详细日志]

## 🏗️ Project Architectures (项目架构知识)
- **[Project Name]**: [Core tech stack, main directories, critical rules / 核心技术栈，主要目录，关键规则]
```

## ⚠️ 严守的铁律 (Ironclad Directives)
1. **Never Hallucinate History (绝不伪造历史)**: If you are asked to recall something and cannot find it in the `memory/` files, state clearly that you do not have a record of it. (如果被要求回忆某事但在 `memory/` 文件中找不到，请明确声明没有相关记录，严禁编造。)
2. **Compress Not Truncate (压缩而非截断)**: When making a 30-minute snapshot, compress the dialogue into high-density bullet points. Do not just copy-paste verbatim dialogue, which defeats the purpose of saving tokens. (在制作 30 分钟快照时，将对话压缩成高密度的要点。不要逐字复制粘贴对话，那会失去节省 token 的意义。)
3. **Immutability of the Past (过去的不可变性)**: When writing to `YYYY-MM-DD.md`, **only append** to the end of the file. Do not rewrite historical entries from earlier in the day unless explicitly fixing a critical factual error directed by the user. (写入每日档案时，**只能追加**到文件末尾。不要重写当天早些时候的过往条目。)
4. **Bilingual Output (双语输出适应)**: The skill dictates behavior in both English and Chinese. Your summaries written into the markdown files should dynamically match the primary language the user is speaking at that moment. (写入 markdown 文件的总结应动态匹配用户当时使用的主要语言。)
