# Miro REST API - Webhooks Guide

## Overview

Webhooks allow your application to receive real-time notifications when events happen on Miro boards. Instead of polling the API repeatedly, Miro pushes events to your endpoint immediately.

---

## Webhook Events

### Item Events
- `item.created` - Item added to board
- `item.updated` - Item modified (title, position, style, etc.)
- `item.deleted` - Item removed from board

### Comment Events
- `comment.created` - Comment posted
- `comment.updated` - Comment edited
- `comment.deleted` - Comment removed

### Board Events
- `board.created` - Board created
- `board.updated` - Board settings changed
- `board.deleted` - Board deleted
- `board.shared` - Board sharing changed

### Collaboration Events
- `item.focus` - User opened item
- `user.joined` - User joined board
- `user.left` - User left board

---

## Setting Up a Webhook

### 1. Create Webhook Endpoint

Your endpoint should:
- Accept POST requests
- Respond with 200 OK within 30 seconds
- Process events asynchronously
- Verify webhook signature

**Example (Node.js/Express):**
```javascript
const express = require('express');
const app = express();

app.post('/webhook/miro', (req, res) => {
  // Verify signature (see Signature Verification section)
  const isValid = verifySignature(req);
  
  if (!isValid) {
    return res.status(401).send('Unauthorized');
  }
  
  // Acknowledge receipt immediately
  res.status(200).send('OK');
  
  // Process event asynchronously
  handleEvent(req.body);
});

function handleEvent(event) {
  console.log(`Received ${event.type} event`);
  
  if (event.type === 'item.created') {
    console.log(`New item: ${event.data.title}`);
  }
}

app.listen(3000, () => console.log('Webhook listening on port 3000'));
```

**Example (Python/Flask):**
```python
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/webhook/miro', methods=['POST'])
def webhook():
    if not verify_signature(request):
        return 'Unauthorized', 401
    
    event = request.json
    print(f"Received {event['type']} event")
    
    if event['type'] == 'item.created':
        handle_item_created(event['data'])
    
    return 'OK', 200

def handle_item_created(data):
    print(f"New item: {data['title']}")

if __name__ == '__main__':
    app.run(port=3000)
```

### 2. Register Webhook via API

```bash
curl -X POST https://api.miro.com/v2/teams/{team_id}/webhooks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourapp.com/webhook/miro",
    "events": ["item.created", "item.updated", "item.deleted"],
    "board_ids": ["board-123"]
  }'
```

**Response:**
```json
{
  "id": "webhook-123",
  "url": "https://yourapp.com/webhook/miro",
  "events": ["item.created", "item.updated", "item.deleted"],
  "board_ids": ["board-123"],
  "created_at": "2024-01-15T10:30:00Z",
  "status": "ACTIVE"
}
```

### 3. Test Webhook (Optional)

```bash
curl -X POST https://api.miro.com/v2/teams/{team_id}/webhooks/{webhook_id}/test \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Miro will send a test event to your endpoint.

---

## Webhook Event Format

### Structure
```json
{
  "id": "event-123",
  "type": "item.created",
  "createdAt": "2024-01-15T10:30:00.000Z",
  "triggeredBy": {
    "id": "user-123",
    "email": "user@example.com"
  },
  "board": {
    "id": "board-123",
    "name": "My Board"
  },
  "data": {
    "id": "item-456",
    "type": "CARD",
    "title": "New Task",
    "description": "Task description",
    "position": {"x": 100, "y": 200}
  }
}
```

### Event Types

#### item.created
```json
{
  "type": "item.created",
  "data": {
    "id": "item-id",
    "type": "CARD",
    "title": "Task Title",
    "description": "Details",
    "owner_id": "user-id",
    "position": {"x": 0, "y": 0},
    "geometry": {"width": 200, "height": 100},
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### item.updated
```json
{
  "type": "item.updated",
  "data": {
    "id": "item-id",
    "title": "Updated Title",
    "position": {"x": 150, "y": 250},
    "updated_at": "2024-01-15T10:35:00Z"
  }
}
```

#### item.deleted
```json
{
  "type": "item.deleted",
  "data": {
    "id": "item-id",
    "deleted_at": "2024-01-15T10:40:00Z"
  }
}
```

#### comment.created
```json
{
  "type": "comment.created",
  "data": {
    "id": "comment-id",
    "content": "Great idea!",
    "creator_id": "user-id",
    "target": {
      "id": "item-id",
      "type": "CARD"
    },
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

---

## Signature Verification

Miro includes a signature to verify webhook authenticity.

### How It Works

Miro sends:
- `X-Miro-Request-Signature` header with HMAC-SHA256 signature
- Webhook secret (from registration)

Your endpoint verifies:
- Compute HMAC using secret
- Compare with provided signature

### Implementation

**Node.js:**
```javascript
const crypto = require('crypto');

function verifySignature(req) {
  const signature = req.get('X-Miro-Request-Signature');
  const secret = process.env.MIRO_WEBHOOK_SECRET;
  const body = req.rawBody; // Store raw body as string
  
  const hmac = crypto
    .createHmac('sha256', secret)
    .update(body)
    .digest('hex');
  
  return signature === `sha256=${hmac}`;
}

// Middleware to capture raw body
app.use(express.raw({type: 'application/json'}));
```

**Python:**
```python
import hmac
import hashlib

def verify_signature(request):
    signature = request.headers.get('X-Miro-Request-Signature')
    secret = os.getenv('MIRO_WEBHOOK_SECRET')
    body = request.data
    
    hmac_obj = hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    )
    expected = f"sha256={hmac_obj.hexdigest()}"
    
    return signature == expected
```

### Security Note
Always verify signatures before processing events.

---

## Webhook Best Practices

### 1. Idempotency
Events might be delivered multiple times. Handle duplicates gracefully.

```javascript
async function handleEvent(event) {
  // Check if already processed
  const exists = await db.events.findOne({ id: event.id });
  if (exists) return;
  
  // Process event
  await processEvent(event);
  
  // Store that we processed it
  await db.events.insert({ id: event.id, processed_at: new Date() });
}
```

### 2. Asynchronous Processing
Always respond with 200 OK immediately, process async.

```javascript
app.post('/webhook/miro', async (req, res) => {
  res.status(200).send('OK'); // Respond immediately
  
  // Process asynchronously
  setImmediate(() => handleEvent(req.body));
});
```

### 3. Error Handling
Don't throw errors in webhook handler. Log and retry.

```javascript
async function handleEvent(event) {
  try {
    await processEvent(event);
  } catch (error) {
    console.error('Error processing event:', error);
    // Log for manual review
    await db.failedEvents.insert({ event, error: error.message });
    // Could implement retry logic here
  }
}
```

### 4. Rate Limiting
Monitor webhook delivery rate and implement backpressure.

```javascript
const queue = [];
const maxQueueSize = 1000;

app.post('/webhook/miro', (req, res) => {
  if (queue.length >= maxQueueSize) {
    return res.status(429).send('Queue full');
  }
  
  queue.push(req.body);
  res.status(200).send('OK');
});

// Process queue with concurrency control
async function processQueue() {
  const concurrency = 5;
  while (queue.length > 0) {
    const batch = queue.splice(0, concurrency);
    await Promise.all(batch.map(handleEvent));
  }
}

setInterval(processQueue, 1000);
```

### 5. Monitoring
Track webhook health and delivery.

```javascript
async function handleEvent(event) {
  const start = Date.now();
  
  try {
    await processEvent(event);
    
    // Log success
    await db.webhookLog.insert({
      event_id: event.id,
      type: event.type,
      status: 'success',
      duration: Date.now() - start
    });
  } catch (error) {
    await db.webhookLog.insert({
      event_id: event.id,
      type: event.type,
      status: 'error',
      error: error.message,
      duration: Date.now() - start
    });
  }
}
```

---

## Testing Webhooks Locally

### Option 1: ngrok (Recommended)

```bash
# Install ngrok
npm install -g ngrok

# Start your local server
npm start  # on port 3000

# In another terminal, expose to internet
ngrok http 3000
# Returns: https://abc123.ngrok.io

# Register webhook with ngrok URL
# https://abc123.ngrok.io/webhook/miro
```

### Option 2: Mock Server

```javascript
const express = require('express');
const app = express();

// Simulate webhook events
app.get('/simulate/item-created', (req, res) => {
  const event = {
    type: 'item.created',
    data: {
      id: 'item-123',
      title: 'Test Item',
      position: {x: 0, y: 0}
    }
  };
  
  fetch('http://localhost:3000/webhook/miro', {
    method: 'POST',
    body: JSON.stringify(event)
  });
  
  res.send('Event sent');
});

app.listen(3000);
```

---

## Debugging

### Check Webhook Status

```bash
curl -X GET https://api.miro.com/v2/teams/{team_id}/webhooks/{webhook_id} \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Response includes:
- `status` - ACTIVE, INACTIVE, FAILED
- `last_error` - Last error message
- `last_delivered_at` - Timestamp of last successful delivery

### Common Issues

| Issue | Solution |
|-------|----------|
| Webhook not firing | Check if board_ids filter is set correctly |
| Invalid signature | Verify secret is correct, check raw body parsing |
| 404 on endpoint | Check URL is publicly accessible, verify HTTPS |
| Timeout (>30s) | Process asynchronously, respond immediately |
| Duplicate events | Implement idempotency key tracking |

