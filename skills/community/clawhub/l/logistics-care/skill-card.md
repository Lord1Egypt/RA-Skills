## Description:

电商物流延迟检测与客户安抚短信发送技能，可导入订单 CSV 或手动输入运单号，查询物流轨迹、检测延迟风险、生成安抚短信，并在确认后通过阿里云或腾讯云短信发送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators use this skill to review order logistics, identify delayed or abnormal shipments, and prepare customer care SMS messages. It supports dry-run previews by default and can send messages through configured SMS providers when the operator chooses send mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Send mode can send customer SMS messages through configured Aliyun or Tencent Cloud credentials.

Mitigation: Use dry-run first and separately review recipients, logistics findings, and message text before enabling send mode.

Risk: The workflow processes customer names, phone numbers, order IDs, tracking numbers, and writes JSON and HTML reports.

Mitigation: Treat generated reports as sensitive customer data, restrict access, and apply retention controls appropriate for customer records.

Risk: The logistics checker can install a Python dependency automatically when requests is missing.

Mitigation: Run it in an environment where package installation is controlled, or preinstall reviewed dependencies before execution.

Risk: SMS and logistics API credentials are required for live integrations.

Mitigation: Store credentials in environment variables or a protected secret store and avoid committing provider keys or local config files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/logistics-care)
- [Publisher Profile](https://clawhub.ai/user/bettermen)
- [Project Homepage](https://github.com/bettermen/logistics-care)
- [API Configuration Reference](references/api_config.md)
- [UAPI Tracking API](https://uapis.cn/api/v1/misc/tracking/query)
- [Aliyun SMS](https://www.aliyun.com/product/sms)
- [Tencent Cloud SMS](https://cloud.tencent.com/product/sms)

## Skill Output:

**Output Type(s):** [text, JSON, HTML, shell commands, configuration guidance]

**Output Format:** [Command-line output plus JSON logistics results, HTML SMS previews, and generated SMS message text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default mode is dry-run preview; send mode can call configured SMS providers and produce per-message send results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
