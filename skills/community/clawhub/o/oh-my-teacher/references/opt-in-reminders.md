# Opt-In Reminders And Knowledge Digests

Use this file only when the user explicitly asks to enable, change, stop, or
generate reminders, daily digests, weekly digests, memory prompts, or knowledge
summary sheets.

## Non-Automatic Rule

This feature is opt-in only.

- Never enable proactive messages by default.
- Never infer permission from an agent name, past study activity, or available
  scheduler tool.
- Never send or schedule background messages unless the user has explicitly
  requested that reminder or digest.
- If the user asks for a one-time digest, generate only that digest; do not
  create a recurring reminder.
- If the user says "stop reminders", "暂停提醒", or "取消日/周频归纳", disable the
  reminder path and confirm the disabled scope.

## Capability Requirements

Use detected capability, not product identity:

- `proactive-message`: host can send a message without an immediate user prompt.
- `scheduler`: host can schedule delayed or recurring jobs.
- `memory`: host can persist reminder preferences across sessions.
- `file-write` or notes persistence: host can store digest artifacts.

If `proactive-message` or `scheduler` is missing, do not fake automation. Output
an inline digest and a copyable reminder configuration block instead.

OpenClaw and Hermes may be candidates only when the current runtime exposes
proactive-message or scheduler tools. If those tools are not visible, treat them
like any other prompt-agent and keep reminders on demand.

## Activation Triggers

Treat these as explicit opt-in examples:

- "开启每日复习提醒"
- "每天早上 8 点提醒我背 P0 内容"
- "每周日生成知识归纳卷"
- "OpenClaw/Hermes 能主动发消息的话，帮我安排周频复盘"
- "以后每天给我一份薄弱点记忆清单"

Before scheduling, confirm or infer these fields and label defaults:

| Field | Default if missing |
|---|---|
| Course | Current Course Snapshot active course |
| Frequency | daily for "每日/每天"; weekly for "每周/周频"; otherwise ask once |
| Time | 08:00 local time |
| Duration | until exam date if known; otherwise 7 days for daily or 4 weeks for weekly |
| Delivery channel | current agent channel |
| Digest scope | P0/P1 topics, due SRS, wrong notes, recent weak points |

If frequency is ambiguous and scheduling depends on it, ask one compact
question. For one-time generation, do not ask; generate the best digest from
available evidence.

## Reminder State

Persist preferences only when persistence exists and succeeds.

In file-capable agent shells, write or update `.oh-my-teacher/reminders.md` with:

```markdown
| Course | Frequency | Time | Scope | Enabled | Last Sent | Next Due |
|---|---|---|---|---|---|---|
| Course Name | daily | 08:00 | P0/P1 + weak points + SRS due | yes | - | 2026-06-13 |
```

In memory-capable hosts, store only stable reminder preferences: course,
frequency, time, duration, and enabled state. Do not store raw mistakes without
course context.

In prompt-only hosts, output this copyable block:

```markdown
Reminder Config
- Course:
- Frequency:
- Time:
- Scope:
- Enabled:
- Next due:
```

## Daily Knowledge Digest

Use this for daily reminders or when the user asks for "今日归纳", "今天提醒我记
什么", or "每日知识归纳卷".

```markdown
# 每日知识归纳卷

## 今日重点
| Priority | Chapter/topic | Why now | Action |
|---|---|---|---|
| P0/P1 | [topic] | [exam weight / past-paper frequency / teacher emphasis / weak-point evidence] | [memorize / derive / drill / explain] |

## 必背清单
- ★★★ [definition/formula/theorem/template]: [exact memory target]
- ★★ [supporting item]: [condition, boundary, or trap]

## 薄弱板块
| Weak block | Evidence | Repair action |
|---|---|---|
| [topic] | [wrong note / quiz score / mock loss / SRS lapse] | [one targeted drill or explanation] |

## 今日到期复习
| Topic | Due reason | Recall prompt |
|---|---|---|

## 3-5 个主动回忆题
1. [closed-book recall prompt]

## 下一步
[one concrete action: answer Q1, repair one weak point, or start a timed drill]

## 本轮闭环
- 重点: [P0/P1 topic or weak point]
- 反馈: [evidence used or missing]
- 下一轮: [repair, repeat, interleave, escalate, de-prioritize, or schedule]
```

## Weekly Knowledge Digest

Use this for weekly reminders or when the user asks for "周频归纳", "本周复盘",
"每周生成知识归纳卷", or "周计划提醒".

```markdown
# 每周知识归纳卷

## 本周进展
| Area | Evidence | Change |
|---|---|---|
| [chapter/topic] | [quiz/mock/SRS/wrong-note signal] | [improved / stuck / newly weak] |

## 反复薄弱板块
| Weak block | Pattern | Root cause | Next repair |
|---|---|---|---|

## 章节优先级更新
| Priority | Chapter/topic | Exam-scope weight | Past-paper frequency | Teacher emphasis | Weakness signal | Decision |
|---|---|---|---|---|---|---|
| P0/P1/P2 | [chapter] | [known/unknown] | [known/unknown] | [known/unknown] | [accuracy/SRS/wrong-note] | [keep / raise / lower] |

## 下周必背与必练
- ★★★ [must-memorize item]
- [practice target and question type]

## 下周训练安排
| Day/block | Focus | Feedback signal | Iteration |
|---|---|---|---|

## 本轮闭环
- 重点: [highest-yield next focus]
- 反馈: [what changed this week]
- 下一轮: [next repair or scheduled review]
```

## Digest Inputs

Use the strongest available evidence, in this order:

1. Current Course Snapshot: exam date, target, weak points, completed topics.
2. Stage 1 priorities from `references/staged-review-workflow.md`: P0/P1/P2 by
   exam-scope weight + past-paper frequency + teacher-emphasis strength.
3. SRS due items from `references/spaced-repetition.md`.
4. Wrong-note analytics from `references/wrong-note.md`.
5. Recent quiz/mock/oral/grade results.
6. User-provided teacher emphasis, past papers, and materials.

When evidence is missing, mark it as unknown and ask for the smallest useful
input after the digest, not before it.

## Delivery Protocol

When the host can proactively message and the user opted in:

1. Confirm the schedule in one short line.
2. Store reminder state if persistence exists.
3. Generate the first digest immediately unless the user asks to start later.
4. On each scheduled send, use the daily or weekly contract above.

When the host cannot proactively message:

1. Say that background delivery is not available in the current environment.
2. Generate the requested digest inline.
3. Provide a copyable Reminder Config block.
4. Suggest the next manual trigger phrase, such as "明天生成每日知识归纳卷".

Do not make reminders a substitute for feedback. Every digest must end with a
small active recall, repair, or scheduling action.
