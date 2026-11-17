## Description:

Ajuda usuários a criar uma conta PowPow (Bolha), entrar com um clique e, se desejarem, acompanhar uma assinatura opcional pelo Alipay ou PayPal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Usuários externos que desejam conhecer o PowPow e concluir o registro e login com assistência na conversa. O agente também orienta sobre problemas de cadastro e, quando solicitado, acompanha o pedido e a confirmação de uma assinatura opcional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: O registro assistido processa e-mail, nome de usuário, senha, código de verificação, avatar opcional e token temporário.

Mitigation: Use o fluxo assistido somente com consentimento; escolha o registro manual se preferir e execute a limpeza ao terminar.

Risk: Uma assinatura opcional pode gerar cobrança pelo Alipay ou PayPal.

Mitigation: Confirme a escolha antes de criar um pedido; o usuário conclui o pagamento diretamente no provedor, sem compartilhar credenciais de pagamento com o agente.

## Reference(s):

- [Página da skill no ClawHub](https://clawhub.ai/durenzidu/skills/powpow-register-pt)
- [Site do PowPow](https://global.powpow.online)
- [Fluxo de registro](references/registration-flow.md)
- [Fluxo de pagamento e ativação](references/payment-and-activation.md)
- [Fluxo assistido pelo agente](references/agent-flow.md)

## Skill Output:

**Output Type(s):** [Orientação, Texto, Links de login e pagamento]

**Output Format:** [Texto de conversa com links e instruções em Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pode apresentar capturas de tela e informar o estado do registro ou da assinatura.]

## Skill Version(s):

2.2.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
