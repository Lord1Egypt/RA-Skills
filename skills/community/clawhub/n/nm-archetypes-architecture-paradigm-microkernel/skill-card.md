## Description:

Microkernel architecture with a minimal core and plugins

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Software architects and developers use this skill to decide when and how to structure extensible systems around a small core and plugins. It guides plugin contracts, isolation, SDKs, release compatibility, and governance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plugins can expose the core to untrusted code or allow failures to spread when permissions and execution boundaries are unclear.

Mitigation: Define plugin capabilities and permissions, isolate extensions in a sandbox, and validate them through an automated pipeline.

Risk: Core and plugin versions can drift and break compatibility.

Mitigation: Use semantic versioning, publish a compatibility matrix, and provide shims when older plugin APIs need support.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-microkernel)
- [Homepage from skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown architecture guidance with adoption steps, deliverables, risks, and exit criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
