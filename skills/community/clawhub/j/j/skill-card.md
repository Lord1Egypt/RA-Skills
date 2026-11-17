## Description:

Short alias skill for joining, merging, or combining files, data, or strings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill when they need an agent to propose concise join, concatenate, or merge approaches for files, text, JSON, CSV/TSV, code files, URLs, or parameter lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples that redirect output with > can overwrite existing files if users reuse filenames carelessly.

Mitigation: Review output paths before running merge examples and write to a new filename or backup existing files first.

Risk: The one-letter alias and broad merge examples may be invoked too loosely for unrelated tasks.

Mitigation: Invoke the skill only for explicit join, concatenate, merge, or combine tasks and confirm the files or data sources before proposing commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with inline shell and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces short command-reference guidance; no external tools, services, or credentials are required by the skill itself.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
