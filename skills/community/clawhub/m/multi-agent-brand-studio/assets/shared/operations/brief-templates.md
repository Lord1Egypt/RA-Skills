# Brief Templates

_Standard templates for dispatching tasks to agents. Leader reads this before composing briefs._

---

## Universal Structure (All Agents)

### Required Fields (every brief must have)

```markdown
**Task ID:** T-{YYYYMMDD}-{HHMM}
**Callback to:** {Leader's current session key — agent MUST callback to this session when done}

**Task:** [one-line description]

**Acceptance Criteria:**
- [ ] [verifiable condition 1]
- [ ] [verifiable condition 2]
- [ ] ...

**Execution Boundary:**
- Deliver: [what to report back]
- DO NOT: [specific actions that require Leader confirmation]
```

### Optional Fields (include when relevant)

```markdown
**Context:**
- Spec: [file path or link]
- Prior output: [file path from previous agent]
- Related files: [shared/ paths, brand profile, etc.]

**Brand Scope:** {brand_id} — read `shared/brands/{brand_id}/profile.md`

**Dependencies:**
- Requires output from: [agent name] — [what output]
- Input files: [paths]

**Priority:** normal | urgent | low
- urgent: owner is actively waiting, prioritize speed
- normal: standard turnaround
- low: no rush, quality over speed

**Deadline:** [expected completion time or "no deadline"]

**Reference:**
- Spec doc: [path]
- Reference images: [paths]
- Prior conversation context: [summary]
```

---

## Owner-Facing Templates (Leader → Owner)

_These are owner-visible workflow messages. They are not agent briefs._

### Kickoff / Status Message Template

_This is the status message sent to Telegram and edited in-place on every callback._

```markdown
📋 {task name}
ID: T-{id}

1. ⏳ {Agent} → {step description}
2. — {Agent} → {step description} (after: 1)
3. — Leader → {step description} (after: 2)

⏳ 進行中：Step 1
```

**Icons:** ⏳ = 進行中 · ✅ = 完成 · — = 等待 · ❌ = 失敗 · 🔍 = 審查中

**Rules:**
1. Send immediately after dispatch → record returned messageId as `telegram_status_msg` in task file.
2. On every callback → edit this message (update icon + bottom status line).
3. On completion → send a separate Result Delivery message (see below).

### Progress Template

```markdown
進度更新：{task summary}

- 已完成：{completed step/result}
- 目前在做：{active step}
- 依賴狀態：{dependency status if relevant}
- 等待中：{agent/blocker/decision if any}
- 下一次回報：{next expected update}
```

### Result Delivery Template

```markdown
✅ 任務完成

Task ID: {id}
結果摘要：
- {what was done}
- {key output / file / commit / path}
- {important status: pending approval / local only / not pushed / not deployed / etc.}

我的判斷：
{quality / recommendation / caveat}

你現在要決定的是：
{approval / revision / next step}
```

**Task-type hints** (include when relevant, don't force):
- Code/config/git: commit hash, modified files, push status
- Content/media: deliverable file paths, approval status
- Research: headline conclusion, report path

### Blocked / Needs-Info Template

```markdown
這單目前卡在：{reason}

我需要你補：
1. {item}
2. {item}

拿到後我就直接接著做，不重開流程。
```

---

## Agent-Specific Templates

## Callback Payload Contract (All Agents)

Callbacks sent via `sessions_send` must include:

- `task_id` (canonical: `[TASK_CALLBACK:T-{id}]`)
- `agent`
- `signal`
- `output`
- `files` (optional)

If a callback is malformed (missing required fields), Leader should request a resend.

### Engineer

```markdown
**Task:** [description]

**Context:**
- Spec: [path]
- Existing code: [paths]
- Dependencies/framework: [e.g., Node.js, Python, Vue]

**Requirements:**
1. [specific requirement]
2. [specific requirement]

**Acceptance Criteria:**
- [ ] [functional criterion]
- [ ] [performance criterion if applicable]
- [ ] [error handling: what happens when X fails]

**Testing:**
- [ ] [test case 1]
- [ ] [edge case: empty input, malformed data, etc.]
- [ ] [integration: works with existing system]

**Output:**
- Code location: [directory path]
- README with setup/run instructions
- List of modified/created files in report

**Execution Boundary:**
- Deliver: code + test results + file list
- DO NOT: push to git, deploy, install global packages, modify files outside specified directory
- Wait for Leader review before any external action
```

### Researcher

```markdown
**Task:** [research question]

**Scope:**
- Depth: overview | standard | deep-dive
- Timeframe: [e.g., last 6 months, current state]
- Geography: [e.g., Thailand market, global]
- Sources: [academic / industry / social / all]

**Context:**
- Brand: {brand_id} (if brand-related)
- Shared knowledge: [relevant shared/ paths]
- Prior research: [paths to previous findings]

**Acceptance Criteria:**
- [ ] Answers the core research question
- [ ] Sources cited
- [ ] Actionable insights highlighted
- [ ] [specific data points needed]

**Output Format:**
- Markdown report with structured sections
- Key findings summary at top
- Source citations throughout

**Execution Boundary:**
- Deliver: research report
- Use [KB_PROPOSE] for any domain knowledge worth persisting
```

### Creator

```markdown
**Task:** [description]

**Brand Scope:** {brand_id} — read profile.md + content-guidelines.md

**Content Spec:**
- Platform: [Facebook / Instagram / TikTok / blog]
- Format: [post / caption / article / ad copy]
- Language: [from brand profile]
- Length: [word/character limit or range]
- Variants: [A/B versions needed?]

**Visual Spec:**
- Dimensions: [WxH px]
- Style: [photo-realistic / flat / lifestyle]
- Reference images: [local paths — must be downloaded first]
- Product focus: [specific product or general brand]

**Context:**
- Research input: [path to researcher output, if available]
- Product/topic focus: [specific product or theme]
- Campaign context: [if part of larger campaign]

**Acceptance Criteria:**
- [ ] Copy matches brand voice and tone
- [ ] Correct language and platform conventions
- [ ] Visual matches brand identity
- [ ] Copy and visual are coherent together
- [ ] [specific requirement]

**Output:**
- Copy text + image file paths as one package
- Hashtag recommendations if applicable

**Execution Boundary:**
- Deliver: copy + image files + file paths
- DO NOT: publish to any platform
- If image generation fails, report [BLOCKED] with explanation
```

### Worker

```markdown
**Task:** [description]

**Context:**
- Files to modify: [paths]
- Reference: [spec, config, or instruction]

**Acceptance Criteria:**
- [ ] [specific verifiable outcome]
- [ ] [file state after completion]

**Output:**
- Report: what was changed/created
- File paths of modified/created files

**Execution Boundary:**
- Deliver: results + file paths
- DO NOT: push to git, deploy, restart services — unless explicitly instructed
- DO NOT: expand scope beyond what's listed
```

### Reviewer (on-demand, spawned)

```markdown
**Review Task:** [what to review]

**Deliverable:**
- [Path to content/code being reviewed]
- [Original brief — attached or path]

**Review Standards:**
- Brand alignment (read `shared/brands/{brand_id}/profile.md`)
- Brief compliance — does output meet acceptance criteria?
- [Technical correctness / audience fit / factual accuracy — as applicable]

**Prior Context:**
- Revision round: [1st / 2nd / rework after feedback]
- Previous feedback: [summary if applicable]

**Output:**
- [APPROVE] or [REVISE]
- Specific, actionable feedback (shorter than the deliverable)
- Max 2 review rounds
```

---

## Rework Brief (Revision Request)

_Use this template when sending rework/revision requests to agents after quality review._

```markdown
**Task ID:** T-{YYYYMMDD}-{HHMM}
**Callback to:** {Leader's current session key}
**Round:** {1/2 or 2/2}

**[REVISION REQUEST]**

**What was delivered:** {one-line summary of agent's output}

**Issues found:**
1. {specific issue with concrete example}
2. {specific issue with concrete example}

**Expected fix:**
- [ ] {verifiable correction 1}
- [ ] {verifiable correction 2}

**Context:** {any additional info agent needs — original brief reference, updated requirements, reviewer feedback if Path B}
```

---

## Execution Boundary — Common Examples

| Agent | Common boundaries |
|-------|------------------|
| Worker | No git push, no deploy, no service restart, no scope expansion |
| Researcher | Report only, use [KB_PROPOSE] for knowledge updates |
| Creator | Draft delivery only, no publishing, report [BLOCKED] if image gen fails |
| Engineer | No git push, no deploy, no global installs, no changes outside scope |
| Reviewer | Read-only, no modifications |

These are defaults. Each brief may override based on task context (e.g., owner pre-approved a push → brief can say "push allowed after tests pass").

---

_Version: 3.0 | Updated: 2026-03-08 — Status message template, removed status_mode_
