## Description:

Automated invoice follow-up sequences that escalate from friendly to firm, track unpaid invoices, log payment interactions, and generate accounts receivable aging reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[audsmith28](https://clawhub.ai/user/audsmith28)

### License/Terms of Use:


## Use Case:

Freelancers, consultants, and small business operators use this skill to configure invoice records, reminder templates, timing rules, and accounts receivable workflows for unpaid invoice follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles payment records and may support outbound collection emails, making incorrect configuration or premature automation sensitive for business relationships.

Mitigation: Review reminder templates, timing rules, account settings, and dry-run behavior before enabling scheduled sends.

Risk: Server security evidence reports incomplete shipped controls and warns not to enable scheduled sending until missing chase, status, and report scripts are available and reviewed.

Mitigation: Limit use to setup and invoice-entry workflows until the missing scripts and safety controls are shipped and assessed.

Risk: Server security evidence identifies a local data-corruption risk from untrusted invoice numbers in jq handling.

Mitigation: Use trusted, simple invoice identifiers and avoid untrusted invoice-number input until the jq handling bug is fixed.

## Reference(s):

- [Invoice Chaser ClawHub Skill Page](https://clawhub.ai/audsmith28/skills/invoice-chaser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog skill and GOG_DEFAULT_ACCOUNT for Gmail-based sending; setup creates local invoice and chase-log JSON files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
