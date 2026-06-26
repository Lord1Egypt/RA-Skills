## Description: <br>
使用慧穗云发票识别 API，通过上传发票影像文件（图片、PDF、OFD、ZIP）自动识别发票信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyierle](https://clawhub.ai/user/xiaoyierle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit invoice image, PDF, OFD, or ZIP files to HuiSuiYun and receive structured invoice-recognition results. It is suited for workflows that need extracted invoice fields such as invoice type, number, date, amount, purchaser, seller, and line items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice files and extracted invoice data may contain sensitive business, tax, or personal information. <br>
Mitigation: Install and run the skill only when the user trusts HuiSuiYun with the selected invoice files and the resulting recognition data. <br>
Risk: HSY_AK and HSY_SK credentials can authorize access to the HuiSuiYun API if exposed. <br>
Mitigation: Keep credentials in environment variables, avoid sharing them in chats or logs, and rotate them if exposure is suspected. <br>
Risk: Changing HSY_API_URL can redirect invoice files and credentials away from the documented HuiSuiYun HTTPS endpoint. <br>
Mitigation: Leave HSY_API_URL set to https://huisuiyun.com unless using a trusted internal proxy. <br>
Risk: Running the command with the wrong file path may upload an unintended local file. <br>
Mitigation: Verify the file path before invoking the script. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoyierle/invoice-discern) <br>
- [HuiSuiYun API Endpoint](https://huisuiyun.com) <br>
- [HuiSuiYun Secret Key Management](https://huisuiyun.com/account/conf/secretkey) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON returned by a Python command-line script, with setup guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and HSY_AK/HSY_SK credentials; HSY_API_URL defaults to https://huisuiyun.com and HSY_TYPE defaults to 2.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
