# Step 2: Claim-Evidence Map

## Goal

把论文里的所有主要 claim 转成可防守/不可防守的证据表。

## Required claim categories

- Problem claim
- Novelty claim
- Method claim
- Theory claim
- Experiment claim
- Efficiency / compute claim
- Reproducibility claim
- Limitation claim
- Practical / deployment claim

## Output table

| Claim | Evidence | Evidence label | Strength | Caveat | Likely question | Safe answer posture |
|---|---|---|---|---|---|---|

## Red-team check

For each claim, ask:

- Is the evidence direct or indirect?
- Does the evidence match the scope of the claim?
- Are there missing baselines or stress tests?
- Does the claim depend on code/training details not shown in the paper?
- Would a reviewer accept the evidence as sufficient?
