#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
import faiss
import os
import logging
from typing import List, Optional, Dict, Any

# --- 日誌設定 ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("memory-pro")

# --- 環境變數設定 ---
MEMORY_PRO_DATA_DIR = os.getenv("MEMORY_PRO_DATA_DIR", "${OPENCLAW_WORKSPACE}/memory/")
MEMORY_PRO_CORE_FILES = os.getenv("MEMORY_PRO_CORE_FILES", "MEMORY.md,SOUL.md,STATUS.md,AGENTS.md,USER.md").split(',')
MEMORY_PRO_PORT = int(os.getenv("MEMORY_PRO_PORT", "8001"))
MEMORY_PRO_INDEX_PATH = os.getenv("MEMORY_PRO_INDEX_PATH", "memory.index")
# 新增：預設模式（保持 vector 以免破壞舊行為）
MEMORY_PRO_MODE = os.getenv("MEMORY_PRO_MODE", "vector").lower()

# --- 初始化 ---
app = FastAPI(title="Memory Pro API", description="Semantic Search Service for OpenClaw Memory")

# 全局變數 (延遲初始化)
model = None
index = None
sentences = []

# --- Pydantic 模型 ---
class SearchRequest(BaseModel):
    query: str = Field(..., description="搜尋查詢字串", min_length=1)
    top_k: int = Field(3, ge=1, le=20, description="返回結果數量")
    mode: Optional[str] = Field(None, description="vector|hybrid (optional)")
    scope: Optional[str] = Field(None, description="global|agent:<id>|... (optional)")
    include_debug: bool = Field(False, description="Include debug scores (hybrid mode)")

class SearchResult(BaseModel):
    score: float
    sentence: str
    debug: Optional[Dict[str, Any]] = None

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]

# --- 啟動事件 ---
@app.on_event("startup")
async def startup_event():
    global model, index, sentences
    try:
        logger.info("Starting Memory Pro service...")

        # 載入模型
        logger.info("Loading SentenceTransformer model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

        # 載入索引
        index_path = MEMORY_PRO_INDEX_PATH
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found at {index_path}")
        logger.info(f"Loading FAISS index from {index_path}...")
        index = faiss.read_index(index_path)

        # 載入句子（優先使用 build_index 產出的 sentences.txt，避免重建後檔案變動造成 mismatch）
        sentences_path = os.getenv("MEMORY_PRO_SENTENCES_PATH", "sentences.txt")
        loaded_from = ""
        if os.path.exists(sentences_path):
            with open(sentences_path, "r", encoding="utf-8") as f:
                sentences = [line.rstrip("\n") for line in f if line.strip()]
            loaded_from = f"file:{sentences_path}"
        else:
            logger.info("sentences.txt not found; fallback to preprocess_directory()...")
            from preprocess import preprocess_directory
            sentences = preprocess_directory()
            loaded_from = "preprocess"

        # 驗證同步
        if index.ntotal != len(sentences):
            error_msg = f"Index size mismatch: FAISS has {index.ntotal}, sentences list has {len(sentences)} (source={loaded_from})"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"Service ready. Indexed {len(sentences)} items.")

    except Exception as e:
        logger.critical(f"Startup failed: {e}")
        raise e

# --- 健康檢查 ---
@app.get("/health")
async def health_check():
    if model is None or index is None or not sentences:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return {"status": "ok", "indexed_items": len(sentences), "mode_default": MEMORY_PRO_MODE}

# --- 搜尋端點 ---
@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        query = request.query.strip()
        top_k = request.top_k

        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        requested_mode = (request.mode or MEMORY_PRO_MODE or "vector").lower()

        # --- Hybrid path (optional) ---
        if requested_mode == "hybrid":
            try:
                from retrieval_hybrid import hybrid_search
                results = hybrid_search(
                    query,
                    model=model,
                    index=index,
                    sentences=sentences,
                    top_k=top_k,
                    scope=request.scope,
                    include_debug=request.include_debug,
                )
                return {"query": query, "results": results}
            except Exception as e:
                logger.warning(f"Hybrid search failed, fallback to vector mode: {e}")

        # --- Vector path (backward compatible default) ---
        query_embedding = model.encode([query])
        # 與 build_index 的 normalize_L2 對齊，避免 query 向量長度影響距離
        faiss.normalize_L2(query_embedding)
        distances, indices = index.search(query_embedding, top_k)

        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx != -1:
                if 0 <= idx < len(sentences):
                    results.append({
                        "score": float(1.0 / (1.0 + max(0.0, float(distance)))),
                        "sentence": sentences[idx]
                    })
                else:
                    logger.warning(f"Index {idx} out of bounds for sentences list (len={len(sentences)})")

        return {
            "query": query,
            "results": results
        }

    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
