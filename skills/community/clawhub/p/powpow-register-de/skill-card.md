## Description:

Hilft Nutzer:innen, ein PowPow-Konto im Chat zu registrieren, sich per Ein-Klick-Link anzumelden und bei Bedarf ein optionales Mitgliedschafts-Upgrade abzuschließen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Nutzer:innen lassen sich bei der PowPow-Registrierung, E-Mail-Verifizierung und Anmeldung begleiten. Auf Wunsch unterstützt der Agent auch bei einem Mitgliedschafts-Upgrade über Alipay oder PayPal; die Zahlung schließen Nutzer:innen selbst ab.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registrierung erfordert E-Mail-Adresse, Passwort und Verifizierungscode; vorübergehende Sitzungsdaten bleiben bis zur Bereinigung lokal gespeichert.

Mitigation: Nur für eine gewünschte Kontoerstellung einsetzen, Zugangsdaten und Code vertraulich behandeln und zum Abschluss die temporären Sitzungsdaten bereinigen.

Risk: Ein optionales Mitgliedschafts-Upgrade kann zu einer Zahlung oder einem wiederkehrenden Abonnement führen.

Mitigation: Vor dem Bezahlen das offizielle PowPow-, Alipay- oder PayPal-Ziel prüfen und den Kauf selbst bestätigen.

## Reference(s):

- [PowPow-Skill auf ClawHub](https://clawhub.ai/durenzidu/skills/powpow-register-de)
- [PowPow-Website](https://global.powpow.online)
- [PowPow-Registrierung](https://global.powpow.online/register)
- [Registrierungsablauf](references/registration-flow.md)
- [Zahlung und Aktivierung](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Chat-Nachrichten mit Anmeldelinks und schrittweisen Anweisungen]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Kann eine Kontozusammenfassung und bei Bedarf einen Link zur optionalen Zahlungsseite liefern.]

## Skill Version(s):

2.2.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
