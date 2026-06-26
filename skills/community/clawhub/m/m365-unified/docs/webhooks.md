# Webhook Integration Guide

## Overview

Webhooks (change notifications) allow Microsoft Graph to push notifications to your application when resources change, instead of polling with cron jobs.

## Benefits vs Cron Polling

| Aspect | Cron Polling | Webhooks |
|--------|-------------|----------|
| **Latency** | Delay until next poll (minutes) | Near real-time (< 1 minute) |
| **API Calls** | Many (every poll interval) | Only when changes occur |
| **Rate Limits** | Can hit limits with frequent polling | No rate limit concerns |
| **Complexity** | Simple to set up | Requires public endpoint |
| **Reliability** | Always works | Depends on endpoint availability |
| **Cost** | Higher (more API calls) | Lower (fewer API calls) |

## Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Microsoft │      │   Your Webhook   │      │   OpenClaw      │
│    Graph    │─────▶│     Endpoint     │─────▶│   Session       │
│  (M365)     │      │  (Public HTTPS)  │      │   (Trigger)     │
└─────────────┘      └──────────────────┘      └─────────────────┘
     │                       │                         │
     │ 1. Resource changes   │                         │
     │ 2. POST notification  │                         │
     │                       │ 3. Process & validate   │
     │                       │ 4. Trigger action       │
```

## Setup Steps

### 1. Create Public Webhook Endpoint

Your endpoint must:
- Be publicly accessible (HTTPS required)
- Respond within 120 seconds
- Handle validation challenge (see below)
- Process JSON notifications

**Example Express.js Endpoint:**

```javascript
import express from 'express';
import { handleValidationChallenge, processNotification } from './m365-unified/src/webhooks/subscriptions.js';

const app = express();
app.use(express.json());

app.post('/webhook/m365', (req, res) => {
  // Step 1: Handle validation challenge (first-time setup)
  const validationToken = handleValidationChallenge(req);
  if (validationToken) {
    console.log('🔔 Webhook validation received');
    return res.status(200).send(validationToken); // Plain text, not JSON!
  }

  // Step 2: Process notification
  const notification = processNotification(req, process.env.M365_WEBHOOK_SECRET);
  
  if (!notification) {
    return res.status(400).send('Invalid notification');
  }

  console.log('📬 Webhook notification received:', notification);

  // Step 3: Trigger OpenClaw action
  // (This depends on your OpenClaw setup)
  handleWebhookAction(notification);

  // Step 4: Acknowledge receipt
  res.status(200).send('OK');
});

function handleWebhookAction(notification) {
  // Example: New email → Create Planner task
  notification.changes.forEach(change => {
    if (change.changeType === 'created' && change.resource.includes('messages')) {
      console.log(`📧 New email detected: ${change.resourceId}`);
      // Trigger OpenClaw session or action
    }
  });
}

app.listen(3000, () => {
  console.log('🔔 Webhook server listening on port 3000');
});
```

### 2. Create Webhook Subscription

```bash
node scripts/manage-webhooks.js create \
  --resource=mail \
  --type=created \
  --days=3
```

### 3. Handle Validation Challenge

When you create a subscription, Microsoft Graph validates your endpoint:

1. Graph sends: `POST /webhook/m365?validationToken=RANDOM_TOKEN`
2. Your endpoint must: Return `200 OK` with token as **plain text**
3. If valid, subscription becomes active

**Common Mistakes:**
- ❌ Returning JSON instead of plain text
- ❌ Returning 404/500 error
- ❌ Taking > 120 seconds to respond
- ❌ Not handling the validationToken query parameter

### 4. Renew Subscriptions

Webhooks expire after **3 days maximum**. Set up auto-renewal:

**Option A: Cron Job (Ironically)**
```bash
# Renew webhooks daily via cron
0 2 * * * cd /path/to/m365-unified && node scripts/manage-webhooks.js renew --id=YOUR_SUBSCRIPTION_ID --days=3
```

**Option B: Self-Renewing Webhook**
Your webhook endpoint can renew itself when processing notifications:

```javascript
if (subscriptionExpiresIn < 1 day) {
  await renewSubscription(subscriptionId);
}
```

## Webhook Payload Examples

### New Email

```json
{
  "value": [
    {
      "subscriptionId": "7f103c7d-b014-4e05-bd77-1c5a9c6d9b0e",
      "clientState": "your-secret",
      "changeType": "created",
      "resource": "users/user@domain.com/messages/AAAABBBBCCCC",
      "resourceData": {
        "@odata.type": "#microsoft.graph.message",
        "id": "AAAABBBBCCCC"
      },
      "subscriptionExpirationDateTime": "2026-04-22T13:52:00Z"
    }
  ]
}
```

### File Created in SharePoint

```json
{
  "value": [
    {
      "subscriptionId": "abc123",
      "changeType": "created",
      "resource": "sites/site-id/drive/root:/Documents/newfile.pdf",
      "resourceData": {
        "@odata.type": "#microsoft.graph.driveItem",
        "id": "01ABCDEF",
        "name": "newfile.pdf"
      }
    }
  ]
}
```

### Task Created in Planner

```json
{
  "value": [
    {
      "subscriptionId": "xyz789",
      "changeType": "created",
      "resource": "planner/plans/plan-id/tasks/task-id",
      "resourceData": {
        "@odata.type": "#microsoft.graph.plannerTask",
        "id": "task-id",
        "title": "New Task"
      }
    }
  ]
}
```

## Use Cases

### 1. Email → Planner Task (Automatic)

```javascript
// Webhook handler
if (notification.changes.some(c => 
  c.changeType === 'created' && 
  c.resource.includes('messages')
)) {
  // Get email details
  const email = await m365.email.get(messageId);
  
  // Check if should create task (e.g., from specific sender)
  if (email.from.emailAddress.address === 'boss@company.com') {
    await m365.planner.createTaskFromEmail(messageId, planId);
  }
}
```

### 2. Email Attachment → SharePoint Backup

```javascript
// Webhook handler for emails with attachments
const email = await m365.email.get(messageId);

if (email.hasAttachments) {
  const attachments = await m365.email.listAttachments(messageId);
  
  for (const attachment of attachments) {
    await m365.email.saveAttachmentToSharePoint(
      messageId,
      attachment.id,
      '/Documents/Email Attachments/' + new Date().getFullYear()
    );
  }
}
```

### 3. New File in SharePoint → Notify Team

```javascript
// Webhook handler for SharePoint
if (notification.changes.some(c => 
  c.changeType === 'created' && 
  c.resource.includes('drive')
)) {
  const file = await m365.sharepoint.getFile(filePath);
  
  await m365.email.send({
    to: ['team@company.com'],
    subject: `New file: ${file.name}`,
    body: `<p>New file uploaded: <a href="${file.webUrl}">${file.name}</a></p>`,
  });
}
```

## Troubleshooting

### Webhook Not Receiving Notifications

**Check:**
1. ✅ Subscription is active (not expired)
2. ✅ Webhook URL is publicly accessible
3. ✅ URL uses HTTPS (not HTTP)
4. ✅ Firewall allows Microsoft Graph IPs
5. ✅ Endpoint returns 200 OK within 120 seconds

**Test:**
```bash
# List subscriptions
node scripts/manage-webhooks.js list

# Check expiration dates
# If expired, renew:
node scripts/manage-webhooks.js renew --id=<id> --days=3
```

### Validation Fails

**Common Issues:**
- Endpoint returns JSON instead of plain text token
- Endpoint takes > 120 seconds to respond
- Endpoint returns error status code
- validationToken query parameter not handled

**Debug:**
```javascript
// Log the full request
console.log('Validation request:', {
  method: req.method,
  path: req.path,
  query: req.query,
  headers: req.headers,
});
```

### Subscription Expires Too Quickly

**Solution:** Set up auto-renewal

```javascript
// In your webhook handler
const subscription = await getSubscription(subscriptionId);
const expires = new Date(subscription.expirationDateTime);
const daysLeft = (expires - new Date()) / (1000 * 60 * 60 * 24);

if (daysLeft < 1) {
  await renewSubscription(subscriptionId, 3); // Renew for 3 days
  console.log('🔄 Subscription auto-renewed');
}
```

## Security Considerations

### Validate Client State

Always set and validate `clientState`:

```javascript
// When creating subscription
const subscription = await createSubscription({
  clientState: process.env.M365_WEBHOOK_SECRET,
});

// When processing notification
if (notification.clientState !== process.env.M365_WEBHOOK_SECRET) {
  console.warn('⚠️  Client state mismatch - possible spoofing');
  return res.status(403).send('Forbidden');
}
```

### Use HTTPS Only

Microsoft Graph requires HTTPS for webhook URLs. Use a valid SSL certificate.

### Rate Limiting

Implement rate limiting on your webhook endpoint to prevent abuse.

### Logging

Log all webhook notifications for debugging and audit purposes.

## Monitoring

### Health Check Endpoint

Add a health check for monitoring:

```javascript
app.get('/webhook/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    lastNotification: lastNotificationTime,
  });
});
```

### Alerting

Set up alerts for:
- Webhook endpoint down
- Subscription expiring soon (< 1 day)
- High error rate on notifications

## References

- [Microsoft Graph Webhooks Documentation](https://learn.microsoft.com/en-us/graph/webhooks)
- [Change Notifications API](https://learn.microsoft.com/en-us/graph/change-notifications-overview)
- [Subscription Resource Type](https://learn.microsoft.com/en-us/graph/api/resources/subscription)
