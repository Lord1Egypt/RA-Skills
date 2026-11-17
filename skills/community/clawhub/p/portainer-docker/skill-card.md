## Description:

Control Docker containers and stacks via Portainer API. List containers, start/stop/restart, view logs, and redeploy stacks from git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratiknarola](https://clawhub.ai/user/pratiknarola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect Portainer environments, manage Docker containers, retrieve logs, and redeploy stacks through the Portainer REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start, stop, restart, and redeploy live Docker workloads reachable through the configured Portainer API token.

Mitigation: Use a least-privilege Portainer token, confirm actions before production changes, and limit the token to the intended environments.

Risk: The skill reads Portainer credentials from environment variables or a local credential file.

Mitigation: Store credentials with restrictive file permissions, avoid sharing logs or shell history that may expose tokens, and rotate the token after suspected exposure.

Risk: The API helper uses curl with certificate verification disabled.

Mitigation: Remove curl -k or require a trusted TLS certificate before using the skill against sensitive or production Portainer instances.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pratiknarola/skills/portainer-docker)
- [Portainer](https://portainer.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, PORTAINER_URL, and PORTAINER_API_KEY; commands call a configured Portainer API endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog also lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
