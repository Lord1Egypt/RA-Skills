# Bring-Your-Own Azure App Registration Guide

> Read this only if you do NOT use the **built-in default app** and want to register your own Azure app; otherwise skip it.
>
> Background: this toolkit signs in via the "device-code flow" - the terminal shows a verification code, and you open microsoft.com/link in a browser and enter it to authorize. The default app already contains all configuration for this flow; a bring-your-own app only needs to be registered and provide one Client ID.

## Why you need a Client ID

- **Client ID (application ID)**: the unique identifier of your app in Microsoft's identity system. Device-code sign-in only needs this.
- **No Tenant ID / Client Secret needed**: those two are for "server-side, no-human-interaction" scenarios (confidential clients). This toolkit is a public client using the device-code flow - any screen asking for them can be ignored.

## Registration steps

1. Open https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
2. Sign in with your Outlook account
3. **New registration** → enter an app name → account type: **"Personal Microsoft accounts only"**
4. **Authentication** → Add a platform → **"Mobile and desktop applications"** → check `https://login.microsoftonline.com/common/oauth2/nativeclient`
5. Bottom of the Authentication page → **"Allow public client flows"** → set to **"Yes"** → Save
6. **API permissions** → Add a permission → Microsoft Graph → Delegated permissions → add all three in turn: `User.Read`, `Calendars.ReadWrite`, `MailboxSettings.Read` (their purposes are listed in the connection-steps table of `configuration.md`)
7. Back on the **Overview** page, copy the **"Application (client) ID"** at the top

## Authentication

Run from the project root.

```bash
python scripts/outlook_setup.py <your Client ID>
```

The rest of the flow is identical to the default app: the script prints a code → open `https://www.microsoft.com/link` in a browser and enter it → authorize with your Outlook account. The token renews automatically.

## Common failures

| Symptom | Cause & fix |
|---------|-------------|
| Device code reports "app not found" | Account type isn't "Personal Microsoft accounts", or "Allow public client flows" isn't enabled |
| 403 Forbidden | The `Calendars.ReadWrite` delegated permission wasn't added |
| Verification code expired | Re-run `python scripts/outlook_setup.py` and try again |
