## Description:

依托全球企业数据库检索目标公司对应的校友以及离职前员工名单，梳理企业历史人员脉络，挖掘潜在商务联系人并拓展业务合作机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, sales teams, and B2B lead builders use this skill to query alumni and former-colleague relationships from a global company database by person and organization identifiers. It supports talent sourcing, background research, contact-list expansion, and professional relationship analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid third-party API and each alumni-list page can incur a charge.

Mitigation: Require explicit user confirmation before paid queries, pagination requests, key creation, or recharge actions.

Risk: Credential handling is unsafe enough to require review before installation, and the skill stores its API key under the user's home directory.

Mitigation: Check only for key presence in shared transcripts, avoid printing secret values, and protect the credential file with owner-only permissions.

Risk: The release security verdict is suspicious due to credential-handling concerns.

Mitigation: Review the skill before installation and restrict use to environments where the third-party API key and paid account can be managed safely.

## Reference(s):

- [Global Company Alumni List API Reference](references/person-alumni-list-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [UpKuajing Homepage](https://www.upkuajing.com)
- [UpKuajing Developer Platform](https://developer.upkuajing.com/)
- [UpKuajing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with command examples and API response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries require a UPKUAJING_API_KEY and may incur per-request charges.]

## Skill Version(s):

1.0.5 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
