## Description:

A local checker for procurement and payable worksheets that runs 14 built-in checks per object directory and prints one conclusion line per object, with findings citing source files and lines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, accounts payable, finance shared service, and internal control teams use this skill at month-end close, supplier reconciliation, payment approval, accrual cleanup, bidding, and contract-payment checkpoints to run local checks over each object directory and review cited findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a clean result as an audit opinion or proof that payments, contracts, invoices, or accounting treatment are valid.

Mitigation: Review the findings, checks not run, and sub-checks not run, and use qualified business, accounting, legal, or audit review for final decisions.

Risk: The skill processes procurement, payables, contract, invoice, and reimbursement text supplied by the user.

Mitigation: Run it only in an environment approved for those business records; the security evidence reports local execution without network use, file writes, persistence, or hidden privilege behavior.

Risk: Some free-version and member-package checks are explicitly not executed, which can be mistaken for a pass.

Mitigation: Inspect the output fields for checks not run and sub-checks not run before relying on the results.

Risk: Missing or poorly structured input can prevent checks from running or route material to the wrong check.

Mitigation: Provide one object per directory and use the documented section headers or separate files so each of the 14 checks receives the intended material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/procurement-payable-pack-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable stdout report by default, or JSON stdout when run with --json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports checks run, checks not run, sub-checks not run, object-level conclusions, issue counts, and cited findings with source file and line references.]

## Skill Version(s):

1.0.24 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
