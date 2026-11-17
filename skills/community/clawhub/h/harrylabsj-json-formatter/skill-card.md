## Description:

Format and validate JSON files with configurable indentation, optional key sorting, stdin or file input, and stdout or file output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to format JSON, validate JSON syntax, normalize indentation, sort keys, and move JSON between files, stdin, stdout, and chosen output paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using --output may replace an existing destination file.

Mitigation: Choose destination paths deliberately, write to a new file when preserving existing content matters, and keep backups for important JSON files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/harrylabsj-json-formatter)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-formatted text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The formatter returns process exit codes for success, invalid JSON, file or permission errors, and other errors.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
