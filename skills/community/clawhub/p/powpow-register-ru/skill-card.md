## Description:

Помогает русскоязычным пользователям зарегистрироваться в PowPow, войти по ссылке и при желании оформить подписку через официальный сайт.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Внешние русскоязычные пользователи используют помощника для регистрации аккаунта PowPow, устранения проблем со входом и, при необходимости, оформления подписки. Оплату в Alipay или PayPal пользователь подтверждает самостоятельно.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A one-click login link or temporary session state can grant access to the account.

Mitigation: Treat the link and session state as credentials; run cleanup when finished.

Risk: Optional checkout could lead to an unintended payment.

Mitigation: Proceed only when ready to pay, and complete payment personally in Alipay or PayPal.

## Reference(s):

- [Страница навыка в ClawHub](https://clawhub.ai/durenzidu/skills/powpow-register-ru)
- [Официальный сайт PowPow](https://global.powpow.online)
- [Процесс регистрации](artifact/references/registration-flow.md)
- [Оплата и активация](artifact/references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with registration steps and login or checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Automated registration requires Node.js 18 or newer; otherwise the skill provides manual guidance.]

## Skill Version(s):

2.2.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
