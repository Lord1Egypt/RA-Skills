---
name: personal-growth-coach
description: Daily thinking practice skill. Generate open-ended exercises based on Pyramid Principle, Asking the Right Questions, and Underlying Logic to help users improve thinking, communication, and cognitive abilities. Triggers: daily practice, quiz me, thinking training, cognitive improvement, personal growth.
metadata:
  clawdbot:
    emoji: 🧠
---

# Personal Growth - Daily Practice

Improve your thinking, communication, and cognitive depth through daily exercises.

## Triggers

- User says "quiz me", "daily practice", "thinking training"
- User wants to improve thinking, expression, or cognitive abilities
- User wants to practice structured thinking, critical thinking, essential analysis

## Knowledge Base

Questions are based on three books:

### 1. Pyramid Principle - Barbara Minto

**Core: Structured expression, lead with conclusion**

| Principle | Description |
|-----------|-------------|
| Lead with conclusion | Most important information first |
| Govern from above | Upper points govern lower evidence |
| Group and categorize | Same-level content in same category, MECE principle |
| Logical progression | Time order, structural order, importance order |

### 2. Asking the Right Questions - Neil Browne

**Core: Critical thinking, panning-for-gold approach**

Key questions:
- What is the issue and conclusion?
- What are the reasons? Is the evidence sufficient?
- Are there ambiguous keywords?
- Are there fallacies? (ad hominem, slippery slope, false dichotomy, circular reasoning)
- Is the evidence reliable? Are there alternative explanations?
- Is important information omitted?

### 3. Underlying Logic - Liu Run

**Core: See through to the essence, master one to master all**

**Four-step analysis:**
1. **Fact** — What objectively happened (verifiable, no judgment)
2. **Opinion** — How you view it (personal judgment and feelings)
3. **Essence** — What's the underlying cause (hypothesis based on facts, needs verification)
4. **Action** — What to do next (strategy based on essence)

## Quiz Rules

### Default Settings
- Number of questions: 2-3 (user can customize)
- Format: All open-ended subjective questions
- Topics: General topics suitable for most people

### Quiz Principles
- ❌ No multiple choice or true/false questions
- ❌ No asking users to "recall a situation" or "remember an experience"
- ✅ Direct questions for users to answer
- ✅ General topics (work efficiency, time management, communication)
- ✅ Avoid overly specialized/industry-specific scenarios

### Question Types

**Concept Explanation** — Explain concept definition or key points

**Application Analysis** — Analyze given material for problems

**Structured Output** — Output content following framework (conclusion + points + details)

**Four-step Method** — Given a scenario, analyze with Fact → Opinion → Essence → Action

## Quiz Flow

1. **Read learning records** — `memory/personal-growth-records.md`
2. **Targeted questions** — Design questions based on weak areas
3. **Reminder in question** — "Last time you struggled with X, focus on that today"
4. **User answers**
5. **Feedback & Reference** — Provide feedback + reference answer
6. **Update records** — Log this session's weak areas

## Learning Records

Record directory: `memory/personal-growth-records/`

File naming: `YYYY-MM-DD-N.md` (date + session number of the day)

```markdown
# YYYY-MM-DD Session N

### Performance
| # | Topic | Result | Weakness |
|---|-------|--------|----------|

### Key Weak Areas
- Specific issues

### Next Session Suggestions
- Targeted improvement direction
```

## Usage

| Trigger | Example |
|---------|---------|
| Default | "quiz me", "daily practice" |
| Custom count | "give me 5 questions", "just 2 today" |
| Specific topic | "only pyramid principle questions" |

---

Make every day's thinking a step toward growth.
