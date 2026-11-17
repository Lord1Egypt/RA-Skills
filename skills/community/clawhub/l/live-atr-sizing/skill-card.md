## Description:

Retired signal. No longer sold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers managing trading agents can use this release information to identify the retired live ATR position-sizing signal and understand its current availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The endpoint returns HTTP 410 Gone, so agents depending on the live signal cannot retrieve ATR sizing recommendations.

Mitigation: Remove this endpoint from agent workflows and use a separately validated position-sizing source.

## Reference(s):

- [Live ATR Sizing signal page](https://apexrunner.ai/signals/live-atr-sizing)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/live-atr-sizing)

## Skill Output:

**Output Type(s):** [Guidance]

**Output Format:** [Markdown release information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retirement notice; no live signal output.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
