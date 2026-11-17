## Description:

Generates project scaffolds, API handler templates, and YAML, JSON, or TOML configuration files for Python, JavaScript, and Go projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create starter project layouts, service templates, API handler snippets, and configuration files for early application development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated files may be written outside the intended project folder when output paths are not constrained.

Mitigation: Use explicit trusted output directories, inspect generated paths before running the generator, and add path containment checks before deployment.

Risk: Untrusted API handler names or HTTP method values may produce unsafe Python code.

Mitigation: Use only trusted handler inputs until identifier and string validation are added, and review generated code before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-code-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown or plain text with generated code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated project file contents and relative file paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
