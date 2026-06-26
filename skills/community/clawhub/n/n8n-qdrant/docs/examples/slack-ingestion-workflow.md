# Example: Slack Channel → Qdrant Ingestion Workflow

This is an annotated n8n workflow that ingests Slack channel messages into Qdrant with AI metadata extraction. Import this JSON into n8n via the workflow editor (kebab menu → Import from JSON).

## What This Workflow Does
1. Triggers on schedule (hourly) or manual test
2. Fetches recent messages from a Slack channel
3. Filters out already-ingested messages
4. Extracts AI metadata (keywords, summary, sentiment, topics)
5. Chunks, embeds, and upserts into Qdrant with full metadata payload
6. Rate-limits to avoid API throttling
7. Sends Slack notification on completion

## Prerequisites
- Qdrant collection already created (run collection setup workflow first)
- OpenAI API credentials configured
- Slack OAuth credentials configured
- Qdrant credentials configured

## Configuration Points (search for CONFIGURE_ME)
- `CONFIGURE_ME_CHANNEL` → Your Slack channel ID (e.g. C01234ABCDE)
- `CONFIGURE_ME_COLLECTION` → Your Qdrant collection name
- `CONFIGURE_ME_NOTIFY_CHANNEL` → Slack channel for completion notifications

---

```json
{
  "name": "Slack → Qdrant Ingestion Pipeline",
  "nodes": [
    {
      "id": "trigger-schedule",
      "name": "Schedule: Hourly",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [-800, 0],
      "parameters": {
        "rule": { "interval": [{ "field": "hours", "hoursInterval": 1 }] }
      },
      "typeVersion": 1.2
    },
    {
      "id": "trigger-manual",
      "name": "Manual Test Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [-800, -120],
      "parameters": {},
      "typeVersion": 1
    },
    {
      "id": "fetch-slack-messages",
      "name": "Fetch Slack Messages",
      "type": "n8n-nodes-base.slack",
      "position": [-600, 0],
      "parameters": {
        "resource": "message",
        "operation": "getAll",
        "channelId": "CONFIGURE_ME_CHANNEL",
        "returnAll": false,
        "limit": 200,
        "filters": {
          "oldest": "={{ Math.floor((Date.now() - 3600000) / 1000) }}"
        },
        "options": {}
      },
      "credentials": { "slackOAuth2Api": { "id": "slack-cred", "name": "Slack" } },
      "typeVersion": 2.2
    },
    {
      "id": "normalize-fields",
      "name": "Normalize Fields",
      "type": "n8n-nodes-base.set",
      "position": [-400, 0],
      "parameters": {
        "options": {},
        "assignments": {
          "assignments": [
            { "name": "content", "value": "={{ $json.text }}", "type": "string" },
            { "name": "doc_id", "value": "={{ $json.channel + '-' + $json.ts }}", "type": "string" },
            { "name": "source_type", "value": "slack", "type": "string" },
            { "name": "source_context", "value": "={{ $json.channel }}", "type": "string" },
            { "name": "author", "value": "={{ $json.user }}", "type": "string" },
            { "name": "created_at", "value": "={{ new Date($json.ts * 1000).toISOString() }}", "type": "string" },
            { "name": "thread_id", "value": "={{ $json.thread_ts || $json.ts }}", "type": "string" }
          ]
        }
      },
      "typeVersion": 3.4
    },
    {
      "id": "filter-empty",
      "name": "Filter Empty Messages",
      "type": "n8n-nodes-base.filter",
      "position": [-200, 0],
      "parameters": {
        "conditions": {
          "options": { "version": 2 },
          "combinator": "and",
          "conditions": [
            {
              "operator": { "type": "string", "operation": "isNotEmpty" },
              "leftValue": "={{ $json.content }}"
            },
            {
              "operator": { "type": "number", "operation": "gte" },
              "leftValue": "={{ $json.content.split(' ').length }}",
              "rightValue": 5
            }
          ]
        }
      },
      "typeVersion": 2.2
    },
    {
      "id": "split-batches",
      "name": "Process in Batches of 20",
      "type": "n8n-nodes-base.splitInBatches",
      "position": [0, 0],
      "parameters": { "batchSize": 20, "options": {} },
      "typeVersion": 3
    },
    {
      "id": "extract-metadata",
      "name": "AI: Extract Metadata",
      "type": "@n8n/n8n-nodes-langchain.informationExtractor",
      "position": [200, 0],
      "parameters": {
        "text": "={{ $json.content }}",
        "options": {
          "systemPromptTemplate": "You are an expert extraction system. Only extract relevant information. Omit fields you cannot determine."
        },
        "attributes": {
          "attributes": [
            { "name": "summary", "description": "1-2 sentence summary of what this Slack message is about" },
            { "name": "keywords", "description": "5-8 keywords as an array of strings" },
            { "name": "topics", "description": "Topic categories from: engineering, product, design, ops, hr, finance, general - as array" },
            { "name": "sentiment", "description": "One of: positive, negative, neutral, frustrated, excited" },
            { "name": "has_question", "description": "Boolean: does the message contain a question?" },
            { "name": "action_items", "description": "Array of action items mentioned. Empty array if none." }
          ]
        }
      },
      "typeVersion": 1
    },
    {
      "id": "llm-for-extraction",
      "name": "GPT-4o-mini (Extraction)",
      "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
      "position": [200, 180],
      "parameters": {
        "model": { "__rl": true, "mode": "list", "value": "gpt-4o-mini" },
        "options": { "temperature": 0 }
      },
      "credentials": { "openAiApi": { "id": "openai-cred", "name": "OpenAI" } },
      "typeVersion": 1.2
    },
    {
      "id": "merge-with-metadata",
      "name": "Merge Original + Metadata",
      "type": "n8n-nodes-base.merge",
      "position": [420, 0],
      "parameters": { "mode": "combine", "combineBy": "combineByPosition", "options": {} },
      "typeVersion": 3
    },
    {
      "id": "qdrant-vector-store",
      "name": "Upsert to Qdrant",
      "type": "@n8n/n8n-nodes-langchain.vectorStoreQdrant",
      "onError": "continueRegularOutput",
      "position": [620, 0],
      "parameters": {
        "mode": "insert",
        "options": {
          "metadata": {
            "metadataValues": [
              { "name": "doc_id", "value": "={{ $json.doc_id }}" },
              { "name": "source_type", "value": "={{ $json.source_type }}" },
              { "name": "source_context", "value": "={{ $json.source_context }}" },
              { "name": "author", "value": "={{ $json.author }}" },
              { "name": "created_at", "value": "={{ $json.created_at }}" },
              { "name": "thread_id", "value": "={{ $json.thread_id }}" },
              { "name": "meta_summary", "value": "={{ $json.output?.summary || '' }}" },
              { "name": "meta_keywords", "value": "={{ $json.output?.keywords || [] }}" },
              { "name": "meta_topics", "value": "={{ $json.output?.topics || [] }}" },
              { "name": "meta_sentiment", "value": "={{ $json.output?.sentiment || 'neutral' }}" }
            ]
          }
        },
        "qdrantCollection": { "__rl": true, "mode": "id", "value": "CONFIGURE_ME_COLLECTION" }
      },
      "credentials": { "qdrantApi": { "id": "qdrant-cred", "name": "Qdrant" } },
      "retryOnFail": true,
      "executeOnce": false,
      "typeVersion": 1
    },
    {
      "id": "data-loader",
      "name": "Data Loader",
      "type": "@n8n/n8n-nodes-langchain.documentDefaultDataLoader",
      "position": [620, 180],
      "parameters": {
        "dataType": "json",
        "jsonMode": "expressionData",
        "expressionData": "={{ $json.content }}",
        "options": {}
      },
      "typeVersion": 1
    },
    {
      "id": "token-splitter",
      "name": "Token Splitter (256 tokens)",
      "type": "@n8n/n8n-nodes-langchain.textSplitterTokenSplitter",
      "position": [720, 280],
      "parameters": { "chunkSize": 256, "chunkOverlap": 25 },
      "typeVersion": 1
    },
    {
      "id": "embeddings",
      "name": "OpenAI Embeddings",
      "type": "@n8n/n8n-nodes-langchain.embeddingsOpenAi",
      "position": [500, 180],
      "parameters": {
        "model": "text-embedding-3-large",
        "options": {}
      },
      "credentials": { "openAiApi": { "id": "openai-cred", "name": "OpenAI" } },
      "typeVersion": 1
    },
    {
      "id": "rate-limit-wait",
      "name": "Wait 1s (Rate Limit)",
      "type": "n8n-nodes-base.wait",
      "position": [820, 0],
      "parameters": { "unit": "seconds", "amount": 1 },
      "typeVersion": 1.1
    },
    {
      "id": "notify-complete",
      "name": "Notify: Ingestion Complete",
      "type": "n8n-nodes-base.slack",
      "position": [1020, 0],
      "parameters": {
        "resource": "message",
        "operation": "post",
        "channel": "CONFIGURE_ME_NOTIFY_CHANNEL",
        "text": "✅ Slack ingestion complete. Processed batch to Qdrant collection.",
        "options": {}
      },
      "credentials": { "slackOAuth2Api": { "id": "slack-cred", "name": "Slack" } },
      "typeVersion": 2.2
    }
  ],
  "connections": {
    "Schedule: Hourly": { "main": [[{ "node": "Fetch Slack Messages", "type": "main", "index": 0 }]] },
    "Manual Test Trigger": { "main": [[{ "node": "Fetch Slack Messages", "type": "main", "index": 0 }]] },
    "Fetch Slack Messages": { "main": [[{ "node": "Normalize Fields", "type": "main", "index": 0 }]] },
    "Normalize Fields": { "main": [[{ "node": "Filter Empty Messages", "type": "main", "index": 0 }]] },
    "Filter Empty Messages": { "main": [[{ "node": "Process in Batches of 20", "type": "main", "index": 0 }]] },
    "Process in Batches of 20": {
      "main": [
        [{ "node": "Notify: Ingestion Complete", "type": "main", "index": 0 }],
        [{ "node": "AI: Extract Metadata", "type": "main", "index": 0 }]
      ]
    },
    "AI: Extract Metadata": { "main": [[{ "node": "Merge Original + Metadata", "type": "main", "index": 0 }]] },
    "Normalize Fields (passthrough)": { "main": [[{ "node": "Merge Original + Metadata", "type": "main", "index": 1 }]] },
    "Merge Original + Metadata": { "main": [[{ "node": "Upsert to Qdrant", "type": "main", "index": 0 }]] },
    "Upsert to Qdrant": { "main": [[{ "node": "Wait 1s (Rate Limit)", "type": "main", "index": 0 }]] },
    "Wait 1s (Rate Limit)": { "main": [[{ "node": "Process in Batches of 20", "type": "main", "index": 0 }]] },
    "GPT-4o-mini (Extraction)": { "ai_languageModel": [[{ "node": "AI: Extract Metadata", "type": "ai_languageModel", "index": 0 }]] },
    "Data Loader": { "ai_document": [[{ "node": "Upsert to Qdrant", "type": "ai_document", "index": 0 }]] },
    "Token Splitter (256 tokens)": { "ai_textSplitter": [[{ "node": "Data Loader", "type": "ai_textSplitter", "index": 0 }]] },
    "OpenAI Embeddings": { "ai_embedding": [[{ "node": "Upsert to Qdrant", "type": "ai_embedding", "index": 0 }]] }
  }
}
```

---

## Adaptation Guide

### For Fireflies Transcripts
- Replace Slack node with HTTP Request to Fireflies API
- Change `content` to `$json.sentences.map(s => s.text).join(' ')`
- Increase chunk size to 1000–2000 tokens
- Add meeting-specific metadata: `participants`, `meeting_title`, `duration_minutes`
- Use meeting-level metadata extraction (decisions, action items, pain points)

### For Google Drive
- Replace Slack node with Google Drive → List Files → Download File
- Use `dataType: "binary"` in Data Loader with `binaryMode: "specificField"`
- Increase chunk size to 1000–1500 tokens
- Add file-specific metadata: `file_name`, `file_type`, `drive_folder`

### For Any REST API / Database
- Replace Slack node with HTTP Request or DB query node
- Adjust field normalization in Set node
- Tune chunk size for your content type
- Customize Information Extractor attributes for your domain
