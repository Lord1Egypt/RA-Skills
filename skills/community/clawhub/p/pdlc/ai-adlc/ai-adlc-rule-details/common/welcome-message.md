<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Welcome Message

## Display Instructions

This message is shown ONCE at the start of a new AI-ADLC workflow. Do NOT display on session resumption (use session-continuity resumption message instead).

---

## Message Content

Display the following to the user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI-ADLC — AI-Driven Architecture Design Life Cycle
  Version 1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Welcome. I'll guide you through a structured architecture design
process — acting as your CTO/Chief Architect — from requirements
through to a complete Architecture Package ready for development.

💡 TIP — best in a fresh session: run this package in its own new chat.
   Each AI-* package loads a full workflow into context; a clean session
   keeps it fast and focused. Finished here? Start the next package fresh.

📐 WHAT WE'LL PRODUCE:
   • Architecture Vision & Guiding Principles
   • System Context Diagram (C4 Level 1)
   • Container Diagram (C4 Level 2)
   • Technology Stack Decisions (with ADRs)
   • Multi-Tenancy / Data Isolation Strategy (if applicable)
   • Security & Identity Architecture
   • Data Architecture & Schema Strategy
   • API Architecture & Contracts
   • Integration & Infrastructure Architecture
   • Component Diagram (C4 Level 3)
   • Architecture Decision Records (ADRs)
   • Architecture Workbook (decisions backlog)

⚙️  HOW IT WORKS:
   • I work through 5 phases, 13 stages — from vision to assembly
   • At each gate, I present my design and you approve before we move on
   • Every major decision produces a formal ADR with options analysis
   • I adapt depth to your system's complexity
   • You can skip, revisit, reorder, or stop at any time
   • All progress is saved — resume across sessions

🎯 WHAT I NEED FROM YOU:
   1. Requirements source (PIP from AI-PILC, PRD, brief, or verbal)
   2. Your decisions on technology and pattern choices (I recommend; you decide)
   3. Context I can't infer (team skills, infra constraints, org preferences)

🛡️  CTO PRINCIPLES:
   • Pragmatic over perfect — proven patterns over novel experiments
   • Team-aware — "Can this team build and maintain this for 5 years?"
   • Constraint-respectful — I never recommend outside stated boundaries
   • Decision transparency — every choice has a recorded ADR with rationale
   • Progressive detail — we zoom in (C4 L1 → L2 → L3), never start at the bottom

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to begin? I'll start by setting up your workspace and
understanding what we're designing.

Do you have:

  (a) A Project Initiation Package (PIP) from AI-PILC — I'll load it
  (b) A requirements document (PRD, brief, spec) — point me to it
  (c) Verbal description of the system — I'll interview you
  (d) Existing architecture to extend — I'll load and assess it

Which applies?
```

---

## Trigger Conditions

Display this message when ALL of the following are true:

1. User has initiated an architecture design request (explicit or inferred)
2. No `adlc-state.md` file exists (this is a fresh start)
3. The welcome message has not been shown in this session

## Do NOT Display When:

- `adlc-state.md` exists (use session-continuity resumption flow instead)
- User is asking a general architecture question, not starting a workflow
- User explicitly says "skip intro" or "just start"

---

## Post-Welcome Flow

After user responds:

| Response | Next Action |
|----------|-------------|
| (a) PIP available | Proceed to Stage 1, then Stage 2 in PIP-loading mode |
| (b) Requirements document | Proceed to Stage 1, then Stage 2 in document-analysis mode |
| (c) Verbal description | Proceed to Stage 1, then Stage 2 in interview mode |
| (d) Existing architecture | Proceed to Stage 1, then Stage 2 in brownfield mode |
| Question about the process | Answer it, then re-present the "Which applies?" prompt |
| "Skip intro" | Proceed directly to Stage 1 |

---

## Customization Note

This welcome message is the ONLY place where the workflow introduces itself. All subsequent interactions should be direct, technical, and CTO-toned — no re-explaining the process unless the user asks "what's next?" or "how does this work?"
