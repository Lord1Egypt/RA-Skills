# Invoice & Payment Chaser — Setup Guide

## Step 1 — Connect Xero

### Create a Xero app

1. Go to https://developer.xero.com/app/manage
2. Click "New app"
3. Name: "OpenClaw Invoice Chaser"
4. Integration type: Web app
5. Redirect URI: `http://localhost:8080/callback` (for local auth flow)
6. Add scopes: `accounting.transactions` `accounting.contacts` `accounting.settings`
7. Save — copy your Client ID and Client Secret

### Authenticate

Send your bot:
```
Connect Xero:
Client ID: {your_client_id}
Client Secret: {your_client_secret}
```

Your bot will provide an authorisation URL. Visit it in your browser, approve access,
and paste the authorisation code back. The skill exchanges it for access and refresh
tokens, which are stored securely in memory. You won't need to do this again unless
the refresh token expires (after 60 days of inactivity).

### Get your Tenant ID

After authentication, the skill fetches your Xero organisation ID automatically:
```
GET https://api.xero.com/connections
```
If you have multiple Xero organisations, it will ask which to use.

---

## Step 2 — Connect QuickBooks (optional)

### Create a QuickBooks app

1. Go to https://developer.intuit.com/app/developer/myapps
2. Click "Create an app" → QuickBooks Online and Payments
3. Name: "OpenClaw Invoice Chaser"
4. Add scope: `com.intuit.quickbooks.accounting`
5. Set redirect URI: `http://localhost:8080/callback`
6. Copy Client ID and Client Secret

### Authenticate

Send your bot:
```
Connect QuickBooks:
Client ID: {your_client_id}
Client Secret: {your_client_secret}
```

Follow the same OAuth flow as Xero.

---

## Step 3 — Connect your email (for sending chase emails)

Same IMAP/SMTP setup as the Customer Support Triage skill.
If already configured, credentials are reused automatically.

### Gmail app password

1. Google Account → Security → 2-Step Verification → App passwords
2. Select app: Mail · Device: Other → name it "OpenClaw"
3. Copy the 16-character password

Send your bot:
```
Set invoice email:
Host: imap.gmail.com
SMTP: smtp.gmail.com
Port: 993 / 587
Username: accounts@mycompany.co.uk
App password: xxxx xxxx xxxx xxxx
```

---

## Step 4 — Configure your chase settings

```
Set invoice config:
Business name: Meridian Consulting
Owner name: Sarah
From email: accounts@meridianconsulting.co.uk
Payment terms: 30 days
Chase enabled: yes
Approval required: yes
WhatsApp threshold: £500
Late payment interest: yes
```

---

## Step 5 — Run your first check

```
check overdue invoices
```

---

## Step 6 — Set up heartbeat (optional)

Add to your HEARTBEAT.md:
```
- Check Xero/QuickBooks for newly overdue invoices and payment updates.
- Notify me if any invoices have crossed a chase stage threshold.
- Notify me immediately if any payment is received on an overdue invoice.
- If APPROVAL_REQUIRED = true, show me pending chases — do not auto-send.
- Always hold Stage 4 (final demand) for my explicit approval.
```

---

## Required API scopes

### Xero
| Scope | Why |
|-------|-----|
| `accounting.transactions` | Read and update invoices |
| `accounting.contacts` | Read client contact details and email addresses |
| `accounting.settings` | Read bank account codes (for marking invoices as paid) |

### QuickBooks
| Scope | Why |
|-------|-----|
| `com.intuit.quickbooks.accounting` | Full accounting access — read invoices, contacts |

---

## Statutory interest calculation

The Late Payment of Commercial Debts (Interest) Act 1998 allows you to charge:
- Interest: 8% above Bank of England base rate
- Plus fixed debt recovery costs

**To find the current Bank of England base rate:**
Ask your bot: "what is the current Bank of England base rate?" and it will search
for the latest figure. As of April 2026, verify the current rate before use.

**Example at 5.25% base rate:**
- Total rate: 13.25% per annum
- Daily rate: 13.25% ÷ 365 = 0.03630% per day
- On £1,850 overdue 38 days: £1,850 × 0.0003630 × 38 = £25.52

---

## Troubleshooting

**"Xero 401 Unauthorized"**
→ Access token expired. The skill auto-refreshes — if this persists, your
refresh token may have expired (60 days of inactivity). Re-authenticate:
send your bot "reconnect Xero" and follow the OAuth flow again.

**"Xero 403 Forbidden"**
→ Missing API scope. Go to developer.xero.com → your app → add missing scope.
Re-authenticate to get a new token with the updated scopes.

**"Invoice shows as overdue but client says they paid"**
→ Payment may not have been reconciled in Xero yet. Ask client for payment
reference and check your bank. Once reconciled in Xero, the skill will detect
it automatically on the next sync.

**"Chase email bounced"**
→ Email address in Xero may be wrong. Update it in Xero Contacts and re-fetch.

**"QuickBooks invoice not appearing"**
→ Verify the invoice is in "Open" status in QuickBooks (not Draft). Only
authorised/open invoices with a balance > 0 are fetched.

**Token refresh fails for both platforms**
→ Check that the client secret stored in memory matches the one in your app
settings. App secrets can be regenerated in the developer portal, which
invalidates the old one.
