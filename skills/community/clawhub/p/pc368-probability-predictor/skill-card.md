## Description:

Analyzes PC368 draw history by collecting recent results, building frequency statistics, and reporting cold-number and hot-number prediction scenarios with validation metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powerzzjohn](https://clawhub.ai/user/powerzzjohn)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to collect recent PC368 draw data, compute per-position frequency statistics, and produce a statistical report with cold-number and hot-number scenarios. The output should be treated as statistical entertainment rather than betting advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens a third-party gambling-adjacent site to retrieve live draw data.

Mitigation: Install only when PC368 analysis is intended, review browser activity, and keep use within applicable policies.

Risk: Broad trigger phrases could activate the skill for generic prediction requests.

Mitigation: Require explicit PC368 wording or narrow triggers before deployment.

Risk: Prediction output may be mistaken for reliable betting advice.

Mitigation: Present results as statistical entertainment and include uncertainty and caveats in the report.

## Reference(s):

- [Pc368 Probability Predictor on ClawHub](https://clawhub.ai/powerzzjohn/skills/pc368-probability-predictor)
- [PC368 website](https://pc368.net/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with frequency distributions, prediction scenarios, validation metrics, and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser access to pc368.net and uses user-selected training period N and prediction duration M.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
