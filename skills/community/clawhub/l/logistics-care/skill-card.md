## Description: <br>
为电商卖家和客服运营人员检测物流延迟风险，生成客户安抚短信，并在确认后通过阿里云或腾讯云短信服务发送通知。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers and customer support teams use this skill to import order CSV data or inspect individual tracking numbers, identify delayed or abnormal shipments, preview customer-care SMS text, and optionally send approved messages. It is most appropriate for operational logistics follow-up where users can review recipient data and message content before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes customer phone numbers, order identifiers, tracking numbers, and generated JSON or HTML reports that may contain sensitive customer data. <br>
Mitigation: Treat CSV inputs and generated reports as sensitive, limit access and retention, and avoid sharing output files outside the approved support workflow. <br>
Risk: The skill requires logistics and SMS service credentials, including UAPI, Aliyun, or Tencent Cloud secrets. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid committing configuration files with secrets, and rotate keys after exposure. <br>
Risk: Using send mode can deliver real SMS messages to customers. <br>
Mitigation: Run dry-run first, review recipients and message text, and require an explicit operator decision before using --send. <br>
Risk: Runtime dependency installation can make execution less predictable. <br>
Mitigation: Preinstall and pin required dependencies in the deployment environment instead of allowing ad hoc installation during execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bettermen/logistics-care) <br>
- [Publisher Profile](https://clawhub.ai/user/bettermen) <br>
- [Clawdis Homepage](https://github.com/bettermen/logistics-care) <br>
- [API Configuration Reference](references/api_config.md) <br>
- [UAPI Tracking Query API](https://uapis.cn/api/v1/misc/tracking/query) <br>
- [Aliyun SMS](https://www.aliyun.com/product/sms) <br>
- [Tencent Cloud SMS](https://cloud.tencent.com/product/sms) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, HTML] <br>
**Output Format:** [Markdown guidance with shell commands, JSON logistics and SMS result files, HTML SMS preview reports, and generated SMS text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default dry-run mode previews messages without sending; send mode can call external SMS providers after configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
