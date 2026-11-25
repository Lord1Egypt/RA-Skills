## Description:

Begleitet Nutzer:innen im Chat durch die Registrierung und Anmeldung bei PowPow und erklärt bei Bedarf das optionale Mitgliedschafts-Upgrade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Nutzer:innen, die ein PowPow- bzw. Bubble-Konto einrichten oder Registrierungs- und Aktivierungsprobleme lösen möchten, nutzen den Skill für E-Mail-Verifizierung, Ein-Klick-Login und bei Bedarf ein optionales Abo-Upgrade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan bewertet den Skill als verdächtig mit mittlerer Zuversicht. Der Scan ist unvollständig; außerdem besteht laut Sicherheitszusammenfassung ein mögliches Risiko, dass der PayPal-Plan nicht zum beabsichtigten Preis oder Abrechnungsintervall passt.

Mitigation: Das Skript vor der Nutzung vollständig prüfen und vor einer PayPal-Autorisierung den angezeigten Plan, Preis und Abrechnungszeitraum bestätigen; bei Abweichungen nicht fortfahren.

## Reference(s):

- [Agentenablauf](artifact/references/agent-flow.md)
- [Registrierungsablauf](artifact/references/registration-flow.md)
- [Zahlung und Aktivierung](artifact/references/payment-and-activation.md)
- [PowPow-Website](https://global.powpow.online)
- [Registrierungsseite](https://global.powpow.online/register)
- [Produktvideo](https://www.bilibili.com/video/BV1Wu826UEVz/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational guidance with inline shell commands and registration or login links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [German-language, step-by-step assistance; no code development]

## Skill Version(s):

2.2.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
