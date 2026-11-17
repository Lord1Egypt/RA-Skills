## Description:

依托全球企业资料库查找目标人员或企业对应的同事及内部团队成员，梳理企业内部人脉网络，助力外贸销售和猎头人员拓展业务人脉，实现精准客户触达。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as recruiters, sales teams, and B2B lead builders use this skill to find colleagues and internal team members for a known company and person. It supports relationship mapping, talent and customer research, and identifying additional contacts around a known decision-maker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and read the Upkuajing API key from a local plaintext `.env` file.

Mitigation: Prefer an environment variable or managed secret store, avoid printing the `.env` file, and limit file access to the user account that runs the skill.

Risk: Colleague lookups and paginated follow-up calls can incur fees, and recharge flows may return payment URLs.

Mitigation: Confirm paid actions before execution, check current pricing through the documented price source, and verify any payment URL before opening it.

Risk: Error reports may include request or response details from failed calls.

Mitigation: Send only the minimum context needed for troubleshooting and avoid including raw sensitive request or response data.

## Reference(s):

- [全球企业库同事列表 API 参考](references/person-colleague-list-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)
- [跨境魔方](https://www.upkuajing.com)
- [跨境魔方开放平台](https://developer.upkuajing.com/)
- [开放平台价格说明](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/global-company-person-colleague-zh)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script output can include colleague records, pagination cursor, fee information, and request ID.]

## Skill Version(s):

1.0.5 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
