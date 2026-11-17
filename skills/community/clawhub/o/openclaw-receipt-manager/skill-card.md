## Description:

Manage personal receipts by extracting data from images, storing records, and providing expense searches and monthly financial summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clinchcc](https://clawhub.ai/user/clinchcc)

### License/Terms of Use:


## Use Case:

External users use this skill to retain recognized receipt images and receipt details locally, then search receipts, review individual records, and generate monthly expense summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt images and extracted receipt details are retained locally on the user's machine.

Mitigation: Install only when local retention is intended, and review or clear the data/receipts folder when long-term storage is not desired.

Risk: Broad receipt and expense triggers may invoke the skill during receipt-adjacent conversations.

Mitigation: Review skill activation and stored outputs when discussing expenses, receipts, invoices, claims, or spending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clinchcc/skills/openclaw-receipt-manager)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores receipt images and SQLite records locally under data/receipts when used.]

## Skill Version(s):

0.1.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
