---
name: m365-unified
description: "Unified Microsoft 365 skill for OpenClaw with modular features for Exchange Online (Email), SharePoint, OneDrive, and Planner. Supports webhooks for real-time notifications."
---

# M365 Unified Skill

**Version:** 1.0.0  
**Author:** OpenClaw Community  
**License:** MIT  
**Repository:** https://github.com/openclaw/m365-unified-skill

## Overview

Unified Microsoft 365 skill for OpenClaw providing modular access to Microsoft Graph API services. Features include Exchange Online (Email), SharePoint, OneDrive, and Planner integration with optional webhook support for real-time notifications instead of polling.

## Features

### Core Modules

| Module | Description | Required Permissions |
|--------|-------------|---------------------|
| **Email** | Send, receive, move emails, manage folders, handle attachments | `Mail.Read`, `Mail.ReadWrite`, `Mail.Send` |
| **SharePoint** | Upload/download files, manage document libraries | `Sites.ReadWrite.All`, `Files.ReadWrite.All` |
| **OneDrive** | Personal file storage, attachment backup | `Files.ReadWrite.All` |
| **Planner** | Task management, create tasks from emails | `Tasks.ReadWrite`, `Group.Read.All` |

### Advanced Features

- **🔔 Webhooks** - Real-time notifications via Microsoft Graph subscriptions (no polling needed)
- **📬 Shared Mailboxes** - Support for team/shared mailboxes
- **🔄 Email → Task** - Automatically create Planner tasks from emails
- **📎 Attachment → SharePoint** - Save email attachments directly to SharePoint
- **🔐 OAuth2 App-Only** - Secure authentication using Azure AD app registrations

## Architecture

```
m365-unified/
├── src/
│   ├── index.js                 # Main entry point (modular client)
│   ├── auth/
│   │   └── graph-client.js      # OAuth2 authentication & token management
│   ├── email/
│   │   ├── mail.js              # Send, receive, search emails
│   │   ├── folders.js           # Folder/mailbox management
│   │   └── attachments.js       # Attachment download & handling
│   ├── sharepoint/
│   │   └── files.js             # SharePoint file operations
│   ├── onedrive/
│   │   └── files.js             # OneDrive file operations
│   ├── planner/
│   │   ├── tasks.js             # Task CRUD operations
│   │   └── plans.js             # Plan & bucket management
│   └── webhooks/
│       └── subscriptions.js     # Webhook subscription lifecycle
├── scripts/
│   ├── setup-wizard.js          # Interactive setup & configuration
│   ├── test-connection.js       # Test authentication & connectivity
│   ├── test-email.js            # Test email features
│   ├── test-sharepoint.js       # Test SharePoint features
│   ├── test-onedrive.js         # Test OneDrive features
│   ├── test-planner.js          # Test Planner features
│   ├── manage-webhooks.js       # Create/list/renew/delete webhooks
│   ├── webhook-handler.js       # Express server for webhook notifications
│   └── process-invoice-email.js # Example: Invoice processing workflow
├── docs/
│   ├── webhooks.md              # Webhook setup & troubleshooting
│   └── SHARED-MAILBOXES.md      # Shared mailbox configuration
├── config/
│   └── template.env             # Environment template (placeholders only)
├── package.json
└── SKILL.md                     # This file
```

## Quick Start

### 1. Install Dependencies

```bash
cd m365-unified
npm install
```

### 2. Run Setup Wizard

```bash
npm run setup
# or
node scripts/setup-wizard.js
```

The interactive wizard will:
- Ask which features you need (Email, SharePoint, OneDrive, Planner, Webhooks)
- Generate a personalized `.env` file with placeholders
- Provide a checklist for Azure AD app registration
- Show required API permissions based on your selections
- Guide you through mailbox access restrictions

### 3. Configure Azure AD App Registration

#### Step 1: Create App Registration

1. Go to [Azure Portal](https://portal.azure.com) → Azure Active Directory → App registrations
2. Click **New registration**
3. Name: `m365-unified-skill` (or your choice)
4. Supported account types: **Single tenant**
5. Redirect URI: Leave empty (not needed for app-only auth)
6. Click **Register**

#### Step 2: Create Client Secret

1. In your app registration → **Certificates & secrets**
2. Click **New client secret**
3. Description: `m365-unified-secret`
4. Expires: Choose 12-24 months
5. Click **Add**
6. **⚠️ IMPORTANT:** Copy the secret value immediately (you can't see it again!)

#### Step 3: Configure API Permissions

1. In your app registration → **API permissions**
2. Click **Add a permission** → **Microsoft Graph**
3. Select **Application permissions** (NOT delegated!)
4. Add the permissions you need:

| Feature | Permissions |
|---------|-------------|
| Email (read) | `Mail.Read` |
| Email (send) | `Mail.Send` |
| Email (full) | `Mail.ReadWrite` |
| SharePoint | `Sites.ReadWrite.All` |
| OneDrive | `Files.ReadWrite.All` |
| Planner | `Tasks.ReadWrite`, `Group.Read.All` |
| Webhooks | `User.Read` (minimum for validation) |

5. Click **Grant admin consent for [Your Tenant]** (admin action required)

#### Step 4: Copy IDs

From the app registration **Overview** page, copy:
- **Application (client) ID** → `M365_CLIENT_ID`
- **Directory (tenant) ID** → `M365_TENANT_ID`

### 4. Configure Environment

Copy the template and fill in your values:

```bash
cp config/template.env .env
```

Edit `.env`:

```bash
# Required - Authentication
M365_TENANT_ID="<your-tenant-id>"
M365_CLIENT_ID="<your-client-id>"
M365_CLIENT_SECRET="<your-client-secret>"

# Optional - Feature Toggles
M365_ENABLE_EMAIL=true
M365_ENABLE_SHAREPOINT=false
M365_ENABLE_ONEDRIVE=false
M365_ENABLE_PLANNER=false
M365_ENABLE_WEBHOOKS=false

# Optional - Module Config
M365_MAILBOX="user@domain.com"
M365_SHARED_MAILBOXES="team1@domain.com,team2@domain.com"
M365_SHAREPOINT_SITE_ID="<tenant>.sharepoint.com,<site-guid>,<web-guid>"
M365_PLANNER_GROUP_ID="<m365-group-id>"
M365_WEBHOOK_URL="https://your-domain.com/webhook/m365"
M365_WEBHOOK_SECRET="<generate-random-secret>"
```

### 5. Test Connection

```bash
npm test
# or
node scripts/test-connection.js
```

## Usage in OpenClaw

### Import and Initialize

```javascript
import { createM365Client } from './skills/m365-unified/src/index.js';

const m365 = await createM365Client({
  tenantId: process.env.M365_TENANT_ID,
  clientId: process.env.M365_CLIENT_ID,
  clientSecret: process.env.M365_CLIENT_SECRET,
  mailbox: process.env.M365_MAILBOX,
  sharepointSiteId: process.env.M365_SHAREPOINT_SITE_ID,
  plannerGroupId: process.env.M365_PLANNER_GROUP_ID,
  enableEmail: true,
  enableSharepoint: true,
  enablePlanner: true,
  enableWebhooks: false,
});
```

### Email Examples

```javascript
// Send email
await m365.email.send({
  to: ['recipient@domain.com'],
  subject: 'Hello',
  body: '<p>Message</p>',
  attachments: [{ name: 'file.pdf', contentBytes: 'base64...' }]
});

// List recent emails
const messages = await m365.email.list({ top: 10, folder: 'inbox' });

// Search emails
const results = await m365.email.search('from:client', { top: 20 });

// Move email to folder
await m365.email.move(messageId, folderId);

// Mark as read
await m365.email.markAsRead(messageId);

// Save attachment to SharePoint
await m365.email.saveAttachmentToSharePoint(
  messageId,
  attachmentId,
  '/Documents/Invoices'
);
```

### SharePoint Examples

```javascript
// Upload file
const file = await m365.sharepoint.upload('/Documents/file.pdf', content, {
  contentType: 'application/pdf',
});

// Download file
const content = await m365.sharepoint.download('/Documents/file.pdf');

// List folder contents
const files = await m365.sharepoint.listFiles('/Documents');

// Delete file
await m365.sharepoint.delete('/Documents/old-file.pdf');
```

### OneDrive Examples

```javascript
// Upload to OneDrive
const file = await m365.onedrive.upload('/Attachments/invoice.pdf', content);

// Download from OneDrive
const content = await m365.onedrive.download('/Attachments/invoice.pdf');

// List OneDrive root
const files = await m365.onedrive.listFiles();
```

### Planner Examples

```javascript
// List all plans
const plans = await m365.planner.listPlans();

// List tasks in a plan
const tasks = await m365.planner.listTasks(planId);

// Create task
await m365.planner.createTask(planId, 'Task Title', {
  priority: 3, // 1=urgent, 3=normal, 5=low
  dueDateTime: '2026-04-25T00:00:00Z',
  description: 'Task description',
  bucketId: 'bucket-id', // optional
});

// Create task from email (automation)
await m365.planner.createTaskFromEmail(messageId, planId, {
  bucketId: 'bucket-id', // optional
  priority: 3,
});

// Update task
await m365.planner.updateTask(taskId, {
  percentComplete: 50,
  priority: 1,
});

// Delete task
await m365.planner.deleteTask(taskId);
```

### Webhook Examples

```javascript
// Create webhook subscription
const subscription = await m365.webhooks.create({
  resource: `users/${mailbox}/messages`,
  changeType: 'created',
  notificationUrl: 'https://your-domain.com/webhook/m365',
  expirationDateTime: '2026-04-22T00:00:00Z',
  clientState: 'your-secret-token',
});

// List active subscriptions
const subscriptions = await m365.webhooks.list();

// Renew subscription (before expiration)
await m365.webhooks.renew(subscriptionId, '2026-04-25T00:00:00Z');

// Delete subscription
await m365.webhooks.delete(subscriptionId);
```

## Webhook Integration

### How Webhooks Work

Instead of polling with cron jobs, Microsoft Graph sends HTTP POST requests to your webhook URL when:
- New email arrives (`created`)
- Email is moved/deleted (`updated`, `deleted`)
- File is created/modified (SharePoint/OneDrive)
- Task is created/updated (Planner)

### Webhook Lifecycle

1. **Create Subscription** - Tell Graph where to send notifications
2. **Validation** - Graph sends validation challenge, your endpoint must respond
3. **Notifications** - Graph sends POST requests on resource changes
4. **Renewal** - Subscriptions expire after 3 days max, must be renewed
5. **Cleanup** - Delete subscriptions when no longer needed

### Setup Webhook Handler

```bash
# Start local webhook handler
node scripts/webhook-handler.js

# Or use the shell script
./scripts/start-webhook.sh
```

### Create Webhook Subscription

```bash
# New emails in inbox
node scripts/manage-webhooks.js create --resource=mail_inbox --type=created

# All mailbox changes
node scripts/manage-webhooks.js create --resource=mail --type=created,updated,deleted

# SharePoint file changes
node scripts/manage-webhooks.js create --resource=sharepoint --type=created,updated

# Planner task changes
node scripts/manage-webhooks.js create --resource=planner --planId=<plan-id> --type=created,updated
```

### Webhook Payload Example

```json
{
  "value": [
    {
      "subscriptionId": "subscription-id-guid",
      "clientState": "your-secret-token",
      "changeType": "created",
      "resource": "users/user@domain.com/messages",
      "resourceData": {
        "@odata.type": "#microsoft.graph.message",
        "id": "message-id"
      },
      "subscriptionExpirationDateTime": "2026-04-22T13:52:00Z"
    }
  ]
}
```

### Webhook Validation Challenge

When you create a subscription, Graph sends a validation request:

```
POST /webhook/m365
Content-Type: text/plain

Validation-Token: <random-token>
```

Your endpoint must:
1. Detect the `Validation-Token` header
2. Respond with status `200 OK` and the token value as plain text
3. Complete within 120 seconds

See `scripts/webhook-handler.js` for a reference implementation.

### Auto-Renewal

Webhooks expire after 3 days maximum. Set up auto-renewal:

```bash
# Cron job example (runs every 6 hours)
0 */6 * * * cd /path/to/m365-unified && node scripts/auto-renew-webhooks.js
```

## Configuration Reference

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `M365_TENANT_ID` | ✅ | Azure AD tenant ID |
| `M365_CLIENT_ID` | ✅ | App registration client ID |
| `M365_CLIENT_SECRET` | ✅ | App registration client secret |
| `M365_ENABLE_EMAIL` | ❌ | Enable email module (default: `false`) |
| `M365_ENABLE_SHAREPOINT` | ❌ | Enable SharePoint module (default: `false`) |
| `M365_ENABLE_ONEDRIVE` | ❌ | Enable OneDrive module (default: `false`) |
| `M365_ENABLE_PLANNER` | ❌ | Enable Planner module (default: `false`) |
| `M365_ENABLE_WEBHOOKS` | ❌ | Enable webhook features (default: `false`) |
| `M365_MAILBOX` | ⚠️ | Primary mailbox (required for email features) |
| `M365_SHARED_MAILBOXES` | ❌ | Comma-separated list of shared mailboxes |
| `M365_SHAREPOINT_SITE_ID` | ⚠️ | SharePoint site ID (required for SharePoint) |
| `M365_ONEDRIVE_USER` | ⚠️ | OneDrive user (default: same as `M365_MAILBOX`) |
| `M365_PLANNER_GROUP_ID` | ⚠️ | M365 Group ID containing Planner plans |
| `M365_WEBHOOK_URL` | ⚠️ | Public webhook endpoint URL (HTTPS required) |
| `M365_WEBHOOK_SECRET` | ⚠️ | Secret for webhook validation |
| `M365_WEBHOOK_PORT` | ❌ | Local webhook handler port (default: `3000`) |

### Getting SharePoint Site ID

```bash
# Use Graph Explorer or run:
curl -H "Authorization: Bearer <token>" \
  "https://graph.microsoft.com/v1.0/sites"
```

Response format:
```json
{
  "value": [
    {
      "id": "tenant.sharepoint.com,site-guid,web-guid",
      "displayName": "My Site"
    }
  ]
}
```

Use the full `id` value for `M365_SHAREPOINT_SITE_ID`.

### Getting Planner Group ID

```bash
# List groups with Planner plans
node scripts/test-planner.js
```

Or use Graph Explorer:
```
GET https://graph.microsoft.com/v1.0/groups?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')
```

## Testing

```bash
# Test connection & authentication
npm test

# Test individual features
npm run test:email
npm run test:sharepoint
npm run test:onedrive
npm run test:planner

# Manage webhooks
npm run webhooks:create -- --resource=mail --type=created
npm run webhooks:list
npm run webhooks:renew -- --id=<subscription-id>
npm run webhooks:delete -- --id=<subscription-id>
```

## Security

### Best Practices

1. **Never commit `.env`** - Already in `.gitignore`
2. **Use app-only permissions** (not delegated) for automated tasks
3. **Restrict mailbox access** via Azure AD app assignment
4. **Rotate secrets** every 12-18 months
5. **Monitor sign-in logs** in Azure AD regularly
6. **Use HTTPS** for webhook endpoints
7. **Validate webhook signatures** with client state secret

### Mailbox Access Restrictions

By default, `Mail.ReadWrite` grants access to ALL mailboxes in the tenant. To restrict:

#### Option 1: Azure AD App Assignment (Recommended)

1. Azure AD → Enterprise Apps → Your App → Users and groups
2. Add ONLY the users/mailboxes that should have access
3. Remove "All users" if present

#### Option 2: Application Access Policies (Exchange PowerShell)

```powershell
# Create security group with specific mailboxes
New-DistributionGroup -Name "M365AppAccess" -Type Security

# Add mailboxes to group
Add-DistributionGroupMember -Identity "M365AppAccess" -Member "user@domain.com"

# Create access policy
New-ApplicationAccessPolicy -AppId "CLIENT-ID" -PolicyScopeGroupId "M365AppAccess" -AccessRight RestrictAccess
```

### Permission Scopes Reference

| Feature | Minimum Permissions | Recommended |
|---------|-------------------|-------------|
| Email (read) | `Mail.Read` | `Mail.Read` |
| Email (send) | `Mail.Send` | `Mail.Send` |
| Email (full) | `Mail.ReadWrite` | `Mail.ReadWrite` |
| SharePoint | `Sites.Read.All` | `Sites.ReadWrite.All` |
| OneDrive | `Files.Read.All` | `Files.ReadWrite.All` |
| Planner | `Tasks.Read`, `Group.Read` | `Tasks.ReadWrite`, `Group.Read.All` |
| Webhooks | `User.Read` | `User.Read` |

## Troubleshooting

### 401 Unauthorized

**Causes:**
- Invalid Tenant ID, Client ID, or Client Secret
- Client secret has expired
- App registration is in wrong tenant

**Solutions:**
1. Verify all three values in `.env`
2. Create new client secret in Azure AD
3. Check tenant ID matches your Azure AD

### 403 Forbidden

**Causes:**
- API permissions not granted
- Admin consent not given
- Using delegated instead of application permissions

**Solutions:**
1. Go to Azure AD → App registrations → Your app → API permissions
2. Ensure permissions are **Application** type (not Delegated)
3. Click "Grant admin consent for [Tenant]"
4. Wait 5-10 minutes for propagation

### 404 Not Found

**Causes:**
- Resource (mailbox/site/group) doesn't exist
- ID is incorrect or malformed
- Wrong format for SharePoint Site ID

**Solutions:**
1. Verify the resource exists in Microsoft 365 admin center
2. Check ID format (especially SharePoint: `tenant.sharepoint.com,site-guid,web-guid`)
3. Use Graph Explorer to test the same query

### Webhooks Not Working

**Common Issues:**

1. **Webhook URL not publicly accessible**
   - Must be HTTPS (not HTTP)
   - Must be reachable from the internet (not localhost)
   - Use ngrok or similar for local development

2. **Validation challenge fails**
   - Endpoint must respond within 120 seconds
   - Response must be status `200` with token as plain text
   - Check `clientState` matches your secret

3. **Subscription expires quickly**
   - Maximum lifetime is 3 days
   - Set up auto-renewal cron job
   - Monitor expiration dates

4. **No notifications received**
   - Check resource path is correct
   - Verify change types match your needs
   - Check Azure AD app has `User.Read` permission minimum

### Rate Limiting

Microsoft Graph uses throttling. If you hit limits:

```
HTTP 429 Too Many Requests
Retry-After: <seconds>
```

**Solutions:**
- Implement exponential backoff
- Batch requests when possible
- Avoid tight loops with many requests
- Respect `Retry-After` header

## Migration from m365-planner

The authentication module is compatible with existing m365-planner configurations. You can:

1. **Keep both skills** - Use m365-planner for tasks, m365-unified for email
2. **Migrate gradually** - Start with email, add Planner later
3. **Merge completely** - Deprecate m365-planner, use unified skill only

Same credentials work for both skills - no need to create new app registrations.

## Dependencies

- `@microsoft/microsoft-graph-client` ^3.0.7
- `axios` ^1.6.0
- `dotenv` ^16.3.1
- `express` ^4.18.0 (for webhook handler)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details.

## Support

- **Documentation:** See `docs/` folder for detailed guides
- **Issues:** Report bugs on GitHub
- **Questions:** Check FAQ in `FAQ-DEPENDENCIES.md`

---

**Built with ❤️ by the OpenClaw Community**
