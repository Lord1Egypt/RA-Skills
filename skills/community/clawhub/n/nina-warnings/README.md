# NINA Warnings

## Deutsch

`nina-warnings` ist ein schlanker, read-only OpenClaw-Skill fuer aktuelle deutsche Bevoelkerungswarnungen ueber die offizielle NINA-API des BBK unter `warnung.bund.de`.

Repository: [openclaw-skill-nina-warnings](https://github.com/wolf128058/openclaw-skill-nina-warnings)

### Changelog

- `1.1.0`: Normalisiert ARS-Eingaben auf die vom Dashboard erwartete Kreisebene, kann Warnungsdetails und GeoJSON pro Meldung nachladen und unterstuetzt bundesweite Quellenfeeds wie `mowas`, `dwd`, `katwarn`, `biwapp`, `lhp` und `police`.
- `1.0.1`: Unterstuetzt verschachtelte Warnungsfelder aus dem aktuellen NINA-Dashboard-Format, zeigt Detail-Links zu einzelnen Meldungen an und haelt die lokale Ortsauflosung mit dem mitgelieferten Cache-Format kompatibel.

### Zweck

- Aktive Warnungen fuer einen Ort, Landkreis oder einen 12-stelligen ARS-Code abfragen
- Ortsnamen ueber einen beim Setup befuellten lokalen ARS-Cache aufloesen
- Warnungsdetails, GeoJSON und bundesweite Quellenfeeds abrufen
- Ergebnisse menschenlesbar oder als JSON ausgeben

### Voraussetzungen

- `bash`
- `curl`
- `jq`

### Nutzung

```bash
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "Berlin"
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "110000000000"
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "Berlin" --json
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "110000000000" --details
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "110000000000" --geojson --json
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh --source mowas
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Berlin"
```

- `--details` laedt pro Warnung den offiziellen Detail-Endpunkt `/warnings/{identifier}.json` nach
- `--geojson` laedt pro Warnung `/warnings/{identifier}.geojson` nach
- `--source <name>` nutzt statt des regionalen Dashboards einen bundesweiten Feed wie `mowas`, `dwd`, `katwarn`, `biwapp`, `lhp` oder `police`
- ARS-Eingaben werden vor dem Dashboard-Abruf automatisch auf Kreisebene normalisiert

### Eigene ARS-Codes finden

Um den ARS-Code fuer deine Stadt oder deinen Landkreis zu finden, nutze das Lookup-Skript:

```bash
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Berlin"
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Hamburg"
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Hamburg" --ars-only
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Hamburg" --first
```

- `--ars-only` gibt nur die passenden ARS-Codes aus
- `--first` nimmt nur den ersten Treffer
- Die Suche arbeitet ueber den lokalen Cache in `references/ars-codes.json`
- Wenn deine Stadt dort noch nicht enthalten ist, kannst du den Cache um weitere Eintraege erweitern

### Struktur

- `SKILL.md`: agentenorientierte Skill-Anleitung fuer OpenClaw
- `scripts/nina-status.sh`: Warnungen fuer Ort oder ARS abrufen
- `scripts/nina-lookup-ars.sh`: ARS-Codes lokal aufloesen
- `references/ars-codes.json`: mitgelieferter Beispiel-Cache mit den 16 Landeshauptstaedten; kann lokal erweitert werden

## English

`nina-warnings` is a small, read-only OpenClaw skill for current German public warning messages via the official BBK NINA API at `warnung.bund.de`.
The package is intentionally prepared for a conservative ClawHub release: no write operations, no secrets, no local persistence, and only public read access.

Repository: [openclaw-skill-nina-warnings](https://github.com/wolf128058/openclaw-skill-nina-warnings)

### Changelog

- `1.1.0`: Normalizes ARS inputs to the district-level format expected by the dashboard, can enrich warnings with detail and GeoJSON endpoints, and adds nationwide source feeds like `mowas`, `dwd`, `katwarn`, `biwapp`, `lhp`, and `police`.
- `1.0.1`: Supports nested warning fields from the current NINA dashboard format, adds per-warning detail links, and keeps local place lookup compatible with the bundled cache format.

### Purpose

- Check active warnings for a city, district, or 12-digit ARS code
- Resolve place names through a local ARS cache populated during setup
- Fetch warning details, GeoJSON, and nationwide source feeds
- Return either human-readable summaries or raw JSON

### Why it fits `Benign`

- Read-only access to a public API
- No control over devices, accounts, or infrastructure
- No local system modification
- No credential or private endpoint handling

### Requirements

- `bash`
- `curl`
- `jq`

### Usage

```bash
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "Berlin"
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "110000000000"
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "Berlin" --json
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "110000000000" --details
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "110000000000" --geojson --json
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh --source mowas
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Berlin"
```

- `--details` enriches each warning via `/warnings/{identifier}.json`
- `--geojson` enriches each warning via `/warnings/{identifier}.geojson`
- `--source <name>` uses a nationwide source feed such as `mowas`, `dwd`, `katwarn`, `biwapp`, `lhp`, or `police`
- ARS inputs are automatically normalized to district level before dashboard requests

### Finding ARS codes for your city

Use the lookup helper to find the ARS code for your city or district:

```bash
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Berlin"
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Hamburg"
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Hamburg" --ars-only
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Hamburg" --first
```

- `--ars-only` prints only matching ARS codes
- `--first` returns only the first match
- The lookup uses the local cache in `references/ars-codes.json`
- If your city is missing there, extend the cache with additional entries

### Layout

- `SKILL.md`: agent-facing skill instructions for OpenClaw / ClawHub
- `scripts/nina-status.sh`: fetch warnings for a place or ARS
- `scripts/nina-lookup-ars.sh`: resolve ARS candidates locally
- `references/ars-codes.json`: bundled sample cache with the 16 state capitals; extend locally as needed
