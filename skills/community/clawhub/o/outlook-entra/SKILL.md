---
name: outlook-entra
description: |
  Microsoft Outlook via OAuth 2.0 (device code flow) et Microsoft Graph API.
  Lecture seule — Mail.Read, Calendars.Read, Contacts.Read.
metadata:
  author: custom
  version: "2.0"
---

# Outlook Entra — SKILL.md

Microsoft Outlook via OAuth 2.0 (device code flow) et Microsoft Graph API.
**Lecture seule** — seules les permissions `Mail.Read`, `Calendars.Read`, `Contacts.Read` sont utilisées.

## Prérequis

- App enregistrée sur **Entra** (Azure AD) avec permissions :
  - `Mail.Read`, `Calendars.Read`, `Contacts.Read`
  - OAuth 2.0 device code flow activé
- Python 3.8+ avec `requests`, `html2text`, `cryptography`
- **Python 3.8+ avec un `.venv` créé dans le répertoire du skill** (`uv venv .venv && uv pip install html2text requests cryptography`)
- Fichier `.env` configuré (voir `.env.example`)

## Installation

```bash
# Créer l'environnement virtuel (obligatoire)
cd ~/.openclaw/workspace/skills/outlook-entra
uv venv .venv
uv pip install html2text requests cryptography

# Copier et éditer la config
cp .env.example .env
# ⚠️ Remplir client_id, client_secret, tenant_id dans .env
```

## Authentification (Flow)

Le device code flow (RFC 8628) nécessite une intervention utilisateur unique.

### Étape 1 — Lancer le script d'auth

```bash
.venv/bin/python scripts/outlook_auth.py
```

Le script va :
1. Demander un device code à Microsoft
2. Afficher un code utilisateur et une URL de vérification

### Étape 2 — S'authentifier

Aller sur **https://login.microsoft.com/device** et entrer le code affiché.
Délai : 15 minutes maximum.

### Étape 3 — Attendre la confirmation

Le script poll automatiquement le endpoint Microsoft jusqu'à obtention du token.
Une fois confirmé, les tokens sont sauvegardés localement.

### Fonctionnement des tokens

- L'`access_token` expire après ~1h
- Le `refresh_token` permet d'obtenir un nouvel `access_token` sans intervention
- Le refresh est **automatisé par cron** toutes les heures (voir section Cron)
- Si le `refresh_token` expire aussi (plusieurs mois d'inactivité) → relancer le flow complet

---

### Commandes utiles

```bash
# Vérifier le statut du token
.venv/bin/python scripts/outlook_auth.py --status

# Rafraîchir le token manuellement
.venv/bin/python scripts/outlook_refresh.py

# Révoquer et supprimer les tokens
.venv/bin/python scripts/outlook_auth.py --revoke
```

## Commandes (lecture seule)

```bash
# Statut de connexion
.venv/bin/python scripts/outlook_auth.py --status

# Lire les derniers messages
.venv/bin/python scripts/outlook_graph.py messages --folder Inbox --top 10

# Détail d'un message (corps complet, Markdown par défaut)
.venv/bin/python scripts/outlook_graph.py message <messageId>

# Détail en HTML brut (pour extraction/collage)
.venv/bin/python scripts/outlook_graph.py message <messageId> --raw

# Lister les dossiers mail
.venv/bin/python scripts/outlook_graph.py folders

# Pièces jointes d'un message
.venv/bin/python scripts/outlook_graph.py attachments <messageId>

# Télécharger une pièce jointe
.venv/bin/python scripts/outlook_graph.py download <messageId> --attach-id <attachmentId> --output /path/to/file

# Événements calendrier
.venv/bin/python scripts/outlook_graph.py events --top 10

# Contacts
.venv/bin/python scripts/outlook_graph.py contacts --top 20

# Rechercher dans les mails
.venv/bin/python scripts/outlook_graph.py search "mot-clé"

# Profil utilisateur
.venv/bin/python scripts/outlook_graph.py profile
```

## Variables d'environnement (.env)

| Variable                | Description                              | Exemple                                                             |
| ----------------------- | ---------------------------------------- | ------------------------------------------------------------------- |
| `AZURE_TENANT_ID`       | GUID du tenant Entra                     | `52ffb8b9-…`                                                        |
| `AZURE_CLIENT_ID`       | ID de l'app (Application ID)             | `xxxxxxxx-…`                                                        |
| `AZURE_CLIENT_SECRET`   | Secret de l'app                          | `~`                                                                 |
| `AZURE_REDIRECT_URI`    | Redirect URI (device flow : tout fait)   | `http://localhost`                                                  |
| `OAUTH_TOKEN_URL`       | URL token endpoint                       | `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token`      |
| `OAUTH_DEVICE_CODE_URL` | URL device code endpoint                 | `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/devicecode` |
| `MS_GRAPH_BASE_URL`     | Base URL Microsoft Graph                 | `https://graph.microsoft.com/v1.0`                                  |
| `TOKEN_FILE`            | Chemin du fichier de stockage des tokens | `~/.openclaw/outlook_tokens.json`                                   |
| `TOKEN_FILE_KEY`        | Clé de chiffrement (optionnel)           | _(vide par défaut)_                                                 |

## Structure du skill

```
outlook-entra/
├── SKILL.md
├── README.md
├── .env.example
├── .gitignore
├── .venv/                   # Environnement virtuel Python (créé via uv venv)
├── scripts/
│   ├── outlook_auth.py      # OAuth device code flow + status/revoke
│   ├── outlook_graph.py     # Appels Graph API (lecture seule)
│   ├── outlook_refresh.py   # Refresh token automatisé (pour cron)
│   └── outlook_token.py     # Module partagé (lecture/refresh tokens)
└── tests/
    └── test_outlook.py      # Tests unitaires
```

## Notes

- Le **device code flow** (RFC 8628) : l'utilisateur authentifie via `https://microsoft.com/devicelogin`. Une seule fois.
- Les **refresh tokens** sont automatiquement utilisés quand l'access token expire.
- Si `TOKEN_FILE_KEY` est défini, les tokens sont chiffrés AES-GCM avant stockage.
- Les erreurs 401 du Graph API déclenchent un refresh automatique.

## Cron — Refresh automatique du token

Le script `outlook_refresh.py` vérifie si le token expire bientôt et le rafraîchit automatiquement.

**Crontab** — refresh toutes les heures à HH:55 :

```cron
55 * * * * /home/fred-ghilini/.openclaw/workspace/skills/outlook-entra/.venv/bin/python /home/fred-ghilini/.openclaw/workspace/skills/outlook-entra/scripts/outlook_refresh.py >> /home/fred-ghilini/.openclaw/outlook_refresh.log 2>&1
```

**Installation** :

```bash
SKILL_DIR="/home/fred-ghilini/.openclaw/workspace/skills/outlook-entra"
( crontab -l 2>/dev/null | grep -v outlook_refresh; echo "55 * * * * ${SKILL_DIR}/.venv/bin/python ${SKILL_DIR}/scripts/outlook_refresh.py >> ~/.openclaw/outlook_refresh.log 2>&1" ) | crontab -
```

**Vérification** :

```bash
crontab -l | grep outlook_refresh
```

## Ressources

- [OAuth 2.0 Device Code Flow — Microsoft](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code)
- [Microsoft Graph — Mail API](https://learn.microsoft.com/en-us/graph/api/user-list-messages)
- [Microsoft Graph — Calendar API](https://learn.microsoft.com/en-us/graph/api/user-list-events)
