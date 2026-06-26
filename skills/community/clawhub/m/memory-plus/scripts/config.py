"""
Memory Workflow 配置
"""
import os
from pathlib import Path

# 记忆文件存储目录
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory-workflow-data" / "memories"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

# Rerank 服务
RERANK_SERVICE_URL = os.environ.get("RERANK_SERVICE_URL", "http://172.17.0.1:18778")

# Embedding 配置
EMBEDDING_API = os.environ.get("EMBEDDING_API", "openai")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIM = 1536


def get_memory_files():
    """获取所有记忆文件，按日期倒序"""
    if not MEMORY_DIR.exists():
        return []
    return sorted(MEMORY_DIR.glob("*.md"), reverse=True)
