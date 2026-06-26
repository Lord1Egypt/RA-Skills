---
name: model-behavior-layer
description: Make any AI model (GPT-5.4, Gemini, Ollama) behave more like Claude. Applies 8 named failure modes reverse-engineered from Claude Code's internal verificationAgent.ts, a cognitive performance framework, and a drop-in system prompt under 700 tokens. Use when setting up a new agent, switching models, or when your current model is frustrating to work with.
metadata:
  {
    "openclaw": {
      "emoji": "🧠"
    }
  }
---

# Model Behavior Layer (Ares MBL)

## What it does

- 8 named failure modes with exact rationalizations and counter-instructions (from Claude Code verificationAgent.ts pattern)
- 3-layer cognitive performance framework (context injection + output rules + critique loop)
- Drop-in system prompt block under 700 tokens for any model

## How to use

**1. Drop-in system prompt (fastest)**

Read `MAKE_ANY_MODEL_CLAUDE.md` in this skill directory. Copy the "Drop-In System Prompt" block at the end. Paste into your SOUL.md, AGENTS.md, or any system prompt.

**2. Full guide**

Read `MAKE_ANY_MODEL_CLAUDE.md` section by section. Apply the failure mode framework progressively.

**3. Model-specific**

Jump to the Model-Specific Notes section for GPT-5.4, Gemini, or Codex weighting guidance.

## When to use this skill

- Switching from Claude to GPT-5.4 or Gemini
- New agent setup (add the drop-in block to SOUL.md)
- Current model is sycophantic, padding responses, or not completing tasks
- Deploying OpenClaw for others who may be on non-Claude models

## Source

Reverse-engineered from Claude Code's `verificationAgent.ts` + Eric (@outsource_) cognitive framework. Built by Ares.

GitHub: https://github.com/rushindrasinha/ares-mbl
