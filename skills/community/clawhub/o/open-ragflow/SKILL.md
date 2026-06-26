---
name: open-ragflow
description: RAGFlow open-source Retrieval-Augmented Generation (RAG) engine — deployment, configuration, management, and troubleshooting.
---

# Open RAGFlow

Open-source RAG engine fusing RAG with Agent capabilities. Full-stack: Python backend (Flask), React/TypeScript frontend, Docker-deployed microservices.

## Use Cases

- Deploying or self-hosting RAGFlow via Docker Compose or from source
- Configuring RAGFlow (LLM providers, API keys, document engines, ports)
- Managing knowledge bases, datasets, documents, agents, and chats via RAGFlow CLI
- Understanding RAGFlow architecture (DeepDoc, Agent system, RAG pipeline)
- Integrating with RAGFlow REST API
- Troubleshooting RAGFlow deployment or runtime issues.


## Quick Reference

- **Website**: https://ragflow.io
- **Cloud**: https://cloud.ragflow.io
- **Docs**: https://ragflow.io/docs/dev/
- **Repo**: https://github.com/infiniflow/ragflow
- **Discord**: https://discord.gg/NjYzJD3GM3
- **Docker Hub**: `infiniflow/ragflow`
- **License**: Apache 2.0

## When to Use Which Reference

- **Deploying / troubleshooting deployment** → [references/deployment.md](references/deployment.md)
- **Understanding architecture / components / data flow** → [references/architecture.md](references/architecture.md)
- **Using CLI to manage datasets, agents, models** → [references/cli-reference.md](references/cli-reference.md)

## Prerequisites

- CPU >= 4 cores, RAM >= 16 GB, Disk >= 50 GB
- Docker >= 24.0.0 & Docker Compose >= v2.26.1
- `vm.max_map_count` >= 262144 (Linux, for Elasticsearch)
- gVisor: optional, only needed for the code executor (sandbox) feature

## Docker Deployment (Quick Start)

```bash
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker
docker compose -f docker-compose.yml up -d
docker logs -f docker-ragflow-cpu-1  # wait for the banner, then login
# Open http://YOUR_SERVER_IP in browser
```

Configure LLM API keys in `docker/service_conf.yaml.template` under `user_default_llm`, then restart:

```bash
docker compose -f docker-compose.yml up -d
```

### Chinese Mirror Images

If Docker Hub is slow:
- Huawei Cloud: `swr.cn-north-4.myhuaweicloud.com/infiniflow/ragflow`
- Alibaba Cloud: `registry.cn-hangzhou.aliyuncs.com/infiniflow/ragflow`

Set HuggingFace mirror if needed: `HF_ENDPOINT=https://hf-mirror.com` in `docker/.env`.

## Key Configuration Files

| File | Scope |
|------|-------|
| `docker/.env` | Environment variables: `SVR_HTTP_PORT`, `MYSQL_PASSWORD`, `MINIO_PASSWORD`, `DOC_ENGINE`, `RAGFLOW_IMAGE`, `HF_ENDPOINT` |
| `docker/service_conf.yaml.template` | Backend services: LLM factory, API keys, embedding/rerank/ASR/TTS models |
| `docker/docker-compose.yml` | Full stack orchestration |
| `docker/docker-compose-base.yml` | Infrastructure services only (dev mode) |

## Post-Deployment LLM Setup

1. Log in via browser
2. Edit `docker/service_conf.yaml.template`:
   ```yaml
   user_default_llm:
     factory: "OpenAI"   # or "DeepSeek", "Gemini", etc.
     api_key: "sk-..."
     base_url: "https://api.openai.com/v1/"
   ```
3. Run `docker compose -f docker-compose.yml up -d` to apply.

## CLI Quick Reference

All CLI commands end with `;`. Full reference: [references/cli-reference.md](references/cli-reference.md).

```bash
# Datasets
LIST DATASETS;
CREATE DATASET 'my_kb' WITH EMBEDDING 'text-embedding-ada-002' PARSER 'pdf';
DROP DATASET 'my_kb';
LIST FILES OF DATASET 'my_kb';

# Documents
IMPORT '/path/to/doc.pdf' INTO DATASET 'my_kb';
PARSE DATASET 'my_kb' SYNC;
PARSE DATASET 'my_kb' ASYNC;

# Search
SEARCH 'What is RAG?' ON DATASETS 'my_kb';

# Models
CREATE MODEL PROVIDER 'openai' 'sk-...';
SET DEFAULT LLM 'gpt-4';
LIST MODEL PROVIDERS;
LIST DEFAULT MODELS;

# Agents & Chats
LIST AGENTS;
LIST CHATS;
CREATE CHAT 'my_session';
DROP CHAT 'my_session';

# Connection
PING;
SHOW CURRENT USER;
```

## Switching Doc Engine (Elasticsearch → Infinity)

```bash
docker compose -f docker/docker-compose.yml down -v  # WARNING: clears data
# Edit docker/.env: set DOC_ENGINE=infinity
docker compose -f docker-compose.yml up -d
```

Infinity is lighter weight but Linux/arm64 is not officially supported.

## Architecture at a Glance

```
Web UI (React+TS+vitejs+shadcn) → Flask API (/api/) → RAG Core (/rag/) + Agent (/agent/)
                                                          ↓
Infrastructure: MySQL + Elasticsearch/Infinity + Redis + MinIO
```

- **Backend** (`/api/`): Flask blueprints — kb, dialog, document, canvas, file, user
- **RAG Core** (`/rag/`): DeepDoc parsing, LLM/embedding/rerank abstractions, chunking, GraphRAG
- **Agent** (`/agent/`): Canvas-based workflow builder with components (LLM, Retrieval, Code Executor, MCP, Search, SQL)
- **Frontend** (`/web/`): React 18 + TypeScript + Vite

See [references/architecture.md](references/architecture.md) for detailed component breakdown.

## Development from Source

```bash
git clone https://github.com/infiniflow/ragflow.git && cd ragflow
uv sync --python 3.12 && uv run python3 download_deps.py
docker compose -f docker/docker-compose-base.yml up -d
# Add to /etc/hosts: 127.0.0.1 es01 infinity mysql minio redis sandbox-executor-manager
source .venv/bin/activate && export PYTHONPATH=$(pwd)
bash docker/launch_backend_service.sh
# Separate terminal:
cd web && npm install && npm run dev
```

## Troubleshooting Quick Reference

| Problem | Fix |
|---------|-----|
| `network abnormal` browser error | Wait for Docker logs to show the RAGFlow banner — server is initializing |
| Docker pull timeout in China | Use `RAGFLOW_IMAGE` mirrors (Huawei Cloud / Alibaba Cloud) |
| HuggingFace unreachable | `export HF_ENDPOINT=https://hf-mirror.com` |
| ARM64 platform | Build Docker image from source (no official ARM64 image) |
| Port conflict | Change `80:80` to `<PORT>:80` in `docker-compose.yml` |
| Elasticsearch exits with 137 | Increase Docker memory allocation |
| `vm.max_map_count` too low | `sudo sysctl -w vm.max_map_count=262144` |

## API & SDK

- REST API: `http://SERVER_IP/api/` — Swagger docs at `/api/docs`
- Python SDK: available in `sdk/python/`
- CLI client: `python admin/client/ragflow_cli.py <command>`
- Guide: [https://ragflow.io/docs/dev/](https://ragflow.io/docs/dev/)