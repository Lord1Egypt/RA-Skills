# Skill Eval — kano-model-strategist

**Date:** 2026-06-15
**Method:** Path B (parallel producer + baseline, subagent_type: general)
**Eval prompt:** Triaging 7 features for a B2B SaaS legal contract tool v1
launch, with CEO pinning 2 politically-loaded features, 6-week capacity
constraint, no user research, and SOC2 Type II as a market-access gate.

## Setup

- **Producer (with-skill)**: loaded
  `C:\Users\Monika\_meta-space\.agents\skills\kano-model-strategist\SKILL.md`
  and all 3 references before responding
- **Baseline (no-skill)**: same task, no skill loaded, used own PM/UX
  knowledge
- **Eval prompt identical for both**

Both outputs are saved to `with-skill.md` and `baseline.md` in this
directory.

## 5-point comparison

| # | Rubric | With-skill | Baseline | Winner |
|---|---|---|---|---|
| 1 | Procedural adherence | Loaded all 3 references, verified input gate, ran Priority Ladder, rot check, failure-handling table, output contract ≤15 rows. Documented in "Procedure used" section. | Used 9 named heuristics in "Reasoning used" section. Solid PM thinking, no formal procedure. | Slight with-skill (explicit failure-handling check) |
| 2 | Output contract compliance | 5/5 elements present in correct order: verdict table, MDP pick, kills (with eng-week estimates), Must-be hardening plan, open questions. | 4/5 — has table, MDP, kills, hardening. Open questions are scattered in "Reasoning used" / "What I'm not doing" but not as a dedicated section. | With-skill |
| 3 | Edge case handling | CEO pushback section with specific scripts ("What to say to the CEO"). SOC2 explicit split (badge vs. cert as "market-access gate vs. feature"). #6 split into "presence+comments" vs. "CRDT" with reverse-test justification. | Same conclusions reached but more diffuse. CEO pushback in "With the CEO" subsection. SOC2 split is there but not labeled as a Kano vs. non-Kano category distinction. #6 split is there but not framed as a reverse-test application. | Slight with-skill (more disciplined) |
| 4 | Hallucination rate | Low. All eng-week estimates are explicitly "rough estimates from first principles" and labeled. Yjs/Automerge/Liveblocks mentioned correctly. No fake sources. | Low. Ironclad/ContractWorks/Evisort mentioned correctly. Geoffrey Moore / Marty Cagan referenced accurately. | Tie |
| 5 | Justification quality | Strong. Concrete segment reasoning ("work in Word, Outlook, and a DMS"). **7 explicit skill gaps documented in dedicated section** — this is gold for the skill author. | Strong. Hypotheses H1/H2/H3 for MDP validation. "What I'm explicitly NOT doing" section. | Tie (both senior-level) |

**Score: With-skill wins 2 (output contract, procedural adherence), baseline
wins 0, ties 3.**

## Verdict

The skill is **not worse than baseline**, and is **measurably better in two
specific dimensions**: output contract compliance and procedural discipline.
This is the right shape for a skill — it should not be making the model
smarter than it already is, it should be **making the output more
predictable, auditable, and reusable.**

The baseline output is genuinely good. The skill output is not dramatically
more insightful, but it is:
- More structured (5/5 output elements, in the right order)
- More auditable (Procedure used section documents exactly what was done)
- More honest about its own limits (7-item Skill gaps section)
- More consistent across users (a junior PM running the skill would get a
  similar shape; a junior PM running with no skill would not)

## Actionable improvements for skill v1.1

Based on the 7 skill gaps the producer identified, prioritized by
value-to-effort:

1. **T-shirt sizing rubric** (HIGH VALUE, LOW EFFORT). Add a 1-line estimate
   per Kano category (S = ≤1 week, M = 1-3, L = 3-6, XL = 6+) to
   `SKILL.md` output contract. Lets users fill in eng-weeks without
   hand-waving.
2. **CEO pushback scripts** (HIGH VALUE, MEDIUM EFFORT). Add a small
   reference file with 3-4 worked conversation scripts for the "Indifferent
   but CEO-pinned" scenario. Biggest emotional/political gap.
3. **Market-access condition vs. user-facing feature** (MEDIUM VALUE, LOW
   EFFORT). Add one paragraph to `kano-classification.md` clarifying that
   SOC2 / compliance certs are NOT user-facing features and should not be
   classified via Kano. They go in a separate "prerequisites" section.
4. **Net-new / no-research pre-Step** (MEDIUM VALUE, MEDIUM EFFORT). Add
   to `SKILL.md` Procedure a Step 0: "If no user research exists, pick the
   smallest defensible segment assumption, flag all classifications as
   Medium-or-Low, and commit to cheapest validation (5 user calls) before
   spec lock."
5. **Kano under hard deadline** (MEDIUM VALUE, MEDIUM EFFORT). Addendum
   noting that under a fixed-capacity constraint, the Priority Ladder may
   force demoting a Must-be to DEFER (partial scope) or Performance to
   "good enough."
6. **Sub-feature decomposition guidance** (LOW VALUE, LOW EFFORT). One
   sentence in the classification reference: when a feature spans multiple
   categories, decompose it into the smallest sub-features that map
   cleanly.
7. **PM pushback scenarios** in failure-handling table (LOW VALUE, LOW
   EFFORT). Add row: "User is a PM being asked to push back on the CEO" →
   use the CEO pushback scripts from #2.

## Recommendation

**Keep the skill as v1.0.** It works, it's lint-clean, it's published, and
it demonstrably helps. Improvements 1-3 are easy enough to do in a v1.1
once the user has a few real backlog runs to confirm the gaps are
universal and not edge cases specific to this one eval.
