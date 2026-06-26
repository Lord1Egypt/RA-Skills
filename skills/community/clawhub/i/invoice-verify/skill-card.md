## Description: <br>
发票查验技能按票面信息或上传文件查验发票真伪，并返回完整票面信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxt](https://clawhub.ai/user/zxt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, reimbursement, and audit users can use this skill to verify invoice authenticity from invoice fields or supported invoice files. It can also query prior verification records by date range, invoice number, invoice code, invoice type, and status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice details, uploaded invoice files, and the invoice-service API key are sent to skill.quandianfapiao.com. <br>
Mitigation: Use only with data approved for that service, and keep ZXT_API_KEY in a secure secret store or temporary environment variable. <br>
Risk: The artifact guidance asks users to provide an API key in chat and may persist it in shell startup files. <br>
Mitigation: Do not paste production API keys into chat, and avoid adding the key to shell startup files unless the exposure is understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxt/invoice-verify) <br>
- [ZXT invoice skill service](https://skill.quandianfapiao.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown guidance with CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ZXT_API_KEY; file verification supports pdf, ofd, xml, jpg, and png files up to 10 MB.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
