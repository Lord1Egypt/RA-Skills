# M365 Unified Skill v1.0.0

Modular Microsoft Graph API skill for OpenClaw with optional features for Exchange Online, SharePoint, OneDrive, and Planner.

## Features

### Core Modules (Choose During Setup)

| Module | Description | Required Permissions |
|--------|-------------|---------------------|
| **Email** | Send, receive, move emails, manage folders, attachments | `Mail.Read`, `Mail.ReadWrite`, `Mail.Send` |
| **SharePoint** | Upload/download files, manage document libraries | `Sites.ReadWrite.All`, `Files.ReadWrite` |
| **OneDrive** | Personal file storage, attachment backup | `Files.ReadWrite.All` |
| **Planner** | Task management, create tasks from emails | `Tasks.ReadWrite`, `Group.Read.All` |

### Advanced Features

- **🔔 Webhook Subscriptions** - Get notified on new emails (no polling needed)
- **📬 Shared Mailboxes** - Support for shared/team mailboxes
- **🔄 Email → Task** - Automatically create Planner tasks from emails
- **📎 Attachment → SharePoint** - Save email attachments directly to SharePoint

## Architecture

```
m365-unified/
├── src/
│   ├── index.js                 # Main entry point (modular)
│   ├── auth/
│   │   └── graph-client.js      # Shared OAuth2 authentication
│   ├── email/
│   │   ├── mail.js              # Send, receive, move
│   │   ├── folders.js           # Folder management
│   │   └── attachments.js       # Attachment handling
│   ├── sharepoint/
│   │   └── files.js             # SharePoint file operations
│   ├── onedrive/
│   │   └── files.js             # OneDrive file operations
│   ├── planner/
│   │   ├── tasks.js             # Task management
│   │   └── plans.js             # Plan & bucket management
│   └── webhooks/
│       └── subscriptions.js     # Webhook subscription management
├── scripts/
│   ├── setup-wizard.js          # Interactive setup (asks what you need)
│   ├── test-connection.js       # Test authentication
│   ├── test-email.js            # Test email features
│   ├── test-sharepoint.js       # Test SharePoint features
│   ├── test-onedrive.js         # Test OneDrive features
│   ├── test-planner.js          # Test Planner features
│   └── manage-webhooks.js       # Create/delete webhook subscriptions
├── docs/
│   ├── setup.md                 # Full setup guide
│   ├── webhooks.md              # Webhook configuration
│   └── shared-mailboxes.md      # Shared mailbox setup
├── config/
│   └── template.env             # Environment template (no real data!)
├── package.json
└── SKILL.md                     # OpenClaw skill documentation
```

## Quick Start

### 1. Run Setup Wizard

```bash
cd m365-unified
npm install
node scripts/setup-wizard.js
```

The wizard will ask:
- ✅ Enable Email (Exchange Online)?
- ✅ Enable SharePoint?
- ✅ Enable OneDrive?
- ✅ Enable Planner?
- ✅ Enable Webhooks (push notifications)?
- ✅ Need Shared Mailbox support?

### 2. Configure Azure AD App Registration

The wizard generates a checklist for your required permissions based on your answers.

### 3. Test Connection

```bash
node scripts/test-connection.js
```

## Configuration

### Environment Variables (`.env`)

```bash
# === REQUIRED: Authentication ===
M365_TENANT_ID="<your-tenant-id>"
M365_CLIENT_ID="<your-client-id>"
M365_CLIENT_SECRET="<your-client-secret>"

# === OPTIONAL: Feature Toggles ===
M365_ENABLE_EMAIL=true
M365_ENABLE_SHAREPOINT=false
M365_ENABLE_ONEDRIVE=false
M365_ENABLE_PLANNER=false
M365_ENABLE_WEBHOOKS=false

# === OPTIONAL: Module-Specific Config ===
# Email
M365_MAILBOX="user@domain.com"
M365_SHARED_MAILBOXES="team1@domain.com,team2@domain.com"  # Comma-separated

# SharePoint
M365_SHAREPOINT_SITE_ID="<tenant>.sharepoint.com,<site-guid>,<web-guid>"

# OneDrive
M365_ONEDRIVE_USER="user@domain.com"  # Usually same as mailbox

# Planner
M365_PLANNER_GROUP_ID="<m365-group-id>"

# Webhooks
M365_WEBHOOK_URL="https://your-domain.com/webhook/m365"
M365_WEBHOOK_SECRET="<random-secret-for-validation>"
```

### Using Placeholders in Templates

**Never commit real credentials!** The `config/template.env` file contains only placeholders:

```bash
# Template - Copy to .env and fill in your values
M365_TENANT_ID="<your-tenant-id-here>"
M365_CLIENT_ID="<your-client-id-here>"
M365_CLIENT_SECRET="<your-client-secret-here>"
```

## Webhook Integration

### How It Works

Instead of polling with cron jobs, Microsoft Graph sends HTTP POST requests to your webhook URL when:
- New email arrives
- Email is moved/deleted
- File is created/modified (SharePoint/OneDrive)
- Task is created/updated (Planner)

### Setup Webhooks

```bash
node scripts/manage-webhooks.js create --resource mail --type newMessage
```

### Webhook Payload Example

```json
{
  "value": [
    {
      "subscriptionId": "subscription-id",
      "clientState": "your-secret",
      "changeType": "created",
      "resource": "users/user@domain.com/messages",
      "resourceData": {
        "@odata.type": "#microsoft.graph.message",
        "id": "message-id"
      },
      "subscriptionExpirationDateTime": "2026-04-20T13:52:00Z"
    }
  ]
}
```

### Integration with OpenClaw

Webhooks can trigger OpenClaw actions:
1. New email → Create Planner task automatically
2. Email with attachment → Save to SharePoint
3. Email from specific sender → Forward + notify

## Security

### Best Practices

1. **Never commit `.env`** - Add to `.gitignore`
2. **Use app-only permissions** (not delegated) for automated tasks
3. **Rotate secrets** every 6-12 months
4. **Limit permissions** to only what you need
5. **Validate webhook signatures** with client state secret

### Permission Scopes

| Feature | Minimum Permissions |
|---------|-------------------|
| Email (read) | `Mail.Read` |
| Email (send) | `Mail.Send` |
| Email (full) | `Mail.ReadWrite` |
| SharePoint | `Sites.ReadWrite.All` |
| OneDrive | `Files.ReadWrite.All` |
| Planner | `Tasks.ReadWrite`, `Group.Read.All` |
| Webhooks | `User.Read` (for validation) |

## API Reference

### Email

```javascript
const m365 = await createM365Client(config);

// Send email
await m365.email.send({
  to: ['recipient@domain.com'],
  subject: 'Hello',
  body: '<p>Message</p>',
  attachments: [{ name: 'file.pdf', contentBytes: 'base64...' }]
});

// List emails
const messages = await m365.email.list({ top: 10, folder: 'inbox' });

// Move email to folder
await m365.email.move(messageId, folderId);

// Save attachment to SharePoint
await m365.email.saveAttachmentToSharePoint(messageId, attachmentId, '/Documents/Invoices');
```

### Planner

```javascript
// List plans
const plans = await m365.planner.listPlans();

// Create task from email
await m365.planner.createTaskFromEmail({
  messageId: 'message-id',
  planId: 'plan-id',
  bucketId: 'bucket-id',  // optional
});
```

### Webhooks

```javascript
// Create subscription
const subscription = await m365.webhooks.create({
  resource: 'users/user@domain.com/messages',
  changeType: 'created',
  notificationUrl: 'https://your-domain.com/webhook',
  expirationDateTime: '2026-04-20T13:52:00Z',
});

// Renew subscription
await m365.webhooks.renew(subscriptionId, newExpirationDate);

// Delete subscription
await m365.webhooks.delete(subscriptionId);
```

## Migration from m365-planner

The authentication module is compatible with the existing m365-planner skill. You can:

1. **Keep both skills** - Use m365-planner for tasks, m365-unified for email
2. **Migrate gradually** - Start with email, add Planner later
3. **Merge completely** - Deprecate m365-planner, use unified skill only

## Troubleshooting

See `docs/setup.md` for detailed troubleshooting guides.

## License

MIT

## Author

OpenClaw Community
