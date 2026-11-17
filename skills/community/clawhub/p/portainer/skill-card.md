## Description:

Control Docker containers and stacks via Portainer API. List containers, start/stop/restart, view logs, and redeploy stacks from git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asteinberger](https://clawhub.ai/user/asteinberger)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and control Docker environments through Portainer without opening the web UI. It supports status checks, environment and container listings, stack inspection, stack redeploys, container start/stop/restart operations, and log retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can stop, restart, or redeploy Docker workloads through Portainer.

Mitigation: Require explicit human confirmation before stop, restart, or redeploy commands and use a least-privilege Portainer token scoped to intended environments.

Risk: The skill can retrieve container logs that may contain secrets or personal data.

Mitigation: Treat logs as sensitive output, limit log retrieval to the minimum needed lines, and avoid sharing logs outside trusted operational channels.

Risk: The skill depends on PORTAINER_API_KEY and may load it from ~/.clawdbot/.env.

Mitigation: Protect ~/.clawdbot/.env with appropriate file permissions and rotate the Portainer token if exposure is suspected.

## Reference(s):

- [ClawHub Portainer skill page](https://clawhub.ai/asteinberger/skills/portainer)
- [Portainer](https://portainer.io/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline bash commands and text or JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, PORTAINER_URL, and PORTAINER_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
