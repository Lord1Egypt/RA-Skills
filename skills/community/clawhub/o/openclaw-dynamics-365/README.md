# openclaw-dynamics-365

> OpenClaw skill for **Microsoft Dynamics 365 CRM** — voice-to-CRM via Dataverse Web API.

[![npm](https://img.shields.io/npm/v/openclaw-dynamics-365)](https://www.npmjs.com/package/openclaw-dynamics-365)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-blue)](https://clawhub.ai)

Create and update CRM records in Microsoft Dynamics 365 by voice — Opportunities, Leads, Contacts, Accounts, and Tasks — using the [Dataverse Web API](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview) with Azure AD OAuth 2.0.

## Supported entities

| Entity | Operations |
|---|---|
| Opportunity | Create, Update (upsert by name) |
| Lead | Create, Update (upsert by name or email) |
| Contact | Create, Update (upsert by name or email) |
| Account | Create, Update (upsert by name) |
| Task | Create |

## Installation

```bash
# Via ClawHub CLI
clawhub install openclaw-dynamics-365

# Or as an npm package
npm install openclaw-dynamics-365
```

## Azure AD setup

This skill requires an **Azure App Registration**. See the [Azure Portal Setup Guide](#azure-portal-setup) below.

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `DYNAMICS365_CLIENT_ID` | ✅ | Azure AD Application (client) ID |
| `DYNAMICS365_CLIENT_SECRET` | ✅ | Azure AD client secret value |
| `DYNAMICS365_TENANT_ID` | ✅ | Azure AD Tenant ID (`common` for multi-tenant) |
| `DYNAMICS365_INSTANCE_URL` | ✅ | Your D365 instance URL, e.g. `https://contoso.crm.dynamics.com` |

## Quick start

```typescript
import {
  Dynamics365Client,
  getAuthorizationUrl,
  exchangeCodeForTokens,
  isTokenExpired,
  refreshAccessToken,
} from "openclaw-dynamics-365";

const config = {
  clientId: process.env.DYNAMICS365_CLIENT_ID,
  clientSecret: process.env.DYNAMICS365_CLIENT_SECRET,
  tenantId: process.env.DYNAMICS365_TENANT_ID ?? "common",
  instanceUrl: process.env.DYNAMICS365_INSTANCE_URL,
};

// 1. Start OAuth flow — redirect user to this URL
const authUrl = getAuthorizationUrl(config, "https://yourapp.com/callback", "csrf-state");

// 2. In the OAuth callback handler
const tokens = await exchangeCodeForTokens(config, code, "https://yourapp.com/callback");

// 3. Use the client
const client = new Dynamics365Client(tokens.instanceUrl, tokens.accessToken);

// Create or update an Opportunity
const result = await client.upsertOpportunity({
  name: "Deal TechNova Q2",
  estimatedvalue: 75000,
  stepname: "Propose",
  actualclosedate: "2026-06-30",
});

console.log(result.created ? "Created:" : "Updated:", result.id);
console.log(Dynamics365Client.recordUrl(tokens.instanceUrl, "opportunity", result.id));
```

## API reference

### `Dynamics365Client`

```typescript
const client = new Dynamics365Client(instanceUrl: string, accessToken: string);
```

| Method | Returns | Description |
|---|---|---|
| `upsertOpportunity(payload)` | `Promise<UpsertResult>` | Create or update an Opportunity |
| `upsertLead(payload)` | `Promise<UpsertResult>` | Create or update a Lead |
| `upsertContact(payload)` | `Promise<UpsertResult>` | Create or update a Contact |
| `upsertAccount(payload)` | `Promise<UpsertResult>` | Create or update an Account |
| `createTask(payload)` | `Promise<string>` | Create a Task — returns `activityid` |
| `searchOpportunity(name)` | `Promise<string \| null>` | Find Opportunity by name |
| `searchLead(query)` | `Promise<string \| null>` | Find Lead by name or email |
| `searchContact(query)` | `Promise<string \| null>` | Find Contact by name or email |
| `searchAccount(name)` | `Promise<string \| null>` | Find Account by name |

**Static helpers:**

```typescript
// Deep link to a record in the Dynamics 365 UI
Dynamics365Client.recordUrl(instanceUrl, "opportunity", id);

// OData binding reference for lookup fields
Dynamics365Client.bindRef("accounts", accountId); // → "/accounts(abc-123)"
```

### OAuth helpers

```typescript
getAuthorizationUrl(config, redirectUri, state): string
exchangeCodeForTokens(config, code, redirectUri): Promise<OAuthTokens>
refreshAccessToken(config, refreshToken): Promise<OAuthTokens>
isTokenExpired(tokens): boolean
```

---

## Azure Portal setup

Follow these steps to create the App Registration needed for OAuth 2.0.

### 1. Create App Registration

1. Go to [portal.azure.com](https://portal.azure.com) → **Microsoft Entra ID** → **App registrations** → **New registration**
2. Fill in:
   - **Name:** `openclaw-dynamics-365` (or any descriptive name)
   - **Supported account types:** `Accounts in any organizational directory (Any Azure AD directory - Multitenant)`
   - **Redirect URI:** Web → `https://yourapp.com/auth/dynamics365/callback`
3. Click **Register**

### 2. Note your credentials

After registration, copy:
- **Application (client) ID** → `DYNAMICS365_CLIENT_ID`
- **Directory (tenant) ID** → `DYNAMICS365_TENANT_ID` (use `common` for multi-tenant)

### 3. Create a client secret

1. Go to **Certificates & secrets** → **New client secret**
2. Set an expiry (24 months recommended)
3. Copy the **Value** immediately → `DYNAMICS365_CLIENT_SECRET`

### 4. Add API permissions

1. Go to **API permissions** → **Add a permission**
2. Select the **APIs my organization uses** tab
3. Search for `Dataverse` and select it from the results
4. Select **Delegated permissions** → `user_impersonation`
5. Click **Add permissions**
6. Click **Grant admin consent** (requires Global Admin or Application Admin role)

### 5. Get your instance URL

Your Dynamics 365 instance URL is shown in the D365 browser address bar:
`https://{org}.crm.dynamics.com` → set as `DYNAMICS365_INSTANCE_URL`

---

## Linking records (OData bindings)

To link a Contact to an Account, or a Task to an Opportunity, use `Dynamics365Client.bindRef()`:

```typescript
// Link contact to account
await client.upsertContact({
  fullname: "João Silva",
  emailaddress1: "joao@techno.com",
  "parentcustomerid_account@odata.bind": Dynamics365Client.bindRef("accounts", accountId),
});

// Link task to opportunity
await client.createTask({
  subject: "Follow-up call",
  prioritycode: 2,
  "regardingobjectid_opportunity_task@odata.bind": Dynamics365Client.bindRef("opportunities", oppId),
});
```

---

## Contributing

Contributions are welcome. Please open an issue or pull request on [GitHub](https://github.com/vieiradiego/openclaw-dynamics-365).

## License

MIT © [Diego Vieira](https://github.com/vieiradiego)
