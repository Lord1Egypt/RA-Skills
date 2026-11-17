## Description:

Move or rename files and directories for file organization, relocation, and renaming operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to move or rename local files and directories during organization, relocation, and cleanup tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move, rename, overwrite, or relocate local files when used.

Mitigation: Review source and destination paths before execution, especially when moving important files or writing into existing directories.

Risk: The documentation lists interactive, force, and verbose options that are not implemented by the bundled script.

Mitigation: Use the script as a two-argument source-to-destination move helper unless the options are separately implemented and reviewed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in real local filesystem moves or renames when the generated command is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
