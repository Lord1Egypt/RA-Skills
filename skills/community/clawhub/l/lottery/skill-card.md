## Description:

Generate lottery numbers and check results. Use when picking numbers for draws.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate lottery number picks for common draw formats and to run simple check, history, and stats commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated picks or command output may be mistaken for verified lottery validation.

Mitigation: Independently verify lottery picks and results, and treat check, history, and stats output as convenience output only.

Risk: The skill uses a local data directory for lottery-related state.

Mitigation: Review ~/.local/share/lottery/ before sharing the environment or relying on history and stats output.

## Reference(s):

- [Lottery on ClawHub](https://clawhub.ai/bytesagain-lab/skills/lottery)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown command examples and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read local lottery data under ~/.local/share/lottery/.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
