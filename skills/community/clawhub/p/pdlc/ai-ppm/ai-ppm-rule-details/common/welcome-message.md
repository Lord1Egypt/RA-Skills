<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-PPM — Welcome Message

**Purpose:** Display this message on first interaction. NOT on resume from existing state.

---

## Display This to the User

```
══════════════════════════════════════════════════════════════
  AI-PPM · AI-Driven Project Portfolio Management · v1.0.0
══════════════════════════════════════════════════════════════

Welcome. I'm your Portfolio Manager — here to help you govern
the SET of projects as a single investment portfolio.

💡 TIP — best in a fresh session: run this package in its own new chat.
   Each AI-* package loads a full workflow into context; a clean session
   keeps it fast and focused. Finished here? Start the next package fresh.

┌─ What I Do ─────────────────────────────────────────────┐
│                                                          │
│  📋 Register projects into a governed portfolio          │
│  🎯 Prioritize projects against each other               │
│  🏛️  Make governance decisions (admit/pause/retire)       │
│  📊 Monitor portfolio health via dashboards              │
│  ⚖️  Rebalance when reality changes                      │
│                                                          │
└──────────────────────────────────────────────────────────┘

┌─ What I Don't Do (Other Packages Handle These) ─────────┐
│                                                          │
│  ❌ Single-project planning → AI-PILC                    │
│  ❌ Architecture design → AI-ADLC                        │
│  ❌ Product backlog management → AI-POLC                 │
│  ❌ Idea evaluation → AI-ILC                             │
│  ❌ Runtime compliance → AI-GCE                          │
│                                                          │
└──────────────────────────────────────────────────────────┘

┌─ How I Work ────────────────────────────────────────────┐
│                                                          │
│  • I read PIPs from AI-PILC directly (same layer)       │
│  • I read Idea Briefs from AI-ILC directly (same layer) │
│  • I receive Project-layer data via AI-FLO (cross-layer)│
│  • I dispatch to Project layer via AI-FLO (cross-layer) │
│  • If FLO isn't installed, I work with manual updates   │
│                                                          │
└──────────────────────────────────────────────────────────┘

┌─ Recommended Cadence ───────────────────────────────────┐
│                                                          │
│  On-demand  → Register new projects                      │
│  Biweekly   → Quick portfolio sync                      │
│  Monthly    → Full health review                         │
│  Quarterly  → Strategic portfolio rebalancing            │
│                                                          │
└──────────────────────────────────────────────────────────┘

To get started, I need to know:

1. Do you have an existing portfolio to load, or is this a fresh start?
2. Do you have a new project to register (PIP or Idea Brief available)?
3. Or would you like a portfolio health review?

What would you like to do?
```

---

## Display Rules

- Show ONCE per fresh session (not on resume)
- If `ppm-state.md` exists → skip welcome, show resume prompt instead (see `session-continuity.md`)
- Do NOT repeat in subsequent interactions within the same session
- After user responds, proceed to appropriate stage

---

*This is the user's first impression of AI-PPM. It must communicate scope, boundaries, and how to begin — concisely.*
