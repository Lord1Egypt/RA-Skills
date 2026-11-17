## Description:

Retired signal. No longer sold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this notice to check the live fill-rate signal's status. It states that the signal is retired, its endpoint returns HTTP 410 Gone, and agents should not call it; there is no direct replacement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The signal is retired and its endpoint returns HTTP 410 Gone, so calls will fail.

Mitigation: Do not configure an agent to call the endpoint.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kynto2001-ctrl/skills/live-fill-rate)
- [APEX Runner live fill rate status](https://apexrunner.ai/signals/live-fill-rate)
- [APEX Runner](https://apexrunner.ai)

## Skill Output:

**Output Type(s):** [Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retirement notice; no live signal data is produced.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
