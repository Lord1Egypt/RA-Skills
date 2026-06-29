# Business Anchors and Agreement Preservation

Use this before writing detailed PRD content, before major rewrites, and whenever a later section may override the user's agreed business understanding. The goal is to prevent obvious-but-critical business facts from being lost during polishing, restructuring, or "best practice" generalization.

## Core Rule

The PRD must follow the business mainline agreed with the user. Anything extended beyond that mainline needs a basis. Generic industry practice, elegant wording, or a mature pattern can guide recommendations, but cannot replace confirmed business facts.

## Business Anchor List

Create a short "business anchors / non-negotiable premises" section for complex PRDs:

| Anchor | Plain-Language Meaning | Why It Must Hold | Source / Who Confirmed | Affected Objects / Flows | What Must Not Override It | Change Requires |
|---|---|---|---|---|---|---|

Anchors are not generic rules. They are the facts this product/business depends on, such as pricing model, fund model, role relationship, source-of-truth decision, or legal/operational constraint.

## Obvious Premise Rule

Ask during early discussion:

- What is so obvious to the business team that they may forget to write it?
- Which phrase would an insider understand immediately but a new developer/tester would not?
- Which "default premise" would break the whole PRD if replaced by generic wording?
- Which money/pricing/status/source rule is treated as common sense by the team?

The more obvious a premise feels to insiders, the more explicitly it should be written.

## Extension Basis

Every derived rule, state, field, page, interaction, exception, or component must trace to one of:

| Basis | How To Label |
|---|---|
| User confirmed | Confirmed by user / business |
| Business anchor | Derived from anchor: X |
| Existing system / historical behavior | Based on current system behavior |
| Source data / source document | Based on source object/document X |
| Market / mature pattern research | Recommended pattern, pending confirmation |
| Product inference | Inferred, pending confirmation |

If none applies, do not write it as final PRD口径.

## Generic Practice Guard

Before using a generic best practice, ask:

| Question | If No |
|---|---|
| Does this fit the agreed business mainline? | Do not use it as final口径 |
| Does it preserve all business anchors? | Mark conflict and ask user |
| Does it change pricing/fund/status/source semantics? | Requires explicit confirmation |
| Is it only "more professional wording"? | Keep business-specific wording |

Example pattern:

- Bad: Replace a confirmed cost-plus model with "receivable should come from contract/receivable bill" because it sounds more standard.
- Better: "This business uses cost-plus pricing; contract/receivable bill wording is only valid if it preserves cost-plus source and service-fee rule."

## Rewrite Preservation

Before rewriting or reorganizing a section, extract its current business conclusions:

| Section | Existing Business Conclusion | Is It An Anchor? | Must Preserve? | New Wording | Changed? | Confirm |
|---|---|---|---|---|---|---|

If new wording changes a conclusion, surface it as a decision. Do not silently replace concrete business facts with generic phrasing.

## Change Control

Any change to a business anchor must be explicit:

- what anchor changes;
- old口径 and new口径;
- why it changes;
- which flows/objects/pages/tests are affected;
- who confirmed it;
- whether previous sections need rewrite.

If confirmation is missing, keep the original anchor and mark the proposed change as待确认.
