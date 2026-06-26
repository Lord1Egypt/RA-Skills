# Auth Reference

## Main path: use the Alitar app

You do not need to create an App Registration to get started. The skill uses **Openclaw Graph Integration by Alitar.one** by default (Client ID: `952d1b34-682e-48ce-9c54-bac5a96cbd42`). Run device login and grant consent.

- **Personal account (Outlook, Hotmail):** `--tenant-id consumers`
- **Work/school account (Entra ID):** `--tenant-id organizations` (or the tenant GUID)

## Recommended authentication profiles

### Personal Microsoft account (`@outlook.com`, `@hotmail.com`, Microsoft 365 Family)

- **Skill default Client ID**: `952d1b34-682e-48ce-9c54-bac5a96cbd42` (Alitar)
- **Skill default tenant**: `consumers`
- **Use when**: you authenticate with Microsoft personal accounts (MSA), without corporate Entra ID.

### Work/school account (Microsoft Entra ID / Azure AD)

- **Default:** use the Alitar Client ID with `--tenant-id organizations` (or tenant GUID).
- **Optional:** if your organization already has an approved App Registration, use `--client-id <your-app-id>` and `--tenant-id <tenant-id>`. See [Create Your Own App Registration](../docs/app-registration.md) for portal steps.
- **Suggested scopes** (for your own app):
  - `Mail.ReadWrite`
  - `Mail.Send`
  - `Calendars.ReadWrite`
  - `Files.ReadWrite.All`
  - `Contacts.ReadWrite` *(remove if contacts are not needed)*
  - `offline_access` (required for refresh token)

## Assisted device-code flow

1. Run (personal-account profile): `python3 scripts/graph_auth.py device-login --client-id 952d1b34-682e-48ce-9c54-bac5a96cbd42 --tenant-id consumers`  
   Or work/school: `python3 scripts/graph_auth.py device-login --client-id 952d1b34-682e-48ce-9c54-bac5a96cbd42 --tenant-id organizations`
2. The script prints **URL** and **code**.
3. Open `https://microsoft.com/devicelogin`, paste the code, and authorize.
4. On success, the script saves `state/graph_auth.json` with `access_token`, `refresh_token`, expiration, and scopes.
5. Tokens auto-refresh before requests. To force refresh: `python3 scripts/graph_auth.py refresh`.
6. Scopes are fixed by the skill defaults; scope override via CLI is intentionally disabled.

## `state/graph_auth.json` structure

```json
{
  "client_id": "952d1b34-682e-48ce-9c54-bac5a96cbd42",
  "tenant_id": "consumers",
  "scopes": ["Mail.ReadWrite", "Mail.Send", ...],
  "token": {
    "access_token": "...",
    "refresh_token": "...",
    "expires_at": 1234567890
  }
}
```

Never commit this file (`.gitignore`).

## Common errors

| Symptom | Fix |
| --- | --- |
| `authorization_pending` | Wait, user has not completed authorization yet. |
| `interaction_required` | Re-run device login (token invalid/consent removed). |
| `AADSTS50059` on `/devicecode` | Tenant is incompatible with account type. For personal accounts use `--tenant-id consumers`. |
| `AADSTS700016` on `consumers` | `client_id` is not valid for Microsoft personal accounts. Use an MSA-compatible app registration. |
| `AADSTS70011 invalid_scope` with `OnlineMeetings.*` on `consumers` | `OnlineMeetings.*` scopes are not supported in this workflow for personal accounts. Remove these scopes and keep default scopes. |
| Repeated 401 errors | Run `graph_auth.py refresh`; if still failing, run `clear` and re-authenticate. |
| 403 (Access Denied) | Add the required scope and grant consent again. |
