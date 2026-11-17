## Description:

Kadoa (kadoa.com). Use this skill for ANY Kadoa request — searching and reading data. Whenever a task involves Kadoa, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Kadoa account use this skill to list workflows, inspect workflow configuration and status, retrieve extracted records, and export matching workflow data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run downloaded code without a separate approval step; the remote installer and CLI implementation were not verified.

Mitigation: Install a verified CLI release yourself and require approval before running any downloaded installer.

Risk: OOMOL brokers access to the connected Kadoa account, and exports can return signed download links.

Mitigation: Limit the connected account's permissions and protect signed export links.

## Reference(s):

- [Kadoa](https://www.kadoa.com)
- [Kadoa API documentation](https://docs.kadoa.com/api-reference/introduction)
- [oo CLI repository (tool reference)](https://github.com/oomol-lab/oo-cli)
- [Kadoa skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-kadoa)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses and oo CLI shell commands, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include workflow metadata, extracted records, or a temporary signed download URL.]

## Skill Version(s):

1.0.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
