# n8n Workflow Templates

Ready-to-use workflow JSON patterns. Copy, customize, deploy via API.

## Template: Minimal Webhook -> Respond

```json
{
  "name": "Webhook Echo",
  "nodes": [
    {
      "id": "1", "name": "Webhook", "type": "n8n-nodes-base.webhook", "typeVersion": 2,
      "position": [250, 300],
      "parameters": { "httpMethod": "POST", "path": "echo", "responseMode": "responseNode", "options": {} }
    },
    {
      "id": "2", "name": "Respond", "type": "n8n-nodes-base.respondToWebhook", "typeVersion": 1,
      "position": [500, 300],
      "parameters": { "respondWith": "json", "responseBody": "={{ JSON.stringify($json) }}", "options": { "responseCode": 200 } }
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Respond", "type": "main", "index": 0 }]] }
  },
  "settings": { "executionOrder": "v1" }
}
```

## Template: Schedule -> HTTP -> Code -> Slack

```json
{
  "name": "Scheduled API Check",
  "nodes": [
    {
      "id": "1", "name": "Schedule", "type": "n8n-nodes-base.scheduleTrigger", "typeVersion": 1,
      "position": [250, 300],
      "parameters": { "rule": { "interval": [{ "field": "cronExpression", "expression": "0 9 * * 1-5" }] } }
    },
    {
      "id": "2", "name": "Fetch Data", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4,
      "position": [500, 300],
      "parameters": { "method": "GET", "url": "https://api.example.com/status", "options": {} }
    },
    {
      "id": "3", "name": "Process", "type": "n8n-nodes-base.code", "typeVersion": 2,
      "position": [750, 300],
      "parameters": {
        "mode": "runOnceForAllItems", "language": "javaScript",
        "jsCode": "return items.map(i => ({ json: { summary: `Status: ${i.json.status}` } }));"
      }
    },
    {
      "id": "4", "name": "Notify Slack", "type": "n8n-nodes-base.slack", "typeVersion": 2,
      "position": [1000, 300],
      "parameters": {
        "operation": "message", "select": "channel",
        "channelId": { "__rl": true, "value": "#alerts", "mode": "name" },
        "text": "={{ $json.summary }}", "otherOptions": {}
      },
      "credentials": { "slackApi": { "id": "CRED_ID", "name": "Slack" } }
    }
  ],
  "connections": {
    "Schedule": { "main": [[{ "node": "Fetch Data", "type": "main", "index": 0 }]] },
    "Fetch Data": { "main": [[{ "node": "Process", "type": "main", "index": 0 }]] },
    "Process": { "main": [[{ "node": "Notify Slack", "type": "main", "index": 0 }]] }
  },
  "settings": { "executionOrder": "v1" }
}
```

## Template: AI Agent with Memory + Tools

```json
{
  "name": "AI Agent Chat",
  "nodes": [
    {
      "id": "1", "name": "Webhook", "type": "n8n-nodes-base.webhook", "typeVersion": 2,
      "position": [250, 300],
      "parameters": { "httpMethod": "POST", "path": "agent", "responseMode": "responseNode", "options": {} }
    },
    {
      "id": "2", "name": "AI Agent", "type": "@n8n/n8n-nodes-langchain.agent", "typeVersion": 1,
      "position": [550, 300],
      "parameters": {
        "agent": "toolsAgent", "promptType": "define",
        "text": "={{ $json.body.message }}",
        "options": { "systemMessage": "You are a helpful assistant.", "maxIterations": 10 }
      }
    },
    {
      "id": "3", "name": "OpenAI", "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi", "typeVersion": 1,
      "position": [400, 550],
      "parameters": { "model": "gpt-4o", "options": { "temperature": 0.7 } },
      "credentials": { "openAiApi": { "id": "CRED_ID", "name": "OpenAI API" } }
    },
    {
      "id": "4", "name": "Memory", "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow", "typeVersion": 1,
      "position": [550, 550],
      "parameters": { "sessionIdType": "customKey", "sessionKey": "={{ $json.body.sessionId ?? 'default' }}", "contextWindowLength": 20 }
    },
    {
      "id": "5", "name": "Calculator", "type": "@n8n/n8n-nodes-langchain.toolCalculator", "typeVersion": 1,
      "position": [700, 550], "parameters": {}
    },
    {
      "id": "6", "name": "Respond", "type": "n8n-nodes-base.respondToWebhook", "typeVersion": 1,
      "position": [850, 300],
      "parameters": { "respondWith": "json", "responseBody": "={{ JSON.stringify({ reply: $json.output }) }}", "options": { "responseCode": 200 } }
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "AI Agent", "type": "main", "index": 0 }]] },
    "OpenAI": { "ai_languageModel": [[{ "node": "AI Agent", "type": "ai_languageModel", "index": 0 }]] },
    "Memory": { "ai_memory": [[{ "node": "AI Agent", "type": "ai_memory", "index": 0 }]] },
    "Calculator": { "ai_tool": [[{ "node": "AI Agent", "type": "ai_tool", "index": 0 }]] },
    "AI Agent": { "main": [[{ "node": "Respond", "type": "main", "index": 0 }]] }
  },
  "settings": { "executionOrder": "v1" }
}
```

## Template: IF Branch with Error Handling

```json
{
  "connections": {
    "IF Check": {
      "main": [
        [{ "node": "Success Path", "type": "main", "index": 0 }],
        [{ "node": "Error Handler", "type": "main", "index": 0 }]
      ]
    }
  }
}
```
IF node ALWAYS has 2 output arrays: index 0 = true, index 1 = false.

## n8n Expression Quick Reference

```javascript
$json.fieldName                              // Current node input
$('Node Name').item.json.field               // Specific node reference
$json.body?.message ?? 'default'             // Safe access with fallback
JSON.stringify({ result: $json.output })     // JSON for response bodies
$now.toISO()                                 // Current timestamp
$execution.id                                // Execution ID
$env.MY_KEY                                  // Environment variable
```
