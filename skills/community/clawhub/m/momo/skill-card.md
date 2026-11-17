## Description:

Momo namespace for Netsnek e.U. time tracking and invoicing tool for freelancers. Logs work hours, generates timesheets, creates invoices, and tracks payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

External freelancers use momo to log work hours, generate timesheet reports, create invoices from recorded time, and track payment status for client billing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests local command execution permission for its timesheet script.

Mitigation: Install only when local execution is acceptable, and review the script before use.

Risk: Generated invoices or reports may be incorrect or incomplete in this early/stub implementation.

Mitigation: Review generated invoices and reports against source work records before using them for client billing.

Risk: Future versions could expand file changes or external actions beyond the inspected artifact behavior.

Mitigation: Confirm each future version still limits local changes and external actions to what you intend before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kleberbaum/skills/momo)
- [Publisher Profile](https://clawhub.ai/user/kleberbaum)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local command execution permission on Linux; generated reports and invoices should be reviewed before client billing.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
