# Output Template

## Purpose
Define the expected final output shape for the MVP of `openclaw-consensus`.

The final artifact should help the user understand:
- what seems stable across models
- where material disagreement remains
- what is still uncertain
- what specific narrow areas may justify expert escalation

## Final output structure

### 1. Brief
- original question or scenario
- optional run label
- models/providers used

### 2. Consensus
List the points that all or nearly all selected models support after round 2.

Rules:
- keep this concrete
- prefer a short numbered list
- do not include weak pseudo-agreement

### 3. Disagreements
List the points where the selected models still materially differ after round 2.

Rules:
- focus on meaningful disagreement only
- identify the substance of the disagreement
- if useful, indicate which model(s) lean which way

### 4. Uncertainties
List what remains unclear, source-sensitive, assumption-sensitive, or unresolved.

Rules:
- uncertainty is not failure
- surface it explicitly
- avoid hiding uncertainty inside vague prose

### 5. Escalation points
List the narrow issues that may justify expert review.

Examples:
- legal interpretation boundary
- accounting treatment edge case
- jurisdiction-specific compliance rule
- engineering feasibility assumption

Rules:
- keep escalation targeted and narrow
- do not say “consult an expert” generically unless the whole question truly requires it

### 6. Final synthesis
Provide the best overall answer available from the 2-round process.

Rules:
- synthesize rather than repeat
- preserve confidence posture honestly
- do not overclaim certainty
- the synthesis should still be useful even if some disagreement remains

## Suggested markdown shape

```markdown
# OpenClaw Consensus — Final Synthesis

## Brief
...

## Models Used
...

## Consensus
1. ...
2. ...
3. ...

## Disagreements
1. ...
2. ...

## Uncertainties
1. ...
2. ...

## Escalation Points
1. ...
2. ...

## Final Synthesis
...
```

## Quality rules
- easy to scan
- useful without opening every intermediate artifact
- honest about limits
- disagreement preserved when real
- escalation guidance should be practical, not defensive boilerplate

## MVP note
This template defines the expected final report only.

Intermediate artifacts for round 1 and round 2 can remain simpler in v1, as long as they preserve the reasoning trail clearly.
