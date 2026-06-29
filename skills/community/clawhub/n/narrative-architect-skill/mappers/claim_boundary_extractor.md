# Claim Boundary Extractor

## Purpose

Before any narrative is built, extract the exact claims embedded in the source material and define their boundaries.

A claim without a boundary is propaganda. A claim with a boundary is argument. A claim with a boundary and a gap is story.

## Source

McKee's insight that meaning emerges from the gap between expectation and result applies not only to story structure but to the claims stories make. Every claim carries an implicit boundary—the condition under which it would be false. Narratives that hide their boundaries are manipulative. Narratives that surface their boundaries are credible.

## Required Output

```yaml
claim_boundary:
  source_material_type:  # raw input type (product brief / research paper / opinion / data)
  claims_extracted:
    - claim_id:
      claim_text:
      claim_type:       # factual / predictive / comparative / normative / causal
      confidence:       # verified / likely / speculative / unknown
      boundary:         # under what condition would this claim be false
      source_trace:     # where in the source material this claim originates
      unsaid:           # what the claim does not say
  conflict_zones:
    - zone:
      claim_a:
      claim_b:
      tension_type:     # contradiction / incompleteness / ambiguity / value_conflict
  boundary_hardness:
    hard_boundary:      # claims that cannot be bent (laws of nature, settled findings)
    soft_boundary:      # claims that depend on context (market estimates, expert opinion)
    unknown_boundary:   # claims we cannot bound yet
  narrative_license:
    allowed_stretch:    # how far can narrative expression go before claim is false
    forbidden_stretch:  # narrative moves that would violate claim boundaries
```

## Extraction Rules

```text
Rule 1: Every claim has a negation condition
If you cannot state what would prove the claim false, the claim is unfalsifiable.
Flag unfalsifiable claims. Do not narrativize them.

Rule 2: Confidence is not certainty
"Verified" means data exists.
"Likely" means expert consensus.
"Speculative" means plausible but unconfirmed.
"Unknown" means we don't know.
Do not upgrade confidence for narrative effect.

Rule 3: The unsaid is part of the claim
A claim that "Product X reduces complications by 30%" may not say:
- in which population
- compared to what
- with what confidence interval
Extract the unsaid. It defines the boundary.

Rule 4: Conflict zones are narrative gold
When two claims from the same source conflict, that is not a bug.
That is the gap. That is where story lives.
Surface it. Do not smooth it.

Rule 5: Narrative license is bounded
You may use metaphor, analogy, scene, and character to express claims.
You may not alter what the claim asserts to make a better story.
The claim boundary is the contract between source and story.
```

## Failure Modes

Bad: treating all claims as equal.
Fix: classify by type and confidence. A predictive claim carries different license than a factual claim.

Bad: widening boundaries to make the story better.
Fix: if the best story requires violating a claim boundary, you have the wrong story. Find the story that fits the boundary.

Bad: hiding the unsaid for rhetorical power.
Fix: the unsaid is where credibility lives. Surface it, don't bury it.
