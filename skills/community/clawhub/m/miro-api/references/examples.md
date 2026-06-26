# Miro REST API - Code Examples

---

## cURL Examples

### Get All Boards

```bash
curl -X GET https://api.miro.com/v2/boards \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### Create a Board

```bash
curl -X POST https://api.miro.com/v2/boards \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Project Planning Board",
    "description": "Q1 2024 planning"
  }'
```

### Create a Card on Board

```bash
curl -X POST https://api.miro.com/v2/boards/uXjVGAeRkgI=/items \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CARD",
    "title": "Design homepage",
    "description": "Create mockups",
    "position": {"x": 0, "y": 0}
  }'
```

### Create Multiple Items

```bash
curl -X POST https://api.miro.com/v2/boards/uXjVGAeRkgI=/items/batch \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "type": "CARD",
        "title": "Task 1",
        "position": {"x": 0, "y": 0}
      },
      {
        "type": "CARD",
        "title": "Task 2",
        "position": {"x": 250, "y": 0}
      },
      {
        "type": "CARD",
        "title": "Task 3",
        "position": {"x": 500, "y": 0}
      }
    ]
  }'
```

### Update Item

```bash
curl -X PATCH https://api.miro.com/v2/boards/uXjVGAeRkgI=/items/item-123 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Task",
    "position": {"x": 100, "y": 100}
  }'
```

### Add Comment

```bash
curl -X POST https://api.miro.com/v2/boards/uXjVGAeRkgI=/comments \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This looks great!",
    "target": {
      "id": "item-123",
      "type": "CARD"
    }
  }'
```

### Register Webhook

```bash
curl -X POST https://api.miro.com/v2/teams/team-123/webhooks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourapp.com/webhook/miro",
    "events": ["item.created", "item.updated"],
    "board_ids": ["board-123"]
  }'
```

---

## JavaScript/Node.js

### Setup

```bash
npm init -y
npm install axios dotenv
```

### .env File

```
MIRO_TOKEN=miro_pat_your_token_here
MIRO_TEAM_ID=team-123
MIRO_BOARD_ID=board-123
```

### Get All Boards

```javascript
require('dotenv').config();
const axios = require('axios');

const miro = axios.create({
  baseURL: 'https://api.miro.com/v2',
  headers: {
    'Authorization': `Bearer ${process.env.MIRO_TOKEN}`,
    'Content-Type': 'application/json'
  }
});

async function getAllBoards() {
  try {
    const response = await miro.get('/boards');
    console.log('Boards:', response.data.data);
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

getAllBoards();
```

### Create Board and Add Items

```javascript
async function createBoardWithItems() {
  try {
    // Create board
    const boardRes = await miro.post('/boards', {
      name: 'Project Board',
      description: 'New project planning'
    });
    
    const boardId = boardRes.data.id;
    console.log('Created board:', boardId);
    
    // Add items
    const itemsRes = await miro.post(`/boards/${boardId}/items/batch`, {
      items: [
        { type: 'CARD', title: 'Design', position: { x: 0, y: 0 } },
        { type: 'CARD', title: 'Development', position: { x: 250, y: 0 } },
        { type: 'CARD', title: 'Testing', position: { x: 500, y: 0 } }
      ]
    });
    
    console.log('Created items:', itemsRes.data.items.length);
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

createBoardWithItems();
```

### List Items with Pagination

```javascript
async function listAllItems(boardId) {
  const allItems = [];
  let cursor = null;
  
  try {
    do {
      const params = { limit: 100 };
      if (cursor) params.cursor = cursor;
      
      const response = await miro.get(`/boards/${boardId}/items`, { params });
      allItems.push(...response.data.data);
      cursor = response.data.cursor;
      
      console.log(`Fetched ${response.data.data.length} items, cursor: ${cursor}`);
    } while (cursor);
    
    console.log(`Total items: ${allItems.length}`);
    return allItems;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

listAllItems(process.env.MIRO_BOARD_ID);
```

### Webhook Server (Express)

```javascript
require('dotenv').config();
const express = require('express');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// Webhook secret (from Miro)
const WEBHOOK_SECRET = process.env.MIRO_WEBHOOK_SECRET;

function verifySignature(req) {
  const signature = req.get('X-Miro-Request-Signature');
  const hmac = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(req.rawBody)
    .digest('hex');
  
  return signature === `sha256=${hmac}`;
}

app.post('/webhook/miro', (req, res) => {
  // Verify signature
  if (!verifySignature(req)) {
    return res.status(401).send('Unauthorized');
  }
  
  // Acknowledge immediately
  res.status(200).send('OK');
  
  // Process asynchronously
  const event = req.body;
  console.log(`Received ${event.type} event`);
  
  if (event.type === 'item.created') {
    console.log(`New item: ${event.data.title}`);
    // Handle item creation
  } else if (event.type === 'item.updated') {
    console.log(`Updated item: ${event.data.id}`);
    // Handle item update
  }
});

app.listen(3000, () => console.log('Webhook server listening on port 3000'));
```

---

## Python

### Setup

```bash
pip install requests python-dotenv
```

### Get All Boards

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('MIRO_TOKEN')
BASE_URL = 'https://api.miro.com/v2'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

def get_all_boards():
    response = requests.get(f'{BASE_URL}/boards', headers=headers)
    response.raise_for_status()
    
    boards = response.json()['data']
    for board in boards:
        print(f"{board['name']} ({board['id']})")

get_all_boards()
```

### Create Items from CSV

```python
import csv
import requests

TOKEN = os.getenv('MIRO_TOKEN')
BOARD_ID = os.getenv('MIRO_BOARD_ID')
BASE_URL = 'https://api.miro.com/v2'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

def import_from_csv(filename):
    items = []
    x, y = 0, 0
    
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append({
                'type': 'CARD',
                'title': row['title'],
                'description': row.get('description', ''),
                'position': {'x': x, 'y': y}
            })
            x += 250  # Horizontal spacing
    
    # Create items in batch
    response = requests.post(
        f'{BASE_URL}/boards/{BOARD_ID}/items/batch',
        json={'items': items},
        headers=headers
    )
    response.raise_for_status()
    
    created = response.json()['items']
    print(f'Created {len(created)} items')

import_from_csv('tasks.csv')
```

### Webhook Handler (Flask)

```python
from flask import Flask, request
import hmac
import hashlib
import os

app = Flask(__name__)
WEBHOOK_SECRET = os.getenv('MIRO_WEBHOOK_SECRET')

def verify_signature(req):
    signature = req.headers.get('X-Miro-Request-Signature')
    hmac_obj = hmac.new(
        WEBHOOK_SECRET.encode(),
        req.data,
        hashlib.sha256
    )
    expected = f"sha256={hmac_obj.hexdigest()}"
    return signature == expected

@app.route('/webhook/miro', methods=['POST'])
def webhook():
    if not verify_signature(request):
        return 'Unauthorized', 401
    
    # Acknowledge immediately
    resp = Response('OK', status=200)
    resp.call_on_close(lambda: handle_event(request.json))
    return resp

def handle_event(event):
    print(f"Received {event['type']} event")
    
    if event['type'] == 'item.created':
        print(f"New item: {event['data']['title']}")
    elif event['type'] == 'comment.created':
        print(f"New comment: {event['data']['content']}")

if __name__ == '__main__':
    app.run(port=3000)
```

---

## Real-World Scenarios

### Sync Jira to Miro

```javascript
async function syncJiraToMiro() {
  // 1. Fetch open issues from Jira
  const jiraIssues = await fetchJiraIssues();
  
  // 2. Create or update board items
  const items = jiraIssues.map(issue => ({
    type: 'CARD',
    title: `[${issue.key}] ${issue.fields.summary}`,
    description: issue.fields.description,
    style: {
      fillColor: getColorByPriority(issue.fields.priority.name)
    }
  }));
  
  // 3. Batch create on Miro
  await miro.post(`/boards/${boardId}/items/batch`, { items });
  
  console.log(`Synced ${items.length} Jira issues to Miro`);
}
```

### Auto-Generate Workflow Diagram

```javascript
async function generateWorkflow(steps) {
  const boardRes = await miro.post('/boards', {
    name: 'Auto-Generated Workflow'
  });
  
  const boardId = boardRes.data.id;
  const items = [];
  const connectors = [];
  
  steps.forEach((step, index) => {
    const x = index * 300;
    
    // Shape for each step
    items.push({
      type: 'SHAPE',
      shape: 'rectangle',
      title: step.name,
      position: { x, y: 0 },
      geometry: { width: 250, height: 100 }
    });
    
    // Connector to next step
    if (index < steps.length - 1) {
      connectors.push({
        type: 'CONNECTOR',
        source: { id: `item-${index}` },
        target: { id: `item-${index + 1}` }
      });
    }
  });
  
  await miro.post(`/boards/${boardId}/items/batch`, {
    items: [...items, ...connectors]
  });
  
  console.log(`Created workflow with ${items.length} steps`);
}
```

