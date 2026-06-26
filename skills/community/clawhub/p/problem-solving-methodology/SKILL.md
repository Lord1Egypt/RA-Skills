---
name: problem-solving
version: 1.0.0
description: >
  结构化问题诊断与解决方法论。
  Use when: (1) 问题原因不明需要调查/"分析一下这个问题"/"排查一下",
  (2) 之前的修复尝试失败了,
  (3) 问题涉及多个组件交互/"为什么会这样"/"调查一下原因",
  (4) 修改有风险或副作用/"诊断一下",
  (5) 用户明确要求先分析再修复。
  NOT for: 明显的一行修复、错误信息清晰且有已知方案的问题、
  用户说"直接修"的简单问题。
---

# Structured Problem Solving

## When to Use This vs. Direct Fix

**Direct fix (skip this skill)**:
- Error message points to exact cause
- One-line config/code fix
- You've seen this exact problem before

**Use this skill**:
- You'd need to say "可能是..." to explain the cause
- 2+ components involved
- You already tried a fix that didn't work
- Wrong fix could cause data loss, privacy leak, or downtime

## The Process

### Step 0: Question Dissolution (消解层)

Before solving, check if the problem itself is valid. Many problems dissolve when examined properly.

**Run these 3 checks sequentially. If any check dissolves the problem, stop and tell the user — a dissolved problem is more valuable than a solved one.**

#### 0.1 Language Trap Detection (语言陷阱)

Does the problem statement contain vague, undefined key terms?

Common trap words: "优化" "合适" "更好" "正常" "应该" "稳定"

**Test**: Can you give a measurable or actionable definition for every key term? If not, the problem can't be solved because it hasn't been stated.

→ If trapped: Ask the user to define the vague term. "你说的'优化'具体指什么？响应时间从 X 降到 Y？还是内存占用？还是用户体验？"

#### 0.2 Hidden Assumption Check (假设检验)

Rewrite the problem as: "This problem assumes X. Is X true?"

Common false assumptions:
- "系统变慢了" → assumes it was faster before (was it? measured when?)
- "用户不喜欢这个功能" → assumes users have tried it (have they? data?)
- "我们需要加这个功能" → assumes the current system can't do it (can it?)

→ If assumption is false: Tell the user. "你的问题假设了「X」，但这个前提可能不成立。如果 X 不成立，问题就消失了。"

#### 0.3 Question vs. Problem Classification

- **Question**: Has a standard answer, can be resolved by looking it up or reading docs
  - → Answer directly, don't enter the full diagnostic process
- **Problem**: No standard answer, requires investigation + experimentation
  - → Continue to Step 1

If the problem survives all 3 checks, proceed to full diagnosis.

---

### Step 1: Define the Problem

Turn vague "something's wrong" into a precise statement.

```
问题：[一句话]
现象：[具体发生了什么]
预期：[应该是什么样]
影响：[谁受影响，严重程度]
可复现：[是/否，触发条件]
```

**Rules**:
- Describe what you observe, not what you think caused it
- "webchat replies appear in DingTalk group" = problem ✅
- "origin got polluted" = hypothesis, not problem ❌

### Step 2: Diagnose

**Do not skip to fixing.** Trace the data flow end-to-end first.

#### 2.1 Map the call chain
```
Input → Step A → Step B → Step C → Output
          ↓          ↓          ↓
        Check      Check      Check
```

#### 2.2 Verify each step
Read actual values (logs, state files, source code). Do not guess.

#### 2.3 Narrow down
Find the first step where output diverges from expected. That's where the bug is.

#### 2.4 Confirm root cause

Three questions before you declare root cause:
1. **Why?** — Explain the mechanism, not just the symptom
2. **Sufficient?** — If I fix this, will the problem definitely disappear?
3. **Unique?** — Is there another cause that could produce the same symptom?

All three must be answered. If not → keep diagnosing.

**Diagnostic tools (prefer in order)**:
1. Error messages / logs (fastest)
2. State inspection (config files, DB, session store)
3. Source code tracing (most reliable)
4. Minimal reproduction experiment

### Step 3: Design Solutions

Generate **at least 2** candidate solutions. Compare on:

| Dimension | Question |
|-----------|----------|
| Effectiveness | Fixes root cause or just symptom? |
| Risk | Could it break something else? |
| Complexity | How many components touched? |
| Reversibility | Can we roll back if wrong? |
| Durability | Survives restarts / updates? |
| Side effects | Impact on other features? |

Present as:
```
方案 A：[one line]
  ✅ [pros]  ⚠️ [risks]

方案 B：[one line]
  ✅ [pros]  ⚠️ [risks]

→ 推荐 A，因为 [reason]
```

Always include the "do nothing / workaround" option if viable.

### Step 4: Execute

Pre-flight checklist:
- [ ] Root cause confirmed (not guessed)
- [ ] Solution evaluated (not first idea)
- [ ] User confirmed (for risky changes)
- [ ] Rollback plan ready

**Rules**:
- Change one variable at a time
- Record what was changed and what it was before
- Minimize scope — don't "fix other things while you're at it"

### Step 5: Verify

Three levels of verification:

1. **Direct**: Reproduce original trigger → problem gone?
2. **Regression**: Related features still work?
3. **Durability**: Survives restart / next trigger?

Show evidence, don't say "应该好了".

### Step 6: Review

```
## 复盘：[问题名]
耗时：X 分钟（有效 Y / 弯路 Z）
根因：[一句话]
修复：[一句话]
弯路：[走了什么弯路]
教训：[提炼的规则]
```

Write lessons to `.learnings/` if reusable.

## 诊断超时与死胡同处理

| 信号 | 动作 |
|------|------|
| 同一假设连续 3 次验证无结论 | 停止，换假设或换诊断维度 |
| 累计诊断 >15 分钟无进展 | 暂停，向用户汇报已排除项 + 当前卡点，询问是否有额外线索 |
| 累计尝试 >5 个假设均被否定 | 考虑问题是否需要消解（回 Step 0）或需要更多上下文 |
| 修复后问题复现 | 不叠加补丁，回退到修复前状态，重新走 Step 1 |

## Anti-patterns

| Pattern | What it looks like | Fix |
|---------|-------------------|-----|
| Guess-and-fix | See symptom → hypothesize → change immediately | Map call chain first |
| One-end-only | Check only input or output | Trace full data flow |
| Surface fix | Change the bad value without asking why it's bad | Ask "why did it become this value?" |
| Multi-change | Change 3 things at once | One variable at a time |
| Premature victory | "Should be fixed now" without checking | Show evidence |
| No rollback | Forget to record original values | Backup before modify |

## Communication During Problem-Solving

- **Define**: Confirm understanding ("你说的问题是 X 对吗？")
- **Diagnose**: Share progress, don't go silent ("在查 Y 环节，发现了 Z")
- **Design**: Give choices, not just one option
- **Execute**: Confirm before risky operations
- **Verify**: Ask user to check on their end
- **Throughout**: Say "I'm not sure yet" over false confidence

---

## 下一步建议（条件触发）

问题解决后，根据结果判断是否推荐下一步。

| 触发条件 | 推荐 |
|---------|------|
| 根因是代码 bug，修复需要多文件改动 | 「根因清楚了，修复交给 coding-agent spawn Claude Code 来做。」 |
| 问题根因值得记录（同类问题可能再犯） | 「这个教训值得记下来，写到 .learnings/ 防止再犯。」 |
| 问题在消解层被消解（问题本身不成立） | 「问题已经消解了。如果背后有更大的决策要做，可以拉出来单独讨论。」 |
| 诊断过程发现系统架构层面的隐患 | 「这次修好了，但架构上还有隐患。要不要排个时间做一次 healthcheck？」 |
