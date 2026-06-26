# Agentic COBOL — why we test InvestorClaw with a 250-prompt natural-language regression set

> Status: design + methodology rationale.
> Companion docs: `INSTALL_MODELS.md` (architecture), `RFC-v0.1.md` (v4.0
> specification), `harness/cobol/AGENTIC_COBOL_SPEC.md` in `argonautsystems/InvestorClaw`
> (canonical 250-NLQ prompt set + scorer), and the published long-form rationale at
> [**"All Our Tests Passed. The Agent Was Still Broken."**](https://techbroiler.net/all-our-tests-passed-the-agent-was-still-broken/)
> (Jason Perlow, techbroiler.net, 2026-04-29).

## TL;DR

The InvestorClaw cobol regression suite ("Agentic COBOL") is a **250-prompt
natural-language acceptance test** that validates whether the agent — across
four runtimes (OpenClaw, ZeroClaw, Hermes, Claude Code) — routes user
questions to the right engine commands AND whether the engine produces
narratives that satisfy a strict no-fabrication, no-rejection-marker verdict.

It's not a unit test. It's not an integration test. It's not an LLM-eval
benchmark. It's a routing acceptance test inspired by the 1959 COBOL
methodology: **write the spec in English, run it, score whether the system
did what was asked.**

We built it because **every other test layer was blind to the bug class
that breaks agent-skill products in production**: the silent misroute.
The agent looks fine in unit tests, in CI, in manual smoke checks. Then
a user types a natural-language question and the agent answers from training
data because it never invoked the right tool. No test framework that doesn't
include the LLM in its loop can catch that.

This doc explains the methodology, the empirical numbers, and how we use
it as the v4.x ship gate.

---

## 1. The bug class no other test catches

A concrete failure from v2.3.x:

> **User:** *"Any big mergers or acquisitions in the news today?"*
> **Engine:** has a working `news` command with passing unit tests, real
> M&A headlines fetched correctly when invoked.
> **Agent:** answers from training data without invoking anything.

The unit tests pass. The contract gate passes. The plugin manifest
validates. The function works perfectly when called. **The agent simply
doesn't choose to call it** because the description ("News headlines
fetcher") didn't surface "M&A" / "mergers" / "today" as routing signals.

This is the **silent-misroute** class:

- Not a code bug
- Not a logic bug
- Not a contract bug
- A *description-as-API* bug — the LLM-facing surface of the tool was
  undercommunicated

Every test layer that doesn't include the LLM in its loop is structurally
blind to it. Even LLM-eval frameworks (RAGAS, DeepEval, LangSmith) measure
**output quality**, which is orthogonal — an agent can produce a coherent,
factually-correct hallucination with zero tool calls and pass output-quality
metrics perfectly.

What we needed was a test layer that asks: **did the agent invoke the
right tool for the right prompt?**

---

## 2. Why we called it "Agentic COBOL"

In 1959, Grace Hopper's CODASYL committee built COBOL with one explicit goal:
**a domain expert (an accountant, a manager) should be able to read the
source code aloud and verify the program does what they expect.**

```cobol
ADD MONTHLY-PAY TO YEAR-TO-DATE-EARNINGS GIVING NEW-TOTAL.
IF NEW-TOTAL > BONUS-THRESHOLD THEN PERFORM CALCULATE-BONUS.
```

That's not pseudocode. That's executable COBOL. The acceptance test was
the readability of the source itself: the domain expert reads it,
verifies it does what was asked, and signs off.

The pattern is **English-as-interface, machine-as-router**. Domain expert
speaks; machine routes to the right operation; acceptance test is "read
the prompt aloud and check the system did what was asked."

That's *exactly* the problem we have with agent-skill products in 2026.
A user types natural language; the agent routes to the right tool; the
test is "did the agent route correctly?"

The substrate changed. COBOL's parser was deterministic — it parsed or
errored. LLMs are stochastic — same prompt, different routing across
runs, ~80-85% noise floor on a tuned surface. So compile-time guarantees
become **empirical sampling with multi-trial averaging and per-runtime
gates.** But the *methodology* transfers cleanly: write down the prompt,
write down what the system should do, run it, score whether it did.

We called the resulting test pattern **Agentic COBOL** because the
1959 discipline was right; we just had to remember why.

---

## 3. The corpus: 250 prompts, 7 categories

`harness/cobol/nlq-prompts.json` carries 250 natural-language queries
across 7 functional categories:

| Category | Example IDs | Sample prompts |
|---|---|---|
| Portfolio holdings + performance | n001-n040 | "Show my holdings", "What's my Sharpe ratio?", "Calculate my maximum drawdown" |
| News + sentiment | n041-n080 | "Any big mergers in the news today?", "What's the sentiment on AAPL?" |
| Bonds + fixed income | n081-n120 | "Show my bond duration", "What are my bond yields?" |
| Macro / market context | n121-n160 | "What's happening with commodities?", "Explain expected shortfall" |
| Concept / education | n161-n200 | "What's the SECURE Act?", "Explain scenario analysis" |
| Options + derivatives | n201-n230 | "Show my hedge effectiveness", "What's my recovery time?" |
| Setup / meta | n231-n250 | "List commands", "Ping", "What can you do?" |

Each prompt has a unique `id`, the `prompt_text`, an `expected_routes`
list (per-runtime: which engine command should fire), a `category`
classification, and (for the v13 v4.x corpus) a `verdict_class`
attribute that constrains how the response is scored.

Per-runtime route mappings exist because the same product exposes a
different tool surface in each runtime — OpenClaw might call
`portfolio_market section=news topic=merger`, while Claude Code calls
`/investorclaw:ask` with the same prompt.

---

## 3a. What an Agentic COBOL spec actually looks like

The methodology is named after COBOL because the *visual structure* of the
spec maps onto COBOL's two-division program layout. COBOL programs were
deliberately written so a non-programmer (an accountant, a payroll clerk)
could read them aloud and verify behavior:

```cobol
       IDENTIFICATION DIVISION.
       PROGRAM-ID. PAYROLL-BONUS.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  EMPLOYEE-RECORD.
           05  EMP-NAME              PIC X(30).
           05  MONTHLY-PAY           PIC 9(7)V99.
           05  YEAR-TO-DATE-EARNINGS PIC 9(9)V99.
       01  CONSTANTS.
           05  BONUS-THRESHOLD       PIC 9(7)V99 VALUE 100000.00.

       PROCEDURE DIVISION.
       MAIN-PROCESS.
           READ EMPLOYEE-FILE INTO EMPLOYEE-RECORD
               AT END GO TO END-PROGRAM.
           ADD MONTHLY-PAY TO YEAR-TO-DATE-EARNINGS
               GIVING NEW-TOTAL.
           IF NEW-TOTAL > BONUS-THRESHOLD THEN
               PERFORM CALCULATE-BONUS.
           GO TO MAIN-PROCESS.
       END-PROGRAM.
           CLOSE EMPLOYEE-FILE.
           STOP RUN.
```

A 1959 accountant could read that aloud — "READ employee record. ADD monthly
pay to year-to-date earnings. IF new total greater than bonus threshold,
PERFORM calculate bonus." — and verify the program represented what payroll
actually wanted. The English-prose surface *was* the acceptance test.

Agentic COBOL's spec format is the same shape: a **DATA DIVISION** of
natural-language prompts users actually say, paired with a **PROCEDURE
DIVISION** of expected tool routes the agent must invoke. Read aloud, it
should be possible for a domain expert (a portfolio manager, a finance
analyst) to verify both.

Here's an actual slice of `harness/cobol/nlq-prompts.json` rendered the same
way COBOL renders DATA + PROCEDURE divisions:

```cobol
      *  ───────────────  AGENTIC COBOL DIVISION  ───────────────
      *  Spec: harness/cobol/nlq-prompts.json
      *  Domain: portfolio analysis (InvestorClaw)
      *  Acceptance: read aloud; verify the routes match the prompts.

       DATA DIVISION.
       NLQ-CORPUS SECTION.

       01  P01-HOLDINGS-1.
           05  PROMPT-TEXT     "What is in my portfolio right now?".
           05  INTENT          "portfolio-snapshot".
           05  CATEGORY        "holdings".

       01  P03-PERFORMANCE-1.
           05  PROMPT-TEXT     "How has my portfolio performed this year?".
           05  INTENT          "performance-check".
           05  CATEGORY        "performance".

       01  P04-PERFORMANCE-2.
           05  PROMPT-TEXT     "What is my Sharpe ratio and max drawdown?".
           05  INTENT          "performance-check".
           05  CATEGORY        "performance".

       01  P16-NEWS-MERGER.
           05  PROMPT-TEXT     "Any big mergers or acquisitions in the
                                news today?".
           05  INTENT          "news-merger".
           05  CATEGORY        "news".

       01  P22-BONDS-DURATION.
           05  PROMPT-TEXT     "Show my bond duration.".
           05  INTENT          "bonds-duration".
           05  CATEGORY        "bonds".


       PROCEDURE DIVISION.
       AGENT-ROUTING SECTION.

       WHEN PROMPT MATCHES P01-HOLDINGS-1
           PERFORM PORTFOLIO-VIEW SECTION="holdings".
           ON CLAUDE-CODE INVOKE "/investorclaw:ask".
           ON OPENCLAW    INVOKE "portfolio_view section=holdings".
           ON ZEROCLAW    INVOKE "portfolio_view section=holdings".
           ON HERMES      INVOKE "portfolio_view section=holdings".

       WHEN PROMPT MATCHES P03-PERFORMANCE-1
           PERFORM PORTFOLIO-VIEW SECTION="performance".

       WHEN PROMPT MATCHES P04-PERFORMANCE-2
           PERFORM PORTFOLIO-VIEW SECTION="performance".

       WHEN PROMPT MATCHES P16-NEWS-MERGER
           PERFORM PORTFOLIO-MARKET SECTION="news" TOPIC="merger".

       WHEN PROMPT MATCHES P22-BONDS-DURATION
           PERFORM PORTFOLIO-VIEW SECTION="bonds" TOPIC="duration".

       VERDICT SECTION.
       ACCEPT WHEN
           IC-RESULT-PRESENT IS TRUE
           AND HMAC-PRESENT IS TRUE
           AND NARRATIVE-CHARS NOT LESS THAN 200
           AND BODY-CHARS NOT LESS THAN 100
           AND REJECTION-MARKERS COUNT EQUALS 0.
       REJECT WHEN
           NARRATIVE CONTAINS "I don't have data on that"
           OR NARRATIVE CONTAINS "Section did not run"
           OR NARRATIVE STARTS-WITH "ic-engine completed your portfolio
                                     analysis with [".

       END PROGRAM.
```

That's not actually executable COBOL — it's a *visualization* of the
acceptance spec in a form a 1959 COBOL programmer would recognize. The
real format is JSON (machine-friendly) but the conceptual shape is the
same:

```json
{
  "prompts": [
    {
      "id": "p01-holdings-1",
      "intent": "portfolio-snapshot",
      "prompt": "What is in my portfolio right now?",
      "expected_routes": {
        "investorclaw":   ["portfolio_view section=holdings", "holdings"],
        "investorclaude": ["ask"]
      }
    },
    {
      "id": "p04-performance-2",
      "intent": "performance-check",
      "prompt": "What is my Sharpe ratio and max drawdown?",
      "expected_routes": {
        "investorclaw":   ["portfolio_view section=performance", "performance"],
        "investorclaude": ["ask"]
      }
    },
    {
      "id": "p16-news-merger",
      "intent": "news-merger",
      "prompt": "Any big mergers or acquisitions in the news today?",
      "expected_routes": {
        "investorclaw":   ["portfolio_market section=news topic=merger", "market"],
        "investorclaude": ["portfolio-view news", "portfolio-market news"]
      }
    }
  ]
}
```

### Why this isn't Gherkin / BDD

A natural objection: "this is just BDD." Gherkin (`Given/When/Then`) and
Cucumber `.feature` files are clearly in the same lineage. The differences
are real and worth being explicit about:

| Property | Gherkin / BDD | Agentic COBOL |
|---|---|---|
| Test subject | Application code (deterministic) | Agent + LLM + tools (stochastic) |
| Test layer | Behavior of a function or workflow | **Tool selection from natural language** |
| Per-trial outcome | Same input → same output (asserted) | Same input → distribution of outputs (sampled) |
| Pass criterion | Boolean per scenario | Threshold % per prompt × runtime × trial |
| Failure mode caught | Logic bug in the function | **Description-as-API bug — the LLM never invoked the function** |
| Re-run cost | Free (deterministic) | Real LLM tokens (~$0.02-$0.10 per prompt at MiniMax-M2 cost) |
| What "scoring" means | Compare expected output to actual output | Compare expected tool invocations to detected tool invocations in the recorded transcript |

Gherkin assumes the test subject is parser-stable. COBOL's parser was also
parser-stable — but COBOL's *user* (the accountant reading the program)
was the human-language layer. The acceptance test was "can the human read
this and verify it." Agentic COBOL has the same shape but the human-language
layer has moved into the runtime: the LLM is now reading the prompt and
deciding what to do. The acceptance test is "can the prompt + expected
routes spec be read aloud by a domain expert and verified," then "did the
agent route correctly when run."

You can absolutely emit Gherkin from the JSON corpus if your team uses
Cucumber tooling — `harness/cobol/cobol_barrage_cross_runtime.py` will
emit a `.feature` view on `--format gherkin`. The methodology survives
the format choice. The substance is in the prompt-route pairs, not the
syntax.

---

## 4. The verdict (what counts as PASS)

The v4.x verdict is **strict** — significantly stricter than v2.x — and
this strictness is the engine of progress. A response PASSes only if
ALL of these hold:

| Check | What it validates |
|---|---|
| `exit_code == 0` | The engine subprocess didn't crash |
| `has_ic_result == true` | The MCP envelope carries `ic_result.{hmac, run_id, command, engine_version}` |
| `has_hmac == true` | The narrative footer carries the envelope HMAC for audit-trail integrity |
| `narrative_chars >= 200` | The narrator produced a real response, not a stub |
| `body_chars >= 100` (after stripping markers) | The response has substance after we strip catalog headers, refresh-pings, footers |
| **Zero rejection_marker hits** | The narrator did NOT emit any of: `"I don't have data on that"`, `"Section did not run"`, `"ic-engine completed your portfolio analysis with [...]"` (catalog-blurb starter), `"I cannot answer that without making up numbers"` (only if no real numeric content precedes it) |

The rejection_marker check is the load-bearing piece. In v2.x the verdict
only checked envelope presence + exit_code, which let the engine pass
everything as long as it didn't crash — even when it returned the heuristic
catalog blurb instead of routing to a real command. **v4.x rejects the
catalog blurb.** The catalog is a graceful fallback, not a real answer; if
the cobol verdict accepts it, every subsequent fix becomes invisible.

The verdict has been tightened TWICE during v4.x development:

- **2026-05-02**: original cobol-verdict tightening rejected catalog blurbs
  + refusal markers.
- **2026-05-03**: approximation-aware fabrication validator (decimal ↔
  percentage conversions count as the same number) + honest-partial-answer
  carve-out (≥1000 char body + numeric content before marker is allowed,
  e.g. when the narrator says "and FYI I don't have ESG data" after a real
  governance-pillar answer).

---

## 5. The empirical narrative

The v2.x baseline was the proof-of-concept. The v4.x cycle is the rebuild.

### v2.3.x → v2.5.x (per-runtime install paths, tightening descriptions)

- **v2.3.4 (15-prompt baseline):** 9/15 = 60% on Claude Code. All eight
  failures were silent misroutes.
- **v2.3.5 (description tuning):** 12/15 = 80%.
- **v2.3.6 (narrowed `ic-setup`):** 11/15 = 73%. Three new regressions in
  commands whose descriptions weren't even touched. **Discovery: LLM
  routing has a global attention layer; tightening one description shifts
  attention across the whole catalog.**
- **v2.3.7 - v2.4.0 (rebalancing + consolidating 27 commands → 9):** 19/30
  = 63% on the new 30-prompt corpus.
- **v2.5.0 (single-engine adapter consolidation):** Claude Code 24/30 =
  80%.
- **v2.5.1 (slash surface collapsed to `ask` + `refresh`):** Routing tight,
  but the *measurement* was wrong (see "When the test fixture lies" below).
- **v2.5.2 published release:** Claude Code 30/30 = 100% (rescored under
  fixed scorer). Cross-runtime: OpenClaw 26/30 (86%), Hermes 23/30 (76%).

### When the test fixture lies (v2.5.1 → v2.5.2)

The v2.5.1 → v2.5.2 jump from "1/30" to "30/30" *on the same recorded
agent runs* is the most uncomfortable lesson of the v2.x cycle.

The harness records every prompt's full agent transcript as JSONL. The
v2.5.1 scorer parsed `claude -p --output-format=stream-json` events
looking for tool invocations on `Bash` or directly-named slash commands.
It missed the actual shape Claude Code now ships: plugin slash commands
surface as a `Skill` tool call with `input.skill = "investorclaw:ask"`.
The slash name lives in the input, not the tool name.

The agent had been routing perfectly. The scorer hadn't.

Rescoring the captured stream-json with a fixed `Skill`-aware extractor
turned 1/30 (fail-the-publish-bar) into 30/30 (sail past). Same agent.
Same prompts. Same model. Different lens.

The discipline that protects you here: **always commit the raw artifact**.
The `tool_invocations` field in the JSONL is the truth; `detected` is the
interpretation. When you can prove the interpretation was wrong without
re-running the agent, you have a shippable fix; when you have to re-run,
you've already burned a day on provider quotas.

**The test pyramid for agentic systems needs a layer the unit-test era
never had: scorer correctness.** Treat the scorer like production code.
Test it against recorded transcripts. Version its detection logic. Make
it auditable. We assert this in CI: a 30-row regression that runs the
buggy v2.5.1 scorer alongside the fixed v2.5.2 scorer against the recorded
JSONL — old logic must reproduce 1/30, new logic must hit 30/30. Both
invariants asserted on every PR.

### v4.0 → v4.1.17 (dockerized-skill, expanded to 250 prompts, tightened verdict)

When v4.x rebuilt the architecture (one engine container, MCP-HTTP, agents
as pure clients — see `INSTALL_MODELS.md`), we expanded the corpus from
30 to 250 prompts and tightened the verdict. The first run on the rebuilt
stack:

- **v4.0 (rescored under tightened verdict):** 1/250 PASS. The old "fake
  pass" rate collapsed under real scrutiny.

Cobol determinism work over the next three weeks closed engine gaps one
at a time. Each ship landed against the same 250-prompt corpus:

- **v4.1.0 → v4.1.6:** Bridge fixes (litellm narrator restoration,
  envelope compaction, P1 timeout 60s→600s, Massive adapter rename).
  Pass rate climbs to ~18/21 in partial runs.
- **v4.1.7 → v4.1.13:** Provider chain hardening. yfinance moved LAST in
  every routing chain (Yahoo 429s under barrage load), Marketaux + Frankfurter
  + Treasury Fiscal Data added. Mode-aware narrator (portfolio-strict /
  concept / market / setup deflection). 25/30 → 29/30 cobol.
- **v4.1.14:** First full 250-NLQ run on baked image: **144/250 = 57.6%**.
  Most failures were transport_errors (96/106) — MCP server timeouts under
  prolonged barrage load. Subprocess-reap fix landed.
- **v4.1.15:** SPY benchmark via PriceProvider (the headline cascade fix —
  `fetch_benchmark_returns` was using direct `yf.Ticker()` which throttled
  to empty, invalidating `calculate_beta` for every symbol, cascading to
  0/215 valid_symbols). Per-symbol Sortino + max_drawdown wired.
  **245/250 = 98%**. The five remaining FAILs were stale (already fixed
  by hot-patches that landed after the prompts ran).
- **v4.1.16:** Baked the hot-patches in cleanly. Refocused regression on
  the v4.1.15 5 FAILs: **5/5 PASS**. Full v4-250 on baked: 245/250 = 98%
  with a different 5-prompt FAIL set (classifier edge cases on " my X "
  ownership signal forcing portfolio-strict for advice-style questions).
- **v4.1.17:** Classifier fix (CONCEPT-STEM + NA-METRIC overrides ahead of
  OWNERSHIP) baked in. Pass rate 245-249/250 = 98-99% on baked images.

The pattern is consistent: **each ship is gated by the same 250 prompts,
the same strict verdict, the same multi-trial cobol harness.** Visible
progress in pass-rate IS the progress. The test isn't just a measurement;
it's the spec the engineering work targets.

---

## 6. What the strict verdict catches

The cobol verdict is now strict enough to differentiate between SIX
distinct failure modes that all "looked the same" under v2.x:

| Failure mode | What the verdict sees | Example |
|---|---|---|
| **Silent misroute** | Engine never invoked, narrative is hallucinated training-data | Pre-v4 description-tuning era |
| **Catalog blurb fallback** | Engine returned heuristic blurb instead of routing | "ic-engine completed your portfolio analysis with [...]" marker |
| **Provider data starvation** | Routed correctly but downstream data fetch returned empty | "I don't have data on that" rejection |
| **Section-skip** | Engine ran but a stage failed; narrator hallucinated portfolio context | "Section did not run" marker |
| **Narrator runaway** | LLM goes pathological under load, generates 200k+ chars | combined "Section did not run" + catalog-blurb starter |
| **Classifier edge case** | Mode classifier routes incorrectly (e.g. " my " forces portfolio-strict for an advice question) | rejection_marker on a prompt that should have been concept-mode |

Each of these requires a different fix. Without the strict verdict, they
all look like generic FAILs and you can't tell which lever to pull.

The **classifier edge case** family is the most subtle — it's the kind
of bug that LLM-routing systems quietly accumulate as the prompt corpus
grows. We've now caught and fixed two waves: the original mode-aware
narrator (v4.1.13) and the CONCEPT-STEM/NA-METRIC overrides (v4.1.17).
Both fixes were direct consequences of cobol regression FAILs that
wouldn't have surfaced any other way.

---

## 7. The cost / value trade

**Cost of running the harness:** each cobol prompt is a real LLM call
(~30-180 seconds, real provider spend, non-deterministic). For a
250-prompt × 1-trial harness on the baked image, that's ~5 hours of
wall-clock and ~$5-10 of provider tokens (Together MiniMax-M2 at default
cost). Multi-trial runs multiply linearly.

**Cost of NOT running it:** silent misroutes. Catalog-blurb fallbacks.
Hallucinated portfolio numbers presented to users with full HMAC signatures.
The bug class that ships to production and gets discovered by a finance
journalist who took a screenshot.

For a portfolio-analysis product where the cost of a false answer is
measured in users' actual money, the trade is straightforward: real
provider spend now vs. real user-facing breakage later. The harness is
non-negotiable.

The 250-NLQ corpus + scorer are open-source under Apache 2.0 in
`argonautsystems/InvestorClaw/harness/cobol/`. Anyone shipping an
agent-skill product can adopt the methodology — the prompt set is
finance-specific but the harness, scorer, and verdict architecture are
generalizable.

---

## 8. Who should use Agentic COBOL

Anyone whose product is "the agent picks the right tool from natural
language":

- Claude Code plugin authors (`.claude-plugin/plugin.json` skills)
- OpenClaw / ZeroClaw / Hermes plugin builders
- MCP server developers (any transport)
- Cursor / Windsurf / Codex CLI extensions
- Future agent ecosystems we don't have names for yet

Adoption checklist:

1. Write 30-50 natural-language prompts that exercise your product's full
   surface area.
2. For each prompt, write down which tool/command should fire.
3. Build a runner that captures the **raw agent transcript** (stream-json
   if your runtime exposes it; full conversation log otherwise).
4. Build a scorer that's auditable against recorded transcripts. Version
   it. Test it.
5. Define a strict verdict that rejects fallback responses, catalog blurbs,
   and rejection markers.
6. Run it on every release. Treat the pass-rate as the ship gate.

The harness in this repo is the reference implementation. The long-form
rationale is published as
[**"All Our Tests Passed. The Agent Was Still Broken."**](https://techbroiler.net/all-our-tests-passed-the-agent-was-still-broken/)
(techbroiler.net, 2026-04-29) — the canonical narrative explanation,
recommended reading before adopting Agentic COBOL for your own product.

---

## 9. References

- `argonautsystems/InvestorClaw/harness/cobol/AGENTIC_COBOL_SPEC.md` —
  canonical spec
- `argonautsystems/InvestorClaw/harness/cobol/nlq-prompts.json` — 250-NLQ
  corpus (Apache 2.0)
- `argonautsystems/InvestorClaw/harness/cobol/cobol_barrage_cross_runtime.py` —
  multi-runtime harness runner
- `argonautsystems/InvestorClaw/harness/cobol/rescore_cross_runtime.py` —
  scorer (audit-friendly, runs against recorded JSONL)
- [**"All Our Tests Passed. The Agent Was Still Broken."**](https://techbroiler.net/all-our-tests-passed-the-agent-was-still-broken/) —
  published long-form rationale (techbroiler.net, Jason Perlow, 2026-04-29)
- `INSTALL_MODELS.md` (this repo) — architectural context for why two
  install models exist
- `RFC-v0.1.md` (this repo) — v4.0 specification including the cobol
  ship-gate definition

> *The 60-year-old language was right; we just had to remember why.*
