## Description:

Ledger provides shell commands for recording, listing, searching, removing, exporting, and summarizing local ledger entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other external users can use Ledger to maintain a simple local text ledger, review recent entries, search records, remove records by line number, export data, and view basic entry counts and storage statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a financial analysis or reporting tool beyond its actual local logging and basic statistics behavior.

Mitigation: Use it only as a basic local text ledger and independently verify any financial calculations, reports, or decisions outside the skill.

Risk: Unsafe shell handling can execute commands if configuration keys or values are attacker-controlled.

Mitigation: Do not pass untrusted configuration input, review commands before execution, and restrict write access to the ledger data directory.

Risk: Ledger records and CSV exports can contain sensitive financial or business information.

Mitigation: Review permissions on ~/.ledger or LEDGER_DIR, avoid storing secrets, and treat exported CSV files as sensitive before opening or sharing them.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/ledger)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output with optional JSONL or CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local ledger data under LEDGER_DIR or ~/.ledger and can export ledger-export.json or ledger-export.csv in the working directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
