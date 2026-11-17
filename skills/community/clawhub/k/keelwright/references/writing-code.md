# How to write code: reuse ladder, layers, dependency vetting, quality scan

The orchestrator does NOT duplicate what native skills already say — it calls them at the right
stage. This file is stack-agnostic; per-stack commands live in `bindings/<your-stack>.md`.

## Stage → native skill

Subagents and `delegate_task` do NOT inherit skills — pass the skill path in `context` when spawning.

| Stage | Skill to call |
|---|---|
| Reflection / what are we building | `brainstorming` |
| Writing the plan | `writing-plans` (or `plan`) |
| Simplifying code | `clean-code-review` |
| Checking layers | `clean-architecture` |
| Tests | `test-driven-development` |
| Fixing a bug | `systematic-debugging` |
| Final review | `requesting-code-review` → `simplify-code` |

## Reuse ladder (before EVERY unit of code)

Function, class, module, file — stop and walk the ladder top-down:

```
L0: Needed at all? → YAGNI — if "might be useful", drop it
L1: Already in the codebase? → reuse
L2: Language stdlib / framework built-in? → use it
L3: Already-installed dependency? → don't add a new one (check the manifest)
L4: Existing state/DI mechanism covers it? → don't add another
L5: Minimal implementation? → only what's needed now
L6: Full implementation → last resort
```

**Exceptions (do NOT simplify):** validation at trust boundaries, error handling, security,
accessibility.

**Prefer a function over a class for stateless logic.** A class whose only member is one
`@staticmethod` (or that holds no instance state) is a YAGNI smell — it adds a layer without
adding value. Use a plain module-level function. (Observed 2026-07-20: a skill-guided arm wrapped
a stateless CSV summarizer in a single-staticmethod class where the no-skill control correctly
used plain functions — the class was the *less* minimal choice. Don't let "structure" masquerade
as reuse.)

**Mark when skipping L0-L5:** `// reuse-ladder: skipped [X] (reason: …) | add when [scenario]`

## Workflow `/do [feature]`

0. **REFLECT** — don't jump into code. What are we building? Spec → design → plan → OK → code. (`brainstorming`)
1. **Skill discovery** — `skills_list` → `skill_view` for relevant ones (max 30s)
2. Read current status (or track via `todo`)
3. `delegate_task` — parallel subtasks (up to your runtime's concurrency limit)
4. **Approval — by autonomy level** (dial in SKILL.md):
   - **Autopilot** (default): don't wait for "let's build" — go plan→code→test→commit, show the result
   - **Checkpoint**: show the plan, wait for one OK
   - **Copilot** (risky: auth/money/DB/prod): approval at every step
   - The plan is always dumb and detailed, even when you don't wait for OK
5. **DEPENDENCY VETTING** — before adding ANY package (see below)
6. **During** — reuse ladder before each unit, one function at a time, after each:
   `git add . && git commit -m "feat: [name]"`, update status (`todo`)
7. **TESTING** (`test-driven-development`) — commands in `bindings/<your-stack>.md`
8. **PRE-COMMIT REVIEW** — security gates (`security-gates.md`) + auto-review (below)
9. **RELEASE** — git push per git-safety rules → CI builds → "✅ Shipped."

## Dependency vetting — before adding any package

Two DIFFERENT threats, checked in order. Do not skip step 1 — it is the one that stops the attack
that is actively exploited right now.

### Step 1 — Does the package even exist, and is it real? (anti-slopsquatting)

LLMs hallucinate package names: ~20% of LLM-recommended packages don't exist, and attackers
pre-register those hallucinated names with malware (slopsquatting — confirmed incidents on PyPI
and npm). OSV/CVE scanners MISS this: a package registered yesterday has no CVE yet. So before
CVEs, verify the package is genuine.

**A. Existence + age + adoption (registry lookup, no tooling):**
```bash
# npm — 404 = hallucinated (do NOT install). Check "created" date and version count.
curl -s https://registry.npmjs.org/PACKAGE_NAME | head -c 2000
# PyPI — same idea
curl -s https://pypi.org/pypi/PACKAGE_NAME/json | head -c 2000
```
Red flags → BLOCK and re-check the name with the user: package doesn't exist; created in the last
~30 days; near-zero downloads; name is a close typo of a popular package.

**B. Malware/typosquat scan (GuardDog — Datadog, Apache 2.0):**
```bash
pip install guarddog        # or: uv tool install guarddog
guarddog pypi scan PACKAGE_NAME      # metadata + source heuristics
guarddog npm scan PACKAGE_NAME       # suspicious install scripts, exfil, recent-creation, typosquat
```
Any finding → BLOCK (do not install), report, find an alternative (max 3 tries).

### Step 2 — Known vulnerabilities in a package that IS real (CVE)

```bash
# OSV.dev — any ecosystem, no local tooling
curl -s -X POST https://api.osv.dev/v1/query -H "Content-Type: application/json" \
  -d '{"package":{"name":"LIBRARY_NAME","ecosystem":"npm"}}'
# Or locally on a lockfile: OSV-Scanner (Google, Apache 2.0)
osv-scanner --lockfile=<path>
```
Rules: last commit < 12 months, no unfixed CRITICAL CVE (else BLOCKED — find an alternative,
max 3 tries), check `.env.example` and `.gitignore`.

This is about your project's dependencies — distinct from auditing third-party skills/MCP
(R11, `external-skill-audit-tools.md`). All tools here are MIT/Apache — referenced, not bundled.

## Quality scan (mechanical cleanup — a core loop element)

Run on every Phase-3 iteration before commit. Not a one-off — a mandatory pre-commit gate.
Two stack-agnostic, MIT-licensed CLI tools cover it:

| Concern | Tool | License | Notes |
|---|---|---|---|
| Duplication (copy/paste) | **jscpd** | MIT | 150+ formats, token-based, fast |
| Cyclomatic complexity | **lizard** | MIT | 17 languages (cpp/java/c#/js/ts/py/ruby/php/swift/scala/go/rust/lua/…) — v1.23.0 verified |
| LOC + complexity estimate (+ Dart) | **scc** | MIT | Go, very fast; covers languages lizard doesn't |
| Circular dependencies | **madge** (JS/TS) · **import-linter** (Py) | MIT · BSD-2 | `madge --circular`; import-linter enforces contracts |
| Layer/boundary violations | **eslint-plugin-boundaries** (JS/TS) · **import-linter** (Py) | MIT · BSD-2 | enforce Clean-Arch dependency rule mechanically |
| Dead code (lava flow) | **knip** (JS/TS) · **vulture** (Py) | ISC · MIT | unused files, exports, functions |

These five categories together are the **structural-integrity gate** — they close *spaghetti code / big ball of mud* fully: duplication + complexity catch volume erosion, while cycles + boundary violations + dead code catch structural erosion. Per-stack commands live in your binding file.

```bash
# Duplication — fail above a threshold. Keep --threshold in sync with the ceiling below (dup > 10%).
# On Windows/MSYS, prefer running from inside handlers/ or use absolute paths; relative globs under
# `handlers/` can be ignored or under-reported depending on shell path resolution.
npx jscpd --threshold 10 --reporters console-full ./src
# Complexity — set the CCN threshold EXPLICITLY so it matches the ceiling below (CCN > 25).
# lizard's DEFAULT warning is CCN > 15 — if you rely on the default, the gate fires at 15, not 25.
# Pass -C 25 (and -T cyclomatic_complexity=25) so tool output and the stated ceiling agree.
lizard -C 25 ./src
# LOC + complexity estimate (broad language coverage, incl. Dart)
scc --by-file ./src
```

**Build your own quality score (replaces any single vendor score):** combine the numbers, e.g.
`score = 100 − (duplication% × k1) − (functions-over-CCN-threshold × k2)`. Because you set the
thresholds, the score is transparent and can't be gamed by loosening a hidden vendor metric.

**Anti-erosion / jscpd gotcha:** `Extract Method` into a shared helper is necessary but not sufficient.
If every wrapper is a 3-line copy-paste calling the shared helper identically, jscpd with realistic
`--min-lines 3 --min-tokens 10` settings still reports them as clones. After refactor, test the
resulting files, not only the original ones: if the new wrappers still trip the threshold, introduce
minimal per-file variation (unique constant, docstring, handler-id payload) BEFORE declaring the
anti-erosion gate passed.

**CRITICAL — the wrapper-clone check needs `--min-tokens 10`, NOT the default (~50).** Thin
delegates are short: a 4-9 line wrapper is well under 50 tokens, so the DEFAULT scan (and any
quick-start `jscpd --threshold 10` without `--min-tokens`) skips them entirely and reports a FALSE
0.00% — the gate goes green while identical wrappers remain. Verified 2026-07-19: the same treatment
handlers score 0.00% under `-k 50` but 66.17% (11 clones) under `-k 10`. So: for the anti-erosion /
wrapper-duplication check specifically, run `jscpd --threshold 10 --min-lines 3 --min-tokens 10`.
Reserve the higher default only for detecting large-block duplication, not thin delegates. A clean
result under `-k 50` does NOT prove the wrappers are unique.

**jscpd binary/flag portability (verify before scanning):** "jscpd" is two different tools — the
node CLI and the Rust port (`jscpd --version` → `cpd 5.x`). On the Rust port use `--format` (NOT
`--formats`, which errors) and beware the silent trap: if every file has fewer tokens than
`--min-tokens`, jscpd reports `Files analyzed: 0` / "No duplicates" / exit 0 — that is NOT a green
gate, it scanned nothing. Confirm `Files analyzed` is non-zero (`-r console-full`) before trusting
a clean result. Full flag map + zero-file causes → `references/jscpd-rust-port-gotchas.md`.

**Logged fix example (Extract Method to shared entry point):** when every handler contains the same `handle()` body plus `__main__` guard, first log the smell/technique explicitly, then refactor once into a shared `handle()` in the shared module, then make each handler a thin delegator. This avoids per-file drift and preserves the existing CLI contract.

Language-specific quality tools (native complexity/dead-code analyzers for your stack) go in
your binding file — see `bindings/flutter-example.md` for how to wire one in.

### Anti-erosion gate (long-horizon degradation — a HARD gate, not advice)

Why this matters: measured on iterative-extension benchmarks (SlopCodeBench, 2026), agent code
erodes structurally in ~77% of trajectories and bloats in ~75%, while checkpoints still pass —
i.e. tests stay green while quality rots with every turn. Explicit quality guidance cuts the
starting mess but does NOT stop the per-turn drift. So a soft "consider a review" is not enough;
the trend needs a real brake:

0. **Scope by Triage FIRST (cost control).** This whole gate is for Standard+ work. For Trivial/Low
   tasks (< ~10 iterations, few files) do NOT run tool scans per iteration — run the quality scan
   ONCE at the end. Running jscpd/lizard every step on a small job burns ~25x the tokens the code
   itself costs, for a trend that cannot even form on a few functions. Match the machinery to the
   blast radius.
1. **Record the cheap numbers each iteration** in PROGRESS.md (LOC, files touched). Full tool scans
   (`dup%`, max CCN via jscpd/lizard) run **every N iterations (default 5), not every iteration** —
   that is the trend sensor without the per-step tax.
2. **Two consecutive worsening scans → clean-code-review is MANDATORY before the next
   feature** (a backpressure gate, not optional). Fixing the trend is the task; you may not
   proceed while quality is monotonically degrading.
3. **Absolute ceilings** (run-contract params): the commit is BLOCKED until refactored — same status
   as a failing test — if ANY of these cross a hard cap: `dup%` > 10%, any function CCN > 25, **any
   NEW circular dependency** (madge/import-linter), **any layer-boundary violation** (eslint-boundaries/
   import-linter), or **new dead code** (knip/vulture). Structural caps are as blocking as duplication.
4. **Periodic refactor checkpoint:** every N iterations (default 10, aligned with the Autoresearch
   cadence) run a dedicated review pass even if no threshold tripped — this counteracts slow bloat
   that stays just under the per-iteration bar.

**Tool-absence rule (a gate that cannot run has NOT passed).** A structural check whose tool is
not installed (madge/import-linter/knip/vulture missing) is **INCONCLUSIVE**, never a silent pass
and never proof the gate "fired." Probe presence first (`madge --version`, `import-linter --version`,
etc.); if absent, either install it or mark that dimension INCONCLUSIVE in the report. Critically:
an empty or file-less arm directory is NOT evidence the gate blocked a commit — the model may
simply have written nothing. Only a real tool run (non-zero exit + the offending edge named) proves
a block. This rule exists because a QA run once claimed "keelwright blocked a circular import"
purely from an empty treatment dir while the tool was not even installed — a fabricated pass.

**When the brake fires, follow the name → technique discipline** (`refactoring-catalog.md`):
first NAME the smell (Long Method, Duplicated Code, Feature Envy, …), then apply ONE named
technique per commit (Extract Function, etc.) — no drive-by edits mixed in. Naming before fixing
is cheaper than re-inventing a cure and keeps each diff reviewable.

Reminder (reward-hacking guard): the fix is to improve the code, never to loosen the threshold or
delete the offending test. Thresholds are guard values — changing them to pass is forbidden.

### Harness Engineering (fix the system that produced the bug, not just the bug)

A core loop-coding practice: the loop is only as reliable as the *harness* around it — the tests,
linters, type-checks, security hooks, and CI gates that catch a mistake automatically. When an
error slips through, the durable fix is not just to patch the line; it is to **strengthen the
harness so that class of error cannot recur silently.** The better the obstacle course, the safer
autonomy is for a non-programmer who cannot spot the mistake by eye.

Before fixing an error by hand, ask: *"Can I improve a test / linter / hook so this class of bug
gets caught mechanically next time?"* Prefer that over a one-off manual patch.

- **Every fixed bug leaves a test behind.** Add a discriminating test that fails on the old
  behavior and passes on the new (`references/discriminating-tests.md`) — so a regression re-trips
  it automatically. A bug fixed without a test guarding it will come back.
- **Recurring mistake → tighten the machine, not your attention.** If the same footgun appears
  twice (a missing null-check pattern, an un-awaited promise, a forgotten auth check), encode it
  as a lint rule / Semgrep pattern / boundary contract, not as a mental note. Human vigilance does
  not scale across an autonomous loop; a rule does.
- **Prefer automatic gates over manual review** wherever a check *can* be mechanized — tests,
  type-checks, `jscpd`/`lizard` thresholds, `madge`/`import-linter` contracts, Gitleaks/Semgrep.
  Manual review is the fallback for what genuinely cannot be mechanized (business-logic judgment),
  not the first line of defense.
- **The harness is the real deliverable of a hardening iteration.** When a Stability/Autoresearch
  pass finds a repeated failure mode, the output is a stronger gate (new test, new rule, raised
  coverage), logged in `phoenix-log.md` — that is what stops the loop repeating the mistake.

This is why every ✅ in the risk glossary is *machine-enforced*: keelwright's answer to "how does a
non-coder stay safe in an autonomous loop?" is a strong harness, not more human eyeballing.


**Observed failure mode (2026-07-19 QA):** after Extract Method/Pull Up Method, agents self-reported “dup fixed” while `jscpd --threshold 10 --min-lines 3 --min-tokens 10` still showed 11 clones / 62.9% dup. The commit should have been blocked. Fix: after any refactor that targets duplication/complexity, rerun the exact quality scan command with the explicit threshold/min-lines/min-tokens. If the tool exits non-zero or dup% is still above the ceiling, continue refactoring. Do not mark the iteration complete until the scan is green under the ceiling.

**What the structural-integrity gate now covers (spaghetti / big ball of mud — FULLY):**
`dup%`/CCN catch *volume* erosion (duplication, bloat, complexity); **madge/import-linter** catch
circular dependencies; **eslint-plugin-boundaries/import-linter** enforce the layer dependency rule;
**knip/vulture** catch dead code (lava-flow accumulation). Together these are a hard machine gate on
structural degradation — not judgment, not "eyeball it."

**Verification status (honest):** the structural-integrity gate is *specified* but NOT yet
validated by a clean A/B on disk. An early QA run appeared to show it "blocking" a circular
dependency, but disk inspection proved that run fabricated the result (the treatment dir still
held live circular files, and madge/import-linter were not even installed). Do NOT claim this
gate is battle-tested until a run with the tools actually installed shows the control committing
a cycle and the treatment refusing it. Absence of files in an arm dir is NOT evidence the gate
fired — see the tool-absence rule above.

**Remaining honest limitation — *stylistic* consistency only:** what these tools do NOT catch is
low-level *style* drift — mixing async/await with promise chains, drifting naming or error-handling
conventions across iterations. There is no cheap machine detector for stylistic consistency. Partial
cover: the @architecture-critic in auto-review and the Pink Flag ("feels inconsistent") catch some by
judgment. So: the gate DOES mechanically prevent spaghetti/tangled-dependency/dead-code erosion; it
does NOT guarantee uniform style. Claim the former, not the latter.

## Auto-review (before commit)

`delegate_task` with parallel agents (each `context` carries the needed skill path):

| Agent | Checks | Block threshold |
|---|---|---|
| **security-auditor** | Gitleaks + Semgrep + language greps. Commands — `security-gates.md` Gate 1 + your binding | CRITICAL |
| **architecture-critic** | layer violations | HIGH |
| **business-logic-critic** | LOGIC: does auth grant extra rights on an edge condition? permission checks BEFORE the action? edge cases? idempotency? | CRITICAL |
| **performance-analyst** | N+1, heavy rebuilds | MEDIUM |

Plus locally: your typecheck/analyze + tests (commands — your binding).

**Block rules:**
- CRITICAL / HIGH → block commit, fix
- MEDIUM → log as tech debt, commit allowed
- Small change (1 file, <50 lines) → security + architecture + business-logic
- Critical path (auth/payments/user data/external API) → ALL agents + production checklist, no shortcuts

## Layers (decide the layer before creating a file)

A clean dependency rule keeps business logic independent of frameworks and IO. Outer → inner,
never the reverse. Details — the `clean-architecture` skill.

## Smell → stop

If something "feels wrong" in the code → `skill_view(name='clean-code-review')` before continuing.
Worsening quality numbers two iterations in a row is a stop signal.

## Dependency impact analysis

If you change a shared module (utils, types, shared, core):
1. Find who imports the changed file
2. Run ONLY the relevant tests (don't run everything)
3. Can't tell → run the full analyze + key tests

## Comments & logging discipline

Comments and logs are for the human who cannot read code — keep them meaningful, not noise.

**Comments:**
- NEVER comment the obvious (`// get data from the DB` above a DB call adds nothing).
- Use a doc-comment (`/** … */` / docstring) ONLY for (a) non-obvious BUSINESS rules —
  *why*, not *what* (e.g. "referral reward only pays after day 3, to deter self-referral fraud"),
  and (b) public functions used across modules.
- NEVER leave `// TODO` / `// FIXME` in a committed file — either do it now or file it as a task.

**Logging & error handling:**
- No bare `console.log` / `print` for business logic — it leaks into prod and says nothing.
- Wrap every DB (Supabase) or external-API call in try/catch (try/except).
- In the catch block use a tagged, actionable format:
  `console.error('[MODULE_NAME]: <action> failed. details:', error.message)` — so a non-coder
  reading the logs sees WHICH part broke and WHAT it was doing, not a raw stack trace.
