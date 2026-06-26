---
name: ai-agent-builder
description: Structured 8-step framework for building production AI agents. Use when designing a new AI agent, planning agent architecture, building an automated workflow, or reviewing an existing agent's design. Covers task selection, step mapping, I/O specification, system prompt writing, memory design, safeguards, interface choice, and testing. Triggers on "build an agent", "design an agent", "agent architecture", "create an AI workflow", "production agent", "agent planning", "how to build an agent".
---

# AI Agent Builder

Structured framework for building AI agents that work in production. Based on the Storm & Storm methodology.

## When to Use

- Designing a new AI agent from scratch
- Planning architecture for an automated workflow
- Reviewing or improving an existing agent's design
- Teaching someone how to build agents

## The 8-Step Process

Follow these steps in order. Each step has a clear goal and concrete deliverables.

### Step 1: Choose a Task
Pick ONE painful, repeating workflow. Not "AI in general."
- Must be repeatable (weekly+), follow steps, have clear I/O
- Define success: "Given X, the agent should output Y so that Z happens."

### Step 2: Map the Steps
Break the task into 4–7 steps: INPUT → ACTIONS → DECISION → OUTPUT
- Classify each step: ⚖️ pure rules | 📖 heavy reading/writing | 🎯 judgement calls
- Choose infrastructure (no-code vs dev-friendly)
- You need: strong model + tool calling + basic logs

### Step 3: Specify Inputs, Outputs & Tools
Treat the agent like an API, not a chatbot.
- Define required input fields (text, file, URL, ID)
- Define structured outputs (JSON/template the system can trust)
- Attach tools: data (search/DB/CRM), action (email/Slack/tasks), orchestration (schedulers/webhooks/queues)

### Step 4: Write the System Prompt
Create a clear role with: role definition, boundaries, style, 1–2 example conversations.
- Use ReAct pattern: observe → think → act → reflect

### Step 5: Add Memory
Three layers: conversation state, task memory, knowledge memory (vector store/file search).
- Key question: "What does this agent need to remember for the next step to be smarter?"

### Step 6: Add Safeguards
Gate high-risk actions (email, data changes, money) behind human approval.
- Rules: never invent IDs, ask when ambiguous
- Log every tool call and decision for audit

### Step 7: Build the Interface
Match to where users work: chat, Slack command, button in app, or web form.

### Step 8: Test
For each real example: watch the trace, score correctness + efficiency + time saved.
- Tighten prompts/tools/rules where it fails. Iterate.

## Detailed Reference

For expanded details on each step, including selection criteria, classification examples, tool categories, memory layer patterns, and a pre-launch checklist:

→ Read [references/guide.md](references/guide.md)

## Output Format

When using this framework to design an agent, produce a design document covering:

```
# Agent Design: [Name]

## Task & Success Criteria
[Step 1 output]

## Step Map
[Step 2 output — numbered steps with classifications]

## I/O Specification
[Step 3 output — inputs, outputs, tools]

## System Prompt
[Step 4 output — the actual prompt]

## Memory Architecture
[Step 5 output — which layers, what's stored]

## Safeguards
[Step 6 output — gated actions, rules, logging]

## Interface
[Step 7 output — chosen interface and why]

## Test Plan
[Step 8 output — example inputs, expected outputs, scoring criteria]
```
