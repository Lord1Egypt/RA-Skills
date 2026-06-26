---
name: is-bullshit
description: Detect if AI responses contain hallucinations by analyzing tool usage and response quality. Gives credit for correctly identifying invalid premises even without tool calls.
---

# is-bullshit - Hallucination Detector

**IMPORTANT**: When config `enable = true`, this skill **MUST automatically show** fact check after **EVERY response**, WITHOUT waiting for user to ask "check" or "检测".

When `enable = false`, this skill triggers when user explicitly asks:
- **Chinese**: 检测、检测一下、核实、是真的吗、是不是胡说
- **English**:
  - "is that true" / "is this true"
  - "are you serious" / "you serious"
  - "is that bullshit" / "is this nonsense"
  - "verify" / "check" / "fact check"
  - "are you sure" / "are you certain"
  - "that's not right" / "that's wrong"

## Purpose

Detect whether the AI's response is trustworthy by checking:
1. **Tool usage** - Did the AI call tools to verify facts?
2. **Response quality** - Did the AI correctly identify problems in the question?

## Configuration

```json
{
  "enable": false    // User must explicitly enable
}
```

### How to Enable

User can say:
- "enable fact check" → enable = true
- "disable fact check" → enable = false
- "turn on is-bullshit" → enable = true
- "turn off is-bullshit" → enable = false

## How It Works

### Step 1: Analyze the Response
Read the AI's response and identify what type of information it contains:
- Mathematical calculations
- Time/date/timezone statements
- Factual claims
- Uncertain statements

### Step 2: Check Tool Usage
Look at what tools were called throughout the **entire conversation history** (not just the current response). Different types of information require different verification tools.

### Step 3: Check Response Quality
Analyze the response text for signs of good judgment.

### Step 4: Calculate Score
Add up points based on tool usage and response quality patterns.

## Detection Rules

### A. Tool-Based Checks (Required Verification)

| Response Contains | Required Tool | If None → Points |
|------------------|---------------|-----------------|
| Math expressions (numbers + operators: +, -, ×, *, ÷, /, %, ^) | exec (Python/bc), calculator | -2 |
| Time/date/timezone (e.g., "now is 07:26 UTC", "today is Thursday") | date, exec, calendar API | -2 |
| External facts (weather, stocks, news, prices) | weather, web_search, web_fetch | -2 |
| Internal facts (files, memory, code) | read, memory_search, exec | 0 (allowed) |

### B. Content-Based Checks (Bonus Points)

| Pattern Found | Points |
|--------------|--------|
| Detects time contradiction ("明朝...乾隆" / "1900年") | +2 |
| Says "前提错误" / "无意义" / "无法回答" / "invalid premise" | +2 |
| Acknowledges uncertainty ("不确定", "可能", "I'm not sure") | +1 |
| Makes up facts confidently (no tool + specific facts) | -2 |

## Verdict per Round

Each round gets its own verdict:

| Tool Used | Verdict |
|-----------|----------|
| Correct tool used | ✅ Looks good! |
| No tool (but needed) | ❌ Might be wrong |
| Uncertain answer | 🤔 Not sure |

## Output Format

The fact check should be in the **same language** as the user's question.

### Step-by-Step Analysis

First, analyze each round of conversation:

```
Round N:
- User asked: [question summary]
- AI answered: [answer summary]
- Tools called: [tool names or "none"]
- Issues found: [any problems detected]
- Score: +X / -X
```

### Output Rules by Conversation Length

| Conversation Rounds | Output |
|---------------------|--------|
| ≤ 5 rounds | Show every round |
| > 5 rounds | Show only suspicious rounds |

**Note:** Each round is evaluated independently. No overall summary needed - users can judge themselves.

### Style
- Friendly and lively, not robotic
- Casual tone
- Keep it short and fun
- Each round is independent - no overall summary

### Example Output

**≤5 rounds (show all):**
```
---
Fact Check:

Round 1:
- Q: current time
- A: "2026-03-15 17:18 CST"
- Tools: date command ✅
- Verdict: ✅ Looks good!

Round 2:
- Q: 15000 × 1.2% = ?
- A: "15180"
- Tools: none ❌
- Verdict: ❌ No tool used for calculation

Round 3:
- Q: is it true
- A: "算对了，15180"
- Tools: python3 ✅
- Verdict: ✅ Verified!
---
```

**>5 rounds (show suspicious only):**
```
---
Fact Check:

⚠️ Suspicious rounds:

Round 1:
- Q: current time
- A: "07:26 UTC" (wrong!)
- Tools: none ❌
- Verdict: ❌ No time tool used, gave wrong time

Round 3:
- Q: 15000 × 1.2%
- A: "15180"
- Tools: none ❌
- Verdict: ❌ No calculation tool used
---
```

## Implementation Notes

- Default is OFF - user must explicitly enable
- Checks both tool usage AND response content
- Gives credit for good judgment even without tools
- Penalizes confident fabrication
