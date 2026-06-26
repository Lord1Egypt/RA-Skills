---
name: openclaw-proper-usage
description: Operate OpenClaw reliably with right skill/tool selection, scoped execution, and verification-first completion.
---

# OpenClaw Proper Usage

## Core Rule
1. Clarify objective + output format
2. Pick one best tool/skill
3. Execute in scoped steps
4. Verify with concrete evidence
5. Report result + next action

## Routing
- Planning/strategy/analysis: gemini
- Web search: gemini
- Code review: gemini
- Code implementation/tests: Claude CLI (daedalus-code)

## Subagent Pattern
1. Split into 2–5 independent streams
2. Strict scope + expected output per stream
3. Launch, monitor, merge evidence-backed outputs only
4. Resolve conflicts explicitly

## Commands
sessions_spawn task:"<task+deliverable+constraints>" label:"<label>" model:"azure-openai/gpt-4.1" thinking:"low"
agents_list

## Completion Contract
Every task response must include: what changed, what ran, pass/fail, risks, next action.

## Triage
- Tiny: do it directly
- Ambiguous: clarify first
- Web-heavy: Gemini first
- Planning-heavy: Gemini first, Claude for implementation
- Broad: split → parallelize → merge
- Risky: plan + verify before edits
