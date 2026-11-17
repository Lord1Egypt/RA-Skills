## Description:

Automatically detects health measurements in chat messages and logs weight, blood sugar, and exercise values to the AX3 Personal system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klcintw](https://clawhub.ai/user/klcintw)

### License/Terms of Use:


## Use Case:

Developers and personal automation agents use this skill to process health-related messages and record detected weight, blood sugar, or running-time metrics in AX3.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically record sensitive health data from broad chat triggers, including ambiguous numeric messages.

Mitigation: Use explicit message routing or confirmation before recording values, especially in shared or ambiguous messaging channels.

Risk: The AX3 write operation depends on a local mcporter configuration and associated credentials.

Mitigation: Run only in a controlled environment with appropriately scoped AX3 credentials and review failures before relying on created records.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, Guidance]

**Output Format:** [JSON plus short confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local mcporter access to AX3 and validates configured metric ranges before recording.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
