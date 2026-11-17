## Description:

Retired signal. No longer sold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External users can check that the position-exposure signal has been retired and should not configure an agent to call its endpoint. The notice points them to the portfolio-heat listing for current alternative details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent configured to call the retired endpoint will receive HTTP 410 and cannot obtain position-exposure data.

Mitigation: Do not configure an agent to call or pay for this endpoint; check the portfolio-heat listing for current product details.

## Reference(s):

- [Position-exposure signal page](https://apexrunner.ai/signals/position-exposure)
- [Portfolio-heat signal listing](https://apexrunner.ai/signals/portfolio-heat)
- [ClawHub release listing](https://clawhub.ai/kynto2001-ctrl/skills/position-exposure)

## Skill Output:

**Output Type(s):** [Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retirement status notice; documents the endpoint's HTTP 410 response.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
