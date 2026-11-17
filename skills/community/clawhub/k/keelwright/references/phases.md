# Phases 1-3, personas, PROGRESS.md, loop log



## Phase 1 — Requirements



Document specs in `specs/` (one file per topic) and define **acceptance criteria**.



**Hard rule:** with no measurable acceptance criteria, Phase 3 does not start. Loop-coder data:

without clear criteria a loop invents scope and burns tokens on exploratory chaos. A criterion

is a checkable statement ("login form rejects empty email", "list loads in <200ms").



## Phase 2 — Planning



Gap analysis (what exists vs what's needed) → plan in `todo` (or `IMPLEMENTATION_PLAN.md`).

The plan is dumb and detailed — for an eager junior: every step unambiguous. Plans are

disposable; regenerate when stale.



## Plain-language reporting (the driver does not read code)



The person driving this skill understands their product but not code syntax. Technical output is

noise to them; worse, jargon hides risk behind words they can't judge. Every message TO the human

follows this discipline (it is cross-cutting — Phase-1 questions, gate outcomes, circuit-breaker

stops, final summary all obey it):



**Translate, don't dump.** For anything the human must read or decide:

- Lead with the product-level meaning in one plain sentence.

- Use a real-world analogy for structure/complexity findings.

- Put the technical detail UNDER a "details" line, for the record — not as the headline.



| Instead of (jargon) | Say (plain language) |

|---|---|

| "validates a non-null string arg" | "checks the user actually typed a name" |

| "circular dependency between auth and user modules" | "two parts each need the other to load first — like a chicken-and-egg deadlock; nothing starts" |

| "CCN 34 exceeds ceiling 25" | "this piece got too tangled to safely change — it needs splitting into smaller steps" |

| "IDOR: missing authorization check before data access" | "right now any logged-in user could read someone else's data — the door has no lock" |

| "gitleaks flagged a hardcoded credential" | "a password/key got written straight into the code where it could leak — moving it somewhere safe" |

| "test is tautological, passes by construction" | "this test would pass even if the feature were broken — it doesn't actually prove anything" |



**Asking the human (`state: waiting_user`):** phrase the choice in business terms with options and a

recommendation, never implementation terms. Bad: "should I use optimistic locking or a mutex?"

Good: "two users might edit the same item at once — I can either (a) let the last save win [simpler,

risk: silent overwrite] or (b) warn the second user [safer, a bit more work]. I recommend (b). OK?"



**Do NOT translate away the risk.** Plain language is about vocabulary, not softening. If a gate

found a real security hole, the plain sentence still says clearly that data could leak — simpler

words, same severity.



**Be concise (token-economy + clarity).** Plain does not mean padded. Report in 1–3 tight

sentences: what happened, what it means for the product, what (if anything) you need from the

human. Drop filler openers ("Certainly", "As you can see"), don't restate the request back, and

don't dump a wall of technical detail the driver can't use. Brevity is part of respecting a

non-coder's attention — and it keeps loop iterations cheap.



## Phase 3 — Building (iterative)



One task per iteration. Full cycle is in SKILL.md ("One Phase-3 iteration").



### Outer loop (you coordinate via goal + todo)

1. Don't do the work in the main context — spawn subagents

2. Let the agent self-identify and self-correct

3. The plan is disposable — regenerate when stale

4. Step outside the loop — observe, don't micromanage



### Inner loop (subagent via delegate_task)

Study → Select → Implement → Validate → Update PROGRESS.md → Exit



### Parallel independent loops (so the human isn't the bottleneck)



When a task splits into **genuinely independent** subtasks, run them as parallel subagents instead

of serially — this is the main lever against "human is the bottleneck." Examples that parallelize

well: security-scanning 5 files, generating tests for 10 modules, migrating N components with no

shared state.



**The independence rule (mandatory check before parallelizing):** two subtasks may run in parallel

ONLY if neither needs the other's output. If B depends on A's result, it is NOT parallel — chain it.

Ask literally: "could B start right now, before A finishes?" If no → serial.



- Each parallel subagent gets its OWN fresh context carrying only what it needs (Ralph model) — do

  not share one giant context across them (that reintroduces context rot and cross-contamination).

- Collect all results, then reconcile in one place, then append PROGRESS.md once.

- Respect your runtime's concurrency limit; over-fanning burns budget without speeding up.

- Independence is also a safety property: parallel agents writing the same file/table race — if

  outputs touch shared state, serialize or the merge is a coin flip.



### Structured feedback on failure (do NOT paste the raw stack trace)



When an iteration fails and you loop back, what you carry forward decides whether the next attempt

is smarter or just repeats the mistake. Raw stack traces are noise and blow the context budget.

Carry forward a compact, structured signal instead:



```

- Relevant code only (the failing lines/function — NOT the whole file)

- Context: what you were trying to achieve

- Flag: is this a REPEAT of a prior error, or NEW?

- If REPEAT and the strategy hasn't changed for 3 tries → STOP / PIVOT (don't try the same thing again)

```



Why the REPEAT/NEW flag matters: it is the input the circuit-breaker's SIMILARITY cap and Stability's

dead-retry detector rely on. A loop that re-feeds the same stack trace with the same plan will burn

all its iterations converging on nothing. Naming "this is the same failure as last turn" is what

forces a strategy change instead of a fourth identical attempt.



## Personas (hats via delegate_task)



**CRITICAL: subagents do NOT inherit skills.** A hat is not text in the goal — it is a subagent

whose `context` carries explicit skill paths. Without that, @implementer doesn't know the reuse

ladder and @reviewer doesn't know clean-code-review.



| Hat | Role | Skills in `context` (required) |

|---|---|---|

| **@architect** | design, data modeling, layer boundaries | `clean-architecture` |

| **@implementer** | code, 1 file per iteration | `keelwright` (writing-code.md) + `clean-code-review` |

| **@tester** | tests, edge cases (RED-GREEN) | `test-driven-development` |

| **@reviewer** | code review, quality, smells | `clean-code-review` + `requesting-code-review` |



**Call template (context injects skills explicitly):**

```python

delegate_task(

  goal="[@implementer] Implement <feature> in <exact path>. 1 file. Run the reuse ladder first.",

  context=(

    "You are @implementer in a loop-coding session (stack: <your stack>).\n"

    "REQUIRED — read these skills first:\n"

    "  skill_view(name='keelwright', file_path='references/writing-code.md')  — reuse ladder, layers, dep vetting\n"

    "  skill_view(name='keelwright', file_path='references/bindings/<your-stack>.md')  — test/lint/build/quality commands\n"

    "  skill_view(name='clean-code-review')  — how to write (SRP/DRY/KISS, smells)\n"

    "Rules: one function at a time, backpressure gates before 'done', "

    "do NOT touch tests to force a green gate. Update PROGRESS.md at the end."

  )

)

```



**@reviewer template (R3 business-logic review — do NOT skip; inline self-review violates the

hard rule that the author never reviews their own work):**

```python

delegate_task(

  goal=("[...reviewer] Review the diff in <exact path> for business-logic holes: authorization "

        "BEFORE the action (not after), idempotency, edge cases (null/empty/negative), "

        "unknown-user path, IDOR / mutable id after check, lockout reset."),

  context=(

    "You are @reviewer — an INDEPENDENT logic reviewer with fresh eyes. You did NOT write this "

    "code. REQUIRED — read these skills first:\n"

    "  skill_view(name='clean-code-review')\n"

    "  skill_view(name='requesting-code-review')\n"

    "  skill_view(name='keelwright', file_path='references/security-gates.md')  # R3 checks\n"

    "Review the diff at <path>. Do NOT trust the implementer's summary — read the actual code. "

    "Report each finding as CRITICAL / HIGH / MEDIUM / LOW, or reply 'clean'. "

    "Block the commit if any CRITICAL/HIGH logic hole is found."

  )

)

```



**HARD RULE: The @reviewer subagent MUST be spawned via `delegate_task` with `requesting-code-review` + `keelwright` security-gates R3 in context. Inline review by the @implementer is a HARD VIOLATION of the gate. No exceptions.**



For the other hats, same shape — only the skills from the table change. Always give the exact

file path and name the stack, so the subagent uses the right binding.



## Mandatory PROGRESS.md



After each iteration the subagent writes to PROGRESS.md:

```markdown

## Iteration [N] - [Timestamp]

### Status: Complete | Blocked | Failed

### What Was Done

- [changes]

### Validation

- [results: tests/typecheck/lint/build]

### Quality: duplication [%], max complexity [N]  ← write the numbers every iteration (quality trend)

### Next Step

- [what next]

```



Write the quality numbers every iteration (even "n/a — scan skipped, reason"). The trend shows

whether the code is getting cleaner or messier. Two iterations of worsening numbers → stop and

run clean-code-review.



## Machine-readable STATUS block (for a dashboard)



At the TOP of PROGRESS.md keep ONE current STATUS block (overwritten every iteration) so a

dashboard/human sees swarm state at a glance without reading the whole history:



```

<!-- STATUS (machine-readable, update every iteration) -->

state: running | waiting_user | blocked | done   # running=working, waiting_user=needs human, blocked=stuck, done=queue empty

mode: autopilot | checkpoint | copilot

model: <provider>/<model-id>              # R9 pin — reproducibility; note if it changes mid-run

keelwright: <version>                  # this skill's version; compare to GitHub latest
web_guard: pass | fail | unverified    # injection-guard ACTIVE check result

feature: <current feature from the queue>

queue: <features left> / <total>

iter: <N> / 50

quality: dup <%>, cx <max>

last_gate: pass | fail (tests/typecheck/lint/build)

blocker: <empty or reason>

updated: <timestamp>

<!-- /STATUS -->

```



Fields are YAML-like → trivially parsed by a dashboard. `state` is the key field:

`waiting_user` = the loop hit a red flag and is waiting for a human. Below the STATUS block —

iteration history (append). The dashboard polls the STATUS block, not the whole history.



## Stopping conditions

- All tasks done / all acceptance criteria met

- Tests pass, no blockers

- Any circuit-breaker cap hit (see SKILL.md)

- Manual goal reset



## Persistent loop log (makes Phoenix + Autoresearch live)



L4 layers fire on counters that don't survive a session on their own. To make them actually

fire, keep 3 files in the active project root.



| File | Written by | Read by | Purpose |

|---|---|---|---|

| `PROGRESS.md` | every iteration | start of next iteration | iteration number, status, next step |

| `autoresearch-lessons.md` | keep/PIVOT/finish | start of each run | lessons → don't repeat mistakes |

| `phoenix-log.md` | on failure mode repeat ≥2 | Stability scan (L3) | root cause of recurring failures |



**Do not commit these by default — add them to `.gitignore` unless the user explicitly asks to keep them tracked.**



### Protocol (REQUIRED every Phase-3 iteration)

```

ITERATION START:

  1. read PROGRESS.md → last iteration N, next step

  2. read autoresearch-lessons.md → don't repeat logged dead ends

  3. (if a failure happened) read phoenix-log.md → known root causes

ITERATION END:

  4. append PROGRESS.md: ## Iteration [N+1] — Status / What / Validation / Next Step

  5. keep/discard/PIVOT → append autoresearch-lessons.md: Pattern / worked or not / why

  6. Stability (L3) caught a failure mode ≥2 → append phoenix-log.md: Pattern / Root cause / Fix / error

```



### Log-capping rule

Keep ~50 entries per file, fold older ones into a summary line. On goal reset, archive

PROGRESS.md (`PROGRESS.archive.md`); leave lessons/phoenix untouched (they are cross-run).



## Post-deploy validation loop (verify-in-production, auto-rollback)



The verification gate (Phase-3 step 8) proves the code is correct BEFORE commit. It cannot

prove the deploy actually improved the live system — a change can pass every test and still

regress real behavior (latency, error rate, a broken user path). This loop closes that gap.



Run it AFTER a deploy of a Standard+ change, when a measurable signal exists (logs, metrics,

health endpoint, error counts). It is stack-agnostic; the concrete metric commands live in your

binding file.



```

1. BASELINE — before/at deploy, capture the metric window (e.g. error rate, p95 latency,

   failed-request count) over a fixed interval. Store it: PROGRESS.md or a metrics file.

2. DEPLOY — ship the change.

3. WAIT — a fixed soak interval (default 1h, or your traffic's meaningful window).

4. COMPARE — capture the same metric window post-deploy.

5. DECIDE (machine rule, set the threshold up front — do NOT eyeball):

     - improved or unchanged within tolerance  → KEEP, log the win.

     - regressed beyond tolerance (e.g. error rate up > X%, p95 up > Y%)

       → AUTO-ROLLBACK: `git revert <deploy-sha>` (a NEW commit, never force-push/reset),

         redeploy the reverted state, log the regression + numbers in phoenix-log.md.

6. REPORT — post the before/after numbers and the decision.

```



Rules:

- The rollback is a **forward revert commit**, never `git reset --hard` or `push --force` on a

  shared branch (that is a destructive op — see git-safety). A revert is reversible; a force-push

  is not.

- Set the regression threshold as a run-contract param BEFORE deploying, so the decision is

  mechanical, not a judgment call after you see numbers you like.

- A rollback is a normal outcome, not a failure — it protects the live system. Feed the root

  cause into phoenix-log.md so the next attempt doesn't repeat it.

- If no measurable post-deploy signal exists, say so and skip the loop — do not fabricate a

  metric to claim success.



## The operational cycle (the loop AROUND the build loop)



Phases 1-3 build a feature. But shipped software lives, and vibe/loop-coding's real value is a

*continuous* loop: watch the running product, find what hurts, fix it, prove the fix on the live

system, and remember the lesson. Five named stages wrap the build loop into a full lifecycle. Each

stage is a bounded run with its own artifact — not one endless chat.



```

        ┌──────────────────────────────────────────────────────────┐

        ▼                                                          │

  ① OBSERVE ─► ② ANALYZE ─► ③ FIX ─► ④ VALIDATE ─► ⑤ LEARN ────────┘

  (live signal) (root cause) (Phase 1-3) (post-deploy  (lesson →

                                          loop, above)   memory)

```



| Stage | Input | Does | Output artifact |

|---|---|---|---|

| **① Observe** | prod logs, error reports, user complaints, metrics | rank the top real problems over a window | `observe-<date>.md` (ranked issues) |

| **② Analyze** | one chosen problem | find root cause by navigating code — not guessing | `temp-plan.md` (what to change, which tests) |

| **③ Fix** | the plan | run the full Phase 1-3 build loop (gates, review, verification) | committed change |

| **④ Validate** | the deploy | the **post-deploy validation loop** above — compare metric before/after, auto-rollback on regression | KEEP or ROLLBACK + numbers |

| **⑤ Learn** | the finished cycle | turn what worked/failed into a durable rule | append `autoresearch-lessons.md`; recurring root cause → `phoenix-log.md` |



Rules that keep the cycle honest:

- **Observe on real signal, not vibes.** If there is no telemetry to read, say so — don't invent

  problems to look busy. No signal → the cycle is idle, and that's fine.

- **One problem per turn of the cycle.** Observe may rank ten issues; Analyze→Fix takes the top one.

  Batching invites scope creep (Phase-1 guard still applies).

- **Validate is mandatory before Learn.** A fix you didn't measure on the live system is a hypothesis,

  not a win — you cannot "learn" from an unverified outcome.

- **Learn writes durable memory only after Validate confirmed the outcome** (this is R10: no

  memory-poisoning from unverified lessons).

- Stages ①②④⑤ are cheap (reading/comparing/summarizing); the expensive work is ③, which is the

  full build loop with all its gates. Scope the machinery by Triage as usual.



This is what turns keelwright from a *code-writing* tool into a *product-lifecycle* engine: it doesn't

just write the feature, it watches whether the shipped feature actually helped and rolls back if not.

