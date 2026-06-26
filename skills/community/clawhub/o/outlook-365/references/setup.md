# Outlook Manual Setup Guide

Use this guide if you prefer manual setup via Azure Portal, or if the automated setup fails.

## Prerequisites

- Microsoft account (Outlook.com, Hotmail, Live, or Microsoft 365)
- Access to [Azure Portal](https://portal.azure.com)
- `jq` installed (`sudo apt install jq`)

## Step 1: Create Azure App Registration

1. Go to https://portal.azure.com
2. Search for **"App registrations"** → Click it
3. Click **"+ New registration"**
4. Configure:
   - **Name:** `Clawdbot-Outlook` (or any name)
   - **Supported account types:** "Accounts in any organizational directory and personal Microsoft accounts"
   - **Redirect URI:** Platform = Web, URI = `http://localhost`
5. Click **Register**
6. Open **Authentication** for the app and confirm:
   - `http://localhost` exists under the **Web** platform
   - **Allow public client flows** is set to **No** (this guide uses confidential client + secret)

## Step 2: Get Client Credentials

After registration:
1. On the app overview page, copy the **Application (client) ID** → This is your `CLIENT_ID`
2. Copy the **Directory (tenant) ID** → This is your `TENANT_ID` (for work/school accounts)
   - For personal Microsoft accounts, use `common` as `TENANT_ID`
3. Go to **Certificates & secrets** in the left menu
4. Click **+ New client secret**
5. Add a description (e.g., "clawdbot") and choose expiration
6. Click **Add**
7. **Immediately copy the Value** (not the ID) → This is your `CLIENT_SECRET`
   - ⚠️ You can only see this once!

## Step 3: Configure API Permissions

1. Go to **API permissions** in the left menu
2. Click **+ Add a permission**
3. Select **Microsoft Graph** → **Delegated permissions**
4. Add these permissions:
   - `Mail.ReadWrite` - Read and write mail
   - `Mail.Send` - Send mail
   - `Calendars.ReadWrite` - Read and write calendar
   - `User.Read` - Read user profile
5. Click **Add permissions**

Note: `offline_access` is requested during auth, not configured here.

## Step 4: Save Configuration

Create the config directory and files:

```bash
mkdir -p ~/.outlook-mcp
```

Create `~/.outlook-mcp/config.json`:
```json
{
  "tenant_id": "YOUR_TENANT_ID_OR_common",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

Secure the file:
```bash
chmod 600 ~/.outlook-mcp/config.json
```

## Step 5: Authorize the App

For Microsoft 365 work/school tenants, use a **tenant-specific** endpoint (not `/common`).
Use your Entra tenant ID (GUID) or tenant domain (for example, `contoso.onmicrosoft.com`).

Build the authorization URL (replace `YOUR_TENANT_ID` and `YOUR_CLIENT_ID`):

```
https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost&scope=https://graph.microsoft.com/Mail.ReadWrite%20https://graph.microsoft.com/Mail.Send%20https://graph.microsoft.com/Calendars.ReadWrite%20offline_access&response_mode=query
```

1. Open the URL in a browser
2. Sign in with your Microsoft account
3. Grant the requested permissions
4. You'll be redirected to `http://localhost?code=XXXXX...`
5. Copy the `code` value from the URL (everything after `code=` until `&` or end)

## Step 6: Exchange Code for Tokens

This step assumes a **confidential client** app registration (web platform + client secret).

```bash
TENANT_ID="your-tenant-id-or-domain"  # should match config.json tenant_id
CLIENT_ID="your-client-id"
CLIENT_SECRET="your-client-secret"
AUTH_CODE="the-code-from-step-5"

curl -s -X POST "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET&code=$AUTH_CODE&redirect_uri=http://localhost&grant_type=authorization_code&scope=https://graph.microsoft.com/Mail.ReadWrite https://graph.microsoft.com/Mail.Send https://graph.microsoft.com/Calendars.ReadWrite offline_access" \
  > ~/.outlook-mcp/credentials.json

chmod 600 ~/.outlook-mcp/credentials.json
```

## Step 7: Verify Setup

```bash
ACCESS_TOKEN=$(jq -r '.access_token' ~/.outlook-mcp/credentials.json)

curl -s "https://graph.microsoft.com/v1.0/me/mailFolders/inbox" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '{total: .totalItemCount, unread: .unreadItemCount}'
```

You should see your inbox statistics.

## Troubleshooting

### "AADSTS700016: Application not found"
- Double-check the client_id is correct
- Ensure you selected "Accounts in any organizational directory and personal Microsoft accounts"

### "AADSTS7000218: Invalid client secret"
- Client secrets can only be viewed once - create a new one if lost

### "AADSTS700025: Client is public..."
- In **App registrations → Your app → Authentication**, set **Allow public client flows** to **No**
- Ensure `http://localhost` is configured under the **Web** platform for this app
- If you changed authentication settings, run Step 5 again to get a new authorization code, then re-run Step 6

### "AADSTS65001: User hasn't consented"
- Re-run the authorization step (Step 5)
- Make sure you click "Accept" on the consent screen

### "Token expired"
- Access tokens last ~1 hour
- Run `./scripts/outlook-token.sh refresh` to get a new one

### Work/School Account Issues
- `AADSTS50194` means your app is single-tenant but you're using `/common`
- Use `https://login.microsoftonline.com/<tenant-id-or-domain>/...` for both authorize and token endpoints
- Your organization may require admin consent
- Contact your IT admin or use a personal Microsoft account
