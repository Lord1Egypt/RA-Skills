## Description: <br>
A GDPR-focused compliance aid for checks, DPIA drafting, data-subject rights review, cross-border transfer assessment, and related report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwumit](https://clawhub.ai/user/wwumit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Privacy, compliance, legal operations, and engineering teams use this skill to produce preliminary GDPR checklists, DPIA materials, data-subject rights guidance, transfer assessments, and compliance reports. Outputs should be reviewed by qualified legal counsel or a DPO before business, audit, customer, or regulatory use. <br>

### Deployment Geography for Use: <br>
EU/EEA and UK <br>

## Known Risks and Mitigations: <br>
Risk: The main GDPR checker can generate favorable compliance results without real supporting evidence. <br>
Mitigation: Treat generated pass rates and reports as preliminary and require human legal or DPO review before using them for business, audit, customer, or regulatory purposes. <br>
Risk: Generated reports may include sensitive business or personal-data context supplied by the user. <br>
Mitigation: Run the skill in a virtual environment, pin dependencies, and store generated reports in a protected folder. <br>


## Reference(s): <br>
- [GDPR regulation reference](references/gdpr-regulation.md) <br>
- [Security check and installation guide](SECURITY_CHECK_GUIDE.md) <br>
- [ClawHub skill page](https://clawhub.ai/wwumit/gpdr-compliance) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and writes compliance, DPIA, data-subject-rights, transfer, and security-check reports.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
