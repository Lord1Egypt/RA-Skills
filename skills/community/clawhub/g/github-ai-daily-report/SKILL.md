---
name: ai-daily-report
description: Daily AI digest skill. Fetches trending GitHub AI/LLM/agent projects and Hacker News discussions, formats a structured report with value analysis, sends it to a user via Feishu, and prepends it to a Feishu document (newest-first). Use when asked to run, generate, or schedule a daily AI report. Triggers on phrases like "run AI daily report", "generate today's AI digest", "日报", "AI日报".
---

# AI Daily Report Skill

Fetch trending AI/LLM projects from GitHub and HN, format a structured daily digest, deliver it via Feishu message, and prepend to a Feishu doc (newest-first order).

---

## Configuration

Before first use, replace these placeholders in the steps below:

| Placeholder | What to fill in |
|---|---|
| `YOUR_FEISHU_USER_OPEN_ID` | Your Feishu open_id (starts with `ou_`) |
| `YOUR_DAILY_DOC_TOKEN` | Feishu doc token for your daily digest archive |
| `YOUR_BACKLOG_DOC_TOKEN` | Feishu doc token for your project backlog/TODO list (optional) |

---

## Step 1 — Fetch Content

Use `web_search` to find today's trending AI projects. Do **not** fetch github.com/trending directly (blocked).

Recommended searches:
- `"github trending AI agent LLM today"`
- `"github trending python AI machine learning today"`
- `"hacker news AI tools today"`

Filter criteria: AI Agent / LLM / automation tooling. Prioritize projects with clear practical value.

---

## Step 2 — Format the Report

For each selected project, include all four fields — no one-liners:

- **What it is**: One sentence on the problem it solves
- **Pain point**: What was the old approach, what does this improve
- **Value**: Concrete use case for you or your team
- **Follow-up**: Effort level (low/medium/high), worth tracking?

Report structure:

```
# YYYY-MM-DD GitHub AI Hot List

## 🔥 Top 3 Today
[project entries]

## 🤖 Most Relevant for AI Agents
[project entries]

## 📋 Recommended Quick Start
Pick 1 low-effort, high-value project. Explain why in 2–3 sentences.

---
```

---

## Step 3 — Send & Archive

### 3a — Send via Feishu

```
message tool:
  channel: feishu
  target: user:YOUR_FEISHU_USER_OPEN_ID
  message: <full report>
```

### 3b — Prepend to Feishu document (newest-first)

> ⚠️ Never use `feishu_doc append` — it adds to the bottom.

Steps:
1. `feishu_doc list_blocks` with `doc_token: YOUR_DAILY_DOC_TOKEN`
2. Find the Page block (`type=Page`), note its `block_id` as `PAGE_ID`
3. `feishu_doc insert` with:
   - `parent_block_id = PAGE_ID`
   - `index = 0`
   - Content: today's full report in Markdown
4. Title format: `# YYYY-MM-DD GitHub AI Hot List`
5. End with a `---` divider

### 3c — Log to backlog (optional)

If any project is worth tracking, append to your backlog doc:
- `doc_token: YOUR_BACKLOG_DOC_TOKEN`, section `📥 Backlog`
- Format: `- 🔲 **ProjectName** \`dimension\` \`priority\` \`source: GitHub YYYY-MM-DD\` — one-line value summary`

---

## Step 4 — Summary

After completing all steps, output:
- Number of projects covered
- Archive status (inserted at position #1 in doc)
- Recommended quick-start project
