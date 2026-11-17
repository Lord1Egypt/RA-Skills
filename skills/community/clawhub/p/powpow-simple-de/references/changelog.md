# Changelog — powpow-simple-de

Versionshistorie (zur Laufzeit nicht nötig; nur für Wartung/Fehlerbehebung).

## 1.0.2 — 2026-09-25

Aktualisierung der Store-Listing-Metadaten (nur Metadaten — keine Funktionsänderungen).

- Anzeigename, Themen und Kategorien (communication/lifestyle/creative) auf den Standard der powpow-register-Serie aktualisiert.
- Hinweis: 1.0.1 war lediglich eine storeseitige Änderung (Entfernung von skill-card.md) und erhält hier keinen eigenen Eintrag.

## 1.0.0 — 2026-09-20

Erste Veröffentlichung der deutschen Ausgabe. Fork von `powpow-simple` v5.7.3
mit funktionaler Gleichheit; `scripts/` sind byte-identisch (SHA256-verifiziert).
Nur Dokumentation und Metadaten — null Skript-Änderungen.

- **Anzeigename auf einen funktionalen Titel gesetzt**: „PowPow Simple DE -
  Beiträge & digitale Menschen auf die öffentliche Karte veröffentlichen"
  (analog zum beschreibenden Anzeigenamen des chinesischen Pakets; der
  routingfähige Slug bleibt `powpow-simple-de`).

- **SKILL.md vollständig ins Deutsche übersetzt**: Trigger (deutsche, englische
  und chinesische Formulierungen), Gesprächs-UX (Tonfall-Tabelle,
  Einstiegsvorlagen, „Nächster Schritt"-Block), der komplette 8-Schritt-Workflow,
  Digital-Human-Erstellung, Fehlerbehandlung und alle harten Regeln.
- **Sprachregel ergänzt (harte Regel)**: Das Gespräch folgt immer der Sprache
  des Nutzers — die deutsche Anleitung bedient Nutzer in jeder Sprache.
- **Platzhalter exakt so dokumentiert, wie das Skript sie akzeptiert**:
  `{{dh}}` / `{{数字人}}`, `{{loc}}` / `{{位置}}`, `{{img}}` / `{{图}}` (die
  chinesischen Aliase sind literale Token, die compose.js erkennt — niemals
  neue erfinden).
- **Ehrliche Lokalisierungs-Hinweise ergänzt**: Die Ortssuche und die
  Bibliothek digitaler Menschen der Plattform sind derzeit am stärksten auf
  Chinesisch; das Banner der Vorschauseite und die in den Screenshots gezeigte
  Produkt-UI sind chinesischsprachig.
- **README.md übersetzt**, einschließlich Hinweise für Reviewer
  (reviewer-gerichteter Kontext, zuvor im chinesischen Paket in 5.7.3
  hinzugefügt).
- **references/ übersetzt**: security.md, file-structure.md, screenshots.md.

## Geerbte Historie (von powpow-simple, chinesische Ausgabe)

Dieses Paket erbt das gesamte Verhalten von `powpow-simple` bis v5.7.3.
Wichtige Meilensteine des chinesischen Pakets:

- **5.7.3 — 2026-09-19**: Audit-Rauschreduktion (Fähigkeitsliste in der
  description, security.md-Neufassung, Reviewer-Hinweise, Pfad-Dokumentation
  der Sitzung). Keine Skript-Änderungen.
- **5.7.2 — 2026-09-19**: Falsche Behauptung „Likes beleben Blasen wieder"
  entfernt; Produkt-Screenshots ergänzt (6 Bilder + jsdelivr-Spiegel). Keine
  Skript-Änderungen.
- **5.7.1 — 2026-09-18**: Umgebungsvariable `POWPOW_PASSWORD` umbenannt
  (behebt einen langjährigen „PowWow"-Tippfehler).
- **5.7.0 — 2026-09-18**, **5.6.0 / 5.5.0 — 2026-09-18**, **5.4.1 / 5.4 —
  2026-09-17**, **5.3 — 2026-09-17**: frühere Evolution der Multi-Skript-
  Pipeline (Anmeldung/Sitzungsbehandlung, Hard-Fail-Semantik der
  compose-Platzhalter, Geokodierungs-Degradation, Digital-Human-Erstellung,
  Gesundheitsfilterung). Vollständige Details: `references/changelog.md` des
  chinesischen Pakets.
