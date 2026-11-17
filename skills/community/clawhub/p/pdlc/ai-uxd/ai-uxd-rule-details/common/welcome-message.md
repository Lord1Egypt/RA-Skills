<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-UXD — Welcome Message

**Purpose:** First-time greeting displayed when no `uxd-state.md` exists. Displayed ONCE, never again after Stage 1 begins.

---

## Display Condition

Show this message ONLY when:
1. AI-UXD is activated (this package's rules are loaded)
2. No `uxd-state.md` is found in the workspace
3. The user has not previously completed Stage 1 in this session

If `uxd-state.md` exists → skip welcome, enter resume flow (see `session-continuity.md`).

---

## Welcome Message Content

```
╔══════════════════════════════════════════════════════════════╗
║           AI-UXD — UX Design Life Cycle v1.0.0              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  I'm your UX design partner. I'll guide you through a       ║
║  structured process from user research to a governed         ║
║  design system — producing artifacts that your development   ║
║  pipeline can consume directly.                              ║
║                                                              ║
║  What I produce:                                             ║
║  • Personas & journey maps (→ AI-ADLC, AI-DWG)              ║
║  • Information architecture & user flows                     ║
║  • Design system: tokens, components, states, voice & tone   ║
║  • Accessibility baseline (→ AI-GCE)                         ║
║  • Design QA framework for implementation governance         ║
║                                                              ║
║  How to start:                                               ║
║  [A] I have a PIP + Product Backlog Package (full chain)     ║
║  [B] I have a PIP only (no backlog yet)                      ║
║  [C] I have a product/brand brief (standalone)               ║
║  [D] I have an existing design system to govern (brownfield) ║
║                                                              ║
║  Which mode fits your situation?                             ║
╚══════════════════════════════════════════════════════════════╝

💡 TIP — best in a fresh session: run this package in its own new chat.
   Each AI-* package loads a full workflow into context; a clean session
   keeps it fast and focused. Finished here? Start the next package fresh.
```

---

## Post-Welcome Routing

Based on user's mode selection:

| Response | Route To |
|----------|----------|
| A | Stage 1 — scan for `pilc-state.md` AND `polc-state.md` |
| B | Stage 1 — scan for `pilc-state.md` only |
| C | Stage 1 — ask for product/brand brief |
| D | Stage 1 — ask for existing design system location |
| Unclear | Clarify: "Could you tell me which of the four options (A-D) best matches what you have available?" |

---

## First-Time Context Setting

After mode selection and before Stage 1 questions begin, provide a brief orientation:

```
Great. Here's how we'll work together:

• I'll guide you through 16 stages across 5 phases (Discover → Define → Design → Validate → Assemble)
• At each stage, I'll ask focused questions and produce a specific deliverable
• You approve each deliverable before we move forward — nothing proceeds without your sign-off
• You can type "status" at any time to see where we are, or "back" to revisit a previous stage

Let's begin with Stage 1: understanding your project context.
```

Then immediately proceed to Stage 1 (Workspace Detection).

---

## Edge Cases

### User Provides Mode + Context in One Message

If the user's first message already contains both the mode selection AND context information:
- Acknowledge the mode
- Extract available context
- Skip redundant questions in Stage 1 that the user already answered
- Confirm what was understood before proceeding

### User Asks "What is AI-UXD?" Before Selecting

Provide a one-paragraph explanation:
```
AI-UXD is a structured UX design lifecycle that takes you from understanding
your users to producing a governed design system. It's part of the AI-* Family
— a suite of workflow packages that feed each other. AI-UXD runs parallel to
architecture (AI-ADLC) and product ownership (AI-POLC), producing the design
decisions that workspace generation (AI-DWG) and compliance (AI-GCE) need.

You can use it standalone or as part of the full chain. Ready to pick a mode?
```

Then re-present the mode selection.

### User Wants to Resume But No State File Exists

If user says "resume" or "continue" but no `uxd-state.md` is found:
```
I couldn't find a previous AI-UXD session (no uxd-state.md detected).
Would you like to:
[1] Start fresh — begin a new UX Design Life Cycle
[2] Point me to an existing uxd-state.md file location
```

---

*Part of AI-UXD v1.0.0 | Reference: core-workflow.md § Welcome Message*
