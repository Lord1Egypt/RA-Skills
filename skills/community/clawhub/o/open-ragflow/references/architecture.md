# RAGFlow Architecture Reference

## System Overview

RAGFlow is a full-stack microservices application with the following layers:

```
┌─────────────────────────────────────────────────┐
│                  Web UI (React/TS)               │
│               vitejs + shadcn/ui                 │
├─────────────────────────────────────────────────┤
│              Flask API Server (/api/)            │
│    kb_app | dialog_app | document_app | ...      │
├──────────────────┬──────────────────────────────┤
│   RAG Core (/rag/)   │   Agent System (/agent/)  │
│   DeepDoc | LLM      │   Canvas | Components     │
│   Chunking | GraphRAG│   Templates | Tools       │
├──────────────────┴──────────────────────────────┤
│              Infrastructure                      │
│   MySQL | ES/Infinity | Redis | MinIO           │
└─────────────────────────────────────────────────┘
```

## Backend (`/api/`)

Flask-based REST API server. Entry point: `api/ragflow_server.py`

### Blueprint Apps (`api/apps/`)

| App | File | Purpose |
|-----|------|---------|
| Knowledge Base | `kb_app.py` | Create, list, delete knowledge bases/datasets |
| Dialog | `dialog_app.py` | Chat/conversation sessions, message handling |
| Document | `document_app.py` | Upload, parse, manage documents |
| Canvas | `canvas_app.py` | Agent workflow canvas CRUD |
| File | `file_app.py` | File upload, management, chunking |
| User | `user_app.py` | User management, authentication |

### Data Layer (`api/db/`)

- `db_models.py` — SQLAlchemy ORM models
- `services/` — Business logic layer for all entities

## RAG Core (`/rag/`)

### DeepDoc (`deepdoc/`)

Deep document understanding engine:
- PDF parsing with layout analysis
- OCR for scanned documents
- Table extraction
- Multi-modal model support for images in PDF/DOCX

### LLM Integration (`rag/llm/`)

Model abstraction layer supporting:
- **Chat models**: OpenAI, DeepSeek, Gemini, GPT-5, local models
- **Embedding models**: Various text embedding providers
- **Reranking models**: Cross-encoder rerankers (BGE, etc.)
- **ASR models**: Whisper and others
- **TTS models**: Text-to-speech

### RAG Pipeline (`rag/flow/`)

- Chunking strategies (template-based)
- Parser selection
- Tokenization
- Pipeline orchestration

### GraphRAG (`rag/graphrag/`)

- Knowledge graph construction from documents
- Graph-based querying and retrieval

## Agent System (`/agent/`)

### Canvas (`agent/canvas.py`)

Visual workflow builder for AI agents. Users can drag-and-drop components to create agent pipelines.

### Components (`agent/component/`)

Modular workflow components:

| Component | Purpose |
|-----------|---------|
| LLM | Chat completion, reasoning |
| Retrieval | Knowledge base query |
| Categorize | Classify input into categories |
| Code Executor | Run Python/JavaScript in sandbox |
| MCP | Model Context Protocol integration |
| Web Search | External search (Tavily, Wikipedia) |
| SQL Executor | Database query execution |
| Begin/End | Workflow start and end nodes |

### Templates (`agent/templates/`)

Pre-built agent workflows for common scenarios:
- Q&A bots
- Customer support
- Data analysis
- RAG pipelines

### Tools (`agent/tools/`)

External integrations: Tavily search, Wikipedia, SQL execution, API calls, etc.

## Frontend (`/web/`)

- **Framework**: React 18 + TypeScript
- **Build**: Vite
- **UI**: shadcn/ui components
- **State**: Zustand
- **CSS**: Tailwind CSS
- **Testing**: Jest + React Testing Library

## Infrastructure Services

| Service | Port | Purpose |
|---------|------|---------|
| MySQL | 3306 | Primary database (users, KBs, configs) |
| Elasticsearch | 9200 | Full-text search + vector storage (default) |
| Infinity | 23817 | Alternative doc engine (lighter weight) |
| Redis | 6379 | Caching, task queues |
| MinIO | 9000 | Object storage for documents/files |
| Sandbox Executor | — | gVisor-based code execution isolation |

## Document Engines

### Elasticsearch (Default)
- Full-text search + dense vector search
- Higher resource usage
- Production-proven

### Infinity
- Lightweight alternative by infiniflow
- Lower resource footprint
- Switch via `DOC_ENGINE=infinity` in `docker/.env`

## Data Flow

1. **Ingestion**: User uploads documents → MinIO storage
2. **Parsing**: DeepDoc extracts text, tables, images from documents
3. **Chunking**: Documents split into chunks via template-based strategies
4. **Embedding**: Chunks vectorized via configured embedding model
5. **Indexing**: Vectors + text stored in Elasticsearch/Infinity
6. **Retrieval**: User query → embedding → vector search → rerank → LLM generation
7. **Agent Pipeline**: Optional agent workflow orchestrates multi-step reasoning

## Python Dependencies

- Package manager: `uv`
- Python version: 3.10-3.12
- Key dependencies: Flask, SQLAlchemy, pyPDF, transformers (optional), onnxruntime (optional)
- Test framework: pytest (p1/p2/p3 priority levels)

## CLI (`admin/client/`)

Python-based CLI client with SQL-like syntax:
- `ragflow_cli.py` — Entry point
- `ragflow_client.py` — HTTP client (REST API wrapper)
- `parser.py` — Command parser
- `http_client.py` — HTTP transport layer
- `user.py` — User management

## Configuration Files

| File | Scope |
|------|-------|
| `docker/.env` | Environment variables for Docker deployment |
| `docker/service_conf.yaml.template` | Backend service configuration |
| `docker/docker-compose.yml` | Full stack service orchestration |
| `docker/docker-compose-base.yml` | Infra services only (dev mode) |
| `pyproject.toml` | Python project metadata and deps |
| `web/package.json` | Frontend dependencies |