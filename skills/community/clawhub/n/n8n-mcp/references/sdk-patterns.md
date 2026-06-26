# n8n Workflow SDK Patterns

## Core Imports

```typescript
import { workflow, trigger, node, expression } from 'n8n-workflow-sdk';
```

## Trigger Types

### Schedule Trigger

```typescript
trigger.schedule({
  name: 'Daily Trigger',
  rule: { interval: [{ field: 'hours', hoursInterval: 24 }] }
})

// Cron expression
trigger.schedule({
  name: 'Cron Trigger',
  rule: { type: 'cron', cronExpression: '0 9 * * 1-5' }  // 9am weekdays
})
```

### Webhook Trigger

```typescript
trigger.webhook({
  name: 'Webhook',
  httpMethod: 'POST',
  path: 'my-webhook',
  authentication: 'none'
})
```

### Manual Trigger

```typescript
trigger.manual({
  name: 'Manual Trigger'
})
```

### Form Trigger

```typescript
trigger.form({
  name: 'Form Trigger',
  formTitle: 'Contact Form',
  formDescription: 'Submit your inquiry',
  formFields: [
    { fieldLabel: 'Name', fieldType: 'text' },
    { fieldLabel: 'Email', fieldType: 'email' },
    { fieldLabel: 'Message', fieldType: 'textarea' }
  ]
})
```

### Chat Trigger

```typescript
trigger.chat({
  name: 'Chat Trigger',
  initialMessage: 'Hello! How can I help you today?'
})
```

## Common Nodes

### Set (Data Transformation)

```typescript
node.set({
  name: 'Transform Data',
  values: {
    message: 'Hello {{ $json.name }}',
    timestamp: '={{ $now.toISO() }}'
  },
  options: { keepOnlySetup: true }
})
```

### HTTP Request

```typescript
node.httpRequest({
  name: 'Fetch API',
  method: 'GET',
  url: 'https://api.example.com/data',
  authentication: 'predefinedCredentialType',
  nodeCredentialType: 'httpHeaderAuth'
})
```

### Code Node

```typescript
node.code({
  name: 'Custom Logic',
  language: 'javaScript',
  code: `
    const items = $input.all();
    const result = items.map(item => ({
      json: { ...item.json, processed: true }
    }));
    return result;
  `
})
```

### If Condition

```typescript
node.if({
  name: 'Check Condition',
  conditions: {
    string: [{
      value1: '={{ $json.status }}',
      operation: 'equals',
      value2: 'active'
    }]
  }
})
```

### Switch (Multiple Conditions)

```typescript
node.switch({
  name: 'Route by Type',
  mode: 'rules',
  rules: [
    { output: 0, conditions: { string: [{ value1: '={{ $json.type }}', operation: 'equals', value2: 'email' }] } },
    { output: 1, conditions: { string: [{ value1: '={{ $json.type }}', operation: 'equals', value2: 'sms' }] } }
  ]
})
```

### Merge

```typescript
node.merge({
  name: 'Combine Data',
  mode: 'combine',
  combinationMode: 'mergeByPosition',
  options: {}
})
```

### Filter

```typescript
node.filter({
  name: 'Filter Items',
  conditions: {
    boolean: [{
      value1: '={{ $json.active }}',
      operation: 'equals',
      value2: true
    }]
  }
})
```

## Service Nodes

### Slack

```typescript
node.slack({
  name: 'Send Message',
  resource: 'message',
  operation: 'send',
  channel: '#general',
  text: '={{ $json.message }}'
})
```

### Gmail

```typescript
node.gmail({
  name: 'Send Email',
  resource: 'message',
  operation: 'send',
  to: 'user@example.com',
  subject: 'Notification',
  message: '={{ $json.body }}'
})
```

### Discord

```typescript
node.discord({
  name: 'Post to Discord',
  resource: 'message',
  operation: 'post',
  channelId: '123456789',
  content: '={{ $json.message }}'
})
```

### Telegram

```typescript
node.telegram({
  name: 'Send Telegram Message',
  resource: 'message',
  operation: 'send',
  chatId: '-1001234567890',
  text: '={{ $json.message }}'
})
```

### Microsoft Teams

```typescript
node.microsoftTeams({
  name: 'Post to Teams',
  resource: 'message',
  operation: 'create',
  teamId: 'xxx',
  channelId: 'xxx',
  content: '={{ $json.message }}'
})
```

## AI & LLM Nodes

### OpenAI Chat

```typescript
node.openAi({
  name: 'Generate Text',
  resource: 'chat',
  operation: 'message',
  model: 'gpt-4',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: '={{ $json.prompt }}' }
  ]
})
```

### Anthropic Claude

```typescript
node.anthropic({
  name: 'Claude Response',
  resource: 'message',
  operation: 'create',
  model: 'claude-3-opus-20240229',
  messages: [
    { role: 'user', content: '={{ $json.prompt }}' }
  ],
  maxTokens: 1024
})
```

## Database Nodes

### PostgreSQL

```typescript
node.postgres({
  name: 'Query Database',
  operation: 'executeQuery',
  query: 'SELECT * FROM users WHERE id = {{ $json.userId }}'
})
```

### MySQL

```typescript
node.mySql({
  name: 'Insert Data',
  operation: 'insert',
  table: 'logs',
  columns: ['message', 'level', 'timestamp'],
  values: ['={{ $json.message }}', '={{ $json.level }}', '={{ $now.toISO() }}']
})
```

### MongoDB

```typescript
node.mongoDb({
  name: 'Find Documents',
  operation: 'find',
  collection: 'users',
  query: { status: 'active' }
})
```

## File Operations

### Read File

```typescript
node.readBinaryFile({
  name: 'Read File',
  fileSelector: '={{ $json.filePath }}'
})
```

### Write File

```typescript
node.writeBinaryFile({
  name: 'Write File',
  fileName: 'output.json',
  data: '={{ $json.content }}'
})
```

### Spreadsheet (Excel/CSV)

```typescript
node.spreadsheetFile({
  name: 'Read Spreadsheet',
  operation: 'read',
  fileSelector: '={{ $json.fileId }}',
  options: { sheetName: 'Sheet1' }
})
```

## Expressions

### Accessing Data

```typescript
// Current node data
'={{ $json.fieldName }}'

// Previous node data
'={{ $node["Previous Node"].json.fieldName }}'

// All items
'={{ $input.all() }}'

// First item
'={{ $input.first().json }}'

// Item by index
'={{ $input.item(0).json }}'
```

### Built-in Functions

```typescript
// Date/Time
'={{ $now.toISO() }}'           // Current timestamp
'={{ $now.plus({days: 1}) }}'   // Tomorrow
'={{ $now.minus({hours: 1}) }}' // 1 hour ago
'={{ $now.format("yyyy-MM-dd") }}' // Formatted date

// String
'={{ $json.name.toUpperCase() }}'
'={{ $json.text.substring(0, 100) }}'
'={{ $json.text.replace("old", "new") }}'
'={{ $json.text.split(",") }}'

// Array
'={{ $json.items.length }}'
'={{ $json.items.filter(i => i.active) }}'
'={{ $json.items.map(i => i.name) }}'
'={{ $json.items.find(i => i.id === "123") }}'
'={{ $json.items.sort((a, b) => a.name.localeCompare(b.name)) }}'

// Math
'={{ $json.price * 1.1 }}'      // Add 10%
'={{ Math.round($json.value) }}'
'={{ Math.floor($json.value) }}'

// Object
'={{ Object.keys($json) }}'
'={{ Object.values($json) }}'
'={{ $json.hasOwnProperty("field") }}'
```

## Connections

```typescript
connections: [
  // Simple: A → B
  { from: 'Node A', to: 'Node B' },

  // With output/input index
  { from: 'Node A', to: 'Node B', fromOutput: 0, toInput: 0 },

  // If node: true/false branches
  { from: 'Check', to: 'Action A', fromOutput: 0 },  // true
  { from: 'Check', to: 'Action B', fromOutput: 1 }   // false

  // Switch node: multiple outputs
  { from: 'Route', to: 'Email Handler', fromOutput: 0 },
  { from: 'Route', to: 'SMS Handler', fromOutput: 1 },
  { from: 'Route', to: 'Default Handler', fromOutput: 2 }
]
```

## Error Handling

```typescript
// Continue on error
node.httpRequest({
  name: 'Fetch API',
  url: 'https://api.example.com/data',
  options: { continueOnFail: true }
})

// Check for errors in subsequent node
node.set({
  name: 'Handle Error',
  values: {
    error: '={{ $json.error?.message || "Unknown error" }}',
    hasError: '={{ $json.error !== undefined }}'
  }
})
```

## Complete Workflow Example

```typescript
import { workflow, trigger, node } from 'n8n-workflow-sdk';

export default workflow({
  name: 'Content Publishing Pipeline',
  description: 'Process and publish content to multiple platforms',
  nodes: [
    // Trigger: Webhook receives content
    trigger.webhook({
      name: 'Content Webhook',
      httpMethod: 'POST',
      path: 'publish-content',
      authentication: 'headerAuth'
    }),

    // Validate content
    node.if({
      name: 'Has Required Fields',
      conditions: {
        string: [
          { value1: '={{ $json.title }}', operation: 'isNotEmpty' },
          { value1: '={{ $json.body }}', operation: 'isNotEmpty' }
        ]
      }
    }),

    // Transform for different platforms
    node.set({
      name: 'Format for Twitter',
      values: {
        text: '={{ $json.title.substring(0, 280) }}',
        platform: 'twitter'
      }
    }),

    node.set({
      name: 'Format for LinkedIn',
      values: {
        text: '={{ $json.title }}\n\n{{ $json.body.substring(0, 700) }}',
        platform: 'linkedin'
      }
    }),

    // Send notifications
    node.slack({
      name: 'Notify Team',
      resource: 'message',
      operation: 'send',
      channel: '#content',
      text: 'New content published: {{ $json.title }}'
    })
  ],
  connections: [
    { from: 'Content Webhook', to: 'Has Required Fields' },
    { from: 'Has Required Fields', to: 'Format for Twitter', fromOutput: 0 },
    { from: 'Has Required Fields', to: 'Format for LinkedIn', fromOutput: 0 },
    { from: 'Format for Twitter', to: 'Notify Team' },
    { from: 'Format for LinkedIn', to: 'Notify Team' }
  ]
});
```

## Best Practices

1. **Always validate** before creating: `validate_workflow(code)`
2. **Get node types** before writing: `get_node_types(nodeIds)`
3. **Use expressions** for dynamic values
4. **Test with pin data** before activating
5. **Add descriptions** for complex workflows
6. **Use meaningful node names** for easier debugging
7. **Handle errors** with `continueOnFail` option
8. **Keep workflows focused** - split complex logic into multiple workflows
