## Description:

帮助微信小程序开发者扫描并修复境外用户在账号登录、表单填写、英文搜索、多语言服务和翻译后排版方面的国际化适配问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate WeChat Mini Program projects for overseas user readiness, prioritize internationalization blockers, and generate practical remediation guidance before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing scanner dependencies in an uncontrolled environment can create normal supply-chain or privilege exposure.

Mitigation: Run the skill in a least-privilege project environment and pin or review npm dependencies with a lockfile before operational use.

Risk: Authentication, phone, email, and locale-routing examples may touch sensitive user data or service credentials when adapted for production.

Mitigation: Apply production privacy controls, encrypt sensitive data, avoid logging personal data, rate-limit verification flows, and keep provider API keys out of frontend code and public repositories.

Risk: Static scanning and overflow prediction can miss project-specific behavior or produce findings that need context.

Mitigation: Review scan-report.md and scan-result.json, validate fixes in the target Mini Program, and complete end-to-end testing before release.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tencent-adm/skills/miniprogram-foreign-user-adaptation)
- [WeChat Mini Program phone number quick verification](https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/getPhoneNumber.html)
- [WeChat Mini Program translation capability](https://developers.weixin.qq.com/community/minihome/article/doc/000222bddd4e70130844a1db66b413)
- [wx.getAppBaseInfo API](https://developers.weixin.qq.com/miniprogram/dev/api/base/system/wx.getAppBaseInfo.html)
- [WeChat Mini Program overseas community](https://developers.weixin.qq.com/community/minihome/mixflow/3721056300659130376)
- [Reference examples](reference.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and optional scan report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled scanner can produce scan-report.md for human review and scan-result.json for structured follow-up.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
