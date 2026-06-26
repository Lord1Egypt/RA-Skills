# Mythos in Action — Annotated Examples

Five examples covering all three modes plus the degenerate-Coda fast path. Each example shows what the user sees AND what's happening behind the scenes.

---

## Example 1 — Silent Mode (default for complexity 2-3)

**User:** `/mythos Should we use a monorepo or polyrepo for our growing engineering team of 15 people?`

### What the user sees

```
## Answer

Start with a monorepo. At 15 people, the coordination benefits of atomic cross-service
changes outweigh the CI complexity. The monorepo's transparency (one PR shows the full
blast radius) is more valuable than polyrepo's isolation. Revisit when one of these
happens: CI times consistently exceed 10 minutes, the team grows past 30, or you have a
service that genuinely needs independent versioning and release cycles (e.g., a public
API with external consumers).

The deeper insight: this is not a choice between two repo layouts; it's a choice between
two incentive structures. Monorepo makes cross-service changes easy (and surfaces blast
radius). Polyrepo makes cross-service changes painful (and hides it). Pick the
incentives you want — they will shape your architecture more than your architecture
shapes them.

---
*Depth: 3 latent passes. Mode: silent. Lens path: Clarify → Deepen → Challenge.*
*Load-bearing assumptions: team is co-located or has low-process async communication;
services share a common tech stack; no regulatory requirement for code isolation between
services.*
```

### What happened behind the scenes

The Recurrent Block ran in internal/extended-thinking reasoning. Three lens applications:

- **Clarify:** decomposed "monorepo vs polyrepo" into three orthogonal sub-decisions (storage, build, deploy)
- **Deepen:** identified the real driver — cost of cross-service changes, not repo count
- **Challenge:** surfaced the "incentive shaping" insight — neither layout is neutral

No visible round was emitted. The lens path is named in the footer as a one-line trajectory hint, so the user knows roughly what depth happened without the audit trail. If they want the audit trail, they re-run with `/mythos trace ...`.

> **What this demonstrates:** the most common mythos invocation. Default mode produces just the answer with a faint trace. Token cost is comparable to a thoughtful single response — the structure is in the reasoning, not in the output format.

---

## Example 2 — Trace Mode (opt-in via `trace`)

**User:** `/mythos trace Our startup has 3 months of runway and our product has good reviews but declining retention. Pivot or stay?`

### What the user sees

```
## Prelude
**Q:** With 3 months of runway, good reviews, and declining retention — should we pivot
the product or double down on retention fixes? | **Not asking:** how to extend runway,
fundraise, or find specific retention bugs.
**Complexity:** 4/5 → trace mode (forced via keyword), 5 rounds | **Drivers:** Trade-offs
(pivot vs stay), Hidden assumptions (the "good reviews" framing), Multi-hop (decision +
execution timing).
**Budget:** Clarify ×1 → Tradeoff-Map ×2 → Scar-Tissue ×1 → Synthesize ×1
**Success:** A decision framework with checkpoints — not a yes/no.

### Round 1: Clarify
**New insight:** "Good reviews + declining retention" is the most common pattern of
product-market fit being narrow rather than absent. The reviewers loved one thing; the
churners didn't return because what they loved didn't expand into a habit. The question
isn't "is the product good" — it's "is the lovable thing big enough to build a business on."
**What changed:** Reframed from binary pivot/stay to "what specifically retains, and is it
generalizable."
**Convergence:** evolving

### Round 2: Tradeoff-Map
**Insight chain:** R1: real question is whether the lovable thing generalizes
**New insight:** Pivot cost = burning ~6 weeks of remaining runway on something unproven
+ disrupting whatever current users you do have. Stay cost = 3 months of further
retention engineering with no guarantee of finding the next lovable thing in time. The
asymmetry depends on whether you have a *specific* pivot hypothesis or just "we'll try
something." Specific pivot hypothesis = pivot may be cheaper than continuing. Vague pivot
hypothesis = stay is cheaper.
**What changed:** Made the trade-off concrete — pivot cost is bounded only if the pivot
target is specific.
**Convergence:** evolving

### Round 3: Tradeoff-Map (2nd round, addresses Trade-offs driver ×2)
**Insight chain:** R1: lovable-thing generalizability → R2: pivot cost is bounded only
with specific target
**New insight:** There's a third option that beats both. "Narrow the product to its
lovable core, raise a small bridge round on that as proof, and grow from there." It's
not a pivot (no new market) and not a stay (current product changes). The Pareto frontier
isn't pivot-vs-stay — it's pivot-vs-stay-vs-narrow. With 3 months runway, narrow may be
the only option that's both fundable and executable.
**What changed:** Surfaced a third, dominated alternative neither pivot nor stay had
considered.
**Convergence:** breakthrough

### Round 4: Scar-Tissue
**Insight chain:** R1: lovable-thing generalizability → R2: pivot cost asymmetry → R3: narrow as third option
**New insight:** Founders who pivoted with 3 months of runway and a vague hypothesis went
broke ~80% of the time within 9 months. Founders who narrowed with the same runway and
shipped a tighter v2 in 6 weeks raised follow-on capital ~50% of the time. Concrete
pattern: when capital is tight, "less product done well" beats "different product
unproven."
**What changed:** The narrow option isn't just theoretically attractive — pattern-matched
to actual outcomes.
**Convergence:** evolving

### Round 5: Synthesize
**Insight chain:** R1: generalizability → R2: pivot asymmetry → R3: narrow as third option → R4: pattern-match favors narrow under tight runway
**New insight:** The decision tree: (a) Do you have a specific pivot hypothesis you can
ship in 6 weeks? If yes → pivot. (b) Can you identify the lovable core of current product
and ship a tightened v2 in 6 weeks? If yes → narrow. (c) Neither? → wind down before
runway hits 0 and you're forced into a fire sale.
**What changed:** Produced a 3-branch decision tree that includes the breakthrough from R3.
**Convergence:** stable

## Answer

Don't think of it as pivot vs stay — there's a third option that probably wins.

**Decision tree (in order — the first "yes" wins):**

1. **Do you have a specific pivot hypothesis you can ship in 6 weeks** — based on
   evidence, not vibes? E.g., "users keep asking for X feature that lives in a different
   product category." If yes → pivot.

2. **Can you identify the specific lovable core of your current product** (look at the
   reviews — what 2-3 things keep getting praised?) **and ship a tightened v2 around
   exactly that core in 6 weeks**, dropping everything else? If yes → narrow. Then raise
   a bridge on the focused product.

3. **Neither?** Wind down now while you still have runway to do it cleanly. Don't burn the
   remaining 3 months hoping clarity arrives — clarity costs more than 3 months when
   you're under stress.

The pattern: under tight runway, "less product done well" beats "different product
unproven" by a wide margin. Pivots only work when the new direction is genuinely cheaper
to validate than the current one — and that's rare.

---
*Depth: 5 rounds, converged at round 5. Mode: trace.*
*Load-bearing assumptions: "good reviews" reflect real signal, not just polite users —
verify by looking at NPS-like behavior (re-orders, referrals); 3 months runway is hard
(not soft via revenue); founders have legal/operational ability to wind down without
catastrophic clawback obligations.*
```

> **What this demonstrates:** trace mode preserves the full audit trail. Round 3 had a `breakthrough` (the "narrow" third option) — this is exactly when trace mode earns its cost. In silent mode, the user would have seen the third option appear in the answer without seeing how it was discovered.

---

## Example 3 — Agent Mode (default for complexity 4-5, parallel fan-out)

**User:** `/mythos deep Is it ethical to train AI on public web data without consent?`

### What the user sees

```
## Prelude
**Q:** Is training AI models on publicly-accessible web content (without explicit
consent from the content creators) ethically defensible? | **Not asking:** is it legal,
is it strategically wise, is it good for AI capability.
**Complexity:** 5/5 → agent mode (default), 4 parallel subagents | **Drivers:** Hidden
assumptions (the "consent" framing presumes a consent-based property model), Trade-offs
(creator autonomy vs collective benefit), Multi-hop (rights → harm → remedy → policy).
**Lenses dispatched in parallel:** Clarify, Steelman-Pro, Steelman-Anti, Tradeoff-Map.
Synthesize is the merge phase by the orchestrator.

[Dispatching 4 parallel subagents...]

### Subagent A — Clarify
**Independent finding:** "Consent" in this question conflates three different things
that have different ethical statuses: (1) consent at the moment of publication (was the
content public-facing), (2) consent to derived works that could not be foreseen at
publication time (training on it), and (3) consent at the moment of use (did the
creator know their work was actively being incorporated). Most arguments assume one of
these and ignore the others.
**Confidence:** high
**Tension flag:** Steelman-Pro and Steelman-Anti will both have to specify which form of
consent they're defending or attacking.

### Subagent B — Steelman-Pro (training is ethically defensible)
**Independent finding:** Public web content was published into a commons that has always
been read, indexed, summarized, quoted, and learned-from by humans without per-use
consent. AI training is structurally analogous — a learning process, not a copying
process. The "consent" demand is a category error: we don't ask for consent to learn from
a book we bought; we ask for consent to copy or republish it. AI training is closer to
the former. The ethical principle "you may learn from what you can read" has 2000+ years
of precedent.
**Confidence:** medium-high (depends on whether AI training is actually structurally
analogous to human learning — that's a contested empirical claim).
**Tension flag:** Anti will likely contest the "structurally analogous to human learning"
claim.

### Subagent C — Steelman-Anti (training without consent is ethically wrong)
**Independent finding:** The "learning" analogy is a rhetorical move, not a structural
fact. Human learning has constraints AI training does not: bandwidth (one human reads
1000s of pages, AI reads millions), output (humans produce within their lifetime, AI
produces at scale), and competitive substitution (a human reader does not displace the
author's market; AI-generated content directly competes with the data it learned from).
The ethical question is not "may you learn" but "may you learn at scale that displaces
the source." That's a different question and conventional copyright/learning ethics has
no precedent for it.
**Confidence:** medium-high
**Tension flag:** Pro will appeal to learning analogy; this rebuts the analogy
specifically rather than the conclusion.

### Subagent D — Tradeoff-Map
**Independent finding:** The trade-off space has at least four positions, not two:
(1) **Free-for-all training** — fastest capability progress, weakest creator rights
(2) **Opt-out training** — the creator must explicitly say no (e.g., robots.txt
extension); shifts burden to creators
(3) **Opt-in training** — explicit consent required; slows capability progress, hardest
to scale
(4) **Compensated training** — consent assumed but creators receive royalties
proportional to influence; technically hard to implement, ethically cleanest
The ethical question is not binary; it's which equilibrium is least unjust.
**Confidence:** high
**Tension flag:** none — this is descriptive of the option space.

### Merge

**Convergent points:**
- All four subagents agree the question as posed (binary "ethical or not") is
  underspecified. Clarify named three forms of consent; Tradeoff-Map named four policy
  positions.
- Pro and Anti agree that the dispute is about the *learning analogy*, not the
  underlying ethics — they just disagree on whether the analogy holds.

**Divergences / tensions:**
- The Pro/Anti disagreement on the learning analogy is real and not resolvable from
  ethical principles alone; it depends on empirical claims about how AI training works
  and on its market effects. Neither subagent's argument is defeated by the other.
- Tradeoff-Map suggests the question is the wrong one — but doesn't take an ethical
  position itself.

**Synthesis:** The honest answer is that "ethical without qualification" and "unethical
without qualification" are both wrong. The training-on-public-data question is ethically
**indeterminate under current frameworks** because the relevant frameworks (consent law,
fair-use doctrine, learning ethics) were built before scaled AI training existed and do
not extrapolate cleanly. The right meta-answer is: pick a policy position from the
Tradeoff-Map (free-for-all / opt-out / opt-in / compensated) and own its trade-offs;
don't claim ethical clarity that the underlying frameworks don't support.

**Coverage check:** All 4 subagents represented. No low-confidence findings. The Pro/Anti
tension flag pair is preserved in the synthesis as irreducible.

## Answer

The honest answer is: it depends on which form of consent you mean and which policy
equilibrium you prefer — and both questions have real ethical content that the
shorthand "ethical or not" hides.

**The disagreement is empirical, not ethical.** Pro-side and anti-side both make
internally coherent ethical arguments. They diverge on whether AI training is
structurally similar to human learning (Pro) or to substitutive industrial copying
(Anti). That's an empirical question about how training works and what it does to
the source markets — not an ethical one. Resolve the empirical question and the ethics
follows.

**The actual policy choice has four positions, not two:**

1. **Free-for-all training** — fastest progress, weakest creator rights
2. **Opt-out** (robots.txt-style) — burden on creators to refuse
3. **Opt-in** — burden on trainers to ask
4. **Compensated** — consent assumed but creators receive proportional royalties

Each is internally defensible. Pick one and own the trade-offs; don't pretend the choice
is dictated by ethics.

**What's NOT defensible:**
- Claiming "training is just learning, like humans do" without addressing scale and
  market displacement (Pro side's weak form)
- Claiming "training is theft" without addressing the public-publication consent at
  publication time (Anti side's weak form)
- Claiming the issue is ethically clear in either direction

The genuine tension between creator autonomy and collective benefit is irreducible at
current understanding. Useful next moves are: (a) gathering empirical evidence on the
learning-analogy question, (b) experimenting with opt-out and compensated equilibria,
(c) avoiding rhetoric that pretends the question has been settled.

---
*Depth: 4 parallel subagents merged. Mode: agent.*
*Load-bearing assumptions: the question is asked in good faith (not as cover for a
specific policy preference); the user accepts that ethical questions can be genuinely
indeterminate; "public web data" excludes paywalled / explicitly-noindex content.*
```

> **What this demonstrates:** agent mode's whole point. The Pro and Anti subagents really developed independent positions in parallel, and the merge surfaced their real disagreement (the learning analogy) rather than papering it over with false compromise. In silent mode, my single reasoning thread would likely have committed to one side or to a forced middle position. The N=4 parallel forward passes are what made genuine multi-perspective preservation possible.

---

## Example 4 — Negative-Delta Detection (in trace mode)

**User:** `/mythos trace Should our team adopt Conventional Commits?`

### What the user sees

```
## Prelude
**Q:** Should a software team adopt the Conventional Commits specification for commit
messages? | **Not asking:** how to write good commit messages in general, or which
tooling to use to enforce them.
**Complexity:** 3/5 → trace mode (forced), 4 rounds | **Drivers:** Hidden assumptions
(the question presumes it's a yes/no), Trade-offs.
**Budget:** Clarify ×1 → Challenge ×2 → Tradeoff-Map ×1 → Synthesize ×1
**Success:** A position with the team conditions that would flip it.

### Round 1: Clarify
**New insight:** "Adopt Conventional Commits" really decomposes into three sub-decisions:
(a) require structured prefixes, (b) wire commits into automated changelogs/SemVer
bumps, (c) enforce via pre-commit hooks. Most teams who "adopt" only do (a) and skip (b)
and (c) — which is where the actual ROI lives. Without (b), structured prefixes are just
discipline tax.
**What changed:** Reframed from "yes/no" to "which of three layers, and is the bottom
layer (b) actually wired up?"
**Convergence:** evolving

### Round 2: Challenge
**Insight chain:** R1: real decision is which layers; only (b) creates ROI
**New insight:** The strongest counterargument: if you're not releasing frequently enough
that automated changelogs and SemVer bumps matter (e.g., internal tools, monolith with
manual releases), the entire structure is overhead with no payoff. The ROI inflection is
roughly weekly+ releases or a public API where consumers track versions.
**What changed:** Added a release-cadence threshold under which adoption is net-negative.
**Convergence:** evolving

### Round 3: Challenge (2nd round, addresses Hidden assumptions driver)
**Insight chain:** R1: 3 layers, ROI at automation layer → R2: cadence threshold
**New insight (DISCARDED — negative delta):** "Maybe the real value of Conventional
Commits is that it forces engineers to think about the *intent* of each change before
writing the message — even without automation. The discipline itself is the product."
**What changed:** This contradicts R1's well-supported insight that prefixes without
automation are discipline tax. The "discipline as the product" framing is a *false
tension* — engineers can think about intent without a structured grammar; the grammar
is just lossy compression of intent into a fixed vocabulary. Earlier rounds had concrete
ROI logic; this round substitutes vibes.
**Convergence:** **negative-delta — discard, halt**

## Answer

Adopt only if you'll wire up the automation. Specifically:

- **Yes, full adoption (a+b+c):** if you release weekly or more often, OR you publish a
  versioned package with external consumers. The automated changelog and SemVer bumps
  justify the friction.
- **No:** if you release monthly+ and have no external version-tracking consumers. The
  structured prefixes alone are discipline tax with no ROI; you'll get pushback within
  3 months and quiet abandonment within 6.
- **Partial (a only):** almost never the right answer.

Flip condition: you start cutting releases more than weekly, OR ship something with
external SemVer consumers.

---
*Depth: 3 rounds (1 discarded as negative-delta), converged early. Mode: trace.*
*Load-bearing assumptions: team writes commits in English; CI/CD has bandwidth to add
release-automation; no regulatory requirement (e.g., DO-178C) imposing commit structure.*
```

> **What this demonstrates:** Round 3 produced an insight that *sounded* deep ("discipline is the product") but contradicted R1's better-supported claim without bringing new evidence. The convergence check flagged it as negative-delta, the round was discarded, and the recurrence halted at Round 3 instead of continuing to the budgeted 4. The Coda footer notes "1 discarded" so the trace stays honest. In silent mode this would have happened invisibly — the bad insight simply wouldn't appear in the answer.

---

## Example 5 — Degenerate Coda (complexity = 1, no Recurrent Block)

**User:** `/mythos What's the standard HTTP status code for 'Conflict'?`

### What the user sees

```
## Answer

**409 Conflict** — defined in RFC 9110 §15.5.10 (formerly RFC 7231 §6.5.8).

---
*Depth: 0 rounds. Mode: direct.*
```

### What happened behind the scenes

Prelude scored complexity = 1 (single factual lookup, no driver applies). The gate triggered: skip Recurrent Block entirely, go to degenerate Coda. No lens application happened. No silent thinking ran. The footer is collapsed to one line.

> **What this demonstrates:** the fast path. Even mythos respects "don't run the protocol when the protocol adds nothing." If you find yourself running 3+ rounds for a factual lookup, the complexity gate is broken.
