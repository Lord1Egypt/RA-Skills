## Description:

Use this skill to operate SerwerSMS.pl through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents managing a SerwerSMS.pl account use this skill to check account limits and delivery reports, manage sender names, and send, schedule, or cancel SMS messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup runs remote code that was not verified.

Mitigation: Review and verify the CLI installation before allowing setup.

Risk: Startup skill synchronization can make persistent changes by installing or refreshing agent skills.

Mitigation: Disable startup skill synchronization unless additional skills should be installed or refreshed.

Risk: SMS sends may incur charges, and scheduled-message cancellation changes account state.

Mitigation: Check recipients, message content, charges, and cancellation targets before approving the operation.

## Reference(s):

- [SerwerSMS.pl API documentation](https://dev.serwersms.pl/en/https-api-v2/introduction)
- [SerwerSMS.pl](https://serwersms.pl/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-serwersms-pl)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector results with concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas are checked before calls; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
