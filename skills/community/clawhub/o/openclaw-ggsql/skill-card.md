## Description:

Generate charts from tabular data using ggsql SQL syntax extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanzhidongyzby](https://clawhub.ai/user/fanzhidongyzby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to turn CSV, JSON, or SQL-table data into ggsql visualization queries and static charts without writing Python or R.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local package installs and generated SQL are code the user chooses to run.

Mitigation: Install ggsql tooling only from trusted package sources, pin versions where practical, and review generated SQL and file paths before execution.

Risk: Using the web playground may expose uploaded datasets to an external service.

Mitigation: Avoid uploading sensitive datasets to the playground unless that handling is acceptable; use local CLI execution for confidential data.

Risk: ggsql syntax and behavior may change while the project is in alpha.

Mitigation: Validate important chart queries against the current ggsql documentation or playground before relying on generated output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanzhidongyzby/skills/openclaw-ggsql)
- [ggsql official website](https://ggsql.org)
- [ggsql syntax documentation](https://ggsql.org/syntax/)
- [ggsql gallery](https://ggsql.org/gallery/)
- [ggsql WASM playground](https://ggsql.org/wasm/)
- [ggsql GitHub repository](https://github.com/posit-dev/ggsql)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML, SQL, and shell command blocks; generated chart artifacts are SVG by default and PNG optionally when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces static chart specifications and execution guidance for ggsql; local execution depends on ggsql-cli or an external playground.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
