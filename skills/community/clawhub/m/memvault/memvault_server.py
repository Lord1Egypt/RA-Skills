#!/usr/bin/env python3
"""MemVault — Production-ready Long-term Memory Server for AI Agents.

Built on memU, with Ebbinghaus memory decay, strength-weighted retrieval,
local LLM support (Ollama), and one-command setup.

GitHub: https://github.com/wjy9902/memvault
License: Apache 2.0
"""

import asyncio
import json
import logging
import os
import re
import time as _time
import uuid
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fix httpx picking up system proxy for local requests
os.environ.setdefault("no_proxy", "localhost,127.0.0.1")
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")

# ========== Configuration (from env or .env file) ==========

DB_DSN = os.environ.get("MEMVAULT_DB_DSN", "postgresql://postgres:postgres@127.0.0.1:5432/memvault")
EMBEDDING_URL = os.environ.get("MEMVAULT_EMBEDDING_URL", "http://127.0.0.1:8001")
EMBEDDING_MODEL = os.environ.get("MEMVAULT_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
LLM_BASE_URL = os.environ.get("MEMVAULT_LLM_BASE_URL", "http://127.0.0.1:11434/v1")
LLM_API_KEY = os.environ.get("MEMVAULT_LLM_API_KEY", "ollama")
LLM_MODEL = os.environ.get("MEMVAULT_LLM_MODEL", "qwen2.5:3b")
TRANSLATION_ENABLED = os.environ.get("MEMVAULT_TRANSLATION", "false").lower() == "true"
TRANSLATION_TARGET_LANG = os.environ.get("MEMVAULT_TRANSLATION_LANG", "Chinese")
LISTEN_HOST = os.environ.get("MEMVAULT_HOST", "0.0.0.0")
LISTEN_PORT = int(os.environ.get("MEMVAULT_PORT", "8002"))
MEMORY_TYPES = os.environ.get("MEMVAULT_MEMORY_TYPES", "event,knowledge").split(",")

# Global service instance
memory_service = None
TEMP_DIR = "/tmp/memvault_conversations"


# ========== Translation (optional, for non-English users) ==========

async def _translate_batch(summaries: list[tuple[str, str]], target_lang: str) -> dict[str, str]:
    """Batch translate summaries to target language via local LLM."""
    import httpx

    if not summaries:
        return {}

    lines = [f"[{i}] {s}" for i, (_, s) in enumerate(summaries)]
    batch_text = "\n".join(lines)

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                LLM_BASE_URL + "/chat/completions",
                json={
                    "model": LLM_MODEL,
                    "messages": [
                        {"role": "system", "content": (
                            f"Translate the following numbered memory summaries to concise {target_lang}. "
                            f"Output strictly one line per item: [number] translation\n"
                            f"No explanations. If already in {target_lang}, output as-is."
                        )},
                        {"role": "user", "content": batch_text}
                    ],
                    "temperature": 0.1,
                },
            )
            resp.raise_for_status()
            data = resp.json()

        content = data["choices"][0]["message"]["content"].strip()
        result = {}
        for match in re.finditer(r'\[(\d+)\]\s*(.+)', content):
            idx = int(match.group(1))
            translation = match.group(2).strip()
            if 0 <= idx < len(summaries):
                result[summaries[idx][0]] = translation

        if not result and len(summaries) == 1:
            result[summaries[0][0]] = content

        return result
    except Exception as e:
        logger.warning(f"Batch translation failed: {e}")
        return {}


def _is_english_text(text: str) -> bool:
    """Heuristic: check if text is primarily English."""
    if not text:
        return False
    ascii_chars = sum(1 for c in text if c.isascii() and c.isalpha())
    total_chars = sum(1 for c in text if c.isalpha())
    if total_chars == 0:
        return False
    return (ascii_chars / total_chars) > 0.7


async def _post_process_translate(user_id: str, items_count: int):
    """Post-memorize: batch translate English summaries and re-embed."""
    import httpx
    import psycopg2

    if items_count <= 0:
        return

    try:
        conn = psycopg2.connect(DB_DSN)
        cur = conn.cursor()
        cur.execute("""
            SELECT id, summary FROM memory_items
            WHERE user_id = %s ORDER BY created_at DESC LIMIT %s
        """, (user_id, items_count + 2))

        rows = cur.fetchall()
        to_translate = [(str(r[0]), r[1]) for r in rows if r[1] and _is_english_text(r[1])]

        if not to_translate:
            conn.close()
            return

        translations = await _translate_batch(to_translate, TRANSLATION_TARGET_LANG)
        if not translations:
            conn.close()
            return

        async def _get_embedding(text: str) -> list | None:
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.post(
                        f"{EMBEDDING_URL}/embeddings",
                        json={"input": text, "model": EMBEDDING_MODEL},
                    )
                    resp.raise_for_status()
                    return resp.json()["data"][0]["embedding"]
            except Exception as e:
                logger.warning(f"Embedding failed: {e}")
                return None

        embeddings = {}
        for mid, translated in translations.items():
            embeddings[mid] = await _get_embedding(translated)

        updated = 0
        for mid, translated in translations.items():
            emb = embeddings.get(mid)
            if emb:
                cur.execute(
                    "UPDATE memory_items SET summary = %s, embedding = %s::vector WHERE id = %s",
                    (translated, str(emb), mid),
                )
            else:
                cur.execute("UPDATE memory_items SET summary = %s WHERE id = %s", (translated, mid))
            updated += 1

        conn.commit()
        conn.close()
        if updated > 0:
            logger.info(f"[translate] Updated {updated} summaries to {TRANSLATION_TARGET_LANG}")
    except Exception as e:
        logger.error(f"Translation post-process failed: {e}")


async def _post_process_new_memories(user_id: str, items_count: int, source_agent: str = "unknown"):
    """Post-memorize: tag source_agent + optional translation."""
    import psycopg2

    if items_count <= 0:
        return

    try:
        conn = psycopg2.connect(DB_DSN)
        cur = conn.cursor()
        cur.execute("""
            WITH recent AS (
                SELECT id FROM memory_items
                WHERE user_id = %s AND (source_agent IS NULL OR source_agent = 'unknown')
                ORDER BY created_at DESC LIMIT %s
            )
            UPDATE memory_items SET source_agent = %s
            FROM recent WHERE memory_items.id = recent.id
        """, (user_id, items_count + 2, source_agent))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"[source_agent] Update failed: {e}")

    if TRANSLATION_ENABLED:
        await _post_process_translate(user_id, items_count)


# ========== App Lifecycle ==========

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize MemVault (memU backend) on startup."""
    global memory_service

    from memu.app import MemoryService

    logger.info("Initializing MemVault...")
    os.makedirs(TEMP_DIR, exist_ok=True)

    llm_config = {
        "default": {
            "base_url": LLM_BASE_URL,
            "api_key": LLM_API_KEY,
            "chat_model": LLM_MODEL,
            "client_backend": "httpx",
            "embed_model": EMBEDDING_MODEL,
        },
        "embedding": {
            "base_url": EMBEDDING_URL,
            "api_key": "not-needed",
            "embed_model": EMBEDDING_MODEL,
            "provider": "openai",
        },
    }

    memory_service = MemoryService(
        llm_profiles=llm_config,
        database_config={
            "metadata_store": {"provider": "postgres", "dsn": DB_DSN},
            "vector_index": {"provider": "pgvector", "dsn": DB_DSN},
        },
        retrieve_config={"method": "rag", "route_intention": False},
        memorize_config={"memory_types": [t.strip() for t in MEMORY_TYPES]},
    )

    # Performance: skip multimodal preprocess for text-only
    async def _fast_preprocess(state, step_context):
        state["preprocessed_resources"] = [{"text": state.get("raw_text"), "caption": None}]
        return state
    memory_service._memorize_preprocess_multimodal = _fast_preprocess

    # Performance: timing wrappers
    _orig_extract = memory_service._memorize_extract_items
    _orig_categorize = memory_service._memorize_categorize_items
    _orig_persist = memory_service._memorize_persist_and_index

    async def _timed(name, fn, state, ctx):
        t0 = _time.monotonic()
        r = await fn(state, ctx)
        logger.info(f"[PERF] {name} {_time.monotonic()-t0:.1f}s")
        return r

    memory_service._memorize_extract_items = lambda s, c: _timed("extract", _orig_extract, s, c)
    memory_service._memorize_categorize_items = lambda s, c: _timed("categorize", _orig_categorize, s, c)
    memory_service._memorize_persist_and_index = lambda s, c: _timed("persist", _orig_persist, s, c)

    logger.info(f"MemVault ready | LLM={LLM_MODEL} | translation={'on' if TRANSLATION_ENABLED else 'off'}")
    yield
    logger.info("MemVault shutting down...")


app = FastAPI(
    title="MemVault",
    description="Production-ready long-term memory server for AI agents",
    version="1.0.0",
)


# ========== Request/Response Models ==========

class MemorizeRequest(BaseModel):
    conversation: list[dict[str, Any]]
    user_id: str = "default"
    modality: str = "conversation"

class RetrieveRequest(BaseModel):
    query: str
    user_id: str = "default"
    method: str = "rag"
    limit: int = 5

class MemorizeResponse(BaseModel):
    success: bool
    items_count: int
    categories_count: int
    message: str

class RetrieveResponse(BaseModel):
    success: bool
    memories: list[dict[str, Any]]
    message: str


# ========== API Endpoints ==========

@app.post("/memorize", response_model=MemorizeResponse)
async def memorize(req: MemorizeRequest) -> MemorizeResponse:
    """Store a conversation in long-term memory."""
    try:
        source_agent = "unknown"
        clean_conversation = []
        for msg in (req.conversation or []):
            if isinstance(msg, dict) and msg.get("role") == "metadata":
                try:
                    meta = json.loads(msg.get("content", "{}"))
                    source_agent = meta.get("source_agent", "unknown")
                except (json.JSONDecodeError, TypeError):
                    pass
            else:
                clean_conversation.append(msg)

        conv_id = str(uuid.uuid4())
        conv_file = os.path.join(TEMP_DIR, f"{req.user_id}_{conv_id}.json")
        with open(conv_file, "w", encoding="utf-8") as f:
            json.dump(clean_conversation, f, ensure_ascii=False)

        try:
            t0 = _time.monotonic()
            result = await memory_service.memorize(
                resource_url=conv_file, modality=req.modality,
                user={"user_id": req.user_id},
            )
            logger.info(f"[PERF] memorize() {_time.monotonic()-t0:.1f}s")
            items_count = len(result.get("items", []))
            categories_count = len(result.get("categories", []))

            if items_count > 0:
                asyncio.create_task(
                    _post_process_new_memories(req.user_id, items_count, source_agent)
                )

            return MemorizeResponse(
                success=True, items_count=items_count,
                categories_count=categories_count,
                message=f"Memorized {items_count} items (source: {source_agent})",
            )
        finally:
            if os.path.exists(conv_file):
                os.remove(conv_file)
    except Exception as e:
        import traceback
        logger.error(f"Memorize error: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e) or repr(e))


@app.post("/retrieve", response_model=RetrieveResponse)
async def retrieve(req: RetrieveRequest) -> RetrieveResponse:
    """Retrieve memories using strength-weighted vector search."""
    try:
        import requests as req_lib
        import psycopg2

        embed_resp = req_lib.post(
            f"{EMBEDDING_URL}/embeddings",
            json={"input": req.query, "model": EMBEDDING_MODEL}, timeout=10,
        )
        embed_resp.raise_for_status()
        query_embedding = embed_resp.json()["data"][0]["embedding"]

        conn = psycopg2.connect(DB_DSN)
        cur = conn.cursor()
        cur.execute("""
            SELECT id, summary, memory_type, created_at, updated_at, extra,
                   strength, access_count, source_agent,
                   (1 - (embedding <=> %s::vector)) * COALESCE(strength, 1.0) AS weighted_score
            FROM memory_items
            WHERE user_id = %s AND COALESCE(strength, 1.0) > 0.1
            ORDER BY weighted_score DESC LIMIT %s
        """, (str(query_embedding), req.user_id, req.limit))

        memories = []
        hit_ids = []
        for row in cur.fetchall():
            hit_ids.append(row[0])
            memories.append({
                "id": str(row[0]), "summary": row[1], "memory_type": row[2],
                "created_at": str(row[3]) if row[3] else None,
                "updated_at": str(row[4]) if row[4] else None,
                "extra": row[5] if row[5] else {},
                "strength": float(row[6]) if row[6] else 1.0,
                "access_count": int(row[7]) if row[7] else 0,
                "source_agent": row[8] or "unknown",
                "score": float(row[9]),
            })

        if hit_ids:
            cur.execute("""
                UPDATE memory_items
                SET access_count = COALESCE(access_count, 0) + 1, last_accessed = NOW()
                WHERE id = ANY(%s)
            """, (hit_ids,))
            conn.commit()
        conn.close()

        return RetrieveResponse(
            success=True, memories=memories,
            message=f"Retrieved {len(memories)} memories (strength-weighted)",
        )
    except Exception as e:
        logger.error(f"Retrieve error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/decay")
async def run_decay(decay_rate: float = 0.1, damping: float = 0.5, user_id: str = "default"):
    """Run Ebbinghaus forgetting curve decay on all memories.
    
    Formula: strength = exp(-rate × days / (1 + damping × ln(1 + access_count)))
    Frequently accessed memories decay slower. Run daily via cron.
    """
    import psycopg2

    try:
        conn = psycopg2.connect(DB_DSN)
        cur = conn.cursor()
        cur.execute("""
            UPDATE memory_items SET
              strength = GREATEST(0.01,
                exp(-%(rate)s * EXTRACT(EPOCH FROM (NOW() - created_at)) / 86400.0
                    / (1.0 + %(damp)s * ln(1.0 + COALESCE(access_count, 0)))))
            WHERE user_id = %(uid)s AND COALESCE(strength, 1.0) > 0.01
        """, {"rate": decay_rate, "damp": damping, "uid": user_id})
        affected = cur.rowcount

        cur.execute("""
            SELECT COUNT(*) FILTER (WHERE strength >= 0.8),
                   COUNT(*) FILTER (WHERE strength >= 0.3 AND strength < 0.8),
                   COUNT(*) FILTER (WHERE strength >= 0.1 AND strength < 0.3),
                   COUNT(*) FILTER (WHERE strength < 0.1),
                   COUNT(*)
            FROM memory_items WHERE user_id = %s
        """, (user_id,))
        row = cur.fetchone()
        conn.commit()
        conn.close()

        return {
            "success": True, "updated": affected,
            "distribution": {
                "strong": row[0], "medium": row[1], "weak": row[2], "fading": row[3], "total": row[4],
            },
            "params": {"decay_rate": decay_rate, "damping": damping},
        }
    except Exception as e:
        logger.error(f"Decay error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def memory_stats(user_id: str = "default"):
    """Memory statistics: distribution, types, sources."""
    import psycopg2

    try:
        conn = psycopg2.connect(DB_DSN)
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*), COUNT(*) FILTER (WHERE strength >= 0.8),
                   COUNT(*) FILTER (WHERE strength >= 0.3 AND strength < 0.8),
                   COUNT(*) FILTER (WHERE strength >= 0.1 AND strength < 0.3),
                   COUNT(*) FILTER (WHERE strength < 0.1),
                   AVG(strength), AVG(access_count), MAX(access_count)
            FROM memory_items WHERE user_id = %s
        """, (user_id,))
        row = cur.fetchone()

        cur.execute("""
            SELECT memory_type, COUNT(*), AVG(strength)::numeric(4,2)
            FROM memory_items WHERE user_id = %s GROUP BY memory_type ORDER BY COUNT(*) DESC
        """, (user_id,))
        by_type = [{"type": r[0], "count": r[1], "avg_strength": float(r[2])} for r in cur.fetchall()]

        cur.execute("""
            SELECT source_agent, COUNT(*), AVG(strength)::numeric(4,2)
            FROM memory_items WHERE user_id = %s GROUP BY source_agent ORDER BY COUNT(*) DESC
        """, (user_id,))
        by_source = [{"agent": r[0], "count": r[1], "avg_strength": float(r[2])} for r in cur.fetchall()]
        conn.close()

        return {
            "total": row[0],
            "distribution": {"strong": row[1], "medium": row[2], "weak": row[3], "fading": row[4]},
            "avg_strength": round(float(row[5]), 3) if row[5] else 0,
            "avg_access_count": round(float(row[6]), 1) if row[6] else 0,
            "max_access_count": row[7] or 0,
            "by_type": by_type,
            "by_source": by_source,
        }
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check."""
    return {
        "status": "ok", "service": "memvault", "version": "1.0.0",
        "initialized": memory_service is not None,
        "translation": TRANSLATION_ENABLED,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=LISTEN_HOST, port=LISTEN_PORT)
