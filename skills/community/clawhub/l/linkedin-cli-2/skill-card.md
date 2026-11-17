## Description:

Post to LinkedIn using the official API v2. Uses OAuth tokens so only post when explicitly asked or scheduled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xmythril](https://clawhub.ai/user/0xmythril)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to authenticate a LinkedIn CLI, verify account access, and publish or delete LinkedIn posts only after explicit user direction or scheduled execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command fetches unaudited global code for the LinkedIn CLI.

Mitigation: Review and trust the upstream package before installation, and prefer an immutable commit pin or isolated install environment.

Risk: The configured LinkedIn token authorizes publishing and deleting account content.

Mitigation: Protect credential files with restricted permissions and require explicit user confirmation before post, share, or delete actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xmythril/skills/linkedin-cli-2)
- [LinkedIn CLI homepage](https://github.com/0xmythril/linkedin-cli)
- [LinkedIn Developer Apps](https://www.linkedin.com/developers/apps)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cause LinkedIn posting or deletion through the configured CLI only after explicit user confirmation or scheduled execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
