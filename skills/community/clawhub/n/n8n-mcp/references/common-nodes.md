# Common n8n Nodes Reference

Quick reference for frequently used n8n nodes with their IDs and discriminators.

## Trigger Nodes

| Node | ID | Description |
|------|------|------|
| Schedule Trigger | `n8n-nodes-base.scheduleTrigger` | Time-based triggers (interval or cron) |
| Webhook | `n8n-nodes-base.webhook` | HTTP webhook endpoint |
| Manual Trigger | `n8n-nodes-base.manualTrigger` | Manual execution from UI |
| Form Trigger | `n8n-nodes-base.formTrigger` | Form submission trigger |
| Chat Trigger | `@n8n/n8n-nodes-langchain.chatTrigger` | AI chat interface trigger |

## Logic Nodes

| Node | ID | Description |
|------|------|------|
| If | `n8n-nodes-base.if` | Conditional branching (true/false) |
| Switch | `n8n-nodes-base.switch` | Multiple conditions routing |
| Merge | `n8n-nodes-base.merge` | Combine data streams |
| Split In Batches | `n8n-nodes-base.splitInBatches` | Batch processing |
| Loop Over Items | `n8n-nodes-base.split` | Iterate over items |
| Filter | `n8n-nodes-base.filter` | Filter items by condition |
| Wait | `n8n-nodes-base.wait` | Delay execution |

## Transform Nodes

| Node | ID | Description |
|------|------|------|
| Set | `n8n-nodes-base.set` | Set/transform values |
| Code | `n8n-nodes-base.code` | Custom JavaScript/Python |
| Edit Fields | `n8n-nodes-base.editFields` | Rename/remove fields |
| Sort | `n8n-nodes-base.sort` | Sort items |
| Remove Duplicates | `n8n-nodes-base.removeDuplicates` | Deduplicate items |
| Limit | `n8n-nodes-base.limit` | Limit number of items |
| Aggregate | `n8n-nodes-base.aggregate` | Aggregate items |

## HTTP & API

| Node | ID | Description |
|------|------|------|
| HTTP Request | `n8n-nodes-base.httpRequest` | Generic HTTP calls |
| GraphQL | `n8n-nodes-base.graphql` | GraphQL queries |

## Communication Nodes

| Node | ID | Resource | Operations |
|------|------|----------|------------|
| Slack | `n8n-nodes-base.slack` | message, file, channel | send, upload, create |
| Discord | `n8n-nodes-base.discord` | message, channel | post, create |
| Telegram | `n8n-nodes-base.telegram` | message, chat | send, get |
| Gmail | `n8n-nodes-base.gmail` | message, label, draft | send, get, create |
| Email (SMTP) | `n8n-nodes-base.emailSend` | - | send |
| Microsoft Teams | `n8n-nodes-base.microsoftTeams` | message, channel, team | create, get, post |
| WeChat | `n8n-nodes-base.weChat` | message | send |
| DingTalk | `n8n-nodes-base.dingTalk` | message | send |
| Feishu/Lark | `n8n-nodes-base.lark` | message, document | send, create |

## Database Nodes

| Node | ID | Description |
|------|------|------|
| PostgreSQL | `n8n-nodes-base.postgres` | PostgreSQL operations |
| MySQL | `n8n-nodes-base.mySql` | MySQL operations |
| MongoDB | `n8n-nodes-base.mongoDb` | MongoDB operations |
| Redis | `n8n-nodes-base.redis` | Redis operations |
| Supabase | `n8n-nodes-base.supabase` | Supabase operations |
| Notion | `n8n-nodes-base.notion` | Notion database operations |
| Airtable | `n8n-nodes-base.airtable` | Airtable operations |

## File Operations

| Node | ID | Description |
|------|------|------|
| Read Binary File | `n8n-nodes-base.readBinaryFile` | Read files |
| Write Binary File | `n8n-nodes-base.writeBinaryFile` | Write files |
| Spreadsheet File | `n8n-nodes-base.spreadsheetFile` | Excel/CSV read/write |
| JSON | `n8n-nodes-base.convertToFile` | JSON conversion |
| PDF | `n8n-nodes-base.readPdf` | PDF text extraction |
| Image | `n8n-nodes-base.image` | Image manipulation |
| Archive | `n8n-nodes-base.archive` | Zip/unzip files |

## AI & LLM Nodes

| Node | ID | Description |
|------|------|------|
| OpenAI | `n8n-nodes-base.openAi` | GPT models (chat, completion, image) |
| Anthropic | `@n8n/n8n-nodes-langchain.anthropic` | Claude models |
| Google Gemini | `@n8n/n8n-nodes-langchain.googleGemini` | Gemini models |
| LangChain | `@n8n/n8n-nodes-langchain` | LangChain tools |
| AI Agent | `@n8n/n8n-nodes-langchain.agent` | AI agent with tools |
| Vector Store | `@n8n/n8n-nodes-langchain.vectorStore` | Vector database operations |
| Embeddings | `@n8n/n8n-nodes-langchain.embeddings` | Text embeddings |

## Date & Time

| Node | ID | Description |
|------|------|------|
| Date & Time | `n8n-nodes-base.dateTime` | Date operations (format, calculate) |
| Cron | `n8n-nodes-base.cron` | Cron scheduling |
| Sleep | `n8n-nodes-base.sleep` | Delay execution |

## Data Storage

| Node | ID | Description |
|------|------|------|
| Redis | `n8n-nodes-base.redis` | Redis key-value store |
| Key-Value Store | `n8n-nodes-base.keyValueStore` | n8n built-in storage |
| Read/Write Binary | `n8n-nodes-base.readBinaryFile` | File-based storage |

## Content & Media

| Node | ID | Description |
|------|------|------|
| HTML to Markdown | `n8n-nodes-base.htmlToMarkdown` | Convert HTML to MD |
| Markdown | `n8n-nodes-base.markdown` | Markdown operations |
| YouTube | `n8n-nodes-base.youTube` | YouTube API |
| Twitter/X | `n8n-nodes-base.twitter` | Twitter API |
| LinkedIn | `n8n-nodes-base.linkedIn` | LinkedIn API |
| Instagram | `n8n-nodes-base.instagram` | Instagram API |

## Workflow Control

| Node | ID | Description |
|------|------|------|
| Execute Workflow | `n8n-nodes-base.executeWorkflow` | Call another workflow |
| Error Trigger | `n8n-nodes-base.errorTrigger` | Catch workflow errors |
| Stop | `n8n-nodes-base.stop` | Stop workflow execution |
| No-Op | `n8n-nodes-base.noOp` | No operation (placeholder) |

## Search Query Examples

```bash
# Search for specific services
search_nodes(["slack", "gmail", "telegram"])

# Search for triggers
search_nodes(["schedule trigger", "webhook", "form", "chat trigger"])

# Search for logic nodes
search_nodes(["if", "switch", "merge", "code", "set", "filter"])

# Search for AI nodes
search_nodes(["openai", "anthropic", "langchain", "gemini"])

# Search for database nodes
search_nodes(["postgres", "mysql", "mongodb", "redis", "notion"])

# Search for communication nodes
search_nodes(["slack", "discord", "teams", "wechat", "dingtalk", "feishu"])

# Search for file operations
search_nodes(["read file", "write file", "spreadsheet", "pdf"])
```

## Node Type with Discriminators

When calling `get_node_types`, include discriminators from search results:

```json
[
  "n8n-nodes-base.scheduleTrigger",
  {
    "nodeId": "n8n-nodes-base.slack",
    "resource": "message",
    "operation": "send"
  },
  {
    "nodeId": "n8n-nodes-base.openAi",
    "resource": "chat",
    "operation": "message"
  }
]
```

## Common Discriminators

### Slack
- Resource: `message`, `file`, `channel`
- Operations: `send`, `upload`, `create`

### Gmail
- Resource: `message`, `label`, `draft`
- Operations: `send`, `get`, `create`

### OpenAI
- Resource: `chat`, `completion`, `image`, `audio`
- Operations: `message`, `create`, `transcribe`

### HTTP Request
- No discriminators, but has `method` property: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`

### Database Nodes
- Operations: `executeQuery`, `insert`, `update`, `delete`, `select`

## Node Categories for get_suggested_nodes

Available categories:
- `chatbot` - AI chatbot workflows
- `notification` - Alert and notification systems
- `scheduling` - Scheduled tasks and automation
- `data_transformation` - Data processing and transformation
- `data_persistence` - Database and storage operations
- `data_extraction` - Web scraping and data extraction
- `document_processing` - PDF, Word, spreadsheet processing
- `form_input` - Form handling and validation
- `content_generation` - AI content creation
- `triage` - Routing and categorization
- `scraping_and_research` - Web research and data collection
