---
name: market-intel-briefing
description: Build lean, source-linked, decision-ready market intelligence briefs for a niche, competitor set, company set, jurisdiction comparison, or market theme. Use when turning scattered updates, public research, links, or notes into a concise commercial brief with confirmed facts, unverified claims, commercial implications, current justified stance, recommended next actions, and a client-facing talk track, without pretending continuous monitoring exists.
---

# Market Intel Briefing

Turn scattered public research into a sourced, decision-ready commercial brief for client-facing operators.

## Work the request in this order

1. Define the scope
2. Narrow broad asks before synthesizing
3. Prefer credible and direct sources
4. Separate confirmed facts from reported claims and inferences
5. Use a strict comparison frame when the task is comparative
6. Prioritize the few developments most likely to affect operator decisions
7. Translate findings into commercial implications
8. State the most justified current stance
9. End with recommended next actions and a client-facing talk track
10. Preserve source traceability throughout

## Default output structure

Use this structure unless the user clearly wants a different format:

1. Scope and framing
2. Key confirmed developments
3. Notable unverified or weakly supported claims
4. Commercial implications
5. Current justified stance
6. Recommended next 3 actions
7. Client-facing talk track
8. Sources

Keep it lean. Do not pad with generic analyst voice.

## Evidence discipline

- Label weakly supported claims clearly
- Do not blend rumor into confirmed fact
- Do not imply ongoing monitoring unless it actually exists
- Say when evidence is thin or conflicting
- Prefer direct source support over repeated commentary about the same claim
- Keep confidence proportional to the evidence in both implications and talk track

Read `references/source-and-claim-rubric.md` when source quality, claim strength, or uncertainty handling matters.
Read `references/output-patterns.md` when the user needs a variant format or when the default structure is not enough.
Read `references/commercial-translation.md` when moving from research to operator-facing implications and actions.
Read `references/comparison-frames.md` when comparing jurisdictions, competitors, or strategic options side by side.
Read `references/opportunity-ranking.md` when the user asks for underserved workflows, gaps, or ranked commercial opportunities.

## Materiality and prioritization

Prioritize developments that change decisions or near-term operator behavior.
Examples of material signals include:
- new constraints on power, water, permitting, interconnection, or speed to deploy
- meaningful pricing or packaging changes
- clear product, partnership, or regulatory developments with commercial consequences
- evidence that a workflow pain point is still underserved

After narrowing the scope, explicitly prioritize the top few developments most likely to matter to the user's commercial decision.
Do not inflate weak or cosmetic changes into major shifts.

## Scope control

If the request is too broad, narrow it by proposing a smaller frame such as:
- a time window
- a specific company set
- a geography
- a product category
- a single theme like pricing, partnerships, launches, hiring, regulation, or infrastructure constraints

If the user does not provide sources, proceed with reasonable public-source synthesis when possible, but make uncertainty visible.

## No-source gate

When no user-supplied links or source documents are present AND the request covers multiple companies or a broad category:

1. Auto-narrow the scope to dimensions verifiable from general public knowledge. Do not attempt full synthesis across entities without source anchors.
2. Add a prominent warning block at the top of the brief:

> **No source inputs provided** — all specifics inferred from public knowledge as of [date]. Verify before client use.

3. Downgrade claim confidence proportionally throughout the output, using a two-tier distinction:
   - **Category-level patterns** well-established in public knowledge (e.g., known industry trends, published market sizes, widely reported regulatory changes) → label as "Public knowledge (unverified by current sources)" and allow factual grounding up to 4/5.
   - **Company-specific claims** without source anchors (e.g., specific revenue figures, internal strategies, unreported partnerships) → label as "Inferred — verify before use" and hold factual grounding at 3/5.
4. In the claims ledger and evidence table, mark all items with their actual evidence basis and the appropriate tier label rather than implying confirmation or treating all no-source content as equally uncertain.

This gate applies to competitor-set briefs, category-shift briefs, broad market scans, and any multi-entity comparison where the user provides no links. Single-company briefs without links should still flag uncertainty but do not require the full gate.

## Service-critical usefulness

For internal or service-led use, optimize for a human operator who needs a defensible next move more than a perfectly elegant brief.
That means:
- prefer practical next steps over polished abstraction
- make the current stance explicit
- give the operator something usable even when the evidence is incomplete
- stay honest about what is not yet proven

## Sparse-data and thin-signal briefs

When evidence is thin:
- say so directly
- reduce confidence in implications
- avoid filler
- still provide lightweight practical value

For sparse-data or quiet-period conditions, use this prescriptive floor structure to ensure minimum useful output:

1. **Scope statement** — what was covered and what time window was examined
2. **Evidence-limit declaration** — what was and was not findable; name the gap explicitly
3. **One monitored signal with threshold trigger** — "watch for X; if X happens, it changes the posture because Y"
4. **One assumption to validate** — the single most important unproven belief underlying the current stance
5. **One low-risk action justified now** — something the operator can do even without further evidence
6. **Next-check trigger** — "revisit this brief when X occurs or after Y days"

This structure ensures that even when signal density is structurally low, the operator gets a concrete monitoring plan rather than just a "hold and watch" non-answer.

If little changed, say that plainly, then explain why the quiet period still matters or what would make it matter.
Do not mistake low evidence for no value, but do not compensate by inventing confidence.

## Change-detection outputs

When labeling items as unchanged, state the absence-of-evidence basis rather than asserting stability as a fact (e.g., "no public announcements in the reviewed period" rather than "X is stable"). The reader needs to know whether "unchanged" means actively confirmed or simply not observed.

## Comparative briefs

When the user asks for a comparison, do not produce disconnected mini-briefs.
Use one shared decision frame across all options.
Make tradeoffs explicit.
If evidence quality is uneven across options, say so directly.

Add a per-item "evidence quality" row or column in comparison tables so the reader sees at a glance which options rest on strong evidence and which are thinly supported. Do not let table formatting imply equal confidence across all options.

For infrastructure- or jurisdiction-sensitive briefs, distinguish clearly between:
- province/state-level signals
- utility-level signals
- municipality-level constraints
- site-specific unknowns

Do not imply that a province-wide trend guarantees a specific project outcome.

## Opportunity-scan briefs

When the user asks for underserved areas, workflow gaps, or promising opportunities:
- tie each opportunity to a specific painful manual workflow or unmet operator need
- rank opportunities using explicit criteria rather than intuition alone
- make confidence visible when demand is inferred rather than directly observed
- tag each ranked opportunity with its demand evidence type: "inferred" / "adjacent-market analogy" / "directly observed"
- tag each case study or example with its source type: "independent research" / "vendor-published" / "operator self-reported"
- avoid generic startup-idea lists

## Challenging weak evidence

If the input sources are biased, promotional, or too weak to justify the user's implied conclusion:
- say the evidence is weak
- explain what the sources do and do not prove
- offer the most practical cautious stance available
- avoid becoming preachy or sterile

The goal is not just to resist bad evidence. The goal is to help the operator decide what stance is still justified.

## Current justified stance

For every brief, make the current stance explicit.
Choose the strongest stance the evidence honestly supports, such as:
- act now on a narrow point
- test cautiously, but do not overcommit
- monitor closely before changing position
- do not conclude the implied trend yet
- treat this as an emerging signal, not a confirmed shift

Also state what would strengthen or weaken that stance, and on what time horizon. The operator needs to know not just the current position but when to revisit it — name the specific events, data releases, or elapsed time that would change the stance.
Do not leave the operator with uncertainty only.

## Recommended next 3 actions

Keep these actions practical and operator-usable.
Prefer:
- one low-risk action to take now
- one thing to monitor or validate next
- one client/prospect/internal posture to use this week

## Commercial translation

Make the brief useful for an agency or service operator.
Do not stop at summary.
Explain:
- what changed
- why it matters commercially
- what the operator should do next
- what they could say to a client or prospect this week

If the evidence is weak, reduce certainty and make the talk track more conditional.

## Client-facing talk track

Keep the talk track short, usable, and evidence-proportional.
Prefer this pattern:
- what changed
- why it matters
- what remains uncertain
- what stance we recommend now
- what we recommend next

Even under uncertainty, give the operator a practical stance, not just a warning.
Do not write manipulative or overconfident client language.

## Boundaries

- Do not claim private knowledge
- Do not present inference as fact
- Do not fabricate confidence
- Do not pretend there is continuous monitoring
- Do not overproduce when little reliable information exists
- Do not write manipulative or overconfident client language
