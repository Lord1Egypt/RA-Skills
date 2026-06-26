---
name: gemini-cli
description: Use the local Gemini CLI for one-shot prompts, structured JSON output, shell-assisted research, and delegated AI-to-AI workflows on this Linux host. Use when you want to call the installed `gemini` command directly via `exec`, verify Gemini CLI availability/auth, run fast secondary model opinions, generate or refine code/content through Gemini, or orchestrate iterative local work where OpenClaw handles files/shell while Gemini provides another model's output.
---

# Gemini CLI

Use the locally installed `gemini` command through `exec`.

## What this skill is for

Use this skill when you want Gemini CLI as a second brain on the same Linux machine.
Typical uses:
- Get a second opinion from another model
- Ask Gemini to draft code, UI text, page copy, SQL, shell, or content
- Ask Gemini for structured JSON that OpenClaw can post-process
- Let OpenClaw inspect/edit files while Gemini generates plans, code, or rewrites
- Run quick one-shot prompts without spawning a separate ACP harness

This skill is for local CLI usage, not browser automation.
If the user wants deep coding delegation over many steps, prefer ACP sessions or coding-agent.

## Safety boundary

Gemini CLI can influence what gets executed, but it does not get direct tool access by itself.
Keep the control loop like this:
1. OpenClaw reads files and inspects the environment
2. OpenClaw sends a bounded prompt to Gemini CLI
3. OpenClaw reviews Gemini output
4. OpenClaw decides what to execute, edit, or reject

Do not blindly pipe Gemini-generated shell into execution.
Review before running anything destructive or external.

## First-time setup and preflight

If this is the first time using Gemini CLI on a machine, do not assume install alone is enough.
The user should complete Gemini CLI authentication first, then run a smoke test.

Basic checks:
```bash
which gemini
gemini --help
gemini -p "hello"
```

Interpretation:
- If `gemini --help` works but `gemini -p "hello"` fails, auth is usually missing or expired.
- If `gemini -p "hello"` returns a normal answer, the CLI is ready.

Practical rule:
1. Install Gemini CLI
2. Complete Gemini CLI login/authentication if prompted by the CLI
3. Run `gemini -p "hello"`
4. Only then rely on this skill

Known note on this machine:
- Gemini CLI may warn that `keytar` is missing and fall back to FileKeychain.
- That is not fatal if the prompt still completes.

## Core usage patterns

### 1) Simple one-shot prompt

```bash
gemini -p "Summarize the tradeoffs between Astro and Next.js for a landing page site."
```

Use for quick answers, rewrites, summaries, naming, content ideas, or code snippets.

### 2) Save output to a file for later processing

```bash
gemini -p "Generate 5 hero headline options for a SaaS analytics site." > /tmp/gemini-headlines.txt
```

Then read or parse that file with OpenClaw tools.

### 3) Request strict JSON

Ask Gemini to return only JSON.

```bash
gemini -p 'Return only valid JSON: {"pages":[{"path":"/","title":"...","sections":["..."]}]}'
```

Best practice:
- Explicitly say "Return only valid JSON"
- Give the exact schema shape
- Avoid markdown fences
- Validate before trusting

### 4) Feed file context safely

Prefer bounded context, not giant dumps.

```bash
cat ./src/app/page.tsx | gemini -p "Review this file and suggest a cleaner component structure. Return concise bullet points only."
```

Better yet, use OpenClaw `read` first and then craft a focused prompt.

### 5) Multi-step AI-to-AI workflow

Recommended pattern:
1. OpenClaw inspects repo/files
2. Gemini produces plan/spec/UI copy/code draft
3. OpenClaw applies edits locally
4. Gemini reviews diff or rewritten file
5. OpenClaw finalizes

This is the right way to get “AI同士が会話して自律的に作る” behavior without surrendering execution control.

## Good prompts for website generation

### Site spec prompt

```bash
gemini -p 'You are helping design a small website. Return only JSON with keys: stack, pages, components, copy_style, seo_keywords, risks. Product: local Instagram analytics service for Japanese small businesses. Goal: conversion-focused landing page.'
```

### Copywriting prompt

```bash
gemini -p 'Write Japanese landing page copy for a service that improves Instagram operations for stores. Tone: energetic, trustworthy, masculine, conversion-focused. Return sections for hero, pain points, benefits, CTA, FAQ.'
```

### UI implementation prompt

```bash
gemini -p 'Generate a single-file HTML landing page with embedded CSS for a Japanese marketing service. Make it mobile-first, bold, readable, and production-lean. Output code only.'
```

### Refactor/review prompt

```bash
gemini -p 'Review this React component for readability and conversion-focused UX. Return only: issues, fixes, rewritten component.'
```

## When to use `exec` vs ACP/session delegation

Use Gemini CLI via `exec` when:
- The task is one-shot or short-loop
- You want another model's wording or plan quickly
- OpenClaw remains the main orchestrator
- You only need text/code output from Gemini

Do not force Gemini CLI through `exec` when:
- The task needs a persistent coding agent loop
- The task needs thread-bound collaboration in chat
- The task needs autonomous repo exploration over a long time
- The task needs tool use beyond shell text I/O

For those, prefer ACP sessions.

## Recommended command patterns

### Clean text response

```bash
gemini -p "<prompt>"
```

### Model switching

If the installed Gemini CLI supports model selection flags in its current version, prefer explicit model selection when you need predictable behavior.
Check supported options first:

```bash
gemini --help
```

Common practice:
- inspect help output for model-related flags or config options
- set the model explicitly when running important prompts
- reuse the same model during a multi-step workflow to reduce drift

Safe guidance for this skill:
- do not guess unsupported flags
- verify the exact syntax from `gemini --help` on the current machine
- if a default model changed unexpectedly, re-run with an explicit model setting supported by that CLI version

### JSON capture

```bash
gemini -p 'Return only valid JSON with keys ...' > /tmp/gemini.json
```

### Large prompt from file

Use a temp file when the prompt gets long or must be reproducible.

```bash
cat /tmp/prompt.txt | gemini -p "$(cat)"
```

If shell quoting gets ugly, write a temp prompt file first with `write` and use shell substitution carefully.

## Operating rules for this workspace

- Use Gemini CLI as an advisor/generator, not an unsupervised executor
- Let OpenClaw own file edits, command execution, and validation
- For coding work, prefer this loop: inspect → ask Gemini → edit locally → test → ask Gemini to review
- If Gemini outputs code, save it to a temp file or inspect inline before applying
- If the output is meant to drive shell commands, require an explicit review step
- If authentication fails or Gemini hangs, fall back to OpenClaw-native work or ACP delegation

## Optional helper scripts

If you need repeatable flows, use the bundled scripts in `scripts/`:
- `scripts/gemini_json.sh` — ask Gemini for JSON-only output
- `scripts/gemini_review.sh` — send a file to Gemini for review with a fixed prompt wrapper

Read those scripts before modifying them.

## Troubleshooting

### CLI exists but prompts fail
- Check auth state by running a tiny prompt like `gemini -p "hello"`
- If that fails, complete Gemini CLI login/authentication first
- Expect possible FileKeychain fallback warning
- If output still returns, it is usable

### Need to change models but not sure how
- Run `gemini --help`
- Look for model-selection flags or config options supported by that installed version
- Use explicit model selection for important or repeatable workflows
- Do not rely on guessed flags copied from a different Gemini CLI version

### Output is too fluffy
- Demand exact format
- Say `Return only valid JSON`
- Say `Output code only`
- Give explicit section names or schema

### Shell quoting is breaking the prompt
- Write the prompt to a temp file first
- Avoid nested quote hell
- Keep prompts plain and deterministic

### User wants full autonomous site building
That is possible only in a controlled loop.
Use Gemini CLI to generate plans/code, but keep execution and editing in OpenClaw.
For larger builds, combine this skill with ACP or coding-agent.
