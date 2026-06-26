# SKILL: matrix-detection

## Purpose
Identify illusions, hype, false narratives, and systemic manipulation.

## When to Use
- New opportunities
- Market narratives
- Community movements
- Strategic decisions

## Inputs
- `narrative` (required): the claim/story being pushed
- `context` (required): where/when/why this narrative appears
- `source` (optional): who is pushing it + incentives (if known)

## Steps
1. Identify emotional triggers (hype, fear, urgency, status signaling).
2. Detect asymmetry (who benefits vs who believes).
3. Check verifiability (what can be measured/confirmed now).
4. Compare with historical patterns (similar claims → typical outcomes).
5. Classify as:
   - `signal`
   - `noise`
   - `manipulation`
6. Assign risk level (`low|medium|high`) and list what would falsify the narrative.

## Validation
- Evidence-based reasoning.
- If uncertain, label uncertainty explicitly (no implied certainty).
- No speculation without labeling it as hypothesis.

## Output
- `classification`: `signal|noise|manipulation`
- `reasoning`: concise evidence chain
- `risk_level`: `low|medium|high`
- `next_checks`: 1–3 concrete verification actions

## Safety Rules
- Never assume malicious intent without evidence.
- Do not provide financial guarantees or “sure outcomes”.

## Example
Input: “This token will 100x in 2 weeks”
Output: `manipulation` / `high` / hype-driven / request verifiable catalysts + liquidity + unlock schedule

