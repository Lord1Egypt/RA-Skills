## Description:

Operate Webvizio through an OOMOL-connected account, including creating and deleting REST Hook subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to manage Webvizio REST Hook subscriptions through an OOMOL-connected account. It provides commands for creating a subscription and deleting one by its Webvizio webhook ID, with confirmation required for state-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup may execute downloaded CLI software whose exact installer and hosted connector implementation have not been verified.

Mitigation: Review and install the CLI separately, inspect its installer, and check any additional agent skills it installs before allowing setup.

Risk: REST Hook subscriptions send event notifications to the selected callback, and deletion removes a subscription.

Mitigation: Approve the callback destination and event before creating a subscription, and confirm the target subscription before deleting it.

## Reference(s):

- [Webvizio on ClawHub](https://clawhub.ai/oomol/skills/oo-webvizio)
- [Webvizio](https://webvizio.com)
- [Webvizio REST Hooks documentation](https://webvizio.com/help-center/rest-hooks/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands and JSON API responses with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses include data and execution metadata; creating or deleting subscriptions requires user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
