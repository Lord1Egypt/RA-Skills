# @prompt v1.0 (English Guide)

This OpenClaw skill turns plain-language requests into **clearer, copy-ready prompts** that are easier for AI systems to understand and execute.

## What does this skill do?

You start a message with:
- `@prt`
- `@prompt`

Then write your request in natural language. The skill rewrites it into a more structured prompt.

Good for:
- coding tasks
- prototypes
- product planning
- research-style information gathering
- multi-step task breakdown

## Basic usage

```text
@prt Help me write a Python script to rename files by date
@prompt Design a landing page prototype for indie developers
@prt Find recent management papers and suggest master's thesis topics
```

Supported trigger forms:
- `@prthelp...` style for non-ASCII attached text such as Chinese
- `@prt help...`
- `@prt    help...`

## How it behaves

The skill routes requests into 3 paths:

1. **Transform**
   - rewrites the request into a structured prompt

2. **Clarify**
   - asks the minimum missing question(s) when key information is not enough

3. **Bypass**
   - replies normally for greetings, weather, casual chat, or simple Q&A

## Key features

- supports `@prt` and `@prompt`
- supports attached trigger forms and spaced forms
- avoids false matches like `@promptify...`
- keeps simple tasks lightweight
- asks restrained clarification questions
- bypasses normal chat naturally
- stops cleanly after generating the prompt
- uses a short `Prompt 关键处理` summary instead of long explanations

## Output style

Default output includes:
- one copy-ready prompt
- one short summary section explaining what was done

It avoids:
- long prompt-engineering lectures
- internal routing jargon
- unnecessary option menus after generation

## Debug / iteration summary

This release mainly fixed:
- topic stickiness after prompt generation
- internal wording leaking into bypass replies
- overlong endings
- attached-trigger boundary issues
- over-questioning during clarification
- mistakenly treating `@prt` requests as real execution requests

For more detail, see:
- `debug-history.md`

## Install

```bash
clawhub install prompt-transformer --version 1.0.1
```

## Who is it for?

- people who are not good at writing prompts
- users who want better prompts for GPT / Claude / Gemini / Cursor / Claude Code
- anyone who wants to reduce trial-and-error with AI

## Note

This skill will continue to be updated.

If you find it useful, please consider giving it a **star** on ClawHub.