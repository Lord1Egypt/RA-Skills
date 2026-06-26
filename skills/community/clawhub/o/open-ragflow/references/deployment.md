# RAGFlow Deployment Reference

## Self-Hosting with Docker (Recommended)

### Prerequisites

- CPU >= 4 cores
- RAM >= 16 GB
- Disk >= 50 GB
- Docker >= 24.0.0 & Docker Compose >= v2.26.1
- `vm.max_map_count` >= 262144 (Linux only)

### Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker

# 2. (Optional) Checkout a stable release
# git checkout v0.25.2

# 3. Start services (CPU mode)
docker compose -f docker-compose.yml up -d

# For GPU acceleration:
# sed -i '1i DEVICE=gpu' .env
# docker compose -f docker-compose.yml up -d
```

### Verify Startup

```bash
docker logs -f docker-ragflow-cpu-1
```

Successful launch shows the RAGFlow ASCII banner and `Running on all addresses (0.0.0.0)`.

### Access

Open `http://YOUR_SERVER_IP` in browser. Default port is 80.

### Post-Deployment Configuration

1. Log in to the web UI
2. Edit `docker/service_conf.yaml.template`:
   - Set `user_default_llm.factory` to your LLM provider
   - Set `user_default_llm.api_key` with your API key
3. Restart to apply:
   ```bash
   docker compose -f docker-compose.yml up -d
   ```

## Configuration Files Reference

### `docker/.env` — Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SVR_HTTP_PORT` | HTTP serving port | `80` |
| `MYSQL_PASSWORD` | MySQL root password | `infini_rag_flow` |
| `MINIO_PASSWORD` | MinIO access password | `infini_rag_flow` |
| `DOC_ENGINE` | Document engine (`elasticsearch` or `infinity`) | `elasticsearch` |
| `RAGFLOW_IMAGE` | Docker image to pull | `infiniflow/ragflow:v0.25.2` |
| `HF_ENDPOINT` | HuggingFace mirror | `https://huggingface.co` |
| `DEVICE` | `cpu` or `gpu` for DeepDoc | `cpu` |

### Chinese Mirror Images

If Docker Hub is slow in China:
```
# Huawei Cloud
RAGFLOW_IMAGE=swr.cn-north-4.myhuaweicloud.com/infiniflow/ragflow:v0.25.2
# Alibaba Cloud  
RAGFLOW_IMAGE=registry.cn-hangzhou.aliyuncs.com/infiniflow/ragflow:v0.25.2
```

HF mirror:
```
HF_ENDPOINT=https://hf-mirror.com
```

### `docker/service_conf.yaml.template` — Backend Config

Key sections:
- `user_default_llm`: Default LLM factory and API key
- `embedding_model`: Default embedding model
- `rerank_model`: Default reranking model
- `asr_model`: Speech recognition model
- `tts_model`: Text-to-speech model

Example for OpenAI:
```yaml
user_default_llm:
  factory: "OpenAI"
  api_key: "sk-..."
  base_url: "https://api.openai.com/v1/"
```

Example for DeepSeek:
```yaml
user_default_llm:
  factory: "DeepSeek"
  api_key: "sk-..."
  base_url: "https://api.deepseek.com/v1"
```

## Port Configuration

To change the HTTP port (default 80), edit `docker/docker-compose.yml`:
```yaml
ports:
  - "YOUR_PORT:80"
```

Then restart: `docker compose -f docker-compose.yml up -d`

## Switching Document Engine

### Elasticsearch → Infinity

```bash
# 1. Stop and clean volumes (WARNING: data loss)
docker compose -f docker/docker-compose.yml down -v

# 2. Edit docker/.env
# Set: DOC_ENGINE=infinity

# 3. Restart
docker compose -f docker-compose.yml up -d
```

> Infinity on Linux/arm64 is not officially supported.

## Development from Source

### Prerequisites
- Python 3.10-3.12
- Node.js >= 18.20.4
- `uv` package manager
- Docker & Docker Compose
- `jemalloc` (optional, recommended)

### Setup

```bash
# 1. Clone and install Python deps
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/
uv sync --python 3.12
uv run python3 download_deps.py
pre-commit install

# 2. Start infrastructure services
docker compose -f docker/docker-compose-base.yml up -d

# 3. Add to /etc/hosts
# 127.0.0.1  es01 infinity mysql minio redis sandbox-executor-manager

# 4. (If in China) Set HF mirror
# export HF_ENDPOINT=https://hf-mirror.com

# 5. Launch backend
source .venv/bin/activate
export PYTHONPATH=$(pwd)
bash docker/launch_backend_service.sh

# 6. Launch frontend (separate terminal)
cd web
npm install
npm run dev
```

### Stop Development Services

```bash
pkill -f "ragflow_server.py|task_executor.py"
```

## Building Docker Image

```bash
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/
docker build --platform linux/amd64 -f Dockerfile -t infiniflow/ragflow:nightly .
```

With proxy:
```bash
docker build --platform linux/amd64 \
  --build-arg http_proxy=http://PROXY:PORT \
  --build-arg https_proxy=http://PROXY:PORT \
  -f Dockerfile -t infiniflow/ragflow:nightly .
```

## ARM64 Platforms

No official ARM64 Docker images. Must build from source:
```bash
docker build -f Dockerfile -t infiniflow/ragflow:custom-arm64 .
```
Then update `RAGFLOW_IMAGE` in `docker/.env` to use your custom image.

## Linux vm.max_map_count

Elasticsearch requires at least 262144. Check:
```bash
sysctl vm.max_map_count
```

Temporary fix:
```bash
sudo sysctl -w vm.max_map_count=262144
```

Permanent fix (add to /etc/sysctl.conf):
```
vm.max_map_count=262144
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `network abnormal` on login | Wait until Docker logs show the RAGFlow ASCII banner — server may still be initializing |
| Docker pull timeout | Use Huawei Cloud or Alibaba Cloud mirror images in `RAGFLOW_IMAGE` |
| HuggingFace unreachable | Set `HF_ENDPOINT=https://hf-mirror.com` in `.env` |
| Port already in use | Change `80:80` to `<NEW_PORT>:80` in `docker-compose.yml` |
| Elasticsearch exits with 137 | Increase Docker memory or reduce `vm.max_map_count` issues |
| Out of disk space | Clean Docker volumes: `docker system prune -a` |
| Frontend build fails | Check Node.js version >= 18.20.4 |
| Python import errors | Ensure `PYTHONPATH=$(pwd)` is set when running from source |