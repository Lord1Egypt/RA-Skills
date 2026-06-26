## Description: <br>
基于妙想 (Meixiang) 智能选股 API，按用户提供的指标、行业或板块条件筛选 A 股、港股、美股等股票，返回完整 CSV 数据并提供列说明，避免使用过时的金融信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xpmars](https://clawhub.ai/user/xpmars) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate natural-language stock-screening criteria into Meixiang API requests and return current screening results, CSV data, and column descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screening keywords are sent to an external API provider and may include confidential trading plans or private business information. <br>
Mitigation: Use the skill only when the user intends to use the Meixiang stock-screening service and avoid sensitive or confidential details in screening keywords. <br>
Risk: The skill requires an API key for the Meixiang service. <br>
Mitigation: Use a dedicated, revocable API key stored in MX_APIKEY and rotate or revoke it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xpmars/mx-select-stock) <br>
- [Meixiang stock-screening API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, CSV] <br>
**Output Format:** [Markdown guidance with curl commands, JSON response handling, and optional CSV and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MX_APIKEY and sends screening keywords to an external Meixiang API provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
