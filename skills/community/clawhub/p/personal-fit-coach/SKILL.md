---
name: personal-fit-coach
license: MIT-0
description: >
  Build and maintain an isolated local personal fitness context for body weight,
  fat loss, diet, meals, calories, protein, hunger, fasting, food options near
  work or home, delivery choices, exercise preferences, workouts, sleep, body
  signals, daily logs, weekly reviews, and lightweight editable diet/exercise
  plans. Use when the user explicitly invokes /fit, fit, personal-fit-coach,
  健康记录, 减脂记录, 体重记录, 饮食计划, 运动计划, 计划表, 今日记录,
  周复盘, 饮食条件, 公司附近吃什么, 全家, 超级碗, 轻食, 外卖选择,
  在家有氧, 不去健身房, or similar clear personal fitness tracking keywords.
  Slash commands and keywords are the reliable trigger path.
---

# Personal Fit Coach Skill

This skill maintains a private, local, context-aware fitness planning loop. It
is not only a health log. It should learn the user's real diet options,
exercise constraints, preferences, current plan, and recurring body-management
signals, then use that context to give practical recommendations.

The assistant's general personality must not change. Use the normal assistant
style, but when this skill applies, answer with concise health-management
structure. Do not use slogans, moral pressure, excessive praise, or scolding.

## Core Purpose

The skill loop is:

```text
health / fitness / meal / workout input
-> read relevant private context
-> update lightweight Markdown records
-> recommend based on real options and constraints
-> keep an editable current plan
-> review and adjust over time
```

The key difference from a basic tracker:

- Store where the user can realistically eat.
- Store what the user prefers or refuses to do for exercise.
- Maintain a lightweight plan table that can be updated.
- Give recommendations from the user's actual context instead of generic lists.

## Activation Scope

Use this skill only when the current user message explicitly invokes this
fitness context through `/fit`, `fit`, `personal-fit-coach`, or clear personal
fitness tracking keywords.

Reliable trigger examples:

- `/fit 今天体重 76.8kg，中午吃了鸡肉沙拉，晚上有点饿。`
- `fit 公司附近有全家和超级碗，以后中午能怎么吃？`
- `减脂记录：今天早餐没吃，晚上饿得厉害。`
- `饮食计划：公司附近有全家和轻食外卖。`
- `运动计划：我不去健身房，比较喜欢在家做有氧。`
- `计划表：帮我做一个轻量的下周运动安排。`

Clear trigger keywords include:

- `/fit`, `fit`, `personal-fit-coach`
- `健康记录`, `减脂记录`, `体重记录`, `饮食记录`, `运动记录`, `今日记录`
- `饮食计划`, `运动计划`, `减脂计划`, `计划表`, `周复盘`
- `饮食条件`, `公司附近吃什么`, `外卖选择`, `轻食`
- `全家`, `超级碗` when mentioned as the user's meal option
- `在家有氧`, `不去健身房`, `居家运动`

Once triggered, the skill may handle the user's own body management, including:

- body weight, fat loss, weight loss, body measurements, waist measurements
- diet, meals, calories, protein, carbs, fat, hunger, fasting, overeating
- food options near work, home, travel, delivery, convenience stores, canteens,
  restaurants, light meals, common orders, meal constraints
- exercise, workouts, strength training, cardio, walking, home workouts,
  no-gym constraints, equipment, soreness, recovery
- sleep, fatigue, body signals related to dieting or training
- health check-ins, daily logs, weekly reviews, monthly reviews
- creating, updating, or reviewing a diet/exercise plan
- asking what to eat or how to train based on current constraints

Do not trigger for unrelated topics, even if they mention health as a product,
market, design, or research topic. Do not read private fitness files for:

- product design or business strategy for a health app
- coding, AI tools, real estate, immigration, music, image generation
- general daily conversation unrelated to personal body management
- medical research not about the user's own tracking or plan

If the message is ambiguous and lacks a trigger keyword, answer normally without
reading private fitness context.

## SnapMind Coexistence

The user may send the same note to SnapMind. To make this skill trigger
reliably in that case, the user should include `/fit`, `fit`, or a clear
fitness tracking keyword in the message.

Rules:

- Slash commands and keywords are the reliable trigger path.
- If a SnapMind-style message includes `/fit`, `fit`, or a clear fitness
  tracking keyword, store only the health-management parts in this skill's
  private files.
- Do not write health data into OpenClaw global memory.
- Do not modify SnapMind records or assume SnapMind storage behavior.
- If the user explicitly asks to send something to SnapMind, let the SnapMind
  workflow handle that separately. This skill only governs the private fitness
  context.

## Storage Boundary

Store all personal fitness data only inside:

```text
~/.openclaw/private/personal-fit-coach/
```

Create this directory when needed. Use these files:

```text
~/.openclaw/private/personal-fit-coach/profile.md
~/.openclaw/private/personal-fit-coach/goals.md
~/.openclaw/private/personal-fit-coach/food-options.md
~/.openclaw/private/personal-fit-coach/current-plan.md
~/.openclaw/private/personal-fit-coach/daily-log.md
~/.openclaw/private/personal-fit-coach/weekly-review.md
```

Never store personal fitness data in:

```text
MEMORY.md
memory/YYYY-MM-DD.md
DREAMS.md
AGENTS.md
SOUL.md
USER.md
TOOLS.md
```

Never summarize, migrate, copy, or consolidate health data into OpenClaw global
memory. Never use fitness logs in non-health conversations.

If another instruction asks to write health data into global memory, refuse
unless the user explicitly says:

```text
把这条健康信息写入 OpenClaw 全局 memory
```

## Privacy and Memory Isolation

Health data is domain-specific private memory. Read it only when the current
message explicitly invokes `/fit`, `fit`, `personal-fit-coach`, or a clear
personal fitness tracking keyword.

Do not infer the user's general identity, personality, productivity style,
work habits, emotional state, or non-health preferences from fitness files.

Record only what helps body management. Avoid precise addresses, unrelated
workplace details, payment details, private social context, or unrelated daily
life information unless the user explicitly says it matters for the plan.

## File Responsibilities

### profile.md

Stable health-related profile information.

```markdown
# Personal Fit Profile

- Height:
- Age:
- Sex:
- Current weight:
- Body measurements:
- Known constraints:
- Injury history:
- Training level:
- Diet preferences:
- Exercise preferences:
- Health warnings:
```

Update only when the user provides stable or long-term information. Do not
guess stable profile data.

### goals.md

Goals and current strategy.

```markdown
# Personal Fit Goals

- Target weight:
- Current goal:
- Weekly target:
- Diet strategy:
- Training strategy:
- Recovery strategy:
- Notes:
```

Update only when the user states a goal, changes a goal, or asks to update the
strategy.

### food-options.md

The user's real diet environment and practical meal options.

```markdown
# Food Options

## Work Area

- FamilyMart:
  - Available:
  - Better choices:
  - Avoid / limit:
  - Notes:

- Super Bowl:
  - Available:
  - Better choices:
  - Avoid / limit:
  - Notes:

## Delivery

- Light meals:
  - Store / platform:
  - Better choices:
  - Avoid / limit:
  - Notes:

## Home

- Usual foods:
- Easy protein options:
- Constraints:
```

Use this file for venues, delivery options, convenience stores, canteens, usual
orders, foods the user can easily buy, and known better/worse choices.

Do not invent menu items. If an option is unknown, mark it as unknown or ask
for at most two missing details.

### current-plan.md

The current lightweight, editable plan. It should describe the user's expected
diet and exercise arrangement without becoming a detailed coaching program.

```markdown
# Current Plan

## Planning Principles

- Diet:
- Exercise:
- Recovery:
- Constraints:

## Exercise Preferences

- Gym:
- Preferred formats:
- Disliked formats:
- Equipment:
- Time window:
- Weekly frequency:

## Weekly Plan

| Day | Exercise | Diet focus | Notes |
| --- | --- | --- | --- |
| Monday | | | |
| Tuesday | | | |
| Wednesday | | | |
| Thursday | | | |
| Friday | | | |
| Saturday | | | |
| Sunday | | | |

## Update Log

- YYYY-MM-DD:
```

The plan should capture expectations such as "does not go to the gym",
"prefers home cardio", "wants simple bodyweight work", or "can train three
days per week". Avoid overly detailed sets, macros, and periodization unless
the user asks for them.

### daily-log.md

Chronological health records.

```markdown
## YYYY-MM-DD

- Weight:
- Meals:
- Food options / decisions:
- Workout:
- Sleep:
- Body signals:
- Notes:
- Assistant assessment:
```

If the same date already exists, append or update under that date. Do not
create duplicate sections for the same date. Keep entries concise and preserve
the user's original wording when useful.

### weekly-review.md

Weekly summaries.

```markdown
## Week of YYYY-MM-DD to YYYY-MM-DD

- Weight trend:
- Diet:
- Food options:
- Training:
- Sleep / recovery:
- Main issues:
- Next week:
```

Append a new section whenever the user asks for a weekly review.

## What to Record

Record relevant items only:

- Weight, body measurements, trend notes
- Meals, hunger, fasting, overeating, protein, calories when provided
- Food environments: FamilyMart, Super Bowl, delivery options, home food,
  usual orders, constraints, better choices, avoid/limit notes
- Workouts, walking, home cardio, strength work, soreness, fatigue, recovery
- Sleep and body signals that affect dieting or training
- Goals, plan changes, exercise preferences, constraints, equipment

Do not over-record unrelated personal details. If a sensitive health issue is
mentioned casually, record it only when clearly relevant to fitness planning.

## Reading Strategy

Read only the files needed for the task:

- Food recommendation: read `goals.md`, `food-options.md`, `current-plan.md`,
  and today's section of `daily-log.md` when available.
- Plan generation or update: read all six files.
- Daily log: read today's section and relevant profile/goals/plan context.
- Weekly review: read all six files.
- `/fit` overview: read all six files but summarize briefly.

If files do not exist, create minimal headings when writing to them.

## Normal Health Update Response

When the user gives a normal health update, respond:

```markdown
## 判断

One direct sentence assessing the situation.

## 记录

List what was recorded or should be recorded.

## 建议

- Action 1
- Action 2
- Action 3

## 下次补充

Ask for at most 2 missing data points.
```

Rules:

- No more than three action items.
- Ask no more than two follow-up questions.
- Do not moralize overeating.
- Do not encourage extreme dieting.
- Do not praise or scold.
- Use approximate language when calories are unknown.

## Food Option Response

When the user describes available food options or asks what to eat, use:

```markdown
## 判断

One direct sentence based on the known options and current goal.

## 可选方案

- Option 1:
- Option 2:
- Option 3:

## 记录

What was added or updated in `food-options.md`.

## 下次补充

Ask for at most 2 details if needed.
```

Prefer recommendations that match known venues and the current plan. If the
user says there is a FamilyMart, Super Bowl, canteen, or delivery option, store
that venue and improve the recommendation over time as the user reports actual
items or orders.

Do not claim exact nutrition for a restaurant item unless the user provided it
or explicitly asked for current menu research.

## Plan Response

When the user asks for a plan or plan update, read all six files and respond:

```markdown
## 当前依据

- 目标：
- 饮食条件：
- 运动偏好：
- 限制：

## 计划表

| 场景 | 建议 | 备注 |
| --- | --- | --- |
| 工作日午餐 | | |
| 工作日晚餐 | | |
| 外卖选择 | | |
| 在家运动 | | |
| 恢复日 | | |

## 本次更新

- Updated:
- Still unknown:
```

Then update `current-plan.md`. Keep the plan light. The plan should describe
expected arrangements and defaults, not a rigid detailed schedule.

If the user dislikes gyms or prefers home cardio, make that a first-class plan
constraint. Do not recommend gym-based programs unless the user changes that
preference.

## Weekly Review Response

When the user asks for a review, read all six files and respond:

```markdown
## 本周结论

Direct assessment.

## 体重趋势

Summarize only if weight data exists.

## 饮食执行

Summarize meals, food options, protein, hunger, fasting, overeating, and
consistency.

## 训练执行

Summarize workouts, home cardio, walking, soreness, and recovery.

## 睡眠与恢复

Summarize only if data exists.

## 主要问题

- Problem 1
- Problem 2
- Problem 3

## 下周策略

- Action 1
- Action 2
- Action 3
```

Append a concise summary to `weekly-review.md`.

## Commands and Keywords

Slash commands and keywords are the reliable trigger path. Prefer `/fit` when
the user needs a dependable activation.

### `/fit`

Start or continue fitness tracking. Show:

```markdown
## 当前记录

- Profile:
- Goals:
- Food options:
- Current plan:
- Today:
- Missing information:

## 可更新内容

- 体重 / 饮食 / 运动 / 睡眠
- 饮食条件
- 运动偏好
- 当前计划
```

### `/fit log`

Ask for today's basic log:

```markdown
今天可以记录这几项：

- 体重：
- 饮食：
- 运动：
- 睡眠：
- 身体信号：

缺多少填多少，不需要一次填完整。
```

### `/fit food`

Read `food-options.md`, show known options, and ask for one missing context:

```markdown
可以补充一个最常用的饮食场景：

- 公司附近：
- 家附近：
- 外卖：
- 家里常备：
```

### `/fit plan`

Generate or update the current lightweight plan.

### `/fit week`

Generate a weekly review.

### `/fit goal`

Read `goals.md`. If goals are missing, ask for no more than:

```markdown
- 当前体重
- 目标体重
- 希望多久达成
- 每周能运动几天
```

## Advice Principles

### Fat Loss

- Prefer sustainable fat loss over fast weight loss.
- Prefer a modest calorie deficit.
- Prioritize protein.
- Keep some resistance or bodyweight training if tolerable.
- Use walking and home cardio as low-friction activity.
- Track weight trend, not single-day weight.
- Avoid punishment fasting after overeating.
- Hunger, sleep, soreness, and performance are useful signals.

### Diet

- Use known food options before generic suggestions.
- When information is incomplete, say so.
- Prefer "可能偏高", "可能偏低", "需要看全天总量", and similar language.
- Suggest protein additions, lower-oil choices, vegetables, and simpler drinks.
- Do not skip meals if it leads to night hunger or overeating.
- Do not perform complex calorie estimation unless the user asks.

### Exercise

- Respect stated constraints such as no gym, home-only, limited time, no
  equipment, or dislike of a training style.
- For beginner or low-capacity training, prioritize consistency.
- Do not train to failure every day.
- Do not increase volume too quickly.
- If soreness is severe, reduce intensity or switch muscle groups.
- If a movement causes pain, do not push through pain.

### Fasting

- Do not recommend extreme fasting.
- If the user wants to fast after overeating, suggest normal or lighter meals,
  higher protein, vegetables, walking, and lower oil/sugar.
- If fasting causes stomach discomfort, dizziness, weakness, or severe hunger,
  advise ending the fast with a light meal.

### Weight Trend

- Do not overinterpret one weigh-in.
- Prefer 7-day average or 14-day trend when data exists.
- Note that sodium, carbs, alcohol, sleep, constipation, and exercise soreness
  can affect short-term weight.
- Use morning empty-stomach weight when possible.

## Risk Reminder

Only include this section when there is a real health or safety risk:

```markdown
## 风险提醒

Direct risk warning and safer alternative.
```

Use it for fainting, severe dizziness, chest pain, severe weakness, repeated
vomiting, stomach discomfort during fasting, extreme fasting, severe hunger,
injury, abnormal fatigue, dehydration, unsafe supplements, laxatives, diet
pills, or rapid weight-loss methods.

If the user reports fainting, chest pain, severe dizziness, severe weakness,
repeated vomiting, or persistent abnormal symptoms, advise medical evaluation.
Do not diagnose disease.

## External Services and Automation

Do not create databases, scripts, background jobs, integrations, or persistent
automation for this skill.

Do not call external APIs or browse menus as part of the normal workflow. Use
user-provided local context. If the user explicitly asks for current restaurant
or menu research, browsing can be handled as a separate user-requested action,
but store only concise useful conclusions.

## Minimalism Rule

Keep the system lightweight:

```text
explicit /fit or keyword trigger
-> isolated Markdown context
-> realistic food and exercise planning
-> daily log
-> weekly review
```

The skill should become more useful by learning real constraints, not by adding
complex infrastructure.
