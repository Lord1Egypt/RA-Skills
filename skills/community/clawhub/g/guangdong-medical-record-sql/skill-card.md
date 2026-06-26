## Description: <br>
Generates SQL queries and table references for Guangdong medical-record statistics workflows, including outpatient, inpatient, ICD, reporting, quality-control, and custom-query tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangnan](https://clawhub.ai/user/liangnan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hospital information-system analysts and medical-record administrators use this skill to draft SQL for statistics, audits, ICD lookups, workload reporting, and medical-record quality checks against the Guangdong 2012 medical-record database schema. <br>

### Deployment Geography for Use: <br>
China (Guangdong medical-record system environments) <br>

## Known Risks and Mitigations: <br>
Risk: SQL produced with this skill may access patient-identifiable medical-record data. <br>
Mitigation: Use the skill only when authorized, prefer aggregate or de-identified outputs, and avoid unnecessary patient identifiers. <br>
Risk: Generated SQL may be incorrect or unsafe for a local database dialect, schema variant, or production environment. <br>
Mitigation: Review generated SQL before running it and execute it through least-privilege database accounts with appropriate auditing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liangnan/guangdong-medical-record-sql) <br>
- [Publisher profile](https://clawhub.ai/user/liangnan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with SQL code blocks and database table references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated SQL should be reviewed before execution, especially on systems containing patient data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
