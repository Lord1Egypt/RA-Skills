## Description:

MeshLink 服务发布 helps an agent publish local services to a group intranet through the MeshLink CLI after port checks and explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jadejadelu](https://clawhub.ai/user/jadejadelu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to share a running local service inside a ZTM or Zero Trust Mesh environment. It guides the agent through checking MeshLink agent status, confirming a listening port, selecting a service name, previewing the publish action, and publishing only after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run MeshLink shell commands with insufficient input validation.

Mitigation: Validate ports as integers from 1 to 65535, validate service names against lowercase kebab-case, and invoke meshlink with structured arguments rather than interpolated shell strings.

Risk: The skill depends on an unpinned external MeshLink CLI.

Mitigation: Install and use only a trusted, pinned MeshLink CLI version before enabling the publishing workflow.

Risk: The skill can publish or remove local service entries through MeshLink.

Mitigation: Require the preview step and explicit user confirmation before publishing, and review unpublish requests to avoid modifying the wrong service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jadejadelu/skills/meshlink-publish)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and structured status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MeshLink CLI access and explicit user confirmation before publishing]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
