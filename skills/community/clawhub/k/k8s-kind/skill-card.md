## Description:

Manage kind (Kubernetes IN Docker) local clusters. Use when creating, testing, or developing with local Kubernetes clusters in Docker containers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to create, configure, inspect, and clean up local kind clusters for Kubernetes development and testing, including image loading and CI/CD workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup instructions leave destructive deletion targets unclear, and cluster deletion can lose cluster-local data.

Mitigation: Before cleanup, require explicit cluster names and verify the installed MCP tool's deletion parameters; do not execute both deletion examples automatically.

Risk: Credentials and host data shared through writable mounts may be exposed.

Mitigation: Keep credentials private and limit writable mounts to directories intended to be shared.

## Reference(s):

- [ClawHub release](https://clawhub.ai/rohitg00/skills/k8s-kind)
- [kind Configuration Reference](references/CONFIGS.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
