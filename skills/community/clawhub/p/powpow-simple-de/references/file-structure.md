# Dateistruktur

> Nur für Wartung/Fehlerbehebung. Die Laufzeit von SKILL.md erfordert keine Lektüre dieser Datei.

```
powpow-simple-de/
├── SKILL.md                          # Hauptdatei (schlank gehalten; Details in references/)
├── config.json                       # platformUrl + optionaler Unsplash-Key des Nutzers (KEINE Geheimnisse; schreibgeschützt)
├── scripts/
│   ├── doctor.js                     # Erstlauf-Selbstprüfung (node/config/netzwerk/sitzung)
│   ├── login.js                      # username/password → JWT (Passwort wird nie gespeichert, versteckte Eingabe)
│   ├── compose.js                    # BEITRAGS-HTML-ASSEMBLIERUNG IN EINEM BEFEHL (der einzige unterstützte Weg; vollständig lokal)
│   ├── publish.js                    # lokale Bilder hochladen + POST /api/posts als angemeldeter Nutzer
│   ├── verify.js                     # Beitrag per ID über die Plattform-API verifizieren
│   ├── delete-post.js                # eigenen Beitrag löschen (Testbereinigung)
│   ├── geocode.js                    # Ortsname → WGS-84-Kandidaten (Nutzer bestätigt)
│   ├── list-digital-humans.js        # auflisten/suchen mit Gesundheitsfilter
│   ├── match-digital-human.js        # Thema → sortierte gesunde Kandidaten
│   ├── create-digital-human.js       # Karten-Digital-Human erstellen (2 Badges, 30 Tage Ablauf; Avatar: generieren/upload/URL)
│   ├── search-image.js               # Unsplash (eigener Key des Nutzers, optional; löst auch Fotoseiten-Links auf)
│   ├── upload-image.js               # lokales Bild → Plattform-Speicher → öffentliche URL (von publish.js verwendet)
│   └── lib/
│       ├── api-client.js             # Plattform-API-Client (JWT, gepinnte Header)
│       ├── dh-match.js               # gemeinsamer DH-Gesundheitsfilter + Themen-Ranking (Name 3x, Beschreibung 1x, Maskierung von Fachbegriffen)
│       ├── coord-transform.js        # GCJ-02 ↔ WGS-84-Umwandlung (iterativ invers)
│       └── html-formatter.js         # HTML-Komponenten + CJK-aware Wortzählung
└── references/
    ├── changelog.md                  # Versionshistorie (dieses Paket: 1.0.0; geerbt: 5.3 → 5.7.3)
    ├── security.md                   # Sicherheitsarchitektur + Plattform-API-Liste
    ├── screenshots.md                # Produkt-Screenshot-Inventar + externe Links
    └── file-structure.md             # diese Datei
```

Anmerkung: Die Anmelde-Sitzung (`session.json`) wird **niemals ins Skill-Paket
geschrieben**; sie liegt im Statusverzeichnis des Nutzers (`POWPOW_STATE_DIR`,
Standard `~/.powpow/`) und läuft nach ~7 Tagen ab (das Skill hält eine
6-Tage-Marge für die erneute Anmeldung ein).

Die Skripte in diesem Paket sind byte-identisch mit `powpow-simple` v5.7.3 —
nur Dokumentation und Metadaten unterscheiden sich.
