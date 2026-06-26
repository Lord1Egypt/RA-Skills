# MIT Reasoning Lite — Free Agent Decision Framework

Your AI agents are making decisions right now. Do you know how?

MIT Reasoning Lite gives your agents a 3-step reasoning scaffold that stops them from taking shortcuts you'll regret.

## What This Skill Does

Forces structured thinking before action. Three steps, drop-in install, no configuration required.

## The 3-Step Scaffold

**Step 1 — Clarify the Objective**
What is actually being asked? Not the surface request — the real intent. What outcome are we optimizing for?

**Step 2 — Check Constraints**
What rules, limits, history, or context applies to this decision? What's out of bounds?

**Step 3 — Reason Before Acting**
Articulate the reasoning *before* taking action. Show the work. If the reasoning doesn't hold up, the action doesn't happen.

## When to Use

Add this to your agent's SKILL.md or AGENTS.md to activate for any significant decision:
- Actions that affect external parties (sending emails, posting content, client communications)
- Actions that are difficult to reverse (file changes, purchases, delegations)
- Situations with ambiguous instructions
- Any time an agent has had a "why did it do that?" moment before

## Install

```bash
npx clawhub@latest install mit-reasoning-lite
```

Or manually: copy SKILL.md to your agent workspace.

## Usage

Reference in AGENTS.md:
```
Before any significant decision or action, apply MIT Reasoning Lite:
1. Clarify the real objective (not just the surface request)
2. Check all constraints and rules that apply
3. State your reasoning before acting
```

## Part of Trust AI Suite

MIT Reasoning Lite is the entry point to the Trust AI framework:

**Free skills (ClawHub):**
- **Accountable AI** — governance & accountability
- **Proof of Work** — verify agents completed what they claimed
- **MIT Reasoning Lite** (this) — structured decision-making

**Full version — MIT Reasoning ($19 on ClawMart):**
- 9-step full reasoning framework with branching logic
- Decision logging with timestamped rationale
- Uncertainty escalation (agent flags low-confidence decisions)
- Cross-agent consistency checks
- 6 pre-built decision templates

→ Full suite: [Trust AI Stack on ClawMart](https://www.shopclawmart.com)
