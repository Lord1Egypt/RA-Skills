## Description:

CMA-ES continuous optimization for AI agents, including derivative-free optimization for hyperparameter tuning, portfolio optimization, and parameter calibration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to run CMA-ES for continuous black-box optimization tasks such as ML hyperparameter tuning, parameter calibration, portfolio allocation, and pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optimization inputs and the billing key are used with the OraClaw external service.

Mitigation: Install only if you trust OraClaw with those inputs and the ORACLAW_API_KEY value; avoid sensitive business, financial, or model data unless that use is acceptable.

Risk: The skill can incur paid external service usage.

Mitigation: Review the disclosed $0.10 per optimization pricing and the free tier before running high-volume optimization.

## Reference(s):

- [Oraclaw Cmaes on ClawHub](https://clawhub.ai/whatsonyourmind/skills/oraclaw-cmaes)
- [OraClaw CMA-ES homepage](https://oraclaw.dev/cmaes)

## Skill Output:

**Output Type(s):** [text, json, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool parameters and text result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ORACLAW_API_KEY and may incur $0.10 per optimization after the free tier.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
