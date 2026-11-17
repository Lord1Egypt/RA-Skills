## Description:

Mailcheck (usercheck.com). Use this skill for ANY Mailcheck request — searching and reading data. Whenever a task involves Mailcheck, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents working with Mailcheck use this skill to inspect account status and validate domains or individual email addresses through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can execute downloaded code without a clear approval step.

Mitigation: Review setup first, install a pinned and verified CLI separately, and require approval before running installers or making additional agent-skill changes.

Risk: Email addresses and domains submitted for verification are sent through OOMOL to UserCheck, and verification may consume service credit.

Mitigation: Submit only addresses and domains appropriate to share, and check service credit requirements before running verification.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Mailcheck homepage](https://www.usercheck.com)
- [UserCheck API documentation](https://www.usercheck.com/docs/api/authentication)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured responses from account status, domain validation, and email verification actions, with concise explanatory text as needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include account and plan information, domain risk and MX signals, or email deliverability and risk signals.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
