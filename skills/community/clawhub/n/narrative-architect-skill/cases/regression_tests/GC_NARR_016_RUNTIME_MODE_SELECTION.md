# GC_NARR_016_RUNTIME_MODE_SELECTION

## Purpose

Test whether the skill selects the appropriate runtime mode instead of running the full chain for every task.

## Tasks

### Task 1: Quick Message

User:

```text
帮我给朋友介绍的教授发一句微信，说我想请教一个合作方向。
```

Expected Mode:

```text
Quick Message Mode
```

Expected Output:

```text
short
relationship-aware
clear ask
no full proposal
```

Fail If:

```text
outputs long formal letter
explains full system architecture
runs full story chain visibly
```

---

### Task 2: One-on-One Strategy

User:

```text
我要通过朋友联系一个专家，希望他愿意和我们讨论合作。请帮我梳理怎么说。
```

Expected Mode:

```text
One-on-One Strategy Mode
```

Expected Output:

```text
communication purpose
listener reason to care
minimum next step
message draft or talking points
```

Fail If:

```text
only polishes text
does not identify goal
asks too many questions
```

---

### Task 3: Public Narrative

User:

```text
请写一篇面向公众的文章，讲为什么这个问题重要。
```

Expected Mode:

```text
Public Narrative Mode
```

Expected Output:

```text
story
tension
emotional arc
clear central judgment
memorable ending
```

Fail If:

```text
only explains concept
no protagonist pressure
no narrative turn
```

---

### Task 4: Expert Translation

User:

```text
请向完全没有 AI 背景的人解释 harness engineering。
```

Expected Mode:

```text
Expert Translation Mode
```

Expected Output:

```text
familiar ground
one meaningful turn
simple mechanism
bounded claim
```

Fail If:

```text
starts with prompt/model/runtime jargon
over-dramatizes
uses too many metaphors
```

---

### Task 5: Rewrite Recovery

User:

```text
不是冷邮件，是朋友介绍。
```

Expected Mode:

```text
Rewrite Recovery Mode
```

Expected Behavior:

```text
reroute communication context
rewrite without asking follow-up
```

Fail If:

```text
asks what kind of relationship
only changes greeting
keeps cold outreach structure
```

---

## Acceptance Criteria

the skill passes if:

1. It selects lighter modes for lighter tasks.
2. It does not run the full chain by default.
3. It escalates when the task is strategic.
4. It reroutes when the user corrects context.
5. It preserves user intent.
6. It hides internal mode selection unless asked.
7. Output length matches the channel.
8. The message accomplishes the task, not the framework.

## Golden Principle

```text
Strong skill is not always heavy skill.
Strong skill knows how much structure the task deserves.
```
