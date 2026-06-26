## Description: <br>
A medical reporting query skill for Oracle and SQL Server healthcare databases, covering outpatient, inpatient, pharmacy, insurance, and operational reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a85012712](https://clawhub.ai/user/a85012712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinic and community hospital staff use this skill to request routine healthcare operations reports, such as outpatient volume, inpatient occupancy, pharmacy inventory, insurance reconciliation, and revenue analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may expose patient, insurance, or other sensitive healthcare data. <br>
Mitigation: Install only in an approved healthcare reporting environment, de-identify sensitive data before display or export, and limit access to authorized users. <br>
Risk: Broad report triggers could lead to unintended database queries or exports. <br>
Mitigation: Use a dedicated read-only database account, restrict schemas and tables, and require explicit user confirmation before any query or export. <br>
Risk: Generated report figures may be incomplete or inconsistent with source systems. <br>
Mitigation: Treat report outputs as reference material and reconcile figures with HIS, ERP, or other authoritative systems before operational use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/a85012712/medical-report-query) <br>
- [Publisher Profile](https://clawhub.ai/user/a85012712) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports, with possible Excel or HTML report formats when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive healthcare data; de-identification and source-system reconciliation are required before displaying, saving, or sharing reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
