## Description:

Provides templates and lifecycle patterns for storage and documentation systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to choose reusable content templates, assign maturity lifecycle stages, and apply consistent storage and naming patterns for knowledge and documentation systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers could activate the skill when storage or template terminology is only incidental.

Mitigation: Review trigger behavior during deployment and narrow activation rules if accidental invocation matters.

Risk: Copied storage examples that write files can become unsafe if callers pass untrusted identifiers or paths.

Mitigation: Validate IDs, constrain paths to expected directories, and review write logic before using example code in production.

Risk: The skill is documentation-only and does not provide a runnable command interface.

Mitigation: Treat outputs as reference guidance and implementation examples rather than executable automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-storage-templates)
- [OpenClaw metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)
- [Template patterns module](modules/template-patterns.md)
- [Lifecycle stages module](modules/lifecycle-stages.md)
- [Storage patterns module](modules/storage-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with YAML, shell, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no hidden execution or data access reported by security evidence.]

## Skill Version(s):

1.9.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
