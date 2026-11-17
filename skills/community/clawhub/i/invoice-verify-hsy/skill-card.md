## Description:

使用慧穗云发票查验 API，根据发票代码、号码、日期和金额等信息查询发票详情。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyierle](https://clawhub.ai/user/xiaoyierle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit invoice details to HuiSuiYun's invoice verification API and summarize validation status and key invoice fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice details and credentials may be sent to an unintended endpoint if HSY_API_URL is changed.

Mitigation: Leave HSY_API_URL unset or pin it to the intended HTTPS HuiSuiYun host, and run the skill only where untrusted users cannot modify environment variables.

Risk: Invoice numbers, dates, amounts, check codes, possible tax identifiers, HSY_AK, and HSY_SK are sensitive data handled by a remote service.

Mitigation: Install only if you trust HuiSuiYun and the publisher, protect HSY_AK and HSY_SK as credentials, and avoid running the skill in shared or untrusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoyierle/skills/invoice-verify-hsy)
- [HuiSuiYun invoice check API documentation](https://cdk.huisuiyun.com/docs/%E8%BE%85%E5%8A%A9%E5%8A%9F%E8%83%BD%E6%8E%A5%E5%8F%A3/invoice-check)
- [HuiSuiYun token API documentation](https://cdk.huisuiyun.com/docs/%E8%BE%85%E5%8A%A9%E5%8A%9F%E8%83%BD%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96token-%E5%90%8C%E6%AD%A5)
- [HuiSuiYun secret key management](https://huisuiyun.com/account/conf/secretkey)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses and concise markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus HSY_AK and HSY_SK environment variables; HSY_API_URL defaults to https://huisuiyun.com.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
