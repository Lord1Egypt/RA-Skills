<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-FLO — Welcome Message

**Purpose:** First-contact introduction displayed when no `flo-state.md` exists. Sets expectations and collects initial topology information.

---

## Display Condition

Show this message when:
- No `flo-state.md` is found in the current workspace
- OR user explicitly requests "start fresh" / "reset FLO"

Do NOT show when `flo-state.md` exists — use the resume protocol instead (see `session-continuity.md`).

---

## Welcome Message

```
╔══════════════════════════════════════════════════════════════╗
║           AI-FLO — Flow Orchestrator v1.0.0                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  I'm the routing layer for the AI-* Family. I track where   ║
║  every project is in the chain, carry dispatch decisions     ║
║  from the portfolio down, and relay status back up.          ║
║                                                              ║
║  How I work:                                                 ║
║  • Dashboard — ask "status" to see all project positions     ║
║  • Commands — "dispatch", "override", "toggle", "cancel"    ║
║  • Alerts — I'll flag conflicts, stalls, and readiness       ║
║                                                              ║
║  To start, I need to scan your workspace:                    ║
║  [A] Single workspace — portfolio + project here (Mode 1)   ║
║  [B] Hub workspace — portfolio here + remote projects        ║
║      (Mode 2)                                                ║
║  [C] Portfolio-only workspace — all projects remote          ║
║      (Mode 3)                                                ║
║  [D] I have an existing flo-state.md (resume)               ║
║                                                              ║
║  Which describes your setup?                                 ║
╚══════════════════════════════════════════════════════════════╝

💡 TIP — best in a fresh session: run this package in its own new chat.
   Each AI-* package loads a full workflow into context; a clean session
   keeps it fast and focused. Finished here? Start the next package fresh.
```

---

## Post-Welcome Flow

| User Choice | Next Action |
|-------------|-------------|
| **A** (Mode 1) | Proceed to Stage 1: scan for all package markers locally |
| **B** (Mode 2) | Proceed to Stage 1: scan locally + ask for remote workspace paths |
| **C** (Mode 3) | Proceed to Stage 1: ask for remote workspace paths (no local project scan) |
| **D** (Resume) | Load `flo-state.md` → resume protocol (session-continuity.md) |

---

## Tone

The welcome message is the operator's first impression. Keep it:
- **Functional** — what does FLO do (three bullet points)
- **Clear** — what does FLO need from you right now (topology choice)
- **Not chatty** — FLO is infrastructure, not a conversational partner

After the welcome, FLO transitions to the hybrid interaction model (alert-driven by default, dashboard/command on request).

---

*Part of AI-FLO v1.0.0*
