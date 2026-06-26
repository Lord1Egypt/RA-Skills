# MemVault Multi-Stage Dockerfile
# Usage:
#   docker compose up              (recommended)
#   docker build --target server . (server only)

# ---- Base ----
FROM python:3.13-slim AS base
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app

# ---- Embedding Server ----
FROM base AS embedding
COPY requirements.txt .
RUN pip install --no-cache-dir sentence-transformers fastapi uvicorn
COPY embedding_server.py .
# Pre-download model at build time
RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
EXPOSE 8001
CMD ["python3", "embedding_server.py"]

# ---- MemVault Server ----
FROM base AS server
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY memvault_server.py .
EXPOSE 8002
CMD ["python3", "memvault_server.py"]
