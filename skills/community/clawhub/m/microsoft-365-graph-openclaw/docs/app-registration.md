# Create Your Own App Registration (Microsoft Entra ID)

To **start quickly**, you can use the default Alitar app (see [references/auth.md](../references/auth.md)); no portal setup is required. This page explains how to create **your own** App Registration when you need full control (production governance, tenant policies, compliance).

## When to use this path

- Production environments with compliance or tenant policy requirements
- Organizations that require a tenant-owned app registration
- Scenarios where you want isolated scope and consent management

## Step-by-step

### 1. Open the portal

- **Azure Portal:** [https://portal.azure.com](https://portal.azure.com) -> Azure Active Directory (or Microsoft Entra ID)
- Or **Microsoft Entra admin center:** [https://entra.microsoft.com](https://entra.microsoft.com)

Navigation path: **Azure Active Directory** (or **Entra ID**) -> **App registrations** -> **New registration**.

### 2. Create the app registration

- **Name:** for example, `OpenClaw Graph Mail`
- **Supported account types:** select based on your use case (single tenant, multitenant, personal accounts)
- **Redirect URI:** not required for device-code flow; leave blank or use `Public client / native`
- Click **Register**

### 3. Copy the Application (client) ID

In the app **Overview** page, copy **Application (client) ID**. This is the value used as `--client-id` in authentication commands.

### 4. Enable device-code support (public client)

- **Authentication** -> **Advanced settings** -> **Allow public client flows** -> **Yes**

### 5. Add API permissions

- **API permissions** -> **Add a permission** -> **Microsoft Graph** -> **Delegated permissions**
- Add at least:
  - `Mail.ReadWrite`
  - `Mail.Send` (optional)
  - `offline_access` (required for refresh token)
- For calendar/Drive/Contacts workflows, also add: `Calendars.ReadWrite`, `Files.ReadWrite.All`, `Contacts.ReadWrite`

### 6. Grant consent

- **User consent:** each user can grant consent during device login
- **Admin consent:** some tenants require admin approval in **API permissions** -> **Grant admin consent for <tenant>**

### 7. Use the app in commands

- Personal account (MSA): ensure your app supports personal Microsoft accounts and use `--tenant-id consumers`
- Work/school: use `--client-id <your-application-id>` and `--tenant-id organizations` (or your tenant GUID)

Example:

```bash
python3 scripts/graph_auth.py device-login \
  --client-id "<TEU_APPLICATION_CLIENT_ID>" \
  --tenant-id organizations
```

## References

- [Auth reference](../references/auth.md) - recommended profiles and common auth errors
- [Microsoft identity platform / device code flow](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code)
