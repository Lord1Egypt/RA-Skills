## Description:

Deploy a sovereign LYGO Protocol Stack community node via Docker or docker compose. Builds lygo-node image, starts health API on port 8787, optional Phase 4 worker profile. No secrets; human approval for registry push.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy and check a local LYGO Protocol Stack community node with Docker or a non-Docker setup path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned remote code and an unpinned installer with Docker-level impact.

Mitigation: Use a pinned and reviewed repository commit plus a pinned ClawHub installer version before installation or execution.

Risk: Docker Compose files, setup scripts, mounts, network exposure, or cleanup commands may affect the host environment.

Mitigation: Inspect those files and commands before running the skill, and use an environment where Docker-level access is acceptable.

Risk: The local health API on port 8787 could be exposed beyond the intended machine.

Mitigation: Keep port 8787 bound locally unless TLS and explicit user approval are in place.

## Reference(s):

- [LYGO Protocol Stack repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [LYGO Protocol Stack documentation](https://deepseekoracle.github.io/lygo-protocol-stack/)
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-docker-deploy)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local health, badge, and gossip endpoint checks after deployment.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
