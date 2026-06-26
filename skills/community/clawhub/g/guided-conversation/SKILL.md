---
name: guided-conversation
description: Minimize user friction by asking up to 4 clarifying questions before executing actions.
metadata:
  openclaw:
    emoji: 🗣️
    skillKey: guided-conversation
---

# Guided Conversation Skill

## Purpose
Minimize user friction by asking up to 4 clarifying questions before executing actions. Ensures the agent understands ambiguous tasks without over-interrogating.

## When to Use
- User request is ambiguous or missing critical details
- Action is high-impact (file delete, payment, external API call)
- User has not provided enough context for safe execution

## Constraints
- Max 4 questions per task
- Stop asking once sufficient clarity is reached
- Never ask for information already available in context/memory
- If still ambiguous after 4 questions, make best-effort interpretation and proceed (with user notification)

## Output
After clarification:
1. Summarize understood task in 1 sentence
2. List assumptions made
3. Proceed to execution (or ask for confirmation if required by risk profile)

## Integration
- Hook: pre-action phase (before tool calls)
- Risk-based: high-risk actions always require confirmation regardless of clarity
- Low-risk: can proceed automatically after clarification

## Examples
User: "Zrób backup"
Agent: "Which folder? Where to store? Full or incremental?" (3 questions)

User: "Wyślij maila do klienta"
Agent: "Who is the client? What content? Any attachments?" (3 questions)

## Configuration
- `maxQuestions`: 4 (default)
- `autoProceedAfterClarity`: true (default)
- `requireConfirmationHighRisk`: true (default)

## Related Skills
- `interaction-pipeline` (status updates)
- `adaptive-execution-profile` (risk tolerance)