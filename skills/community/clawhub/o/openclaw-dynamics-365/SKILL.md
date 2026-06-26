---
name: openclaw-dynamics-365
description: Create and update CRM records in Microsoft Dynamics 365 — Opportunities, Leads, Contacts, Accounts, and Tasks via Dataverse Web API with Azure AD OAuth 2.0.
metadata:
  openclaw:
    requires:
      env:
        - DYNAMICS365_CLIENT_ID
        - DYNAMICS365_CLIENT_SECRET
        - DYNAMICS365_TENANT_ID
        - DYNAMICS365_INSTANCE_URL
    primaryEnv: DYNAMICS365_INSTANCE_URL
---

# Dynamics 365 CRM Skill

## When to activate

Activate this skill when the user mentions **Microsoft Dynamics 365**, **D365**, **Dynamics CRM**, or any of the following actions directed at a Dynamics 365 CRM:

- Creating or updating an **opportunity** / deal / oportunidade
- Creating or updating a **lead**
- Creating or updating a **contact** / contacto
- Creating or updating an **account** / empresa / conta
- Creating a **task** / activity linked to a CRM record

## Credentials required

| Variable | Description |
|---|---|
| `DYNAMICS365_CLIENT_ID` | Azure AD Application (client) ID |
| `DYNAMICS365_CLIENT_SECRET` | Azure AD client secret |
| `DYNAMICS365_TENANT_ID` | Azure AD Tenant ID — use `common` for multi-tenant |
| `DYNAMICS365_INSTANCE_URL` | Dynamics 365 instance URL, e.g. `https://contoso.crm.dynamics.com` |

## Step-by-step execution

### 1 — Identify intent and entity type

Determine from the user's message which entity to create or update:

| User says | Entity | Action |
|---|---|---|
| "create deal", "new opportunity", "deal com X" | Opportunity | upsert |
| "new lead", "criar lead", "prospect X" | Lead | upsert |
| "add contact", "criar contacto", "cliente X no CRM" | Contact | upsert |
| "new account", "empresa Y no CRM", "criar conta" | Account | upsert |
| "create task", "follow-up", "lembrete para X" | Task | create |

### 2 — Extract fields from user input

**Opportunity fields:**
- `name` — deal / opportunity name (required)
- `estimatedvalue` — numeric value in local currency
- `stepname` — pipeline stage: "Qualify" / "Develop" / "Propose" / "Close"
- `actualclosedate` — expected close date (ISO: YYYY-MM-DD)

**Lead fields:**
- `fullname` — full name (required)
- `emailaddress1` — email address
- `companyname` — company name
- `telephone1` — phone number
- `jobtitle` — job title

**Contact fields:**
- `fullname` — full name (required)
- `emailaddress1` — email address
- `telephone1` — phone number
- `jobtitle` — job title

**Account fields:**
- `name` — company / account name (required)
- `emailaddress1` — email address
- `telephone1` — phone number
- `websiteurl` — website

**Task fields:**
- `subject` — task title (required)
- `description` — details / notes
- `scheduledend` — due date-time (ISO 8601)
- `prioritycode` — 0 = Low, 1 = Normal, 2 = High

### 3 — Call the appropriate method

Use the `Dynamics365Client` from the `openclaw-dynamics-365` npm package:

```typescript
import { Dynamics365Client } from "openclaw-dynamics-365";

const client = new Dynamics365Client(
  process.env.DYNAMICS365_INSTANCE_URL,
  accessToken,  // obtained via OAuth flow
);

// Opportunity
const result = await client.upsertOpportunity({ name: "Deal Contoso", estimatedvalue: 50000 });

// Lead
const result = await client.upsertLead({ fullname: "João Silva", companyname: "TechNova" });

// Contact
const result = await client.upsertContact({ fullname: "Maria Santos", emailaddress1: "maria@techno.com" });

// Account
const result = await client.upsertAccount({ name: "TechNova Ltda" });

// Task
const taskId = await client.createTask({ subject: "Follow-up call", prioritycode: 2 });
```

### 4 — Format response to the user

On success:
```
✅ [Entity] "[name]" [created/updated] in Dynamics 365.
🔗 [record URL]
```

On error:
```
❌ Could not [create/update] [entity] in Dynamics 365: [error message]
```

## OAuth setup

For initial authorization, use `getAuthorizationUrl()` to redirect the user to
Microsoft's consent screen, then `exchangeCodeForTokens()` in the callback:

```typescript
import { getAuthorizationUrl, exchangeCodeForTokens } from "openclaw-dynamics-365";

// 1. Redirect user
const url = getAuthorizationUrl(config, redirectUri, state);

// 2. In callback
const tokens = await exchangeCodeForTokens(config, code, redirectUri);

// 3. Refresh when expired (~1h)
if (isTokenExpired(tokens)) {
  tokens = await refreshAccessToken(config, tokens.refreshToken);
}
```

## Notes

- The Dataverse Web API uses **OData v4** — all queries use `$filter`, `$select`, `$top`
- Upsert operations search by name/email first to avoid duplicates
- Lookup fields (e.g. linking a Contact to an Account) use OData binding syntax:
  `"parentcustomerid_account@odata.bind": "/accounts({accountId})"`
- Rate limit: **6,000 requests / 5 minutes** per user — well within typical usage
- Access tokens expire after **~1 hour** — implement refresh logic using `refreshAccessToken()`
