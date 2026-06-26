# Routing table

## Zero-LLM first

Route to `zero-llm` when:

- the task matches an existing deterministic skill
- the task is a shell command or script invocation with no reasoning dependency
- the task is repetitive automation with known safe inputs

Examples:

- `pet all my 53 gotchis`
- `show current cooldown`
- `run the existing batch script`

## Low-risk route

Route to `bankr/minimax-m2.5` when:

- the task is casual conversation
- the task is lightweight rewriting or summarization
- the task is simple classification or extraction
- the task is low-stakes and cheap turnaround matters most

## General reasoning route

Route to `bankr/claude-sonnet-4.5` when:

- the task involves planning, product thinking, architecture, or medium-complexity coding
- the request is important but not unusually risky
- the request is a routine wallet or treasury operation like a common swap, send, or treasury movement
- you need better judgment than a low-cost route provides

## Coding specialist route

Route to `bankr/gpt-5.2-codex` when:

- the task is code-heavy
- the task is repo surgery, refactoring, or implementation detail work
- precision in code generation matters more than general conversation quality

## Long-context / multimodal routes

- Use `bankr/gemini-3-pro` for long-context document digestion.
- Use `bankr/gemini-3-flash` for quick multimodal triage and cheap vision tasks.

## High-stakes route

Route to `bankr/claude-opus-4.6` when:

- the request is explicitly marked high-stakes
- the request touches wallet security review, signing risk, approvals, or ambiguous fund movement
- failure would be expensive enough that caution should dominate cost

## Default fallback policy

- primary low-risk fallback: `bankr/claude-sonnet-4.5`
- primary high-stakes fallback: `bankr/claude-opus-4.6`
- zero-LLM routes do not need a model fallback
