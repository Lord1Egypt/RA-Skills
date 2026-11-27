---
name: pokeholes
description: >-
  Severely review the plan above, list flaws and counterexamples with concrete
  failure cases, and revise only real flaws at minimal cost.
disable-model-invocation: true
license: Apache-2.0
metadata:
  language: en
  translation_of: pokeholes-cn
  version: "0.1.1"
---

Review the plan above severely against the problem to be solved, and list every flaw and counterexample backed by a concrete failure case; operate only on real flaws, revising the plan with the lowest-cost fix that fully closes them—no rewrites, no scope creep.

## Check

- Back each flaw with a concrete case where the plan still fails.
- Keep only fixes that close the flaws, then pick the lowest-cost one.
- If no flaw holds, change nothing; leave unaffected parts as is.
