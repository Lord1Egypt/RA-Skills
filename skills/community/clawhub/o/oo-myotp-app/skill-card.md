## Description:

Use a connected OOMOL account to read OTP status and transaction reports, generate or extend OTPs, and verify OTPs in MyOTP.App.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill through a connected OOMOL account to manage MyOTP.App OTP messages and retrieve transaction reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release needs review because its CLI dependency can change other agent skills, and the skill's safety labels do not mention that successful OTP verification consumes the code.

Mitigation: Install a verified CLI release, set OO_SKILLS_SYNC_DISABLED=1 to prevent startup writes, and treat successful verification as consuming the OTP.

Risk: Generating or extending an OTP changes service state, and OTP requests use the connected account through OOMOL.

Mitigation: Confirm the intended account, recipient, and message effects before making a change; do not include raw credentials in command payloads.

## Reference(s):

- [MyOTP.App skill release](https://clawhub.ai/oomol/skills/oo-myotp-app)
- [MyOTP.App developer API documentation](https://myotp.app/developer-api/)
- [MyOTP.App homepage](https://myotp.app)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples; connector responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured action responses may contain OTP status or transaction data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
