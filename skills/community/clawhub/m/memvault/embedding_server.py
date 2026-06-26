#!/usr/bin/env python3
"""MemVault Local Embedding Server.

Provides OpenAI-compatible /embeddings endpoint using sentence-transformers.
No API key needed — runs entirely locally.
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ.setdefault("no_proxy", "localhost,127.0.0.1")
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")

MODEL_NAME = os.environ.get("MEMVAULT_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
PORT = int(os.environ.get("MEMVAULT_EMBEDDING_PORT", "8001"))

model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    logger.info(f"Loading embedding model: {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    logger.info("Model loaded!")
    yield
    logger.info("Shutting down...")


app = FastAPI(title="MemVault Embedding Server", lifespan=lifespan)


class EmbedRequest(BaseModel):
    input: list[str] | str
    model: str = "all-MiniLM-L6-v2"


class EmbedResponse(BaseModel):
    data: list[dict]
    model: str
    usage: dict


@app.post("/embeddings")
@app.post("/v1/embeddings")
async def embed(req: EmbedRequest) -> EmbedResponse:
    """Create embeddings (OpenAI-compatible format)."""
    inputs = req.input if isinstance(req.input, list) else [req.input]
    embeddings = model.encode(inputs).tolist()
    return EmbedResponse(
        data=[{"embedding": emb, "index": i, "object": "embedding"} for i, emb in enumerate(embeddings)],
        model=MODEL_NAME,
        usage={"prompt_tokens": sum(len(t.split()) for t in inputs), "total_tokens": sum(len(t.split()) for t in inputs)},
    )


@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL_NAME, "loaded": model is not None}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
