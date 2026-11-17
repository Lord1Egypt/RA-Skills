## Description:

Search text files for lines matching a pattern using regular expressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and analysts use this skill to search local text files, logs, source code, and filtered data for lines that match regular-expression patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads files and directories supplied by the user, which can expose local file contents to the running agent session.

Mitigation: Run it only on files or directories that are intended for inspection, and avoid pointing it at sensitive paths.

Risk: Large directory trees, large files, or complex regular expressions can create availability issues.

Mitigation: Limit search scope, avoid huge untrusted directories and complex untrusted regex patterns, and prefer narrower file targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/grep-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text search results with Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output may include matching lines, line numbers, counts, filenames, context lines, or ANSI highlighting depending on selected options.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
