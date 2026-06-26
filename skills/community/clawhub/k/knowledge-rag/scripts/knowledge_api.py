#!/usr/bin/env python3
"""
knowledge_api.py — FastAPI 后端

提供 RAG 搜索、索引、统计等 API。
TS Express 通过 HTTP 调用本服务，不再 execSync 子进程。

用法：
  .venv/bin/python3 -m uvicorn knowledge_api:app --host 0.0.0.0 --port 8768
  或直接用 start.py 一键启动
"""

import os, sys, json, io, contextlib
from pathlib import Path
from contextlib import asynccontextmanager

import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import query_knowledge as qk
import index_knowledge as idxk


# ─── 路径辅助 ────────────────────────────────────────────

CONFIG_FILE = os.path.expanduser("~/workspace/knowledge/.knowledge-config.json")
DEFAULT_KNOWLEDGE_DIR = os.path.expanduser("~/workspace/knowledge")

_config_cache = None
_config_mtime = 0


def load_config():
    global _config_cache, _config_mtime
    try:
        current_mtime = os.path.getmtime(CONFIG_FILE)
    except OSError:
        current_mtime = 0
    if _config_cache is not None and current_mtime <= _config_mtime:
        return _config_cache
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            _config_cache = json.load(f)
        _config_mtime = current_mtime
    except Exception:
        _config_cache = {"knowledge_dir": "~/workspace/knowledge"}
    return _config_cache


def get_knowledge_dir():
    cfg = load_config()
    kd = cfg.get("knowledge_dir", "").strip()
    if not kd:
        kd = "~/workspace/knowledge"
    return os.path.expanduser(kd)


def sync_paths():
    global CONFIG_FILE
    kdir = get_knowledge_dir()
    rag = os.path.join(kdir, ".rag_data")
    CONFIG_FILE = os.path.join(kdir, ".knowledge-config.json")
    idxk.KNOWLEDGE_DIR = kdir
    idxk.RAG_DIR = rag
    idxk.MODEL_META_FILE = os.path.join(rag, "model_meta.json")
    qk.RAG_DIR = rag
    qk.MODEL_META_FILE = os.path.join(rag, "model_meta.json")
    qk.CONFIG_FILE = os.path.join(kdir, ".knowledge-config.json")


# ─── Pydantic 模型 ──────────────────────────────────────

class SearchRequest(BaseModel):
    query: str
    source: str | None = None
    author: str | None = None
    top: int = Field(default=5, ge=1, le=200)


class ReindexRequest(BaseModel):
    force: bool = False
    source_only: str | None = None


# ─── FastAPI 应用 ───────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    sync_paths()
    yield

app = FastAPI(title="知识仓库 API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5777", "http://127.0.0.1:5777"], allow_methods=["*"], allow_headers=["*"])


# ─── API: 搜索 ──────────────────────────────────────────

@app.post("/api/search")
def search(req: SearchRequest):
    sync_paths()
    if not req.query.strip():
        return {"error": "缺少 query 参数"}
    try:
        idxk.build_index(force=False)
        results = qk.search(req.query, top_k=req.top, source=req.source, author=req.author)
        items = []
        for score, c in results:
            items.append({
                "title": c.get("title", ""),
                "author": c.get("author", ""),
                "date": c.get("date", ""),
                "bvid": c.get("bvid", ""),
                "source_type": c.get("source_type", ""),
                "source_label": c.get("source_label", ""),
                "text": c["text"],
                "score": round(float(score), 3),
            })
        return {"results": items}
    except qk.IndexNotFoundError as e:
        return {"error": str(e), "results": []}
    except qk.ModelMismatchError as e:
        return {"error": str(e), "results": []}
    except Exception as e:
        return {"error": str(e)}


# ─── API: 统计 ──────────────────────────────────────────

@app.get("/api/stats")
def stats():
    sync_paths()
    index = {"total_chunks": 0, "source_stats": {}}
    indexed_files = set()
    try:
        conn = idxk._get_db()
        cursor = conn.execute("SELECT source_label, COUNT(*) FROM chunks GROUP BY source_label")
        sources = dict(cursor.fetchall())
        total = sum(sources.values())
        index["total_chunks"] = total
        index["source_stats"] = sources
        cursor = conn.execute("SELECT DISTINCT filename FROM chunks")
        indexed_files = {row[0] for row in cursor}
        conn.close()
    except Exception:
        pass

    files = _list_files(get_knowledge_dir())

    ollama = _check_ollama()

    stored_model, stored_dim = idxk.load_model_meta()
    current_model = qk.get_embed_model()

    return {
        "index": index,
        "files": files,
        "ollama": ollama,
        "indexed_files": list(indexed_files),
        "embed_model": {
            "current": current_model,
            "stored": stored_model,
            "stored_dim": stored_dim,
            "mismatch": stored_model is not None and stored_model != current_model,
        }
    }


# ─── API: 重新索引 ──────────────────────────────────────

@app.post("/api/reindex")
def reindex(req: ReindexRequest = ReindexRequest()):
    sync_paths()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            idxk.build_index(force=req.force, source_only=req.source_only)
            result = {"ok": True}
            conn = idxk._get_db()
            cursor = conn.execute("SELECT COUNT(*) FROM chunks")
            result["chunks"] = cursor.fetchone()[0]
            conn.close()
        except Exception as e:
            result = {"ok": False, "error": str(e)}
    return result


# ─── API: 配置读写 ──────────────────────────────────────

@app.get("/api/config")
def get_config():
    return load_config()


@app.post("/api/config")
def save_config_api(data: dict):
    try:
        if not isinstance(data.get("sources"), list):
            return {"error": "sources 必须是数组"}
        if "knowledge_dir" in data and not isinstance(data.get("knowledge_dir"), str):
            return {"error": "knowledge_dir 必须是字符串"}
        if "embed_model" in data and not isinstance(data.get("embed_model"), str):
            return {"error": "embed_model 必须是字符串"}
        kdir = get_knowledge_dir()
        os.makedirs(kdir, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        global _config_cache, _config_mtime
        _config_cache = None
        _config_mtime = 0
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}


# ─── API: Ollama 状态 ───────────────────────────────────

@app.get("/api/status")
def status():
    return _check_ollama()


# ─── API: 目录浏览 ──────────────────────────────────────

@app.get("/api/browse")
def browse(path: str = Query(default_factory=lambda: os.path.expanduser("~"))):
    p = os.path.expanduser(path)
    if not os.path.exists(p):
        p = os.path.expanduser("~")
    if not os.path.isdir(p):
        p = os.path.dirname(p)
    p = os.path.abspath(p)

    entries = []
    try:
        names = sorted(os.listdir(p))
        for name in names:
            full = os.path.join(p, name)
            if os.path.isdir(full):
                entries.append({"name": name, "type": "dir", "path": full})
    except PermissionError:
        pass

    parent = os.path.dirname(p) if p != "/" else "/"
    return {"current": p, "parent": parent, "entries": entries}


# ─── API: 删除文件索引 ───────────────────────────────────

@app.delete("/api/delete-file")
def delete_file(filename: str = Query(...), source_type: str = None):
    sync_paths()
    conn = idxk._get_db()
    if source_type:
        cursor = conn.execute(
            "DELETE FROM chunks WHERE filename = ? AND source_type = ?",
            (filename, source_type)
        )
    else:
        cursor = conn.execute("DELETE FROM chunks WHERE filename = ?", (filename,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return {"ok": True, "deleted": deleted}


# ─── 内部工具 ──────────────────────────────────────────

def _list_files(root_dir):
    files = []
    if not os.path.isdir(root_dir):
        return files

    cfg = load_config()
    sources = cfg.get("sources", [])

    for src in sources:
        src_dir = os.path.join(root_dir, src)
        if not os.path.isdir(src_dir):
            continue
        label = idxk.SOURCE_MAP.get(src, src)
        for fp in Path(src_dir).glob("*"):
            if not fp.is_file():
                continue
            if not fp.suffix.lower() in (".txt", ".md", ".pdf", ".docx"):
                continue
            try:
                st = fp.stat()
                files.append({
                    "name": fp.name,
                    "dir": label,
                    "size": st.st_size,
                    "path": fp.name,
                })
            except OSError:
                pass
    return files


def _check_ollama():
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=3)
        data = resp.json()
        models = [m["name"] for m in data.get("models", [])]
        current_model = qk.get_embed_model()
        embed_ready = current_model in models
        if not embed_ready:
            for m in models:
                if current_model.startswith(m.split(":")[0]):
                    embed_ready = True
                    break
        return {
            "online": True,
            "models": models,
            "embed_ready": embed_ready,
            "embed_model": current_model,
        }
    except Exception as e:
        return {"online": False, "error": str(e)}


# ─── 启动入口 ───────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8768
    uvicorn.run(app, host="0.0.0.0", port=port)
