# outlook-entra

Microsoft Outlook / Office 365 via OAuth 2.0 (device code flow) et Microsoft Graph API.
**Lecture seule** — permissions `Mail.Read`, `Calendars.Read`, `Contacts.Read`.

## Ce que fait ce skill

- **Lire** des emails, événements calendrier, contacts et pièces jointes
- **Rechercher** dans les emails
- Token OAuth chiffré (AES-GCM) avant stockage
- Refresh automatique du token par cron

## Prérequis

- Python 3.8+ (`requests`, `cryptography`, `html2text`)
- App enregistrée sur **Microsoft Entra** avec permissions :
  - `Mail.Read`, `Calendars.Read`, `Contacts.Read`
  - OAuth 2.0 device code flow activé

## Installation

```bash
# 1. Cloner le repo
git clone https://github.com/fredguile/openclaw-skill-outlook-entra.git
cd openclaw-skill-outlook-entra

# 2. Créer l'environnement virtuel (obligatoire)
uv venv .venv
uv pip install html2text requests cryptography

# 3. Créer et remplir la config
cp .env.example .env
# Éditer .env : AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
```

## Première authentification

Le device code flow (RFC 8628) nécessite une intervention utilisateur unique.

```bash
# Lancer le script d'auth
.venv/bin/python scripts/outlook_auth.py
```

Le script va :
1. Demander un device code à Microsoft
2. Afficher un code utilisateur et une URL de vérification

**Étape 2 — S'authentifier :** aller sur **https://login.microsoft.com/device** et entrer le code affiché (délai : 15 min).

Le script poll automatiquement jusqu'à obtention du token.

## Commandes

```bash
# Statut du token
.venv/bin/python scripts/outlook_auth.py --status

# Rafraîchir le token manuellement
.venv/bin/python scripts/outlook_refresh.py

# Lire les derniers messages
.venv/bin/python scripts/outlook_graph.py messages --folder Inbox --top 10

# Détail d'un message (corps complet, Markdown par défaut)
.venv/bin/python scripts/outlook_graph.py message <messageId>

# Détail en HTML brut (pour extraction/collage)
.venv/bin/python scripts/outlook_graph.py message <messageId> --raw

# Pièces jointes d'un message
.venv/bin/python scripts/outlook_graph.py attachments <messageId>

# Télécharger une pièce jointe
.venv/bin/python scripts/outlook_graph.py download <messageId> --attach-id <id> --output /path/to/file

# Dossiers mail
.venv/bin/python scripts/outlook_graph.py folders

# Calendrier
.venv/bin/python scripts/outlook_graph.py events --top 10

# Contacts
.venv/bin/python scripts/outlook_graph.py contacts --top 20

# Rechercher dans les mails
.venv/bin/python scripts/outlook_graph.py search "mot-clé"

# Profil utilisateur
.venv/bin/python scripts/outlook_graph.py profile

# Révoquer et supprimer le token
.venv/bin/python scripts/outlook_auth.py --revoke
```

## Variables d'environnement (.env)

| Variable | Description |
|---|---|
| `AZURE_TENANT_ID` | GUID du tenant Entra |
| `AZURE_CLIENT_ID` | Application (client) ID |
| `AZURE_CLIENT_SECRET` | Client secret |
| `AZURE_REDIRECT_URI` | Redirect URI (device flow : `http://localhost`) |
| `OAUTH_DEVICE_CODE_URL` | Device code endpoint |
| `OAUTH_TOKEN_URL` | Token endpoint |
| `MS_GRAPH_BASE_URL` | Base URL Graph API |
| `TOKEN_FILE` | Chemin du fichier de tokens |
| `TOKEN_FILE_KEY` | Clé de chiffrement (optionnel) |
| `SCOPES_DEVICE_CODE` | Scopes OAuth demandés |
| `REQUEST_TIMEOUT` | Timeout requêtes HTTP |

## Cron — Refresh automatique du token

Le token expire après ~1h. Le script `outlook_refresh.py` le rafraîchit automatiquement.

**Installation (refresh toutes les heures à HH:55) :**

```bash
SKILL_DIR="/home/fred-ghilini/.openclaw/workspace/skills/outlook-entra"
( crontab -l 2>/dev/null | grep -v outlook_refresh; echo "55 * * * * ${SKILL_DIR}/.venv/bin/python ${SKILL_DIR}/scripts/outlook_refresh.py >> ~/.openclaw/outlook_refresh.log 2>&1" ) | crontab -
```

**Vérification :**

```bash
crontab -l | grep outlook_refresh
```

Si le `refresh_token` expire (plusieurs mois d'inactivité) → relancer le flow complet : `.venv/bin/python scripts/outlook_auth.py`

## Chiffrement des tokens

Les tokens sont chiffrés AES-GCM si `TOKEN_FILE_KEY` est défini dans `.env` :

```bash
openssl rand -base64 32
```

## Ressources

- [OAuth 2.0 Device Code Flow — Microsoft](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code)
- [Microsoft Graph — Mail API](https://learn.microsoft.com/en-us/graph/api/user-list-messages)