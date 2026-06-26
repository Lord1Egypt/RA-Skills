# 🔍 li_sentry_check - Server-Inspektions-Skill

> Plattformübergreifende Server-Inspektions- und Gesundheits-Check-Skill. SSH-Anmeldung an entfernten Linux-Servern mit Schlüsselauthentifizierung, Ausführung von schreibgeschützten Inspektionsbefehlen und Generierung strukturierter Markdown-Berichte.

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://clawhub.ai/skills/li_sentry_check)
[![Plattformen](https://img.shields.io/badge/plattformen-nanobot%20%7C%20OpenClaw%20%7C%20Hermes-green.svg)]()
[![Lizenz](https://img.shields.io/badge/lizenz-MIT-green.svg)](LICENSE)

## 📋 Übersicht

`li_sentry_check` ist eine plattformübergreifende Server-Inspektions-Skill, die **nanobot**, **OpenClaw** und **Hermes Agent** unterstützt. Sie meldet sich über SSH-Schlüsselauthentifizierung bei entfernten Linux-Servern an, führt schreibgeschützte Inspektionsbefehle aus (CPU, Speicher, Festplatte, Netzwerk, Dienste, Sicherheit) und generiert strukturierte Markdown-Berichte mit automatischer Hervorhebung von Anomalien.

## ✨ Kernfunktionen

| Funktion | Beschreibung |
|----------|--------------|
| 🔐 SSH-Schlüsselauthentifizierung | Nur Schlüsselauthentifizierung, Passwort-Anmeldung deaktiviert, Sicherheit gehärtet |
| 📊 Hardware-Inspektion | CPU, Speicher, Festplatte, Netzwerknutzung |
| 🖥️ Dienst-Inspektion | Wichtiger Dienststatus, Fehlerprotokolle |
| 🛡️ Sicherheitsinspektion | Anomale SSH-Anmeldungen, Firewall-Warnungen, Kernel-Fehler |
| 📝 Strukturierte Berichte | Markdown/JSON-Format, Anomalien priorisiert |
| 🌐 Plattformübergreifend | Unterstützt nanobot, OpenClaw, Hermes |

## 🚀 Schnellstart

### 1. Skill Installieren

```bash
# nanobot
./manage.sh skill install li_sentry_check

# OpenClaw
npx clawhub@latest install li_sentry_check

# Hermes
hermes skill install li_sentry_check
```

### 2. SSH-Schlüssel Konfigurieren

```bash
# Schlüsselpaar generieren
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# Öffentlichen Schlüssel auf den entfernten Server kopieren
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@<SERVER_IP>

# Verbindung testen
ssh -i ~/.ssh/li_sentry_check inspector@<SERVER_IP>
```

### 3. ZielsERVER Konfigurieren

`references/targets.yaml` bearbeiten:

```yaml
targets:
  produktions-web:
    host: IHRE_SERVER_IP
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - nginx
      - docker
      - sshd
```

### 4. Inspektion Ausführen

```bash
# Basisinspektion (Hardware-Ressourcen)
python3 scripts/inspect.py --target produktions-web --checks basic

# Dienst-Inspektion
python3 scripts/inspect.py --target produktions-web --checks services

# Vollständige Inspektion (Basis + Dienste + Sicherheit + Protokolle)
python3 scripts/inspect.py --target produktions-web --checks daily

# JSON-Format-Ausgabe
python3 scripts/inspect.py --target produktions-web --checks daily --format json

# In Datei ausgeben
python3 scripts/inspect.py --target produktions-web --checks daily --output bericht.md
```

## 📖 Inspektions-Check-Gruppen

| Gruppe | Inhalt | Befehle |
|--------|--------|---------|
| `basic` | CPU, Speicher, Festplatte, Netzwerk | 8 |
| `services` | Dienststatus + Fehlerprotokolle (dynamisch) | 3×N |
| `daily` | Vollständige Inspektion (Basis + Dienste + Sicherheit + Protokolle) | 26 |

## 📊 Bericht-Beispiel

```markdown
# 🔍 Server-Inspektionsbericht

- Ziel: produktions-web
- Host: IHRE_SERVER_IP
- Benutzer: inspector
- Checks: daily
- Gestartet: 2026-04-26T09:00:00+00:00
- Gesamtchecks: 26
- ⚠️ Anomalien: 3

## Gesamtstatus: ⚠️ WARNUNG

## ⚠️ Anomalien (Priorität)

### ⚠️ systemd_failed_units
Befehl: `systemctl --failed --no-pager`
Status: OK (enthält Anomalien)

Ausgabe:
```
UNIT          LOAD   ACTIVE SUB    DESCRIPTION
mcelog.service loaded failed failed Machine Check Exception Logging Daemon
```
```

## 🔧 Befehlszeilen-Optionen

| Option | Beschreibung | Standard |
|--------|--------------|----------|
| `--target` | Zielserver-Name (in targets.yaml definiert) | (erforderlich) |
| `--checks` | Check-Gruppe: `basic`, `services`, `daily` | `basic` |
| `--format` | Ausgabeformat: `markdown`, `json` | `markdown` |
| `--output` | In Datei ausgeben (Standard: stdout) | stdout |

## 🌐 Plattformübergreifende Unterstützung

| Plattform | Laufzeit | Script | Befehl |
|-----------|----------|--------|--------|
| **OpenClaw** | Node.js 24+ | `scripts/inspect.mjs` | `node scripts/inspect.mjs --target bogon --checks daily` |
| **NanoBot** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |
| **Hermes** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |

## 📁 Dateistruktur

```
li_sentry_check/
├── SKILL.md                  # Skill-Dokumentation
├── _meta.json                # Skill-Metadaten
├── design.md                 # Design-Dokumentation
├── references/
│   ├── targets.yaml          # ZielsERVER-Konfiguration
│   └── checks.yaml           # Inspektionsbefehls-Whitelist
└── scripts/
    ├── inspect.mjs           # Node.js-Implementierung (OpenClaw)
    └── inspect.py            # Python-Implementierung (NanoBot/Hermes)
```

## 🔒 Sicherheits-Best Practices

- **Schlüsselberechtigungen**: `chmod 600 ~/.ssh/li_sentry_check`
- **Host-Verifizierung**: Für die Produktion `known_hosts` vorab befüllen statt `accept-new` zu verwenden
- **Dienstnamen**: Nur alphanumerisch, Bindestriche, Unterstriche erlaubt (vor Verwendung validiert)
- **Befehls-Whitelist**: `checks.yaml` niemals mit zustandsändernden Befehlen modifizieren
- **Berichts-Handhabung**: Berichte können Systemdaten enthalten — nicht öffentlich teilen

## 🔧 Erweiterungsleitfaden

### Neuen Zielserver Hinzufügen

`references/targets.yaml` bearbeiten:

```yaml
targets:
  datenbank-server:
    host: IHRE_SERVER_IP
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - mysql
      - redis
```

### Neue Check-Gruppe Hinzufügen

`references/checks.yaml` bearbeiten:

```yaml
checks:
  datenbank:
    description: Datenbank-Inspektion
    commands:
      - id: mysql_status
        cmd: "systemctl status mysql --no-pager | sed -n '1,20p'"
        timeoutSec: 10
      - id: mysql_connections
        cmd: "mysql -e 'SHOW STATUS LIKE \"Threads_connected\"' || true"
        timeoutSec: 15
```

## 📝 Versionsverlauf

| Version | Datum | Änderungen |
|---------|-------|------------|
| 0.1.0 | 2026-04-26 | Erstveröffentlichung: Basis-, Dienst- und Vollinspektion |

## 📄 Lizenz

MIT-Lizenz
