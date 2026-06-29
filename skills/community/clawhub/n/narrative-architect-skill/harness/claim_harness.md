# Claim Harness

## Purpose

Validate that the rendered output respects the claim boundaries established by the Claim Boundary Extractor.

A story can be beautiful, natural, and audience-appropriate, and still be false. The Claim Harness is the gate that catches this.

## Position in Chain

```
Main Renderer + Style Wrapper → Claim Harness → Source Fidelity Harness → Surface Naturalness Harness → Final Output
```

## Checkpoints

### 1. Claim Boundary Violation

Check every substantive sentence in the output against its source claim.

Fail if:
- A "verified" claim becomes a "proven" claim
- A "speculative" claim becomes an asserted claim
- A claim's boundary condition is removed or softened
- A "likely" claim is presented without its uncertainty qualifier
- A claim whose negation condition is known is presented as unconditional

Example:
Source claim: "Product X reduced complications by 30% in a 200-patient single-center study."
Boundary: limited to the study population and setting.
Pass: "In one study of 200 patients, X reduced complications by 30%."
Fail: "X reduces complications by 30%." (boundary removed, tense changed to universal)

### 2. Unsupported Assertion

Check for claims in the output that have no trace to source material.

Fail if:
- A new factual assertion appears without source provenance
- A causal claim is made without evidence trace
- A quantitative claim appears without data provenance
- "Research shows..." without citing what research

### 3. Boundary Hardness Violation

Check that hard boundaries are treated as hard and soft boundaries remain soft.

Fail if:
- A hard boundary (laws of physics, settled clinical findings) is presented as debatable
- A soft boundary (market estimate, expert opinion) is presented as settled fact

Example:
Hard boundary: "The device requires 220V power."
Fail: "The device can work with any power supply."
Pass: "The device requires 220V power, which means..."

### 4. Unsaid Suppression

Check that the output does not suppress what the source material explicitly does not say.

Fail if:
- A claim's explicit limitation ("not tested in patients over 65") is omitted
- A claim's comparator ("compared to standard suture, not to antibacterial suture") is omitted
- A claim's timeframe ("at 6-month follow-up, not at 1 year") is omitted

### 5. Upgraded Implication

Check that narrative language does not imply stronger claims than the source.

Fail if:
- "may" → implied as "does"
- "associated with" → implied as "caused by"
- "in select cases" → implied as "generally"
- "preliminary evidence" → implied as "established"

## Rewrite Instruction

If the output fails this harness, do not patch it. Return to the Main Renderer with the specific violations flagged. Patch-level fixes to claim violations compound over multiple edits and degrade traceability.
