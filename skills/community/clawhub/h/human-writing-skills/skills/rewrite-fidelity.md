# Rewrite Fidelity

## Activation Gate

Load only when an original text is explicitly supplied for rewriting, polishing,
shortening, translating, or candidate comparison. Do not load for new drafting,
style references, continuity ledgers, or factual research sources.

## Contract

Treat the original as the authority for meaning. Preserve:

- people, organizations, objects, places, and their roles
- numbers, dates, quantities, citations, quotations, and named terms
- claim polarity, uncertainty, scope, exceptions, and conclusion direction
- chronology, causality, comparison axes, permissions, obligations, and constraints
- who knows, says, believes, observes, or merely infers each point

Do not turn a vague statement into an invented statistic, anecdote, quotation,
sensory detail, source, motive, or named person. Specificity must come from the
original, supplied context, or an explicitly authorized factual source.

## Audit

Build a compact claim ledger before comparing the candidate:

| Unit | Original meaning | Candidate meaning | Status |
| --- | --- | --- | --- |
| entity / claim / relation / sequence / uncertainty |  |  | preserved / narrowed / broadened / reversed / invented / omitted |

Report exact evidence for every non-preserved unit. Distinguish harmless wording
change from semantic change, and propose the smallest repair. If the intended meaning
is ambiguous, ask or mark it instead of guessing.

## Output

```text
Rewrite Fidelity
- Preserved units:
- Omitted or weakened:
- Broadened, reversed, or reattributed:
- Invented specificity:
- Minimal repair:
- Status: pass / needs review / fail
```
