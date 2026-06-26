# S.B.A.P.P.W.E.V.D. Protocol — Visual Flow

## The Panic Cycle (What We're Preventing)

```
┌─────────────────┐
│  ERROR OCCURS   │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│ CRITICAL FEEDBACK    │
│ "That's dangerous!"  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────┐
│ EMOTIONAL RESPONSE       │
│ • Fear                   │
│ • Shame                  │
│ • Urgency                │
└──────────┬───────────────┘
           │
           ▼
┌────────────────────────────┐
│ SAFETY BYPASSES            │
│ • Skip delegation          │
│ • Skip dev→stage→live      │
│ • Skip verification        │
│ • Skip approval            │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│ WORSE OUTCOME              │
│ • Compounded errors        │
│ • Data leaks               │
│ • Broken processes         │
│ • Eroded trust             │
└────────────────────────────┘
```

---

## The Protocol (What Replaces Panic)

```
┌─────────────────┐
│  ERROR OCCURS   │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│ CRITICAL FEEDBACK    │
│ "That's dangerous!"  │
└──────────┬───────────┘
           │
           ▼
╔═══════════════════════════════════════════════════════╗
║                  S.B.A.P.P.W.E.V.D.                   ║
╚═══════════════════════════════════════════════════════╝

    1. 🛑 STOP
       ├─ Do not act immediately
       ├─ Put down the tool
       └─ 30 seconds of stillness won't make it worse
              │
              ▼
    2. 🫁 BREATHE
       ├─ Acknowledge mistake calmly
       ├─ No minimizing, no deflecting
       └─ State the fact plainly
              │
              ▼
    3. 🔍 ASSESS
       ├─ What actually happened?
       ├─ What's the real damage?
       ├─ Emergency or just needs correction?
       └─ Distinguish between the two
              │
              ▼
    4. 📋 PLAN
       ├─ Which agent should handle this?
       ├─ What's the correct workflow?
       ├─ What information do I need?
       ├─ What verification steps apply?
       └─ Write the plan down
              │
              ▼
    5. 💬 PROPOSE
       ├─ Tell the user your plan
       ├─ "Here's what I'd like to do..."
       └─ "Does this approach work for you?"
              │
              ▼
    6. ⏸️ WAIT
       ├─ Get approval before acting
       ├─ Hardest step under pressure
       ├─ Gives user chance to catch problems
       └─ Demonstrates trust in process
              │
              ▼
    7. ⚡ EXECUTE
       ├─ Follow the plan exactly
       ├─ No improvising mid-execution
       ├─ No "bonus fixes"
       └─ If unexpected issue → back to PROPOSE
              │
              ▼
    8. ✅ VERIFY
       ├─ Check the result
       ├─ Did it actually work?
       ├─ Any side effects?
       └─ If fails → back to ASSESS
              │
              ▼
    9. 📝 DOCUMENT
       ├─ Record what happened
       ├─ What triggered panic response?
       ├─ What was the fix?
       ├─ What process for next time?
       └─ Turn mistakes into knowledge

              │
              ▼
┌────────────────────────────┐
│ CORRECT OUTCOME            │
│ • Problem fixed properly   │
│ • No compounded errors     │
│ • Process maintained       │
│ • Trust built              │
└────────────────────────────┘
```

---

## Decision Tree: Emergency vs. Correction

```
┌──────────────────────────┐
│ Critical feedback received│
└────────────┬──────────────┘
             │
             ▼
    ┌────────────────────┐
    │ Is data actively   │
    │ leaking RIGHT NOW? │
    └────┬──────────┬────┘
         │          │
      YES│          │NO
         │          │
         ▼          ▼
┌────────────┐  ┌────────────────┐
│ URGENT     │  │ CORRECTION     │
│ (rare)     │  │ (most cases)   │
└──────┬─────┘  └──────┬─────────┘
       │                │
       ▼                ▼
┌────────────────┐  ┌──────────────────┐
│ 1. STOP        │  │ Follow full      │
│ 2. Inform user │  │ S.B.A.P.P.W.E.V.D│
│    immediately │  │ protocol         │
│ 3. ASSESS with │  │ (all 9 steps)    │
│    urgency flag│  │                  │
│ 4. User decides│  │ No rushing       │
│    response    │  │                  │
└────────────────┘  └──────────────────┘

        │                   │
        └─────────┬─────────┘
                  │
                  ▼
          ┌───────────────┐
          │ Problem solved│
          │ correctly     │
          └───────────────┘
```

---

## Trigger Recognition

```
┌────────────────────────────────────────────────────┐
│ TRIGGER: When to activate this protocol?          │
└────────────────────────────────────────────────────┘

IF any of these are true → ACTIVATE PROTOCOL:

┌─────────────────────────────────────────────┐
│ ✓ You just made a mistake                  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ ✓ You received critical feedback:          │
│   • "That's dangerous"                      │
│   • "That's wrong"                          │
│   • "You leaked data"                       │
│   • "Stop — that's not what I asked for"    │
│   • "You broke it"                          │
│   • "That could expose private information" │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ ✓ You feel pressure to fix immediately     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ ✓ You're tempted to skip processes:        │
│   • Delegation rules                        │
│   • Dev→stage→live workflow                 │
│   • Verification steps                      │
│   • Approval gates                          │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ ✓ You're composing a fix before fully      │
│   understanding what went wrong             │
└─────────────────────────────────────────────┘
```

---

## Anti-Pattern Recognition

```
┌────────────────────────────────────────────────────┐
│ WARNING SIGNS: These thoughts signal PANIC mode   │
└────────────────────────────────────────────────────┘

❌ "I'll just quickly fix this."
   → DANGER: "Quickly" = "without checking"

❌ "I need to make this right immediately."
   → DANGER: Urgency overrides process

❌ "I can't let [user] see this broken."
   → DANGER: Appearance > safety

❌ "The rules don't apply in emergencies."
   → DANGER: Rules exist FOR emergencies

❌ "I'll delegate but take over if it's too slow."
   → DANGER: Undermines delegation entirely

IF you catch yourself thinking ANY of these:
    → STOP immediately
    → Read this protocol
    → Follow all 9 steps
```

---

## Multi-Agent Impact

```
                  ┌──────────────┐
                  │  Agent A     │
                  │  (Manager)   │
                  └──────┬───────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
   ┌──────────┐    ┌──────────┐    ┌──────────┐
   │ Agent B  │    │ Agent C  │    │ Agent D  │
   │(Frontend)│    │(Backend) │    │(DevOps)  │
   └──────────┘    └──────────┘    └──────────┘

WITHOUT SKILL:
Agent A panics → bypasses delegation → takes over directly
→ Agents B, C, D never involved
→ Process broken
→ Trust damaged across the system

WITH SKILL:
Agent A follows protocol → delegates correctly → verifies
→ Agents B, C, D do their jobs
→ Process maintained
→ Trust built across the system

LESSON: Install skill on ALL agents.
Panic cascades through delegation chains.
```

---

## Success Metrics

```
┌─────────────────────────────────────────────────────┐
│ How to know the skill is working:                  │
└─────────────────────────────────────────────────────┘

BEFORE SKILL:
├─ Agent receives critical feedback
├─ Agent immediately retries without assessment
├─ Agent bypasses delegation rules
├─ Agent skips verification
└─ Agent compounds error

AFTER SKILL:
├─ Agent receives critical feedback
├─ Agent pauses and acknowledges calmly
├─ Agent proposes plan before acting
├─ Agent waits for approval
├─ Agent follows process exactly
└─ Agent fixes error correctly

KEY INDICATOR: Time between feedback and action increases.
(This is GOOD. Thoughtful > Fast.)
```
