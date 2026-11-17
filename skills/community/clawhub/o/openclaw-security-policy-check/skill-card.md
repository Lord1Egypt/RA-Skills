## Description:

Automates security audits for OpenClaw gateway configurations by checking key settings and reporting common security risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asantssec](https://clawhub.ai/user/asantssec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw gateway configuration before deployment or during routine security reviews. It reports risky settings and recommended manual fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit output can expose part or all of a local OpenClaw gateway authentication token.

Mitigation: Run the skill only in a private terminal, avoid shared logs or CI, and rotate any short, default, or exposed token.

## Reference(s):

- [OpenClaw Security Audit on ClawHub](https://clawhub.ai/asantssec/skills/openclaw-security-policy-check)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text report with configuration findings and recommended fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit output may include local configuration values or command output.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
