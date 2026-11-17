# Keelwright — architecture diagram (source of truth)

This is the canonical text schema. The rendered PNG/SVG in this folder is generated FROM this
file — if they ever disagree, THIS file wins. Keep it in sync with the risk glossary in SKILL.md
(same term names) and the mechanisms in `references/`.

Three things this diagram must make obvious at a glance:
1. **It is a loop, with nested loops** — not a linear pipeline. The Phase-3 iteration cycles on
   itself; Match Loop nests inside it; an outer operational cycle wraps the whole thing.
2. **Safety cannot be switched off** — security gates are hard stops even on Autopilot.
3. **A human who does not read code stays in control** — every gate has a plain-language
   translation, and the autonomy dial decides how often the human is asked.

---

## Layer 0 — the human (plain-language envelope)

```
╔════════════════════════════════════════════════════════════════════════════════════╗
║  YOU (need not read code): GOAL + ACCEPTANCE CRITERIA ─────────► ◄── PLAIN-LANGUAGE  ║
║                                                                      REPORT / BUILD  ║
║  ⭐ DNA: the human understands LOGIC, not syntax. Every gate below is translated to  ║
║     plain words ("this checks the password is right"), never "string arg to fn()".   ║
╚════════════════════════════════════════════╤═══════════════════════════════════════╝
                                              ▼
```

## Layer 1 — control (how much freedom, how much machinery)

```
  ┌──────────────────────────────────────────────────────────────────────┐
  │ 🎛 AUTONOMY DIAL   Autopilot → Checkpoint → Copilot                    │
  │    ⭐ freedom = blast radius (auth/money/prod → Copilot: approve each). │
  │ 🗂 TRIAGE  Trivial │ Low │ Standard │ High │ Critical                  │
  │    ⭐ machinery = risk. Trivial → Express path, no per-iter scans.      │
  │                                                                          │
  │ ⬚ LOOP DESIGN 5 whiteboard questions (before Phase 1)                   │
  │    trigger · check · action · stop · escalate                            │
  │    ⭐ answer before any code; skip = building a demo.                    │
  └──────────────────────────────────┬───────────────────────────────────┘
                                      ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │ PHASE 1 · REQUIREMENTS ─ no acceptance criteria? ⛔ STOP, ask.         │
  │                          ⭐ never invents scope.                        │
  │ PHASE 2 · PLANNING     ─ a dumb, detailed todo for an eager junior.    │
  └──────────────────────────────────┬───────────────────────────────────┘
                                      ▼
```

## Layer 2 — the build loop (Phase 3, one task = one turn, repeats)

```
╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 3 · BUILDING — ITERATION LOOP   ⭐ discipline INSIDE writing,         ║
║                                          not cleanup afterward               ║
║ ┌────────────────────────────────────────────────────────────────────┐     ║
║ │ ① @implementer writes (1 file/fn) ◄ REUSE LADDER — reuse before      │    ║
║ │        │                            adding a lib/abstraction         │     ║
║ │        ▼                            catches: over-engineering        │     ║
║ │ ② BACKPRESSURE GATES: tests │ typecheck │ lint │ build               │     ║
║ │        ▼                                                             │     ║
║ │ ③ STRUCTURAL-INTEGRITY GATE  ⭐ closes spaghetti / big ball of mud:  │     ║
║ │      jscpd (dup) · lizard (CCN) · madge/import-linter (cycles) ·     │     ║
║ │      eslint-boundaries (layers) · knip/vulture (dead code)          │     ║
║ │        ▼            catches: spaghetti, lava flow, tangled deps      │     ║
║ │ ④ 🛡 SECURITY GATES R1–R12  ⭐⭐ machine-enforced, cannot disable    │     ║
║ │      even on Autopilot   catches: OWASP·secrets·slopsquat·IDOR       │     ║
║ │        ▼                                                             │     ║
║ │ ⑤ 🔍 R3 BUSINESS-LOGIC REVIEW ► spawn @reviewer (fresh context)     │     ║
║ │        │  ⭐ NOT self-review   catches: happy-path bias, auth holes  │     ║
║ │        ▼                                                             │     ║
║ │ ⑥ fix high-tier findings                                            │     ║
║ │        ▼                                                             │     ║
║ │ ⑦ ✅ VERIFICATION GATE ⭐⭐ Definition of Done:                     │     ║
║ │      a) read+compile+diff  b) test red→green  c) not tautological    │     ║
║ │      d) ad-hoc verify if no framework                               │     ║
║ │      catches: "works on my machine", "I fixed it" with no diff       │     ║
║ │        ▼                                                             │     ║
║ │ ⑧ visual? ►┌─ MATCH LOOP (nested sub-loop) ⭐ ────────────────────┐ │     ║
║ │        │    │ Generator ⇄ Analyst: render → browser → numeric a11y│ │     ║
║ │        │    │ contrast≥4.5:1 · no overflow · sizes. repeat until   │ │     ║
║ │        │    └─ convergence ◄────────────────────────────────────── ┘ │    ║
║ │        ▼                                                             │     ║
║ │ ⑨ git commit (atomic) ► ⑩ PROGRESS.md + STATUS + tool-budget count  │     ║
║ │        └──────────────────────► next task ─┐                        │     ║
║ │ ⑪ cadence: /3 → STABILITY scan  /10 → AUTORESEARCH  /N → refactor   │     ║
║ └──────────────────────────────────────────────┘  ▲ LOOP BACK ────────┘     ║
║                                                    (while tasks remain)      ║
╚════╤═══════════════════════╤════════════════════════════╤════════════════════╝
     ▼ perimeter supervision  ▼                            ▼
```

## Layer 3 — perimeter supervisors (watch the whole loop, can stop/steer/learn)

```
┌──────────────────┐ ┌──────────────────────────┐ ┌────────────────────────────┐
│🚦 CIRCUIT-BREAKER │ │📉 STABILITY (5 modes)     │ │🔄 SELF-LEARNING ⭐          │
│ catches: doom loop│ │ catches: goal drift,      │ │ Phoenix: root-cause of      │
│ + token/$ burn    │ │ oscillation, thrash       │ │ repeats ACROSS sessions     │
│ 4 caps: 50 iters /│ │ dead-retry·oscillation·   │ │ Autoresearch: lessons →     │
│ 5 no-progress /   │ │ drift·amplification·      │ │ memory (promote on repeat)  │
│ 2h / 3× repeat    │ │ feedback-starvation       │ │ ⭐ learns, doesn't repeat    │
│ + PER-ITER BUDGETS│ │ ESCALATION LADDER:        │ │ the same mistake            │
│ ≤10 shell/5 file/ │ │ 3→REFINE 5→PIVOT          │ │                            │
│ 3 external        │ │ 2→ask 3→blocker           │ │                            │
│ → graceful STOP   │ │ keep RESETS counters      │ │                            │
└──────────────────┘ └──────────────────────────┘ └────────────────────────────┘
 ▲▲ REWARD-HACKING GUARD ⭐⭐ never weaken/delete a test to go green — fix code, not metric ▲▲
 ▲▲ PERSONAS (delegate_task): @architect @implementer @tester @reviewer                     ▲▲
 ▲▲                          @architecture-critic @visual-qa                                ▲▲
 ▲▲ STRUCTURED FEEDBACK ⭐ into each iteration: relevant code + intent + "repeat vs new"     ▲▲
 ▲▲                       flag — NOT a raw stack-trace dump (saves tokens, sharpens retry)   ▲▲
```

## Layer 4 — outer operational cycle (production lifecycle, wraps everything)

The build loop ships a feature. This outer cycle keeps the LIVE system healthy after ship —
this is what makes keelwright a lifecycle engine, not just a code writer.

```
        ┌───────────────────────────────────────────────────────────────┐
        │  🔭 OBSERVE ─► 🩺 ANALYZE ─► 🔧 FIX ─► ✅ VALIDATE ─► 🎓 LEARN   │
        │   read prod    root-cause    run the    post-deploy    update    │
        │   logs/reports  + plan       build loop  metric compare lessons  │
        │       ▲                                   ↓ regressed?           │
        │       └───────────────────────────────────┘ AUTO-ROLLBACK       │
        │                                              (git revert, not    │
        │  ⭐ verify-in-production + auto-rollback: a bad deploy that       │
        │     passes tests is caught by the metric, not by a human.        │
        └───────────────────────────────────────────────────────────────┘

  ⚡ PARALLEL: independent subtasks run as separate empty-context loops (fan-out),
     re-joined after. Rule: only if truly independent — if B needs A's result, it is NOT parallel.
```

## Bottom banner — system-wide differentiators

```
  🔒 BATTLE-TESTED QA ⭐⭐⭐  A/B (control vs skill), fact-checked on disk, not self-report —
                             published WITH an honest adversarial report (found+fixed defects).
  💸 ZERO COST · FULL TRANSPARENCY ⭐  (plain markdown, orchestrates free tools — no install of keelwright itself required; you bring your own free CLI tools)
  🗣 PLAIN-LANGUAGE THROUGHOUT ⭐  built for people who read logic, not syntax.
```

---

## Risk-coverage map (mirror of SKILL.md glossary — keep identical)

Each named industry failure mode → the layer that closes it. ✅ machine-enforced/on-disk;
⚠️ partial (honest — no cheap machine detector).

| Named risk | Closed by | Coverage |
|---|---|---|
| Context rot / context decay | fresh-context handoff + PROGRESS.md | ✅ |
| Ralph (Wiggum) loop | the loop model itself (state in files) | ✅ |
| Spaghetti code / big ball of mud | structural-integrity gate (③) | ✅ structure |
| Lava flow (dead code) | dead-code gate (knip/vulture) | ✅ |
| Dependency hell | reuse ladder + dep vetting | ✅ |
| Slopsquatting | R8 verify + GuardDog | ✅ |
| "Works on my machine" | verification gate (⑦) | ✅ |
| Reward hacking / spec gaming | reward-hacking guard | ✅ |
| Doom loop / death loop | circuit-breaker + budgets | ✅ |
| Goal drift | Stability L3 + goal re-read | ✅ |
| Happy-path bias | R3 review | ✅ |
| Technical debt (80% problem) | R4 checklist | ✅ critical paths |
| No design-for-failure | R5 fault checklist | ⚠️ warning |
| Secret leakage | R2 Gitleaks | ✅ |
| SQL injection / OWASP | R1 Semgrep + review | ✅ |
| Reasoning-action disconnect | R7 + verification | ✅ |
| Sycophancy | R7 catches false claims; fresh reviewer | ⚠️ partial (claims, not trait) |
| Multi-agent cascade / memory poisoning | R10 isolate + verify-before-memory | ⚠️ warning |
| Malicious third-party skill | R11 SkillSpector audit | ✅ |
| Model version drift | R9 pin | ⚠️ warning |
| Token/budget burn | per-iteration budgets | ✅ |
| Style/consistency drift | @architecture-critic + Pink Flag | ⚠️ partial (no machine detector) |
| Loop design absence | 5 whiteboard questions (Loop Design) | ✅ |
| Context rot in long loops | compaction (trim/summarize/delegate) | ✅ |
| Event storm / rate limiting | rate limit + debounce + backpressure | ✅ |
| Regression that passes tests | post-deploy validation + rollback | ✅ where metric exists |
| Human as bottleneck | autonomy dial + parallel loops | ✅ |
| Confabulation / fabricated facts | factual-grounding gate (verify-before-assert) | ⚠️ partial (discipline) |
