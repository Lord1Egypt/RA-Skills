---
load: on demand — when a feature is Indifferent / Reverse but the user (or their leadership) is pushing for it
parent: ../SKILL.md
---

# CEO Pushback Scripts

When a feature classifies as Indifferent or Reverse for the target segment, but
a stakeholder (CEO, VP, board member) is pushing for it in v1, you need both
the honest classification AND a script that survives the conversation. This
file gives you the scripts.

The skill's stance is non-negotiable: **classify honestly, then make the case
in the output.** Don't soften the classification to make the conversation
easier. Soft classifications rot into Experience Rot.

## The four patterns

Every CEO-pushed feature falls into one of four patterns. Identify which one
you're in, then use the matching script.

### Pattern 1 — Personal preference dressed as product decision

The stakeholder genuinely wants the feature, but the want is personal
(preference of the founder, the dev org, the early-access design partners) and
is not the target segment's need.

**Signal:** The stakeholder says "I really want this" or "users have been
asking for this" but the requestors are not in the target segment.

**Script:**

> "I classified [feature] as Indifferent for our launch segment
> — [segment name, with one-line evidence]. It would consume [T-shirt size]
> and [design surface impact]. I want to put those weeks into [MDP pick],
> which is the one feature that would make our target user choose us over
> [incumbent]. I'm happy to commit to [feature] in v[1.1 / 2.0] once we have
> post-launch data on whether the segment actually wants it. If it's truly
> important, I want to understand what I might be missing — is there a
> specific user or deal in the pipeline driving this?"

**Fallback if they insist:** Ship the feature as a *user setting that
defaults to off*, behind a feature flag, with the lightest possible design
investment. Do not ship it as a polished default-on feature.

---

### Pattern 2 — Mis-shaped implementation, right outcome

The stakeholder is right that the *outcome* matters, but wrong about the
*implementation*. The feature is a real need for the segment, but the version
they're asking for is over-engineered for the segment's actual workflow.

**Signal:** "We need Google-Docs-style real-time collab" (when the segment
needs comments + presence, not CRDT). "We need AI that summarizes every
contract" (when the segment needs AI clause extraction, not full NLU).

**Script:**

> "I agree that [outcome — e.g., 'the product must feel collaborative'] is a
> v1 must for our segment. Where I'd push back is on the implementation. The
> version you're describing — [Google-Docs-style CRDT, full NLU, etc.] —
> costs [T-shirt size L/XL] and has [risk profile — audit trail, accuracy,
> etc.] concerns for our segment. I'd ship [alternative — comments + presence
> indicators, scoped clause extraction, etc.] in v1, which delivers the
> outcome at [smaller size]. [Full implementation] goes on the v[2.0]
> backlog with a clear acceptance criteria — [X% of contracts have multiple
> simultaneous editors, or 80% extraction accuracy on the 8 named clause
> types]. If you want, I can write up the trade-off in one page so we have
> something to refer back to."

**Fallback if they insist:** Scope-split. Ship the v1 thin version in v1,
and ship the full version as a *separate opt-in mode* (e.g., a "Live mode"
toggle, a "Full AI" mode) rather than the default. Do not let the full
version become the default editing experience.

---

### Pattern 3 — Market-access condition, not a product feature

The stakeholder is asking for something that is a sales/security/legal
prerequisite, but it keeps getting scheduled on the product eng roadmap
because it has a UI component.

**Signal:** SOC2 Type II, HIPAA, GDPR, PCI-DSS, FedRAMP, ISO 27001, regional
data residency, audit log export. Anything where the *certification* is the
real work and the *UI element* is a 1-day ticket.

**Script:**

> "[Compliance item] is a market-access gate, not a product feature. The
> real work is the [certification, attestation, infrastructure] — that lives
> on a separate track with [compliance lead / security lead / GRC consultant]
> as the owner, not on product eng. The [UI element — badge, toggle,
> indicator] is a 1-day ticket once the gate is in hand. Let me make sure
> [stakeholder] understands this is parallel work, not on the 6-week critical
> path. If we try to put it on the product roadmap, it will consume eng cycles
> that belong to the user-facing Must-bes, and we'll still miss the
> certification date."

**Fallback if they insist:** Add a *placeholder* on the v1 roadmap (a UI
shell that links to "Coming Q2") so the stakeholder has something to point
at, and run the actual certification in parallel. Never block v1 launch on
the cert unless the compliance officer has said the cert must be in hand
before *any* sale closes (in which case it's a launch gate, not a feature).

---

### Pattern 4 — Politically-attached feature (no segment case at all)

The stakeholder wants the feature because of a personal relationship, a
board promise, a customer commitment, or political optics. There is no
analytical case for it.

**Signal:** "Customer X specifically asked for this." "The board expects
this." "We promised this at the last all-hands."

**Script:**

> "I want to make sure I understand the commitment. Is this [feature] tied
> to a specific customer contract, a board commitment, or a public statement?
> If so, I need to know the date and the audience so I can scope the
> minimum viable version that honors the commitment without consuming
> capacity we need for [MDP pick / Must-be features]. I can almost always
> find a [T-shirt size S or M] version of any feature that meets a
> specific commitment. The full version can wait."

**Fallback if they insist:** Find the smallest shippable version. Even if
the feature is a poor fit, a small version that meets the commitment is
better than a large version that consumes the whole roadmap. Document the
small version's limitations explicitly in the readout so the stakeholder
knows what they're getting.

---

## What to NEVER do in these conversations

- **Don't soften the classification** to make the conversation easier. A
  Reverse feature called Indifferent is a Reverse feature with a rebrand.
- **Don't promise "we'll add it later" without scoping the later**. "v1.1"
  is a real commitment only if there's a named T-shirt size and a named
  eng-weeks. Otherwise it's a kick-the-can promise.
- **Don't say "users want it" without naming the users**. The target segment
  is named. "Users" without a name is a vague request that everyone agrees
  with and no one is responsible for.
- **Don't ship the full version as the default to avoid a fight**. The
  default is the product. If the default is the wrong version, every user
  pays the cost.
- **Don't accept "do both"** without showing what gets cut. There is no
  infinite capacity. "Do both" with no cuts is the same as "do neither"
  because nothing actually ships on time.

## Closing the loop

After every CEO-pushed feature call, write down the decision and the
reasoning in a one-line format the stakeholder can refer back to:

```
[Feature]: KEEP / DEFER / SCOPE-SPLIT / KILL
Reason: [one sentence]
Trigger to revisit: [what data would change the call]
Date: [when this was decided]
```

Put it in the v1 spec doc, the design doc, or the project tracker. Verbal
alignment on scope is the #1 killer of B2B launches. The one-line writeup
prevents "I thought we agreed to..." two weeks later.
