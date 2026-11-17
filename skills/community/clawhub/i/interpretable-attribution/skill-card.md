## Description:

Interpretable Attribution is a model-agnostic skill that explains single predictions with global permutation importance, local feature ablation, greedy counterfactual changes, and a natural-language rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, model owners, and compliance reviewers use this skill to explain why a single classification or regression prediction was produced and to explore whether small feature changes would alter the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs user-supplied Python predictor files as executable code.

Mitigation: Use predictor files you wrote or audited, and run attribution work in an isolated workspace when handling unfamiliar code.

Risk: The learner module can store local usage notes and preferences.

Mitigation: Avoid sensitive data in learner notes or preferences, or disable the learner module when local usage history is not needed.

Risk: Attribution results can be unreliable with small samples, nested features, or approximate counterfactual searches.

Mitigation: Use adequate sample sizes, flatten nested features before use, and treat greedy counterfactual results as approximate explanations.

## Reference(s):

- [ClawHub skill page: interpretable-attribution](https://clawhub.ai/qq435912743/skills/interpretable-attribution)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with optional JSON attribution output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses flat JSON records with a label field and a Python predict(r) function; attribution reliability depends on the dataset and predictor.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
