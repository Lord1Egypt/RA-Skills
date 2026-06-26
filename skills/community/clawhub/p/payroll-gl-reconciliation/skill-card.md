## Description: <br>
Reconcile payroll processor reports from Gusto, ADP, Paychex, or Rippling to general ledger journal entries in QuickBooks Online, Xero, or other accounting software, with account mapping, variance detection, and audit-ready workpapers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting and finance teams use this skill during month-end close to reconcile payroll processor exports against general ledger payroll accounts, prepare journal entry proposals, identify variances, and assemble review workpapers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payroll exports and generated workpapers can contain sensitive employee compensation, withholding, benefit, and bank-related data. <br>
Mitigation: Use only in approved agent workspaces for payroll data, keep files in encrypted access-controlled storage, and avoid sharing employee-level registers unless necessary. <br>
Risk: Generated journal entries or variance explanations may be incorrect if account mappings, payroll exports, GL extracts, or tax assumptions are incomplete or stale. <br>
Mitigation: Require an authorized accounting reviewer to approve reconciliations and journal entries before posting to any accounting system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/payroll-gl-reconciliation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/samledger67-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, reconciliation tables, journal entry structures, and workpaper templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed reconciliations and journal-entry workpapers for authorized review before posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
