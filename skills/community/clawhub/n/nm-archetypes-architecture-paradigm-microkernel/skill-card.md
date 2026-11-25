## Description:

Microkernel architecture with a minimal core and plugins

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software architects use this skill to assess when a microkernel architecture fits and plan its core services, plugin contract, sandboxing, SDK, and release governance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plugins can fail or exceed their intended access if their capabilities and permissions are not constrained.

Mitigation: Define a plugin permission model and run extensions in an isolated sandbox with limited capabilities.

Risk: Core and plugin versions can drift out of compatibility.

Mitigation: Use semantic versioning, publish a compatibility matrix, and provide backward-compatible shims when needed.

Risk: An uncontrolled number of plugins can make ongoing support unsustainable.

Mitigation: Use a formal certification process or marketplace-style review for third-party plugins.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-microkernel)
- [Archetypes project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown]

**Output Format:** [Markdown architecture guidance and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on the system's requirements and plugin model.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
