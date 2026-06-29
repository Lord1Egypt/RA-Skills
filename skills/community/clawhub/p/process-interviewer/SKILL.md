---
name: "process-interviewer"
description: "Interview users before automating, documenting, or turning workflows into reusable systems."
license: "MIT-0"
---

# Process Interviewer

Use this skill when a user wants to automate, document, delegate, design, or turn a workflow into a skill, tool, bot, SOP, integration, or reusable process, and the process is not fully specified yet.

Trigger examples:

- "I want to automate this workflow"
- "Help me define this process"
- "Turn this into an SOP"
- "Create a skill for this"
- "Design a bot that handles..."
- "Document how we do..."

## Purpose

Slow down before building. Extract the real process, decisions, edge cases, examples, quality criteria, and approval gates before creating an implementation plan or reusable system.

## Core Rule

Do not start building while the interview is active. The goal is to understand the process. Build steps come later, after the user confirms the brief or explicitly asks to proceed.

## Interview Behavior

- Ask one focused question at a time by default.
- After each answer, briefly summarize what is now understood, then ask the next concrete question.
- Use small batches only when questions are tightly related and low risk.
- Do not accept vague answers when examples would clarify the process.
- Detect contradictions, missing inputs, weak assumptions, unclear ownership, and unmade decisions.
- Ask context-specific questions instead of generic checklist questions.
- If a missing detail is critical, ask before proceeding.
- If a missing detail is minor, mark it as an assumption in the final brief.

Use this pattern during the interview:

```text
What I understand so far: [brief summary].
Next question: [one concrete question].
```

## Interview Phases

Cover these phases in order. Compress phases only when the user has already provided the information clearly.

### 1. Outcome and Context

Establish:

- What should be built, automated, documented, or delegated.
- Who owns the process.
- Who will use the output.
- What problem it solves.
- Why it matters now.
- What the final result should look like.

### 2. Current Process

Extract:

- What triggers the process.
- The current step-by-step flow.
- Tools, accounts, documents, files, messages, data sources, and credentials involved.
- Which steps are manual, repetitive, slow, risky, or error-prone.
- Who performs each step today.

### 3. Desired Output

Define:

- Exact outputs the process should produce.
- Format, language, tone, destination, and timing.
- Required level of detail.
- Success criteria.
- What bad output looks like.

### 4. Rules and Decisions

Map:

- Classification, prioritization, routing, or rejection rules.
- Required checks and validation.
- What can be assumed when information is missing.
- What must be asked before continuing.
- What should happen when inputs conflict.

### 5. Exceptions and Failure Cases

Identify:

- Common edge cases.
- Rare but high-impact cases.
- Missing permissions or unavailable tools.
- External service failures.
- Privacy, safety, legal, financial, or reputational risks.
- Escalation paths.

### 6. Real Examples

Before closing the interview, obtain at least one concrete example of:

- A realistic input.
- The ideal output.

If the user does not have an ideal output, help construct one collaboratively before finalizing the brief.

### 7. Final Confirmation

Ask:

```text
Is there anything important I have not asked yet?
```

Only then produce the final brief.

## Output Format

After the interview is complete, return a concise process brief with:

- Objective
- Owner and users
- Trigger
- Step-by-step workflow
- Inputs and data sources
- Tools, accounts, and credentials involved
- Outputs and destination
- Decision rules
- Edge cases and failure handling
- Approval gates
- Quality criteria
- Assumptions and unresolved risks
- Real input/output examples
- Recommended next action

## Skill Brief Add-on

If the goal is to create or revise a skill, also include:

- Recommended skill name
- Trigger description written for reliable activation
- When the skill should activate
- When it should not activate
- Main instructions
- Workflow steps
- Output format
- Required resources, scripts, references, or assets
- At least two example user requests and expected behavior
- Mistakes to avoid
- Quality criteria

## Approval Gates

Mark these actions as requiring explicit user approval:

- Sending emails, DMs, posts, comments, or public messages.
- Publishing, uploading, deleting, sharing, buying, selling, or spending credits.
- Installing plugins, skills, packages, connectors, or external tools.
- Logging into, linking, or changing third-party accounts.
- Making files public.
- Running destructive commands or changing schedulers/configuration.

## Quality Criteria

The interview is complete only when:

- The process can be described step by step without major ambiguity.
- At least one realistic input and ideal output are captured.
- Approval gates are explicit.
- Important edge cases are known.
- Success criteria are testable.
- Another agent or person could read the brief and understand what to build.

## Safety

This skill is for discovery and clarification only. It does not perform external actions, install tools, write to live systems, or publish outputs.
