## Description:

Okta (okta.com). Use this skill for ANY Okta request — reading, creating, updating, and deleting data. Whenever a task involves Okta, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

IT administrators and support agents use this skill to inspect and manage Okta users and groups through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags that Okta account access changes may occur without confirmation.

Mitigation: Before each lifecycle operation or other write, confirm the exact target account or group and the intended effect; use an Okta connection with only the permissions needed.

Risk: The remote CLI installer and hosted connector implementation were not inspected by the security review.

Mitigation: Verify the CLI installer separately and review its automatic skill synchronization behavior before installation or use.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Okta](https://www.okta.com/)
- [Okta Management API documentation](https://developer.okta.com/docs/api/openapi/okta-management/management/tags/user/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, API Calls]

**Output Format:** [Markdown with shell commands and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned Okta data depends on the selected action.]

## Skill Version(s):

1.0.5 (source: ClawHub release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
