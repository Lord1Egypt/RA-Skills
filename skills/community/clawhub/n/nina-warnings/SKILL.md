---
name: NINA Warnings
slug: nina-warnings
description: Read-only access to current German public warnings via the official NINA / warnung.bund.de API. Use when asked about NINA alerts, Bevölkerungswarnungen, civil protection alerts, weather warnings, flood warnings, Katwarn-style warning checks, or whether there are active warnings for a German city, district, or ARS region code.
changelog: v1.1.0 adds district-level ARS normalization, optional warning detail and GeoJSON enrichment, and nationwide source-feed access for mowas, dwd, katwarn, biwapp, lhp, and police.
metadata: {"clawdbot":{"emoji":"W","requires":{"bins":["bash","curl","jq"]},"os":["linux","darwin"]}}
---

# NINA Warnings

Read current public warnings from the official German NINA API.
Lese aktuelle oeffentliche Warnmeldungen ueber die offizielle deutsche NINA-API.

Repository: [openclaw-skill-nina-warnings](https://github.com/wolf128058/openclaw-skill-nina-warnings)

## Scope / Umfang

- Read-only only. Do not modify systems, accounts, settings, or local state.
- Nutze ausschliesslich lesende Zugriffe. Keine Schreiboperationen, keine Konfigurationsaenderungen.
- The published skill is intentionally limited to public warning lookup via `warnung.bund.de`.
- Dieser Skill ist bewusst auf die Abfrage oeffentlicher Warnungen ueber `warnung.bund.de` begrenzt.
- No secrets, auth tokens, or private endpoints are required.
- Es sind keine Zugangsdaten, Tokens oder privaten Endpunkte noetig.

## Runtime

- Requires `bash`, `curl`, and `jq`.
- Benoetigt `bash`, `curl` und `jq`.
- Public API base URL: `https://warnung.bund.de/api31`
- Oeffentliche API-Basis-URL: `https://warnung.bund.de/api31`

## Default Behavior / Standardverhalten

- Accept either a German place/district name or a 12-digit ARS code.
- Akzeptiere entweder einen deutschen Orts-/Kreisnamen oder einen 12-stelligen ARS-Code.
- Normalize ARS values to district level before dashboard requests.
- Normalisiere ARS-Werte vor Dashboard-Abrufen auf Kreisebene.
- Prefer the helper script instead of handcrafted `curl`.
- Bevorzuge das Helper-Skript statt manuellem `curl`.
- If a place name resolves to multiple matches, use the best local cache match and mention ambiguity briefly if needed.
- Wenn ein Ortsname mehrere Treffer hat, nutze den besten lokalen Cache-Treffer und erwaehne Mehrdeutigkeit kurz, falls noetig.

## Quick Use / Schnellstart

```bash
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "110000000000"
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "Berlin" --json
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "110000000000" --details
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh "110000000000" --geojson --json
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-status.sh --source dwd
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Berlin"
```

To find ARS codes for other cities or districts, use:
Um ARS-Codes fuer weitere Staedte oder Landkreise zu finden, nutze:

```bash
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Hamburg"
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Hamburg" --ars-only
~/.openclaw/workspace/skills/nina-warnings/scripts/nina-lookup-ars.sh "Hamburg" --first
```

## Agent Workflow / Agenten-Workflow

1. Resolve the user location to an ARS code with `scripts/nina-lookup-ars.sh` unless the user already provided a 12-digit ARS.
2. Fetch current warnings with `scripts/nina-status.sh`.
3. Add `--details` when the user needs description or instructions.
4. Add `--geojson` when geometry or machine-readable area data is needed.
5. Use `--source <name>` for nationwide feeds like `mowas`, `dwd`, `katwarn`, `biwapp`, `lhp`, or `police`.
6. Summarize the result clearly:
   active warnings, sender, severity, effective time, expiry if present.
7. If there are no warnings, say so plainly.

## Output Guidance / Ausgabehinweise

- Prefer concise summaries over raw JSON unless machine-readable output was requested.
- Bevorzuge knappe Zusammenfassungen statt rohem JSON, ausser explizit angefordert.
- Mention when an ARS was normalized to district level.
- Erwaehne, wenn ein ARS auf Kreisebene normalisiert wurde.
- Mention the resolved region when the user asked for a city or district.
- Nenne die aufgeloeste Region, wenn der User nach einer Stadt oder einem Landkreis gefragt hat.
- If lookup is ambiguous, say which match was used.
- Wenn die Suche mehrdeutig ist, sage kurz, welcher Treffer verwendet wurde.
- Do not overstate certainty beyond the API result.
- Stelle keine groessere Sicherheit dar als die API hergibt.

## Bundled Files / Enthaltene Dateien

- `scripts/nina-status.sh`
  Fetches and formats current warnings for an ARS code or location query.
- `scripts/nina-lookup-ars.sh`
  Resolves German place and district names to ARS candidates using the local cache.
- `references/ars-codes.json`
  Empty cache placeholder. Populate it during setup with installation-specific ARS mappings.

## Notes / Hinweise

- ARS = `Amtlicher Regionalschluessel`, 12 digits.
- The dashboard endpoint returns an array of current warning objects or `[]`.
- `references/ars-codes.json` contains the 16 German state capitals as bundled starter entries.
- Add more cities or districts to `references/ars-codes.json` if you want local lookup beyond the bundled defaults.
- Ergaenze `references/ars-codes.json` um weitere Staedte oder Landkreise, wenn du mehr als die mitgelieferten Standard-Eintraege lokal aufloesen willst.
- This skill is suitable for a conservative ClawHub release because it is public, read-only, and has no credential handling.
