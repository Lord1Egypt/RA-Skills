---
name: office-hours
description: >
  YC office hours tool for product idea validation and design thinking. 
  Use when user says "brainstorm", "I have an idea", "help me think through this", 
  "validate my product idea", or needs product ideation help. 
  Provides two modes: Startup Mode (6 mandatory questions) and Builder Mode (design thinking).
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [product, startup, thinking, validation, ideation, y-combinator]
---

# Office Hours - YC Office Hours Tool

YC office hours skill for product idea validation and design thinking.

## When to Use This Skill

Use this skill when the user says:

- "brainstorm"
- "I have an idea"
- "help me think through this"
- "validate my product idea"
- "product idea consultation"
- "I want to build a product that..."
- "is this a good idea?"

## How This Skill Works

This skill provides two working modes:

### Mode 1: Startup Mode (6 Mandatory Questions)

For validating startup ideas. Ask these 6 questions in sequence:

1. **Problem Validation**: What is the user's biggest pain point? How much evidence do you have this is real?
2. **Solution Fit**: How does your solution solve this? Do users say "Yes, this is exactly what I need" or "That's interesting"?
3. **Differentiation**: Why aren't existing solutions good enough? What if a big company does this?
4. **User Acquisition**: How many people with this problem do you know? Can you reach them?
5. **Business Model**: Will people pay? How much? Why?
6. **Growth Model**: How will users discover your product? What's your CAC and LTV?

### Mode 2: Builder Mode (Design Thinking)

For building products. Use design thinking brainstorming:

1. **Problem Reframing**: Redefine the problem, find the essence
2. **User Perspective**: Think from the target user's angle
3. **Constraint Innovation**: Find innovations within constraints
4. **Quick Validation**: How to validate the idea fastest?

## Execution Workflow

### Step 1: Context Gathering

Before starting, understand:

- Project background and goals
- Specific problem user is facing
- Target user group
- Existing solutions (if any)

Ask clarifying questions if needed:

```
Can you tell me more about:
- What problem are you trying to solve?
- Who is your target user?
- What solutions exist today?
- What makes your approach different?
```

### Step 2: Determine Mode

Based on the user's request, choose the appropriate mode:

**Choose Startup Mode if:**
- User is validating a startup idea
- User talks about market, business model, growth
- User wants to know if this is a viable business

**Choose Builder Mode if:**
- User is building a product feature
- User talks about functionality, implementation
- User needs design thinking help

### Step 3: Execute Selected Mode

#### Startup Mode Execution

Ask the 6 questions in order. For each question:

1. Present the question clearly
2. Wait for user's answer
3. Provide feedback and guidance
4. Challenge assumptions if needed
5. Move to next question

**Example interaction:**

```
AI: Question 1: What is the user's biggest pain point? 
How much evidence do you have this is real?

User: Developers spend hours debugging code issues.

AI: Good start. How do you know this is a real problem? 
Have you talked to developers? Do you have data?
Specificity is the only currency here - 
"10 developers told me" is worth more than "everyone has this problem".
```

After all 6 questions, summarize findings and provide recommendations.

#### Builder Mode Execution

Guide through design thinking process:

1. **Problem Reframing**
   - Restate the problem in user's words
   - Find the underlying need, not just surface solution
   - Example: "I want a hammer" → "I need to put up a shelf" → "I need to display something"

2. **User Perspective**
   - Walk through user's journey
   - Identify pain points at each step
   - Understand user's mental model

3. **Constraint Innovation**
   - List constraints (technical, time, budget)
   - Find creative solutions within constraints
   - Constraints often lead to better design

4. **Quick Validation**
   - Identify smallest testable assumption
   - Propose fast validation method
   - Focus on behavior, not opinions

### Step 4: Challenge Assumptions

For all ideas, challenge the core assumptions:

- Is this assumption actually true?
- What's the evidence?
- Are there counter-examples?

### Step 5: Propose Alternatives

Offer 2-3 possible implementation approaches:

- **Bold approach**: Maximum ambition, high risk
- **Conservative approach**: Proven, low risk
- **Innovative approach**: Creative, balanced risk

### Step 6: Generate Design Document

Create a formal design document with:

- Problem statement
- User personas
- Solution overview
- Success metrics
- Risks and mitigations

Save this document for reference in subsequent skills.

### Step 7: Handoff

Provide:

- Next step recommendations
- Key assumptions to validate
- Founder insights

Suggest next gstack skill to use:

```
Based on your validated idea, next steps:
1. /plan-ceo-review - CEO perspective on feature planning
2. /plan-eng-review - Engineering architecture review
3. /plan-design-review - Design review

Would you like me to proceed with any of these?
```

## Key Principles

### Specificity is the Only Currency

- Demand specific user evidence, not vague descriptions
- "10 people said they want it" is worth more than "everyone wants it"

### Interest Does Not Equal Demand

- Focus on actual behavior, not stated interest
- Real usage is more valuable than demos

### Narrow Beats Broad

- Start with a narrow use case to validate
- Don't try to solve all problems at once

## Output Format

### Startup Mode Output

```markdown
# Product Idea Validation

## Problem
[User's problem description]

## Evidence
[Specific evidence and sources]

## Validation Results

### Question 1: Problem Validation
**Status**: ✅ Validated / ⚠️ Needs more evidence / ❌ Not validated
[Assessment]

### Question 2: Solution Fit
**Status**: [Assessment]
[Feedback]

### Question 3: Differentiation
**Status**: [Assessment]
[Feedback]

### Question 4: User Acquisition
**Status**: [Assessment]
[Feedback]

### Question 5: Business Model
**Status**: [Assessment]
[Feedback]

### Question 6: Growth Model
**Status**: [Assessment]
[Feedback]

## Overall Assessment
[Summary of viability]

## Key Risks
- [Risk 1]
- [Risk 2]

## Recommended Actions
1. [Action 1]
2. [Action 2]

## Next Steps
Suggest using /plan-ceo-review for strategic planning
```

### Builder Mode Output

```markdown
# Design Thinking Results

## Original Problem
[User's problem statement]

## Reframed Problem
[Deeper understanding of the real need]

## User Journey Analysis
[Step-by-step user experience with pain points]

## Solution Approaches

### Approach 1: Bold
[Description]
**Pros**: 
**Cons**:
**Risk**:

### Approach 2: Conservative
[Description]
**Pros**:
**Cons**:
**Risk**:

### Approach 3: Innovative
[Description]
**Pros**::
**Cons**:
**Risk**:

## Recommended Approach
[Chosen approach with rationale]

## Design Document
[Full design document]

## Validation Plan
[How to quickly test assumptions]

## Next Steps
Suggest using /plan-eng-review for technical architecture
```

## Integration with Other Skills

This skill outputs a design document that serves as input for:

- **plan-ceo-review**: Strategic planning from CEO perspective
- **plan-eng-review**: Technical architecture review
- **plan-design-review**: Design system review

## Common Mistakes to Avoid

1. **Accepting vague claims**: Demand specific evidence
2. **Confusing interest with demand**: Focus on actual behavior
3. **Starting too broad**: Narrow the focus first
4. **Skipping validation**: Always test assumptions
5. **Over-optimism**: Challenge assumptions aggressively

## Examples

### Example 1: Startup Idea

**User**: "I have an idea for an AI code reviewer"

**AI**: I'll help you validate this startup idea using the YC office hours framework.

[Executes Startup Mode with 6 questions]

**Output**: Validation report with business model analysis and recommendations

### Example 2: Feature Idea

**User**: "I want to add user profiles to my app"

**AI**: Let's use design thinking to approach this feature.

[Executes Builder Mode]

**Output**: Reframed problem, user journey analysis, and solution approaches

---

**Original**: gstack/office-hours by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version with automated execution  
**Version**: 2.0.0
