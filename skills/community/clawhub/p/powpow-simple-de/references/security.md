# Sicherheitsarchitektur & Plattform-API

> Nur für Wartung/Fehlerbehebung. Die Laufzeit von SKILL.md erfordert keine Lektüre dieser Datei.

## Warum dieses Skill sicher verteilbar ist

Dieses Skill enthält **keine Plattform-Geheimnisse**:

| Punkt | Garantie |
|---|---|
| Plattform-Geheimnisse | Keine im Paket — jeder Vorgang läuft über die eigene HTTP-API der Plattform |
| Identität | JWT aus einer echten Anmeldung; du kannst nur als du selbst posten |
| Nutzer-Passwort | Wird nie gespeichert; nur einmal im Speicher verwendet, um ein kurzlebiges (~7 Tage) Token zu erhalten |
| Ratenlimits / Moderation | Serverseitig erzwungen (10 Beiträge/Stunde/Nutzer, Inhaltsmoderation) |
| Unsplash-Key | Vom Nutzer angegeben, optional (Bilder sind optional) |

Das Skill liest, schreibt oder liefert niemals Dateien mit Zugangsdaten. Der
einzige Zustand, den es schreibt, ist das eigene Sitzungs-Token des Nutzers,
abgelegt im Statusverzeichnis des Nutzers (siehe unten), niemals im
Skill-Paket.

`config.json` enthält NUR `{ "platformUrl", "unsplashAccessKey"(optional),
"sessionMaxAgeDays", "skillVersion" }`. Niemals Supabase-Keys, Service-Roles
oder Admin-Tokens zu diesem Skill hinzufügen.

### Dateien, die niemals die Maschine des Nutzers verlassen dürfen
- `<POWPOW_STATE_DIR>/session.json` (Standard `~/.powpow/session.json`) — das
  JWT des angemeldeten Nutzers (läuft nach ~7 Tagen automatisch ab). Wird ins
  Statusverzeichnis des Nutzers geschrieben, niemals ins (möglicherweise
  schreibgeschützte) Skill-Paket.

## Verwendete Plattform-API-Endpunkte

- `POST /api/auth/login` — `{step:1, username, password}` → JWT (Cookie `powpow_token`)
- `GET  /api/digital-humans?scope=all&search=...` — digitale Menschen auflisten/suchen (Anmeldung erforderlich)
- `GET  /api/amap/place/text?keywords=...` — Ortsnamensuche (Anmeldung erforderlich;
  liefert GCJ-02, von geocode.js clientseitig nach WGS-84 umgerechnet). Der
  Endpunkt-Pfad ist plattformintern und darf dem Nutzer gegenüber nicht genannt
  werden; in interner Diskussion neutral als Ortssuchdienst bezeichnen (dem
  Nutzer niemals den Namen nennen).
- `POST /api/upload/post-image` — Upload lokaler Bilder (multipart `file`; Anmeldung erforderlich)
- `POST /api/posts` — Beitrag erstellen (Anmeldung erforderlich; Server erzwingt Limits & Moderation)
- `GET  /api/posts/{id}` — einen Beitrag verifizieren
- `DELETE /api/posts/{id}` — eigenen Beitrag löschen (Testbereinigung)
- `POST /api/digital-humans` — digitalen Menschen erstellen (Anmeldung erforderlich;
  verbraucht 2 Badges, läuft nach 30 Tagen ab)
- `POST /api/digital-humans/generate-avatar` — KI-Avatar aus der Persona
  (Anmeldung erforderlich; 8–30 s; benötigt laut Plattform-Design eine Referenzbild-URL)
- `GET  /api/badges/balance?userId=...` — Badge-Guthaben vorab prüfen

Hinweis: Das JWT ist an einen Geräte-Fingerabdruck gebunden (User-Agent + Accept-Language). Der API-Client pinnt diese Header bei der Anmeldung und verwendet sie automatisch wieder. Bei `DEVICE_MISMATCH` oder 401: einfach neu anmelden.
