## Description:

OmniSkill is a universal skill dispatch and execution hub for LLM agents that routes natural-language requests and automation hooks to registered plugins through a local gateway and dispatcher.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elohia](https://clawhub.ai/user/elohia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use OmniSkill to package, register, route, and execute local agent skills or plugins from a single dispatcher. It is intended for workflows where an agent needs to select a sub-skill, invoke it, and return the result as human-readable output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dispatcher can run registered plugin code through unauthenticated routing paths.

Mitigation: Keep the gateway local or otherwise access-controlled, and review and approve each plugin before registration.

Risk: The skill can persistently alter its own instructions or registry-managed skill metadata.

Mitigation: Require human approval for registry changes, sanitize third-party metadata, and review instruction changes before deployment.

Risk: Auto-cloning or auto-installing plugin code can introduce unreviewed dependencies or behavior.

Mitigation: Disable unattended clone or install flows and run security review before executing newly packaged plugins.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elohia/skills/omni-skill)
- [README_EN.md](artifact/README_EN.md)
- [Architecture and deployment](artifact/docs/architecture_and_deployment.md)
- [Specification](artifact/docs/spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON request examples, command snippets, and human-readable plugin results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the registered plugin selected by the dispatcher.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
