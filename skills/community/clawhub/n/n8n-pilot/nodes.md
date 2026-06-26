# Core Node Catalog — n8n

Complete reference of n8n node types organized by category. For node-specific parameters, consult https://docs.n8n.io/integrations/builtin/

## Trigger Nodes (Start Workflows)

| Node | Type | Description | Key Parameters |
|------|------|-------------|---------------|
| Manual Trigger | Core | Click-to-run, one-off testing | None |
| Webhook | Core | HTTP endpoint for external systems | path, method, authentication, responseMode |
| Schedule Trigger | Core | Cron/interval-based scheduling | rule (cron/interval), timezone |
| Email Trigger (IMAP) | App | New email detection | mailbox, folder, filter |
| Polling Trigger | App | Periodic API polling | URL, interval, pagination |
| Workflow Trigger | Core | Called by parent workflow (sub-workflows) | None |
| Error Trigger | Core | Fires when any workflow errors | None (separate workflow) |
| Execute Workflow Trigger | Core | Triggered by Execute Workflow node | None |

## Flow Control Nodes

| Node | Description | Key Parameters |
|------|-------------|---------------|
| IF | Binary conditional branching | conditions (boolean/string/number) |
| Switch | Multi-way branching (2+ outputs) | rules, output indices |
| Merge | Combine data from multiple branches | mode (append/mergeByPosition/mergeByKey) |
| Split In Batches | Process large datasets in chunks | batchSize (ALWAYS set this!) |
| Loop Over Items | Iterate items one by one | — |
| Wait | Delay execution | amount, unit, resumeAt |
| No Operation | Passthrough (placeholder/routing) | — |
| Set | Add/modify/remove fields | assignments (name, value, type) |
| Remove Duplicates | Deduplicate items | fields to compare |

## Data Transformation Nodes

| Node | Description | Key Parameters |
|------|-------------|---------------|
| Code (JavaScript) | Custom logic and transformation | jsCode, language |
| HTML Extract | Parse HTML with CSS selectors | source, extractionValues |
| XML | Parse/serialize XML | mode (parse/compose) |
| Spreadsheet File | Read/write CSV, XLSX | fileFormat, options |
| Date & Time | Format, convert, manipulate dates | format, timezone |
| Crypto | Hash, encrypt, HMAC, sign | algorithm, key |
| Markdown | Convert markdown to HTML | mode |
| JQ | JSON transformation with jq expressions | jqString |

## Communication Nodes

| Node | Description | Auth Method |
|------|-------------|-------------|
| Gmail | Send/read emails | OAuth2 |
| Email (SMTP) | Send emails via SMTP | SMTP credentials |
| Telegram | Send messages, photos, files | Bot token |
| Slack | Messages, channels, files | OAuth2 / Bot token |
| Discord | Messages, webhooks | Bot token / Webhook URL |
| Microsoft Teams | Messages, channels | OAuth2 |
| WhatsApp Business | Send template messages | API key |

## Database Nodes

| Node | Description | Auth Method |
|------|-------------|-------------|
| PostgreSQL | Query, insert, update, delete | Connection string |
| MySQL | Query, insert, update, delete | Connection string |
| MongoDB | Find, insert, update, aggregate | Connection string |
| Redis | Get, set, delete, publish | Connection string |
| Snowflake | Query, insert | Account + credentials |
| Microsoft SQL Server | Query, insert, update | Connection string |
| SQLite | Query local SQLite files | File path |

## API & HTTP Nodes

| Node | Description | Key Parameters |
|------|-------------|---------------|
| HTTP Request | Any REST/GraphQL API call | URL, method, headers, auth, body, pagination |
| GraphQL | GraphQL queries | endpoint, query, variables |
| WebSocket | Real-time connections | URL, protocol |
| MQTT | IoT messaging | broker, topic, payload |

## AI & LLM Nodes

| Node | Description | Auth Method |
|------|-------------|-------------|
| OpenAI | GPT-4, DALL-E, Whisper | API key |
| Google Gemini (PaLM) | Gemini Pro, embeddings | API key |
| Hugging Face | Models, inference | API token |
| LangChain | Chain orchestrations | Depends on sub-nodes |
| Azure OpenAI | OpenAI via Azure | API key + endpoint |
| Anthropic (Claude) | Claude models | API key |

## File & Storage Nodes

| Node | Description | Key Parameters |
|------|-------------|---------------|
| Google Drive | Upload, download, list | OAuth2 |
| Dropbox | Upload, download, list | OAuth2 |
| AWS S3 | Upload, download, list | Access key + secret |
| SFTP | Remote file operations | SSH credentials |
| Read/Write File | Local filesystem | filePath, operation |

## Utility Nodes

| Node | Description | Key Parameters |
|------|-------------|---------------|
| Execute Command | Run shell commands | command |
| Execute Workflow | Call sub-workflow | workflowId, mode |
| Respond to Webhook | Send HTTP response | respondWith, responseBody |
| Item Lists | Sum, count, group items | aggregateFunction |
| Filter | Remove items matching conditions | conditions |
| Sort | Sort items by field | sortFieldsUi |
| Limit | Cap number of items | maxItems |

## Community Nodes

Install via `npm install` in n8n container:
```bash
docker exec n8n npm install n8n-nodes-PACKAGE_NAME
docker restart n8n
```

Browse available: https://www.npmjs.com/search?q=n8n-nodes