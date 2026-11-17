# PowPow Simple DE — Beiträge & digitale Menschen auf die öffentliche Karte veröffentlichen

PowPow-Assistent, deutsche Ausgabe (OpenClaw): Verwandle deine Fotos oder dein
Rohmaterial in einen Reisebericht und veröffentliche ihn auf PowPow, oder mache
aus einer Person/Figur einen chatfähigen digitalen Menschen, der auf der
öffentlichen Karte festgepinnt wird.

Dies ist die deutsche Ausgabe von [powpow-simple](https://clawhub.ai/durenzidu/skills/powpow-simple)
(funktionsgleich mit v5.7.3; die Skripte sind byte-identisch).

## Installation

```
openclaw skills install @durenzidu/powpow-simple-de
```

## Voraussetzungen

- Node.js 18+ (Skripte nutzen globales `fetch`, keine Drittanbieter-Abhängigkeiten)
- Ein PowPow-Konto: https://global.powpow.online/register

## Statusverzeichnis

Das Skill-Paket bleibt schreibgeschützt. Anmelde-Tokens und Nutzerkonfiguration liegen in einem Statusverzeichnis:

- Standard: `~/.powpow/`
- Über die Umgebungsvariable `POWPOW_STATE_DIR` überschreibbar

Um die Plattform-URL oder den Unsplash-Key anzupassen, lege eine `config.json` ins
Statusverzeichnis — sie überschreibt die mitgelieferten Standardwerte.

## Nutzungsbeispiele

```
cd <skill-verzeichnis>
node scripts/doctor.js                                   # Selbstprüfung + Sitzungstest
node scripts/login.js <username>                         # Anmeldung (Passwort via stdin, wird nie gespeichert)
node scripts/geocode.js "地坛公园" --limit 5              # Ortsname -> Koordinaten
node scripts/match-digital-human.js "读书 作家" --limit 3  # digitale Menschen matchen
node scripts/compose.js --text-file post.txt --loc "地坛公园" --lng 116.408195 --lat 39.952372 --image @/abs/pfad/cover.jpg --out post-draft.html
node scripts/publish.js post-draft.html                  # veröffentlichen
node scripts/verify.js <post-id>                         # nach der Veröffentlichung prüfen
node scripts/delete-post.js <post-id>                    # löschen (Testbereinigung)
```

Lokale Pfade für `--image` **müssen absolut** sein.

Hinweis: Die Ortssuche und die Bibliothek digitaler Menschen der Plattform sind
derzeit am stärksten auf Chinesisch; nicht-chinesische Nutzer können Namen und
Themen in ihrer Landessprache einfügen.

## Sicherheit

- Keine Plattform-Geheimnisse im Paket; jeder Vorgang läuft über die öffentliche API der Plattform + das eigene JWT des Nutzers.
- Das Passwort wird nur einmal bei der Anmeldung verwendet und nie gespeichert; Tokens laufen nach ~7 Tagen ab.
- Details: `references/security.md`.

## Hinweise für Reviewer (SkillSpector / manuelle Prüfung)

- Dies ist ein **anweisungsbasiertes Skill**: SKILL.md orchestriert eine
  Multi-Skript-Pipeline. Jedes Skript unter `scripts/` ist ein dokumentierter
  Schritt des Veröffentlichungs-Workflows (Anmeldung → Selbstprüfung →
  Geokodierung → Matching → Assemblierung → Veröffentlichung → Verifikation),
  kein unabhängiges verstecktes Werkzeug.
- `delete-post.js` löscht nur den eigenen Beitrag des angemeldeten Nutzers
  (`DELETE /api/posts/{id}`, JWT-beschränkt, serverseitig erzwungen) und ist in
  SKILL.md Schritt 8 zur Testbereinigung dokumentiert. Diese Fähigkeit ist auch
  in der Skill-Beschreibung deklariert.
- Keine Geheimnisse im Paket. `config.json` enthält nur Standardwerte. Das
  Sitzungs-JWT wird ins Statusverzeichnis des Nutzers geschrieben
  (`POWPOW_STATE_DIR`, Standard `~/.powpow/session.json`), niemals ins
  Skill-Paket. Passwörter werden nie persistiert.
- Alle verwendeten Umgebungsvariablen (`POWPOW_STATE_DIR`, `POWPOW_PASSWORD`,
  `UNSPLASH_ACCESS_KEY`) sind optional und im SKILL.md-Frontmatter deklariert
  (`metadata.openclaw.envVars`).
- Dieses Paket ist die deutsche Ausgabe von `powpow-simple`; die Skripte sind
  byte-identisch mit v5.7.3 jenes Pakets (nur Dokumentation und Metadaten
  sind übersetzt).

## Lizenz

MIT-0 (ClawHub-weite Lizenz).

## Links

- Website: https://global.powpow.online
- Karte: https://global.powpow.online/map
- Chinesische Ausgabe: https://clawhub.ai/durenzidu/skills/powpow-simple
- Englische Ausgabe: https://clawhub.ai/durenzidu/skills/powpow-simple-en
