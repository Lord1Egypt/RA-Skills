## Description:

Pomaga użytkownikom założyć konto PowPow, zweryfikować adres e-mail i zalogować się jednym kliknięciem, a na życzenie przejść przez opcjonalną subskrypcję.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Użytkownicy PowPow korzystają z asystenta, aby przejść rejestrację i logowanie w rozmowie, rozwiązać problemy z kodem e-mail lub kontem oraz, jeśli zechcą, rozpocząć subskrypcję Alipay lub PayPal. Bez Node.js asystent może zamiast tego udzielać wskazówek.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration handles passwords, email verification codes, and login tokens.

Mitigation: Use a PowPow-specific password, do not share mailbox access, and run cleanup after registration.

Risk: An optional payment flow may open a checkout page and involve recurring PayPal billing.

Mitigation: Confirm PayPal auto-renewal before authorizing payment, do not share payment-account access, and delete temporary checkout HTML files afterward.

## Reference(s):

- [PowPow — strona główna](https://global.powpow.online)
- [PowPow — rejestracja](https://global.powpow.online/register)
- [PowPow Register — ClawHub](https://clawhub.ai/durenzidu/skills/powpow-register-pl)
- [Przebieg obsługi przez agenta](references/agent-flow.md)
- [Rejestracja i rozwiązywanie problemów](references/registration-flow.md)
- [Płatność i aktywacja](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text guidance, Shell commands, Login links]

**Output Format:** [Conversational text with commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide account status and a one-click login link; optional payment is completed by the user.]

## Skill Version(s):

2.2.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
