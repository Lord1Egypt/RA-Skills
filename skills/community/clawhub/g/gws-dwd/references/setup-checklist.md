# GWS Skill — Setup Checklist

One-time setup for GCP service account + domain-wide delegation.

## 1. GCP Project

- Select or create a GCP project
- Enable these APIs:
  - Google Vault API
  - Admin SDK API
  - Gmail API
  - Google Drive API
  - Google Calendar API
  - Google Sheets API
  - Google Docs API
  - People API

```bash
gcloud services enable \
  vault.googleapis.com \
  admin.googleapis.com \
  gmail.googleapis.com \
  drive.googleapis.com \
  calendar-json.googleapis.com \
  sheets.googleapis.com \
  docs.googleapis.com \
  people.googleapis.com \
  --project <PROJECT_ID>
```

## 2. Service Account

- GCP Console → IAM & Admin → Service Accounts → Create
- Name it (e.g. `jarvis-gws`)
- No GCP roles needed (only GWS API access via DWD)
- Create a JSON key and download it
- Store at `~/.config/gws/service-account.json`
- `chmod 600 ~/.config/gws/service-account.json`
- Note the **Client ID** (numeric) from the service account details page

## 3. Domain-Wide Delegation

- Google Admin console → Security → Access and data control → API controls
- Manage Domain Wide Delegation → Add new
- Client ID: paste the numeric client ID from step 2
- OAuth scopes (paste as comma-separated):

```
https://www.googleapis.com/auth/ediscovery,https://www.googleapis.com/auth/admin.reports.audit.readonly,https://www.googleapis.com/auth/admin.reports.usage.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly,https://www.googleapis.com/auth/admin.directory.group.readonly,https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/calendar.readonly,https://www.googleapis.com/auth/spreadsheets.readonly,https://www.googleapis.com/auth/documents.readonly,https://www.googleapis.com/auth/contacts.readonly,https://www.googleapis.com/auth/directory.readonly
```

- Click Authorize

## 4. Environment

Set these env vars (or rely on defaults in `auth.py`):

```bash
GWS_SERVICE_ACCOUNT_PATH=~/.config/gws/service-account.json
GWS_ADMIN_EMAIL=admin@yourdomain.com
GWS_DOMAIN=yourdomain.com
```

## 5. Dependencies

```bash
pip3 install google-auth google-auth-httplib2 google-api-python-client
```

## 6. Test

```bash
cd scripts/
python3 auth.py vault  # Should return {"status": "ok"}
```

## Google Workspace License Requirements

- **Vault API** requires Business Plus, Enterprise, or Vault add-on license
- All other APIs work with any Google Workspace tier
