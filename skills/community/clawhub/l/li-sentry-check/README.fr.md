# 🔍 li_sentry_check - Compétence d'Inspection de Serveurs

> Compétence multi-plateforme d'inspection et de santé des serveurs. Connexion SSH par authentification par clé aux serveurs Linux distants, exécution de commandes d'inspection en lecture seule, et génération de rapports structurés en Markdown.

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://clawhub.ai/skills/li_sentry_check)
[![Plateformes](https://img.shields.io/badge/plateformes-nanobot%20%7C%20OpenClaw%20%7C%20Hermes-green.svg)]()
[![Licence](https://img.shields.io/badge/licence-MIT-green.svg)](LICENSE)

## 📋 Aperçu

`li_sentry_check` est une compétence d'inspection de serveurs multi-plateforme qui prend en charge **nanobot**, **OpenClaw** et **Hermes agent**. Il se connecte aux serveurs Linux distants via l'authentification par clé SSH, exécute des commandes d'inspection en lecture seule (CPU, mémoire, disque, réseau, services, sécurité) et génère des rapports Markdown structurés avec mise en surbrillance automatique des anomalies.

## ✨ Fonctionnalités Principales

| Fonctionnalité | Description |
|----------------|-------------|
| 🔐 Authentification par Clé SSH | Authentification par clé uniquement, connexion par mot de passe désactivée, sécurité renforcée |
| 📊 Inspection Matérielle | CPU, mémoire, disque, utilisation du réseau |
| 🖥️ Inspection des Services | État des services clés, journaux d'erreurs |
| 🛡️ Inspection de Sécurité | Connexions SSH anormales, alertes pare-feu, erreurs noyau |
| 📝 Rapports Structurés | Format Markdown/JSON, anomalies prioritaires |
| 🌐 Multi-Plateforme | Prend en charge nanobot, OpenClaw, Hermes |

## 🚀 Démarrage Rapide

### 1. Installer la Compétence

```bash
# nanobot
./manage.sh skill install li_sentry_check

# OpenClaw
npx clawhub@latest install li_sentry_check

# Hermes
hermes skill install li_sentry_check
```

### 2. Configurer les Clés SSH

```bash
# Générer une paire de clés
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# Copier la clé publique sur le serveur distant
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@<IP_SERVEUR>

# Tester la connexion
ssh -i ~/.ssh/li_sentry_check inspector@<IP_SERVEUR>
```

### 3. Configurer les Serveurs Cibles

Modifier `references/targets.yaml` :

```yaml
targets:
  production-web:
    host: IP_DE_VOTRE_SERVEUR
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - nginx
      - docker
      - sshd
```

### 4. Exécuter l'Inspection

```bash
# Inspection de base (ressources matérielles)
python3 scripts/inspect.py --target production-web --checks basic

# Inspection des services
python3 scripts/inspect.py --target production-web --checks services

# Inspection complète (base + services + sécurité + journaux)
python3 scripts/inspect.py --target production-web --checks daily

# Sortie au format JSON
python3 scripts/inspect.py --target production-web --checks daily --format json

# Sortie dans un fichier
python3 scripts/inspect.py --target production-web --checks daily --output rapport.md
```

## 📖 Groupes de Vérification d'Inspection

| Groupe | Contenu | Commandes |
|--------|---------|-----------|
| `basic` | CPU, mémoire, disque, réseau | 8 |
| `services` | État des services + journaux d'erreurs (dynamique) | 3×N |
| `daily` | Inspection complète (base + services + sécurité + journaux) | 26 |

## 📊 Exemple de Rapport

```markdown
# 🔍 Rapport d'Inspection de Serveur

- Cible : production-web
- Hôte : IP_DE_VOTRE_SERVEUR
- Utilisateur : inspector
- Vérifications : daily
- Démarré : 2026-04-26T09:00:00+00:00
- Total des vérifications : 26
- ⚠️ Anomalies : 3

## État Global : ⚠️ AVERTISSEMENT

## ⚠️ Anomalies (Priorité)

### ⚠️ systemd_failed_units
Commande : `systemctl --failed --no-pager`
État : OK (contient des anomalies)

Sortie :
```
UNIT          LOAD   ACTIVE SUB    DESCRIPTION
mcelog.service loaded failed failed Machine Check Exception Logging Daemon
```
```

## 🔧 Options de Ligne de Commande

| Option | Description | Défaut |
|--------|-------------|--------|
| `--target` | Nom du serveur cible (défini dans targets.yaml) | (requis) |
| `--checks` | Groupe de vérification : `basic`, `services`, `daily` | `basic` |
| `--format` | Format de sortie : `markdown`, `json` | `markdown` |
| `--output` | Sortie dans un fichier (défaut : stdout) | stdout |

## 🌐 Prise en Charge Multi-Plateforme

| Plateforme | Environnement | Script | Commande |
|------------|---------------|--------|----------|
| **OpenClaw** | Node.js 24+ | `scripts/inspect.mjs` | `node scripts/inspect.mjs --target bogon --checks daily` |
| **NanoBot** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |
| **Hermes** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |

## 📁 Structure des Fichiers

```
li_sentry_check/
├── SKILL.md                  # Documentation de la compétence
├── _meta.json                # Métadonnées de la compétence
├── design.md                 # Documentation de conception
├── references/
│   ├── targets.yaml          # Configuration des serveurs cibles
│   └── checks.yaml           # Liste blanche des commandes d'inspection
└── scripts/
    ├── inspect.mjs           # Implémentation Node.js (OpenClaw)
    └── inspect.py            # Implémentation Python (NanoBot/Hermes)
```

## 🔒 Bonnes Pratiques de Sécurité

- **Permissions des clés** : `chmod 600 ~/.ssh/li_sentry_check`
- **Vérification de l'hôte** : Pour la production, pré-remplissez `known_hosts` au lieu d'utiliser `accept-new`
- **Noms de services** : Uniquement alphanumérique, tirets, tirets bas autorisés (validés avant utilisation)
- **Liste blanche des commandes** : Ne jamais modifier `checks.yaml` avec des commandes modifiant l'état
- **Gestion des rapports** : Les rapports peuvent contenir des données système — ne pas partager publiquement

## 🔧 Guide d'Extension

### Ajouter un Nouveau Serveur Cible

Modifier `references/targets.yaml` :

```yaml
targets:
  serveur-base-donnees:
    host: IP_DE_VOTRE_SERVEUR
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - mysql
      - redis
```

### Ajouter un Nouveau Groupe de Vérification

Modifier `references/checks.yaml` :

```yaml
checks:
  base-de-donnees:
    description: Inspection de la base de données
    commands:
      - id: mysql_status
        cmd: "systemctl status mysql --no-pager | sed -n '1,20p'"
        timeoutSec: 10
      - id: mysql_connections
        cmd: "mysql -e 'SHOW STATUS LIKE \"Threads_connected\"' || true"
        timeoutSec: 15
```

## 📝 Historique des Versions

| Version | Date | Modifications |
|---------|------|---------------|
| 0.1.0 | 2026-04-26 | Version initiale : inspection de base, des services et complète |

## 📄 Licence

Licence MIT
