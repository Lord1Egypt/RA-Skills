## Description:

批量检测手机号是否空号、实号、沉默号或风险号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check batches of mobile phone numbers through JisuAPI and group them as real, empty, unknown, or risk numbers. It is suited for contact-list quality checks where the user has authority to process the submitted phone numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checked phone numbers are personal data sent to a third-party JisuAPI service under the user's API key.

Mitigation: Use only with permission to process the numbers, avoid unnecessary bulk checks, and review the provider's privacy and retention terms before using customer or regulated data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/mobileempty)
- [JisuAPI Mobile Empty API Documentation](https://www.jisuapi.com/api/mobileempty/)
- [JisuAPI Provider Site](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON returned by a Python CLI, with optional markdown summaries or grouped lists for users]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; accepts a comma-separated mobiles string with up to 100 phone numbers.]

## Skill Version(s):

1.0.2 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
