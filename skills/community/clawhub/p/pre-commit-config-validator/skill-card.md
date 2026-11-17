## Description:

Validate .pre-commit-config.yaml files for structure, repository entries, hook definitions, local hooks, and best practices. 23 rules across 5 categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate pre-commit configuration files for structural errors, repository and hook issues, local hook definitions, and best-practice warnings before committing or releasing code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an executable Python validator.

Mitigation: Review the validator before installation and run it in the intended local workspace with only the configuration files selected for validation.

Risk: The skill does not explicitly declare allowed tools in frontmatter.

Mitigation: Apply normal agent tool restrictions when using the skill and limit execution to local validation commands for pre-commit configuration files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/pre-commit-config-validator)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; validator output can be text, JSON, or summary diagnostics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-specified YAML files and reports diagnostics; --strict treats warnings as errors.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
