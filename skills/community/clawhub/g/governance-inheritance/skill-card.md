## Description:

Hierarchical policy inheritance system for OpenClaw agents that enables policies to be defined at organization, team, project, and session levels with automatic inheritance, override rules, and conflict resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aakash2289](https://clawhub.ai/user/aakash2289)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up cascading governance policies for OpenClaw agents, define policy hierarchies, and validate policy conflicts across organization, team, project, and session scopes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent governance files that can affect later agent behavior.

Mitigation: Use it only in a trusted workspace with an explicit, controlled GOVERNANCE_ROOT and review generated policies.yaml files before relying on them.

Risk: Weak path containment and incomplete validation may affect security-sensitive policy data.

Mitigation: Avoid untrusted organization, team, project, and session names; fix path containment and schema validation before using this skill for security enforcement.

## Reference(s):

- [Policy Schema Reference](references/policy-schema.md)
- [Inheritance Algorithm Reference](references/inheritance-algorithm.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files, JSON, Markdown]

**Output Format:** [Markdown guidance with shell commands, YAML policy examples, and JSON validation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create persistent policies.yaml governance files under GOVERNANCE_ROOT and report validation errors or warnings for policy chains.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
