## Description:

Parse personal finance CSV exports, validate schema, categorize transactions via local rules, and summarize/report income, expenses, merchants, and categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to validate, categorize, summarize, and report on exported bank or credit-card CSVs locally with account masking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional CSV export can overwrite files in user-writable locations.

Mitigation: Choose a fresh, non-sensitive output path and check for existing files before using export.

Risk: CSV rows may contain attacker-controlled spreadsheet formulas or misleading transaction data.

Mitigation: Process only trusted CSV exports and avoid opening generated CSVs in spreadsheet software without reviewing or sanitizing formula-like cells.

Risk: The documented output-path safety claim is stronger than the security evidence supports.

Mitigation: Treat output-path checks as a convenience guard, not as protection against overwrites or unsafe destinations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell command examples; command output is plain text with optional CSV export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline CSV processing; optional categorized CSV export when an explicit output path is provided.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
