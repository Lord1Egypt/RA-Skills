# n8n Verified Node Type Catalog

## CRITICAL: Only use these exact `type` values. Never invent node types.

## Trigger Nodes

| Node | type | typeVersion |
|------|------|-------------|
| Manual Trigger | `n8n-nodes-base.manualTrigger` | 1 |
| Schedule Trigger | `n8n-nodes-base.scheduleTrigger` | 1 |
| Webhook | `n8n-nodes-base.webhook` | 2 |
| Gmail Trigger | `n8n-nodes-base.gmailTrigger` | 1 |
| Telegram Trigger | `n8n-nodes-base.telegramTrigger` | 1 |
| GitHub Trigger | `n8n-nodes-base.githubTrigger` | 1 |
| Error Trigger | `n8n-nodes-base.errorTrigger` | 1 |

## Core Logic Nodes

| Node | type | typeVersion |
|------|------|-------------|
| IF | `n8n-nodes-base.if` | 2 |
| Switch | `n8n-nodes-base.switch` | 3 |
| Merge | `n8n-nodes-base.merge` | 3 |
| Split In Batches | `n8n-nodes-base.splitInBatches` | 3 |
| Code | `n8n-nodes-base.code` | 2 |
| Set | `n8n-nodes-base.set` | 3 |
| HTTP Request | `n8n-nodes-base.httpRequest` | 4 |
| Respond to Webhook | `n8n-nodes-base.respondToWebhook` | 1 |
| Wait | `n8n-nodes-base.wait` | 1 |
| Stop And Error | `n8n-nodes-base.stopAndError` | 1 |
| Execute Workflow | `n8n-nodes-base.executeWorkflow` | 1 |
| No-Op | `n8n-nodes-base.noOp` | 1 |

## AI / LangChain Nodes

| Node | type | typeVersion |
|------|------|-------------|
| AI Agent | `@n8n/n8n-nodes-langchain.agent` | 1 |
| Basic LLM Chain | `@n8n/n8n-nodes-langchain.chainLlm` | 1 |
| Summarization Chain | `@n8n/n8n-nodes-langchain.chainSummarization` | 2 |
| Retrieval QA Chain | `@n8n/n8n-nodes-langchain.chainRetrievalQa` | 1 |
| OpenAI Chat Model | `@n8n/n8n-nodes-langchain.lmChatOpenAi` | 1 |
| Anthropic Chat Model | `@n8n/n8n-nodes-langchain.lmChatAnthropic` | 1 |
| Ollama Chat Model | `@n8n/n8n-nodes-langchain.lmChatOllama` | 1 |
| Google Gemini Chat | `@n8n/n8n-nodes-langchain.lmChatGoogleGemini` | 1 |
| OpenAI Embeddings | `@n8n/n8n-nodes-langchain.embeddingsOpenAi` | 1 |
| Buffer Window Memory | `@n8n/n8n-nodes-langchain.memoryBufferWindow` | 1 |
| Postgres Chat Memory | `@n8n/n8n-nodes-langchain.memoryPostgresChat` | 1 |
| Redis Chat Memory | `@n8n/n8n-nodes-langchain.memoryRedisChat` | 1 |
| Pinecone Vector Store | `@n8n/n8n-nodes-langchain.vectorStorePinecone` | 1 |
| Postgres Vector Store | `@n8n/n8n-nodes-langchain.vectorStorePostgres` | 1 |
| Qdrant Vector Store | `@n8n/n8n-nodes-langchain.vectorStoreQdrant` | 1 |
| In-Memory Vector Store | `@n8n/n8n-nodes-langchain.vectorStoreInMemory` | 1 |
| Document Loader | `@n8n/n8n-nodes-langchain.documentDefaultDataLoader` | 1 |
| Character Text Splitter | `@n8n/n8n-nodes-langchain.textSplitterCharacterTextSplitter` | 1 |
| Recursive Text Splitter | `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter` | 1 |
| Structured Output Parser | `@n8n/n8n-nodes-langchain.outputParserStructured` | 1 |
| Auto-fixing Output Parser | `@n8n/n8n-nodes-langchain.outputParserAutofixing` | 1 |
| Tool: Calculator | `@n8n/n8n-nodes-langchain.toolCalculator` | 1 |
| Tool: Code | `@n8n/n8n-nodes-langchain.toolCode` | 1 |
| Tool: HTTP Request | `@n8n/n8n-nodes-langchain.toolHttpRequest` | 1 |
| Tool: Wikipedia | `@n8n/n8n-nodes-langchain.toolWikipedia` | 1 |
| Tool: Workflow | `@n8n/n8n-nodes-langchain.toolWorkflow` | 1 |
| Tool: Vector Store | `@n8n/n8n-nodes-langchain.toolVectorStore` | 1 |

## Integration Nodes

| Node | type |
|------|------|
| Gmail | `n8n-nodes-base.gmail` |
| Slack | `n8n-nodes-base.slack` |
| Telegram | `n8n-nodes-base.telegram` |
| Discord | `n8n-nodes-base.discord` |
| Google Sheets | `n8n-nodes-base.googleSheets` |
| Notion | `n8n-nodes-base.notion` |
| Airtable | `n8n-nodes-base.airtable` |
| Postgres | `n8n-nodes-base.postgres` |
| MySQL | `n8n-nodes-base.mySql` |
| MongoDB | `n8n-nodes-base.mongoDb` |
| Redis | `n8n-nodes-base.redis` |
| Supabase | `n8n-nodes-base.supabase` |
| Google Drive | `n8n-nodes-base.googleDrive` |
| GitHub | `n8n-nodes-base.github` |
| Jira | `n8n-nodes-base.jira` |
| Linear | `n8n-nodes-base.linear` |
| Stripe | `n8n-nodes-base.stripe` |
| HubSpot | `n8n-nodes-base.hubspot` |
| Microsoft Teams | `n8n-nodes-base.microsoftTeams` |
| SendGrid | `n8n-nodes-base.sendGrid` |
| Twilio | `n8n-nodes-base.twilio` |
| AWS S3 | `n8n-nodes-base.awsS3` |

## HALLUCINATION RED FLAGS — These DO NOT exist:

```
n8n-nodes-base.openAI
n8n-nodes-base.chatGPT
n8n-nodes-base.llm
n8n-nodes-base.aiAgent
n8n-nodes-base.langchain
n8n-nodes-base.anthropic
@n8n/n8n-nodes-langchain.openAiChat
@n8n/n8n-nodes-langchain.chatModel
@n8n/n8n-nodes-langchain.memory
n8n-nodes-base.functionItem
```

## AI Connection Types

| Type | Used For |
|------|----------|
| `ai_languageModel` | LLM models -> chains/agents |
| `ai_memory` | Memory nodes -> agents |
| `ai_tool` | Tool nodes -> agents |
| `ai_vectorStore` | Vector stores -> retrieval chains |
| `ai_document` | Document loaders -> vector stores |
| `ai_textSplitter` | Text splitters -> document loaders |
| `ai_embedding` | Embedding models -> vector stores |
| `ai_outputParser` | Output parsers -> chains |

Sub-nodes connect FROM themselves TO their parent. Never via `main`.
