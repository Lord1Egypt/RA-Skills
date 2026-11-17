## Description:

Moses Audit records agent actions in a local SHA-256 hash-chained audit ledger and provides commands to log entries, verify chain integrity, and view recent activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add tamper-evident local audit logging around agent activity, including recording actions, inspecting recent entries, and verifying the ledger chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create broad persistent records of agent activity in a local audit ledger.

Mitigation: Install only when persistent local audit logging is intended, and keep log details limited to action descriptions and outcomes.

Risk: Freeform log detail fields may capture secrets, personal data, private keys, or tokens if users include them.

Mitigation: Do not place secrets or personal data in audit details; sanitize entries before logging.

Risk: The script can mark recovery as needed based on failure, block, decline, or error outcomes.

Mitigation: Review or modify the script so recovery-state changes are opt-in and handled through a separate explicit command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunrisesillneversee/skills/moses-audit)
- [MOSES anchor DOI](https://zenodo.org/records/18792459)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and Python CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes JSONL audit entries to a local ledger path and can include HMAC attestations when MOSES_OPERATOR_SECRET is set.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact openclaw metadata reports 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
