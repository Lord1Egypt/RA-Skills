## Description:

Write MIND source for deterministic agentic systems, with canonical MIC@3 artifacts, supported native ELF compilation, and feature-aware guidance for MIND v0.10.2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[star-ga](https://clawhub.ai/user/star-ga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, port, and explain .mind programs for deterministic agentic or numerical systems while staying within the documented MIND v0.10.2 compiler capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated MIND examples can be incompatible with a user's exact compiler version, cargo features, or target toolchain.

Mitigation: Compile and test generated code with the intended compiler version and explicitly requested feature set before deployment.

Risk: The skill covers documented MIND v0.10.2 capabilities and may need to describe requested constructs as unsupported or migration-dependent.

Mitigation: Treat unsupported constructs, autodiff limits, native subset limits, and signing status as explicit compatibility boundaries in generated guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/star-ga/skills/mind)
- [Publisher profile](https://clawhub.ai/user/star-ga)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with MIND code fences and optional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code should be compiled and tested with the user's intended MIND compiler version and selected cargo features.]

## Skill Version(s):

1.0.4 (source: server evidence, skill metadata, README, metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
