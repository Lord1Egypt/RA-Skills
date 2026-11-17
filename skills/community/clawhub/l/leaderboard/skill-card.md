## Description:

Record scores, rank players, and analyze game stats with terminal leaderboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to record game or challenge scores, inspect recent activity, search logged entries, view summary statistics, and export leaderboard data from a local terminal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Leaderboard entries are stored as local plaintext files under ~/.local/share/leaderboard.

Mitigation: Do not record passwords, tokens, private prompts, or sensitive personal data in leaderboard entries.

Risk: Exported CSV and JSON files may contain values that are not safely escaped.

Mitigation: Review exported files before sharing or importing them into other tools, especially when entries contain commas, quotes, formulas, or untrusted text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/leaderboard)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text terminal output with optional JSON, CSV, or text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores leaderboard entries locally under ~/.local/share/leaderboard and can export accumulated logs.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
