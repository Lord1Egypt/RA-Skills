## Description: <br>
帮助开发者扫描并修复微信小程序面向境外用户时的账号登录、表单国际化、英文搜索触达、多语言服务和翻译后排版溢出问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit WeChat Mini Program projects for overseas user blockers and receive prioritized remediation guidance for login, forms, search, language routing, and translated UI overflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanner reports may include details from the target Mini Program project. <br>
Mitigation: Run the scanner only against the intended project in a normal development sandbox and review generated reports before sharing them. <br>
Risk: Login and verification examples touch phone numbers, email addresses, SMS providers, and user-facing authentication flows. <br>
Mitigation: Remove example phone-number logging, keep provider keys server-side, add rate limits, use generic error handling, and protect stored user information. <br>
Risk: Language-based UI differences can confuse users if hidden features or changed flows are not clear. <br>
Mitigation: Make language-based UI differences transparent and verify the international experience with end-to-end testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/miniprogram-foreign-user-adaptation) <br>
- [reference.md](reference.md) <br>
- [WeChat Mini Program phone number verification component](https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/getPhoneNumber.html) <br>
- [WeChat Mini Program translation capability](https://developers.weixin.qq.com/community/minihome/article/doc/000222bddd4e70130844a1db66b413) <br>
- [wx.getAppBaseInfo API](https://developers.weixin.qq.com/miniprogram/dev/api/base/system/wx.getAppBaseInfo.html) <br>
- [WeChat Mini Program overseas community](https://developers.weixin.qq.com/community/minihome/mixflow/3721056300659130376) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and optional JSON or Markdown scan reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When the scanner is run, it can create validation/reports/scan-report.md and validation/reports/scan-result.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
