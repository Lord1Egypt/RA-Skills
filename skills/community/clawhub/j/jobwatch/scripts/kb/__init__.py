"""KB adapter layer.

入库不写死在流水线里：pipeline 只调用 get_kb().upload_doc(...)。
后端选择：env KB_BACKEND > config.json 的 kb.backend > 默认 local。

- local    零依赖，写 kb_local/ 目录 + index.jsonl（默认）
- twobrain 2brain 知识库（需要 .env 里的 TWOBRAIN_* key）
- aidigest 预留：对接自建 RAG（见模块 docstring）
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def get_kb():
    from common import CONFIG
    backend = os.environ.get("KB_BACKEND") or CONFIG.get("kb", {}).get("backend", "local")
    if backend == "local":
        from . import local
        return local
    if backend == "twobrain":
        from . import twobrain
        return twobrain
    if backend == "aidigest":
        from . import aidigest
        return aidigest
    raise ValueError(f"unknown KB backend: {backend}")
