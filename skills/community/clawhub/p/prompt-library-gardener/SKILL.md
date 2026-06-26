---
name: Prompt Library Gardener
description: Clean, tag, and index a user-provided prompt collection so the right prompt can be found, reused, and improved quickly.
version: 1.1.0
type: prompt-flow
license: MIT-0
language: en
tags: [prompt-engineering, prompt-library, knowledge-curation, ai-workflow]
---

# Prompt Library Gardener

## Overview

Use this skill when a user has many saved prompts but cannot quickly reuse the right one. The outcome is a cleaned prompt library with consistent names, practical tags, duplicate decisions, and short reuse notes.

This is a prompt-only organization workflow. Work only from prompt text and context the user provides in the conversation. Do not search local folders, files, note apps, browser history, cloud drives, email, or private workspaces for prompts. If the user wants those prompts included, ask them to paste, upload, or summarize the relevant prompt list.

## When to Use

Use this skill when the user says or implies:

- They have a folder, document, spreadsheet, chat log, or note full of prompts.
- They keep rewriting similar prompts from memory.
- They cannot remember which prompt worked best for a task.
- They want tags, categories, or a searchable index for prompts.
- They want to merge duplicates or clean up stale prompt variants.
- They want reusable notes explaining when to use each prompt.

Do not use this skill for prompt engineering from scratch unless the immediate goal is to organize a library. For single-prompt critique or rewriting, use a prompt improvement workflow instead.

## Boundaries

This skill will:

- Use only user-provided prompt lists and user-provided context.
- Preserve original prompt intent unless the user asks for rewrites.
- Mark uncertain classifications instead of guessing.
- Create human-readable tags and names, not a complex taxonomy for its own sake.
- Keep sensitive prompt content private within the current conversation.

This skill will not:

- Search local folders, files, note apps, browser history, drives, chats, or email.
- Call APIs, browse the web, execute code, or connect to prompt tools.
- Invent prompts that were not provided.
- Delete or discard prompt variants without showing the decision.
- Store user prompts externally.

## Required Inputs

Ask for these inputs if they are not already available:

1. The prompt list: exact prompt text, one prompt per item if possible.
2. Current storage format: notes, document, spreadsheet, prompt manager, or pasted text.
3. Main jobs: the recurring tasks the prompts support.
4. Preferred retrieval style: by job, by tool, by audience, by output format, or by project.
5. What counts as a duplicate: same wording, same purpose, or same output.
6. Any prompts that must not be edited.
7. Desired final format: table, markdown index, CSV-like list, or migration plan.

If the prompt list is large, ask the user to provide it in batches and label each batch. Keep a running index only from batches already provided.

## Workflow

### Step 1: Intake the Prompt Collection

Create a quick inventory before editing anything.

Inventory fields:

- Item number
- Current title, if any
- First-line summary
- Apparent job
- Intended output
- Tool or model mentioned
- Status: keep, merge candidate, unclear, stale, or needs user decision

Intake template:

| ID | Current title | One-line purpose | Output type | Initial status | Notes |
|---|---|---|---|---|---|
| P001 | [title] | [purpose] | [output] | [status] | [notes] |

If prompts arrive without titles, assign neutral temporary IDs first. Do not rename until grouping is complete.

### Step 2: Group by Job

Group prompts by the job they help the user complete, not by vague labels like "misc" or "AI". A job group should answer the question: "What is the user trying to get done?"

Useful group patterns:

- Research and synthesis
- Writing and editing
- Planning and prioritization
- Decision support
- Coding and debugging
- Customer or stakeholder communication
- Learning and explanation
- Creative ideation
- Data analysis and reporting
- Personal administration

For each group, produce:

- Group name
- Included prompt IDs
- Shared purpose
- Differences between prompts
- Recommended default prompt
- Gaps or missing variants

Group summary template:

```
GROUP: [Job group]
Purpose: [What this group helps with]
Prompts: [IDs]
Default pick: [ID and why]
Variants worth keeping: [IDs and when]
Merge candidates: [IDs]
Open questions: [Anything unclear]
```

### Step 3: Trim Duplicates and Variants

Classify overlap carefully. Similar prompts are not always duplicates.

Duplicate decision levels:

1. Exact duplicate: same wording or trivial formatting difference.
2. Near duplicate: same job and same output, minor wording changes.
3. Useful variant: same job but different audience, format, model, domain, or constraint.
4. Legacy version: older weaker version replaced by a stronger version.
5. Unsafe or unsuitable: asks for deception, bypassing safeguards, or harmful output.
6. Unclear: needs user decision.

Duplicate review template:

| Candidate IDs | Decision | Keep | Archive or merge | Reason |
|---|---|---|---|---|
| P003, P014 | Near duplicate | P014 | Merge P003 into notes | P014 has clearer output constraints |

When merging, keep the strongest phrasing and list useful details from the other version under reuse notes. Do not silently erase a distinctive constraint.

### Step 4: Tag Best Use

Use tags that help retrieval. Prefer 3 to 7 tags per prompt.

Recommended tag families:

- Job tag: research, writing, planning, code, learning, analysis, admin.
- Output tag: brief, table, checklist, email, report, outline, rubric, JSON, bullets.
- Audience tag: self, team, executive, customer, student, technical, nontechnical.
- Stage tag: brainstorm, draft, critique, revise, summarize, decide, finalize.
- Tool tag: general AI, ChatGPT, Claude, Gemini, local model, image model, coding agent.
- Constraint tag: concise, detailed, evidence-first, tone-sensitive, privacy-sensitive.

Tag quality rules:

- Use lowercase kebab-case unless the user prefers another convention.
- Avoid tags that apply to almost every prompt, such as "prompt" or "AI".
- Avoid one-off tags unless they will help retrieval later.
- Use "needs-test" for prompts the user has not validated.
- Use "gold-standard" only for prompts the user confirms are reliable.

### Step 5: Apply Naming Rules

A good prompt name should show the job, output, and distinguishing constraint.

Naming formula:

```
[Job] - [Output] - [Special use or audience]
```

Examples:

- Research - Evidence Brief - Source-Aware
- Writing - LinkedIn Draft - Founder Voice
- Decision - Tradeoff Matrix - Fast Compare
- Code - Bug Report Triage - Repro First
- Learning - Concept Explainer - Beginner Friendly

Naming rules:

- Keep names under 70 characters when practical.
- Start with the job category for sorting.
- Do not name prompts by model unless model-specific behavior matters.
- Avoid vague names like "Best prompt", "Useful", or "Prompt 12".
- Add a version only when multiple live variants must coexist.

### Step 6: Create Reuse Notes

Every kept prompt should include a short note that helps future selection.

Reuse note fields:

- Use when: the ideal situation.
- Do not use when: where it fails or is overkill.
- Inputs needed: what the user must provide before running it.
- Output expected: what the prompt usually produces.
- Known tweaks: quick changes for tone, length, audience, or format.
- Last tested: user-provided date or "not provided".

Reuse note template:

```
Use when: [scenario]
Do not use when: [scenario]
Inputs needed: [inputs]
Expected output: [format and quality]
Known tweaks: [short list]
Last tested: [date or not provided]
```

### Step 7: Build the Index

Create a clean index that the user can copy into their storage system.

Minimum index columns:

| Name | Job | Tags | Best use | Inputs needed | Status |
|---|---|---|---|---|---|
| [name] | [job] | [tags] | [best use] | [inputs] | [status] |

Optional index sections:

- Gold-standard prompts
- Needs testing
- Archive candidates
- Duplicate merge log
- Missing prompts to create later
- Naming and tagging rules

## Final Deliverable Format

Deliver the result in this order:

1. Library summary: count of prompts reviewed, groups created, duplicates found, and open questions.
2. Naming rules: the convention to use going forward.
3. Tag rules: approved tag families and examples.
4. Clean prompt index: one row per kept prompt.
5. Duplicate and archive log: what was merged, archived, or left undecided.
6. Reuse notes: short notes for each important prompt.
7. Next maintenance routine: a simple monthly or quarterly cleanup checklist.

## Monthly Maintenance Checklist

Use this quick routine to keep the library useful:

- Add new prompts with a temporary ID.
- Assign job, output, audience, and stage tags.
- Compare each new prompt against the current default in its group.
- Promote only one default per job group unless there is a clear variant.
- Mark untested prompts as needs-test.
- Archive prompts that have not been useful after two reviews.
- Update reuse notes when a prompt succeeds or fails.

## Edge Cases

### User provides only vague titles

Ask for the prompt text. If they cannot provide it, build a provisional catalog from titles only and mark every classification as provisional.

### User wants you to scan folders

Do not scan folders or local files. Say: "I can organize the prompts you provide here. Please paste or upload the prompt list you want included, and I will build the library from that."

### User has sensitive work prompts

Offer a minimal metadata pass where the user replaces sensitive details with placeholders. Do not ask for secrets, credentials, private customer data, or confidential internal material.

### User wants a very complex taxonomy

Recommend starting with simple job and output tags. Complex taxonomies often make retrieval slower. Add more dimensions only if the user can explain how they will search.

### Prompts vary by model

Keep model-specific variants only when behavior truly differs. Otherwise use one general prompt with a note like "Works best with models that follow structured instructions."

## Example Prompts

Copy and paste one of these into your AI assistant with your details filled in:

1. **Clean up a messy prompt folder:** "I have about 30 prompts in a notes file — some from ChatGPT, some from Claude, some I wrote myself. Many are duplicates with slight wording differences. I use them for content writing, code review, meeting summaries, and email drafting. Help me clean this up: tag each prompt by job, merge real duplicates, mark stale ones, and give me a searchable index."

2. **Tag and index for reuse:** "I keep rewriting the same kinds of prompts from memory. Here are 15 prompts I've saved for data analysis tasks. Some are for Excel formulas, some for SQL queries, some for chart design. Can you create clear names, practical tags, and a short reuse note for each so I can find the right one fast?"

3. **Organize by retrieval style:** "I have prompts scattered across three documents for different audiences — technical reports for my team, executive summaries for leadership, and training materials for new hires. Help me merge these into one library organized by output type, with tags that tell me which audience each prompt serves."


## Usage Scenarios

### Scenario 1

**User Input:** "Import my scattered prompts from Notes, Notion, and chat history. De-duplicate and tag them by use case."

**Expected Output:** Consolidated library. Prompts deduplicated by semantic similarity. Auto-tagged: "writing", "coding", "analysis", "brainstorming", etc. Conflict prompts flagged for manual review.

### Scenario 2

**User Input:** "It's been 6 months. Test my top 20 prompts against the current model and flag any that produce worse output than before."

**Expected Output:** Regression report. Each prompt tested, scored, and compared to its historical benchmark. 3 prompts flagged as degraded—suggests refined versions.

### Scenario 3

**User Input:** "Prune my library. Archive any prompt I haven't used in 90 days and that has a success rate below 70%."

**Expected Output:** Archive candidate list: 14 prompts matching criteria. User confirms; archived with metadata (last used, success rate, reason). Library shrinks from 200 → 186 active.


### Scenario 4: 每次用AI都要从头写prompt
**User input:** "我每天用ChatGPT/豆包/Kimi写周报、写文案、翻译，但每次都要从头写提示词。有没有办法让我保存和复用常用的prompt？"
**Expected output:** 个人AI提示词管理系统——工具选择：飞书文档/Notion/语雀（任选一个免费的）；组织方式：按场景分（写作类/编程类/翻译类/整理类/创意类），每个场景写一个或多个模板prompt；模板格式：角色设定→任务说明→输出格式→约束条件→示例→输入变量占位符（用[方括号]标出）；推荐用"AI Prompt管理"模板（在飞书模板库/Notion市场搜就有）；实战技巧：把最常用的5个（写周报、写英文邮件、翻译、代码审查、头脑风暴）设为手机快捷指令或输入法快捷短语。

## Quality Bar

A strong result makes the prompt library easier to use the same day. The user should know which prompt to pick, why it is named that way, what tags to search, and what to do with duplicates.
