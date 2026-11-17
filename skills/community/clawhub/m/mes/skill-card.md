## Description:

Manufacturing execution system tracker

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams can use this skill to manage a simple local manufacturing execution tracker through shell commands for status, entries, search, export, statistics, and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently remove stored records by line number.

Mitigation: Review intended delete behavior before use, keep backups of ~/.mes/data.jsonl, and avoid delegating remove commands without human confirmation.

Risk: The security evidence flags unsafe shell/data handling for untrusted config or entry text.

Mitigation: Use only trusted input until shell quoting, JSON/CSV encoding, and deletion safeguards are fixed.

Risk: The skill is presented as an MES tool but only implements a local entry tracker.

Mitigation: Treat it as local note tracking, not as a full manufacturing execution system integration.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/mes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and shell command guidance for local CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying script stores JSONL records under ~/.mes by default and can export local data as JSONL or CSV.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
