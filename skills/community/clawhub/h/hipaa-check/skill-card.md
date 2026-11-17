## Description:

HIPAA Check runs a bilingual 12-item HIPAA privacy, security, and breach-notification compliance check and produces local reports from previewed or cloud-scored answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and compliance teams use this skill to collect HIPAA control answers, submit scored runs to the CQDev cloud compliance engine, and generate text, JSON, or HTML compliance reports. It is suited for preliminary self-assessment and does not replace legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scored checks send HIPAA compliance answers to compliancehub.cn.

Mitigation: Use preview mode first and run scored checks only when sending those answers to the cloud service is acceptable.

Risk: The security assessment flags redirect and HTML-report hardening gaps.

Mitigation: Confirm the destination is compliancehub.cn, avoid opening unexpected HTML reports from cloud responses, and review hardening before broad deployment.

Risk: The skill can use an API key and stores optional local key or anonymous trial identifiers.

Mitigation: Treat the API key as a credential, prefer environment-based secrets where appropriate, and keep any local key file private with 0600 permissions.

## Reference(s):

- [HIPAA Check ClawHub Listing](https://clawhub.ai/wwumit/skills/hipaa-check)
- [ComplianceHub Cloud Scoring Service](https://compliancehub.cn)
- [ComplianceHub Account and API Key Page](https://compliancehub.cn/account.html?skill=hipaa-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text, JSON, or HTML reports with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scored runs send answers to compliancehub.cn; preview mode lists check items without sending answers.]

## Skill Version(s):

1.1.3 (source: evidence release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
