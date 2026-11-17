## Description:

A focused personal finance tool built for Pension. Log entries, review trends, and export reports - all locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Pension to log personal finance notes, review balances and trends, search recent activity, and export local reports from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance notes are stored locally in plaintext under ~/.local/share/pension.

Mitigation: Use the skill only on trusted machines and restrict permissions on the local data directory, especially on shared or backed-up systems.

Risk: Exported CSV, JSON, or text reports may contain sensitive personal finance details.

Mitigation: Review exported files before sharing them and handle CSV files carefully when opening them in spreadsheet software.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain1/skills/pension)
- [Publisher Profile](https://clawhub.ai/user/bytesagain1)
- [BytesAgain Feedback](https://bytesagain.com/feedback/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Command-line text output with optional JSON, CSV, or plain text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and reads local finance logs under ~/.local/share/pension.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
