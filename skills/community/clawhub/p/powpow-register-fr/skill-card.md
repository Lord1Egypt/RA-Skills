## Description:

Accompagne l'inscription à PowPow (Bulle), la vérification par e-mail et la connexion en un clic, avec une aide facultative pour souscrire un abonnement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Les utilisateurs de PowPow peuvent demander à leur agent de créer un compte, résoudre les difficultés d'inscription et obtenir un lien de connexion. L'agent peut aussi préparer une commande d'abonnement facultative, mais l'utilisateur effectue lui-même le paiement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: L'agent traite le mot de passe, le code de vérification par e-mail et des jetons de session pendant l'inscription.

Mitigation: Utiliser un mot de passe nouveau et unique, vérifier les liens avant ouverture, demander le nettoyage en fin de parcours ou choisir l'inscription manuelle si l'on ne souhaite pas confier ses identifiants à l'agent.

Risk: Les liens de connexion et les étapes de commande ou d'abonnement peuvent exposer la session ou entraîner un paiement non voulu.

Mitigation: Vérifier que les liens restent sur global.powpow.online ou les pages officielles Alipay/PayPal ; confirmer le choix d'abonnement et effectuer le paiement soi-même sur la caisse officielle.

## Reference(s):

- [Fiche de la compétence sur ClawHub](https://clawhub.ai/durenzidu/skills/powpow-register-fr)
- [Site officiel de PowPow](https://global.powpow.online)
- [Parcours d'inscription](references/registration-flow.md)
- [Parcours pris en charge par l'agent](references/agent-flow.md)
- [Paiement et activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Images]

**Output Format:** [Markdown avec liens de connexion et captures d'écran du produit]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [L'inscription et la préparation d'une commande facultative peuvent être effectuées par l'agent ; un mode guidé est disponible sans Node.js 18 ou plus.]

## Skill Version(s):

2.2.0 (source: frontmatter et version de publication ClawHub)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
