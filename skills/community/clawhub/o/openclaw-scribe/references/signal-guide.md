# Signal Classification Guide

How scribe classifies extracted signals from conversation history.

## Signal Types

### 🔑 Decisions Made
Concrete choices the user committed to during the conversation.

**Examples:**
- "用方案B，做成cron skill"
- "先发布到GitHub，再上ClawdHub"
- "不用 Claude，改用 GPT-4o"

**How to identify:** Look for user confirming an option, or clearly choosing a direction after alternatives were presented.

### 💡 Preferences & Rules
Standing preferences, constraints, or operating rules the user expressed.

**Examples:**
- "回复用中文"
- "不要问太多问题，自己想办法"
- "Moltbook 不要发主动推送"

**How to identify:** Instructions the user gives about *how* they want things done, not just what to do now.

### 🗣️ Framework Sentences
Strong directive phrases that reveal the user's communication style and expectations.

These are high-value memory — they tell the AI how to behave long-term.

**Examples:**
- "不管，你来决定"  → user delegates freely
- "做不到就换个方法，别来问我" → zero tolerance for blocking
- "一步一步来" → user prefers incremental execution
- "你自己安排，没效果拿你是问" → accountability expected

**How to identify:** Short, punchy phrases the user repeats or says with emphasis. Often imperative. Often reveal frustration with AI hedging.

### 📦 Project Updates
Progress, status changes, or new information about ongoing projects.

**Examples:**
- "TextZap 日报 cron 已配置，每天09:00运行"
- "Promptfolio profile 已发布: https://promptfolio.club/u/BMLpsezJE-"
- "Feishu bridge 服务已启动"

**How to identify:** Factual state changes about named projects or systems.

### ✅ Todos / Follow-ups
Tasks mentioned or planned but not confirmed complete in this session.

**Examples:**
- "需要把 scribe 发布到 ClawdHub"
- "下次验证 TextZap GA4 数据"
- "等用户确认 GitHub 仓库名"

**How to identify:** Future-tense plans, "下次", "待确认", or tasks where the agent said it would do something but the session ended.

## Quality Guidelines

- **Be specific**: "讨论了架构" is useless. "用户选择方案B（cron+skill）实现速记员" is useful.
- **Preserve quotes**: Framework sentences should be quoted verbatim when possible.
- **Skip noise**: Greetings, confirmations ("好的"), and pure question-answer exchanges without decisions.
- **Date context**: If a project update has a version or timestamp, include it.
