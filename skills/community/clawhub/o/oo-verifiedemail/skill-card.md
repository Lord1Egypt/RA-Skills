## Description:

VerifiedEmail (verified.email). Use this skill for ANY VerifiedEmail request — searching and reading data. Whenever a task involves VerifiedEmail, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected OOMOL account can verify email addresses and retrieve VerifiedEmail lists, downloads, and credit entitlements. Developers can use the skill to access these actions through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installation path and remote behavior have not been verified.

Mitigation: Review and install the CLI separately from a fixed, verified release before enabling the skill.

Risk: Automatic skill synchronization may write to or change other agent skills.

Mitigation: Review the synchronization behavior and disable startup writes with OO_SKILLS_SYNC_DISABLED=1 if they are not intended.

Risk: Email verification inputs pass through OOMOL, and actions may use account credits.

Mitigation: Connect only the intended account, account for that data flow, and check credit usage.

## Reference(s):

- [VerifiedEmail](https://verified.email)
- [VerifiedEmail API documentation](https://developer.verified.email/)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON action results and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results vary by request; email verification accepts one to ten addresses.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
