## Description:

提供维普、知网和万方论文报告的中文验真步骤，说明官方入口、所需字段及结果核对方法。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zslzxy](https://clawhub.ai/user/zslzxy)

### License/Terms of Use:

MIT-0

## Use Case:

学生、教师及报告接收方可用它识别报告品牌，找到验真页面，并按步骤自行填写字段、核对返回的信息；它不能代替官方验真结果。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A report's embedded link or QR code could lead to an untrusted verification page.

Mitigation: Confirm the current official page before entering identifiers; do not follow unknown links from the report.

Risk: Sharing a complete report, credentials, identifiers or CAPTCHA could expose private information.

Mitigation: Use redacted examples; keep credentials and full reports private, and enter identifiers and CAPTCHAs yourself on the official page.

Risk: A familiar layout or a successful lookup could be mistaken for proof that the paper meets academic requirements.

Mitigation: Cross-check the report's title, subject, type, date and number against the official result; do not treat verification as a quality judgment.

## Reference(s):

- [图文验真教程](references/tutorial.md)
- [验真页面与字段](references/browser-pages.md)
- [验真入口与安全边界](references/contract.md)
- [报告验真统一入口](https://vpcs.cqccjy.cn/pwp/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese step-by-step Markdown with links and illustrated references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Explains field locations and result checks; does not submit verification forms.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
