## Description:

Reconcile QuickBooks Online payroll GL accounts against payroll provider reports from Gusto, ADP, or Paychex across 12 payroll categories and produce an Excel workbook for discrepancies, Form 941 tax reconciliation, W-2 checks, headcount, per-employee cost, and change logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting and finance teams use this skill during month-end close, quarterly payroll tax review, and W-2 season to compare payroll provider reports with QuickBooks Online payroll GL activity and investigate discrepancies before close or filing review.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Payroll reports, generated workbooks, and the CDC cache may contain sensitive payroll data.

Mitigation: Run only in an environment approved for payroll data, protect generated workbooks and .cache/payroll-reconciliation/{slug}.json, and delete or relocate cache files according to retention policy.

Risk: The workflow requires installing openpyxl, which can introduce dependency supply-chain risk.

Mitigation: Use a dedicated virtual environment and pin openpyxl to a reviewed version before installing.

Risk: Reconciliation outputs could be mistaken for payroll tax preparation or filing advice.

Mitigation: Use outputs for review support and require CPA review before payroll tax preparation or filing decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/payroll-reconciliation)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash command examples and Excel workbook output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an .xlsx reconciliation workbook and a local CDC cache when the referenced pipeline is run.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
