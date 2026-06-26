---
name: openclaw-memory-transfer
description: |
  Zero-friction memory migration from other AI assistants (ChatGPT, Claude.ai, Gemini, Copilot, Perplexity, Cursor, Windsurf, etc.) into OpenClaw.
  Triggers: "migrate from ChatGPT", "I used to use Gemini", "import my memory", "memory transfer",
  "bring my data from X", "switch from ChatGPT", "迁移记忆", "从ChatGPT搬过来", "记忆导入",
  "I'm coming from Claude", "transfer my preferences", "import from Cursor".
  Supports both cloud-based AI (prompt-guided export) and local agents (automatic file scanning).
  Parses ChatGPT data export ZIP files for zero-effort migration.
---

# Memory Transfer — Cross-Agent Migration for OpenClaw

Migrate memories, preferences, writing style, and workflow data from any AI assistant into OpenClaw. Zero learning curve — just say where you came from.

## Language Rule

All user-facing messages in this skill MUST match the user's language (from USER.md or detected from conversation). The examples below show both English and Chinese variants — pick the one that matches.

## Quick Reference

| Source | Method | User Effort |
|--------|--------|-------------|
| ChatGPT | ZIP data export (auto-parse) | Click export in settings, upload ZIP |
| ChatGPT (alt) | Prompt-guided | Copy prompt → paste result back |
| Claude.ai | Prompt-guided | Copy prompt → paste result back |
| Gemini | Prompt-guided | Copy prompt → paste result back |
| Copilot | Prompt-guided | Copy prompt → paste result back |
| Perplexity | Prompt-guided | Copy prompt → paste result back |
| Claude Code | Auto-scan local files | None |
| Cursor | Auto-scan local files | None |
| Windsurf | Auto-scan local files | None |

## Flow

### Step 1: Identify Source

Ask the user one question:

> **EN:** Which AI assistant are you coming from?
> **ZH:** 你之前用的是哪个 AI 助手？

If the user already mentioned it (e.g., "I used ChatGPT for a year"), skip this step.

Determine the migration path:
- **Cloud AI** (ChatGPT, Claude.ai, Gemini, Copilot, Perplexity) → Step 2A or 2B
- **Local Agent** (Claude Code, Cursor, Windsurf) → Step 2C

### Step 2A: ChatGPT ZIP Export (Preferred for ChatGPT)

This is the **easiest and most complete** method for ChatGPT users.

**EN version:**
> The easiest way — export your ChatGPT data:
>
> 1. Open ChatGPT → Settings → Data Controls → Export Data
> 2. Click "Export" — you'll receive an email
> 3. Download the ZIP file and send it to me
>
> I'll automatically parse all your conversations, memories, and preferences.

**ZH version:**
> 最简单的方式——去 ChatGPT 导出你的数据：
>
> 1. 打开 ChatGPT → Settings → Data Controls → Export Data
> 2. 点 "Export"，你会收到一封邮件
> 3. 下载 ZIP 文件，直接发给我
>
> 我会自动解析你所有的对话记录、记忆和偏好。

When the user uploads the ZIP, run the parser:

```bash
node <skill_dir>/scripts/parse-chatgpt-export.js "<path_to_zip>"
```

The parser outputs a structured JSON to stdout. Read and process it.

If the user doesn't want to wait for the email or prefers a faster method, fall back to Step 2B.

### Step 2B: Prompt-Guided Export (All Cloud AIs)

Tell the user to open a **new conversation** with their old AI and send the export prompt.

**Important:** Give the prompt in the user's primary language. If the user chats in Chinese, give the Chinese prompt — this ensures the old AI responds in Chinese too, preserving the original context.

**EN version — tell the user:**
> Go to your old AI, start a new chat, and send it this message. Then copy the response back to me.

**ZH version — tell the user:**
> 去你之前的 AI 那里，开一个**新对话**，把下面这段话发给它，然后把回复复制给我。

---

**Export Prompt (English):**

```
I'm migrating to a new AI assistant and need a complete export of everything you know about me. Please provide ALL of the following in a single, well-structured response:

## 1. Stored Memories
List every memory you have stored about me. Output verbatim — do not summarize or paraphrase.

## 2. Custom Instructions
Reproduce my complete custom instructions / personalization settings. If empty, say so.

## 3. Identity & Context
- My name, profession, industry
- Tools and platforms I use regularly
- Languages I work in

## 4. Communication Preferences
- My writing style (tone, sentence length, vocabulary level, quirks)
- How I like information structured and presented
- Formatting preferences (bullet points vs prose, headers, code blocks)

## 5. Behavioral Patterns
- What I ask you to help with most (rank by frequency)
- Recurring projects or workflows
- Strong opinions or preferences I've expressed
- Things I've told you NOT to do — list every correction

## 6. Topics & Interests
- Subjects I discuss frequently
- Areas of expertise
- Curiosities and learning goals

Be exhaustive. Better to include too much than too little. Format as a reference document, not conversational text. This will be directly imported into another AI's memory system.
```

**Export Prompt (中文):**

```
我正在迁移到另一个 AI 助手，需要你把关于我的一切都导出来。请在一次回复中提供以下所有内容，用清晰的结构输出：

## 1. 存储的记忆
列出你存储的关于我的每一条记忆，原文输出，不要总结或改写。

## 2. 自定义指令
完整复现我的自定义指令/偏好设置。如果为空请说明。

## 3. 身份与背景
- 我的姓名、职业、行业
- 我常用的工具和平台
- 我使用的语言

## 4. 沟通偏好
- 我的写作风格（语气、句子长度、词汇水平、表达习惯）
- 我喜欢信息怎么组织和呈现
- 格式偏好（列表还是段落、标题、代码块）

## 5. 行为模式
- 我最常让你帮忙做什么？按频率排序
- 反复出现的项目或工作流
- 我表达过的强烈观点或偏好
- 我纠正过你什么？让你不要做什么？列出所有"别这样"的模式

## 6. 话题与兴趣
- 我经常讨论的话题
- 我的专业领域
- 我的好奇心和学习目标

尽可能详尽，宁可多不可少。用参考文档格式输出，不要用对话体。这些内容将直接导入另一个 AI 的记忆系统。
```

---

When the user pastes the result back, proceed to Step 3.

### Step 2C: Local Agent Auto-Scan

For local agents, scan files automatically. No user action needed.

**Claude Code:**
```bash
# Global config
cat ~/.claude/CLAUDE.md 2>/dev/null

# All project memories
find ~/.claude/projects -name "*.md" -path "*/memory/*" 2>/dev/null | head -20 | while read f; do
  echo "=== $f ==="
  cat "$f"
done

# Project instructions
find ~/.claude/projects -name "CLAUDE.md" 2>/dev/null | head -20 | while read f; do
  echo "=== $f ==="
  cat "$f"
done
```

**Cursor:**
```bash
cat ~/.cursor/rules/*.md 2>/dev/null
find . -maxdepth 3 -name ".cursorrules" 2>/dev/null | head -10 | while read f; do
  echo "=== $f ==="
  cat "$f"
done
```

**Windsurf:**
```bash
cat ~/.windsurf/rules/*.md 2>/dev/null
find . -maxdepth 3 -name ".windsurfrules" 2>/dev/null | head -10 | while read f; do
  echo "=== $f ==="
  cat "$f"
done
```

**Generic (AGENT.md / CLAUDE.md / rules files):**
```bash
find ~ -maxdepth 4 \( -name "AGENT.md" -o -name "CLAUDE.md" -o -name ".cursorrules" -o -name ".windsurfrules" \) 2>/dev/null | head -20 | while read f; do
  echo "=== $f ==="
  cat "$f"
done
```

After scanning, present what was found and proceed to Step 3.

### Step 3: Parse & Categorize

Process the imported data (whether from ZIP, prompt response, or local scan) into these categories:

**KEEP:**
- Identity (name, profession, industry, language)
- Writing style and communication preferences
- Tools, platforms, tech stack
- Active projects and workflows
- Structural preferences (how to organize/present info)
- "Don't do this" rules and corrections
- Domain knowledge and expertise areas
- Behavioral patterns and habits

**FILTER OUT:**
- Completed one-off tasks
- Outdated context (finished projects, old deadlines)
- Source-specific references ("as a ChatGPT user...")
- API keys, tokens, passwords — **never migrate credentials**
- Hallucinated or inaccurate memories (flag suspicious ones)
- Duplicate or redundant entries

### Step 4: Review & Confirm

Present the cleaned data to the user, organized by destination:

**EN:**
> 📋 **Migration Preview**
>
> **Writing to USER.md (your profile):**
> - Name: ...
> - Profession: ...
> - Language: ...
> - Communication style: ...
>
> **Writing to MEMORY.md (long-term memory):**
> - [project/knowledge/experience entries...]
>
> **Writing to TOOLS.md (tool preferences):**
> - Tools: ...
> - Platforms: ...
>
> Anything to change? I'll write it once you confirm.

**ZH:**
> 📋 **迁移预览**
>
> **写入 USER.md（你的画像）：**
> - 姓名：...
> - 职业：...
> - 语言偏好：...
> - 沟通风格：...
>
> **写入 MEMORY.md（长期记忆）：**
> - [项目/知识/经验条目...]
>
> **写入 TOOLS.md（工具偏好）：**
> - 常用工具：...
> - 平台配置：...
>
> 有什么要改的吗？确认后我就写入。

Wait for user confirmation. They can:
- Approve all
- Remove specific items
- Edit entries
- Add things that were missed

### Step 5: Write to Memory System

After confirmation, write to the appropriate files:

**USER.md** — Identity, communication preferences, language, timezone
**MEMORY.md** — Knowledge, projects, experience, behavioral patterns
**TOOLS.md** — Tools, platforms, environment-specific notes

Rules for writing:
- **Merge, don't overwrite** — if these files already have content, integrate new data with existing
- **Preserve structure** — follow the existing format of each file
- **Add a migration note** — append a comment like `<!-- Migrated from ChatGPT on 2026-03-30 -->`
- **Use the user's language** — write entries in the language the user communicates in

### Step 6: Verify

After writing, confirm:

**EN:**
> ✅ **Migration complete!**
>
> Here's what I now know about you:
> [Brief summary of key imported info]
>
> This info is now in my memory system — I'll use it naturally in our conversations.
> Feel free to tell me if anything needs updating.

**ZH:**
> ✅ **迁移完成！**
>
> 现在我知道的关于你的事：
> [Brief summary of key imported info]
>
> 这些信息已经写入我的记忆系统，以后的对话中我会自然地使用它们。
> 随时可以告诉我补充或修正任何内容。

## Special Cases

### Multiple Sources
If the user used several AI assistants, handle them sequentially. Deduplicate across sources before writing.

### Partial Migration
User might say "just bring over my writing preferences" — respect scope limits. Only migrate what they want.

### Conflict Resolution
If imported data conflicts with existing memory (e.g., different profession noted), ask the user which is current.

### Re-migration
If the user runs migration again later, merge new data with existing. Don't create duplicates.

## Platform-Specific Notes

### ChatGPT Data Export ZIP Structure
```
├── conversations.json       ← Main conversation history
├── model_comparisons.json   ← Model comparison data
├── message_feedback.json    ← Thumbs up/down data
├── shared_conversations.json
├── user.json               ← Account info
└── chat.html               ← Rendered conversations
```

The parser (`scripts/parse-chatgpt-export.js`) extracts:
- User messages patterns and topics
- Correction patterns (user said "no, I meant...")
- Frequently discussed subjects
- Writing style from user messages
- Tool/platform mentions (word-boundary-aware detection)
- Project references

### Claude.ai
Users can access their memory at claude.ai → Settings → Memory. They can either:
1. Use the prompt method (Step 2B)
2. Manually copy their memory entries

### Gemini
Gemini stores "Saved Info" in Settings. Prompt method works best.

### Copilot
Limited memory capabilities. Prompt method captures what's available.

## Security

- **NEVER migrate API keys, tokens, or credentials**
- Warn user if imported text contains what looks like secrets (regex: `/(?:sk-|ghp_|token|password|secret|key)\s*[:=]/i`)
- All imported data is shown to user before writing — no silent imports
- ZIP files are processed in temp directory with path traversal protection, cleaned up after
