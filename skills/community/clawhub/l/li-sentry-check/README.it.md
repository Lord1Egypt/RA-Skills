# 🔍 li_sentry_check - Skill di Ispezione Server

> Skill multi-piattaforma per ispezione e health check dei server. Accesso SSH ai server Linux remoti tramite autenticazione a chiave, esecuzione di comandi di ispezione in sola lettura e generazione di report strutturati in Markdown.

[![Versione](https://img.shields.io/badge/versione-0.1.0-blue.svg)](https://clawhub.ai/skills/li_sentry_check)
[![Piattaforme](https://img.shields.io/badge/piattaforme-nanobot%20%7C%20OpenClaw%20%7C%20Hermes-green.svg)]()
[![Licenza](https://img.shields.io/badge/licenza-MIT-green.svg)](LICENSE)

## 📋 Panoramica

`li_sentry_check` è una skill di ispezione server multi-piattaforma che supporta **nanobot**, **OpenClaw** e **Hermes agent**. Si connette ai server Linux remoti tramite autenticazione a chiave SSH, esegue comandi di ispezione in sola lettura (CPU, memoria, disco, rete, servizi, sicurezza) e genera report Markdown strutturati con evidenziazione automatica delle anomalie.

## ✨ Funzionalità Principali

| Funzionalità | Descrizione |
|--------------|-------------|
| 🔐 Autenticazione a Chiave SSH | Solo autenticazione a chiave, accesso con password disabilitato, sicurezza rinforzata |
| 📊 Ispezione Hardware | CPU, memoria, disco, utilizzo della rete |
| 🖥️ Ispezione Servizi | Stato dei servizi chiave, log degli errori |
| 🛡️ Ispezione Sicurezza | Accessi SSH anomali, avvisi firewall, errori del kernel |
| 📝 Report Strutturati | Formato Markdown/JSON, anomalie prioritarie |
| 🌐 Multi-Piattaforma | Supporta nanobot, OpenClaw, Hermes |

## 🚀 Guida Rapida

### 1. Installare la Skill

```bash
# nanobot
./manage.sh skill install li_sentry_check

# OpenClaw
npx clawhub@latest install li_sentry_check

# Hermes
hermes skill install li_sentry_check
```

### 2. Configurare le Chiavi SSH

```bash
# Generare coppia di chiavi
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# Copiare la chiave pubblica sul server remoto
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@<IP_SERVER>

# Testare la connessione
ssh -i ~/.ssh/li_sentry_check inspector@<IP_SERVER>
```

### 3. Configurare i Server Target

Modificare `references/targets.yaml`:

```yaml
targets:
  produzione-web:
    host: IL_TUO_IP_SERVER
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - nginx
      - docker
      - sshd
```

### 4. Eseguire l'Ispezione

```bash
# Ispezione base (risorse hardware)
python3 scripts/inspect.py --target produzione-web --checks basic

# Ispezione servizi
python3 scripts/inspect.py --target produzione-web --checks services

# Ispezione completa (base + servizi + sicurezza + log)
python3 scripts/inspect.py --target produzione-web --checks daily

# Output in formato JSON
python3 scripts/inspect.py --target produzione-web --checks daily --format json

# Output su file
python3 scripts/inspect.py --target produzione-web --checks daily --output report.md
```

## 📖 Gruppi di Verifica Ispezione

| Gruppo | Contenuto | Comandi |
|--------|-----------|---------|
| `basic` | CPU, memoria, disco, rete | 8 |
| `services` | Stato servizi + log errori (dinamico) | 3×N |
| `daily` | Ispezione completa (base + servizi + sicurezza + log) | 26 |

## 📊 Esempio di Report

```markdown
# 🔍 Report Ispezione Server

- Target: produzione-web
- Host: IL_TUO_IP_SERVER
- Utente: inspector
- Verifiche: daily
- Avviato: 2026-04-26T09:00:00+00:00
- Totale verifiche: 26
- ⚠️ Anomalie: 3

## Stato Generale: ⚠️ AVVISO

## ⚠️ Anomalie (Priorità)

### ⚠️ systemd_failed_units
Comando: `systemctl --failed --no-pager`
Stato: OK (contiene anomalie)

Output:
```
UNIT          LOAD   ACTIVE SUB    DESCRIPTION
mcelog.service loaded failed failed Machine Check Exception Logging Daemon
```
```

## 🔧 Opzioni da Riga di Comando

| Opzione | Descrizione | Predefinito |
|---------|-------------|-------------|
| `--target` | Nome server target (definito in targets.yaml) | (obbligatorio) |
| `--checks` | Gruppo di verifica: `basic`, `services`, `daily` | `basic` |
| `--format` | Formato output: `markdown`, `json` | `markdown` |
| `--output` | Output su file (predefinito: stdout) | stdout |

## 🌐 Supporto Multi-Piattaforma

| Piattaforma | Runtime | Script | Comando |
|-------------|---------|--------|---------|
| **OpenClaw** | Node.js 24+ | `scripts/inspect.mjs` | `node scripts/inspect.mjs --target bogon --checks daily` |
| **NanoBot** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |
| **Hermes** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |

## 📁 Struttura dei File

```
li_sentry_check/
├── SKILL.md                  # Documentazione della skill
├── _meta.json                # Metadati della skill
├── design.md                 # Documentazione di design
├── references/
│   ├── targets.yaml          # Configurazione server target
│   └── checks.yaml           # Whitelist comandi di ispezione
└── scripts/
    ├── inspect.mjs           # Implementazione Node.js (OpenClaw)
    └── inspect.py            # Implementazione Python (NanoBot/Hermes)
```

## 🔒 Best Practice di Sicurezza

- **Permessi chiave**: `chmod 600 ~/.ssh/li_sentry_check`
- **Verifica host**: Per la produzione, pre-compilare `known_hosts` invece di usare `accept-new`
- **Nomi servizi**: Solo alfanumerico, trattini, underscore consentiti (validati prima dell'uso)
- **Whitelist comandi**: Non modificare mai `checks.yaml` con comandi che modificano lo stato
- **Gestione report**: I report possono contenere dati di sistema — non condividere pubblicamente

## 🔧 Guida all'Estensione

### Aggiungere un Nuovo Server Target

Modificare `references/targets.yaml`:

```yaml
targets:
  server-database:
    host: IL_TUO_IP_SERVER
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - mysql
      - redis
```

### Aggiungere un Nuovo Gruppo di Verifica

Modificare `references/checks.yaml`:

```yaml
checks:
  database:
    description: Ispezione database
    commands:
      - id: mysql_status
        cmd: "systemctl status mysql --no-pager | sed -n '1,20p'"
        timeoutSec: 10
      - id: mysql_connections
        cmd: "mysql -e 'SHOW STATUS LIKE \"Threads_connected\"' || true"
        timeoutSec: 15
```

## 📝 Cronologia Versioni

| Versione | Data | Modifiche |
|----------|------|-----------|
| 0.1.0 | 2026-04-26 | Versione iniziale: ispezione base, servizi e completa |

## 📄 Licenza

Licenza MIT
