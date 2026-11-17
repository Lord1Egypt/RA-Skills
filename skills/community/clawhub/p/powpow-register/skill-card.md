## Description:

陪用户在自己浏览器里完成 PowPop（泡泡）账号注册、邮箱验证与会员订阅，并帮他判断账号是否已经可用。当用户说「注册泡泡」「注册一个 powpow 账号」「泡泡怎么注册」「泡泡怎么付费」「注册收不到验证码」时触发。本技能不含任何脚本，不联网、不索取密码、验证码或支付凭证；注册与付款全部在用户自己的浏览器和官方收银台完成，助手只负责给链接、讲规则、陪排错。不含发帖与创建数字人，不含代码开发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this assistant skill to register for a PowPop account, verify their email, understand optional membership payment, troubleshoot registration issues, and confirm account availability. Users complete registration and payment themselves in their browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passwords, verification codes, or payment details could be shared in conversation instead of being entered on the official pages.

Mitigation: Enter credentials and payment details only in your own browser, and do not send them in chat.

Risk: Users may misunderstand current checkout prices or PayPal renewal terms.

Mitigation: Confirm prices and renewal terms on the checkout page before paying.

Risk: Account information included in the closing account card may appear in the conversation.

Mitigation: Share account details for the closing card only if you are comfortable having them in the conversation.

## Reference(s):

- [PowPop official website](https://global.powpow.online)
- [PowPop registration page](https://global.powpow.online/register?src=clawhub&skill=powpow-register)
- [PowPop subscription page](https://global.powpow.online/subscription?src=clawhub&skill=powpow-register)
- [Product overview video](https://www.bilibili.com/video/BV1Wu826UEVz/)
- [Registration and verification flow](artifact/references/registration-flow.md)
- [Payment and activation guidance](artifact/references/payment-and-activation.md)
- [Assistant interaction flow](artifact/references/agent-flow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Images]

**Output Format:** [Conversational guidance with links and optional packaged product screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-led browser workflow; no scripts, network requests, or access to user files.]

## Skill Version(s):

2.4.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
