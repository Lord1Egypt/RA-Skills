## Description:

查企业工商基本信息、名称搜索、变更与股东高管等。当用户说：查一下某某公司的注册资本、法人是谁？企业变更记录，或类似工商信息问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query JisuAPI for Chinese enterprise business registration details, name search results, change records, shareholders, and executives. Agents can summarize returned company records for questions about registered capital, legal representatives, addresses, operating status, ownership, and change history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names, registration numbers, credit codes, organization codes, and the configured API key are sent to JisuAPI during lookups.

Mitigation: Use the skill only when your organization permits JisuAPI for these searches, and avoid confidential investigations unless that provider is approved.

Risk: Returned company records may be incomplete, unavailable, rate-limited, or provider-error responses.

Mitigation: Check API error responses and corroborate important business decisions with authoritative records before relying on the output.

## Reference(s):

- [JisuAPI Enterprise Business Information API](https://www.jisuapi.com/api/enterprise/)
- [JisuAPI](https://www.jisuapi.com/)
- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-enterprise)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends lookup terms to JisuAPI.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
