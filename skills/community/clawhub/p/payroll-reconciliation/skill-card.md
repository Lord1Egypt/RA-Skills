## Description: <br>
Reconcile QuickBooks Online payroll GL accounts against payroll provider reports from Gusto, ADP, and Paychex across payroll, tax, headcount, employee-cost, and change-log views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, accounting, and month-end close teams use this skill to compare payroll provider reports with QuickBooks Online payroll GL activity, review discrepancies, and prepare Excel workbooks for reconciliation, 941 checks, W-2 support, headcount, employee-cost, and change tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payroll reconciliation outputs may affect financial close work, payroll tax review, or public-facing accounting decisions. <br>
Mitigation: Review discrepancies, 941 comparisons, W-2 helper totals, and suggested journal-entry actions with qualified finance staff before posting entries or filing taxes. <br>
Risk: QuickBooks Online access, payroll reports, and cached reconciliation history can include sensitive payroll and employee information. <br>
Mitigation: Install and run the skill only in trusted environments, protect payroll files and QBO credentials, and limit access to authorized maintainers. <br>
Risk: Provider auto-detection and keyword-based GL categorization can produce best-effort results when CSV headers or account names are customized. <br>
Mitigation: Confirm provider detection, validate account mappings, adjust thresholds when needed, and manually review unsupported or generic provider formats. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/payroll-reconciliation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated Excel workbook expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of a payroll reconciliation pipeline that expects payroll CSV inputs and can produce an eight-tab Excel workbook.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
