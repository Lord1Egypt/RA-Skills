## Description:

Monitor Docker container health: running status, CPU/memory usage, restart counts, and available image updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laolaoqi](https://clawhub.ai/user/laolaoqi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check Docker container status, resource usage, restart counts, and image freshness through a single health-report script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to the Docker daemon, which can expose privileged control over containers and host-adjacent resources.

Mitigation: Run it only in trusted Docker contexts and grant Docker socket access only to users or automation that are allowed to inspect and manage local containers.

Risk: The default full report includes image update checks that can contact registries, use registry credentials, consume bandwidth/storage, and change local image cache state through docker pull.

Mitigation: Use --status, --resources, or --restarts for passive checks on sensitive hosts, and run --images only when outbound registry access and local image cache changes are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laolaoqi/skills/laolaoqi-docker-health)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and terminal report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose passive Docker checks or a full report; image update checks can contact registries and modify local Docker image state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
