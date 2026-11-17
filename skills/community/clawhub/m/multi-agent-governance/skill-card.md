## Description:

A comprehensive governance system for managing agent roles, responsibilities, handoff policies, and conflict resolution in multi-agent environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terr123123](https://clawhub.ai/user/terr123123)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to define role boundaries, validate handoffs, resolve conflicts, and save reusable governance rules for multi-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Governance checks can fail open and allow agent workflows to bypass intended role boundaries.

Mitigation: Review or fix enforcement logic before relying on allowed or success outputs as authoritative security decisions.

Risk: Handoff identities may be non-canonical or mismatched, weakening policy enforcement.

Mitigation: Canonicalize handoff identities or reject mismatches, and keep configuration file paths explicit and trusted.

Risk: Automated conflict strategies may resolve sensitive workflow disputes without user review.

Mitigation: Use user-first conflict resolution for sensitive workflows.

## Reference(s):

- [Usage Guide](docs/usage-guide.md)
- [API Reference](docs/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/terr123123/skills/multi-agent-governance)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples plus YAML or JSON configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return structured validation results, conflict-resolution outcomes, and governance reports.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
