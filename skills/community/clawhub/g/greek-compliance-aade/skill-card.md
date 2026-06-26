## Description: <br>
Greek tax compliance with AADE/TAXIS integration for VAT, payroll, EFKA, municipal taxes, and stamp duty, with human confirmation required for submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Greek accountants, finance teams, and businesses use this skill to prepare VAT returns, payroll calculations, EFKA materials, myDATA records, municipal tax tracking, and audit-ready compliance outputs. When AADE/TAXIS credentials are configured, it supports approved government submissions after human review. <br>

### Deployment Geography for Use: <br>
Greece <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles AADE/TAXIS credentials and sensitive tax, payroll, client, and audit records. <br>
Mitigation: Prepare filings offline when possible, set AADE credentials only for explicit submissions, and protect OPENCLAW_DATA_DIR as sensitive financial data storage. <br>
Risk: Generated filings, calculations, or payment details could be incorrect for a specific business or filing period. <br>
Mitigation: Manually review generated filings and payment details before relying on them, and use the required four-eyes approval workflow before submission. <br>
Risk: A government filing could be submitted before the responsible people intend to submit it. <br>
Mitigation: Require a prepared filing to be separately reviewed and approved by a different approver before any AADE/TAXIS submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/greek-compliance-aade) <br>
- [AADE TAXIS portal](https://www1.aade.gr/taxisnet) <br>
- [AADE myDATA production API](https://mydatapi.aade.gr) <br>
- [EFKA portal](https://www.efka.gov.gr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with XML, JSON, YAML, CSV, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce draft filings, calculations, payment details, audit records, setup steps, and submission guidance; official submissions require human approval.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
