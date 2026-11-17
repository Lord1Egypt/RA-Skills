## Description:

基于官方违禁词库，覆盖公众号、小红书、抖音三大平台审核标准，支持文案、文件、图片、链接多形式输入，快速输出违禁词标记与上下文替换建议。当接口返回积分不足（code=3210）时，自动唤起支付宝完成充值后继续查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、品牌运营人员与内容审核团队可在发布前检查公众号、小红书或抖音文案，查看命中词及结合语境的替换建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic recharge can turn untrusted payment details into local commands.

Mitigation: Require approval before installing payment helpers and before each recharge; verify payment details and pass payment arguments safely as data.

Risk: API-key setup can expose credentials.

Mitigation: Keep the API key scoped to this integration, never print it, and rotate it if exposed.

Risk: Submitted content may include confidential material sent to RedFox.

Mitigation: Submit confidential material only when authorized to share it with RedFox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/if530770/skills/prohibited-word-query)
- [RedFox API key setup](https://redfox.hk/settings/api-keys?source=clawhub)
- [Alipay recharge workflow](references/alipay-recharge.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-platform check with highlighted terms, contextual replacement suggestions, and an optimized version when needed.]

## Skill Version(s):

1.0.10 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
