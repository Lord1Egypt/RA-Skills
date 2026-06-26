# RAGFlow CLI Reference

All CLI commands end with a semicolon (`;`). Prompt: `ragflow>`.

## Server & User Commands

### PING — Test Connection

```
PING;
```

Tests connectivity to the RAGFlow server.

### SHOW CURRENT USER — Display User Info

```
SHOW CURRENT USER;
```

Shows currently logged-in user information.

---

## Model Provider Management

### CREATE MODEL PROVIDER — Add Provider

```
CREATE MODEL PROVIDER <provider_name> <provider_key>;
```

**Parameters:**
- `provider_name`: Provider name (quoted string), e.g., `'openai'`, `'deepseek'`
- `provider_key`: API key (quoted string)

**Example:**
```
CREATE MODEL PROVIDER 'openai' 'sk-xxxxxxxx';
```

### DROP MODEL PROVIDER — Remove Provider

```
DROP MODEL PROVIDER <provider_name>;
```

**Example:**
```
DROP MODEL PROVIDER 'openai';
```

### LIST MODEL PROVIDERS — Show All Providers

```
LIST MODEL PROVIDERS;
```

---

## Default Model Configuration

### SET DEFAULT LLM / VLM / EMBEDDING / RERANKER / ASR / TTS

```
SET DEFAULT LLM <llm_id>;
SET DEFAULT VLM <vlm_id>;
SET DEFAULT EMBEDDING <embedding_id>;
SET DEFAULT RERANKER <reranker_id>;
SET DEFAULT ASR <asr_id>;
SET DEFAULT TTS <tts_id>;
```

**Examples:**
```
SET DEFAULT LLM 'gpt-4';
SET DEFAULT VLM 'clip-vit-large';
SET DEFAULT EMBEDDING 'text-embedding-ada-002';
SET DEFAULT RERANKER 'bge-reranker-large';
SET DEFAULT ASR 'whisper-large';
SET DEFAULT TTS 'tts-1';
```

### RESET DEFAULT Models

```
RESET DEFAULT LLM;
RESET DEFAULT VLM;
RESET DEFAULT EMBEDDING;
RESET DEFAULT RERANKER;
RESET DEFAULT ASR;
RESET DEFAULT TTS;
```

Resets to system default values.

### LIST DEFAULT MODELS — Show Current Defaults

```
LIST DEFAULT MODELS;
```

---

## Dataset Management

### CREATE DATASET — With Parser

```
CREATE DATASET <dataset_name> WITH EMBEDDING <embedding> PARSER <parser_type>;
```

**Parameters:**
- `dataset_name`: Dataset name (quoted)
- `embedding`: Embedding model name (quoted)
- `parser_type`: Parser type, e.g., `'pdf'`, `'docx'`, `'txt'`

**Example:**
```
CREATE DATASET 'my_kb' WITH EMBEDDING 'text-embedding-ada-002' PARSER 'pdf';
```

### CREATE DATASET — With Pipeline

```
CREATE DATASET <dataset_name> WITH EMBEDDING <embedding> PIPELINE <pipeline>;
```

**Example:**
```
CREATE DATASET 'my_kb' WITH EMBEDDING 'text-embedding-ada-002' PIPELINE 'standard';
```

### DROP DATASET — Delete Dataset

```
DROP DATASET <dataset_name>;
```

**Example:**
```
DROP DATASET 'my_kb';
```

### LIST DATASETS — Show All Datasets

```
LIST DATASETS;
```

### LIST FILES OF DATASET — Show Documents

```
LIST FILES OF DATASET <dataset_name>;
```

**Example:**
```
LIST FILES OF DATASET 'my_kb';
```

---

## Document Operations

### IMPORT — Add Documents to Dataset

```
IMPORT <document_list> INTO DATASET <dataset_name>;
```

**Parameters:**
- `document_list`: Comma-separated file paths (quoted)
- `dataset_name`: Target dataset name (quoted)

**Example:**
```
IMPORT '/path/to/doc1.pdf,/path/to/doc2.pdf' INTO DATASET 'my_kb';
```

### PARSE Documents — Specific Files

```
PARSE <document_names> OF DATASET <dataset_name>;
```

**Example:**
```
PARSE 'doc1.pdf,doc2.pdf' OF DATASET 'my_kb';
```

### PARSE DATASET — Entire Dataset

```
PARSE DATASET <dataset_name> SYNC;
PARSE DATASET <dataset_name> ASYNC;
```

- `SYNC`: Wait for parsing to complete
- `ASYNC`: Return immediately, parse in background

**Example:**
```
PARSE DATASET 'my_kb' SYNC;
```

---

## Search

### SEARCH — Query Datasets

```
SEARCH <question> ON DATASETS <dataset_list>;
```

**Parameters:**
- `question`: Search query (quoted)
- `dataset_list`: Comma-separated dataset names (quoted)

**Example:**
```
SEARCH 'What is RAG?' ON DATASETS 'kb1,kb2';
```

---

## Agent Management

### LIST AGENTS — Show All Agents

```
LIST AGENTS;
```

---

## Chat Session Management

### CREATE CHAT — New Session

```
CREATE CHAT <chat_name>;
```

**Example:**
```
CREATE CHAT 'support_session';
```

### DROP CHAT — Delete Session

```
DROP CHAT <chat_name>;
```

**Example:**
```
DROP CHAT 'support_session';
```

### LIST CHATS — Show All Sessions

```
LIST CHATS;
```

---

## Performance Testing

### BENCHMARK — Test Command Performance

```
BENCHMARK <concurrency> <iterations> <user_command>;
```

**Parameters:**
- `concurrency`: Number of concurrent requests
- `iterations`: Number of iterations per request
- `user_command`: Any valid command (including semicolon)

**Example:**
```
BENCHMARK 5 10 PING;
```

---

## Notes

- All string parameters must be quoted with single (`'`) or double (`"`) quotes
- Commands must end with `;`
- CLI client: `python admin/client/ragflow_cli.py <command>`
- Requires authentication (login first or configure credentials in environment)