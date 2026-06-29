## Description: <br>
Helps agents generate SQL and Python query templates for extracting vital signs, laboratory results, diagnoses, comorbidities, and related ICU data from MIMIC-IV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongfanbeta](https://clawhub.ai/user/yongfanbeta) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, data analysts, and clinical researchers use this skill to draft MIMIC-IV PostgreSQL queries and Python extraction snippets for ICU cohort analysis. Users run generated queries against their own authorized MIMIC-IV database instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MIMIC-IV access is restricted and generated queries may expose sensitive clinical research data. <br>
Mitigation: Use the skill only with authorized MIMIC-IV access, treat query outputs as sensitive data, and scope extracts to the minimum patients, columns, and time ranges needed. <br>
Risk: Generated Python examples may require database credentials to run. <br>
Mitigation: Use read-only or least-privilege database accounts where practical and avoid hardcoding real passwords in generated scripts. <br>
Risk: Generated SQL or Python templates may need adaptation for a local MIMIC-IV deployment or study design. <br>
Mitigation: Review table names, item IDs, filters, time windows, and cohort logic before running queries or using outputs in analysis. <br>


## Reference(s): <br>
- [MIMIC-IV Database Schema Reference](references/schema.md) <br>
- [MIMIC-IV Vital Signs Queries](references/vital_signs.md) <br>
- [MIMIC-IV Laboratory Queries](references/labs.md) <br>
- [MIMIC-IV Diagnoses and Comorbidities Queries](references/diagnoses.md) <br>
- [MIMIC-IV Common Query Templates](references/common_queries.md) <br>
- [MIMIC-IV Official Documentation](https://mimic.mit.edu/docs/IV/) <br>
- [MIMIC-IV on PhysioNet](https://physionet.org/content/mimiciv/3.1/) <br>
- [MIMIC Code Repository](https://github.com/MIT-LCP/mimic-code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, SQL, Python, Guidance] <br>
**Output Format:** [Markdown with SQL and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated queries are templates that require authorized database access, user-provided connection details, and review before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
