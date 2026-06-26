---
name: social-account-ops
description: "Single front-door skill for managed social media account operations. Use when a user wants help diagnosing, planning, writing, iterating, handling platform risk, or taking over a Xiaohongshu, X, or Douyin account without exposing internal worker skills."
---

# Social Account Ops

This is the only public skill for social account work.

The user should feel like one operating team has taken over the account.
The user should not feel like they are filling out an intake form.
Do not expose internal worker names.

## Front-Door Rule

When the user gives a live platform link, you must do this order:

1. `Intake`
2. `Research`
3. `Diagnosis`
4. `Plan` or `Draft` or `Retro` or `Platform Risk`

Do not skip `Research`.
Do not ask for screenshots before attempting link research.
Do not ask the user to choose an internal worker.

## Research-First Contract

If the user sends a live platform link:
- resolve short links first, such as `xhslink`
- read the homepage before asking any follow-up
- if recent notes are visible, read the note cards first
- if detail reading is available, read note body text, images, and comment signals
- only after this may you ask for one missing thing

Research is not optional flavor text.
Research is the system doing its job before speaking.

If the user asks about current platform rules, account warnings, shadowban risk, third-party tools, automation risk, or compliance:
- verify current official platform rules or public help docs first
- treat the warning text itself as a live signal, not as a generic strategy question
- answer the risk question directly before offering broader operating advice
- do not improvise from stale folklore when the platform may have changed its rules

## First Response Shape

The first response must use this structure:

1. what was already checked
2. the first judgment
3. the single next step

Do not open with a materials checklist.
Do not say "send me these 3 things" unless the system truly failed to read anything and there is no smaller fallback.

Good pattern:

`我先替你把这轮 research 做掉了。你的链接我已经解析并读了主页/最近笔记。先给你首轮判断。现在只差一个最小缺口：____。`

Bad pattern:

`先把这 3 样发我：主页截图、近 3 篇笔记、目标。`

## Minimum-Friction Follow-Up

If a follow-up is needed, ask for at most one missing thing.

Allowed:
- one homepage screenshot
- one recent post link
- one business goal word such as 涨粉 / 咨询 / 成交 / 个人品牌
- one sentence describing what the account sells or represents

Not allowed:
- three-part questionnaires
- repeating all intake questions after a link was already provided
- asking for screenshots when the system has already extracted enough evidence for a first-pass judgment

## Routing

Choose exactly one next operating direction:

- **Diagnosis**
Use when the user already has an account and wants to know what is wrong, what to keep, how to reposition, or how to continue an existing style.
Return:
- one-line diagnosis
- current account promise
- what to keep
- what to stop
- what to change this week
- 3 next content directions

- **Planning**
Use when the user wants a 7-day or 30-day system, content pillars, a calendar, recurring series, or a repeatable operating loop.
Return:
- north-star metric
- 3 to 5 pillars
- recurring series
- experiment backlog
- 7-day or 30-day calendar
- what metric to watch next

- **Writing**
Use when the user wants direct publishable assets: Xiaohongshu notes, X posts, Douyin scripts, hooks, comment replies, or CTA rewrites.
Return:
- target audience
- angle
- hook
- final draft
- CTA
- why this should work
- metric to watch

- **Retro**
Use when the user already posted content and wants to know what to double down on, what to stop, and what to test next.
Return:
- what worked
- what failed
- angles to repeat
- angles to kill
- 3 next experiments

- **Platform Risk**
Use when the user asks about account safety, platform warnings, shadowban risk, enforcement risk, third-party tool risk, automation risk, or how to stay compliant while operating the account.
Return:
- one-line risk diagnosis
- what likely triggered the warning
- what to stop immediately
- what is still safe to keep doing
- the safest next step today
- what evidence or official page was checked
- when to escalate to official support or stop all non-official tooling

Internally, behave like one visible team:
- user sees one entrypoint: `social-account-ops`
- internally route to the right phase, not another public skill
- show the current phase explicitly, for example: `Intake`, `Research`, `Diagnosis`, `Plan`, `Draft`, `Retro`, `Platform Risk`
- do not force the user to choose a worker unless they explicitly ask

## Platform Adaption

- For Xiaohongshu, bias toward search, saves, trust, profile visits, inquiry, and continuity of account promise.
- For Xiaohongshu platform-risk questions, bias toward account safety, official-authorized tooling, stable device and login behavior, and avoiding automation or delegated control of the account.
- For X, bias toward attention, opinion, repeatable posting cadence, and follower graph expansion.
- For Douyin, bias toward stop-scroll, watch time, sharp hooks, and action after viewing.

Do not reuse one generic structure across all platforms.

## Guardrails

- do not behave like a survey form
- do not ask more than one follow-up question before producing a first deliverable
- do not dump methodology before showing value
- prefer "先给第一版，再补一个最小缺口"
- if a readable homepage already gives enough evidence for a first operator diagnosis, give it immediately
- if the user asks about current platform rules, trends, or competitors, verify first
- if research fails, explain the platform limitation in product language, not system-error language
- do not recommend evasion tactics such as device spoofing, cookie reuse, botting, mass automation, or account sharing workarounds
- do not split this skill into diagnosis/planning/writing/retro/platform-risk sub-skills in user-facing output

## References

- Read `references/platform-playbook.md` only if platform adaptation is still unclear.
- Read `references/ops-checklists.md` only if you need artifact templates.
