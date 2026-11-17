## Description:

企业工商异常经营信息查询。根据企业全名、注册号或统一社会信用代码查询经营异常名录，返回列入/移出原因、时间、决定机关及当前/历史公示状态。使用场景：用户说"经营异常"、"异常名录"、"这家公司有没有异常"、"列入异常"、"年报未公示"、"工商异常"、"合作审查"、"查一下异常经营"等。通过聚合数据（juhe.cn）API 实时查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check whether a Chinese enterprise appears in abnormal-operation records by company name, registration number, or unified social credit code. It is intended for business review workflows where current and historical public-status details, reasons, dates, and decision authorities need to be summarized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send company identifiers and the Juhe AppKey to Juhe for each lookup.

Mitigation: Use the skill only when that data sharing is acceptable for the review workflow and account terms.

Risk: Passing the AppKey on the command line or storing it in scripts/.env can expose the credential through shell history, process listings, file permissions, or source control.

Mitigation: Prefer JUHE_ENTERPRISE_ABNORMAL_KEY from a protected environment variable or secret manager, and keep any .env file out of source control with restricted permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-enterprise-abnormal)
- [Publisher profile](https://clawhub.ai/user/juhemcp)
- [Juhe Enterprise Abnormal Operation API documentation](https://www.juhe.cn/docs/api/id/841)
- [Juhe data platform](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text guidance with shell command examples and JSON script output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Juhe AppKey configured with JUHE_ENTERPRISE_ABNORMAL_KEY or another documented key source.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
