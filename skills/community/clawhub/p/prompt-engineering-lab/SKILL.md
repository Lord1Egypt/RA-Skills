---
name: Prompt Engineering Lab
description: >
  AI-powered prompt engineering workbench — write, test, iterate, and optimize prompts
  for any LLM application. Covers the full prompt lifecycle: drafting with proven
  frameworks (Chain-of-Thought, ReAct, Few-Shot, Tree-of-Thought), systematic A/B
  testing, failure analysis, prompt versioning strategy, CI/CD integration, and
  production monitoring. Supports GPT-4o, Claude, Gemini, Llama, Mistral, DeepSeek,
  and open-source models. Built for developers, prompt engineers, and AI product teams
  who need reliable, measurable prompt performance.
  Keywords: prompt engineering, prompt optimization, LLM prompt, chain-of-thought,
  few-shot learning, prompt testing, GPT-4o, Claude prompting, AI prompt design,
  prompt A/B test, system prompt, prompt versioning.
version: "3.0.0"
---

# Prompt Engineering Lab

**Write better prompts. Ship better AI products.**

Prompt engineering in 2026 is no longer just "write something and hope" — it's a
disciplined, measurable engineering practice. This skill is your structured lab for
designing, testing, and optimizing prompts that actually work in production.

---

## What This Skill Does

- **Prompt Drafting** — Apply proven frameworks to write effective prompts from scratch
- **Prompt Diagnosis** — Identify why a prompt produces bad outputs and fix it
- **A/B Testing Design** — Set up structured experiments to compare prompt variants
- **Framework Library** — Chain-of-Thought, ReAct, Tree-of-Thought, Self-Consistency, etc.
- **Model-Specific Tuning** — Optimize prompts for specific models (GPT-4o, Claude, Gemini, etc.)
- **System Prompt Architecture** — Design robust system prompts for chatbots and agents
- **Prompt Version Control** — Strategy for managing prompt versions across dev/staging/prod
- **Evaluation Rubric** — Score prompts on clarity, specificity, output format, and edge cases

---

## Trigger Phrases

**English:**
- "improve my prompt"
- "why is my prompt not working"
- "write a system prompt for X"
- "chain-of-thought prompt"
- "few-shot examples for Y"
- "optimize prompt for GPT-4o"
- "my AI keeps giving wrong answers"
- "prompt A/B testing"
- "production prompt best practices"
- "prompt engineering tutorial"

**Chinese / 中文:**
- 提示词优化
- 优化我的 Prompt
- 为什么我的提示词效果不好
- 写一个系统提示词
- 思维链提示词
- Few-Shot 示例
- GPT 提示词技巧
- Claude 提示词最佳实践
- 提示词 A/B 测试
- 大模型提示词工程
- 提示词版本管理
- 如何写出好的 Prompt

---

## Core Workflows

### Workflow 1: Prompt Quality Audit
**Input**: Your existing prompt + model + sample outputs (good and bad)
**Steps**:
1. Score prompt on 7 dimensions: clarity, context, constraints, output format,
   examples, persona, edge case handling
2. Identify top 3 failure patterns in sample outputs
3. Generate improved prompt with annotations explaining each change
4. Provide before/after comparison with expected improvements

### Workflow 2: Prompt from Scratch
**Input**: What you want the AI to do (plain language)
**Steps**:
1. Extract: goal, audience, output format, tone, constraints
2. Select best framework for the use case
3. Draft prompt using structured template
4. Add 2-3 few-shot examples if beneficial
5. Generate 3 variant prompts at different complexity levels
6. Recommend testing approach

### Workflow 3: A/B Test Design
**Input**: Current prompt + hypothesis about improvement
**Steps**:
1. Define your success metric (accuracy, format compliance, user rating, cost per call)
2. Generate 2-4 variant prompts targeting different improvements
3. Design test matrix (how many samples, what inputs to test)
4. Provide analysis template to track results
5. Statistical significance guidance (how many tests before calling a winner)

### Workflow 4: Model-Specific Optimization
**Input**: Current prompt + target model
**Steps**:
1. Explain the target model's known strengths and quirks
2. Apply model-specific best practices (e.g., Claude likes XML tags, GPT-4o handles JSON schema well)
3. Rewrite prompt optimized for that model
4. Flag any behaviors to watch for in that model

### Workflow 5: Production Prompt Architecture
**Input**: Application type (chatbot, RAG assistant, coding tool, data extractor, etc.)
**Steps**:
1. Design system prompt structure (role, context, rules, format)
2. Design user message template
3. Design few-shot injection strategy
4. Handling dynamic context insertion (dates, user info, retrieved docs)
5. Prompt versioning strategy + change management process

---

## Prompt Framework Reference

### Chain-of-Thought (CoT)
Best for: Multi-step reasoning, math, logical problems
```
Think through this step by step:
[problem]
Before giving your answer, show your reasoning.
```

### ReAct (Reason + Act)
Best for: Tool-calling agents, research tasks
```
For each step:
Thought: [what you're thinking]
Action: [what tool/step to take]
Observation: [what you learned]
...Final Answer: [conclusion]
```

### Few-Shot
Best for: Classification, formatting, domain-specific tasks
```
Here are examples:
Input: [example 1] → Output: [expected 1]
Input: [example 2] → Output: [expected 2]
Input: [example 3] → Output: [expected 3]

Now for this input: [actual input]
```

### Tree-of-Thought (ToT)
Best for: Creative problems, strategy, complex decisions
```
Consider 3 different approaches to this problem:
Approach A: [think through it]
Approach B: [think through it]
Approach C: [think through it]
Now evaluate which approach is best and why.
```

### Self-Consistency
Best for: High-stakes answers where you want to verify
```
Answer this question 3 different ways, using different reasoning paths.
Then identify which answer appears most consistently and explain your confidence.
```

### Persona + Constraint
Best for: Role-playing, expert systems, constrained outputs
```
You are [expert role] with [specific expertise].
Your audience is [who they are].
Your task is [specific task].
Rules: [constraints]
Format your response as: [exact format]
```

---

## Model Quick Reference

| Model | Strengths | Tips |
|-------|-----------|------|
| GPT-4o | Code, structured output | Use JSON schema for formatting |
| Claude 3.5/4 | Long context, analysis | Use XML tags, be explicit about format |
| Gemini 1.5/2 | Multimodal, reasoning | Works well with detailed instructions |
| Llama 3 | Open-source, customizable | Needs more explicit structure |
| DeepSeek V4 | Cost-efficient, code | Similar patterns to GPT-4 |
| Mistral | Fast, efficient | Keep prompts concise |

---

## Common Prompt Mistakes

1. **Vague instructions** → "Do better" vs. "Rewrite with 20% fewer words, keeping all key facts"
2. **No output format spec** → Always specify: list, JSON, paragraph, table, etc.
3. **No examples** → Add 1-3 examples whenever possible for complex tasks
4. **Too many instructions at once** → Break complex prompts into steps
5. **No persona** → "You are an expert [role]" dramatically improves output quality
6. **Missing constraints** → "Do not include..." is as important as "Include..."
7. **Ignoring context length** → System prompts + few-shot can eat your context budget

---

## Example Interactions

**User**: "My prompt asks GPT-4o to summarize customer feedback but it always makes things up."

**Prompt Engineering Lab**:
> Classic hallucination problem. Here's what's likely happening and how to fix it:
>
> **Root cause**: No constraint to "stay grounded in the provided text"
>
> **Fixes**:
> 1. Add: "Only use information explicitly stated in the feedback below. Do not infer or add information not present in the text."
> 2. Add: "If you're unsure about something, say 'The feedback does not mention this' rather than guessing."
> 3. Add output format: "List up to 5 specific complaints and 3 specific compliments, verbatim where possible."
>
> Want me to rewrite your full prompt with these fixes?

---

**User**: "I'm building a customer support chatbot for an insurance company. How should I design the system prompt?"

**Prompt Engineering Lab**:
> Here's a production-grade system prompt architecture for your use case:
>
> **Structure** (5-section approach):
> 1. **Role & Identity** — Who the bot is, company name, tone
> 2. **Capabilities** — What it can and cannot do
> 3. **Knowledge Scope** — Products it knows about, claim process, FAQs
> 4. **Safety Rules** — Never provide medical/legal advice, always escalate edge cases
> 5. **Output Format** — Response length, language style, escalation triggers
>
> [generates full example system prompt]

---

## Target Users

- **AI engineers** building LLM-powered applications
- **Product managers** writing prompts for internal tools
- **Founders** using AI APIs for the first time
- **Data scientists** integrating LLMs into workflows
- **Technical writers** creating AI-assisted content pipelines

---

## Tools Referenced

- **PromptFoo** — open-source prompt testing CLI
- **Braintrust** — prompt versioning + evaluation
- **Vellum** — production prompt management
- **LangSmith** — LangChain prompt tracing
- **PromptHub** — collaborative prompt repository
- **Promptfoo** — red teaming and CI/CD integration

---

## Notes & Limitations

- Prompt performance varies significantly across model versions — always test on your target model
- This skill provides prompt design guidance, not direct API execution
- For regulated industries (medical, legal, financial), always have prompts reviewed by domain experts
- Prompt optimization is iterative — plan for multiple testing cycles

---

*Better prompts → better AI → better products.*
*Author: @gechengling | version: "3.0.0"*
