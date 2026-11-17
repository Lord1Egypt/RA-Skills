## Description:

ProxiedMail (proxiedmail.com). Use this skill for ANY ProxiedMail request — reading, creating, and updating data. Whenever a task involves ProxiedMail, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected ProxiedMail account can retrieve received email and manage proxy email bindings. Developers and users can inspect action schemas and run supported read or write operations through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may run downloaded code without separate user approval.

Mitigation: Review and approve CLI installation separately, preferably using a verified release; consider disabling automatic agent-skill synchronization.

Risk: Connecting ProxiedMail lets OOMOL process email requests and manage forwarding bindings.

Mitigation: Review the requested action and data, and confirm the exact payload and effect before creating or updating a binding.

## Reference(s):

- [ProxiedMail](https://proxiedmail.com/)
- [ProxiedMail API documentation](https://docs.proxiedmail.com/docs/intro/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and shell commands with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports reading email and proxy binding data, and creating or updating proxy bindings.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
