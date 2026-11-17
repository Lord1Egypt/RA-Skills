## Description:

View formatted commit history, author stats, and commit frequency patterns. Use when reviewing logs, comparing contributions, or generating repo reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Gitlog to record and review local command-line notes about commit checks, validations, changelog generation, linting, diffs, and release reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores user-provided text in persistent local log files under ~/.local/share/gitlog.

Mitigation: Avoid entering secrets, tokens, private incident details, or sensitive repository notes, and review or delete the local data directory when the logs are no longer needed.

Risk: The release is presented as a Git history tool, while security evidence says it mainly records typed local activity notes.

Mitigation: Use it as a local activity logger and independently verify repository history with trusted Git commands or review tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/gitlog)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance for local CLI use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local log entries and exports as JSON, CSV, or plain text when invoked by the user.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
