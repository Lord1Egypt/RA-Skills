## Description:

Portainer manages Portainer CE environments and stacks through the Portainer HTTP API, including environment listing, stack deployment and inspection, and raw Docker API proxy commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leventsoft](https://clawhub.ai/user/leventsoft)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure operators use this skill to inspect Portainer environments, deploy or update Docker Compose stacks, remove stacks, and run advanced Docker API operations through Portainer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform powerful infrastructure operations through Portainer, including stack deployment, stack removal, and raw Docker API proxy requests.

Mitigation: Use a least-privilege Portainer API token, restrict which environments the token can manage, and require explicit operator confirmation before destructive or broad Docker actions.

Risk: The security evidence identifies insecure TLS handling.

Mitigation: Use this only in trusted operator contexts and avoid production infrastructure until TLS certificate verification is fixed.

Risk: Raw Docker proxying can bypass higher-level safety boundaries.

Mitigation: Restrict or remove raw Docker proxy access for normal use and prefer narrowly scoped stack and environment operations.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/leventsoft/skills/portainer-skill-openclaw)
- [Publisher profile](https://clawhub.ai/user/leventsoft)
- [Portainer](https://www.portainer.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Portainer API URL and API token in the agent runtime environment.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
