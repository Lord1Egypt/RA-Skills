## Description:

使用慧穗云发票识别 API，通过上传发票影像文件（图片、PDF、OFD、ZIP）自动识别发票信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyierle](https://clawhub.ai/user/xiaoyierle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit authorized invoice image, PDF, OFD, or ZIP files to the Huisuiyun invoice recognition API and summarize returned invoice details such as type, amount, purchaser, and seller.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice files and authentication material may be sent to an API host controlled through the HSY_API_URL environment variable.

Mitigation: Run the skill only in trusted environments, set HSY_API_URL to the trusted HTTPS Huisuiyun service, and prevent untrusted parties from controlling environment variables.

Risk: Invoices can contain sensitive financial, tax, business, or personal data.

Mitigation: Submit only invoices the user is authorized to process and protect HSY_AK and HSY_SK as credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoyierle/skills/invoice-discern)
- [Huisuiyun service](https://huisuiyun.com)
- [Huisuiyun secret key configuration](https://huisuiyun.com/account/conf/secretkey)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON API responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the HSY_AK and HSY_SK environment variables; accepts an invoice file path and optional tax number.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
