## Description:

Generates low-code module scaffolding for ACM-style systems, including Java backend classes, React frontend pages, and database initialization SQL from a Chinese module name and field specification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjfeilg](https://clawhub.ai/user/hjfeilg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to generate an initial full-stack module codebase for low-code ACM-style applications from simplified Chinese module and field descriptions. The generated Java, React, mapper, service, controller, and SQL outputs should be reviewed and adapted before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to write generated source code and SQL into broad user-selected project paths.

Mitigation: Install only where the agent is limited to intended project directories and review generated file lists and resolved paths before allowing writes.

Risk: Absolute paths, traversal paths, or unintended path overrides could route generated files outside the expected project directories.

Mitigation: Reject unexpected absolute or traversal path overrides before executing file writes.

Risk: Generated SQL may be unsuitable for the target database schema or operational environment.

Mitigation: Inspect generated SQL manually before running it against any database.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hjfeilg/skills/lowcode-module-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/hjfeilg)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [SQL generator documentation](src/documents/sql-generator.md)
- [Velocity template variables](src/documents/template/velocity-variables.md)
- [Template constraints](src/documents/template/template-constraints.md)
- [Form controls](src/documents/form-controls/form-controls.md)
- [Layout documentation](src/documents/layout-types/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated code snippets, SQL, configuration values, and file path recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can direct agents to write generated source code and SQL under user-selected backend and frontend project paths.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
