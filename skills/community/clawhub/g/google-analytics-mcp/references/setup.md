# Google Analytics Skill — Setup Guide

## What you need

- A Google Cloud project
- A Google Analytics 4 property
- `uv` / `uvx` installed (`brew install uv` on macOS)
- `mcporter` installed (`npm i -g mcporter`)

## Step 1 — Enable GCP APIs

In your Google Cloud project, enable:
- [Google Analytics Admin API](https://console.cloud.google.com/apis/library/analyticsadmin.googleapis.com)
- [Google Analytics Data API](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com)

## Step 2 — Create a service account

1. Go to [GCP IAM → Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Create a new service account (e.g. `openclaw-ga-reader`)
3. No GCP roles needed (GA handles access separately)
4. Create a JSON key: **Keys → Add Key → Create new key → JSON**
5. Save the downloaded JSON as:
   ```
   {workspace}/credentials/ga-service-account.json
   ```
   e.g. `~/.openclaw/workspace-relayter/credentials/ga-service-account.json`

## Step 3 — Grant GA access

In Google Analytics 4:
1. **Admin → Property Access Management** (or Account Access Management for account-level access)
2. Click **+** → **Add users**
3. Enter the service account email (looks like `name@project.iam.gserviceaccount.com`)
4. Role: **Viewer** (read-only) is sufficient for all reporting tools

## Step 4 — Optional config file

Create `{workspace}/credentials/ga-config.json`:
```json
{
  "projectId": "your-gcp-project-id",
  "defaultProperty": "properties/123456789"
}
```

`projectId` — your GCP project ID (find it in the GCP console header)
`defaultProperty` — your GA4 property ID (GA4 → Admin → Property Settings → Property ID, prefixed with `properties/`)

## Step 5 — Test

```bash
bash ~/.openclaw/skills/google-analytics/scripts/ga.sh \
  ~/.openclaw/workspace-relayter \
  get_account_summaries
```

Should return a list of GA accounts and properties the service account can access.

## Multiple workspaces

Each workspace gets its own service account pointing to its own GA properties:

```
~/.openclaw/workspace-relayter/credentials/ga-service-account.json  → RELAYTO GA
~/.openclaw/workspace-nickta/credentials/ga-service-account.json    → Ticket-Alerts GA
~/.openclaw/workspace/credentials/ga-service-account.json           → Main / personal GA
```

No shared credentials. No global config changes. Each agent only sees its own GA data.

## Security notes

- Keep `credentials/` out of version control (add to `.gitignore`)
- Service accounts with Viewer role can only read data, never modify GA config
- The `ga-service-account.json` key can be rotated in GCP console at any time
