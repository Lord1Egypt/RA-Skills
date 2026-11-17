## Description:

MSG91 (msg91.com). Use this skill for ANY MSG91 request — reading, creating, and updating data. Whenever a task involves MSG91, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can send SMS and OTPs, resend OTPs, and verify OTPs through an OOMOL-connected MSG91 account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs changeable remote code without a clear approval or verification step.

Mitigation: Prefer a separately approved, verified oo CLI release and review its automatic skill synchronization before installing.

Risk: Sending or resending SMS and OTPs can reach unintended recipients or expose unintended message content.

Mitigation: Confirm recipients and message contents before sending.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [MSG91](https://msg91.com)
- [MSG91 API documentation](https://docs.msg91.com/overview)

## Skill Output:

**Output Type(s):** [API calls, JSON responses, Shell commands]

**Output Format:** [JSON payloads and responses with oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may send or resend SMS and OTP messages.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
